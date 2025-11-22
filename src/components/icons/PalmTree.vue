<template>
  <svg
    viewBox="0 0 24 24"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    :class="className"
  >
    <!-- Ствол пальмы -->
    <path
      d="M11 20L11 22M13 20L13 22"
      stroke="currentColor"
      stroke-width="1.2"
      stroke-linecap="round"
    />
    <path
      d="M11.5 16L11.5 20M12.5 16L12.5 20"
      stroke="currentColor"
      stroke-width="1.5"
      stroke-linecap="round"
    />
    <!-- Листья пальмы (реалистичные) -->
    <!-- Центральный лист -->
    <path
      d="M12 2L12 8L10 10L12 12L14 10L12 8L12 2Z"
      fill="currentColor"
      opacity="0.9"
    />
    <!-- Левые листья -->
    <path
      d="M12 4L8 6L6 8L8 10L10 9L12 8L12 4Z"
      fill="currentColor"
      opacity="0.8"
    />
    <path
      d="M12 6L7 8L5 10L7 12L9 11L12 10L12 6Z"
      fill="currentColor"
      opacity="0.7"
    />
    <!-- Правые листья -->
    <path
      d="M12 4L16 6L18 8L16 10L14 9L12 8L12 4Z"
      fill="currentColor"
      opacity="0.8"
    />
    <path
      d="M12 6L17 8L19 10L17 12L15 11L12 10L12 6Z"
      fill="currentColor"
      opacity="0.7"
    />
    <!-- Дополнительные боковые листья для объема -->
    <path
      d="M10 5L8 7L6 9L8 11L10 10L10 5Z"
      fill="currentColor"
      opacity="0.6"
    />
    <path
      d="M14 5L16 7L18 9L16 11L14 10L14 5Z"
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

