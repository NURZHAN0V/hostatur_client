import { fileURLToPath, URL } from 'node:url'
import { readFileSync, writeFileSync } from 'fs'
import { resolve } from 'path'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import tailwindcss from '@tailwindcss/vite'

// Функция для обработки index.html
function processIndexHtml(distIndexPath, baseUrl) {
  const baseUrlNoSlash = baseUrl.replace(/\/$/, '')

  try {
    let html = readFileSync(distIndexPath, 'utf-8')
    const beforeReplace = html

    // Сначала исправляем пути к assets (приоритет) - Vite создает их при сборке
    html = html.replace(
      /(href|src)="\/assets\//g,
      `$1="${baseUrlNoSlash}/assets/`
    )

    // КРИТИЧЕСКИ ВАЖНО: Если есть /src/main.js, нужно заменить его на правильный путь к assets
    if (html.includes('/src/main.js')) {
      console.warn('⚠️ Обнаружен путь /src/main.js, который должен был быть заменен Vite')

      // Ищем JS файлы в assets
      const jsMatches = html.matchAll(/(href|src)="\/assets\/[^"]+\.js"/g)
      const jsFiles = Array.from(jsMatches).map(m => m[0])
      console.log('Найдены JS файлы в HTML:', jsFiles)

      if (jsFiles.length > 0) {
        // Ищем главный скрипт (обычно index-xxx.js)
        let mainAsset = jsFiles.find(f => f.includes('index-'))
        if (!mainAsset) {
          mainAsset = jsFiles[0] // Берем первый, если нет index-
        }
        console.log('Выбран главный скрипт:', mainAsset)

        const correctedPath = mainAsset.replace(/="\/assets\//, `="${baseUrlNoSlash}/assets/`)
        console.log('Исправленный путь:', correctedPath)

        // Заменяем /src/main.js на правильный путь
        html = html.replace(
          /(href|src)="\/src\/main\.js"/g,
          correctedPath
        )
        console.log('✅ Заменен /src/main.js на:', correctedPath)
      } else {
        console.error('❌ НЕ НАЙДЕНЫ JS ФАЙЛЫ В ASSETS!')
        console.error('Полный HTML:', html)
        // В крайнем случае просто добавляем base URL
        html = html.replace(
          /(href|src)="\/src\/main\.js"/g,
          `$1="${baseUrlNoSlash}/src/main.js"`
        )
        console.warn('⚠️ Использован fallback путь:', `${baseUrlNoSlash}/src/main.js`)
      }
    }

    // Исправляем остальные пути к src (если есть)
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
      console.log('✅ Исправлены пути в index.html с base URL:', baseUrl)
      console.log('Исправленный index.html (первые 1000 символов):', html.substring(0, 1000))
      return true
    } else {
      console.log('⚠️ Пути в index.html не требуют исправления (возможно, проблема!)')
      console.log('Проверяем содержимое:', html.substring(0, 1000))
      return false
    }
  } catch (err) {
    if (err.code !== 'ENOENT') {
      console.error('Не удалось исправить пути в index.html:', err.message)
      console.error('Ошибка:', err)
    }
    return false
  }
}

// Плагин для исправления путей в index.html после сборки
function fixIndexHtmlPaths() {
  return {
    name: 'fix-index-html-paths',
    writeBundle() {
      // Используем writeBundle, чтобы сработать после записи файлов
      const baseUrl = process.env.BASE_URL || '/'
      if (baseUrl === '/') {
        console.log('BASE_URL = /, пропускаем исправление путей')
        return // Не нужно исправлять для корневого пути
      }

      const distIndexPath = resolve(__dirname, 'dist/index.html')
      console.log('=== НАЧАЛО ОБРАБОТКИ index.html (writeBundle) ===')
      console.log('BASE_URL:', baseUrl)
      processIndexHtml(distIndexPath, baseUrl)
      console.log('=== КОНЕЦ ОБРАБОТКИ index.html (writeBundle) ===')
    },
    buildEnd() {
      // Дополнительная обработка в buildEnd на случай, если writeBundle не сработал
      const baseUrl = process.env.BASE_URL || '/'
      if (baseUrl === '/') {
        return
      }

      const distIndexPath = resolve(__dirname, 'dist/index.html')
      console.log('=== НАЧАЛО ОБРАБОТКИ index.html (buildEnd) ===')
      console.log('BASE_URL:', baseUrl)
      processIndexHtml(distIndexPath, baseUrl)
      console.log('=== КОНЕЦ ОБРАБОТКИ index.html (buildEnd) ===')
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
