---
config:
  layout: tidy-tree
  theme: base
  fontFamily: "MapFont, Calibri, Carlito, sans-serif"
  themeVariables:
    fontFamily: "MapFont, Calibri, Carlito, sans-serif"
    fontSize: 15px
    primaryColor: "#F2F4F7"
    primaryTextColor: "#1B2230"
    cScale0: "#E8A33D"
    cScaleLabel0: "#1B2230"
    cScale1: "#2A9D8F"
    cScaleLabel1: "#FFFFFF"
    cScale2: "#7FA7D9"
    cScaleLabel2: "#1B2230"
    cScale3: "#D1495B"
    cScaleLabel3: "#FFFFFF"
    cScale4: "#9CCB86"
    cScaleLabel4: "#1B2230"
    cScale5: "#B49FDA"
    cScaleLabel5: "#1B2230"
    cScale6: "#F08A5D"
    cScaleLabel6: "#1B2230"
    cScale7: "#8A97A8"
    cScaleLabel7: "#1B2230"
---
mindmap
  root(("Символни низове в C#"))
    Типът string
      Последователност от char
      Референтен тип, стойност null
      Неизменим: всеки метод връща нов низ
      n1["'A' е char, „A“ е string"]
      n2["null ≠ празен низ „“"]
    Дължина и индекси
      s.Length
      n3["Индекси от 0 до Length − 1"]
      n4["s[i] е само за четене"]
      IndexOutOfRangeException
    Долепване
      n5["Оператори + и +="]
      n6["string.Concat(a, b)"]
      n7["Интерполация $„Здравей, {name}!“"]
    Малки и главни букви
      n8["ToLower()"]
      n9["ToUpper()"]
      Сравнение без регистър
    Търсене
      n10["IndexOf(x) → първо срещане"]
      n11["LastIndexOf(x) → последно срещане"]
      n12["Връщат −1, ако няма"]
      Различават регистъра
    Извличане и замяна
      n13["Substring(начало, дължина)"]
      n14["Substring(начало) → до края"]
      n15["Replace(стар, нов) → всички срещания"]
    Специални символи
      n16["Escaping с обратна наклонена черта"]
      n17["Нов ред, табулация, кавичка"]
      n18["Цитиран низ @ → всичко буквално"]
    Графични приложения
      n19["textBox1.Text → вход"]
      n20["label1.Text → резултат"]
      n21["button1_Click → събитие"]
      n22["Число към текст: .ToString()"]
