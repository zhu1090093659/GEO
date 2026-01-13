/**
 * Claude Content Script
 * Captures conversations from claude.ai
 */

import { ConversationData } from '../types'

// Selectors for Claude DOM elements (may need updates as UI changes)
const SELECTORS = {
  // Conversation container
  conversationContainer: '[data-testid="conversation"]',
  // Human message (user)
  humanMessage: '[data-testid="human-message"]',
  // Assistant message (Claude)
  assistantMessage: '[data-testid="assistant-message"]',
  // Message content wrapper
  messageContent: '.prose',
}

// Track processed messages to avoid duplicates
const processedMessages = new Set<string>()

/**
 * Generate unique ID for a conversation
 */
function generateId(): string {
  return `claude-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
}

/**
 * Extract text content from message element
 */
function extractMessageText(element: Element): string {
  const contentElement = element.querySelector(SELECTORS.messageContent)
  return contentElement?.textContent?.trim() || element.textContent?.trim() || ''
}

/**
 * Create a hash for deduplication
 */
function hashMessage(query: string, response: string): string {
  return `${query.substring(0, 50)}-${response.substring(0, 50)}`
}

/**
 * Capture a conversation pair (user query + Claude response)
 */
function captureConversation(
  humanElement: Element,
  assistantElement: Element
): void {
  const query = extractMessageText(humanElement)
  const response = extractMessageText(assistantElement)

  // Skip if empty
  if (!query || !response) return

  // Skip if already processed
  const hash = hashMessage(query, response)
  if (processedMessages.has(hash)) return
  processedMessages.add(hash)

  const data: ConversationData = {
    id: generateId(),
    query,
    response,
    platform: 'claude',
    timestamp: new Date().toISOString(),
    metadata: {
      language: document.documentElement.lang || undefined,
    },
  }

  // Send to background script
  chrome.runtime.sendMessage({
    type: 'CONVERSATION_CAPTURED',
    data,
  })

  console.log('[GEO] Captured Claude conversation')
}

/**
 * Process all visible conversations on the page
 */
function processConversations(): void {
  const humanMessages = document.querySelectorAll(SELECTORS.humanMessage)
  const assistantMessages = document.querySelectorAll(SELECTORS.assistantMessage)
  
  // Pair up human and assistant messages
  const minLength = Math.min(humanMessages.length, assistantMessages.length)
  
  for (let i = 0; i < minLength; i++) {
    captureConversation(humanMessages[i], assistantMessages[i])
  }
}

/**
 * Set up MutationObserver to watch for new messages
 */
function setupObserver(): void {
  const observer = new MutationObserver((mutations) => {
    // Check if new messages were added
    for (const mutation of mutations) {
      if (mutation.addedNodes.length > 0) {
        // Debounce processing to wait for streaming to complete
        setTimeout(processConversations, 1000)
        break
      }
    }
  })

  // Start observing
  const targetNode = document.body
  observer.observe(targetNode, {
    childList: true,
    subtree: true,
  })

  console.log('[GEO] Claude observer initialized')
}

// Initialize
function init(): void {
  // Wait for page to load
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      setupObserver()
      processConversations()
    })
  } else {
    setupObserver()
    processConversations()
  }
}

init()
