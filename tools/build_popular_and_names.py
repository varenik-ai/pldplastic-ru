#!/usr/bin/env python3
"""Популярные марки и русские названия полимеров.

Что делает (повторный запуск заменяет блоки, ничего не дублируя):
  1. На страницах product-*.html (RU и EN) — блок «Популярные марки» перед первым описанием.
  2. На страницах RU — блок «Названия и частые вопросы» (по реальным запросам Яндекс Вордстат, окт–ноя 2026).
  3. В карточках products.html и en/products.html — строка «Популярные марки».
  4. Страница-справочник polymer-names.html «Полимеры: русские названия и аббревиатуры» (RU).

«Популярные» — редакционная подборка известных на рынке марок из нашего каталога (data/grades.*.json),
а не статистика продаж. Наличие и условия поставки подтверждаем по запросу.
Запуск из корня репозитория: python3 tools/build_popular_and_names.py
"""
import html as H
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

# Подборка: pid -> [(подпись, страница-марки или None)]. Названия марок — как в таблицах каталога.
POPULAR = {
    'poe': [('ENGAGE™ 8150', None), ('ENGAGE™ 8200', None), ('ENGAGE™ 8100', None), ('LUCENE™ LC670', 'grade-lucene-poe-lc670.html'),
            ('LUCENE™ LC875', None), ('EXACT™ 5101', 'grade-exact-poe-5101.html')],
    'pop': [('AFFINITY™ PL 1880G', None), ('AFFINITY™ PL 1850G', None), ('AFFINITY™ PF 1140G', None), ('VISTAMAXX™ 6102', None)],
    'obc': [('INFUSE™ 9100', None), ('INFUSE™ 9107', None), ('INFUSE™ 9507', None), ('INFUSE™ 9530', None)],
    'eva': [('SEETEC™ VA900', None), ('SEETEC™ VA600', None), ('ELVAX™ 3150', None), ('SEETEC™ EA28150', None),
            ('EVASINE® UE4055', 'grade-evasine-eva-ue4055.html')],
    'eaa': [('PRIMACOR™ 3440', None), ('PRIMACOR™ 3460', None), ('PRIMACOR™ 5986', None), ('NUCREL™ 3990', None)],
    'emaa': [('SURLYN™ 8920', None), ('SURLYN™ 8940', None), ('NUCREL™ 0910', None)],
    'evoh': [('Sinopec EW-3201S', 'grade-sinopec-evoh-ew-3201s.html'), ('EVASIS™ EV3251F', 'grade-evasis-ev3251f.html'),
             ('EVAL™ F171B', None), ('SOARNOL™ DC3233RB', None)],
    'epdm': [('NORDEL™ 4725P', None), ('NORDEL™ 3722P', None), ('SABIC® EPDM 626', None), ('EPT™ 3072EM', None)],
    'mlldpe': [('Exceed™ 1018MA', None), ('DOWLEX™ 2045G', None), ('ELITE™ 5400G', None), ('Exceed™ 3518CB', None)],
    'pa66': [('Shenmamid™ 2500', None), ('Shenmamid™ 2550', None), ('Ultramid® A3WG6', None), ('Ultramid® A3WG7', None)],
    'pa12': [('Wanmide™ L2001T', None), ('Wanmide™ L2040P', None), ('Rilsan® AESN P20 TL', None)],
    'pc': [('Clarnate® A1227', 'grade-clarnate-pc-a1227.html'), ('Clarnate® A1105', 'grade-clarnate-pc-a1105.html'),
           ('Clarnate® A1225', None), ('Clarnate® HL6157', 'grade-clarnate-pc-hl6157.html')],
    'pcabs': [('WanBlend® CA1580', None), ('WanBlend® CA1560', None), ('WanBlend® CA3250', None)],
    'pmma': [('Wanhua® HD01', None), ('Wanhua® HD03', None), ('Wanhua® MG01', None), ('Acryrex® CM-205', None)],
    'pom': [('Delrin® 500P', None), ('Delrin® 100P', None), ('KEPITAL™ F20-03', 'grade-kepital-f20-03.html'),
            ('Hostaform™ C9021', None), ('Yuntianhua® M90/N90', None), ('Yuntianhua® GM90', 'grade-yuntianhua-pom-gm90.html')],
    'ppsu': [('Ultrason® PPSU P 3010', None), ('Holand® PPSU P300', None), ('Wanhua PPSU P6070', None)],
    'psu': [('Ultrason® S PSU 3010', None), ('Ultrason® S PSU 2010', None), ('Wanhua PSU U3060', None), ('Holand® PSU S200', None)],
    'pes': [('Ultrason® E PES 2010', 'grade-basf-ultrason-e-pes-2010.html'), ('Veradel® 3500', None),
            ('Sumikaexcel® 4100G', None), ('Holand® PES E200', None)],
    'lcp': [('Wote™ KD230NI/BI', None), ('Wote™ KD235NI/BI', None), ('Wote™ KD130NI/BI', None)],
}

