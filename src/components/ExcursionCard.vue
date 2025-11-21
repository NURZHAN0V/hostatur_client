<template>
  <div class="group relative overflow-hidden rounded-lg border bg-card hover:shadow-xl transition-all">
    <div class="aspect-video overflow-hidden relative">
      <img
        :src="excursion.image"
        :alt="excursion.title"
        class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
        @error="handleImageError"
      />
      <div class="absolute top-4 right-4 flex flex-col gap-2">
        <span class="px-3 py-1 bg-primary text-primary-foreground rounded-full text-sm font-semibold shadow-lg">
          {{ excursion.price }}
        </span>
        <span
          v-if="excursion.duration"
          class="px-3 py-1 bg-background/90 text-foreground rounded-full text-xs font-medium backdrop-blur-sm"
        >
          {{ excursion.duration }}
        </span>
      </div>
      <div
        v-if="excursion.images && excursion.images.length > 1"
        class="absolute bottom-4 left-4 px-2 py-1 bg-background/90 text-foreground rounded text-xs font-medium backdrop-blur-sm"
      >
        {{ excursion.images.length }} фото
      </div>
    </div>
    <div class="p-6">
      <div class="mb-2">
        <span
          :class="[
            'inline-block px-2 py-1 rounded text-xs font-medium',
            excursion.category === 'sochi' 
              ? 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200' 
              : 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
          ]"
        >
          {{ excursion.category === 'sochi' ? 'Сочи' : 'Абхазия' }}
        </span>
      </div>
      <h3 class="text-xl font-semibold mb-2 group-hover:text-primary transition-colors line-clamp-2">
        {{ excursion.title }}
      </h3>
      <p class="text-muted-foreground mb-4 line-clamp-2 text-sm">
        {{ excursion.description }}
      </p>
      <div class="flex items-center justify-between">
        <RouterLink
          :to="`/excursions/detail/${excursion.id}`"
          class="inline-flex items-center gap-2 text-primary font-medium hover:gap-3 transition-all"
        >
          Подробнее
          <ArrowRight class="w-4 h-4" />
        </RouterLink>
        <button
          v-if="!inCart"
          @click="$emit('add-to-cart', excursion)"
          class="px-4 py-2 bg-primary text-primary-foreground rounded-lg text-sm font-medium hover:bg-primary/90 transition-colors"
        >
          В корзину
        </button>
        <span
          v-else
          class="px-4 py-2 bg-muted text-muted-foreground rounded-lg text-sm font-medium"
        >
          В корзине
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { RouterLink } from 'vue-router'
import { ArrowRight } from 'lucide-vue-next'

const props = defineProps({
  excursion: {
    type: Object,
    required: true,
  },
  inCart: {
    type: Boolean,
    default: false,
  },
})

defineEmits(['add-to-cart'])

const handleImageError = (event) => {
  event.target.src = 'https://placehold.net/400x300'
}
</script>
