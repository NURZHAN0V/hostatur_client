<template>
  <div class="py-12">
    <div class="container mx-auto px-4">
      <h1 class="text-4xl font-bold mb-8 text-primary">Корзина</h1>

      <div v-if="cartItems.length === 0" class="text-center py-12">
        <ShoppingCart class="w-16 h-16 mx-auto mb-4 text-muted-foreground" />
        <p class="text-lg text-muted-foreground mb-4">Ваша корзина пуста</p>
        <RouterLink
          to="/excursions"
          class="inline-flex items-center gap-2 px-6 py-3 bg-primary text-primary-foreground rounded-lg font-semibold hover:bg-primary/90 transition-colors"
        >
          Выбрать экскурсию
        </RouterLink>
      </div>

      <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div class="lg:col-span-2 space-y-4">
          <div
            v-for="item in cartItems"
            :key="item.id"
            class="bg-card border rounded-lg p-6 flex gap-4"
          >
            <img
              :src="item.image"
              :alt="item.title"
              class="w-24 h-24 object-cover rounded-lg"
            />
            <div class="flex-1">
              <h3 class="font-semibold mb-2">{{ item.title }}</h3>
              <p class="text-sm text-muted-foreground mb-4">{{ item.description }}</p>
              <div class="flex items-center justify-between">
                <span class="font-semibold text-primary">{{ item.price }}</span>
                <button
                  @click="removeItem(item.id)"
                  class="text-destructive hover:text-destructive/80 transition-colors"
                >
                  Удалить
                </button>
              </div>
            </div>
          </div>
        </div>

        <div class="lg:col-span-1">
          <div class="bg-card border rounded-lg p-6 sticky top-20">
            <h2 class="text-xl font-bold mb-4">Итого</h2>
            <div class="space-y-2 mb-6">
              <div class="flex justify-between">
                <span>Товаров:</span>
                <span>{{ cartItems.length }}</span>
              </div>
              <div class="flex justify-between text-lg font-semibold">
                <span>Сумма:</span>
                <span class="text-primary">{{ total }}</span>
              </div>
            </div>
            <button
              class="w-full px-6 py-3 bg-primary text-primary-foreground rounded-lg font-semibold hover:bg-primary/90 transition-colors"
            >
              Оформить заказ
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { RouterLink } from 'vue-router'
import { ShoppingCart } from 'lucide-vue-next'

const cartItems = ref([])

const removeItem = (id) => {
  cartItems.value = cartItems.value.filter(item => item.id !== id)
}

const total = ref('0 ₽') // TODO: вычислить сумму
</script>

