# 🎨 Тематични фонове за папките

## Как работи сега?

Системата автоматично разпознава популярни предмети и им дава **тематични изображения**:

### 📚 Автоматично разпознати папки:

| Папка | Тематичен фон |
|-------|---------------|
| **Математика** | 📐 Формули, графики, числа |
| **Алгебра** | 🔢 Математически символи |
| **Геометрия** | 📊 Геометрични фигури |
| **Програмиране** | 💻 Екран с код |
| **Информатика** | ⌨️ Програмен код |
| **JavaScript** | 🟨 JS код на екран |
| **Python** | 🐍 Python код |
| **HTML & CSS** | 🌐 Уеб код |
| **Lessons** | 📝 Код на лаптоп |
| **Физика** | ⚛️ Лаборатория, експерименти |
| **Химия** | 🧪 Колби, формули |
| **Биология** | 🧬 Природа, микроскоп |
| **История** | 📜 Стари книги, архиви |
| **Литература** | 📚 Библиотека |
| **География** | 🗺️ Карти, глобус |
| **Изкуство** | 🎨 Палитри, четки |
| **Музика** | 🎵 Ноти, инструменти |

### 🎯 Други папки

Папки, които не са в списъка по-горе, получават **красиви градиенти** автоматично.

---

## ✏️ Как да добавя своя папка?

### Метод 1: Редактиране на index.html

Отворете `index.html`, намерете обекта `themedBackgrounds` и добавете вашата папка:

```javascript
const themedBackgrounds = {
    // ... съществуващи папки ...
    
    // Вашите папки
    '10 клас': 'https://images.unsplash.com/photo-1427504494785-3a9ca7044f45?w=1600&h=900&fit=crop',
    'Data Science': 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1600&h=900&fit=crop',
    'Web Design': 'https://images.unsplash.com/photo-1467232004584-a241de8bcf5d?w=1600&h=900&fit=crop'
};
```

### Метод 2: Търсене на безплатни изображения

