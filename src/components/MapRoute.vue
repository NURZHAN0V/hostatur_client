<template>
  <div ref="mapContainer" class="w-full h-full rounded-lg overflow-hidden"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'

const props = defineProps({
  pickupPoints: {
    type: Array,
    default: () => []
  },
  excursionTitle: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['selectPoint'])

const mapContainer = ref(null)
let map = null
let markers = []
let routePolyline = null

// Координаты для локаций (примерные координаты для Сочи и окрестностей)
const locationCoordinates = {
  'Сочи': [43.5855, 39.7231],
  'Хосты': [43.5200, 39.8500],
  'Адлера': [43.4283, 39.9239],
  'Адлер': [43.4283, 39.9239],
  'Лазаревское': [43.9000, 39.3333],
  'Лоо': [43.7167, 39.6000],
  'Дагомыс': [43.6667, 39.6667],
  'Красная Поляна': [43.6833, 40.2833],
  'Роза Хутор': [43.6833, 40.2833],
  'Гагра': [43.3000, 40.2500],
  'Пицунда': [43.1667, 40.3333],
  'Новый Афон': [43.0833, 40.8333],
  'Сухум': [43.0000, 41.0167],
  'Псоу': [43.3833, 40.0167]
}

// Загружаем Leaflet из CDN
const loadLeaflet = () => {
  return new Promise((resolve) => {
    if (window.L) {
      resolve(window.L)
      return
    }

    // Загружаем CSS
    const link = document.createElement('link')
    link.rel = 'stylesheet'
    link.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css'
    link.integrity = 'sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY='
    link.crossOrigin = ''
    document.head.appendChild(link)

    // Загружаем JS
    const script = document.createElement('script')
    script.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js'
    script.integrity = 'sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo='
    script.crossOrigin = ''
    script.onload = () => resolve(window.L)
    document.head.appendChild(script)
  })
}

// Получаем координаты для локации
const getLocationCoordinates = (locationName) => {
  const normalizedName = locationName.trim()
  
  // Прямое совпадение
  if (locationCoordinates[normalizedName]) {
    return locationCoordinates[normalizedName]
  }

  // Поиск по частичному совпадению
  for (const [key, coords] of Object.entries(locationCoordinates)) {
    if (normalizedName.toLowerCase().includes(key.toLowerCase()) || 
        key.toLowerCase().includes(normalizedName.toLowerCase())) {
      return coords
    }
  }

  // Если не найдено, возвращаем координаты Сочи по умолчанию
  return [43.5855, 39.7231]
}

// Инициализация карты
const initMap = async () => {
  if (!mapContainer.value) return

  const L = await loadLeaflet()

  // Создаем карту
  map = L.map(mapContainer.value, {
    zoomControl: false, // Отключаем стандартные элементы управления
    scrollWheelZoom: true
  })

  // Добавляем элементы управления зумом в правый верхний угол
  L.control.zoom({
    position: 'topright'
  }).addTo(map)

  // Добавляем тайлы OpenStreetMap
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
    maxZoom: 19
  }).addTo(map)

  // Получаем координаты всех точек
  const points = props.pickupPoints.map(point => ({
    location: point.location,
    price: point.price,
    coordinates: getLocationCoordinates(point.location)
  }))

  if (points.length === 0) {
    // Если точек нет, показываем Сочи
    map.setView([43.5855, 39.7231], 12)
    return
  }

  // Добавляем маркеры
  points.forEach((point, index) => {
    const originalPoint = props.pickupPoints[index]
    
    const marker = L.marker(point.coordinates)
      .addTo(map)
      .bindPopup(`
        <div class="p-2">
          <strong>${point.location}</strong><br>
          <span class="text-primary font-semibold">${point.price}</span>
        </div>
      `)
      .on('click', () => {
        // При клике на маркер выбираем соответствующую точку
        if (originalPoint) {
          emit('selectPoint', originalPoint)
        }
      })

    markers.push(marker)
  })

  // Вычисляем границы для отображения всех точек
  if (points.length > 0) {
    const bounds = points.map(p => p.coordinates)
    map.fitBounds(bounds, { padding: [50, 50] })

    // Если только одна точка, устанавливаем зум
    if (points.length === 1) {
      map.setZoom(13)
    }

    // Если точек больше одной, рисуем маршрут (полилинию)
    if (points.length > 1) {
      const routeCoordinates = points.map(p => p.coordinates)
      routePolyline = L.polyline(routeCoordinates, {
        color: '#3b82f6',
        weight: 4,
        opacity: 0.7,
        smoothFactor: 1
      }).addTo(map)
    }
  }
}

// Очистка карты
const destroyMap = () => {
  if (map) {
    markers.forEach(marker => map.removeLayer(marker))
    markers = []
    
    if (routePolyline) {
      map.removeLayer(routePolyline)
      routePolyline = null
    }
    
    map.remove()
    map = null
  }
}

watch(() => props.pickupPoints, () => {
  if (map) {
    destroyMap()
    initMap()
  }
}, { deep: true })

onMounted(() => {
  initMap()
})

onUnmounted(() => {
  destroyMap()
})
</script>

<style scoped>
/* Стили для контейнера карты */
:deep(.leaflet-container) {
  font-family: inherit;
  z-index: 1;
}

:deep(.leaflet-map-pane) {
  z-index: 1;
}

:deep(.leaflet-tile-pane) {
  z-index: 1;
}

:deep(.leaflet-overlay-pane) {
  z-index: 2;
}

:deep(.leaflet-shadow-pane) {
  z-index: 3;
}

:deep(.leaflet-marker-pane) {
  z-index: 4;
}

:deep(.leaflet-tooltip-pane) {
  z-index: 5;
}

:deep(.leaflet-popup-pane) {
  z-index: 6;
}

/* Элементы управления зумом должны быть ниже поля выбора */
:deep(.leaflet-control-zoom) {
  z-index: 10 !important;
}

:deep(.leaflet-control) {
  z-index: 10 !important;
}

:deep(.leaflet-popup-content-wrapper) {
  border-radius: 8px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

:deep(.leaflet-popup-content) {
  margin: 0;
  padding: 0;
}
</style>

