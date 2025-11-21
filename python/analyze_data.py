"""
Скрипт для анализа и переклассификации уже собранных данных
"""

import json
import re
from typing import Dict, List


def classify_page(page: Dict) -> str:
    """Классифицировать страницу по содержимому"""
    url = page.get('url', '').lower()
    title = page.get('title', '').lower()
    content = page.get('content', {})
    paragraphs = ' '.join(content.get('paragraphs', [])).lower()
    headings = ' '.join([h.get('text', '') for h in content.get('headings', [])]).lower()
    
    full_text = f"{url} {title} {paragraphs} {headings}"
    
    # Ключевые слова для экскурсий
    excursion_keywords = [
        'экскурс', 'excursion', '/ekskursii/', 'маршрут', 'roza', 'gazprom', 
        'olimp', 'ritsa', 'afon', 'vodopad', 'delfinariy', 'akvapark', 
        'красная поляна', 'абхазия', 'сочи', 'обзорная', 'кольцо', 
        'водопад', 'пещера', 'монастырь', 'дач', 'чай', 'ахун', 'агур'
    ]
    
    # Ключевые слова для услуг
    service_keywords = [
        'услуг', 'service', '/uslugi/', 'gid', 'переводчик', 'гид', 
        'transfer', 'трансфер', 'размещение', 'razmeshchenie', 
        'мероприятие', 'meropriyatie', 'организация'
    ]
    
    # Ключевые слова для контактов
    contact_keywords = [
        'контакт', 'contact', 'телефон', 'адрес', 'email', 'почта'
    ]
    
    excursion_score = sum(1 for keyword in excursion_keywords if keyword in full_text)
    service_score = sum(1 for keyword in service_keywords if keyword in full_text)
    contact_score = sum(1 for keyword in contact_keywords if keyword in full_text)
    
    # Проверяем наличие цены или длительности (признак экскурсии)
    has_price = bool(re.search(r'\d+\s*(руб|₽|рублей)', full_text, re.IGNORECASE))
    has_duration = bool(re.search(r'\d+\s*(час|часа|часов|день|дня|дней)', full_text, re.IGNORECASE))
    
    if has_price or has_duration:
        excursion_score += 2
    
    # Определяем тип
    if excursion_score > service_score and excursion_score > contact_score and excursion_score > 0:
        return 'excursion'
    elif service_score > contact_score and service_score > 0:
        return 'service'
    elif contact_score > 0:
        return 'contact'
    else:
        return 'page'


