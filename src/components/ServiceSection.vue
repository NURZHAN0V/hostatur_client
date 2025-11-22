<template>
  <section :id="id" class="scroll-mt-20">
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
      <div>
        <div class="flex items-center gap-4 mb-6">
          <div class="w-16 h-16 rounded-lg bg-primary/10 flex items-center justify-center">
            <component :is="iconComponent" class="w-8 h-8 text-primary" />
          </div>
          <h2 class="text-3xl font-bold text-primary">{{ title }}</h2>
        </div>
        <p class="text-lg text-muted-foreground mb-6">{{ description }}</p>
        <ul class="space-y-3">
          <li
            v-for="(feature, index) in featuresList"
            :key="index"
            class="flex items-start gap-3"
          >
            <CheckCircle class="w-5 h-5 text-primary mt-0.5 flex-shrink-0" />
            <span>{{ feature }}</span>
          </li>
        </ul>
      </div>
      <div class="relative aspect-video rounded-lg overflow-hidden bg-gradient-to-br from-primary/20 to-accent/20">
        <img
          :src="getServiceImage(id)"
          :alt="title"
          class="w-full h-full object-cover"
          @error="handleImageError"
        />
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue'
import { Users, Calendar, Car, Hotel, CheckCircle } from 'lucide-vue-next'

const props = defineProps({
  id: {
    type: String,
    required: true,
  },
  icon: {
    type: String,
    required: true,
  },
  title: {
    type: String,
    required: true,
  },
  description: {
    type: String,
    required: true,
  },
  features: {
    type: String,
    required: true,
  },
})

const iconMap = {
  Users,
  Calendar,
  Car,
  Hotel,
}

const iconComponent = computed(() => iconMap[props.icon] || Users)

const featuresList = computed(() => {
  return props.features.split(',').map(f => f.trim())
})

const getServiceImage = (serviceId) => {
  try {
    if (!serviceId) {
      return 'https://placehold.net/600x400/55c4e8/ffffff?text=' + encodeURIComponent(props.title || 'Service')
    }
    // Используем placeholder изображения, так как внешние источники могут быть недоступны
    // Если у вас есть локальные изображения, поместите их в public/images/services/ и используйте:
    // return `${import.meta.env.BASE_URL}images/services/${serviceId}.jpg`
    const images = {
      guides: 'https://placehold.net/600x400/55c4e8/ffffff?text=' + encodeURIComponent('Гиды-переводчики'),
      events: 'https://placehold.net/600x400/55c4e8/ffffff?text=' + encodeURIComponent('Мероприятия'),
      transfer: 'https://placehold.net/600x400/55c4e8/ffffff?text=' + encodeURIComponent('Трансфер'),
      accommodation: 'https://placehold.net/600x400/55c4e8/ffffff?text=' + encodeURIComponent('Размещение'),
    }
    return images[serviceId] || 'https://placehold.net/600x400/55c4e8/ffffff?text=' + encodeURIComponent(props.title || 'Service')
  } catch (err) {
    console.warn('Ошибка при получении изображения услуги:', err)
    return 'https://placehold.net/600x400/55c4e8/ffffff?text=' + encodeURIComponent(props.title || 'Service')
  }
}

const handleImageError = (event) => {
  try {
    if (event && event.target) {
      event.target.src = 'https://placehold.net/600x400/55c4e8/ffffff?text=' + encodeURIComponent(props.title || 'Service')
    }
  } catch (err) {
    console.warn('Ошибка при обработке ошибки изображения:', err)
  }
}
</script>

