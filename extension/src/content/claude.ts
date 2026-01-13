/**
 * Claude Content Script
 * Captures conversations from claude.ai
 */

import { ConversationData } from '../types'
import {
  CLAUDE_SELECTORS,
  findElement,
  findAllElements,
} from '../config/selectors'

const SELECTORS = CLAUDE_SELECTORS

// Track processed messages to avoid duplicates
const processedMessages = new Set<string>()

// Debounce timer
let processTimeout: ReturnType<typeof setTimeout> | null = null

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
  
  // If message is very short, might still be streaming
  const text = element.textContent?.trim() || ''
  if (text.length < 10) {
    return false
  }
  
  return !hasStreamingCursor
}

/**
 * Capture a conversation pair (user query + Claude response)
 */
function captureConversation(
  humanElement: Element,
  assistantElement: Element
): void {
  // Wait for response to complete
  if (!isResponseComplete(assistantElement)) {
    console.log('[GEO] Response still streaming, waiting...')
    return
  }

  const query = extractMessageText(humanElement)
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
    platform: 'claude',
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

  console.log('[GEO] Captured Claude conversation', {
    queryPreview: query.substring(0, 50),
    responseLength: response.length,
  })
}

/**
 * Process all visible conversations on the page
 */
function processConversations(): void {
  // Find user and assistant messages
  const humanMessages = findAllElements(
    document,
    SELECTORS.userMessage,
    SELECTORS.fallbacks?.userMessage
  )
  const assistantMessages = findAllElements(
    document,
    SELECTORS.assistantMessage,
    SELECTORS.fallbacks?.assistantMessage
  )

  console.log(`[GEO] Found ${humanMessages.length} human messages, ${assistantMessages.length} assistant messages`)

  // Pair up human and assistant messages
  const minLength = Math.min(humanMessages.length, assistantMessages.length)

  for (let i = 0; i < minLength; i++) {
    captureConversation(humanMessages[i], assistantMessages[i])
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

  console.log('[GEO] Claude observer initialized')
}

/**
 * Debug function to log found selectors
 */
function debugSelectors(): void {
  console.log('[GEO] Debugging Claude selectors...')
  
  const tests = [
    { name: 'conversationContainer', sel: SELECTORS.conversationContainer },
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
