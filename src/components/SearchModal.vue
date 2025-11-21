<template>
  <Transition
    enter-active-class="transition ease-out duration-300"
    enter-from-class="opacity-0"
    enter-to-class="opacity-100"
    leave-active-class="transition ease-in duration-200"
    leave-from-class="opacity-100"
    leave-to-class="opacity-0"
  >
    <div
      v-if="open"
      class="fixed inset-0 z-50 flex items-center justify-center bg-background/80 backdrop-blur-sm"
      @click.self="close"
    >
      <div class="w-full max-w-2xl px-4">
        <div class="relative">
          <input
            ref="searchInput"
            v-model="query"
            type="text"
            placeholder="Поиск экскурсий, услуг..."
            class="w-full px-6 py-4 text-lg rounded-lg border-2 border-primary focus:outline-none focus:ring-2 focus:ring-primary"
            @keyup.escape="close"
          />
          <Search class="absolute right-6 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
        </div>
        <button
          @click="close"
          class="absolute top-4 right-4 p-2 rounded-full hover:bg-accent transition-colors"
          aria-label="Закрыть"
        >
          <X class="w-5 h-5" />
        </button>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'
import { Search, X } from 'lucide-vue-next'

const props = defineProps({
  open: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['update:open'])

const query = ref('')
const searchInput = ref(null)

const close = () => {
  emit('update:open', false)
  query.value = ''
}

watch(() => props.open, async (newVal) => {
  if (newVal) {
    await nextTick()
    searchInput.value?.focus()
  }
})
</script>

