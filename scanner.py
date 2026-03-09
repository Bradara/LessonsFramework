#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт за сканиране на директория и генериране на structure.json
Автоматично открива папки и HTML файлове за образователния портал
"""

import os
import json
import argparse
from pathlib import Path
from typing import List, Dict

# Файлове и папки за игнориране
IGNORE_ITEMS = {
    'scanner.py',
    'index.html',
    'structure.json',
    '.git',
    '.gitignore',
    '__pycache__',
    '.vscode',
    '.idea',
    'node_modules',
    '.DS_Store',
    'Thumbs.db',
    'backgrounds'
}

def should_ignore(item_name: str) -> bool:
    """
    Проверява дали даден файл/папка трябва да бъде игнориран
    
    Args:
        item_name: Име на файл или папка
        
    Returns:
        True ако трябва да се игнорира, иначе False
    """
    # Игнорира скрити файлове/папки (започващи с .)
    if item_name.startswith('.'):
        return True
    
    # Игнорира файлове/папки от списъка
    if item_name in IGNORE_ITEMS:
        return True
    
    return False

def scan_directory(directory: Path, recursive: bool = False, parent_path: str = "") -> List[Dict[str, str]]:
    """
    Сканира директория и връща структурата като списък от обекти
    
    Args:
        directory: Път до директорията за сканиране
        recursive: Дали да сканира рекурсивно поддиректории
        parent_path: Родителски път (за рекурсивно сканиране)
        
    Returns:
        Списък с обекти {"name": "...", "type": "...", "path": "..."}
    """
    items = []
    
    try:
        # Получаване на всички елементи в директорията
        for item in sorted(directory.iterdir()):
            # Игнориране на системни файлове
            if should_ignore(item.name):
                continue
            
            # Обработка на папки
            if item.is_dir():
                folder_path = f"{parent_path}{item.name}/" if parent_path else f"{item.name}/"
                
                items.append({
                    "name": item.name,
                    "type": "folder",
                    "path": folder_path
                })
                
                # Рекурсивно сканиране на поддиректории
                if recursive:
                    sub_items = scan_directory(item, recursive=True, parent_path=folder_path)
                    items.extend(sub_items)
            
            # Обработка на HTML файлове
            elif item.is_file() and item.suffix.lower() == '.html':
                # Премахваме .html от името за по-красив дисплей
                display_name = item.stem
                file_path = f"{parent_path}{item.name}" if parent_path else item.name
                
                items.append({
                    "name": display_name,
                    "type": "file",
                    "path": file_path
                })
    
    except PermissionError:
        print(f"⚠️  Няма достъп до директория: {directory}")
    except Exception as e:
        print(f"❌ Грешка при сканиране на {directory}: {e}")
    
    return items

def generate_structure_json(directory: Path, output_file: str = "structure.json", 
                           recursive: bool = False) -> None:
    """
    Генерира structure.json файл за дадена директория
    
    Args:
        directory: Път до директорията за сканиране
        output_file: Име на изходния JSON файл
        recursive: Дали да сканира рекурсивно
    """
    print(f"🔍 Сканиране на директория: {directory.absolute()}")
    print(f"📋 Режим: {'Рекурсивен' if recursive else 'Само текущо ниво'}")
    print("-" * 50)
    
    # Сканиране на директорията
    items = scan_directory(directory, recursive=recursive)
    
    # Статистика
    folders_count = sum(1 for item in items if item["type"] == "folder")
    files_count = sum(1 for item in items if item["type"] == "file")
    
    print(f"✅ Открити папки: {folders_count}")
    print(f"✅ Открити уроци (HTML): {files_count}")
    print(f"📊 Общо елементи: {len(items)}")
    print("-" * 50)
    
    # Записване на JSON файл
    output_path = directory / output_file
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Генериран файл: {output_path}")
        print("✨ Готово! Можете да отворите index.html в браузър.")
    
    except Exception as e:
        print(f"❌ Грешка при записване на {output_file}: {e}")

def main():
    """Главна функция"""
    parser = argparse.ArgumentParser(
        description='Сканира директория и генерира structure.json за образователния портал',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примери за използване:
  python scanner.py                    # Сканира текущата директория (само първо ниво)
  python scanner.py -r                 # Сканира рекурсивно всички поддиректории
  python scanner.py -d ./lessons       # Сканира конкретна директория
  python scanner.py -r -o data.json    # Рекурсивно сканиране с различно име на файла
        """
    )
    
    parser.add_argument(
        '-d', '--directory',
        type=str,
        default='.',
        help='Директория за сканиране (по подразбиране: текущата)'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='structure.json',
        help='Име на изходния JSON файл (по подразбиране: structure.json)'
    )
    
    parser.add_argument(
        '-r', '--recursive',
        action='store_true',
        help='Рекурсивно сканиране на всички поддиректории'
    )
    
    args = parser.parse_args()
    
    # Преобразуване на пътя
    directory = Path(args.directory).resolve()
    
    # Проверка дали директорията съществува
    if not directory.exists():
        print(f"❌ Директорията не съществува: {directory}")
        return
    
    if not directory.is_dir():
        print(f"❌ Пътят не е директория: {directory}")
        return
    
    # Генериране на структурата
    generate_structure_json(directory, args.output, args.recursive)

if __name__ == '__main__':
    main()