# Блок «Названия и частые вопросы» (RU). Темы — из Вордстат и GSC; ответы — общеизвестные сведения о материалах.
NAMES = {
    'pom': [
        ('Как ещё называют POM?',
         'Полиоксиметилен (POM) — то же вещество, что полиацеталь и полиформальдегид. На рынке встречаются торговые названия Delrin, '
         'Hostaform, Celcon, KEPITAL. Делрин — гомополимер; Hostaform, Celcon и KEPITAL — сополимеры. Марки обоих типов есть в таблицах ниже.'),
        ('Чем склеить или сварить POM?',
         'POM плохо склеивается из-за низкой поверхностной энергии: как правило, нужна подготовка поверхности (травление или праймер). '
         'Поэтому в серийном производстве чаще используют сварку трением, ультразвуком или нагретым инструментом, а также защёлки и винты.'),
        ('Как выбрать марку POM по текучести?',
         'Марки различаются показателем текучести расплава (ПТР): с высоким ПТР удобнее отливать тонкостенные и сложные детали, '
         'с низким — экструдировать и изготавливать нагруженные детали. Значения ПТР указаны в таблицах марок.'),
    ],
    'pa66': [
        ('Как ещё называют PA66?',
         'Полиамид 66 — это ПА 66, ПА66, PA66 и нейлон 66. Гранулы поставляем в ненаполненном и наполненном виде; в обозначении Ultramid '
         'буквы WG означают стеклонаполненную марку.'),
        ('Чем PA66 отличается от PA6?',
         'PA66 плавится при более высокой температуре (около 262 °C против примерно 220 °C у PA6), жёстче и теплостойче; PA6 сильнее впитывает влагу '
         'и обычно дешевле. Выбор зависит от рабочей температуры детали и условий эксплуатации.'),
        ('Сколько стоят гранулы PA66 из Китая?',
         'Цена зависит от марки, наполнения (стекловолокно, минеральные наполнители, антипирен), объёма партии и условий поставки. '
         'Укажите марку и объём в форме запроса — подготовим коммерческое предложение.'),
    ],
    'epdm': [
        ('Что такое EPDM и как его называют по-русски?',
         'EPDM — этилен-пропилен-диеновый каучук (в российской терминологии — СКЭПТ, этиленпропиленовый каучук). Диеновый сомономер даёт '
         'возможность вулканизации серой; каучук без диена (EPM) вулканизуют пероксидом.'),
        ('Вы поставляете готовые мембраны и вспененный каучук?',
         'Нет, мы поставляем сырьё — марки EPDM для переработки и компаундирования. Готовые мембраны, шнуры и вспененные листы изготавливает заказчик.'),
    ],
    'eva': [
        ('Как ещё называют EVA?',
         'EVA — этиленвинилацетат, ЭВА, СЭВА (сополимер этилена с винилацетатом). Главный параметр марки — содержание винилацетата (VA): '
         'чем оно выше, тем мягче, прозрачнее и клейче материал и ниже температура плавления.'),
        ('Вы продаёте листы и вспененный EVA для обуви?',
         'Нет, мы поставляем гранулы EVA: для литья, экструзии, термоплавких клеев, плёнок, солнечных модулей и вспененных изделий. '
         'Вспененные листы и подошвы делают из гранул с вспенивающей системой на стороне заказчика.'),
        ('Как подобрать марку EVA?',
         'Назовите назначение, нужное содержание VA и показатель текучести расплава (ПТР) — подберём марку из каталога или аналог.'),
    ],
    'evoh': [
        ('Что означает «PE-Xa/EVOH» на трубах?',
         'В трубах из сшитого полиэтилена (PE-Xa, PE-Xb) и PE-RT для отопления и тёплого пола тонкий слой EVOH работает как '
         'кислородный (антидиффузионный) барьер: он ограничивает проникновение кислорода в теплоноситель и снижает коррозию металлических элементов системы. '
         'Допустимая кислородопроницаемость нормируется, например, стандартом DIN 4726.'),
        ('Почему EVOH ставят внутрь многослойной структуры?',
         'Барьерные свойства EVOH ухудшаются при высокой влажности, поэтому слой защищают внешними слоями полиолефина или полиамида; '
         'для адгезии между слоями используют связующие (адгезионные) слои. Подробнее — в разделе про многослойные структуры выше.'),
        ('Где ещё применяют EVOH?',
         'В упаковочных плёнках и пакетах (в том числе для вакуумной упаковки), бутылках и ёмкостях для пищевых продуктов, '
         'топливных баках и медицинской упаковке.'),
    ],
    'ppsu': [
        ('Что такое PPSU?',
         'PPSU — полифенилсульфон. Из него выпускают фитинги для систем из сшитого полиэтилена (тройники, угольники, гильзы), детские бутылочки, '
         'медицинские инструменты и изделия, которые стерилизуют паром.'),
        ('Чем PPSU отличается от PSU и PES?',
         'PPSU — самый ударопрочный и гидролитически стойкий из трёх; PSU и PES жёстче и дешевле. Все три — аморфные '
         'термопласты с высокой теплостойкостью; подбор — по температуре, нагрузке и числу циклов стерилизации.'),
    ],
    'psu': [
        ('Как называют PSU по-русски?',
         'PSU — полисульфон (ПСУ). Применяется для мембран и фильтрующих элементов, медицинских изделий, деталей для горячей воды и электроники.'),
        ('Какую марку PSU выбрать?',
         'Марки различаются вязкостью расплава и формой выпуска (гранулы, порошок). Укажите способ переработки и назначение детали — предложим подходящие марки.'),
    ],
    'pmma': [
        ('Как ещё называют PMMA?',
         'Полиметилметакрилат (PMMA, ПММА) — это оргстекло, акрил, плексиглас.'),
        ('Вы продаёте листовое оргстекло?',
         'Нет. Мы поставляем гранулы PMMA для литья под давлением и экструзии: рассеиватели, световоды, линзы, панели приборов, декоративные детали. '
         'Листовое оргстекло — другая продукция (отливка из мономера или экструзия листа).'),
    ],
    'pc': [
        ('Как называют PC по-русски?',
         'Поликарбонат (ПК, PC). Здесь — гранулы для литья под давлением и экструзии: прозрачные, цветные, огнестойкие, '
         'для оптики и светотехники — марки смотрите в таблицах ниже.'),
        ('Как выбрать гранулы поликарбоната по текучести?',
         'Высокий показатель текучести расплава (ПТР) подходит для тонкостенного литья, низкий — для экструзии листов и профилей. '
         'Назначение и способ переработки напишите в форме запроса — подберём марку.'),
    ],
    'pa12': [
        ('Как ещё называют PA12?',
         'Полиамид 12 — ПА 12, PA12, нейлон 12. Выбирают за низкое водопоглощение, гибкость и стойкость к химикатам; '
         'применяют для трубок (топливных, пневматических), кабельной оболочки и 3D-печати.'),
    ],
    'mlldpe': [
        ('Что такое mLLDPE?',
         'mLLDPE — металлоценовый линейный полиэтилен низкой плотности: полиэтилен, полученный на металлоценовом катализаторе. '
         'Даёт более прочную, прозрачную и легко свариваемую плёнку, чем обычный LLDPE, и используется в упаковочных и стретч-плёнках.'),
    ],
}

