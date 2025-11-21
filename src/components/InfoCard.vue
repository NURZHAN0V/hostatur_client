<template>
  <div class="bg-card border rounded-lg p-6 hover:shadow-lg transition-shadow">
    <h3 class="text-xl font-semibold mb-3 text-primary">{{ title }}</h3>
    <p class="text-muted-foreground">{{ description }}</p>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true,
  },
  description: {
    type: String,
    required: true,
  },
})
</script>

