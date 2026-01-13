# GEO Browser Extension

Chrome extension for capturing AI conversation data.

## Development

```bash
# Install dependencies
npm install

# Build extension
npm run build

# Watch mode for development
npm run dev
```

## Installation (Development)

1. Build the extension: `npm run build`
2. Open Chrome and go to `chrome://extensions/`
3. Enable "Developer mode"
4. Click "Load unpacked" and select the `extension` folder

## Structure

```
extension/
├── manifest.json          # Extension manifest (v3)
├── src/
│   ├── background.ts      # Service worker
│   ├── types.ts           # TypeScript types
│   ├── content/
│   │   ├── chatgpt.ts     # ChatGPT content script
│   │   └── claude.ts      # Claude content script
│   ├── popup/
│   │   ├── popup.html     # Popup UI
│   │   └── popup.ts       # Popup logic
│   └── utils/
│       ├── api.ts         # Backend API client
│       └── sanitizer.ts   # PII sanitization
├── icons/                 # Extension icons (add your own)
└── dist/                  # Built output
```

## Icons

You need to add the following icon files to the `icons/` folder:

- `icon16.png` (16x16)
- `icon32.png` (32x32)
- `icon48.png` (48x48)
- `icon128.png` (128x128)

## Supported Platforms

- ChatGPT (chat.openai.com, chatgpt.com)
- Claude (claude.ai)

## Privacy

The extension sanitizes all captured data to remove PII before uploading:
- Email addresses
- Phone numbers
- Credit card numbers
- SSN
- IP addresses