POP_CSS = """
/* popular grades + names (tools/build_popular_and_names.py) */
.popular-grades { margin-top: 24px; }
.pg-chips { display: flex; flex-wrap: wrap; gap: 8px; margin: 10px 0 8px; }
.pg-chip { display: inline-block; padding: 6px 12px; border: 1px solid var(--border); border-radius: 18px; background: #f5f8ff; font-size: 13.5px; font-weight: 600; color: #223; text-decoration: none; }
a.pg-chip { color: var(--blue); }
a.pg-chip:hover { background: #e6efff; }
.pg-note { font-size: 12.5px; color: #777; margin: 4px 0 0; }
.prod-card-pop { font-size: 12.5px; color: #555; line-height: 1.6; margin-bottom: 14px; }
.prod-card-pop strong { color: #223; }
.names-faq { margin-top: 28px; }
.glossary-table { width: 100%; border-collapse: collapse; font-size: 14px; }
.glossary-table th, .glossary-table td { border: 1px solid var(--border); padding: 9px 11px; text-align: left; vertical-align: top; }
.glossary-table th { background: #f0f5ff; }
.glossary-table td:first-child { font-weight: 700; white-space: nowrap; }
@media (max-width: 700px) { .glossary-table td:first-child { white-space: normal; } .glossary-table { font-size: 13px; } }
"""

