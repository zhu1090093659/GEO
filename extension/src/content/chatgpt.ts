/**
 * ChatGPT Content Script
 * Captures conversations from chat.openai.com / chatgpt.com
 */

import { ConversationData } from '../types'
import {
  CHATGPT_SELECTORS,
  findElement,
  findAllElements,
} from '../config/selectors'

const SELECTORS = CHATGPT_SELECTORS

// Track processed messages to avoid duplicates
const processedMessages = new Set<string>()

// Debounce timer
let processTimeout: ReturnType<typeof setTimeout> | null = null

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
  const contentElement = findElement(
    element,
    SELECTORS.messageContent,
    SELECTORS.fallbacks?.messageContent
  )
  return contentElement?.textContent?.trim() || element.textContent?.trim() || ''
}

/**
 * Create a hash for deduplication
 */
function hashMessage(query: string, response: string): string {
  return `${query.substring(0, 100)}-${response.substring(0, 100)}`
}

/**
 * Check if response appears complete (not still streaming)
 */
function isResponseComplete(element: Element): boolean {
  // Check for streaming indicators
  const hasStreamingCursor = element.querySelector('.cursor, .typing-indicator, [class*="streaming"]')
  const hasPendingDots = element.textContent?.includes('...')
  
  // If message is very short, might still be streaming
  const text = element.textContent?.trim() || ''
  if (text.length < 10 && hasPendingDots) {
    return false
  }
  
  return !hasStreamingCursor
}

/**
 * Capture a conversation pair (user query + AI response)
 */
function captureConversation(
  userElement: Element,
  assistantElement: Element
): void {
  // Wait for response to complete
  if (!isResponseComplete(assistantElement)) {
    console.log('[GEO] Response still streaming, waiting...')
    return
  }

  const query = extractMessageText(userElement)
  const response = extractMessageText(assistantElement)

  // Skip if empty or too short
  if (!query || !response || response.length < 20) return

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
      language: document.documentElement.lang || navigator.language || undefined,
    },
  }

  // Send to background script
  chrome.runtime.sendMessage({
    type: 'CONVERSATION_CAPTURED',
    data,
  }).catch(err => {
    console.error('[GEO] Failed to send message:', err)
  })

  console.log('[GEO] Captured ChatGPT conversation', {
    queryPreview: query.substring(0, 50),
    responseLength: response.length,
  })
}

/**
 * Process all visible conversations on the page
 */
function processConversations(): void {
  // Find all message turns
  const turns = findAllElements(
    document,
    SELECTORS.messageTurn,
    ['[data-testid*="conversation"]', '[class*="message-group"]']
  )

  if (turns.length === 0) {
    // Try alternative: look for messages directly
    const userMessages = findAllElements(
      document,
      SELECTORS.userMessage,
      SELECTORS.fallbacks?.userMessage
    )
    const assistantMessages = findAllElements(
      document,
      SELECTORS.assistantMessage,
      SELECTORS.fallbacks?.assistantMessage
    )

    console.log(`[GEO] Found ${userMessages.length} user messages, ${assistantMessages.length} assistant messages`)

    // Pair up messages
    const minLength = Math.min(userMessages.length, assistantMessages.length)
    for (let i = 0; i < minLength; i++) {
      captureConversation(userMessages[i], assistantMessages[i])
    }
    return
  }

  console.log(`[GEO] Found ${turns.length} conversation turns`)

  // Process turns looking for user-assistant pairs
  for (let i = 0; i < turns.length; i++) {
    const turn = turns[i]
    const userMsg = findElement(turn, SELECTORS.userMessage, SELECTORS.fallbacks?.userMessage)
    
    // Look for assistant message in next turn or same turn
    let assistantMsg = findElement(turn, SELECTORS.assistantMessage, SELECTORS.fallbacks?.assistantMessage)
    if (!assistantMsg && turns[i + 1]) {
      assistantMsg = findElement(turns[i + 1], SELECTORS.assistantMessage, SELECTORS.fallbacks?.assistantMessage)
    }

    if (userMsg && assistantMsg) {
      captureConversation(userMsg, assistantMsg)
    }
  }
}

/**
 * Debounced process function
 */
function debouncedProcess(): void {
  if (processTimeout) {
    clearTimeout(processTimeout)
  }
  processTimeout = setTimeout(processConversations, 1500)
}

/**
 * Set up MutationObserver to watch for new messages
 */
function setupObserver(): void {
  const observer = new MutationObserver((mutations) => {
    // Check if meaningful content was added
    let hasNewContent = false
    for (const mutation of mutations) {
      if (mutation.addedNodes.length > 0) {
        for (const node of mutation.addedNodes) {
          if (node.nodeType === Node.ELEMENT_NODE) {
            hasNewContent = true
            break
          }
        }
      }
      if (hasNewContent) break
    }

    if (hasNewContent) {
      debouncedProcess()
    }
  })

  // Start observing
  observer.observe(document.body, {
    childList: true,
    subtree: true,
  })

  console.log('[GEO] ChatGPT observer initialized')
}

/**
 * Debug function to log found selectors
 */
function debugSelectors(): void {
  console.log('[GEO] Debugging ChatGPT selectors...')
  
  const tests = [
    { name: 'messageTurn', sel: SELECTORS.messageTurn },
    { name: 'userMessage', sel: SELECTORS.userMessage },
    { name: 'assistantMessage', sel: SELECTORS.assistantMessage },
    { name: 'messageContent', sel: SELECTORS.messageContent },
  ]

  for (const test of tests) {
    const found = document.querySelectorAll(test.sel)
    console.log(`[GEO] ${test.name} (${test.sel}): ${found.length} found`)
  }
}

// Initialize
function init(): void {
  // Wait for page to load
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      setupObserver()
      debugSelectors()
      setTimeout(processConversations, 2000)
    })
  } else {
    setupObserver()
    debugSelectors()
    setTimeout(processConversations, 2000)
  }
}

init()