def reclassify_data(input_file: str = "../parsed_data.json", output_file: str = "../parsed_data_classified.json"):
    """Переклассифицировать данные из JSON файла"""
    
    print("Загрузка данных...")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Создаем новую структуру
    new_data = {
        'pages': [],
        'excursions': [],
        'services': [],
        'contacts': {},
        'navigation': [],
        'images': data.get('images', []),
        'metadata': data.get('metadata', {})
    }
    
    print("Классификация страниц...")
    pages = data.get('pages', [])
    total = len(pages)
    
    for i, page in enumerate(pages, 1):
        page_type = classify_page(page)
        
        if page_type == 'excursion':
            # Преобразуем в формат экскурсии
            excursion = {
                'url': page.get('url'),
                'title': page.get('title'),
                'description': page.get('description'),
                'content': page.get('content'),
                'images': page.get('images', []),
                'price': None,
                'duration': None,
                'pickup_points': None,
                'additional_costs': None
            }
            
            # Собираем весь текст для поиска
            paragraphs = ' '.join(page.get('content', {}).get('paragraphs', []))
            lists_text = ' '.join([' '.join(lst) if isinstance(lst, list) else str(lst) for lst in page.get('content', {}).get('lists', [])])
            divs_text = ' '.join(page.get('content', {}).get('divs_text', []))
            spans_text = ' '.join(page.get('content', {}).get('spans_text', []))
            full_text = f"{paragraphs} {lists_text} {divs_text} {spans_text}"
            
            # Ищем цену (улучшенные паттерны)
            price_patterns = [
                r'Цена\s+(\d+[\s\d]*)\s*(руб|₽)',
                r'(\d+)\s*руб\s*$',
                r'от\s+(\d+)\s*(руб|₽)',
            ]
            for pattern in price_patterns:
                price_match = re.search(pattern, full_text, re.IGNORECASE | re.MULTILINE)
                if price_match:
                    excursion['price'] = price_match.group(0).strip()
                    break
            
            # Ищем длительность
            duration_patterns = [
                r'Продолжительность[:\s]+(\d+[\s\-]?(час|часа|часов|ч|день|дня|дней))',
                r'(\d+)\s*(час|часа|часов|ч)\s*$',
                r'(\d+)\s*ч\b',
            ]
            for pattern in duration_patterns:
                duration_match = re.search(pattern, full_text, re.IGNORECASE)
                if duration_match:
                    excursion['duration'] = duration_match.group(0).strip()
                    break
            
            # Ищем точки посадки - улучшенные паттерны
            pickup_points = []
            
            # Паттерн 1: "Отправление из Сочи - 3000р.взр./ 2500р.дет.(7-14)"
            pickup_pattern1_adult_child = r'Отправление\s+из\s+([А-Яа-я]+)\s*[-–]\s*(\d+)р\.взр\./\s*(\d+)р\.дет\.\(([^)]+)\)'
            matches1_ac = re.findall(pickup_pattern1_adult_child, full_text, re.IGNORECASE)
            for match in matches1_ac:
                if match[0] not in [p['location'] for p in pickup_points]:
                    pickup_points.append({
                        'location': match[0],
                        'price_adult': f"{match[1]}р.",
                        'price_child': f"{match[2]}р.",
                        'child_age': match[3],
                        'price': f"{match[1]}р. взр. / {match[2]}р. дет. ({match[3]})"
                    })
            
            # Паттерн 1.5: "Отправление из Сочи - 4000 р."
            pickup_pattern1 = r'Отправление\s+из\s+([А-Яа-я]+)\s*[-–]\s*(\d+)\s*[р\.]'
            matches1 = re.findall(pickup_pattern1, full_text, re.IGNORECASE)
            for match in matches1:
                if match[0] not in [p['location'] for p in pickup_points]:
                    pickup_points.append({
                        'location': match[0],
                        'price': f"{match[1]} р."
                    })
            
            # Паттерн 2: "из Сочи - 4000 р."
            if not pickup_points:
                pickup_pattern2 = r'из\s+([А-Яа-я]+)\s*[-–]\s*(\d+)\s*[р\.]'
                matches2 = re.findall(pickup_pattern2, full_text, re.IGNORECASE)
                for match in matches2:
                    if match[0] not in [p['location'] for p in pickup_points]:
                        pickup_points.append({
                            'location': match[0],
                            'price': f"{match[1]} р."
                        })
            
            if pickup_points:
                excursion['pickup_points'] = pickup_points
            
            # Ищем дополнительные расходы - улучшенные паттерны
            additional_costs = []
            
            # Паттерн 1: "4000 р. / 3000 р. (с 5 лет до 9 лет вкл.) / 1200 р. (тариф "Малыш" - до 4 лет вкл.) - билет в аквапарк"
            # Улучшенный паттерн с более гибким поиском
            cost_pattern1 = r'(\d+\s*[р\.]+)\s*[/–]\s*(\d+\s*[р\.]+)?\s*\([^)]+\)\s*[/–]?\s*(\d+\s*[р\.]+)?\s*\([^)]+\)\s*–\s*([^\.\n]+)'
            cost_matches1 = re.findall(cost_pattern1, full_text, re.IGNORECASE)
            for match in cost_matches1:
                price_str = match[0].strip()
                if match[1]:
                    price_str += f" / {match[1].strip()}"
                if match[2]:
                    price_str += f" / {match[2].strip()}"
                desc = match[3].strip() if len(match) > 3 else ''
                if desc and desc not in [c.get('description', '') for c in additional_costs]:
                    additional_costs.append({
                        'price': price_str,
                        'description': desc
                    })
            
            # Паттерн 1.5: Более простой вариант "4000 р. / 3000 р. (с 5 лет) / 1200 р. (тариф Малыш) - билет"
            cost_pattern1_5 = r'(\d+\s*[р\.]+)\s*[/–]\s*(\d+\s*[р\.]+)?\s*\([^)]+\)\s*[/–]?\s*(\d+\s*[р\.]+)?\s*\([^)]+\)\s*–\s*([^\.\n]+)'
            cost_matches1_5 = re.findall(cost_pattern1_5, full_text, re.IGNORECASE | re.DOTALL)
            for match in cost_matches1_5:
                price_str = match[0].strip()
                if match[1]:
                    price_str += f" / {match[1].strip()}"
                if match[2]:
                    price_str += f" / {match[2].strip()}"
                desc = match[3].strip() if len(match) > 3 else ''
                if desc and desc not in [c.get('description', '') for c in additional_costs]:
                    additional_costs.append({
                        'price': price_str,
                        'description': desc
                    })
            
            # Паттерн 2: "4000 р. / 3000 р. (с 5 лет до 9 лет вкл.) - билет"
            cost_pattern2 = r'(\d+\s*[р\.]+)\s*[/–]\s*(\d+\s*[р\.]+)?\s*\([^)]+\)\s*–\s*([^\.\n]+)'
            cost_matches2 = re.findall(cost_pattern2, full_text, re.IGNORECASE | re.DOTALL)
            for match in cost_matches2:
                price_str = match[0].strip()
                if match[1]:
                    price_str += f" / {match[1].strip()}"
                desc = match[2].strip() if len(match) > 2 else ''
                if desc and desc not in [c.get('description', '') for c in additional_costs]:
                    additional_costs.append({
                        'price': price_str,
                        'description': desc
                    })
            
            # Паттерн 2.5: Ищем после "Дополнительные расходы" напрямую (с учетом экранированных кавычек)
            if 'Дополнительные расходы' in full_text:
                # Ищем текст после "Дополнительные расходы"
                after_costs = full_text.split('Дополнительные расходы')[-1]
                # Ищем паттерн с несколькими ценами (учитываем экранированные кавычки)
                cost_pattern2_5 = r'(\d+\s*[р\.]+)\s*[/–]\s*(\d+\s*[р\.]+)?\s*\([^)]+\)\s*[/–]?\s*(\d+\s*[р\.]+)?\s*\([^)]+\)\s*–\s*([^\.\n]+)'
                cost_matches2_5 = re.findall(cost_pattern2_5, after_costs, re.IGNORECASE | re.DOTALL)
                for match in cost_matches2_5:
                    price_str = match[0].strip()
                    if match[1]:
                        price_str += f" / {match[1].strip()}"
                    if match[2]:
                        price_str += f" / {match[2].strip()}"
                    desc = match[3].strip() if len(match) > 3 else ''
                    if desc and desc not in [c.get('description', '') for c in additional_costs]:
                        additional_costs.append({
                            'price': price_str,
                            'description': desc
                        })
                
                # Альтернативный паттерн: ищем просто строку с ценами и описанием (более гибкий)
                # Паттерн: "4000 р. / 3000 р. (с 5 лет до 9 лет вкл.) / 1200 р. (тариф "Малыш" - до 4 лет вкл.) - билет в аквапарк"
                # Используем более простой подход - ищем строку целиком
                cost_line_pattern = r'(\d+\s*[р\.]+)\s*[/–]\s*(\d+\s*[р\.]+)\s*\([^)]+\)\s*[/–]\s*(\d+\s*[р\.]+)\s*\([^)]+\)\s*–\s*([^\.\n]+)'
                cost_line_matches = re.findall(cost_line_pattern, after_costs[:1000], re.IGNORECASE | re.DOTALL)
                for match in cost_line_matches:
                    price_str = f"{match[0].strip()} / {match[1].strip()} / {match[2].strip()}"
                    desc = match[3].strip() if len(match) > 3 else ''
                    # Очищаем описание от лишних символов
                    desc = desc.replace('\\"', '"').replace('\\n', ' ').replace('- 3 часа купания', '').strip()
                    if desc and 'билет' in desc.lower() and desc not in [c.get('description', '') for c in additional_costs]:
                        additional_costs.append({
                            'price': price_str,
                            'description': desc
                        })
            
            # Паттерн 3: Простые дополнительные расходы "800 р. - обед"
            simple_cost_pattern = r'(\d+\s*[р\.]+)\s*–\s*([^\.\n]+)'
            simple_matches = re.findall(simple_cost_pattern, full_text, re.IGNORECASE)
            for match in simple_matches:
                desc = match[1].strip()
                if desc and desc not in [c.get('description', '') for c in additional_costs]:
                    # Проверяем, что это действительно дополнительный расход
                    if 'обед' in desc.lower() or 'канат' in desc.lower() or 'билет' in desc.lower() or 'тариф' in desc.lower() or 'дегустация' in desc.lower():
                        additional_costs.append({
                            'price': match[0].strip(),
                            'description': desc
                        })
            
            if additional_costs:
                excursion['additional_costs'] = additional_costs
            
            new_data['excursions'].append(excursion)
        elif page_type == 'service':
            new_data['services'].append(page)
        elif page_type == 'contact':
            if page.get('contacts'):
                new_data['contacts'].update(page.get('contacts'))
            new_data['pages'].append(page)
        else:
            new_data['pages'].append(page)
        
        if i % 10 == 0:
            print(f"Обработано: {i}/{total}")
    
    # Добавляем уже существующие экскурсии и услуги
    new_data['excursions'].extend(data.get('excursions', []))
    new_data['services'].extend(data.get('services', []))
    if data.get('contacts'):
        new_data['contacts'].update(data.get('contacts', {}))
    
    # Сохраняем результат
    print(f"\nСохранение в {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, ensure_ascii=False, indent=2)
    
    # Статистика
    print("\n=== Статистика ===")
    print(f"Страниц: {len(new_data['pages'])}")
    print(f"Экскурсий: {len(new_data['excursions'])}")
    print(f"Услуг: {len(new_data['services'])}")
    print(f"Изображений: {len(new_data['images'])}")
    print(f"Контактная информация: {len(new_data['contacts'])} полей")
    
    # Примеры экскурсий
    if new_data['excursions']:
        print("\n=== Примеры экскурсий ===")
        for exc in new_data['excursions'][:5]:
            print(f"- {exc.get('title', 'Без названия')}")


if __name__ == "__main__":
    reclassify_data()

