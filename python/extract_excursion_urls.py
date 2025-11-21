#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Извлечение списка ссылок на экскурсии из parsed_data.json"""

import json
import os

def extract_excursion_urls():
    # Путь к файлу
    json_file = '../parsed_data.json'
    output_file = '../excursions_urls.txt'
    
    # Читаем JSON
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Извлекаем URL экскурсий
    urls = []
    for excursion in data.get('excursions', []):
        url = excursion.get('url', '')
        if url and 'ekskursii' in url:
            urls.append(url)
    
    # Удаляем дубликаты и сортируем
    urls = sorted(list(set(urls)))
    
    # Сохраняем в файл
    with open(output_file, 'w', encoding='utf-8') as f:
        for url in urls:
            f.write(url + '\n')
    
    print(f"Найдено уникальных ссылок на экскурсии: {len(urls)}")
    print(f"Список сохранен в файл: {output_file}")
    
    # Выводим первые 10 для проверки
    print("\nПервые 10 ссылок:")
    for i, url in enumerate(urls[:10], 1):
        print(f"{i}. {url}")

if __name__ == '__main__':
    extract_excursion_urls()

