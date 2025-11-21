<template>
  <div class="bg-card border rounded-lg p-6">
    <div class="flex items-center gap-3 mb-4">
      <component :is="iconComponent" class="w-6 h-6 text-primary" />
      <h3 class="text-xl font-semibold">{{ title }}</h3>
    </div>
    <div class="space-y-2">
      <div v-for="(item, index) in items" :key="index">
        <span v-if="item.label" class="text-sm text-muted-foreground">{{ item.label }}: </span>
        <a
          v-if="item.href"
          :href="item.href"
          class="text-foreground hover:text-primary transition-colors"
        >
          {{ item.value }}
        </a>
        <span v-else class="text-foreground">{{ item.value }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Phone, Mail, MapPin } from 'lucide-vue-next'

const props = defineProps({
  icon: {
    type: String,
    required: true,
  },
  title: {
    type: String,
    required: true,
  },
  items: {
    type: Array,
    required: true,
  },
})

const iconMap = {
  Phone,
  Mail,
  MapPin,
}

const iconComponent = computed(() => iconMap[props.icon] || Phone)
</script>

