# Публикация и обслуживание pldpolymer.com

Актуально на 2026-10-19.

## 1. Хостинг (GitHub Pages)

- Репозиторий: `varenik-ai/pldplastic-ru`, ветка `main`, корень `/`.
- Файл `CNAME` содержит `pldpolymer.com`; `.nojekyll` присутствует.
- Деплой: запустить `push.command` двойным кликом в Finder (коммит + push).
  Токен GitHub лежит внутри скрипта — не публиковать и не пересылать файл.

## 2. Домен (reg.ru)

- NS: `ns1.reg.ru`, `ns2.reg.ru`.
- 4 записи A для `@`: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`.
- В GitHub: Settings → Pages → Custom domain = `pldpolymer.com`, «Enforce HTTPS» включено.
- Cloudflare / Workers не задействованы.

## 3. Контакты на сайте

- Email: `export@pldpolymer.com`; WeChat: `Leo_Li81`.
- Телефон — только placeholder в поле формы `+7 (XXX) XXX-XX-XX` (`contact.html`, `en/contact.html`); публичного номера на сайте нет.

## 4. Форма обратной связи

Форма в `contact.html` / `en/contact.html`. Отправка идёт через web3forms (`https://api.web3forms.com/submit`, скрытое поле `access_key` в обеих contact-страницах). Письма приходят на почту владельца ключа; при смене почты получить новый ключ на web3forms.com.

## 5. Аналитика

- Яндекс.Метрика: счётчик `111389593` (старый `110251458` удалён).
- Google Analytics 4: `G-J4C1XB482H`.
- Google Search Console: ресурс-домен `pldpolymer.com`, sitemap `https://pldpolymer.com/sitemap.xml` (74 URL).

## 6. Чек-лист после изменений

1. Обновить `sitemap.xml` (lastmod) и `gsc-url-checklist.txt` при добавлении страниц.
2. Проверить взаимные hreflang RU↔EN и canonical у новых страниц.
3. Задеплоить через `push.command`, затем запросить индексирование новых URL в GSC (лимит ~10/сутки).

## 7. Структура

```
pldplastic-ru/
├── index.html, products.html, about.html, contact.html, applications.html,
│   brands.html, news.html, news-industry.html, warehouse.html, 404.html
├── product-*.html (21), news-detail-1..4.html, new-ind-1..6.html
├── en/            ← английская версия (21 product + 13 страниц разделов)
├── css/style.css, js/main.js, img/, products/
├── sitemap.xml, robots.txt, CNAME, .nojekyll
├── gsc-url-checklist.txt, push.command (локально, в .gitignore), download-media.sh
└── CONTEXT.md, DEPLOY.md
```
