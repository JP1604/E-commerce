import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@domain': path.resolve(__dirname, './src/domain'),
      '@application': path.resolve(__dirname, './src/application'),
      '@infrastructure': path.resolve(__dirname, './src/infrastructure'),
      '@presentation': path.resolve(__dirname, './src/presentation'),
    },
  },
  server: {
    port: 3000,
    proxy: {
      '/api/v1/products': {
        target: 'http://localhost:30000',
        changeOrigin: true,
      },
      '/api/v1/carts': {
        target: 'http://localhost:30003',
        changeOrigin: true,
      },
      '/api/v1/users': {
        target: 'http://localhost:30001',
        changeOrigin: true,
      },
      '/api': {
        target: 'http://localhost:30000',
        changeOrigin: true,
      },
    },
  },
})
