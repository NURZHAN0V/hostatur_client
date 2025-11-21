<template>
  <div class="py-12">
    <div class="container mx-auto px-4">
      <!-- Page Header -->
      <div class="text-center mb-12">
        <h1 class="text-4xl md:text-5xl font-bold mb-4 text-primary">Контакты</h1>
        <p class="text-lg text-muted-foreground max-w-2xl mx-auto">
          Свяжитесь с нами любым удобным способом
        </p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
        <!-- Contact Information -->
        <div class="space-y-8">
          <ContactCard
            icon="Phone"
            title="Телефоны"
            :items="[
              { label: 'Основной', value: '+7 (988) 504-25-45', href: 'tel:+79885042545' },
              { label: 'Дополнительный', value: '+7 (918) 901-32-11', href: 'tel:+79189013211' }
            ]"
          />
          <ContactCard
            icon="Mail"
            title="Email"
            :items="[
              { label: 'Email', value: 'info@hostaotdykh.ru', href: 'mailto:info@hostaotdykh.ru' }
            ]"
          />
          <ContactCard
            icon="MapPin"
            title="Адрес"
            :items="[
              { label: 'Город', value: 'Сочи, Краснодарский край' }
            ]"
          />
        </div>

        <!-- Contact Form -->
        <div class="bg-card border rounded-lg p-8">
          <h2 class="text-2xl font-bold mb-6">Отправить сообщение</h2>
          <form @submit.prevent="handleSubmit" class="space-y-4">
            <div>
              <label for="name" class="block text-sm font-medium mb-2">Имя</label>
              <input
                id="name"
                v-model="form.name"
                type="text"
                required
                class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
              />
            </div>
            <div>
              <label for="phone" class="block text-sm font-medium mb-2">Телефон</label>
              <input
                id="phone"
                v-model="form.phone"
                type="tel"
                required
                class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
              />
            </div>
            <div>
              <label for="email" class="block text-sm font-medium mb-2">Email</label>
              <input
                id="email"
                v-model="form.email"
                type="email"
                required
                class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
              />
            </div>
            <div>
              <label for="message" class="block text-sm font-medium mb-2">Сообщение</label>
              <textarea
                id="message"
                v-model="form.message"
                rows="4"
                required
                class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
              />
            </div>
            <button
              type="submit"
              class="w-full px-6 py-3 bg-primary text-primary-foreground rounded-lg font-semibold hover:bg-primary/90 transition-colors"
            >
              Отправить
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Phone, Mail, MapPin } from 'lucide-vue-next'
import ContactCard from '@/components/ContactCard.vue'

const form = ref({
  name: '',
  phone: '',
  email: '',
  message: '',
})

const handleSubmit = () => {
  // TODO: реализовать отправку формы
  console.log('Form submitted:', form.value)
  alert('Сообщение отправлено! Мы свяжемся с вами в ближайшее время.')
  form.value = {
    name: '',
    phone: '',
    email: '',
    message: '',
  }
}
</script>

