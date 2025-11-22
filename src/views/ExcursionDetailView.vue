<template>
  <div class="py-12 bg-background">
    <div class="container mx-auto px-4 max-w-6xl">
      <!-- Loading State -->
      <div v-if="loading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
        <p class="mt-4 text-muted-foreground">Загрузка...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error || !excursion" class="text-center py-12">
        <p class="text-destructive mb-4 text-lg">{{ error || 'Экскурсия не найдена' }}</p>
        <RouterLink
          to="/excursions"
          class="inline-flex items-center gap-2 px-6 py-3 bg-primary text-primary-foreground rounded-lg font-semibold hover:bg-primary/90 transition-colors"
        >
          <ArrowLeft class="w-5 h-5" />
          Вернуться к экскурсиям
        </RouterLink>
      </div>

      <!-- Content -->
      <div v-else>
        <!-- Breadcrumbs -->
        <nav class="mb-6 text-sm text-muted-foreground flex items-center gap-2">
          <RouterLink to="/" class="hover:text-primary transition-colors">Главная</RouterLink>
          <ChevronRight class="w-4 h-4" />
          <RouterLink to="/excursions" class="hover:text-primary transition-colors">Экскурсии</RouterLink>
          <ChevronRight class="w-4 h-4" />
          <span class="text-foreground font-medium">{{ excursion.title }}</span>
        </nav>

        <!-- Header Section -->
        <div class="mb-8">
          <div class="mb-4 flex items-center gap-3">
            <span
              :class="[
                'inline-block px-3 py-1.5 rounded-lg text-sm font-medium',
                excursion.category === 'sochi'
                  ? 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200'
                  : 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
              ]"
            >
              {{ excursion.category === 'sochi' ? 'Сочи' : 'Абхазия' }}
            </span>
            <span v-if="excursion.duration" class="text-sm text-muted-foreground flex items-center gap-1">
              <Clock class="w-4 h-4" />
              {{ excursion.duration }}
            </span>
          </div>
          <h1 class="text-4xl md:text-5xl font-bold mb-4 text-primary leading-tight">
            {{ excursion.title }}
          </h1>
          <p class="text-lg text-muted-foreground leading-relaxed">
            {{ excursion.description }}
          </p>
        </div>

        <!-- Main Image Gallery -->
        <div class="mb-8">
          <div class="relative rounded-lg overflow-hidden bg-muted">
            <img
              :src="currentImage"
              :alt="excursion.title"
              class="w-full h-[600px] object-cover"
              @error="handleImageError"
            />
            <!-- Image Navigation -->
            <div v-if="excursion.images && excursion.images.length > 1" class="absolute inset-0 flex items-center justify-between p-4">
              <button
                @click="previousImage"
                :disabled="currentImageIndex === 0"
                :class="[
                  'p-3 rounded-full bg-background/90 backdrop-blur-sm hover:bg-background transition-colors',
                  currentImageIndex === 0 && 'opacity-50 cursor-not-allowed'
                ]"
                aria-label="Предыдущее изображение"
              >
                <ChevronLeft class="w-6 h-6" />
              </button>
              <button
                @click="nextImage"
                :disabled="currentImageIndex === excursion.images.length - 1"
                :class="[
                  'p-3 rounded-full bg-background/90 backdrop-blur-sm hover:bg-background transition-colors',
                  currentImageIndex === excursion.images.length - 1 && 'opacity-50 cursor-not-allowed'
                ]"
                aria-label="Следующее изображение"
              >
                <ChevronRight class="w-6 h-6" />
              </button>
            </div>
            <!-- Image Counter -->
            <div
              v-if="excursion.images && excursion.images.length > 1"
              class="absolute bottom-4 left-1/2 -translate-x-1/2 px-4 py-2 bg-background/90 backdrop-blur-sm rounded-full text-sm font-medium"
            >
              {{ currentImageIndex + 1 }} / {{ excursion.images.length }}
            </div>
          </div>
        </div>

        <!-- Info Cards Grid -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <!-- Price Card -->
          <div class="bg-card border rounded-lg p-6 shadow-sm">
            <div class="flex items-center gap-3 mb-2">
              <div class="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
                <Tag class="w-5 h-5 text-primary" />
              </div>
              <h3 class="text-sm font-medium text-muted-foreground">Цена</h3>
            </div>
            <p class="text-2xl font-bold text-primary">{{ excursion.price }}</p>
          </div>

          <!-- Duration Card -->
          <div v-if="excursion.duration" class="bg-card border rounded-lg p-6 shadow-sm">
            <div class="flex items-center gap-3 mb-2">
              <div class="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
                <Clock class="w-5 h-5 text-primary" />
              </div>
              <h3 class="text-sm font-medium text-muted-foreground">Длительность</h3>
            </div>
            <p class="text-2xl font-bold text-primary">{{ excursion.duration }}</p>
          </div>

          <!-- Images Count Card -->
          <div v-if="excursion.images && excursion.images.length > 0" class="bg-card border rounded-lg p-6 shadow-sm">
            <div class="flex items-center gap-3 mb-2">
              <div class="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
                <ImageIcon class="w-5 h-5 text-primary" />
              </div>
              <h3 class="text-sm font-medium text-muted-foreground">Фотографий</h3>
            </div>
            <p class="text-2xl font-bold text-primary">{{ excursion.images.length }}</p>
          </div>
        </div>

        <!-- Two Column Layout -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
          <!-- Main Content -->
          <div class="lg:col-span-2 space-y-8">
            <!-- Description Content -->
            <section class="bg-card border rounded-lg p-6">
              <h2 class="text-2xl font-bold mb-6 text-primary">Описание экскурсии</h2>
              <div class="prose prose-lg max-w-none">
                <!-- Headings -->
                <div
                  v-for="(heading, index) in excursion.content?.headings"
                  :key="`heading-${index}`"
                  class="mb-4"
                >
                  <h3
                    :class="[
                      'font-bold text-foreground',
                      heading.level === 'h1' && 'text-3xl',
                      heading.level === 'h2' && 'text-2xl',
                      heading.level === 'h3' && 'text-xl'
                    ]"
                  >
                    {{ heading.text }}
                  </h3>
                </div>

                <!-- Paragraphs -->
                <div
                  v-for="(paragraph, index) in excursion.content?.paragraphs"
                  :key="`paragraph-${index}`"
                  class="mb-4 text-muted-foreground leading-relaxed whitespace-pre-line"
                >
                  {{ paragraph }}
                </div>

                <!-- Lists -->
                <div
                  v-for="(list, listIndex) in excursion.content?.lists"
                  :key="`list-${listIndex}`"
                  class="mb-4"
                >
                  <ul v-if="Array.isArray(list)" class="list-disc list-inside space-y-2 text-muted-foreground">
                    <li v-for="(item, itemIndex) in list" :key="`item-${itemIndex}`">
                      {{ item }}
                    </li>
                  </ul>
                </div>
              </div>
            </section>

            <!-- All Images Gallery -->
            <section v-if="excursion.images && excursion.images.length > 1" class="bg-card border rounded-lg p-6">
              <div class="flex items-center justify-between mb-6">
                <h2 class="text-2xl font-bold text-primary">Галерея</h2>
                <button
                  @click="showAllImages = !showAllImages"
                  class="text-sm text-primary hover:underline flex items-center gap-1"
                >
                  {{ showAllImages ? 'Свернуть' : 'Показать все' }}
                  <ChevronDown :class="['w-4 h-4 transition-transform', showAllImages && 'rotate-180']" />
                </button>
              </div>
              <div
                :class="[
                  'grid gap-4 transition-all duration-300',
                  showAllImages
                    ? 'grid-cols-2 md:grid-cols-3 lg:grid-cols-4'
                    : 'grid-cols-2 md:grid-cols-3 lg:grid-cols-4'
                ]"
              >
                <div
                  v-for="(image, index) in (showAllImages ? excursion.images : excursion.images.slice(0, 8))"
                  :key="index"
                  :class="[
                    'relative aspect-square overflow-hidden rounded-lg cursor-pointer group',
                    index === currentImageIndex && 'ring-2 ring-primary'
                  ]"
                  @click="setCurrentImage(index)"
                >
                  <img
                    :src="image.url"
                    :alt="image.alt || excursion.title"
                    class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
                    @error="handleImageError"
                  />
                  <div class="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-colors" />
                </div>
              </div>
            </section>
          </div>

          <!-- Sidebar -->
          <aside class="space-y-6">
            <!-- Pickup Points -->
            <div v-if="excursion.pickupPoints && excursion.pickupPoints.length > 0" class="bg-card border rounded-lg p-6">
              <div class="flex items-center justify-between mb-4">
                <h3 class="text-xl font-bold text-primary flex items-center gap-2">
                  <MapPin class="w-5 h-5" />
                  Точки отправления
                </h3>
                <button
                  @click="showMapModal = true"
                  class="text-sm text-primary hover:underline flex items-center gap-1"
                  aria-label="Показать маршрут на карте"
                >
                  <MapPin class="w-4 h-4" />
                  Маршрут
                </button>
              </div>
              <div class="space-y-3">
                <div
                  v-for="(point, index) in excursion.pickupPoints"
                  :key="index"
                  class="flex items-center justify-between p-3 bg-muted/50 rounded-lg"
                >
                  <span class="font-medium">{{ point.location }}</span>
                  <span class="text-primary font-semibold">{{ point.price }}</span>
                </div>
              </div>
            </div>

            <!-- Additional Costs -->
            <div v-if="excursion.additionalCosts" class="bg-card border rounded-lg p-6">
              <h3 class="text-xl font-bold mb-4 text-primary flex items-center gap-2">
                <DollarSign class="w-5 h-5" />
                Дополнительные расходы
              </h3>
              <div class="space-y-3">
                <!-- Если это массив -->
                <div
                  v-if="Array.isArray(excursion.additionalCosts)"
                  v-for="(cost, index) in excursion.additionalCosts"
                  :key="index"
                  class="flex items-start justify-between gap-4 p-3 bg-muted/50 rounded-lg"
                >
                  <div class="flex-1">
                    <p class="font-medium text-foreground">{{ cost.description || cost }}</p>
                  </div>
                  <span class="text-primary font-semibold whitespace-nowrap">{{ cost.price || cost }}</span>
                </div>
                <!-- Если это строка -->
                <p v-else class="text-sm text-muted-foreground">{{ excursion.additionalCosts }}</p>
              </div>
            </div>

            <!-- Actions -->
            <div class="bg-card border rounded-lg p-6 sticky top-20">
              <h3 class="text-xl font-bold mb-4 text-primary">Забронировать</h3>
              <div class="space-y-3">
                <button
                  @click="handleAddToCart"
                  class="w-full px-6 py-3 bg-primary text-primary-foreground rounded-lg font-semibold hover:bg-primary/90 transition-colors flex items-center justify-center gap-2"
                >
                  <ShoppingCart class="w-5 h-5" />
                  Добавить в корзину
                </button>
                <a
                  :href="excursion.url"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="w-full px-6 py-3 bg-muted text-foreground rounded-lg font-semibold hover:bg-muted/80 transition-colors flex items-center justify-center gap-2"
                >
                  <ExternalLink class="w-5 h-5" />
                  Подробнее на сайте
                </a>
                <a
                  href="tel:+79885042545"
                  class="w-full px-6 py-3 bg-accent text-accent-foreground rounded-lg font-semibold hover:bg-accent/90 transition-colors flex items-center justify-center gap-2"
                >
                  <Phone class="w-5 h-5" />
                  Позвонить
                </a>
              </div>
            </div>
          </aside>
        </div>

        <!-- Related Excursions -->
        <section v-if="relatedExcursions.length > 0" class="mt-12">
          <h2 class="text-3xl font-bold mb-6 text-primary">Похожие экскурсии</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <ExcursionCard
              v-for="related in relatedExcursions"
              :key="related.id"
              :excursion="related"
            />
          </div>
        </section>
      </div>
    </div>

    <!-- Full Screen Image Modal -->
    <Transition
      enter-active-class="transition ease-out duration-300"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition ease-in duration-200"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="selectedImage"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/95 p-4"
        @click="selectedImage = null"
      >
        <div class="relative max-w-7xl max-h-full">
          <img
            :src="selectedImage"
            :alt="excursion.title"
            class="max-w-full max-h-[90vh] object-contain"
          />
          <button
            @click="selectedImage = null"
            class="absolute top-4 right-4 p-2 rounded-full bg-background/90 hover:bg-background transition-colors"
            aria-label="Закрыть"
          >
            <X class="w-6 h-6" />
          </button>
        </div>
      </div>
    </Transition>

    <!-- Map Route Modal -->
    <Transition
      enter-active-class="transition ease-out duration-300"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition ease-in duration-200"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="showMapModal"
        class="fixed inset-0 z-50 flex items-center justify-center bg-background/95 backdrop-blur-sm p-4"
        @click.self="showMapModal = false"
      >
        <div class="relative w-full max-w-6xl max-h-[90vh] bg-card border rounded-lg overflow-hidden shadow-2xl flex flex-col">
          <!-- Modal Header -->
          <div class="flex items-center justify-between p-4 border-b bg-card">
            <h3 class="text-xl font-bold text-primary flex items-center gap-2">
              <MapPin class="w-5 h-5" />
              Бронирование экскурсии
            </h3>
            <button
              @click="showMapModal = false"
              class="p-2 rounded-lg hover:bg-muted transition-colors"
              aria-label="Закрыть"
            >
              <X class="w-6 h-6" />
            </button>
          </div>

          <!-- Booking Form -->
          <div class="p-4 md:p-6 space-y-4 md:space-y-6 overflow-y-auto flex-1">
            <!-- Количество людей и выбор места встречи -->
            <div class="grid grid-cols-1 md:grid-cols-[2fr_1fr_1fr] gap-3 md:gap-4">
              <!-- Выбор места встречи -->
              <div v-if="excursion?.pickupPoints && excursion.pickupPoints.length > 0" class="relative z-30">
                <label class="block text-sm font-medium text-muted-foreground mb-2">
                  Выберите место встречи
                </label>
                <div class="relative">
                  <button
                    @click="showPickupDropdown = !showPickupDropdown"
                    class="w-full flex items-center justify-between p-3 border rounded-lg hover:bg-muted/50 transition-colors text-left"
                  >
                    <span class="font-medium text-sm truncate">
                      {{ selectedPickupPoint ? `${selectedPickupPoint.location} - ${selectedPickupPoint.price}` : 'Выберите место встречи' }}
                    </span>
                    <ChevronDown :class="['w-5 h-5 transition-transform shrink-0', showPickupDropdown && 'rotate-180']" />
                  </button>

                  <!-- Dropdown -->
                  <Transition
                    enter-active-class="transition ease-out duration-200"
                    enter-from-class="opacity-0 -translate-y-1"
                    enter-to-class="opacity-100 translate-y-0"
                    leave-active-class="transition ease-in duration-150"
                    leave-from-class="opacity-100 translate-y-0"
                    leave-to-class="opacity-0 -translate-y-1"
                  >
                    <div
                      v-if="showPickupDropdown"
                      class="absolute z-50 w-full mt-1 bg-card border rounded-lg shadow-lg max-h-60 overflow-y-auto"
                    >
                      <button
                        v-for="(point, index) in excursion.pickupPoints"
                        :key="index"
                        @click="selectPickupPoint(point)"
                        :class="[
                          'w-full text-left px-4 py-3 hover:bg-primary/10 transition-colors',
                          selectedPickupPoint?.location === point.location && 'bg-primary/20'
                        ]"
                      >
                        <div class="font-medium">{{ point.location }}</div>
                        <div class="text-sm text-primary font-semibold">{{ point.price }}</div>
                      </button>
                    </div>
                  </Transition>
                </div>
              </div>

              <!-- Взрослые -->
              <div>
                <label class="block text-sm font-medium text-muted-foreground mb-2">
                  Взрослый
                </label>
                <div class="flex items-center gap-3 border rounded-lg p-2">
                  <button
                    @click="decrementAdults"
                    :disabled="adultsCount <= 1"
                    class="p-1 rounded hover:bg-muted transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                    aria-label="Уменьшить количество взрослых"
                  >
                    <Minus class="w-4 h-4" />
                  </button>
                  <input
                    v-model.number="adultsCount"
                    type="number"
                    min="1"
                    class="w-12 text-center border-none bg-transparent focus:outline-none"
                  />
                  <button
                    @click="incrementAdults"
                    class="p-1 rounded hover:bg-muted transition-colors"
                    aria-label="Увеличить количество взрослых"
                  >
                    <Plus class="w-4 h-4" />
                  </button>
                </div>
              </div>

              <!-- Дети -->
              <div>
                <label class="block text-sm font-medium text-muted-foreground mb-2">
                  Детский
                </label>
                <div class="flex items-center gap-3 border rounded-lg p-2">
                  <button
                    @click="decrementChildren"
                    :disabled="childrenCount <= 0"
                    class="p-1 rounded hover:bg-muted transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                    aria-label="Уменьшить количество детей"
                  >
                    <Minus class="w-4 h-4" />
                  </button>
                  <input
                    v-model.number="childrenCount"
                    type="number"
                    min="0"
                    class="w-12 text-center border-none bg-transparent focus:outline-none"
                  />
                  <button
                    @click="incrementChildren"
                    class="p-1 rounded hover:bg-muted transition-colors"
                    aria-label="Увеличить количество детей"
                  >
                    <Plus class="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>

            <!-- Карта -->
            <div class="border rounded-lg overflow-hidden" style="height: 300px; min-height: 300px;">
              <MapRoute
                v-if="excursion?.pickupPoints"
                :pickup-points="excursion.pickupPoints"
                :excursion-title="excursion.title"
                @select-point="selectPickupPoint"
              />
            </div>

            <!-- Итого и кнопка -->
            <div class="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-4 pt-4 border-t">
              <div>
                <span class="text-sm text-muted-foreground">Итого:</span>
                <span class="text-2xl font-bold text-primary ml-2">{{ formatPrice(totalPrice) }}</span>
              </div>
              <button
                @click="handleAddToCartFromModal"
                class="px-6 py-3 bg-primary text-primary-foreground rounded-lg font-semibold hover:bg-primary/90 transition-colors flex items-center gap-2"
              >
                <ShoppingCart class="w-5 h-5" />
                В корзину
              </button>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import {
  X,
  ArrowLeft,
  ChevronRight,
  ChevronLeft,
  ChevronDown,
  Clock,
  Tag,
  ImageIcon,
  MapPin,
  DollarSign,
  ShoppingCart,
  ExternalLink,
  Phone,
  Plus,
  Minus,
  ChevronUp
} from 'lucide-vue-next'
import { useExcursions } from '@/composables/useExcursions'
import ExcursionCard from '@/components/ExcursionCard.vue'
import MapRoute from '@/components/MapRoute.vue'

