# Инструкция по публикации сайта

## 1. GitHub Pages

### Создать репозиторий
1. Зайдите на github.com → New repository
2. Название: `pldplastics` (или другое)
3. Публичный (Public)
4. Загрузите все файлы папки в репозиторий

### Включить GitHub Pages
1. Settings → Pages
2. Source: Deploy from branch → `main` → `/ (root)`
3. Сайт появится по адресу: `https://username.github.io/pldplastics/`

---

## 2. Домен на reg.ru

### Рекомендуемый домен
`pldplastics.com` — ближайший к оригиналу `pldplastic.com`

Альтернативы: `pld-plastic.com`, `pulide.com`, `pulide.ru`

### Привязать домен к GitHub Pages
1. На reg.ru зайдите в управление DNS домена
2. Удалите стандартные записи A
3. Добавьте 4 записи A:
   ```
   @ → 185.199.108.153
   @ → 185.199.109.153
   @ → 185.199.110.153
   @ → 185.199.111.153
   ```
4. Добавьте CNAME:
   ```
   www → username.github.io
   ```
5. На GitHub: Settings → Pages → Custom domain → введите `pldplastics.com`
6. Поставьте галочку "Enforce HTTPS"

SSL (HTTPS) включается автоматически через ~24 часа после привязки DNS.

---

## 3. Заполнить контакты

Найдите в файлах и замените:
- `+7 (XXX) XXX-XX-XX` → ваш реальный номер
- `info@pldplastics.com` → ваш email
- `https://wa.me/7XXXXXXXXXX` → ваш WhatsApp
- `https://t.me/username` → ваш Telegram

---

## 4. Форма обратной связи

На странице contact.html форма настроена под **Formspree**:
1. Зарегистрируйтесь на formspree.io
2. Создайте форму и получите ID (вида `f/xpzgkwqo`)
3. В contact.html замените `YOUR_FORM_ID` на ваш ID

---

## 5. Яндекс.Метрика

Добавьте код Яндекс.Метрики перед `</head>` на каждой странице:
```html
<!-- Yandex.Metrika counter -->
<script type="text/javascript">
   (function(m,e,t,r,i,k,a){...})(...);
</script>
```
Получить код: metrika.yandex.ru → Добавить счётчик

---

## Структура файлов
```
pldplastics/
├── index.html          ← Главная
├── about.html          ← О компании
├── products.html       ← Каталог продуктов
├── brands.html         ← Бренды
├── applications.html   ← Применение
├── news.html           ← Новости
├── contact.html        ← Контакты
├── css/
│   └── style.css
├── js/
│   └── main.js
├── img/                ← Добавьте изображения с оригинального сайта
├── .nojekyll
└── DEPLOY.md
```
