<template>
  <div class="py-12">
    <div class="container mx-auto px-4">
      <!-- Page Header -->
      <div class="text-center mb-12">
        <h1 class="text-4xl md:text-5xl font-bold mb-4 text-primary">
          Экскурсии по Сочи и Абхазии
        </h1>
        <p class="text-lg text-muted-foreground max-w-2xl mx-auto">
          Выберите увлекательное путешествие по самым живописным местам побережья
        </p>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
        <p class="mt-4 text-muted-foreground">Загрузка экскурсий...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="text-center py-12">
        <p class="text-destructive mb-4">{{ error }}</p>
        <button
          @click="loadExcursions"
          class="px-6 py-3 bg-primary text-primary-foreground rounded-lg font-semibold hover:bg-primary/90 transition-colors"
        >
          Попробовать снова
        </button>
      </div>

      <!-- Content -->
      <div v-else>
        <!-- Category Tabs -->
        <div class="flex flex-wrap justify-center gap-4 mb-12">
          <button
            v-for="category in categories"
            :key="category.id"
            @click="selectedCategory = category.id"
            :class="[
              'px-6 py-3 rounded-lg font-semibold transition-all',
              selectedCategory === category.id
                ? 'bg-primary text-primary-foreground shadow-lg'
                : 'bg-muted hover:bg-muted/80'
            ]"
          >
            {{ category.name }}
            <span
              v-if="category.count !== undefined"
              class="ml-2 px-2 py-0.5 bg-background/50 rounded text-xs"
            >
              {{ category.count }}
            </span>
          </button>
        </div>

        <!-- Excursions Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <ExcursionCard
            v-for="excursion in filteredExcursions"
            :key="excursion.id"
            :excursion="excursion"
            :in-cart="isInCart(excursion.id)"
            @add-to-cart="handleAddToCart"
          />
        </div>

        <!-- Empty State -->
        <div v-if="filteredExcursions.length === 0" class="text-center py-12">
          <p class="text-muted-foreground text-lg">Экскурсии не найдены</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import ExcursionCard from '@/components/ExcursionCard.vue'
import { useExcursions } from '@/composables/useExcursions'

const route = useRoute()
const { 
  excursions, 
  excursionsByCategory, 
  loading, 
  error, 
  loadExcursions 
} = useExcursions()

const selectedCategory = ref(route.params.category || 'all')
const cartItems = ref([]) // TODO: подключить к store

const categories = computed(() => [
  { 
    id: 'all', 
    name: 'Все экскурсии',
    count: excursionsByCategory.value.all.length
  },
  { 
    id: 'sochi', 
    name: 'Сочи',
    count: excursionsByCategory.value.sochi.length
  },
  { 
    id: 'abkhazia', 
    name: 'Абхазия',
    count: excursionsByCategory.value.abkhazia.length
  },
])

const filteredExcursions = computed(() => {
  if (selectedCategory.value === 'all') {
    return excursionsByCategory.value.all
  }
  return excursionsByCategory.value[selectedCategory.value] || []
})

const isInCart = (id) => {
  return cartItems.value.some(item => item.id === id)
}

const handleAddToCart = (excursion) => {
  // TODO: добавить в store
  cartItems.value.push(excursion)
}

onMounted(() => {
  loadExcursions()
})
</script>
