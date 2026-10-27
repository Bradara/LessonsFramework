# 📚 Образователен Портал - Статична Система за Уроци

Модерна, лесна за използване система за управление на интерактивни образователни материали. Изградена с React, Tailwind CSS и Python автоматизация.

## ✨ Характеристики

- 🎨 **Модерен дизайн** - чист, минималистичен интерфейс с Tailwind CSS
- 📱 **Responsive** - адаптивен дизайн за всички устройства
- 🚀 **Статичен** - без нужда от сървър, работи директно в браузъра
- 🔄 **Автоматизиран** - Python скрипт за генериране на структурата
- 🎯 **Лесен за използване** - просто добавяте HTML файлове и стартирате скрипта
- 📁 **Навигация между папки** - йерархична организация с breadcrumb навигация
- 🖼️ **Уникални фонове** - всяка папка има автоматично генериран красив фон от Unsplash

## 📁 Структура на проекта

```
LessonsFramework/
├── index.html              # Главно табло (Dashboard)
├── scanner.py              # Python скрипт за сканиране
├── lesson_template.html    # Шаблон за уроци
├── structure.json          # Генерирана структура (автоматична)
└── README.md              # Тази документация
```

## 🚀 Бърз старт

### 1. Подготовка

Уверете се, че имате инсталиран Python 3.6 или по-нова версия:

```powershell
python --version
```

### 2. Тествайте с примерните данни

Вече има **примерен `structure.json` файл**, така че можете веднага да отворите `index.html` в браузър:

```powershell
# Отваряне в браузър (Windows)
start index.html

# Или с PowerShell
ii index.html
```

Ще видите примерно табло с 3 папки и 3 урока.

### 3. Създайте собствено съдържание

#### Създаване на папка и уроци

```powershell
# Създайте папка за уроци
mkdir Математика

# Копирайте шаблона в папката
copy lesson_template.html Математика\Урок1.html
```

#### Редактирайте урока

Отворете `Математика\Урок1.html` във VS Code и персонализирайте:

1. Променете заглавието в `<h1>` тага
2. Добавете вашето съдържание в секцията `.content`
3. Запазете файла

### 4. Генерирайте структурата

```powershell
# Основно използване (само текущо ниво)
python scanner.py

# Рекурсивно сканиране (включва поддиректории)
python scanner.py -r
```

### 5. Преглед на резултата

Отворете `index.html` в браузър - вашите нови папки и уроци ще се появят автоматично!

## 🛠️ Разширени опции на scanner.py

```powershell
# Помощ с всички опции
python scanner.py --help

# Сканиране на конкретна директория
python scanner.py -d ./lessons

# Рекурсивно сканиране с различно име на изходния файл
python scanner.py -r -o data.json

# Сканиране на друга директория рекурсивно
python scanner.py -d C:\MyLessons -r
```

### Параметри

| Параметър | Съкращение | Описание | По подразбиране |
|-----------|------------|----------|-----------------|
| `--directory` | `-d` | Директория за сканиране | `.` (текуща) |
| `--output` | `-o` | Име на изходния файл | `structure.json` |
| `--recursive` | `-r` | Рекурсивно сканиране | `false` |

## 📝 Създаване на нови уроци

### Метод 1: Копиране на шаблона

```powershell
# Копирайте шаблона
copy lesson_template.html "Моя урок.html"

# Редактирайте новия файл
code "Моя урок.html"
```

### Метод 2: Използване на template като база

1. Отворете `lesson_template.html` във VS Code
2. Редактирайте съдържанието
3. Запазете като нов файл (Ctrl+Shift+S)

### Структура на урока

```html
<!-- Заглавие -->
<div class="header">
    <h1>Вашето заглавие</h1>
    <p>Описание</p>
</div>

<!-- Съдържание -->
<div class="content">
    <h2>Секция 1</h2>
    <p>Текст...</p>
    
    <h3>Подсекция</h3>
    <ul>
        <li>Точка 1</li>
        <li>Точка 2</li>
    </ul>
    
    <!-- Код -->
    <pre><code>console.log("Hello!");</code></pre>
    
    <!-- Важна бележка -->
    <div class="highlight-box">
        <p><i class="fas fa-lightbulb icon"></i>
        <strong>Важно:</strong> Текст...</p>
    </div>
</div>
```

## 🎨 Дизайн елементи

