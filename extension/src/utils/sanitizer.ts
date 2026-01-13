/**
 * Data Sanitizer for PII removal
 */

import { ConversationData } from '../types'

// Patterns for PII detection
const PII_PATTERNS = {
  // Email addresses
  email: /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g,
  // Phone numbers (various formats)
  phone: /(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}/g,
  // Credit card numbers (basic pattern)
  creditCard: /\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b/g,
  // SSN (US format)
  ssn: /\b\d{3}[-\s]?\d{2}[-\s]?\d{4}\b/g,
  // IP addresses
  ipAddress: /\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b/g,
}

// Replacement text for sanitized content
const SANITIZED_TEXT = '[REDACTED]'

export class Sanitizer {
  /**
   * Sanitize conversation data by removing PII
   */
  sanitize(data: ConversationData): ConversationData {
    return {
      ...data,
      query: this.sanitizeText(data.query),
      response: this.sanitizeText(data.response),
    }
  }

  /**
   * Sanitize a text string by removing PII patterns
   */
  private sanitizeText(text: string): string {
    let sanitized = text

    // Apply all PII patterns
    for (const pattern of Object.values(PII_PATTERNS)) {
      sanitized = sanitized.replace(pattern, SANITIZED_TEXT)
    }

    return sanitized
  }

  /**
   * Check if text contains potential PII
   */
  containsPII(text: string): boolean {
    for (const pattern of Object.values(PII_PATTERNS)) {
      if (pattern.test(text)) {
        // Reset regex lastIndex for reuse
        pattern.lastIndex = 0
        return true
      }
    }
    return false
  }
}
