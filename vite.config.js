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
      if (baseUrl === '/') {
        console.log('BASE_URL = /, пропускаем исправление путей')
        return // Не нужно исправлять для корневого пути
      }

      const distIndexPath = resolve(__dirname, 'dist/index.html')
      try {
        let html = readFileSync(distIndexPath, 'utf-8')
        console.log('Исходный index.html (первые 500 символов):', html.substring(0, 500))

        // Убираем завершающий слэш из baseUrl для правильной замены
        const baseUrlNoSlash = baseUrl.replace(/\/$/, '')

        // Заменяем абсолютные пути на пути с base URL
        // Ищем паттерны: href="/..." или src="/..." (но не href="//..." или src="//...")
        // Исключаем пути, которые уже содержат base URL или являются внешними ссылками
        const beforeReplace = html

        // Исправляем пути, которые начинаются с /, но не содержат base URL
        // Это включает пути к assets, которые Vite уже обработал
        // Исключаем внешние ссылки и пути, которые уже содержат base URL
        html = html.replace(
          /(href|src)="\/(?!\/)(?!.*(?:hostatur_client|http|https|data:|mailto:|tel:|#))/g,
          `$1="${baseUrlNoSlash}/`
        )

        // Также исправляем пути к assets, которые Vite может создать без base URL
        // Например: /assets/main.js -> /hostatur_client/assets/main.js
        html = html.replace(
          /(href|src)="\/assets\//g,
          `$1="${baseUrlNoSlash}/assets/`
        )

        if (beforeReplace !== html) {
          writeFileSync(distIndexPath, html, 'utf-8')
          console.log('Исправлены пути в index.html с base URL:', baseUrl)
          console.log('Исправленный index.html (первые 500 символов):', html.substring(0, 500))
        } else {
          console.log('Пути в index.html не требуют исправления')
        }
      } catch (err) {
        // Игнорируем ошибку, если файл не найден (может быть в dev режиме)
        if (err.code !== 'ENOENT') {
          console.error('Не удалось исправить пути в index.html:', err.message)
          console.error('Ошибка:', err)
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
