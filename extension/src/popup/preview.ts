/**
 * Data Preview Script
 * Shows queued data waiting for upload
 */

interface PreviewData {
  id: string
  query: string
  response: string
  platform: string
  timestamp: string
}

// DOM Elements
const dataList = document.getElementById('data-list') as HTMLElement
const emptyState = document.getElementById('empty-state') as HTMLElement
const queueCount = document.getElementById('queue-count') as HTMLElement
const clearBtn = document.getElementById('clear-btn') as HTMLButtonElement
const backBtn = document.getElementById('back-btn') as HTMLButtonElement

/**
 * Format timestamp for display
 */
function formatTime(isoString: string): string {
  try {
    const date = new Date(isoString)
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  } catch {
    return 'Unknown'
  }
}

/**
 * Truncate text with ellipsis
 */
function truncate(text: string, maxLength: number = 150): string {
  if (text.length <= maxLength) return text
  return text.substring(0, maxLength) + '...'
}

/**
 * Create HTML for a data item
 */
function createDataItemHTML(item: PreviewData): string {
  const platformClass = item.platform === 'chatgpt' ? 'platform-chatgpt' : 'platform-claude'
  
  return `
    <div class="data-item">
      <div class="data-header">
        <span class="platform-badge ${platformClass}">${item.platform}</span>
        <span class="timestamp">${formatTime(item.timestamp)}</span>
      </div>
      <div class="data-field">
        <div class="field-label">Query</div>
        <div class="field-content">${truncate(item.query)}</div>
      </div>
      <div class="data-field">
        <div class="field-label">Response</div>
        <div class="field-content">${truncate(item.response, 200)}</div>
      </div>
    </div>
  `
}

/**
 * Render the data list
 */
function renderDataList(items: PreviewData[]): void {
  if (items.length === 0) {
    emptyState.style.display = 'block'
    clearBtn.disabled = true
    queueCount.textContent = '0 items'
    return
  }
  
  emptyState.style.display = 'none'
  clearBtn.disabled = false
  queueCount.textContent = `${items.length} item${items.length > 1 ? 's' : ''}`
  
  // Remove empty state and render items
  dataList.innerHTML = items.map(createDataItemHTML).join('')
}

/**
 * Get queued data from background
 */
async function getQueuedData(): Promise<PreviewData[]> {
  const response = await chrome.runtime.sendMessage({ type: 'GET_QUEUE_DATA' })
  return response?.items || []
}

/**
 * Clear the queue
 */
async function clearQueue(): Promise<void> {
  await chrome.runtime.sendMessage({ type: 'CLEAR_QUEUE' })
  renderDataList([])
}

/**
 * Load and display data
 */
async function loadData(): Promise<void> {
  const items = await getQueuedData()
  renderDataList(items)
}

// Event listeners
backBtn?.addEventListener('click', () => {
  window.location.href = 'popup.html'
})

clearBtn?.addEventListener('click', async () => {
  if (confirm('Are you sure you want to clear all queued data?')) {
    await clearQueue()
  }
})

// Initialize
loadData()
