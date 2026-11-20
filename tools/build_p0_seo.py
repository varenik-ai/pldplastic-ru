#!/usr/bin/env python3
"""P0 из audit/competitors-ru.md: H1/title RU, BreadcrumbList, блок «Условия поставки».

1. product-*.html (RU): H1 = аббревиатура + описательная подпись (span) с русским названием материала;
   <title> и og:title под связку «название + гранулы/купить + оптом + из Китая». Английское имя в hero остаётся.
2. product-*.html (RU и EN) и products.html (RU и EN): JSON-LD BreadcrumbList по видимым хлебным крошкам.
3. product-*.html (RU и EN): блок «Условия поставки» — только факты, уже опубликованные на сайте
   (EXW/FOB/CIF, TDS/COA/MSDS, образцы, цена и наличие по запросу, ответ за 24 часа). Сроки/MOQ/оплату не указываем.
Повторный запуск заменяет блоки. Запуск из корня: python3 tools/build_p0_seo.py
"""
import html as H
import json
import os
import re
from urllib.parse import urljoin

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
SITE = 'https://pldpolymer.com/'

# pid -> (аббревиатура в H1, описательная подпись H1, title)
RU = {
    'poe': ('POE', 'полиолефиновый эластомер', 'Полиолефиновый эластомер POE — купить оптом из Китая | SUPULIDE'),
    'pop': ('POP', 'полиолефиновый пластомер', 'Полиолефиновый пластомер POP — купить оптом из Китая | SUPULIDE'),
    'obc': ('OBC', 'олефиновый блок-сополимер', 'Олефиновый блок-сополимер OBC — купить оптом из Китая | SUPULIDE'),
    'eva': ('EVA', 'этиленвинилацетат (ЭВА, СЭВА)', 'Этиленвинилацетат EVA (ЭВА) — гранулы оптом из Китая | SUPULIDE'),
    'eaa': ('EAA', 'сополимер этилена и акриловой кислоты', 'Сополимер этилена и акриловой кислоты EAA — оптом из Китая | SUPULIDE'),
    'emaa': ('EMAA', 'сополимер этилена и метакриловой кислоты, иономеры', 'EMAA (этилен-метакриловая кислота) — оптом из Китая | SUPULIDE'),
    'evoh': ('EVOH', 'этиленвиниловый спирт (барьерный полимер)', 'EVOH — этиленвиниловый спирт, барьерный полимер из Китая | SUPULIDE'),
    'epdm': ('EPDM', 'этиленпропиленовый каучук (СКЭПТ)', 'Этиленпропиленовый каучук EPDM — купить оптом из Китая | SUPULIDE'),
    'mlldpe': ('MLLDPE', 'металлоценовый полиэтилен', 'Металлоценовый полиэтилен MLLDPE — купить оптом из Китая | SUPULIDE'),
    'xlpe': ('XLPE', 'сшитый полиэтилен для кабелей', 'Сшитый полиэтилен XLPE для кабелей — оптом из Китая | SUPULIDE'),
    'pc': ('PC', 'поликарбонат (ПК) в гранулах', 'Поликарбонат PC в гранулах — купить оптом из Китая | SUPULIDE'),
    'pcabs': ('PC/ABS', 'сплав поликарбоната и АБС', 'Сплав PC/ABS (поликарбонат + АБС) — купить оптом из Китая | SUPULIDE'),
    'pmma': ('PMMA', 'полиметилметакрилат (оргстекло, акрил)', 'Полиметилметакрилат PMMA в гранулах — оптом из Китая | SUPULIDE'),
    'pom': ('POM', 'полиацеталь (полиоксиметилен, полиформальдегид)', 'Полиацеталь POM (полиоксиметилен) — гранулы оптом из Китая | SUPULIDE'),
    'pa66': ('PA66', 'полиамид 66 (нейлон 66, ПА 66)', 'Полиамид 66 PA66 (нейлон) — гранулы оптом из Китая | SUPULIDE'),
    'pa12': ('PA12', 'полиамид 12 (нейлон 12, ПА 12)', 'Полиамид 12 PA12 (нейлон) — гранулы оптом из Китая | SUPULIDE'),
    'pa12e': ('PA12 эластомер', 'полиамидный термопластичный эластомер (PEBA)', 'Эластомер PA12 (PEBA) — купить оптом из Китая | SUPULIDE'),
    'lcp': ('LCP', 'жидкокристаллический полимер', 'Жидкокристаллический полимер LCP — купить оптом из Китая | SUPULIDE'),
    'ppsu': ('PPSU', 'полифенилсульфон', 'Полифенилсульфон PPSU — купить гранулы оптом из Китая | SUPULIDE'),
    'psu': ('PSU', 'полисульфон', 'Полисульфон PSU — купить гранулы оптом из Китая | SUPULIDE'),
    'pes': ('PES', 'полиэфирсульфон', 'Полиэфирсульфон PES — купить гранулы оптом из Китая | SUPULIDE'),
}