### Използвани икони

Dashboard използва FontAwesome за следните икони:

**Папки:** 
- `fa-folder` (фиксирана икона)

**Уроци (случайни):**
- `fa-book`
- `fa-graduation-cap`
- `fa-chalkboard`
- `fa-lightbulb`
- `fa-book-open`
- `fa-brain`
- `fa-flask`
- `fa-microscope`
- `fa-pencil`
- `fa-laptop-code`

### Цветова схема

```css
Primary Gradient: #667eea → #764ba2 (сине-лилаво)
Folders: #facc15 → #f97316 (жълто-оранжево)
Files: #60a5fa → #6366f1 (синьо-индиго)
```

## 🔧 Персонализация

### Промяна на заглавието

Редактирайте `index.html`, линия ~30:

```html
<h1 class="text-3xl font-bold text-gray-900">
    Вашето Заглавие
</h1>
```

### Промяна на шрифтовете

За Dashboard (в `index.html`):
```html
<!-- Променете от Inter на друг шрифт -->
<link href="https://fonts.googleapis.com/.../Roboto...">
```

За уроци (в `lesson_template.html`):
```html
<!-- Променете от Montserrat на друг шрифт -->
<link href="https://fonts.googleapis.com/.../Poppins...">
```

### Промяна на броя колони

Редактирайте `index.html`, намерете:

```html
<!-- Променете lg:grid-cols-3 на желания брой -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
```

## 📋 Workflow за добавяне на съдържание

1. **Създайте структура от папки** (по желание)
   ```powershell
   mkdir Математика, Физика, Химия
   ```

2. **Добавете уроци** (копирайте template)
   ```powershell
   copy lesson_template.html Математика\Урок1.html
   ```

3. **Редактирайте уроците** във VS Code

4. **Генерирайте структурата**
   ```powershell
   python scanner.py -r
   ```

5. **Отворете в браузър**
   ```powershell
   start index.html
   ```

## ⚠️ Важни бележки

### Игнорирани файлове

Скриптът автоматично игнорира:
- `scanner.py` - самия скрипт
- `index.html` - главното табло
- `structure.json` - генерирания файл
- `.git`, `.gitignore` - Git файлове
- `.vscode`, `.idea` - IDE конфигурации
- Скрити файлове (започващи с `.`)

### Само HTML файлове

Скриптът **сканира само `.html` файлове**. Ако имате други файлове (`.pdf`, `.docx`), те няма да се покажат в Dashboard.

### Кирилица в имената

Системата **поддържа кирилица** в имената на файлове и папки! Използвайте смело български имена.

## 🌐 Локално тестване

### ⚠️ ВАЖНО: CORS проблем

**Не можете** да отваряте `index.html` директно (двоен клик)! Поради CORS политиките на браузърите, `fetch()` заявките към локални файлове се блокират.

**Решение:** Винаги използвайте HTTP сървър за локално тестване.

### Метод 1: Python HTTP Server (Бърз)

```powershell
# Стартирайте сървъра
python -m http.server 8000

# Отворете в браузър
start http://localhost:8000
```

За да спрете сървъра: `Ctrl+C`

### Метод 2: Live Server в VS Code (Препоръчително)

1. Отворете `index.html` във VS Code
2. Щракнете с десен бутон → **"Open with Live Server"**
3. Или натиснете `Alt+L Alt+O`
4. Браузърът ще се отвори автоматично с live reload!

**Предимства:**
- ✅ Автоматично обновяване при промени
- ✅ Без ръчно стартиране на сървър
- ✅ Перфектно за разработка

### Метод 3: Директно отваряне (НЕ РАБОТИ)

```powershell
# ❌ НЕ използвайте - ще получите CORS грешка!
start index.html
```

Ще видите грешка: **"NetworkError when attempting to fetch resource."**

## 🚀 Публикуване

След като сте готови, можете да публикувате проекта като статичен сайт:

### GitHub Pages
1. Качете всички файлове в GitHub repository
2. Отидете в Settings → Pages
3. Изберете branch (обикновено `main`)
4. Вашият сайт ще е на: `https://username.github.io/repo-name`

### Netlify
1. Влачете папката в Netlify Drop
2. Сайтът е публикуван веднага

### Vercel
```powershell
# Инсталирайте Vercel CLI
npm i -g vercel

# Публикувайте
vercel
```

