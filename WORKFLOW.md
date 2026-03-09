# 🔄 Работен процес - Визуализация

## Диаграма на работния процес

```mermaid
flowchart TD
    Start([🚀 Започнете тук]) --> Check{Имате ли<br/>съдържание?}
    
    Check -->|Не| CreateFolder[📁 Създайте папка<br/>mkdir "Тема"]
    Check -->|Да| Scan
    
    CreateFolder --> CopyTemplate[📋 Копирайте шаблон<br/>copy lesson_template.html]
    CopyTemplate --> EditLesson[✏️ Редактирайте урока<br/>code урок.html]
    EditLesson --> Scan
    
    Scan[🔍 Сканирайте<br/>python scanner.py -r] --> Generate[📊 Генериране на<br/>structure.json]
    Generate --> Open[🌐 Отворете в браузър<br/>start index.html]
    
    Open --> View{Изглежда<br/>добре?}
    View -->|Не| Edit[✏️ Редактирайте]
    Edit --> Scan
    
    View -->|Да| Publish{Публикувате<br/>ли?}
    Publish -->|Не| Done([✅ Готово!])
    Publish -->|Да| Deploy[🚀 Публикувайте<br/>GitHub Pages / Netlify]
    Deploy --> Done
    
    style Start fill:#667eea,stroke:#333,color:#fff
    style Done fill:#10b981,stroke:#333,color:#fff
    style Check fill:#f59e0b,stroke:#333,color:#fff
    style View fill:#f59e0b,stroke:#333,color:#fff
    style Publish fill:#f59e0b,stroke:#333,color:#fff
    style Scan fill:#8b5cf6,stroke:#333,color:#fff
    style Generate fill:#8b5cf6,stroke:#333,color:#fff
    style CreateFolder fill:#3b82f6,stroke:#333,color:#fff
    style CopyTemplate fill:#3b82f6,stroke:#333,color:#fff
    style EditLesson fill:#3b82f6,stroke:#333,color:#fff
    style Open fill:#06b6d4,stroke:#333,color:#fff
    style Edit fill:#ec4899,stroke:#333,color:#fff
    style Deploy fill:#10b981,stroke:#333,color:#fff
```

## Структура на системата

```mermaid
graph TB
    subgraph "📁 LessonsFramework"
        A[index.html<br/>🌐 Dashboard]
        B[scanner.py<br/>🐍 Скрипт]
        C[lesson_template.html<br/>📝 Шаблон]
        D[structure.json<br/>📊 Данни]
        
        subgraph "📖 Документация"
            E[README.md<br/>📚 Пълна документация]
            F[TESTING.md<br/>🧪 Тестване]
            G[QUICKREF.md<br/>📋 Справка]
        end
        
        subgraph "📁 Примерни уроци"
            H[Увод в HTML.html<br/>📄 Примерен урок]
        end
    end
    
    B -->|Генерира| D
    D -->|Зарежда| A
    C -->|Копирайте за| H
    A -->|Показва| H
    
    style A fill:#667eea,stroke:#333,color:#fff
    style B fill:#10b981,stroke:#333,color:#fff
    style C fill:#f59e0b,stroke:#333,color:#fff
    style D fill:#8b5cf6,stroke:#333,color:#fff
    style H fill:#06b6d4,stroke:#333,color:#fff
```

## Компоненти на Dashboard

```mermaid
graph LR
    subgraph "🌐 index.html"
        A[Header<br/>🎓 Заглавие]
        B[App Component<br/>⚛️ React]
        C[Card Component<br/>🎴 Карти]
        
        B --> D{Fetch<br/>structure.json}
        D -->|Успешно| E[Сортиране:<br/>Папки → Файлове]
        D -->|Грешка| F[Показване на грешка]
        
        E --> C
        C --> G[📁 Папки]
        C --> H[📄 Файлове]
        
        G -->|Кликване| I[Навигация]
        H -->|Кликване| J[Отваряне на урок]
    end
    
    style A fill:#667eea,stroke:#333,color:#fff
    style B fill:#10b981,stroke:#333,color:#fff
    style C fill:#f59e0b,stroke:#333,color:#fff
    style D fill:#8b5cf6,stroke:#333,color:#fff
    style E fill:#06b6d4,stroke:#333,color:#fff
    style F fill:#ef4444,stroke:#333,color:#fff
    style G fill:#facc15,stroke:#333,color:#fff
    style H fill:#3b82f6,stroke:#333,color:#fff
```

