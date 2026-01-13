/**
 * API Client for communicating with GEO backend
 */

import { ConversationData, ApiResponse, UploadResponse } from '../types'

const DEFAULT_API_URL = 'http://localhost:8000/api'

export class ApiClient {
  private baseUrl: string

  constructor(baseUrl: string = DEFAULT_API_URL) {
    this.baseUrl = baseUrl
  }

  /**
   * Upload batch of conversations to backend
   */
  async uploadConversations(
    conversations: ConversationData[]
  ): Promise<ApiResponse<UploadResponse>> {
    try {
      const response = await fetch(`${this.baseUrl}/tracking/upload`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ conversations }),
      })

      if (!response.ok) {
        throw new Error(`HTTP error: ${response.status}`)
      }

      const data = await response.json()
      return { success: true, data }
    } catch (error) {
      console.error('[GEO API] Upload failed:', error)
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error',
      }
    }
  }

  /**
   * Check backend health
   */
  async healthCheck(): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseUrl}/health`)
      return response.ok
    } catch {
      return false
    }
  }

  /**
   * Update base URL (for settings changes)
   */
  setBaseUrl(url: string): void {
    this.baseUrl = url
  }
}