## 🧩 H5P ресурси (куизове и интерактивни упражнения)

H5P ресурсите се вграждат в урока с локалния плейър `h5p-standalone` (без сървър на H5P). Общите библиотеки се пазят веднъж в `libs/h5p-libraries/`, а всеки ресурс има само своите данни.

### Структура за нов H5P ресурс

```
Lessons/<предмет>/<клас>/
├── 02 Урок.html               ← урокът
└── H5P/
    ├── Име-на-ресурса.h5p     ← оригиналният експорт (по желание, за архив)
    └── Име-на-ресурса/        ← разархивирана папка
        ├── h5p.json           ← оставя се
        └── content/           ← оставя се (content.json, config.json)

libs/h5p-libraries/            ← общите библиотеки (H5P.*, FontAwesome-4.5, H5PEditor.* ...)
```

### Стъпки

1. Експортирай ресурса от H5P редактора (или Lumi) като `.h5p`.
2. Сложи го в `H5P/` в папката на урока и го разархивирай в подпапка със същото име (без `.h5p`).
3. Копирай всички папки на библиотеките (всичко освен `content/` и `h5p.json`) в `libs/h5p-libraries/`, ако ги няма там. Папките с версии, които вече съществуват, не е нужно да се копират отново.
4. Изтрий библиотечните папки от разархивираната папка, така че да останат само `h5p.json` и `content/`.
5. В урока добави контейнер и инициализация (замени името на папката с ресурса):

```html
<div id="h5p-container"></div>

<!-- в края на <body> -->
<script src="../../../libs/h5p-standalone/dist/main.bundle.js" charset="UTF-8"></script>
<script>
    document.addEventListener('DOMContentLoaded', function () {
        new H5PStandalone.H5P(document.getElementById('h5p-container'), {
            h5pJsonPath: 'H5P/Име-на-ресурса',
            librariesPath: '../../../libs/h5p-libraries',
            frameJs: '../../../libs/h5p-standalone/dist/frame.bundle.js',
            frameCss: '../../../libs/h5p-standalone/dist/styles/h5p.css'
        });
    });
</script>
```

6. Регенерирай структурата: `python scanner.py -r`. Папката `H5P/` е в `IGNORE_ITEMS`, така че не се появява в Dashboard-а.

Пътищата са относителни спрямо урока (`../../../` е от `Lessons/<предмет>/<клас>/`). Тествай през HTTP сървър (`python -m http.server 8000`), не с двоен клик.

Версията на `h5p-standalone` (`libs/h5p-standalone/`) се управлява от `download_libs.py`.

## 📚 Библиотека с markdown статии (Other/Library)

`Lessons/Other/Library/library.html` показва филтрируем списък със статии, написани като обикновени `.md` файлове в `Lessons/Other/Library/library/` (data-папка, игнорирана от scanner-а по същия начин като `quizzes/`/`H5P/`).

### Добавяне на статия

1. Сложи нов `.md` файл в `Lessons/Other/Library/library/` (директно или в подпапка по избор).
2. По желание добави frontmatter в началото на файла:

   ```markdown
   ---
   title: Заглавие
   author: Автор
   date: 2026-03-01
   topic: Категория
   tags: таг1, таг2
   ---
   ```

   Всички полета са опционални — липсващо `title` пада обратно на първия `# heading` в текста, липсващо `date` пада на датата на последния git commit за файла (после file mtime).
3. Регенерирай манифеста: `python build_library_manifest.py`. Това пренаписва `library/manifest.json`, който `library.html` чете при зареждане.
4. (По желание) `python scanner.py -r`, ако е добавена нова подпапка извън `Other/Library`.

Markdown се рендерира в браузъра с `marked.js` (`libs/marked.min.js`, качен от `download_libs.py`).

## 📝 Вграждане на .md файл директно в урок

Освен през общата Library (виж по-горе), всеки урок може да вгради съседен `.md` файл директно в своето съдържание — по същия модел като H5P (контейнер `<div>` + малък init скрипт), чрез споделения helper `libs/md-embed.js` + `libs/md-embed.css`.

### Стъпки за вграждане

1. Сложи `.md` файла до урока (или в подпапка), напр. `Lessons/<предмет>/<клас>/статия.md`. YAML frontmatter (`title:`/`author:`/...) е по желание — маха се автоматично преди рендериране.
2. В `<head>` добави стиловете:

   ```html
   <link rel="stylesheet" href="../../../libs/md-embed.css">
   ```