const route = useRoute()
const { loading, error, getExcursionById, loadExcursions, excursions } = useExcursions()

const currentImageIndex = ref(0)
const selectedImage = ref(null)
const showAllImages = ref(false)
const showMapModal = ref(false)

// Данные для бронирования
const adultsCount = ref(1)
const childrenCount = ref(0)
const selectedPickupPoint = ref(null)
const showPickupDropdown = ref(false)

const excursion = computed(() => {
  const id = route.params.id
  return getExcursionById(id)
})

const currentImage = computed(() => {
  if (!excursion.value?.images || excursion.value.images.length === 0) {
    return 'https://placehold.net/800x600'
  }
  return excursion.value.images[currentImageIndex.value]?.url || excursion.value.images[0].url
})

const relatedExcursions = computed(() => {
  if (!excursion.value) return []
  return excursions.value
    .filter(ex =>
      ex.id !== excursion.value.id &&
      ex.category === excursion.value.category
    )
    .slice(0, 3)
})

const nextImage = () => {
  if (excursion.value?.images && currentImageIndex.value < excursion.value.images.length - 1) {
    currentImageIndex.value++
  }
}

const previousImage = () => {
  if (currentImageIndex.value > 0) {
    currentImageIndex.value--
  }
}

const setCurrentImage = (index) => {
  currentImageIndex.value = index
  selectedImage.value = excursion.value.images[index].url
}

