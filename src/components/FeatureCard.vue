<template>
  <RouterLink
    :to="link"
    class="group block p-6 rounded-lg border bg-card hover:shadow-lg transition-all hover:border-primary"
  >
    <div class="flex items-center gap-4 mb-4">
      <div class="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center group-hover:bg-primary/20 transition-colors">
        <component :is="iconComponent" class="w-6 h-6 text-primary" />
      </div>
      <h3 class="text-xl font-semibold">{{ title }}</h3>
    </div>
    <p class="text-muted-foreground">{{ description }}</p>
  </RouterLink>
</template>

<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import { MapPin, Car, Hotel } from 'lucide-vue-next'

const props = defineProps({
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
  link: {
    type: String,
    required: true,
  },
})

const iconMap = {
  MapPin,
  Car,
  Hotel,
}

const iconComponent = computed(() => iconMap[props.icon] || MapPin)
</script>

