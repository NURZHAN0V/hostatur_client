<template>
  <RouterLink
    :to="to"
    :class="[
      'px-4 py-2 rounded-md text-sm font-medium transition-colors',
      active
        ? 'bg-primary text-primary-foreground'
        : 'text-foreground hover:bg-accent hover:text-accent-foreground'
    ]"
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
  active: {
    type: Boolean,
    default: false,
  },
})
</script>