const handleImageError = (event) => {
  event.target.src = 'https://placehold.net/800x600'
}

const handleAddToCart = () => {
  // TODO: добавить в store
  console.log('Добавить в корзину:', excursion.value)
  alert('Экскурсия добавлена в корзину!')
}

// Функции для изменения количества
const incrementAdults = () => {
  adultsCount.value++
}

const decrementAdults = () => {
  if (adultsCount.value > 1) {
    adultsCount.value--
  }
}

const incrementChildren = () => {
  childrenCount.value++
}

const decrementChildren = () => {
  if (childrenCount.value > 0) {
    childrenCount.value--
  }
}

// Выбор точки отправления
const selectPickupPoint = (point) => {
  selectedPickupPoint.value = point
  showPickupDropdown.value = false
}

// Расчет итоговой цены
const totalPrice = computed(() => {
  if (!selectedPickupPoint.value) {
    // Если точка не выбрана, используем первую доступную или базовую цену
    const basePrice = excursion.value?.pickupPoints?.[0]?.price || excursion.value?.price || '0'
    const price = parseInt(basePrice.replace(/\D/g, '')) || 0
    return price * adultsCount.value
  }

  const price = parseInt(selectedPickupPoint.value.price.replace(/\D/g, '')) || 0
  return price * adultsCount.value
})

