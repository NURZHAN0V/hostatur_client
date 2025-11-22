import './style.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

console.log('Инициализация приложения...')
console.log('BASE_URL:', import.meta.env.BASE_URL)

const app = createApp(App)

app.use(createPinia())
app.use(router)

// Обработка ошибок
app.config.errorHandler = (err, instance, info) => {
  console.error('Ошибка Vue:', err)
  console.error('Информация:', info)
  console.error('Экземпляр:', instance)
}

try {
  app.mount('#app')
  console.log('Приложение успешно смонтировано')
} catch (err) {
  console.error('Ошибка монтирования приложения:', err)
}
