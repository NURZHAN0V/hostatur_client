import { createRouter, createWebHistory } from 'vue-router'
import Layout from '@/components/Layout.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: Layout,
      children: [
        {
          path: '',
          name: 'home',
          component: () => import('@/views/HomeView.vue'),
        },
        {
          path: 'about',
          name: 'about',
          component: () => import('@/views/AboutView.vue'),
        },
        {
          path: 'excursions',
          name: 'excursions',
          component: () => import('@/views/ExcursionsView.vue'),
        },
        {
          path: 'excursions/detail/:id',
          name: 'excursion-detail',
          component: () => import('@/views/ExcursionDetailView.vue'),
        },
        {
          path: 'excursions/:category',
          name: 'excursions-category',
          component: () => import('@/views/ExcursionsView.vue'),
        },
        {
          path: 'services',
          name: 'services',
          component: () => import('@/views/ServicesView.vue'),
        },
        {
          path: 'tourists',
          name: 'tourists',
          component: () => import('@/views/TouristsView.vue'),
        },
        {
          path: 'contacts',
          name: 'contacts',
          component: () => import('@/views/ContactsView.vue'),
        },
        {
          path: 'cart',
          name: 'cart',
          component: () => import('@/views/CartView.vue'),
        },
      ],
    },
  ],
})

export default router
