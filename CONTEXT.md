# CONTEXT — Сайт-зеркало SUPULIDE / pldplastics.com (рус.)

> Этот файл передаёт полный контекст проекта в новую сессию.
> Прочитай его целиком, прежде чем делать что-либо.

---

## 1. Суть проекта

Статический HTML-сайт (GitHub Pages) — русскоязычное зеркало китайского производителя пластиков
**Jiangsu Pulide Plastic Co., Ltd.** (бренд SUPULIDE).
Домен: **pldplastics.com** (хостинг reg.ru → GitHub Pages).

### Жёсткие ограничения (нельзя нарушать):
- Весь текст — **на русском языке**.
- Контакты — только плейсхолдеры: `+7 (XXX) XXX-XX-XX`, `info@pldplastics.com`.
- **Все изображения локальные** в `img/`. CDN `thefastimg.com` блокирует не-китайские IP.
- `<meta name="referrer" content="no-referrer">` — **на каждой странице** в `<head>`.
- Ни слова о том, что сайт является дистрибьютором/представителем — позиционируется как сама компания.
- `onerror="this.src='img/adv-tech.jpg'"` (или другой fallback) — **на каждом** `<img>`.

---

## 2. Структура файлов

```
pldplastic-ru/
├── index.html             ✅
├── products.html          ✅
├── about.html             ✅
├── contact.html           ✅
├── applications.html      ✅
├── brands.html            ✅
├── news.html              ✅
├── news-industry.html     ✅
├── warehouse.html         ✅
├── new-ind-1.html … new-ind-6.html   ✅ (6 отраслевых новостей)
├── product-poe.html       ✅
├── product-pop.html       ✅
├── product-obc.html       ✅
├── product-eva.html       ✅
├── product-eaa.html       ✅
├── product-emaa.html      ✅
├── product-evoh.html      ✅
├── product-pa12e.html     ✅
├── product-epdm.html      ✅
├── product-mlldpe.html    ✅
├── product-xlpe.html      ✅
├── product-pc.html        ✅
├── product-pcabs.html     ✅
├── product-pmma.html      ✅
├── product-pom.html       ✅
├── product-pa66.html      ✅
├── product-pa12.html      ✅  ← создан последним
├── product-lcp.html       ❌  ← СЛЕДУЮЩИЙ на очереди
├── product-ppsu.html      ❌
├── product-psu.html       ❌
├── product-pes.html       ❌
├── news-detail-1.html … news-detail-4.html  ❌
├── css/style.css          ✅
├── js/main.js             ✅
├── img/                   ✅ (частично, нужен download-media.sh)
├── download-media.sh      ✅ (нужно добавить PA12-блок)
└── СКАЧАТЬ-ФОТО.command   ✅
```

---

## 3. Боковая панель — порядок категорий (21 позиция)

```
POE · POP · OBC · EVA · EAA · EMAA · EVOH · PA12 Эластомер ·
EPDM · MLLDPE · XLPE · PC · PC/ABS · PMMA · POM · PA66 · PA12 ·
LCP · PPSU · PSU · PES
```

На каждой странице продукта — ссылка на текущую страницу имеет `class="active"`.

---

## 4. Шаблон страницы продукта

Все страницы следуют одному шаблону. Эталон — `product-pa66.html`.
Ключевые элементы:
- `<meta name="referrer" content="no-referrer">` в `<head>`
- Hero-баннер: `img/prod-hero.jpg` (onerror: `img/hero-1.jpg`), height 280px
- Хлебные крошки: `Главная › Продукты › [НАЗВАНИЕ]`
- Боковая панель (все 21 категория, активная — с `class="active"`)
- `<div class="proddet-top">`: фото продукта + info-панель с H1, категория, описание, кнопки
- `<div class="proddet-body">`: описание, иконки применения, таблицы марок
- Форма запроса (textarea предзаполнен `"[НАЗВАНИЕ] — "`)
- Блок «Похожие продукты»

---

## 5. Следующий файл: product-lcp.html

### Откуда взять данные:
Скачать HTML-источник: `https://www.pldplastic.com/Products1/LCP.html`
Затем создать по шаблону `product-pa66.html`.

---

## 5a. ✅ ВЫПОЛНЕНО: product-pa12.html

### Основные данные:
- **Файл**: `pldplastic-ru/product-pa12.html`
- **Активная ссылка в сайдбаре**: `product-pa12.html` (после PA66, перед LCP)
- **Категория**: Термопласты
- **Фото продукта**: `img/prod-pa12.jpg` (UUID: `8e7b1afa-7a05-4ac6-a71f-638bc77a66e4.jpg`)
- **Форма**: textarea предзаполнен `"PA12 — "`
- **Похожие продукты**: PA66, POM, PA12 Эластомер, PC

### Описание (русский текст):

