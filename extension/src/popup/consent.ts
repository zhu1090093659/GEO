/**
 * Consent Popup Script
 * Handles user consent for data collection
 */

const STORAGE_KEY = 'geo_consent'

interface ConsentData {
  hasConsented: boolean
  consentedAt: string | null
  version: string
}

const CONSENT_VERSION = '1.0'

/**
 * Save consent status to storage
 */
async function saveConsent(consented: boolean): Promise<void> {
  const data: ConsentData = {
    hasConsented: consented,
    consentedAt: consented ? new Date().toISOString() : null,
    version: CONSENT_VERSION,
  }
  
  await chrome.storage.local.set({ [STORAGE_KEY]: data })
}

/**
 * Handle accept button click
 */
async function handleAccept(): Promise<void> {
  await saveConsent(true)
  
  // Notify background script
  chrome.runtime.sendMessage({ type: 'CONSENT_UPDATED', consented: true })
  
  // Close this popup and open main popup
  window.location.href = 'popup.html'
}

/**
 * Handle decline button click
 */
async function handleDecline(): Promise<void> {
  await saveConsent(false)
  
  // Notify background script
  chrome.runtime.sendMessage({ type: 'CONSENT_UPDATED', consented: false })
  
  // Show declined message briefly then close
  document.body.innerHTML = `
    <div style="padding: 40px; text-align: center; color: #a0aec0;">
      <p style="margin-bottom: 16px;">Data collection is disabled.</p>
      <p style="font-size: 12px;">You can enable it later from the extension popup.</p>
    </div>
  `
  
  setTimeout(() => window.close(), 2000)
}

// Event listeners
document.getElementById('accept-btn')?.addEventListener('click', handleAccept)
document.getElementById('decline-btn')?.addEventListener('click', handleDecline)
document.getElementById('privacy-link')?.addEventListener('click', (e) => {
  e.preventDefault()
  // Open privacy policy in new tab
  chrome.tabs.create({ url: 'http://localhost:3000/privacy' })
})
