# 📋 Кратка справка - Образователен Портал

## 🎯 Основни команди

### Генериране на структура
```powershell
python scanner.py           # Само текущо ниво
python scanner.py -r        # Рекурсивно (препоръчително)
```

### Отваряне в браузър
```powershell
# ⚠️ Използвайте HTTP сървър (не директно отваряне)!
python -m http.server 8000    # Стартирайте сървър
start http://localhost:8000   # Отворете в браузър

# Или използвайте VS Code Live Server:
# Десен бутон на index.html → "Open with Live Server"
```

### Създаване на нов урок
```powershell
copy lesson_template.html "Име на урок.html"
code "Име на урок.html"
python scanner.py -r
```

## 📁 Структура на файловете

```
LessonsFramework/
├── 📄 index.html              → Dashboard (отваряйте в браузър)
├── 🐍 scanner.py              → Скрипт за сканиране
├── 📝 lesson_template.html    → Шаблон за копиране
├── 📊 structure.json          → Автоматично генериран
├── 📖 README.md               → Пълна документация
├── 🧪 TESTING.md              → Инструкции за тестване
├── 📋 QUICKREF.md             → Тази справка
├── 📁 Примерни уроци/         → Примерна папка
│   └── 📄 Увод в HTML.html   → Примерен урок
└── 🙈 .gitignore              → Git ignore rules
```

## 🔄 Типичен работен процес

1. **Създайте папка** за тема
   ```powershell
   mkdir "Математика"
   ```

2. **Копирайте шаблон**
   ```powershell
   copy lesson_template.html "Математика\Урок 1.html"
   ```

3. **Редактирайте урока**
   ```powershell
   code "Математика\Урок 1.html"
   ```

4. **Генерирайте структурата**
   ```powershell
   python scanner.py -r
   ```

5. **Прегледайте в браузър**
   ```powershell
   start index.html
   ```

## ✏️ Редактиране на урок

### Променете заглавието
```html
<h1>✨ Вашето заглавие</h1>
<p>Вашето описание</p>
```

### Добавете секция
```html
<h2>Заглавие на секция</h2>
<p>Вашият текст...</p>
```

### Добавете код
```html
<pre><code>console.log("Здравей!");</code></pre>
```

### Добавете важна бележка
```html
<div class="highlight-box">
    <p>
        <i class="fas fa-lightbulb icon"></i>
        <strong>Важно:</strong> Вашата бележка
    </p>
</div>
```

### Добавете списък
```html
<ul>
    <li>Точка 1</li>
    <li>Точка 2</li>
</ul>
```

## 🎨 Персонализация

### Заглавие на Dashboard
Редактирайте `index.html` → ред ~30

### Цветова схема
- **Dashboard:** Търсете `from-blue-500 to-purple-600`
- **Уроци:** Търсете `#667eea` и `#764ba2`

### Шрифт
- **Dashboard:** `font-family: 'Inter'`
- **Уроци:** `font-family: 'Montserrat'`

### Брой колони
Редактирайте `index.html` → `lg:grid-cols-3` → променете на 2, 3, 4, 5

## 🚨 Често срещани проблеми

| Проблем | Решение |
|---------|---------|| "NetworkError when attempting to fetch" | Използвайте HTTP сървър: `python -m http.server 8000` || "Не може да се зареди structure.json" | `python scanner.py -r` |
| Не виждам новите уроци | Refresh браузъра (Ctrl+F5) |
| Python грешка | Проверете версията: `python --version` |
| Кирилица не се показва | Използвайте UTF-8 encoding |

## 📦 Използвани технологии

- **React 18** - UI библиотека (CDN)
- **Tailwind CSS** - CSS framework (CDN)
- **FontAwesome 6** - Икони (CDN)
- **Google Fonts** - Шрифтове (CDN)
- **Python 3.6+** - За автоматизация

## 🌐 Публикуване

### GitHub Pages
```powershell
git init
git add .
git commit -m "Initial commit"
git push origin main
```
Settings → Pages → Select branch

### Netlify
Влачете папката в Netlify Drop → Готово!

## 💡 Съвети

- ✅ Използвайте **описателни имена** на файловете
- ✅ **Организирайте** уроците в папки и подпапки
- ✅ **Кликнете на папка**, за да влезете в нея и да видите съдържанието
- ✅ Използвайте **breadcrumb** навигацията за връщане назад
- ✅ Винаги стартирайте **scanner.py -r** след промени
- ✅ **Тествайте** в различни браузъри
- ✅ Правете **backup** на уроците
- ✅ Използвайте **Git** за версиониране

## 📞 За помощ

1. Прочетете [README.md](README.md) за пълна документация
2. Прочетете [TESTING.md](TESTING.md) за инструкции
3. Прочетете [FOLDERS.md](FOLDERS.md) за навигация между папки
4. Проверете секцията Troubleshooting в README

---

**Успех с вашия образователен портал! 🎓**

*Актуализирано: Февруари 2026*
