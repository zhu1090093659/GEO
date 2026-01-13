/**
 * Popup Script - Extension popup UI logic
 */

// DOM Elements
const statusIndicator = document.getElementById('status-indicator') as HTMLElement
const statusText = document.getElementById('status-text') as HTMLElement
const toggleBtn = document.getElementById('toggle-btn') as HTMLButtonElement
const queueCount = document.getElementById('queue-count') as HTMLElement

// State
let isEnabled = true
let hasConsented = false

/**
 * Check if user has consented
 */
async function checkConsent(): Promise<boolean> {
  const response = await chrome.runtime.sendMessage({ type: 'GET_STATUS' })
  return response?.hasConsented || false
}

/**
 * Redirect to consent page if not consented
 */
async function ensureConsent(): Promise<void> {
  hasConsented = await checkConsent()
  if (!hasConsented) {
    window.location.href = 'consent.html'
  }
}

/**
 * Update UI based on current state
 */
function updateUI(enabled: boolean, queueSize: number = 0): void {
  isEnabled = enabled
  
  if (enabled) {
    statusIndicator.classList.remove('bg-red-500')
    statusIndicator.classList.add('bg-green-500')
    statusText.textContent = 'Active'
    toggleBtn.textContent = 'Pause Collection'
    toggleBtn.classList.remove('bg-green-600', 'hover:bg-green-700')
    toggleBtn.classList.add('bg-red-600', 'hover:bg-red-700')
  } else {
    statusIndicator.classList.remove('bg-green-500')
    statusIndicator.classList.add('bg-red-500')
    statusText.textContent = 'Paused'
    toggleBtn.textContent = 'Resume Collection'
    toggleBtn.classList.remove('bg-red-600', 'hover:bg-red-700')
    toggleBtn.classList.add('bg-green-600', 'hover:bg-green-700')
  }
  
  queueCount.textContent = queueSize.toString()
}

/**
 * Toggle data collection on/off
 */
async function toggleCollection(): Promise<void> {
  const newState = !isEnabled
  const response = await chrome.runtime.sendMessage({
    type: 'SET_ENABLED',
    enabled: newState,
  })
  
  if (response?.success) {
    updateUI(newState)
  }
}

/**
 * Get current status from background
 */
async function getStatus(): Promise<void> {
  const response = await chrome.runtime.sendMessage({ type: 'GET_STATUS' })
  if (response) {
    hasConsented = response.hasConsented
    updateUI(response.isEnabled, response.queueSize)
  }
}

// Event listeners
toggleBtn?.addEventListener('click', toggleCollection)

// Preview button
document.getElementById('preview-btn')?.addEventListener('click', () => {
  window.location.href = 'preview.html'
})

// Initialize
async function init(): Promise<void> {
  await ensureConsent()
  await getStatus()
}

init()
