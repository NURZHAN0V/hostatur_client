<template>
  <RouterLink
    :to="to"
    class="block px-3 py-2 rounded-sm text-sm hover:bg-accent hover:text-accent-foreground transition-colors"
  >
    <slot />
  </RouterLink>
</template>

<script setup>
defineProps({
  to: {
    type: String,
    required: true,
  },
})
</script>

