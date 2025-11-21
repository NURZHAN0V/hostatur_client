<template>
  <div class="relative" @mouseenter="open = true" @mouseleave="open = false">
    <button
      :class="[
        'px-4 py-2 rounded-md text-sm font-medium transition-colors flex items-center gap-1',
        open
          ? 'bg-primary text-primary-foreground'
          : 'text-foreground hover:bg-accent hover:text-accent-foreground'
      ]"
    >
      {{ label }}
      <ChevronDown :class="['w-4 h-4 transition-transform', open && 'rotate-180']" />
    </button>
    <Transition
      enter-active-class="transition ease-out duration-200"
      enter-from-class="opacity-0 translate-y-1"
      enter-to-class="opacity-100 translate-y-0"
      leave-active-class="transition ease-in duration-150"
      leave-from-class="opacity-100 translate-y-0"
      leave-to-class="opacity-0 translate-y-1"
    >
      <div
        v-if="open"
        class="absolute top-full left-0 mt-1 w-56 rounded-md border bg-popover p-1 shadow-lg z-50"
      >
        <slot />
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ChevronDown } from 'lucide-vue-next'

defineProps({
  label: {
    type: String,
    required: true,
  },
})

const open = ref(false)
</script>

