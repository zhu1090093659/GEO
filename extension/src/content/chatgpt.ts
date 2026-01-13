/**
 * ChatGPT Content Script
 * Captures conversations from chat.openai.com / chatgpt.com
 */

import { ConversationData } from '../types'

// Selectors for ChatGPT DOM elements (may need updates as UI changes)
const SELECTORS = {
  // Message container
  messageContainer: '[data-testid="conversation-turn"]',
  // User message
  userMessage: '[data-message-author-role="user"]',
  // Assistant message
  assistantMessage: '[data-message-author-role="assistant"]',
  // Message content
  messageContent: '.markdown',
}

// Track processed messages to avoid duplicates
const processedMessages = new Set<string>()

/**
 * Generate unique ID for a conversation
 */
function generateId(): string {
  return `chatgpt-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
}

/**
 * Extract text content from message element
 */
function extractMessageText(element: Element): string {
  const contentElement = element.querySelector(SELECTORS.messageContent)
  return contentElement?.textContent?.trim() || ''
}

/**
 * Create a hash for deduplication
 */
function hashMessage(query: string, response: string): string {
  return `${query.substring(0, 50)}-${response.substring(0, 50)}`
}

/**
 * Capture a conversation pair (user query + AI response)
 */
function captureConversation(
  userElement: Element,
  assistantElement: Element
): void {
  const query = extractMessageText(userElement)
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
    platform: 'chatgpt',
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

  console.log('[GEO] Captured ChatGPT conversation')
}

/**
 * Process all visible conversations on the page
 */
function processConversations(): void {
  const turns = document.querySelectorAll(SELECTORS.messageContainer)
  
  for (let i = 0; i < turns.length - 1; i++) {
    const userMsg = turns[i].querySelector(SELECTORS.userMessage)
    const assistantMsg = turns[i + 1]?.querySelector(SELECTORS.assistantMessage)
    
    if (userMsg && assistantMsg) {
      captureConversation(userMsg, assistantMsg)
    }
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

  console.log('[GEO] ChatGPT observer initialized')
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
