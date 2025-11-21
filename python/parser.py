"""
Парсер сайта hostaotdykh.ru
Извлекает всю информацию с сайта и сохраняет в JSON
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from urllib.parse import urljoin, urlparse
from typing import Dict, List, Set
import time
import os


class SiteParser:
    """Класс для парсинга сайта hostaotdykh.ru"""
    
    def __init__(self, base_url: str = "https://hostaotdykh.ru"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.visited_urls: Set[str] = set()
        self.data: Dict = {
            'pages': [],
            'excursions': [],
            'services': [],
            'contacts': {},
            'navigation': [],
            'images': [],
            'metadata': {}
        }
        
    def get_page(self, url: str) -> BeautifulSoup:
        """Получить и распарсить страницу"""
        try:
            print(f"Парсинг: {url}")
            response = self.session.get(url, timeout=10)
            response.encoding = 'utf-8'
            response.raise_for_status()
            return BeautifulSoup(response.text, 'lxml')
        except Exception as e:
            print(f"Ошибка при загрузке {url}: {e}")
            return None
    
    def extract_text_content(self, soup: BeautifulSoup) -> Dict:
        """Извлечь текстовый контент со страницы"""
        # НЕ удаляем скрипты сразу - сначала извлечем данные из data-атрибутов
        # Удаляем только стили
        for style in soup(["style", "link"]):
            style.decompose()
        
        # Извлекаем заголовок
        title = soup.find('title')
        title_text = title.get_text(strip=True) if title else ""
        
        # Извлекаем мета-описание
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        description = meta_desc.get('content', '') if meta_desc else ""
        
        # Извлекаем основной контент
        main_content = soup.find('main') or soup.find('div', class_=re.compile('content|main|article'))
        if not main_content:
            main_content = soup.find('body')
        
        # Извлекаем все заголовки
        headings = []
        for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            for heading in soup.find_all(tag):
                text = heading.get_text(strip=True)
                if text:
                    headings.append({'level': tag, 'text': text})
        
        # Извлекаем параграфы
        paragraphs = []
        for p in soup.find_all('p'):
            text = p.get_text(strip=True)
            if text and len(text) > 20:  # Игнорируем короткие тексты
                paragraphs.append(text)
        
        # Извлекаем списки
        lists = []
        for ul in soup.find_all(['ul', 'ol']):
            items = [li.get_text(strip=True) for li in ul.find_all('li')]
            if items:
                lists.append(items)
        
        # Извлекаем div'ы с текстом (могут содержать цены и другую информацию)
        divs_with_text = []
        # Ищем div'ы с классами, содержащими ключевые слова
        for div in soup.find_all('div', class_=re.compile('price|cost|duration|time|pickup|additional|info|detail', re.I)):
            text = div.get_text(strip=True)
            if text and len(text) > 5:
                divs_with_text.append(text)
        
        # Также извлекаем все div'ы с текстом (для поиска скрытой информации)
        for div in soup.find_all('div'):
            text = div.get_text(strip=True)
            # Ищем информацию о ценах, точках посадки и т.д.
            if text and (re.search(r'\d+\s*[р\.]', text) or 'Отправление' in text or 'дополнительные расходы' in text.lower()):
                if text not in divs_with_text and len(text) > 10:
                    divs_with_text.append(text)
        
        # Извлекаем span'ы с важной информацией
        spans_with_info = []
        for span in soup.find_all('span', class_=re.compile('price|cost|duration|time', re.I)):
            text = span.get_text(strip=True)
            if text:
                spans_with_info.append(text)
        
        # Извлекаем все span'ы с ценами
        for span in soup.find_all('span'):
            text = span.get_text(strip=True)
            if text and re.search(r'\d+\s*[р\.]', text):
                if text not in spans_with_info:
                    spans_with_info.append(text)
        
        # Извлекаем данные из data-атрибутов (могут содержать JSON с информацией)
        data_attributes = []
        for elem in soup.find_all(attrs={'data-price': True}):
            data_attributes.append(f"data-price: {elem.get('data-price')}")
        for elem in soup.find_all(attrs={'data-cost': True}):
            data_attributes.append(f"data-cost: {elem.get('data-cost')}")
        
        # Теперь удаляем скрипты
        for script in soup(["script", "meta"]):
            script.decompose()
        
        # Извлекаем ссылки
        links = []
        for a in soup.find_all('a', href=True):
            href = a.get('href')
            text = a.get_text(strip=True)
            if href and text:
                full_url = urljoin(self.base_url, href)
                links.append({'text': text, 'url': full_url})
        
        return {
            'title': title_text,
            'description': description,
            'headings': headings,
            'paragraphs': paragraphs,
            'lists': lists,
            'links': links,
            'divs_text': divs_with_text,
            'spans_text': spans_with_info,
            'data_attributes': data_attributes
        }
    
    def extract_images(self, soup: BeautifulSoup, page_url: str) -> List[Dict]:
        """Извлечь изображения со страницы"""
        images = []
        for img in soup.find_all('img', src=True):
            src = img.get('src')
            if src:
                full_url = urljoin(self.base_url, src)
                alt = img.get('alt', '')
                images.append({
                    'url': full_url,
                    'alt': alt,
                    'page': page_url
                })
        return images
    
    def extract_contacts(self, soup: BeautifulSoup) -> Dict:
        """Извлечь контактную информацию"""
        contacts = {}
        text = soup.get_text()
        
        # Телефоны
        phone_pattern = r'[\+]?[7-8]?[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}'
        phones = re.findall(phone_pattern, text)
        if phones:
            contacts['phones'] = list(set(phones))
        
        # Email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails:
            contacts['emails'] = list(set(emails))
        
        # Адреса (ищем упоминания Сочи, Адлер и т.д.)
        address_keywords = ['Сочи', 'Адлер', 'Хоста', 'улица', 'ул.', 'проспект', 'пр.']
        addresses = []
        for keyword in address_keywords:
            if keyword.lower() in text.lower():
                # Пытаемся извлечь контекст вокруг ключевого слова
                pattern = rf'.{{0,50}}{re.escape(keyword)}.{{0,50}}'
                matches = re.findall(pattern, text, re.IGNORECASE)
                addresses.extend(matches[:3])  # Берем первые 3 совпадения
        
        if addresses:
            contacts['addresses'] = list(set(addresses))
        
        return contacts
    
    def find_all_links(self, soup: BeautifulSoup, current_url: str) -> Set[str]:
        """Найти все внутренние ссылки на сайте"""
        links = set()
        base_domain = urlparse(self.base_url).netloc
        
        for a in soup.find_all('a', href=True):
            href = a.get('href')
            if href:
                # Пропускаем якоря и javascript ссылки
                if href.startswith('#') or href.startswith('javascript:'):
                    continue
                
                full_url = urljoin(current_url, href)
                parsed = urlparse(full_url)
                
                # Только ссылки на тот же домен
                if parsed.netloc == base_domain or (not parsed.netloc and parsed.path):
                    # Убираем якоря из URL
                    clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
                    if parsed.query:
                        clean_url += f"?{parsed.query}"
                    links.add(clean_url)
        return links
    
    def parse_excursion_page(self, soup: BeautifulSoup, url: str) -> Dict:
        """Парсинг страницы экскурсии"""
        content = self.extract_text_content(soup)
        images = self.extract_images(soup, url)
        page_text = soup.get_text()
        
        # Ищем цену в HTML элементах с классами price, cost и т.д.
        price = None
        price_elements = soup.find_all(['span', 'div', 'p'], class_=re.compile('price|cost', re.I))
        for elem in price_elements:
            text = elem.get_text(strip=True)
            price_match = re.search(r'(\d+)\s*(руб|₽)', text, re.IGNORECASE)
            if price_match:
                price = price_match.group(0).strip()
                break
        
        # Если не нашли в элементах, ищем в тексте
        if not price:
            price_patterns = [
                r'Цена\s+(\d+[\s\d]*)\s*(руб|₽)',
                r'(\d+)\s*руб\s*$',
                r'от\s+(\d+)\s*(руб|₽)',
                r'(\d+)\s*(руб|₽)\s*/\s*(час|день|чел)',
            ]
            for pattern in price_patterns:
                price_match = re.search(pattern, page_text, re.IGNORECASE | re.MULTILINE)
                if price_match:
                    price = price_match.group(0).strip()
                    break
        
        # Ищем длительность в HTML элементах
        duration = None
        duration_elements = soup.find_all(['span', 'div', 'p'], class_=re.compile('duration|time|продолжительность', re.I))
        for elem in duration_elements:
            text = elem.get_text(strip=True)
            duration_match = re.search(r'(\d+)\s*(час|часа|часов|ч)', text, re.IGNORECASE)
            if duration_match:
                duration = duration_match.group(0).strip()
                break
        
        # Если не нашли в элементах, ищем в тексте
        if not duration:
            duration_patterns = [
                r'Продолжительность[:\s]+(\d+[\s\-]?(час|часа|часов|ч|день|дня|дней))',
                r'(\d+)\s*(час|часа|часов|ч)\s*$',
                r'(\d+)\s*ч\b',
            ]
            for pattern in duration_patterns:
                duration_match = re.search(pattern, page_text, re.IGNORECASE)
                if duration_match:
                    duration = duration_match.group(0).strip()
                    break
        
        # Ищем точки посадки с ценами - улучшенные паттерны
        pickup_points = []
        
        # Собираем весь текст включая divs и spans
        all_text = page_text
        for div_text in content.get('divs_text', []):
            all_text += f" {div_text}"
        for span_text in content.get('spans_text', []):
            all_text += f" {span_text}"
        
        # Паттерн 1: "Отправление из Сочи - 3000р.взр./ 2500р.дет.(7-14)"
        pickup_pattern1_adult_child = r'Отправление\s+из\s+([А-Яа-я]+)\s*[-–]\s*(\d+)р\.взр\./\s*(\d+)р\.дет\.\(([^)]+)\)'
        matches1_ac = re.findall(pickup_pattern1_adult_child, all_text, re.IGNORECASE)
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
        matches1 = re.findall(pickup_pattern1, all_text, re.IGNORECASE)
        for match in matches1:
            if match[0] not in [p['location'] for p in pickup_points]:
                pickup_points.append({
                    'location': match[0],
                    'price': f"{match[1]} р."
                })
        
        # Паттерн 2: "из Сочи - 4000 р."
        if not pickup_points:
            pickup_pattern2 = r'из\s+([А-Яа-я]+)\s*[-–]\s*(\d+)\s*[р\.]'
            matches2 = re.findall(pickup_pattern2, all_text, re.IGNORECASE)
            for match in matches2:
                if match[0] not in [p['location'] for p in pickup_points]:
                    pickup_points.append({
                        'location': match[0],
                        'price': f"{match[1]} р."
                    })
        
        # Паттерн 3: Ищем в списках и div'ах
        for list_item in content.get('lists', []):
            list_text = ' '.join(list_item) if isinstance(list_item, list) else str(list_item)
            matches3 = re.findall(pickup_pattern1, list_text, re.IGNORECASE)
            for match in matches3:
                if match[0] not in [p['location'] for p in pickup_points]:
                    pickup_points.append({
                        'location': match[0],
                        'price': f"{match[1]} р."
                    })
        
        # Ищем дополнительные расходы - улучшенные паттерны
        additional_costs = []
        
        # Используем весь текст включая divs и spans
        all_text = page_text
        for div_text in content.get('divs_text', []):
            all_text += f" {div_text}"
        for span_text in content.get('spans_text', []):
            all_text += f" {span_text}"
        
        # Также добавляем текст из списков
        for list_item in content.get('lists', []):
            if isinstance(list_item, list):
                all_text += f" {' '.join(list_item)}"
            else:
                all_text += f" {str(list_item)}"
        
        # Паттерн 1: "4000 р. / 3000 р. (с 5 лет до 9 лет вкл.) / 1200 р. (тариф "Малыш" - до 4 лет вкл.) - билет в аквапарк"
        cost_pattern1 = r'(\d+\s*[р\.]+)\s*[/–]\s*(\d+\s*[р\.]+)?\s*\([^)]+\)\s*[/–]?\s*(\d+\s*[р\.]+)?\s*\([^)]+\)\s*–\s*([^\.\n]+)'
        cost_matches1 = re.findall(cost_pattern1, all_text, re.IGNORECASE)
        for match in cost_matches1:
            # Формируем описание с ценами
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
        cost_matches2 = re.findall(cost_pattern2, all_text, re.IGNORECASE)
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
        
        # Паттерн 3: Простые дополнительные расходы "800 р. - обед"
        simple_cost_pattern = r'(\d+\s*[р\.]+)\s*–\s*([^\.\n]+)'
        simple_matches = re.findall(simple_cost_pattern, all_text, re.IGNORECASE)
        for match in simple_matches:
            desc = match[1].strip()
            # Пропускаем, если это уже есть в списке
            if desc and desc not in [c.get('description', '') for c in additional_costs]:
                # Проверяем, что это действительно дополнительный расход, а не основная цена
                if any(keyword in desc.lower() for keyword in ['обед', 'канат', 'билет', 'тариф', 'дегустация', 'малыш']):
                    additional_costs.append({
                        'price': match[0].strip(),
                        'description': desc
                    })
        
        # Также ищем в списках
        for list_item in content.get('lists', []):
            list_text = ' '.join(list_item) if isinstance(list_item, list) else str(list_item)
            matches_list = re.findall(cost_pattern2, list_text, re.IGNORECASE)
            for match in matches_list:
                price_str = match[0].strip()
                if match[1]:
                    price_str += f" / {match[1].strip()}"
                desc = match[2].strip() if len(match) > 2 else ''
                if desc and desc not in [c.get('description', '') for c in additional_costs]:
                    additional_costs.append({
                        'price': price_str,
                        'description': desc
                    })
        
        return {
            'url': url,
            'title': content['title'],
            'description': content['description'],
            'content': {
                'headings': content['headings'],
                'paragraphs': content['paragraphs'],
                'lists': content['lists'],
                'divs_text': content.get('divs_text', []),
                'spans_text': content.get('spans_text', []),
                'data_attributes': content.get('data_attributes', [])
            },
            'price': price,
            'duration': duration,
            'pickup_points': pickup_points if pickup_points else None,
            'additional_costs': additional_costs if additional_costs else None,
            'images': images
        }
    
    def parse_page(self, url: str) -> Dict:
        """Парсинг обычной страницы"""
        soup = self.get_page(url)
        if not soup:
            return None
        
        content = self.extract_text_content(soup)
        images = self.extract_images(soup, url)
        contacts = self.extract_contacts(soup)
        
        return {
            'url': url,
            'title': content['title'],
            'description': content['description'],
            'content': {
                'headings': content['headings'],
                'paragraphs': content['paragraphs'],
                'lists': content['lists']
            },
            'images': images,
            'contacts': contacts if contacts else None
        }
    
    def crawl_site(self, start_url: str = None, max_pages: int = 100):
        """Обход всех страниц сайта"""
        if start_url is None:
            start_url = self.base_url
        
        to_visit = [start_url]
        page_count = 0
        
        while to_visit and page_count < max_pages:
            current_url = to_visit.pop(0)
            
            # Пропускаем уже посещенные
            if current_url in self.visited_urls:
                continue
            
            # Пропускаем файлы
            if any(current_url.endswith(ext) for ext in ['.jpg', '.png', '.gif', '.pdf', '.css', '.js']):
                continue
            
            self.visited_urls.add(current_url)
            soup = self.get_page(current_url)
            
            if not soup:
                continue
            
            page_count += 1
            
            # Определяем тип страницы
            url_lower = current_url.lower()
            page_text = soup.get_text().lower()
            title_text = soup.find('title')
            title_lower = title_text.get_text().lower() if title_text else ""
            
            # Определяем экскурсии по URL и контенту
            is_excursion = (
                'экскурс' in url_lower or 
                'excursion' in url_lower or
                '/ekskursii/' in url_lower or
                'экскурс' in title_lower or
                ('маршрут' in page_text and 'экскурс' in page_text) or
                any(keyword in url_lower for keyword in ['roza', 'gazprom', 'olimp', 'ritsa', 'afon', 'vodopad', 'delfinariy', 'akvapark'])
            )
            
            # Определяем услуги
            is_service = (
                'услуг' in url_lower or 
                'service' in url_lower or
                '/uslugi/' in url_lower or
                'услуг' in title_lower or
                any(keyword in url_lower for keyword in ['gid', 'transfer', 'razmeshchenie', 'meropriyatie'])
            )
            
            # Определяем контакты
            is_contact = (
                'контакт' in url_lower or 
                'contact' in url_lower or
                'контакт' in title_lower
            )
            
            if is_excursion:
                excursion_data = self.parse_excursion_page(soup, current_url)
                if excursion_data:
                    self.data['excursions'].append(excursion_data)
            elif is_service:
                page_data = self.parse_page(current_url)
                if page_data:
                    self.data['services'].append(page_data)
            elif is_contact:
                page_data = self.parse_page(current_url)
                if page_data:
                    if page_data.get('contacts'):
                        self.data['contacts'].update(page_data['contacts'])
                    self.data['pages'].append(page_data)
            else:
                page_data = self.parse_page(current_url)
                if page_data:
                    self.data['pages'].append(page_data)
            
            # Находим новые ссылки для обхода
            new_links = self.find_all_links(soup, current_url)
            for link in new_links:
                if link not in self.visited_urls and link not in to_visit:
                    to_visit.append(link)
            
            # Добавляем изображения в общий список
            images = self.extract_images(soup, current_url)
            self.data['images'].extend(images)
            
            # Небольшая задержка между запросами
            time.sleep(1)
        
        print(f"\nПарсинг завершен. Обработано страниц: {page_count}")
    
    def save_to_json(self, filename: str = "parsed_data.json"):
        """Сохранить данные в JSON файл"""
        output_path = os.path.join(os.path.dirname(__file__), '..', filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        print(f"Данные сохранены в {output_path}")


def main():
    """Основная функция"""
    parser = SiteParser()
    
    print("Начинаю парсинг сайта hostaotdykh.ru...")
    parser.crawl_site(max_pages=100)
    
    # Сохраняем результаты
    parser.save_to_json("parsed_data.json")
    
    # Выводим статистику
    print("\n=== Статистика ===")
    print(f"Страниц обработано: {len(parser.data['pages'])}")
    print(f"Экскурсий найдено: {len(parser.data['excursions'])}")
    print(f"Услуг найдено: {len(parser.data['services'])}")
    print(f"Изображений найдено: {len(parser.data['images'])}")
    print(f"Контактная информация: {len(parser.data['contacts'])} полей")


if __name__ == "__main__":
    main()

