<template>
  <div class="py-12">
    <div class="container mx-auto px-4">
      <div class="text-center mb-12">
        <h1 class="text-4xl md:text-5xl font-bold mb-4 text-primary">Туристам</h1>
        <p class="text-lg text-muted-foreground max-w-2xl mx-auto">
          Полезная информация для вашего комфортного отдыха
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
        <InfoCard
          title="Как забронировать"
          description="Просто выберите экскурсию или услугу и свяжитесь с нами по телефону или через форму обратной связи"
        />
        <InfoCard
          title="Оплата"
          description="Оплата производится наличными или банковской картой. Возможна предоплата для групповых экскурсий"
        />
        <InfoCard
          title="Отмена бронирования"
          description="Вы можете отменить бронирование не менее чем за 24 часа до начала экскурсии"
        />
        <InfoCard
          title="Что взять с собой"
          description="Рекомендуем взять удобную обувь, головной убор, солнцезащитный крем и фотоаппарат"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import InfoCard from '@/components/InfoCard.vue'
</script>