```
PA12 (полиамид 12, нейлон 12) — термопластичный полиамид с длинной алифатической цепью. Обладает исключительной гибкостью, низким водопоглощением, превосходной химической стойкостью и усталостной прочностью. Применяется в автомобильных трубопроводах, кабельных оболочках, 3D-печати и порошковых покрытиях.

В октябре 2022 года компания Wanhua Chemical (万华化学) ввела в строй полную производственную цепочку PA12 в Китае, став первым производителем в Азии и вторым в мире, освоившим полный цикл синтеза полиамида 12. До этого монополию на производство PA12 удерживали четыре западных и японских производителя: EMS (Швейцария), Arkema (Франция), Ube (Япония) и Evonik (Германия).
```

### Иконки применения (4 шт., `repeat(4, 1fr)`):

| Файл иконки | UUID | Подпись |
|---|---|---|
| `icon-pa12-auto.jpg` | `6e3ef03b-8a35-49db-bdc2-1bc57ca3b6a3.jpg` | Автомобильные трубопроводы |
| `icon-pa12-cable.jpg` | `7e023b15-1418-4b0a-9bbd-20fcc65f976d.jpg` | Кабели |
| `icon-pa12-3d.jpg` | `a9b14cdd-82ea-455f-b9ee-1dd0583bba9b.jpg` | 3D-печать |
| `icon-pa12-powder.jpg` | `ec83bed1-bbf8-4e72-bba4-2b7f3da1576a.jpg` | Порошковое покрытие |

### Дополнительное фото (Wanhua, в тексте описания):
- `img/img-pa12-wanhua.jpg` (UUID: `ca83a6ad-c07a-4d99-aa7a-5f91fcc2823a.jpg`)
- Вставить как `<img>` в блок описания рядом с текстом про Wanhua
- onerror: `img/adv-tech.jpg`

### Таблицы марок:

#### Таблица 1: Wanmide™ PA12 (Wanhua Chemical / 万华化学)
**4 колонки**: Торговая марка | Марка | Плотность г/см³ | Прочность на разрыв МПа

| Торговая марка | Марка | Плотность г/см³ | Прочность на разрыв МПа |
|---|---|---|---|
| Wanmide™ PA12 | L2001T | 1.02 | 36 |
| Wanmide™ PA12 | L2040P | 1.02 | 27 |
| Wanmide™ PA12 | L2030P | 1.03 | 24 |
| Wanmide™ PA12 | L2102E | 0.98 | 40 |
| Wanmide™ PA12 | L2150C | 1.08 | 120 |
| Wanmide™ PA12 | L2300G | 1.23 | 120 |

#### Таблица 2: Rilsan® PA12 (Arkema / 阿科玛)
**5 колонок**: Торговая марка | Марка | Плотность г/см³ | ПТР г/10 мин | Прочность на разрыв МПа

| Торговая марка | Марка | Плотность г/см³ | ПТР г/10 мин | Прочность на разрыв МПа |
|---|---|---|---|---|
| Rilsan® PA12 | AESN P20 TL | 1.02 | 30 | 30 |

---

## 6. Обновление download-media.sh

После PA66-блока (строки 162–169) добавить:

```bash
# Изображение продукта и иконки применения — страница PA12
download "$BASE/8e7b1afa-7a05-4ac6-a71f-638bc77a66e4.jpg"   "prod-pa12.jpg"
download "$BASE/6e3ef03b-8a35-49db-bdc2-1bc57ca3b6a3.jpg"   "icon-pa12-auto.jpg"
download "$BASE/7e023b15-1418-4b0a-9bbd-20fcc65f976d.jpg"   "icon-pa12-cable.jpg"
download "$BASE/a9b14cdd-82ea-455f-b9ee-1dd0583bba9b.jpg"   "icon-pa12-3d.jpg"
download "$BASE/ec83bed1-bbf8-4e72-bba4-2b7f3da1576a.jpg"   "icon-pa12-powder.jpg"
download "$BASE/ca83a6ad-c07a-4d99-aa7a-5f91fcc2823a.jpg"   "img-pa12-wanhua.jpg"
```

---

## 7. Оставшиеся задачи (в порядке приоритета)

1. **`product-lcp.html`** — скачать источник с pldplastic.com, создать страницу ← СЛЕДУЮЩЕЕ
2. **`product-ppsu.html`** — скачать источник, создать страницу
3. **`product-psu.html`** — скачать источник, создать страницу
4. **`product-pes.html`** — скачать источник, создать страницу
5. **`news-detail-1.html` … `news-detail-4.html`** — 4 страницы новостей-деталей
6. **Деплой** на GitHub Pages + домен pldplastics.com через reg.ru

---

## 8. CDN-базовый URL для UUID изображений

```
https://omo-oss-image.thefastimg.com/portal-saas/pg2024042811332048086/cms/image/{UUID}.{ext}
```

Формат вызова в download-media.sh:
```bash
download "$BASE/{UUID}.jpg"   "локальное-имя.jpg"
```

---

## 9. Источник оригинала

Оригинальный сайт: **https://www.pldplastic.com/**
Страницы продуктов: `https://www.pldplastic.com/Products1/{PRODUCT}.html`

---

*Файл создан для передачи контекста между сессиями. Актуален на 2026-06-24.*