3. В тялото на урока добави контейнер и инициализация (замени пътя до `.md` файла с твоя):

   ```html
   <div id="md-embed"></div>

   <script src="../../../libs/marked.min.js" onerror="this.onerror=null;this.src='https://unpkg.com/marked@12.0.2/marked.min.js'"></script>
   <script src="../../../libs/md-embed.js"></script>
   <script>
       document.addEventListener('DOMContentLoaded', function () {
           renderMarkdownEmbed('md-embed', 'статия.md');
       });
   </script>
   ```

Пътят до `.md` файла в `renderMarkdownEmbed(...)` е относителен спрямо самия урок (не спрямо `libs/`). Относителната дълбочина до `libs/` зависи от нивото на урока, както при останалите библиотеки (`../../../` за `Lessons/<предмет>/<клас>/`). Тествай през `python -m http.server`, не с двоен клик (CORS).

`md-embed.js`/`md-embed.css` са собствени файлове на проекта (не се вендорват от `download_libs.py` — няма CDN версия за тях).

### Mermaid диаграми и LaTeX/KaTeX формули

`renderMarkdownEmbed(...)` (ползва се и от `library.html`) автоматично засича в markdown текста:

- ` ```mermaid ` code block → зарежда `libs/mermaid.min.js` и рендира диаграмата
- `$...$` / `$$...$$` → зарежда `libs/katex/` (CSS + JS + auto-render) и рендира формулите

Зареждането е мързеливо — ако статията няма нито едното, нито другото, тези библиотеки изобщо не се теглят. Не е нужен допълнителен `<script>` таг в урока за това, работи автоматично за всеки `.md` файл, вграден през `renderMarkdownEmbed`. И двете са управлявани от `download_libs.py`.

### Съдържание (TOC) чрез бутон-хамбургер

Добави `toc: true` във frontmatter-а на `.md` файла:

```markdown
---
toc: true
---
```

При рендиране `renderMarkdownEmbed(...)` автоматично генерира съдържание от `##`/`###` заглавията в текста (не е нужно да ги изброяваш ръчно) и показва бутон „☰" в горния десен ъгъл на статията. Клик върху него отваря/затваря падащо меню със списъка; клик върху елемент от него скролва плавно до съответното заглавие. Без `toc: true` (или с липсващо поле) бутонът не се показва.

## 🧠 Интерактивна мисловна карта (markmap) от `mermaid mindmap`

