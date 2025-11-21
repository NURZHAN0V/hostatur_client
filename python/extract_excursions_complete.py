#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Извлечение полных данных об экскурсиях: ссылки, изображения и все поля"""

import json
import os

def extract_excursions_complete():
    # Путь к файлу
    json_file = '../parsed_data.json'
    output_file = '../excursions_complete.json'
    
    # Читаем JSON
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Извлекаем экскурсии (фильтруем только реальные экскурсии)
    excursions = []
    
    for excursion in data.get('excursions', []):
        url = excursion.get('url', '')
        
        # Пропускаем главную страницу и категории
        if url in ['https://hostaotdykh.ru', 'https://hostaotdykh.ru/']:
            continue
        if not url or 'detail.html' not in url:
            continue
        if 'dirDesc.html' in url or 'kalendar.html' in url:
            continue
        # Базовые данные
        excursion_data = {
            'url': excursion.get('url', ''),
            'title': excursion.get('title', ''),
            'description': excursion.get('description', ''),
            'price': excursion.get('price'),
            'duration': excursion.get('duration'),
            'pickup_points': excursion.get('pickup_points'),
            'additional_costs': excursion.get('additional_costs'),
        }
        
        # Извлекаем только релевантные изображения (фильтруем служебные)
        image_urls = []
        excluded_patterns = [
            'oldlogo.png',
            'mod_ebwhatsappchat',
            'mc.yandex.ru',
            'ps4-5.png',
            'Sergeyqweqwe.jpg',
            'filetype_jpg.png',
            'vmgeneral',
            'components/com_virtuemart/assets'
        ]
        
        if excursion.get('images'):
            for img in excursion.get('images', []):
                img_url = img.get('url', '')
                if not img_url:
                    continue
                
                # Пропускаем служебные изображения
                if any(pattern in img_url for pattern in excluded_patterns):
                    continue
                
                # Проверяем, что это изображение экскурсии (обычно в папке product)
                if 'virtuemart/product' in img_url or 'images/virtuemart' in img_url:
                    image_urls.append({
                        'url': img_url,
                        'alt': img.get('alt', ''),
                        'is_main': False  # Определим позже
                    })
        
        # Первое изображение - основное
        if image_urls:
            image_urls[0]['is_main'] = True
        
        excursion_data['images'] = image_urls
        excursion_data['image_count'] = len(image_urls)
        
        # Извлекаем только релевантный контент (фильтруем футер и служебную информацию)
        content = excursion.get('content', {})
        
        # Фильтруем заголовки (убираем футер)
        excluded_headings = ['ССЫЛКИ', 'Популярное', 'Контакты', 'О нас', 'Награды']
        headings = [
            h for h in content.get('headings', [])
            if h.get('text', '') not in excluded_headings
        ]
        
        # Фильтруем параграфы (убираем юридическую информацию и служебный текст)
        excluded_paragraphs = [
            'ООО "Хостинский Отдых"',
            'ИНН:',
            'ОГРН:',
            'КПП:',
            'Политика конфиденциальности',
            'Условия возврата',
            'Способы оплаты',
            'Здравствуйте. У вас возникли вопросы?',
            'Этот адрес электронной почты защищён от спам-ботов',
            '8 (988)',
            '8 (918)',
            'г. Сочи, ул.'
        ]
        paragraphs = [
            p for p in content.get('paragraphs', [])
            if not any(excluded in p for excluded in excluded_paragraphs) and len(p.strip()) > 10
        ]
        
        # Фильтруем списки (убираем навигационные меню и контакты)
        lists = []
        nav_items = ['Главная', 'О компании', 'Экскурсии', 'Туристам', 'Услуги', 'Контакты', 
                     'О нас', 'Награды', 'Сочи', 'Абхазия', 'Услуги гидов', 'Трансфер', 'Размещение']
        contact_items = ['8 (988)', '8 (918)', 'Этот адрес электронной почты', 'г. Сочи']
        
        for lst in content.get('lists', []):
            if isinstance(lst, list):
                lst_str = ' '.join(str(item) for item in lst)
                # Пропускаем навигационные меню
                if any(nav in lst_str for nav in nav_items) and len(lst) <= 15:
                    continue
                # Пропускаем контактную информацию
                if any(contact in lst_str for contact in contact_items):
                    continue
                # Оставляем только релевантные списки (например, список популярных экскурсий)
                if len(lst) > 0:
                    lists.append(lst)
        
        excursion_data['content'] = {
            'headings': headings,
            'paragraphs': paragraphs,
            'lists': lists,
        }
        
        # Извлекаем все ссылки из контента
        links = []
        if content.get('links'):
            for link in content.get('links', []):
                links.append({
                    'text': link.get('text', ''),
                    'url': link.get('url', '')
                })
        excursion_data['links'] = links
        
        # Определяем категорию из URL
        url = excursion.get('url', '')
        if 'ekskursii-sochi' in url:
            excursion_data['category'] = 'Сочи'
        elif 'ekskursii-abkhaziya' in url:
            excursion_data['category'] = 'Абхазия'
        else:
            excursion_data['category'] = 'Общие'
        
        excursions.append(excursion_data)
    
    # Сохраняем в JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'total': len(excursions),
            'excursions': excursions
        }, f, ensure_ascii=False, indent=2)
    
    print(f"Извлечено экскурсий: {len(excursions)}")
    print(f"Сохранено в файл: {output_file}")
    
    # Статистика
    with_price = sum(1 for e in excursions if e.get('price'))
    with_duration = sum(1 for e in excursions if e.get('duration'))
    with_pickup_points = sum(1 for e in excursions if e.get('pickup_points'))
    with_additional_costs = sum(1 for e in excursions if e.get('additional_costs'))
    total_images = sum(e.get('image_count', 0) for e in excursions)
    
    print(f"\n=== Статистика ===")
    print(f"С ценой: {with_price}")
    print(f"С продолжительностью: {with_duration}")
    print(f"С точками посадки: {with_pickup_points}")
    print(f"С дополнительными расходами: {with_additional_costs}")
    print(f"Всего изображений: {total_images}")
    
    # Создаем также упрощенный CSV-подобный файл
    csv_file = '../excursions_summary.txt'
    with open(csv_file, 'w', encoding='utf-8') as f:
        f.write("URL\tНазвание\tЦена\tПродолжительность\tИзображений\tКатегория\n")
        for exc in excursions:
            f.write(f"{exc['url']}\t{exc['title']}\t{exc.get('price', '')}\t{exc.get('duration', '')}\t{exc['image_count']}\t{exc['category']}\n")
    
    print(f"\nУпрощенная сводка сохранена в: {csv_file}")

if __name__ == '__main__':
    extract_excursions_complete()

