/**
 * DOM Selectors Configuration
 * 
 * These selectors may need updates when AI platforms change their UI.
 * To update selectors:
 * 1. Open the target platform in Chrome
 * 2. Use DevTools (F12) to inspect the conversation area
 * 3. Find the correct selectors for user/assistant messages
 * 4. Update the relevant platform config below
 * 
 * Last verified: 2026-01-13
 */

export interface PlatformSelectors {
  /** Container for the entire conversation */
  conversationContainer: string
  /** Individual message turn/block */
  messageTurn: string
  /** User message element */
  userMessage: string
  /** Assistant/AI message element */
  assistantMessage: string
  /** Text content within a message */
  messageContent: string
  /** Alternative selectors to try if primary fails */
  fallbacks?: {
    userMessage?: string[]
    assistantMessage?: string[]
    messageContent?: string[]
  }
}

/**
 * ChatGPT Selectors (chat.openai.com, chatgpt.com)
 * 
 * ChatGPT uses React with data-testid and data-message-author-role attributes
 */
export const CHATGPT_SELECTORS: PlatformSelectors = {
  conversationContainer: '[role="presentation"]',
  messageTurn: '[data-testid^="conversation-turn"]',
  userMessage: '[data-message-author-role="user"]',
  assistantMessage: '[data-message-author-role="assistant"]',
  messageContent: '.markdown, .prose, [data-message-text="true"]',
  fallbacks: {
    userMessage: [
      '[data-testid="user-message"]',
      '.user-message',
      '[class*="user"]',
    ],
    assistantMessage: [
      '[data-testid="assistant-message"]',
      '.assistant-message',
      '[class*="assistant"]',
    ],
    messageContent: [
      '.text-base',
      '.whitespace-pre-wrap',
      '[class*="markdown"]',
    ],
  },
}

/**
 * Claude Selectors (claude.ai)
 * 
 * Claude uses a different structure with human/assistant naming
 */
export const CLAUDE_SELECTORS: PlatformSelectors = {
  conversationContainer: '[data-testid="conversation"]',
  messageTurn: '[data-testid*="message"]',
  userMessage: '[data-testid="human-message"], [data-testid="user-message"]',
  assistantMessage: '[data-testid="assistant-message"], [data-testid="ai-message"]',
  messageContent: '.prose, .font-claude-message, [class*="message-content"]',
  fallbacks: {
    userMessage: [
      '[class*="human"]',
      '[class*="user"]',
    ],
    assistantMessage: [
      '[class*="assistant"]',
      '[class*="claude"]',
    ],
    messageContent: [
      'p',
      '.text-content',
    ],
  },
}

/**
 * Try to find element using primary selector, then fallbacks
 */
export function findElement(
  root: Element | Document,
  primarySelector: string,
  fallbacks?: string[]
): Element | null {
  // Try primary selector
  let element = root.querySelector(primarySelector)
  if (element) return element

  // Try fallbacks
  if (fallbacks) {
    for (const selector of fallbacks) {
      element = root.querySelector(selector)
      if (element) {
        console.log(`[GEO] Using fallback selector: ${selector}`)
        return element
      }
    }
  }

  return null
}

/**
 * Find all elements using primary selector, then fallbacks
 */
export function findAllElements(
  root: Element | Document,
  primarySelector: string,
  fallbacks?: string[]
): Element[] {
  // Try primary selector
  let elements = Array.from(root.querySelectorAll(primarySelector))
  if (elements.length > 0) return elements

  // Try fallbacks
  if (fallbacks) {
    for (const selector of fallbacks) {
      elements = Array.from(root.querySelectorAll(selector))
      if (elements.length > 0) {
        console.log(`[GEO] Using fallback selector: ${selector}`)
        return elements
      }
    }
  }

  return []
}
