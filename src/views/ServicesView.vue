<template>
  <div class="py-12">
    <div class="container mx-auto px-4">
      <!-- Page Header -->
      <div class="text-center mb-12">
        <h1 class="text-4xl md:text-5xl font-bold mb-4 text-primary">Наши услуги</h1>
        <p class="text-lg text-muted-foreground max-w-2xl mx-auto">
          Полный спектр услуг для организации вашего идеального отдыха
        </p>
      </div>

      <!-- Services Grid -->
      <div class="space-y-16">
        <ServiceSection
          id="guides"
          icon="Users"
          title="Услуги гидов-переводчиков"
          description="Профессиональные гиды с опытом работы и знанием нескольких языков"
          features="Многоязычные гиды, Индивидуальные и групповые экскурсии, Профессиональные знания истории и культуры"
        />
        <ServiceSection
          id="events"
          icon="Calendar"
          title="Организация мероприятий"
          description="Организация корпоративных мероприятий, свадеб и праздников"
          features="Корпоративные мероприятия, Свадебные торжества, Праздничные программы"
        />
        <ServiceSection
          id="transfer"
          icon="Car"
          title="Трансфер"
          description="Комфортный трансфер из аэропорта, вокзала и между городами"
          features="Трансфер из аэропорта, Междугородние перевозки, Комфортабельные автомобили"
        />
        <ServiceSection
          id="accommodation"
          icon="Hotel"
          title="Размещение"
          description="Подбор и бронирование отелей, гостевых домов и апартаментов"
          features="Отели и гостевые дома, Апартаменты, Помощь в выборе"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import ServiceSection from '@/components/ServiceSection.vue'
</script>