NOTE = {
    'ru': 'Подборка известных на рынке марок из нашего каталога. Полный список — в таблицах ниже; наличие, происхождение и условия поставки подтверждаем по запросу.',
    'en': 'A selection of well-known grades from our catalogue. The full list is in the tables below; availability, origin and delivery terms are confirmed on request.',
}


def popular_block(pid, lang):
    ru = lang == 'ru'
    chips = ''
    for label, page in POPULAR[pid]:
        t = H.escape(label)
        chips += f'<a class="pg-chip" href="{page}">{t}</a>' if page else f'<span class="pg-chip">{t}</span>'
    return ('<!-- popular -->\n      <div class="proddet-body popular-grades" id="popular-grades"><h2>'
            '<i class="fas fa-star" style="margin-right:8px;color:var(--blue);"></i>'
            + ('Популярные марки' if ru else 'Popular grades') + f'</h2><div class="pg-chips">{chips}</div>'
            f'<p class="pg-note">{NOTE[lang]}</p></div>\n      <!-- /popular -->\n')


def names_block(pid):
    items = ''.join(f'<details class="faq-item"><summary>{H.escape(q)}</summary><p>{H.escape(a)}</p></details>' for q, a in NAMES[pid])
    return ('<!-- names -->\n      <div class="proddet-body names-faq"><h2>Названия и частые вопросы</h2>'
            + items + '</div>\n      <!-- /names -->\n')


def strip(s, tag):
    return re.sub(rf'[ \t]*<!-- {tag} -->.*?<!-- /{tag} -->\n?', '', s, flags=re.S)


def process_product(path, pid, lang):
    s = open(path, encoding='utf-8').read()
    s = strip(strip(s, 'popular'), 'names')
    # 1. популярные марки — перед первым телом страницы (описанием)
    anchor = '<div class="proddet-body"'
    i = s.find(anchor)
    assert i > 0, path
    ls = s.rfind('\n', 0, i) + 1
    s = s[:ls] + '      ' + popular_block(pid, lang).lstrip() + s[ls:]
    # 2. названия и вопросы (RU) — перед FAQ или формой запроса
    if lang == 'ru' and pid in NAMES:
        j = next((s.find(a) for a in ('<!-- faq', '<div class="proddet-form"') if a in s), -1)
        assert j > 0, path
        ls = s.rfind('\n', 0, j) + 1
        s = s[:ls] + '      ' + names_block(pid).lstrip() + s[ls:]
    open(path, 'w', encoding='utf-8').write(s)