SUPPLY = {
    'ru': ('Условия поставки', [
        ('Условия', 'EXW, FOB или CIF — выбираете вы'),
        ('Документы', 'TDS, COA и MSDS по запросу; образцы для испытаний'),
        ('Цена и наличие', 'по запросу — коммерческое предложение по марке и объёму'),
        ('География', 'Россия и СНГ'),
        ('Срок ответа', 'специалист свяжется в течение 24 часов'),
    ], 'Минимальную партию, сроки поставки и порядок оплаты согласуем в коммерческом предложении.'),
    'en': ('Supply terms', [
        ('Terms', 'EXW, FOB or CIF — your choice'),
        ('Documents', 'TDS, COA and MSDS on request; samples for testing'),
        ('Price and availability', 'on request — a quotation for your grade and volume'),
        ('Destinations', 'Russia and CIS'),
        ('Reply time', 'our manager replies within 24 hours'),
    ], 'Minimum order, lead time and payment terms are agreed in the quotation.'),
}

CSS = """
/* P0 SEO (tools/build_p0_seo.py) */
.prod-hero-h1-d { display: block; font-size: clamp(13px, .36em, 22px); font-weight: 600; letter-spacing: 0; line-height: 1.3; margin-top: 8px; }
.prod-hero-section { height: auto; min-height: 340px; }
@media (max-width: 768px) { .prod-hero-section { height: auto; min-height: 250px; } }
@media (max-width: 480px) { .prod-hero-section { height: auto; min-height: 220px; } }
.supply-terms { margin-top: 24px; }
.supply-list { list-style: none; margin: 10px 0 8px; padding: 0; }
.supply-list li { padding: 7px 0; border-bottom: 1px solid var(--border); line-height: 1.5; }
.supply-list li strong { display: inline-block; min-width: 150px; }
.supply-note { font-size: 13px; color: #666; margin: 6px 0 0; }
@media (max-width: 600px) { .supply-list li strong { display: block; min-width: 0; } }
"""


def strip(s, tag):
    return re.sub(rf'[ \t]*<!-- {tag} -->.*?<!-- /{tag} -->\n?', '', s, flags=re.S)


def set_head(s, title):
    t = H.escape(title, quote=True)
    s = re.sub(r'<title>.*?</title>', lambda m: f'<title>{H.escape(title)}</title>', s, count=1, flags=re.S)
    s = re.sub(r'(<meta property="og:title" content=")[^"]*(")', lambda m: m.group(1) + t + m.group(2), s, count=1)
    s = re.sub(r'(<meta name="twitter:title" content=")[^"]*(")', lambda m: m.group(1) + t + m.group(2), s, count=1)
    return s


def set_h1(s, abbr, desc):
    new = f'<h1 class="prod-hero-h1">{H.escape(abbr)}<span class="prod-hero-h1-d"> — {H.escape(desc)}</span></h1>'
    s, n = re.subn(r'<h1 class="prod-hero-h1">.*?</h1>', lambda m: new, s, count=1, flags=re.S)
    assert n == 1
    # английское имя в подзаголовке остаётся, русское дублирование убираем
    s = re.sub(r'(<p class="prod-hero-sub">[^<&]*?)\s*&mdash;\s*[^<]*(</p>)', r'\1\2', s, count=1)
    return s


