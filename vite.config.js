import { fileURLToPath, URL } from 'node:url'
import { readFileSync, writeFileSync } from 'fs'
import { resolve } from 'path'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import tailwindcss from '@tailwindcss/vite'

// Плагин для исправления путей в index.html после сборки
function fixIndexHtmlPaths() {
  return {
    name: 'fix-index-html-paths',
    closeBundle() {
      const baseUrl = process.env.BASE_URL || '/'
      if (baseUrl === '/') return // Не нужно исправлять для корневого пути

      const distIndexPath = resolve(__dirname, 'dist/index.html')
      try {
        let html = readFileSync(distIndexPath, 'utf-8')
        // Заменяем абсолютные пути на пути с base URL (только для href и src, которые начинаются с /)
        // Но не трогаем пути, которые уже содержат base URL
        const baseUrlNoSlash = baseUrl.replace(/\/$/, '')
        html = html.replace(/(href|src)="\/(?!\/)/g, `$1="${baseUrlNoSlash}/`)
        writeFileSync(distIndexPath, html, 'utf-8')
        console.log('Исправлены пути в index.html с base URL:', baseUrl)
      } catch (err) {
        // Игнорируем ошибку, если файл не найден (может быть в dev режиме)
        if (err.code !== 'ENOENT') {
          console.warn('Не удалось исправить пути в index.html:', err.message)
        }
      }
    }
  }
}

// https://vite.dev/config/
export default defineConfig({
  base: process.env.BASE_URL || '/',
  plugins: [
    vue(),
    vueDevTools(),
    tailwindcss(),
    fixIndexHtmlPaths()
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
})
