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
    writeBundle() {
      // Используем writeBundle вместо closeBundle, чтобы сработать после того, как Vite записал файлы
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

        // Сначала исправляем пути к assets (приоритет) - Vite создает их при сборке
        html = html.replace(
          /(href|src)="\/assets\//g,
          `$1="${baseUrlNoSlash}/assets/`
        )

        // Исправляем пути к src/main.js (если Vite не заменил его на assets)
        // Vite должен заменить /src/main.js на /assets/index-xxx.js, но если этого не произошло,
        // нужно найти правильный путь к главному скрипту
        if (html.includes('/src/main.js')) {
          console.warn('Обнаружен путь /src/main.js, который должен был быть заменен Vite')
          // Пытаемся найти правильный путь к главному скрипту в assets
          const assetMatch = html.match(/(href|src)="\/assets\/index-[^"]+\.js"/)
          if (assetMatch) {
            // Заменяем /src/main.js на правильный путь к assets с base URL
            html = html.replace(
              /(href|src)="\/src\/main\.js"/g,
              assetMatch[0].replace(/="\/assets\//, `="${baseUrlNoSlash}/assets/`)
            )
          } else {
            // Если не нашли assets, просто исправляем путь с base URL
            html = html.replace(
              /(href|src)="\/src\/main\.js"/g,
              `$1="${baseUrlNoSlash}/src/main.js"`
            )
          }
        }

        // Исправляем все остальные пути к src (на случай, если Vite не обработал их)
        html = html.replace(
          /(href|src)="\/src\//g,
          `$1="${baseUrlNoSlash}/src/`
        )

        // Затем исправляем все остальные абсолютные пути (кроме внешних ссылок и уже обработанных)
        html = html.replace(
          /(href|src)="\/(?!\/)(?!.*(?:hostatur_client|http|https|data:|mailto:|tel:|#|assets\/|src\/))/g,
          `$1="${baseUrlNoSlash}/`
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