// Форматирование цены
const formatPrice = (price) => {
  return `${price} ₽`
}

// Добавление в корзину из модального окна
const handleAddToCartFromModal = () => {
  if (!selectedPickupPoint.value) {
    alert('Пожалуйста, выберите место встречи')
    return
  }

  const bookingData = {
    excursion: excursion.value,
    adults: adultsCount.value,
    children: childrenCount.value,
    pickupPoint: selectedPickupPoint.value,
    totalPrice: totalPrice.value
  }

  // TODO: добавить в store
  console.log('Добавить в корзину:', bookingData)
  alert('Экскурсия добавлена в корзину!')
  showMapModal.value = false
}

// Инициализация выбранной точки при открытии модального окна
watch(showMapModal, (isOpen) => {
  if (isOpen && excursion.value?.pickupPoints?.length > 0) {
    selectedPickupPoint.value = excursion.value.pickupPoints[0]
    adultsCount.value = 1
    childrenCount.value = 0
    showPickupDropdown.value = false
  }
})

// Закрытие выпадающего списка при клике вне его
const handleClickOutside = (event) => {
  if (showPickupDropdown.value && !event.target.closest('.relative')) {
    showPickupDropdown.value = false
  }
}

onMounted(() => {
  loadExcursions()
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

// Сброс индекса изображения при смене экскурсии
watch(() => route.params.id, () => {
  currentImageIndex.value = 0
  showAllImages.value = false
})

onMounted(() => {
  loadExcursions()
})
</script>

<style scoped>
.prose {
  color: inherit;
}

.prose p {
  margin-top: 0;
  margin-bottom: 1rem;
}

.prose ul {
  margin-top: 0;
  margin-bottom: 1rem;
  padding-left: 1.5rem;
}
</style>
