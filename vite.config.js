import { fileURLToPath, URL } from 'node:url'
import { readFileSync, writeFileSync } from 'fs'
import { resolve } from 'path'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import tailwindcss from '@tailwindcss/vite'

// Функция для обработки index.html
function processIndexHtml(distIndexPath, baseUrl, mainJsPath) {
  try {
    let html = readFileSync(distIndexPath, 'utf-8')
    console.log('=== Начало обработки index.html ===')
    console.log('BASE_URL:', baseUrl)
    console.log('Исходный index.html (первые 1000 символов):', html.substring(0, 1000))

    // Убираем завершающий слэш из baseUrl для правильной замены
    const baseUrlNoSlash = baseUrl.replace(/\/$/, '')

    // Заменяем абсолютные пути на пути с base URL
    const beforeReplace = html

    // Сначала исправляем пути к assets (приоритет) - Vite создает их при сборке
    html = html.replace(
      /(href|src)="\/assets\//g,
      `$1="${baseUrlNoSlash}/assets/`
    )

    // КРИТИЧЕСКИ ВАЖНО: Исправляем пути к src/main.js
    // Vite должен заменить /src/main.js на /assets/index-xxx.js, но с base URL это может не работать
    if (html.includes('/src/main.js')) {
      console.warn('⚠️ Обнаружен путь /src/main.js, который должен был быть заменен Vite')

      // Ищем JS файлы в HTML
      const allJsMatches = html.matchAll(/(href|src)="\/assets\/[^"]+\.js"/g)
      const jsFiles = Array.from(allJsMatches).map(m => m[0])
      console.log('Найдены JS файлы в HTML:', jsFiles)

      if (jsFiles.length > 0) {
        // Ищем главный скрипт - обычно это index-xxx.js
        let mainAsset = jsFiles.find(f => f.includes('index-'))
        if (!mainAsset && mainJsPath) {
          // Если не нашли index-, ищем по имени из bundle
          const bundleFileName = mainJsPath.split('/').pop()
          mainAsset = jsFiles.find(f => f.includes(bundleFileName))
        }
        if (!mainAsset) {
          // В крайнем случае берем первый
          mainAsset = jsFiles[0]
        }

        console.log('Используем главный скрипт:', mainAsset)
        const correctedPath = mainAsset.replace(/="\/assets\//, `="${baseUrlNoSlash}/assets/`)
        console.log('Исправленный путь:', correctedPath)

        // Заменяем /src/main.js на правильный путь
        html = html.replace(
          /(href|src)="\/src\/main\.js"/g,
          correctedPath
        )
        console.log('✅ Заменен /src/main.js на:', correctedPath)
      } else {
        console.error('❌ Не найдены JS файлы в assets!')
        console.error('Содержимое HTML:', html.substring(0, 2000))
        // В крайнем случае исправляем путь с base URL
        html = html.replace(
          /(href|src)="\/src\/main\.js"/g,
          `$1="${baseUrlNoSlash}/src/main.js"`
        )
      }
    }

    // Затем исправляем все остальные абсолютные пути (кроме внешних ссылок и уже обработанных)
    html = html.replace(
      /(href|src)="\/(?!\/)(?!.*(?:hostatur_client|http|https|data:|mailto:|tel:|#|assets\/|src\/))/g,
      `$1="${baseUrlNoSlash}/`
    )

    if (beforeReplace !== html) {
      writeFileSync(distIndexPath, html, 'utf-8')
      console.log('✅ Исправлены пути в index.html с base URL:', baseUrl)
      console.log('Исправленный index.html (первые 1000 символов):', html.substring(0, 1000))
      console.log('=== Конец обработки index.html ===')
    } else {
      console.log('⚠️ Пути в index.html не требуют исправления (возможно, проблема!)')
      console.log('Проверяем содержимое:', html.substring(0, 1000))
    }
  } catch (err) {
    // Игнорируем ошибку, если файл не найден (может быть в dev режиме)
    if (err.code !== 'ENOENT') {
      console.error('Не удалось исправить пути в index.html:', err.message)
      console.error('Ошибка:', err)
    }
  }
}

// Плагин для исправления путей в index.html после сборки
function fixIndexHtmlPaths() {
  let mainJsPath = null

  return {
    name: 'fix-index-html-paths',
    generateBundle(options, bundle) {
      // Сохраняем путь к главному JS файлу из bundle
      const jsFiles = Object.keys(bundle).filter(name => name.endsWith('.js'))
      if (jsFiles.length > 0) {
        // Ищем главный entry файл
        mainJsPath = jsFiles.find(name => name.includes('index') || name.includes('main')) || jsFiles[0]
        console.log('📦 Найден главный JS файл в bundle:', mainJsPath)
      }
    },
    writeBundle() {
      // Используем writeBundle для финальной обработки index.html
      const baseUrl = process.env.BASE_URL || '/'
      if (baseUrl === '/') {
        console.log('BASE_URL = /, пропускаем исправление путей')
        return // Не нужно исправлять для корневого пути
      }

      const distIndexPath = resolve(__dirname, 'dist/index.html')
      processIndexHtml(distIndexPath, baseUrl, mainJsPath)
    },
    buildEnd() {
      // Дополнительная обработка в buildEnd на случай, если writeBundle не сработал
      const baseUrl = process.env.BASE_URL || '/'
      if (baseUrl === '/') {
        return
      }

      const distIndexPath = resolve(__dirname, 'dist/index.html')
      try {
        processIndexHtml(distIndexPath, baseUrl, mainJsPath)
      } catch (err) {
        if (err.code !== 'ENOENT') {
          console.error('Ошибка в buildEnd:', err)
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
