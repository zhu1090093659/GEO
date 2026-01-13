/**
 * GEO Extension Background Service Worker
 * Handles message passing and data upload coordination
 */

import { ConversationData, UploadQueue } from './types'
import { ApiClient } from './utils/api'
import { Sanitizer } from './utils/sanitizer'

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

// Listen for messages from content scripts
chrome.runtime.onMessage.addListener((message, _sender, sendResponse) => {
  if (message.type === 'CONVERSATION_CAPTURED') {
    handleConversationCapture(message.data)
    sendResponse({ success: true })
  } else if (message.type === 'GET_STATUS') {
    sendResponse({
      isEnabled: true,
      queueSize: uploadQueue.items.length,
    })
  }
  return true // Keep message channel open for async response
})

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
  
  const batch = uploadQueue.items.splice(0, BATCH_SIZE)
  
  try {
    await api.uploadConversations(batch)
    uploadQueue.lastUpload = Date.now()
    console.log(`[GEO] Uploaded ${batch.length} conversations`)
  } catch (error) {
    // Put items back in queue on failure
    uploadQueue.items.unshift(...batch)
    console.error('[GEO] Upload failed, will retry:', error)
  }
}

// Periodic upload check
setInterval(uploadBatch, UPLOAD_INTERVAL)

// Log initialization
console.log('[GEO] Background service worker initialized')
