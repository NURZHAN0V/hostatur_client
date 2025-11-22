<template>
  <svg
    viewBox="0 0 24 24"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    :class="className"
  >
    <!-- Ствол пальмы -->
    <path
      d="M11.5 18L11.5 22"
      stroke="currentColor"
      stroke-width="1.5"
      stroke-linecap="round"
    />
    <path
      d="M12.5 18L12.5 22"
      stroke="currentColor"
      stroke-width="1.5"
      stroke-linecap="round"
    />
    <!-- Листья пальмы (веер) -->
    <path
      d="M12 4L8 8L12 10L16 8L12 4Z"
      fill="currentColor"
      opacity="0.9"
    />
    <path
      d="M12 4L6 10L12 12L18 10L12 4Z"
      fill="currentColor"
      opacity="0.7"
    />
    <path
      d="M12 4L4 12L12 14L20 12L12 4Z"
      fill="currentColor"
      opacity="0.5"
    />
    <!-- Дополнительные листья для объема -->
    <path
      d="M10 6L7 9L10 10L13 9L10 6Z"
      fill="currentColor"
      opacity="0.6"
    />
    <path
      d="M14 6L17 9L14 10L11 9L14 6Z"
      fill="currentColor"
      opacity="0.6"
    />
  </svg>
</template>

<script setup>
defineProps({
  className: {
    type: String,
    default: 'w-6 h-6'
  }
})
</script>

