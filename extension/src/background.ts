/**
 * GEO Extension Background Service Worker
 * Handles message passing and data upload coordination
 */

import { ConversationData, UploadQueue, ExtensionSettings } from './types'
import { ApiClient } from './utils/api'
import { Sanitizer } from './utils/sanitizer'

// Storage keys
const STORAGE_KEYS = {
  consent: 'geo_consent',
  settings: 'geo_settings',
}

// Default settings
const DEFAULT_SETTINGS: ExtensionSettings = {
  isEnabled: true,
  hasConsented: false,
  apiUrl: 'http://localhost:8000/api',
}

// Upload queue for batching requests
const uploadQueue: UploadQueue = {
  items: [],
  lastUpload: Date.now(),
}

const BATCH_SIZE = 10
const UPLOAD_INTERVAL = 30000 // 30 seconds

// Initialize API client
const api = new ApiClient()
const sanitizer = new Sanitizer()

// Current settings state
let currentSettings: ExtensionSettings = { ...DEFAULT_SETTINGS }

/**
 * Load settings from storage
 */
async function loadSettings(): Promise<ExtensionSettings> {
  const result = await chrome.storage.local.get([STORAGE_KEYS.consent, STORAGE_KEYS.settings])
  
  const consent = result[STORAGE_KEYS.consent]
  const settings = result[STORAGE_KEYS.settings] || {}
  
  currentSettings = {
    ...DEFAULT_SETTINGS,
    ...settings,
    hasConsented: consent?.hasConsented || false,
  }
  
  return currentSettings
}

/**
 * Save settings to storage
 */
async function saveSettings(settings: Partial<ExtensionSettings>): Promise<void> {
  currentSettings = { ...currentSettings, ...settings }
  await chrome.storage.local.set({ [STORAGE_KEYS.settings]: currentSettings })
}

/**
 * Check if data collection is allowed
 */
function isCollectionAllowed(): boolean {
  return currentSettings.isEnabled && currentSettings.hasConsented
}

// Listen for messages from content scripts and popup
chrome.runtime.onMessage.addListener((message, _sender, sendResponse) => {
  handleMessage(message).then(sendResponse)
  return true // Keep message channel open for async response
})

/**
 * Handle incoming messages
 */
async function handleMessage(message: { type: string; [key: string]: unknown }): Promise<unknown> {
  switch (message.type) {
    case 'CONVERSATION_CAPTURED':
      if (isCollectionAllowed()) {
        await handleConversationCapture(message.data as ConversationData)
        return { success: true }
      }
      return { success: false, reason: 'Collection not allowed' }
    
    case 'GET_STATUS':
      return {
        isEnabled: currentSettings.isEnabled,
        hasConsented: currentSettings.hasConsented,
        queueSize: uploadQueue.items.length,
      }
    
    case 'SET_ENABLED':
      await saveSettings({ isEnabled: message.enabled as boolean })
      return { success: true }
    
    case 'CONSENT_UPDATED':
      currentSettings.hasConsented = message.consented as boolean
      return { success: true }
    
    case 'GET_SETTINGS':
      return currentSettings
    
    case 'GET_QUEUE_DATA':
      return { items: uploadQueue.items }
    
    case 'CLEAR_QUEUE':
      uploadQueue.items = []
      return { success: true }
    
    default:
      return { error: 'Unknown message type' }
  }
}

/**
 * Handle captured conversation data
 */
async function handleConversationCapture(data: ConversationData): Promise<void> {
  // Sanitize data to remove PII
  const sanitizedData = sanitizer.sanitize(data)
  
  // Add to upload queue
  uploadQueue.items.push(sanitizedData)
  
  // Upload if batch size reached or interval passed
  if (
    uploadQueue.items.length >= BATCH_SIZE ||
    Date.now() - uploadQueue.lastUpload > UPLOAD_INTERVAL
  ) {
    await uploadBatch()
  }
}

/**
 * Upload batched data to backend
 */
async function uploadBatch(): Promise<void> {
  if (uploadQueue.items.length === 0) return
  if (!isCollectionAllowed()) return
  
  const batch = uploadQueue.items.splice(0, BATCH_SIZE)
  
  try {
    const result = await api.uploadConversations(batch)
    if (result.success) {
      uploadQueue.lastUpload = Date.now()
      console.log(`[GEO] Uploaded ${batch.length} conversations`)
    } else {
      throw new Error(result.error)
    }
  } catch (error) {
    // Put items back in queue on failure
    uploadQueue.items.unshift(...batch)
    console.error('[GEO] Upload failed, will retry:', error)
  }
}

/**
 * Check consent on extension install/update
 */
chrome.runtime.onInstalled.addListener(async (details) => {
  await loadSettings()
  
  if (details.reason === 'install') {
    // First install - open consent page
    chrome.tabs.create({ url: 'popup/consent.html' })
    console.log('[GEO] Extension installed, showing consent page')
  } else if (details.reason === 'update') {
    console.log('[GEO] Extension updated to version', chrome.runtime.getManifest().version)
  }
})

// Periodic upload check
setInterval(uploadBatch, UPLOAD_INTERVAL)

// Initialize on startup
loadSettings().then(() => {
  console.log('[GEO] Background service worker initialized', {
    hasConsented: currentSettings.hasConsented,
    isEnabled: currentSettings.isEnabled,
  })
})
