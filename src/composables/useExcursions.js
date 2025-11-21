import { ref, computed } from 'vue'

const excursions = ref([])
const loading = ref(false)
const error = ref(null)

export function useExcursions() {
  const loadExcursions = async () => {
    if (excursions.value.length > 0) {
      return // Данные уже загружены
    }

    loading.value = true
    error.value = null

    try {
      const response = await fetch('/json/excursions_complete.json')
      if (!response.ok) {
        throw new Error('Не удалось загрузить данные об экскурсиях')
      }
      const data = await response.json()
      excursions.value = data.excursions || []
    } catch (err) {
      error.value = err.message
      console.error('Ошибка загрузки экскурсий:', err)
    } finally {
      loading.value = false
    }
  }

  // Определяем категорию экскурсии (Сочи или Абхазия)
  const getCategory = (excursion) => {
    const title = (excursion.title || '').toLowerCase()
    const description = (excursion.description || '').toLowerCase()
    const url = (excursion.url || '').toLowerCase()

    // Ключевые слова для Абхазии
    const abkhaziaKeywords = [
      'абхазия', 'абхаз', 'гагра', 'пицунда', 'новый афон', 'новоафон',
      'сухум', 'рица', 'псху', 'бзыбь', 'псырцха'
    ]

    // Проверяем наличие ключевых слов
    const text = `${title} ${description} ${url}`
    const isAbkhazia = abkhaziaKeywords.some(keyword => text.includes(keyword))

    return isAbkhazia ? 'abkhazia' : 'sochi'
  }

  // Создаем ID из URL (извлекаем slug)
  const createIdFromUrl = (url) => {
    if (!url) return Math.random().toString(36).substr(2, 9)
    
    try {
      // Извлекаем последнюю часть пути перед .html
      const urlObj = new URL(url)
      const pathParts = urlObj.pathname.split('/').filter(Boolean)
      const lastPart = pathParts[pathParts.length - 1] || ''
      
      // Убираем расширение .html и возвращаем slug
      const slug = lastPart.replace(/\.html$/, '').replace(/-detail$/, '')
      return slug || Math.random().toString(36).substr(2, 9)
    } catch {
      // Если URL некорректный, создаем slug из строки
      const match = url.match(/\/([^/]+)\.html/)
      if (match) {
        return match[1].replace(/-detail$/, '')
      }
      return Math.random().toString(36).substr(2, 9)
    }
  }

  // Форматируем экскурсию для отображения
  const formatExcursion = (excursion, index) => {
    const mainImage = excursion.images?.find(img => img.is_main) || excursion.images?.[0]
    
    return {
      id: createIdFromUrl(excursion.url) || `excursion-${index}`,
      title: excursion.title?.replace(/^Экскурсии\s*:\s*/i, '') || 'Экскурсия',
      description: excursion.description || '',
      price: excursion.price || 'Цена по запросу',
      duration: excursion.duration || '',
      image: mainImage?.url || 'https://placehold.net/400x300',
      images: excursion.images || [],
      category: getCategory(excursion),
      url: excursion.url,
      pickupPoints: excursion.pickup_points || [],
      content: excursion.content || {},
      additionalCosts: excursion.additional_costs || null,
    }
  }

  const formattedExcursions = computed(() => {
    return excursions.value
      .filter(ex => {
        // Фильтруем некорректные записи
        return ex.title && 
               !ex.title.includes('404') && 
               !ex.title.includes('не существует')
      })
      .map((ex, index) => formatExcursion(ex, index))
  })

  const excursionsByCategory = computed(() => {
    const result = {
      all: formattedExcursions.value,
      sochi: formattedExcursions.value.filter(ex => ex.category === 'sochi'),
      abkhazia: formattedExcursions.value.filter(ex => ex.category === 'abkhazia'),
    }
    return result
  })

  const getExcursionById = (id) => {
    // Ищем по ID (slug)
    let found = formattedExcursions.value.find(ex => ex.id === id)
    
    // Если не найдено, пробуем найти по URL (для обратной совместимости)
    if (!found && id.includes('http')) {
      found = formattedExcursions.value.find(ex => ex.url === id)
    }
    
    // Если все еще не найдено, пробуем найти по части URL
    if (!found) {
      const slugFromId = id.split('/').pop()?.replace(/\.html$/, '').replace(/-detail$/, '')
      if (slugFromId) {
        found = formattedExcursions.value.find(ex => ex.id === slugFromId)
      }
    }
    
    return found
  }

  const getPopularExcursions = (limit = 6) => {
    return formattedExcursions.value.slice(0, limit)
  }

  return {
    excursions: formattedExcursions,
    excursionsByCategory,
    loading,
    error,
    loadExcursions,
    getExcursionById,
    getPopularExcursions,
  }
}

