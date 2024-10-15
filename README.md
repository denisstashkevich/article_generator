# PoC generátoru SEO-optimalizovaných článků

Tento Proof of Concept má za cíl vytvořit generátor článků, který pomůže uživateli vytvářet SEO-optimalizovaný obsah na základě zadaných klíčových slov a parametrů. 

## Postup

### 1. Shromáždění vstupních parametrů od uživatele
- **Cíl**: Získat informace pro generování článku.
- **Postup**:
  - Uživatel musí zadat název článku, hlavní klíčové slovo, sekundární klíčové slova (není povinné), požadovaný tón a délku článku.
  - Vstupní data jsou validována a připravena pro další zpracování.

### 2. Generování SEO titulu
- **Cíl**: Vytvořit SEO titulek na základě zadaného názvu a klíčového slova.
- **Postup**:
  - Použití modelu `ChatOpenAI` pro generování SEO titulu.
  - Funkce `generate_seo_title(title, keyword)` vytváří SEO optimalizovaný titulek pomocí předem definovaného promptu.
  - V případě chyby je chyba zaznamenána a proces pokračuje.

### 3. Generování meta popisu
- **Cíl**: Vytvořit meta popis pro článek.
- **Postup**:
  - Funkce `generate_meta_description(title, keyword)` využívá model `ChatOpenAI` k vytvoření poutavého meta popisu zaměřeného na hlavní klíčové slovo.
  - V případě chyby je chyba zaznamenána a proces pokračuje.

### 4. Vytvoření osnovy článku
- **Cíl**: Generovat strukturu článku na základě zadaných klíčových slov.
- **Postup**:
  - Funkce `generate_outline(title, keyword, secondary_keywords)` používá model `ChatOpenAI` k vytvoření podrobné osnovy článku.
  - Osnova zahrnuje hlavní a sekundární témata, která budou pokryta v článku.
  - V případě chyby je chyba zaznamenána a proces pokračuje.

### 5. Generování článku
- **Cíl**: Vytvořit samotný článek na základě zadaných parametrů.
- **Postup**:
  - Funkce `generate_article(title, keyword, secondary_keywords, tone, length)` využívá model `ChatOpenAI` k napsání článku s požadovaným tónem a délkou.
  - Článek je strukturován s nadpisy a podnadpisy, obsahuje přirozené začlenění klíčových slov.
  - V případě chyby je chyba zaznamenána a proces se ukončí.

### 6. Hodnocení čitelnosti článku
- **Cíl**: Posoudit čitelnost a úroveň složitosti textu.
- **Postup**:
  - Funkce `evaluate_readability(article)` používá knihovnu `textstat` k výpočtu Flesch Reading Ease a Flesch-Kincaid Grade Level skóre.
  - Výsledky poskytují objektivní měření čitelnosti článku.

### 7. Hodnocení kvality obsahu
- **Cíl**: Subjektivně posoudit kvalitu obsahu článku.
- **Postup**:
  - Funkce `evaluate_content_quality(article)` využívá model `ChatOpenAI` k hodnocení koherence, konzistence tónu a celkové kvality článku.
  - Výsledky poskytují subjektivní hodnocení obsahu.

### 8. Uložení a zobrazení výsledků
- **Cíl**: Uložit vygenerovaný článek a jeho hodnocení do souboru a zobrazit je uživateli.
- **Postup**:
  - Funkce `save_article_to_file(...)` ukládá SEO titulek, meta popis, osnovu, generovaný článek, hodnocení čitelnosti a hodnocení obsahu do textového souboru.
  - Výsledky jsou také zobrazeny v konzoli pro okamžitou kontrolu uživatelem.


