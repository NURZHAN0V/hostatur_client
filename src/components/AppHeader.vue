<template>
  <header class="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
    <!-- Top Bar -->
    <div class="hidden md:flex items-center justify-between px-4 py-2 bg-primary/10 text-sm">
      <div class="container mx-auto flex items-center justify-between">
        <div class="flex items-center gap-6">
          <a href="tel:+79885042545" class="flex items-center gap-2 hover:text-primary transition-colors">
            <Phone class="w-4 h-4" />
            <span>+7 (988) 504-25-45</span>
          </a>
          <a href="tel:+79189013211" class="flex items-center gap-2 hover:text-primary transition-colors">
            <Phone class="w-4 h-4" />
            <span>+7 (918) 901-32-11</span>
          </a>
        </div>
        <div class="flex items-center gap-4">
          <LanguageSwitcher />
        </div>
      </div>
    </div>

    <!-- Main Navigation -->
    <nav class="container mx-auto px-4">
      <div class="flex h-16 items-center justify-between">
        <!-- Logo -->
        <RouterLink to="/" class="flex items-center gap-2">
          <PalmTree class="w-6 h-6 text-primary flex-shrink-0" />
          <div class="flex flex-col">
            <span class="text-xl font-bold text-primary" style="font-family: 'Leonov SP', serif;">Хостинский отдых</span>
            <span class="text-xs text-muted-foreground">г. Сочи</span>
          </div>
        </RouterLink>

        <!-- Desktop Navigation -->
        <div class="hidden md:flex items-center gap-1">
          <NavLink to="/" :active="$route.name === 'home'">Главная</NavLink>
          <NavDropdown label="О компании">
            <NavDropdownItem to="/about">О нас</NavDropdownItem>
            <NavDropdownItem to="/about#awards">Награды</NavDropdownItem>
          </NavDropdown>
          <NavDropdown label="Экскурсии">
            <NavDropdownItem to="/excursions/sochi">Сочи</NavDropdownItem>
            <NavDropdownItem to="/excursions/abkhazia">Абхазия</NavDropdownItem>
          </NavDropdown>
          <NavLink to="/tourists" :active="$route.name === 'tourists'">Туристам</NavLink>
          <NavDropdown label="Услуги">
            <NavDropdownItem to="/services#guides">Гиды-переводчики</NavDropdownItem>
            <NavDropdownItem to="/services#events">Организация мероприятий</NavDropdownItem>
            <NavDropdownItem to="/services#transfer">Трансфер</NavDropdownItem>
            <NavDropdownItem to="/services#accommodation">Размещение</NavDropdownItem>
          </NavDropdown>
          <NavLink to="/contacts" :active="$route.name === 'contacts'">Контакты</NavLink>
        </div>

        <!-- Right Actions -->
        <div class="flex items-center gap-4">
          <button
            @click="toggleSearch"
            class="hidden md:flex items-center justify-center w-10 h-10 rounded-md hover:bg-accent transition-colors"
            aria-label="Поиск"
          >
            <Search class="w-5 h-5" />
          </button>
          <RouterLink
            to="/cart"
            class="relative flex items-center justify-center w-10 h-10 rounded-md hover:bg-accent transition-colors"
            aria-label="Корзина"
          >
            <ShoppingCart class="w-5 h-5" />
            <span
              v-if="cartCount > 0"
              class="absolute -top-1 -right-1 flex h-5 w-5 items-center justify-center rounded-full bg-primary text-xs font-medium text-primary-foreground"
            >
              {{ cartCount }}
            </span>
          </RouterLink>
          <button
            @click="toggleMobileMenu"
            class="md:hidden flex items-center justify-center w-10 h-10 rounded-md hover:bg-accent transition-colors"
            aria-label="Меню"
          >
            <Menu v-if="!mobileMenuOpen" class="w-5 h-5" />
            <X v-else class="w-5 h-5" />
          </button>
        </div>
      </div>
    </nav>

    <!-- Mobile Menu -->
    <Transition
      enter-active-class="transition ease-out duration-200"
      enter-from-class="opacity-0 -translate-y-1"
      enter-to-class="opacity-100 translate-y-0"
      leave-active-class="transition ease-in duration-150"
      leave-from-class="opacity-100 translate-y-0"
      leave-to-class="opacity-0 -translate-y-1"
    >
      <div v-if="mobileMenuOpen" class="md:hidden border-t bg-background">
        <div class="container mx-auto px-4 py-4 space-y-2">
          <MobileNavLink to="/" @click="closeMobileMenu">Главная</MobileNavLink>
          <MobileNavLink to="/about" @click="closeMobileMenu">О компании</MobileNavLink>
          <MobileNavLink to="/excursions" @click="closeMobileMenu">Экскурсии</MobileNavLink>
          <MobileNavLink to="/tourists" @click="closeMobileMenu">Туристам</MobileNavLink>
          <MobileNavLink to="/services" @click="closeMobileMenu">Услуги</MobileNavLink>
          <MobileNavLink to="/contacts" @click="closeMobileMenu">Контакты</MobileNavLink>
        </div>
      </div>
    </Transition>

    <!-- Search Modal -->
    <SearchModal v-model:open="searchOpen" />
  </header>
</template>

<script setup>
import { ref } from 'vue'
import { RouterLink } from 'vue-router'
import { Phone, Search, ShoppingCart, Menu, X } from 'lucide-vue-next'
import NavLink from './ui/NavLink.vue'
import NavDropdown from './ui/NavDropdown.vue'
import NavDropdownItem from './ui/NavDropdownItem.vue'
import MobileNavLink from './ui/MobileNavLink.vue'
import LanguageSwitcher from './LanguageSwitcher.vue'
import SearchModal from './SearchModal.vue'
import PalmTree from './icons/PalmTree.vue'

const mobileMenuOpen = ref(false)
const searchOpen = ref(false)
const cartCount = ref(0) // TODO: получить из store

const toggleMobileMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value
}

const closeMobileMenu = () => {
  mobileMenuOpen.value = false
}

const toggleSearch = () => {
  searchOpen.value = !searchOpen.value
}
</script>