def process_cards(path, lang):
    s = open(path, encoding='utf-8').read()
    s = re.sub(r'[ \t]*<div class="prod-card-pop">.*?</div>\n', '', s, flags=re.S)
    for pid, items in POPULAR.items():
        names = ', '.join(H.escape(l) for l, _ in items[:3])
        title = 'Популярные марки' if lang == 'ru' else 'Popular grades'
        pat = re.compile(rf'([ \t]*)(<a href="product-{pid}\.html" class="prod-card-btn">)')
        m = pat.search(s)
        if not m:
            print('  нет карточки', pid, path)
            continue
        ins = f'{m.group(1)}<div class="prod-card-pop"><strong>{title}:</strong> {names}</div>\n'
        s = s[:m.start()] + ins + s[m.start():]
    open(path, 'w', encoding='utf-8').write(s)


def add_css():
    p = 'css/style.css'
    s = open(p, encoding='utf-8').read()
    s = re.sub(r'\n/\* popular grades \+ names.*?(?=\n/\* P0 SEO|\Z)', '', s, flags=re.S)
    open(p, 'w', encoding='utf-8').write(s.rstrip('\n') + '\n' + POP_CSS)


GLOSSARY = [
    ('POE', 'Полиолефиновый эластомер', 'Сополимер этилена и α-олефина: модификатор ударной прочности PP, инкапсулянт солнечных модулей, плёнки, кабели.', 'poe'),
    ('POP', 'Полиолефиновый пластомер', 'Металлоценовый пластомер: термосвариваемые слои плёнок и упаковки.', 'pop'),
    ('OBC', 'Олефиновый блок-сополимер', 'Эластичные нетканые материалы, обувь, пены, кабели.', 'obc'),
    ('EVA', 'Этиленвинилацетат, ЭВА, СЭВА', 'Термоплавкие клеи, плёнки, фотомодули, вспененные изделия и подошвы (из гранул).', 'eva'),
    ('EAA', 'Сополимер этилена и акриловой кислоты', 'Адгезионные слои ламинатов, экструзионное покрытие, упаковка.', 'eaa'),
    ('EMAA', 'Сополимер этилена и метакриловой кислоты; иономеры', 'Прозрачная упаковка, термосвариваемые и ударопрочные слои.', 'emaa'),
    ('EVOH', 'Этиленвиниловый спирт (сополимер этилена и винилового спирта)', 'Кислородный барьер в плёнках, упаковке и трубах PE-Xa/EVOH.', 'evoh'),
    ('EPDM', 'Этилен-пропилен-диеновый каучук, СКЭПТ', 'Резинотехнические изделия, кровельные мембраны, модификация пластиков.', 'epdm'),
    ('mLLDPE', 'Металлоценовый линейный полиэтилен низкой плотности', 'Упаковочные и стретч-плёнки с повышенной прочностью.', 'mlldpe'),
    ('XLPE', 'Сшитый полиэтилен для кабельной изоляции', 'Изоляция кабелей среднего и высокого напряжения.', 'xlpe'),
    ('PC', 'Поликарбонат, ПК', 'Литьё и экструзия: оптика, светотехника, корпуса, электротехника.', 'pc'),
    ('PC/ABS', 'Смесь поликарбоната и АБС-пластика', 'Корпуса электроники, автомобильные детали.', 'pcabs'),
    ('PMMA', 'Полиметилметакрилат, оргстекло, акрил', 'Гранулы для светотехники, оптики, дисплеев, декоративных деталей.', 'pmma'),
    ('POM', 'Полиоксиметилен, полиацеталь, полиформальдегид', 'Шестерни, подшипники скольжения, топливная арматура, замки.', 'pom'),
    ('PA66', 'Полиамид 66, ПА 66, нейлон 66', 'Автомобильные и электротехнические детали, конструкционные изделия.', 'pa66'),
    ('PA12', 'Полиамид 12, ПА 12, нейлон 12', 'Трубки, кабельная оболочка, 3D-печать.', 'pa12'),
    ('PA12 эластомер', 'Полиамидный термопластичный эластомер на основе PA12', 'Упругие детали, спортивные изделия, гибкие трубки.', 'pa12e'),
    ('LCP', 'Жидкокристаллический полимер', 'Тонкостенные разъёмы и электронные компоненты.', 'lcp'),
    ('PPSU', 'Полифенилсульфон', 'Фитинги PEX, медицинские изделия, детские бутылочки.', 'ppsu'),
    ('PSU', 'Полисульфон, ПСУ', 'Мембраны, медицинские изделия, детали для горячей воды.', 'psu'),
    ('PES', 'Полиэфирсульфон', 'Мембраны, электроника, медицинские и пищевые изделия.', 'pes'),
]
GLOSSARY_URL = 'https://pldpolymer.com/polymer-names.html'
G_TITLE = 'Полимеры: русские названия и аббревиатуры (POM, PA66, EVA, EVOH…) — SUPULIDE'
G_DESC = 'Справочник: как называют POM, PA66, EVA, EVOH, EPDM, PMMA, PC, PPSU и другие полимеры по-русски. Ссылки на страницы с марками.'


