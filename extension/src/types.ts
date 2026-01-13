/**
 * GEO Extension Type Definitions
 */

/**
 * Captured conversation data from AI platforms
 */
export interface ConversationData {
  /** Unique identifier for this conversation */
  id: string
  /** User's query/prompt */
  query: string
  /** AI's response */
  response: string
  /** Platform identifier (chatgpt, claude) */
  platform: 'chatgpt' | 'claude'
  /** ISO timestamp when captured */
  timestamp: string
  /** Optional conversation metadata */
  metadata?: {
    /** Detected language */
    language?: string
    /** User's region (from browser) */
    region?: string
    /** Model used (if detectable) */
    model?: string
  }
}

/**
 * Upload queue for batching API requests
 */
export interface UploadQueue {
  /** Queued items waiting for upload */
  items: ConversationData[]
  /** Timestamp of last upload */
  lastUpload: number
}

/**
 * Extension settings stored in chrome.storage
 */
export interface ExtensionSettings {
  /** Is data collection enabled */
  isEnabled: boolean
  /** Has user consented to data collection */
  hasConsented: boolean
  /** Backend API URL */
  apiUrl: string
  /** User's tracked brands (optional) */
  trackedBrands?: string[]
}

/**
 * Message types for communication between scripts
 */
export type MessageType =
  | { type: 'CONVERSATION_CAPTURED'; data: ConversationData }
  | { type: 'GET_STATUS' }
  | { type: 'SET_ENABLED'; enabled: boolean }
  | { type: 'GET_SETTINGS' }

/**
 * API response types
 */
export interface ApiResponse<T = unknown> {
  success: boolean
  data?: T
  error?: string
}

/**
 * Upload response from backend
 */
export interface UploadResponse {
  received: number
  processed: number
}