`renderMarkdownEmbed(...)` рендира ` ```mermaid ` блокове през `mermaid.js`, но за `mindmap` диаграми това е **статично** SVG — няма клик, няма пан/зуум. За урок, в който мисловната карта трябва да е навигируема (клик върху възел разгъва/свива клона му, плъзгане за преместване, бутони за мащаб), използвай `libs/markmap-embed.js` вместо `md-embed.js` — рендира **същия** `mermaid mindmap` синтаксис през [markmap](https://markmap.js.org/) (`libs/markmap/`).

### Стъпки за интерактивна мисловна карта

1. Напиши мисловната карта в `.md` файл със стандартен mermaid `mindmap` синтаксис. Поддържат се два варианта:

   - ` ```mermaid ` код блок вътре в markdown текст (виж `Lessons/IT/8 клас/H5P/Urok4/mindMap.md`):

     ````markdown
     ```mermaid
     mindmap
       root((Централна тема))
         Клон 1
           Подточка 1.1
         Клон 2
     ```
     ````

   - Суров mermaid source, както се копира директно от [mermaid.live](https://mermaid.live) (незадължителен YAML frontmatter с `config:`/`theme:`/цветове, последван директно от `mindmap` без ` ``` ` ограждане — виж `Lessons/Информатика/Modul1/H5P/Urok2/Тип_данни_string_мисловна_карта.md`). Frontmatter-ът се маха и игнорира — `markmap-view` си има собствено оцветяване по клон, не чете mermaid-специфичната тема.

   И в двата случая възлите може да са във формата `id((...))`/`id[...]`/`id{{...}}`/`id(...)`, по желание с кавичков текст вътре (`id["текст с \"специални\" знаци"]`) — `markmap-embed.js` маха обвивката и показва само текста.

2. В `<head>` добави стиловете:

   ```html
   <link rel="stylesheet" href="../../../libs/markmap-embed.css">
   ```

3. В тялото на урока добави контейнера (точно тази структура — `markmap-embed.js` очаква `<svg>` + `.markmap-toolbar-host` като деца на `.markmap-host`) и инициализацията:

   ```html
   <div class="markmap-host">
       <svg id="my-mindmap"></svg>
       <div class="markmap-toolbar-host"></div>
   </div>

   <script src="../../../libs/markmap-embed.js"></script>
   <script>
       document.addEventListener('DOMContentLoaded', function () {
           renderMermaidMindmap('my-mindmap', 'мисловна-карта.md');
       });
   </script>
   ```

`renderMermaidMindmap(svgId, mdPath)` зарежда `libs/markmap/d3.min.js` + `markmap-view.min.js` + `markmap-toolbar.min.js`/`.css` мързеливо (само при първо извикване), парсва mermaid `mindmap` текста директно в дърво (без markdown-it/markmap-lib — йерархията е по отстъпа на редовете), рендира интерактивната карта и добавя toolbar с zoom in / zoom out / fit бутони в `.markmap-toolbar-host`. По подразбиране са разгънати само първите 2 нива (`initialExpandLevel: 2`) — кликни възел, за да разгънеш/свиеш клона му.

**Същият капан като при H5P/mermaid в таб-базирани уроци:** markmap измерва контейнера си при инициализация, затова вика `renderMermaidMindmap(...)` само след като табът му вече е `display:block` (лениво, при първо превключване към него — виж примера в `Lessons/IT/8 клас/Съвременни компютърни системи.html`), иначе картата излиза с нулев размер.

Версиите на `d3`/`markmap-view`/`markmap-toolbar` (`libs/markmap/`) се управляват от `download_libs.py`. `markmap-embed.js`/`.css` са собствени файлове на проекта (не се вендорват от CDN), както `md-embed.js`.

## 🐛 Troubleshooting

### CORS грешка / NetworkError (НАЙ-ЧЕСТО)

**Проблем:** „NetworkError when attempting to fetch resource" или „CORS policy" грешка

**Причина:** Отворихте `index.html` директно (двоен клик или `start index.html`), вместо през HTTP сървър.

**Решение:**
```powershell
# Стартирайте HTTP сървър
python -m http.server 8000

# Отворете в НОВА табове
start http://localhost:8000
```

**Или използвайте Live Server в VS Code** (препоръчително за разработка).

### Не се зареждат уроците

**Проблем:** Dashboard показва грешка "Не може да се зареди structure.json"

**Решение:**
```powershell
# Уверете се, че structure.json съществува
python scanner.py
```

### Не виждам новите файлове

**Проблем:** Добавих нови уроци, но не се показват

**Решение:**
```powershell
# Регенерирайте структурата
python scanner.py -r

# Презаредете браузъра (Ctrl+F5)
```

### Грешка в Python скрипта

**Проблем:** `ModuleNotFoundError` или подобна грешка

**Решение:**
```powershell
# Проверете версията на Python
python --version

# Трябва да е 3.6+
# Ако е по-стара, обновете Python
```

### Папките не се виждат

**Проблем:** Създадох папки, но не се показват в Dashboard

**Решение:**
- Уверете се, че папките съдържат `.html` файлове (или използвайте `-r` флаг)
- Регенерирайте структурата: `python scanner.py -r`

## 💡 Съвети

1. **Организация:** Използвайте папки за различни теми/предмети
2. **Имена:** Давайте описателни имена на файловете (без `.html` суфикс в името)
3. **Версии:** Използвайте Git за проследяване на промените
4. **Backup:** Правете редовно копия на вашите уроци
5. **Тестване:** Винаги тествайте новите уроци в браузър преди публикуване

## 📚 Ресурси

- [React Документация](https://react.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [FontAwesome Икони](https://fontawesome.com/icons)
- [Google Fonts](https://fonts.google.com/)
- [Markdown Guide](https://www.markdownguide.org/)

## 📧 Поддръжка

За въпроси и проблеми, моля:
1. Прочетете секцията Troubleshooting
2. Проверете дали сте следвали стъпките правилно
3. Уверете се, че всички файлове са на правилните места

---

**Създадено с ❤️ за образованието**

*Последна актуализация: Февруари 2026*