def build_glossary():
    s = open('privacy.html', encoding='utf-8').read()
    t, d = H.escape(G_TITLE, quote=True), H.escape(G_DESC, quote=True)
    s = re.sub(r'<title>.*?</title>', f'<title>{t}</title>', s, count=1)
    s = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{d}">', s, count=1)
    s = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{t}">', s, count=1)
    s = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{d}">', s, count=1)
    s = s.replace('https://pldpolymer.com/privacy.html', GLOSSARY_URL)
    s = re.sub(r'[ \t]*<link rel="alternate" hreflang="en" href="[^"]*">\n', '', s, count=1)
    s = s.replace('/en/privacy.html', '/en/products.html')
    rows = ''.join(
        f'<tr><td>{H.escape(a)}</td><td>{H.escape(n)}</td><td>{H.escape(u)}</td>'
        f'<td><a href="product-{p}.html">Марки {H.escape(a)}</a></td></tr>' for a, n, u, p in GLOSSARY)
    body = ('<section class="contact-info-section" style="padding:60px 0;background:#fff;color:#222;">\n'
            '  <div class="container" style="max-width:980px;line-height:1.7;">\n'
            '    <h1 style="margin-bottom:6px;">Полимеры: русские названия и аббревиатуры</h1>\n'
            '    <p style="opacity:.75;margin-bottom:22px;">Один и тот же материал в российских источниках называют по-разному: по латинской аббревиатуре, '
            'полному названию или торговой марке. Таблица помогает сопоставить названия с нашими страницами марок. '
            'Мы поставляем сырьё (гранулы, каучук, порошок), а не готовые изделия. Цены и документы — по запросу на '
            '<a href="mailto:export@pldpolymer.com">export@pldpolymer.com</a> или через <a href="contact.html">форму</a>.</p>\n'
            '    <div style="overflow-x:auto;"><table class="glossary-table"><thead><tr><th>Обозначение</th><th>Русские названия</th>'
            '<th>Где применяют</th><th>Страница</th></tr></thead><tbody>' + rows + '</tbody></table></div>\n'
            '  </div>\n</section>\n')
    s = re.sub(r'<section class="contact-info-section".*?</section>\n', lambda m: body, s, count=1, flags=re.S)
    open('polymer-names.html', 'w', encoding='utf-8').write(s)


def main():
    for pid in POPULAR:
        for lang, path in (('ru', f'product-{pid}.html'), ('en', f'en/product-{pid}.html')):
            if os.path.exists(path):
                process_product(path, pid, lang)
            else:
                print('нет файла', path)
    # страницы без списка марок, но с блоком «Названия»: нет (все в POPULAR)
    process_cards('products.html', 'ru')
    process_cards('en/products.html', 'en')
    add_css()
    build_glossary()
    print('ok')


if __name__ == '__main__':
    main()
