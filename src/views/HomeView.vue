<template>
  <div>
    <!-- Hero Section -->
    <section class="relative h-[80vh] min-h-[600px] flex items-center justify-center overflow-hidden">
      <div
        class="absolute inset-0 bg-cover bg-center bg-no-repeat"
        :style="{ backgroundImage: 'url(https://placehold.net/1920x1080)' }"
      >
        <div class="absolute inset-0 bg-gradient-to-b from-black/40 via-black/30 to-black/50" />
      </div>
      
      <div class="relative z-10 container mx-auto px-4 text-center text-white">
        <h1 class="text-5xl md:text-7xl font-bold mb-4 animate-fade-in">
          Приключения и развлечения
        </h1>
        <h2 class="text-3xl md:text-5xl font-bold mb-6 text-accent animate-fade-in-delay">
          Яркий отдых
        </h2>
        <p class="text-xl md:text-2xl mb-8 max-w-2xl mx-auto animate-fade-in-delay-2">
          Экскурсии – трансфер – размещение
        </p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center animate-fade-in-delay-3">
          <RouterLink
            to="/excursions"
            class="px-8 py-4 bg-primary text-primary-foreground rounded-lg font-semibold hover:bg-primary/90 transition-all transform hover:scale-105 shadow-lg"
          >
            Выбрать экскурсию
          </RouterLink>
          <RouterLink
            to="/services"
            class="px-8 py-4 bg-accent text-accent-foreground rounded-lg font-semibold hover:bg-accent/90 transition-all transform hover:scale-105 shadow-lg"
          >
            Наши услуги
          </RouterLink>
        </div>
      </div>
    </section>

    <!-- About Section -->
    <section class="py-20 bg-muted/30">
      <div class="container mx-auto px-4">
        <div class="text-center mb-12">
          <h2 class="text-4xl font-bold mb-4 text-primary">
            Мы раскроем для вас все красоты Сочи и Абхазии
          </h2>
          <p class="text-lg text-muted-foreground max-w-2xl mx-auto">
            Профессиональная организация экскурсий, трансфера и размещения для незабываемого отдыха
          </p>
        </div>

        <!-- Features Grid -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mt-12">
          <FeatureCard
            icon="MapPin"
            title="Экскурсии"
            description="Увлекательные экскурсии по Сочи и Абхазии с опытными гидами"
            link="/excursions"
          />
          <FeatureCard
            icon="Car"
            title="Трансфер"
            description="Комфортный трансфер из аэропорта и между городами"
            link="/services#transfer"
          />
          <FeatureCard
            icon="Hotel"
            title="Размещение"
            description="Подбор и бронирование отелей и гостевых домов"
            link="/services#accommodation"
          />
        </div>
      </div>
    </section>

    <!-- Popular Excursions -->
    <section class="py-20">
      <div class="container mx-auto px-4">
        <div class="text-center mb-12">
          <h2 class="text-4xl font-bold mb-4 text-primary">Популярные экскурсии</h2>
          <p class="text-lg text-muted-foreground">
            Выберите увлекательное путешествие по самым живописным местам
          </p>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="text-center py-12">
          <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
        </div>

        <!-- Excursions Grid -->
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <ExcursionCard
            v-for="excursion in popularExcursions"
            :key="excursion.id"
            :excursion="excursion"
            :in-cart="isInCart(excursion.id)"
            @add-to-cart="handleAddToCart"
          />
        </div>

        <div class="text-center mt-12">
          <RouterLink
            to="/excursions"
            class="inline-flex items-center gap-2 px-8 py-4 bg-primary text-primary-foreground rounded-lg font-semibold hover:bg-primary/90 transition-all"
          >
            Все экскурсии
            <ArrowRight class="w-5 h-5" />
          </RouterLink>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="py-20 bg-primary text-primary-foreground">
      <div class="container mx-auto px-4 text-center">
        <h2 class="text-4xl font-bold mb-4">Готовы начать путешествие?</h2>
        <p class="text-xl mb-8 opacity-90">
          Свяжитесь с нами, и мы поможем организовать незабываемый отдых
        </p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <a
            href="tel:+79885042545"
            class="px-8 py-4 bg-accent text-accent-foreground rounded-lg font-semibold hover:bg-accent/90 transition-all"
          >
            +7 (988) 504-25-45
          </a>
          <RouterLink
            to="/contacts"
            class="px-8 py-4 bg-background text-foreground rounded-lg font-semibold hover:bg-background/90 transition-all"
          >
            Все контакты
          </RouterLink>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { ArrowRight } from 'lucide-vue-next'
import FeatureCard from '@/components/FeatureCard.vue'
import ExcursionCard from '@/components/ExcursionCard.vue'
import { useExcursions } from '@/composables/useExcursions'

const { loading, getPopularExcursions, loadExcursions } = useExcursions()
const cartItems = ref([]) // TODO: подключить к store

const popularExcursions = computed(() => getPopularExcursions(6))

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

<style scoped>
@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in {
  animation: fade-in 0.8s ease-out;
}

.animate-fade-in-delay {
  animation: fade-in 0.8s ease-out 0.2s both;
}

.animate-fade-in-delay-2 {
  animation: fade-in 0.8s ease-out 0.4s both;
}

.animate-fade-in-delay-3 {
  animation: fade-in 0.8s ease-out 0.6s both;
}
</style>
