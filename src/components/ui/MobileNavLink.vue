<template>
  <RouterLink
    :to="to"
    class="block px-4 py-2 rounded-md text-base font-medium hover:bg-accent transition-colors"
    @click="$emit('click')"
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

defineEmits(['click'])
</script>

