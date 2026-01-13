import { defineConfig } from 'vite'
import { resolve } from 'path'

export default defineConfig({
  build: {
    outDir: 'dist',
    rollupOptions: {
      input: {
        background: resolve(__dirname, 'src/background.ts'),
        'content/chatgpt': resolve(__dirname, 'src/content/chatgpt.ts'),
        'content/claude': resolve(__dirname, 'src/content/claude.ts'),
        'popup/popup': resolve(__dirname, 'src/popup/popup.ts'),
        'popup/consent': resolve(__dirname, 'src/popup/consent.ts'),
        'popup/preview': resolve(__dirname, 'src/popup/preview.ts'),
      },
      output: {
        entryFileNames: '[name].js',
        chunkFileNames: 'chunks/[name]-[hash].js',
      },
    },
    sourcemap: true,
    emptyOutDir: true,
  },
})
