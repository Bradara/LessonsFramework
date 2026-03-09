# 🎨 Backgrounds - Локални изображения за фонове на папки

## 📁 Тази папка е за вашите фонови изображения

### Как да използвате локални изображения?

#### Стъпка 1: Добавете изображения в тази папка

Сложете вашите изображения тук с ясни имена:
```
backgrounds/
├── math.jpg           (за Математика)
├── physics.jpg        (за Физика)
├── chemistry.jpg      (за Химия)
├── programming.jpg    (за Програмиране)
├── history.jpg        (за История)
└── default.jpg        (по подразбиране)
```

**Препоръчителни размери:** 1600x900px или подобни (16:9 съотношение)

**Формати:** JPG, PNG, WEBP

#### Стъпка 2: Редактирайте index.html

Отворете `index.html`, намерете функцията `getFolderBackground()` и разкоментирайте следния код:

```javascript
const customBackgrounds = {
    'Математика': 'backgrounds/math.jpg',
    'Физика': 'backgrounds/physics.jpg',
    'Химия': 'backgrounds/chemistry.jpg',
    'Програмиране': 'backgrounds/programming.jpg'
};

if (customBackgrounds[folderName]) {
    return { type: 'image', value: customBackgrounds[folderName] };
}
```

#### Стъпка 3: Персонализирайте

Добавете вашите папки:
```javascript
const customBackgrounds = {
    'Моята папка': 'backgrounds/my-image.jpg',
    '10 клас': 'backgrounds/class10.jpg',
    'JavaScript': 'backgrounds/js.jpg'
};
```

---

## 🎨 Текущо решение: CSS Градиенти

**Текущо системата използва красиви CSS градиенти, които:**
- ✅ Винаги работят (не зависят от интернет)
- ✅ Зареждат се моментално
- ✅ Заемат 0 байта дисково пространство
- ✅ Всяка папка получава различен цвят автоматично

**12 налични градиента:**
1. Сине-лилаво (667eea → 764ba2)
2. Розово-червено (f093fb → f5576c)
3. Синьо (4facfe → 00f2fe)
4. Зелено (43e97b → 38f9d7)
5. Розово-жълто (fa709a → fee140)
6. Тюркоаз (30cfd0 → 330867)
7. Пастелно (a8edea → fed6e3)
8. Нежно розово (ff9a9e → fecfef)
9. Портокалово (ffecd2 → fcb69f)
10. Червено-синьо (ff6e7f → bfe9ff)
11. Лилаво-синьо (e0c3fc → 8ec5fc)
12. Огнено (f77062 → fe5196)

---

## 🖼️ Къде да намерите безплатни изображения?

### Препоръчани сайтове:

1. **[Unsplash](https://unsplash.com/)** - Високо качество, безплатни
   - Търсете: education, learning, mathematics, science
   
2. **[Pexels](https://www.pexels.com/)** - Безплатни stock photos
   
3. **[Pixabay](https://pixabay.com/)** - Безплатни изображения и илюстрации

4. **[FreeImages](https://www.freeimages.com/)** - Голям избор

### Примерни търсения:

- Mathematics → формули, графики, числа
- Physics → лаборатория, молекули, космос
- Chemistry → химикали, колби, таблица на елементите
- Programming → код, компютър, binary
- History → книги, архиви, стари карти
- Literature → библиотека, книги
- Art → четки, палитра, рисунки
- Music → ноти, инструменти

---

## 🎯 Примерна конфигурация

След като свалите изображения (`math.jpg`, `physics.jpg`, и т.н.) и ги сложите в тази папка:

```javascript
// В index.html, във функцията getFolderBackground():

const customBackgrounds = {
    // Основни предмети
    'Математика': 'backgrounds/math.jpg',
    'Физика': 'backgrounds/physics.jpg',
    'Химия': 'backgrounds/chemistry.jpg',
    'Биология': 'backgrounds/biology.jpg',
    'История': 'backgrounds/history.jpg',
    'География': 'backgrounds/geography.jpg',
    
    // Програмиране
    'Програмиране': 'backgrounds/programming.jpg',
    'JavaScript': 'backgrounds/javascript.jpg',
    'Python': 'backgrounds/python.jpg',
    'HTML & CSS': 'backgrounds/html-css.jpg',
    
    // Класове
    '10 клас': 'backgrounds/class10.jpg',
    '11 клас': 'backgrounds/class11.jpg',
    '12 клас': 'backgrounds/class12.jpg',
    
    // Default за непознати папки
    'default': 'backgrounds/default.jpg'
};

if (customBackgrounds[folderName]) {
    return { type: 'image', value: customBackgrounds[folderName] };
}

// Ако папката не е в списъка, използва градиент
```

---

## 💡 Съвети

### Размер на файловете
- Компресирайте изображенията (напр. с [TinyPNG](https://tinypng.com/))
- Целете 100-300KB на изображение
- Използвайте JPEG за снимки, PNG за графики

### Качество
- Минимум 1200px ширина
- Избягвайте размазани или пикселирани изображения
- Предпочитайте landscape ориентация (хоризонтална)

### Цветност
- Изберете изображения с добър контраст
- Избягвайте твърде тъмни изображения (текстът ще е нечетим)
- Или използвайте светли изображения

### Performance
- Не използвайте огромни файлове (5MB+)
- Оптимизирайте преди качване
- Кешът на браузъра ще ги зарежда бързо след първия път

---

## 🔄 Смяна между градиенти и изображения

### Само градиенти (текущо)
Не трябва да правите нищо! Работи out-of-the-box.

### Смесени (градиенти + изображения)
Разkоментирайте кода в `index.html` и добавете само папките, които искате с изображения. Останалите ще използват градиенти.

### Само изображения
Добавете default изображение:
```javascript
const customBackgrounds = {
    // ... вашите папки
};

if (customBackgrounds[folderName]) {
    return { type: 'image', value: customBackgrounds[folderName] };
}

// Fallback към default изображение
return { type: 'image', value: 'backgrounds/default.jpg' };
```

---

## 📊 Файлова структура

```
LessonsFramework/
├── backgrounds/              ← Тази папка
│   ├── README.md            ← Този файл
│   ├── math.jpg             ← Вашите изображения
│   ├── physics.jpg
│   ├── chemistry.jpg
│   └── ...
├── index.html               ← Редактирайте тук
└── ...
```

---

**Готово!** Сега имате пълен контрол над фоновете на папките! 🎨

За въпроси, вижте [FOLDERS.md](../FOLDERS.md) и [README.md](../README.md).