## Логика на scanner.py

```mermaid
flowchart TD
    Start([▶️ Start]) --> Parse[📋 Parse аргументи]
    Parse --> CheckDir{Директорията<br/>съществува?}
    
    CheckDir -->|Не| Error1[❌ Грешка:<br/>Невалидна директория]
    CheckDir -->|Да| ScanStart[🔍 Започване на сканиране]
    
    ScanStart --> GetFiles[📂 Получаване на файлове]
    GetFiles --> Loop{За всеки<br/>файл/папка}
    
    Loop --> Ignore{Игнорира<br/>се?}
    Ignore -->|Да| Loop
    Ignore -->|Не| Type{Тип?}
    
    Type -->|Папка| AddFolder[➕ Добавяне като папка]
    Type -->|HTML файл| AddFile[➕ Добавяне като файл]
    Type -->|Друго| Loop
    
    AddFolder --> Recursive{Рекурсивен<br/>режим?}
    Recursive -->|Да| SubScan[🔄 Сканиране на поддиректория]
    Recursive -->|Не| Loop
    SubScan --> Loop
    
    AddFile --> Loop
    
    Loop -->|Край| Sort[🔤 Сортиране:<br/>Папки → Файлове]
    Sort --> WriteJSON[💾 Запис на JSON]
    WriteJSON --> Stats[📊 Показване на статистика]
    Stats --> Done([✅ Готово])
    
    Error1 --> End([❌ Край])
    
    style Start fill:#667eea,stroke:#333,color:#fff
    style Done fill:#10b981,stroke:#333,color:#fff
    style Error1 fill:#ef4444,stroke:#333,color:#fff
    style End fill:#ef4444,stroke:#333,color:#fff
    style CheckDir fill:#f59e0b,stroke:#333,color:#fff
    style Ignore fill:#f59e0b,stroke:#333,color:#fff
    style Type fill:#f59e0b,stroke:#333,color:#fff
    style Recursive fill:#f59e0b,stroke:#333,color:#fff
    style Loop fill:#f59e0b,stroke:#333,color:#fff
    style ScanStart fill:#8b5cf6,stroke:#333,color:#fff
    style SubScan fill:#8b5cf6,stroke:#333,color:#fff
    style Sort fill:#06b6d4,stroke:#333,color:#fff
    style WriteJSON fill:#10b981,stroke:#333,color:#fff
```

## Структура на lesson template

```mermaid
graph TB
    subgraph "📄 lesson_template.html"
        A[HTML DOCTYPE]
        B[HEAD<br/>Meta, Fonts, Icons, Styles]
        C[BODY]
        
        C --> D[Container]
        D --> E[Header<br/>🎨 Градиент с анимация]
        D --> F[Content<br/>📝 Съдържание на урока]
        D --> G[Footer<br/>ℹ️ Copyright]
        
        F --> H[Заглавия h2, h3]
        F --> I[Параграфи]
        F --> J[Списъци ul, ol]
        F --> K[Код pre, code]
        F --> L[Highlight Box<br/>💡 Важни бележки]
        F --> M[Бутон "Назад"<br/>🔙 Към Dashboard]
    end
    
    style A fill:#667eea,stroke:#333,color:#fff
    style B fill:#8b5cf6,stroke:#333,color:#fff
    style C fill:#10b981,stroke:#333,color:#fff
    style D fill:#06b6d4,stroke:#333,color:#fff
    style E fill:#f59e0b,stroke:#333,color:#fff
    style F fill:#3b82f6,stroke:#333,color:#fff
    style G fill:#6b7280,stroke:#333,color:#fff
    style M fill:#ec4899,stroke:#333,color:#fff
```

---

**Използвайте тези диаграми за по-добро разбиране на системата! 🎨**
