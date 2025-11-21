<template>
  <div class="relative" @mouseenter="open = true" @mouseleave="open = false">
    <button
      class="flex items-center gap-2 px-3 py-1.5 rounded-md text-sm hover:bg-accent transition-colors"
    >
      <Globe class="w-4 h-4" />
      <span>{{ currentLanguage }}</span>
      <ChevronDown :class="['w-3 h-3 transition-transform', open && 'rotate-180']" />
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
        class="absolute top-full right-0 mt-1 w-32 rounded-md border bg-popover p-1 shadow-lg z-50"
      >
        <button
          v-for="lang in languages"
          :key="lang.code"
          @click="selectLanguage(lang.code)"
          :class="[
            'w-full text-left px-3 py-2 rounded-sm text-sm hover:bg-accent transition-colors',
            currentLanguage === lang.name && 'bg-accent'
          ]"
        >
          {{ lang.name }}
        </button>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Globe, ChevronDown } from 'lucide-vue-next'

const languages = [
  { code: 'ru', name: 'Русский' },
  { code: 'en', name: 'English' },
  { code: 'es', name: 'Español' },
  { code: 'de', name: 'Deutsch' },
  { code: 'it', name: 'Italiano' },
  { code: 'fr', name: 'Français' },
]

const currentLanguage = ref('Русский')
const open = ref(false)

const selectLanguage = (code) => {
  // TODO: реализовать переключение языка
  currentLanguage.value = languages.find(l => l.code === code)?.name || 'Русский'
  open.value = false
}
</script>

