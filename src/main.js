import './style.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

// Инициализация приложения

// Глобальная обработка ошибок (только логирование, не блокируем)
window.addEventListener('error', (event) => {
  console.error('Глобальная ошибка:', event.error)
  console.error('Файл:', event.filename, 'Строка:', event.lineno)
  // НЕ вызываем preventDefault, чтобы браузер мог обработать ошибку нормально
})

window.addEventListener('unhandledrejection', (event) => {
  console.error('Необработанное отклонение промиса:', event.reason)
  // НЕ вызываем preventDefault, чтобы браузер мог обработать ошибку нормально
})

const app = createApp(App)

app.use(createPinia())
app.use(router)

// Обработка ошибок Vue
app.config.errorHandler = (err, instance, info) => {
  console.error('Ошибка Vue:', err)
  console.error('Информация:', info)
  console.error('Экземпляр:', instance)
}

// Обработка предупреждений
app.config.warnHandler = (msg, instance, trace) => {
  console.warn('Предупреждение Vue:', msg)
  console.warn('Трассировка:', trace)
}

try {
  app.mount('#app')
} catch (err) {
  console.error('Ошибка монтирования приложения:', err)
  // Показываем ошибку пользователю
  const appElement = document.getElementById('app')
  if (appElement) {
    appElement.innerHTML = `
      <div style="padding: 20px; font-family: sans-serif; max-width: 800px; margin: 50px auto;">
        <h1 style="color: #dc2626;">Произошла ошибка</h1>
        <p style="color: #6b7280;">Не удалось загрузить приложение. Пожалуйста, перезагрузите страницу.</p>
        <details style="margin-top: 20px;">
          <summary style="cursor: pointer; color: #3b82f6;">Детали ошибки</summary>
          <pre style="background: #f3f4f6; padding: 15px; border-radius: 5px; overflow-x: auto; margin-top: 10px;">${err.message}\n${err.stack}</pre>
        </details>
        <button onclick="location.reload()" style="margin-top: 20px; padding: 10px 20px; background: #3b82f6; color: white; border: none; border-radius: 5px; cursor: pointer;">Перезагрузить страницу</button>
      </div>
    `
  }
}