def breadcrumb_ld(s, url):
    m = re.search(r'<nav aria-label="breadcrumb"[^>]*>(.*?)</nav>', s, re.S)
    if not m:
        return None
    items = []
    if '<ol' in m.group(1):  # разметка списком: <li><a>…</a></li> › <li>Текущая</li>
        for li in re.findall(r'<li[^>]*>(.*?)</li>', m.group(1), re.S):
            txt = re.sub(r'<[^>]+>', '', li).strip()
            if txt in ('›', '/', '»', ''):
                continue
            a = re.search(r'<a href="([^"]*)"', li)
            items.append((txt, urljoin(url, a.group(1)) if a else url))
        return None if len(items) < 2 else {'@context': 'https://schema.org', '@type': 'BreadcrumbList',
            'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': u} for i, (n, u) in enumerate(items)]}
    for a in re.finditer(r'<a href="([^"]*)"[^>]*>(.*?)</a>', m.group(1), re.S):
        items.append((re.sub(r'<[^>]+>', '', a.group(2)).strip(), urljoin(url, a.group(1))))
    last = re.search(r'<span[^>]*>(.*?)</span>\s*$', m.group(1).strip(), re.S)
    if last:
        items.append((re.sub(r'<[^>]+>', '', last.group(1)).strip(), url))
    if len(items) < 2:
        return None
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList',
            'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': u} for i, (n, u) in enumerate(items)]}


def add_breadcrumb(s, path):
    s = re.sub(r'[ \t]*<script type="application/ld\+json" id="breadcrumb-ld">.*?</script>\n?', '', s, flags=re.S)
    url = SITE + path
    ld = breadcrumb_ld(s, url)
    if not ld:
        return s
    tag = ('  <script type="application/ld+json" id="breadcrumb-ld">\n' + json.dumps(ld, ensure_ascii=False, indent=2)
           + '\n  </script>\n')
    return s.replace('</head>', tag + '</head>', 1)


def supply_block(lang):
    title, rows, note = SUPPLY[lang]
    li = ''.join(f'<li><strong>{H.escape(k)}:</strong> {H.escape(v)}</li>' for k, v in rows)
    return ('<!-- supply -->\n      <div class="proddet-body supply-terms" id="supply-terms"><h2><i class="fas fa-truck" '
            f'style="margin-right:8px;color:var(--blue);"></i>{title}</h2><ul class="supply-list">{li}</ul>'
            f'<p class="supply-note">{H.escape(note)}</p></div>\n      <!-- /supply -->\n')


def add_supply(s, lang):
    s = strip(s, 'supply')
    j = next((s.find(a) for a in ('<!-- names -->', '<!-- faq', '<div class="proddet-form"') if a in s), -1)
    assert j > 0
    ls = s.rfind('\n', 0, j) + 1
    return s[:ls] + '      ' + supply_block(lang).lstrip() + s[ls:]


def add_css():
    p = 'css/style.css'
    s = open(p, encoding='utf-8').read()
    s = re.sub(r'\n/\* P0 SEO \(tools/build_p0_seo.py\) \*/.*?(?=\n/\* popular grades|\Z)', '', s, flags=re.S)
    open(p, 'w', encoding='utf-8').write(s.rstrip('\n') + '\n' + CSS)


def main():
    for pid, (abbr, desc, title) in RU.items():
        for lang, path in (('ru', f'product-{pid}.html'), ('en', f'en/product-{pid}.html')):
            if not os.path.exists(path):
                print('нет файла', path)
                continue
            s = open(path, encoding='utf-8').read()
            if lang == 'ru':
                s = set_head(s, title)
                s = set_h1(s, abbr, desc)
            s = add_breadcrumb(s, path)
            s = add_supply(s, lang)
            open(path, 'w', encoding='utf-8').write(s)
    for path in ('products.html', 'en/products.html'):
        s = open(path, encoding='utf-8').read()
        open(path, 'w', encoding='utf-8').write(add_breadcrumb(s, path))
    add_css()
    print('ok')


if __name__ == '__main__':
    main()