**Препоръчани сайтове:**
- [Unsplash](https://unsplash.com/) - високо качество
- [Pexels](https://www.pexels.com/) - безплатни stock photos
- [Pixabay](https://pixabay.com/) - илюстрации и снимки

**Как да намерите URL на изображение в Unsplash:**

1. Отидете на [unsplash.com](https://unsplash.com)
2. Търсете по тема (напр. "mathematics formulas")
3. Изберете изображение
4. Копирайте URL-то и добавете `?w=1600&h=900&fit=crop` в края
5. Пример: 
   ```
   https://images.unsplash.com/photo-XXXXXXX?w=1600&h=900&fit=crop
   ```

**Примерни търсения:**
- `mathematics formulas` - формули
- `coding screen` - екран с код
- `physics laboratory` - физическа лаборатория
- `chemistry molecules` - химически формули
- `history books` - исторически книги
- `computer code` - компютърен код
- `abstract technology` - технологични абстракции

---

## 🖼️ Използване на локални изображения

Ако искате да използвате **собствени изображения** вместо Unsplash:

### Стъпка 1: Подгответе изображенията

Свалете или създайте изображения и ги сложете в папка `backgrounds/`:

```
backgrounds/
├── math.jpg            (1600x900px)
├── coding.jpg          (1600x900px)
├── physics.jpg         (1600x900px)
└── chemistry.jpg       (1600x900px)
```

**Препоръчителни размери:** 1600x900px (16:9)

**Препоръчителен размер файл:** 100-300KB (компресирайте с [TinyPNG](https://tinypng.com/))

### Стъпка 2: Редактирайте index.html

Отворете `index.html`, намерете секцията с коментар за локални изображения и я разkоментирайте:

```javascript
// Премахнете /* и */ около този код:
const customBackgrounds = {
    'Математика': 'backgrounds/math.jpg',
    'Физика': 'backgrounds/physics.jpg',
    'Химия': 'backgrounds/chemistry.jpg',
    'Програмиране': 'backgrounds/coding.jpg'
};

if (customBackgrounds[folderName]) {
    return { type: 'image', value: customBackgrounds[folderName] };
}
```

### Стъпка 3: Готово!

Локалните изображения имат **приоритет** над Unsplash URL-тата.

---

## 🎨 Създаване на собствени тематични фонове

### CSS Patterns (без изображения)

Можете да създадете **CSS patterns** за математика, код и т.н.:

```javascript
// Пример за математически pattern с CSS
const getFolderBackground = (folderName) => {
    if (folderName === 'Математика') {
        return {
            type: 'pattern',
            value: `
                background-color: #1e3a8a;
                background-image: 
                    repeating-linear-gradient(45deg, transparent, transparent 10px, rgba(255,255,255,.05) 10px, rgba(255,255,255,.05) 20px);
            `
        };
    }
    // ...
};
```

### SVG Patterns

За по-сложни patterns (формули, код):

1. Използвайте [Hero Patterns](https://heropatterns.com/)
2. Изберете pattern
3. Копирайте CSS кода
4. Поставете в `index.html`

---

## 📊 Примери за добри URL-та

### Математика
```
https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=1600&h=900&fit=crop
https://images.unsplash.com/photo-1596495578065-6e0763fa1178?w=1600&h=900&fit=crop
```

### Програмиране
```
https://images.unsplash.com/photo-1542831371-29b0f74f9713?w=1600&h=900&fit=crop
https://images.unsplash.com/photo-1587620962725-abab7fe55159?w=1600&h=900&fit=crop
```

### Физика
```
https://images.unsplash.com/photo-1532094349884-543bc11b234d?w=1600&h=900&fit=crop
https://images.unsplash.com/photo-1636466497217-26a8cbeaf0aa?w=1600&h=900&fit=crop
```

### Химия
```
https://images.unsplash.com/photo-1603126857599-f6e157fa2fe6?w=1600&h=900&fit=crop
https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?w=1600&h=900&fit=crop
```

---

## ⚡ Performance съвети

### Бързо зареждане

1. **Unsplash URL параметри:**
   - `w=1600` - ширина 1600px
   - `h=900` - височина 900px
   - `fit=crop` - изрязване
   - `q=80` - качество 80% (по-малък размер)

2. **Локални изображения:**
   - Компресирайте с TinyPNG
   - Използвайте JPEG за снимки
   - WebP формат е най-добър (по-малък размер)

### Кеширане

Браузърът автоматично кешира изображенията, така че:
- Първо зареждане: бавно
- Следващи пъти: моментално

---

## 🔄 Как да сменя между Unsplash и локални?

### Само Unsplash (текущо състояние)
Не трябва да правите нищо - работи веднага!

### Само локални изображения
Разkоментирайте секцията `customBackgrounds` и коментирайте проверката за `themedBackgrounds`.

### Миксирани (препоръчително)
Текущата настройка:
1. Проверява за локални изображения
2. Ако няма - използва Unsplash URL
3. Ако няма и това - използва градиент

---

## 🎯 Бързо добавяне на нова папка

```javascript
// В index.html, в themedBackgrounds обекта:

'Моята папка': 'URL_към_изображение',

// Пример:
'Модул 1': 'https://images.unsplash.com/photo-1516116216624-53e697fedbea?w=1600&h=900&fit=crop',
'Модул 2': 'https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=1600&h=900&fit=crop',
```

---

## 📝 Checklist

- ✅ Отворете `index.html`
- ✅ Намерете `themedBackgrounds`
- ✅ Добавете вашите папки с URL-та
- ✅ Запазете файла
- ✅ Refresh браузъра (Ctrl+F5)
- ✅ Готово!

---

**Сега вашите папки имат красиви тематични фонове! 🎨**

Математика → Формули  
Програмиране → Код  
Физика → Лаборатория  
И т.н. ✨
