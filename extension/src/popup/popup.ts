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
  chrome.runtime.sendMessage(
    { type: 'SET_ENABLED', enabled: !isEnabled },
    (response) => {
      if (response?.success) {
        updateUI(!isEnabled)
      }
    }
  )
}

/**
 * Get current status from background
 */
async function getStatus(): Promise<void> {
  chrome.runtime.sendMessage({ type: 'GET_STATUS' }, (response) => {
    if (response) {
      updateUI(response.isEnabled, response.queueSize)
    }
  })
}

// Event listeners
toggleBtn.addEventListener('click', toggleCollection)

// Initialize
getStatus()
