<template>
  <footer class="border-t bg-muted/50">
    <div class="container mx-auto px-4 py-12">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
        <!-- О компании -->
        <div>
          <h3 class="font-semibold mb-4 text-primary">О компании</h3>
          <ul class="space-y-2 text-sm">
            <li>
              <RouterLink to="/about" class="hover:text-primary transition-colors">
                О нас
              </RouterLink>
            </li>
            <li>
              <RouterLink to="/about#awards" class="hover:text-primary transition-colors">
                Награды
              </RouterLink>
            </li>
          </ul>
        </div>

        <!-- Экскурсии -->
        <div>
          <h3 class="font-semibold mb-4 text-primary">Экскурсии</h3>
          <ul class="space-y-2 text-sm">
            <li>
              <RouterLink to="/excursions/sochi" class="hover:text-primary transition-colors">
                Экскурсии по Сочи
              </RouterLink>
            </li>
            <li>
              <RouterLink to="/excursions/abkhazia" class="hover:text-primary transition-colors">
                Экскурсии в Абхазию
              </RouterLink>
            </li>
          </ul>
        </div>

        <!-- Услуги -->
        <div>
          <h3 class="font-semibold mb-4 text-primary">Услуги</h3>
          <ul class="space-y-2 text-sm">
            <li>
              <RouterLink to="/services#guides" class="hover:text-primary transition-colors">
                Гиды-переводчики
              </RouterLink>
            </li>
            <li>
              <RouterLink to="/services#transfer" class="hover:text-primary transition-colors">
                Трансфер
              </RouterLink>
            </li>
            <li>
              <RouterLink to="/services#accommodation" class="hover:text-primary transition-colors">
                Размещение
              </RouterLink>
            </li>
          </ul>
        </div>

        <!-- Контакты -->
        <div>
          <h3 class="font-semibold mb-4 text-primary">Контакты</h3>
          <ul class="space-y-2 text-sm">
            <li>
              <a href="tel:+79885042545" class="flex items-center gap-2 hover:text-primary transition-colors">
                <Phone class="w-4 h-4" />
                +7 (988) 504-25-45
              </a>
            </li>
            <li>
              <a href="tel:+79189013211" class="flex items-center gap-2 hover:text-primary transition-colors">
                <Phone class="w-4 h-4" />
                +7 (918) 901-32-11
              </a>
            </li>
            <li>
              <RouterLink to="/contacts" class="hover:text-primary transition-colors">
                Все контакты
              </RouterLink>
            </li>
          </ul>
        </div>
      </div>

      <div class="mt-8 pt-8 border-t text-center text-sm text-muted-foreground">
        <p>&copy; {{ currentYear }} Хостинский отдых г. Сочи. Все права защищены.</p>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import { Phone } from 'lucide-vue-next'

const currentYear = computed(() => new Date().getFullYear())
</script>

