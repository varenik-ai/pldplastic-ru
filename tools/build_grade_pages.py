#!/usr/bin/env python3
"""Страницы отдельных марок (RU и EN) из data/grades.{ru,en}.json + ссылки на них из таблиц страниц продуктов.

Страницы нужны под запросы по точному названию марки (по данным Яндекс Вебмастера люди ищут «ev3251f», «evoh ew-3201s»,
«pom gm-90», «clarnate a1105» и т.д.). Набор марок — FEATURED ниже: добавляйте строки по реальным запросам.
Сначала: python3 tools/build_grades.py. Запуск из корня:  python3 tools/build_grade_pages.py
"""
import html as H
import json
import math
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
SITE = 'https://pldpolymer.com/'
TODAY = '2026-10-29'

# (id продукта, марка, фрагмент торговой марки)
FEATURED = [
    ('evoh', 'EV3251F', 'EVASIS'),
    ('evoh', 'EW-3201S', 'Sinopec'),
    ('poe', 'LC565', 'LUCENE'),
    ('poe', 'LC670', 'LUCENE'),
    ('pom', 'GM90', 'Yuntianhua'),
    ('pom', 'F20-03', 'KEPITAL'),
    ('pc', 'A1105', 'Clarnate'),
    ('pc', 'HL6157', 'Clarnate'),
    ('pc', 'A1227', 'Clarnate'),
    ('eva', 'UE4055', 'EVASINE'),
    ('poe', '5101', 'EXACT'),
    ('pes', 'Ultrason® E PES 2010', 'BASF'),
]
CAT = {
    'evoh': ('EVOH (этилен-винилспиртовый сополимер)', 'EVOH (ethylene-vinyl alcohol copolymer)',
             'Барьерный слой многослойных плёнок для пищевой и медицинской упаковки: EVOH даёт кислородный барьер.',
             'Barrier layer for multilayer food and medical packaging films: EVOH provides the oxygen barrier.'),
    'poe': ('POE (полиолефиновый эластомер)', 'POE (polyolefin elastomer)',
            'Применяется для инкапсуляции фотоэлектрических модулей, в автомобилестроении и в обувной промышленности.',
            'Used for photovoltaic module encapsulation, in automotive parts and in footwear.'),
    'pom': ('POM (полиоксиметилен, полиацеталь)', 'POM (polyoxymethylene, acetal)', '', ''),
    'pc': ('PC (поликарбонат)', 'PC (polycarbonate)',
           'Применяется для корпусов электроники, LED-линз и деталей высокоточного литья.',
           'Used for electronics housings, LED lenses and precision injection-moulded parts.'),
    'pes': ('PES (полиэфирсульфон)', 'PES (polyethersulfone)', '', ''),
    'eva': ('EVA (сополимер этилена и винилацетата)', 'EVA (ethylene-vinyl acetate copolymer)',
            'Применяется для инкапсуляции фотоэлектрических модулей и в обувной промышленности.',
            'Used for photovoltaic module encapsulation and in footwear.'),
}
# Дополнительные сведения по марке из открытых паспортов производителей (ru, en)
NOTES = {
    ('poe', '5101'): (
        'Этилен-октеновый пластомер ExxonMobil на металлоценовом катализаторе для моно- и многослойной выдувной плёнки: низкая температура запечатывания, высокая прочность и ударная вязкость, низкий модуль, мало экстрактов в гексане. Температура размягчения по Вика 76,6 °C, пик плавления 92 °C (паспорт ExxonMobil от 12.08.2022).',
        'ExxonMobil ethylene-octene plastomer made with metallocene technology for mono- and multilayer blown film: low sealing temperature, high toughness and impact strength, low modulus, low hexane extractables. Vicat softening temperature 76.6 °C, peak melting temperature 92 °C (ExxonMobil datasheet, 12/08/2022).'),
    ('pes', 'Ultrason® E PES 2010'): (
        'Ненаполненный полиэфирсульфон BASF средней вязкости для литья под давлением. По данным BASF: плотность 1370 кг/м³ (ISO 1183), показатель текучести расплава MVR 70 см³/10 мин (360 °C, 10 кг, ISO 1133), температура расплава 340–390 °C, температура формы 140–180 °C, сушка 4 ч при 140 °C, усадка при литье 0,82 % вдоль и 0,86 % поперёк (паспорт BASF, 09/2026).',
        'Unreinforced, medium-viscosity BASF polyethersulfone for injection moulding. Per BASF: density 1370 kg/m³ (ISO 1183), melt volume rate MVR 70 cm³/10 min (360 °C, 10 kg, ISO 1133), melt temperature 340–390 °C, mould temperature 140–180 °C, drying 4 h at 140 °C, moulding shrinkage 0.82 % parallel and 0.86 % normal (BASF processing data sheet, 09/2026).'),
}
T = {
    'ru': dict(h1sub='Характеристики марки и запрос цены', props='Показатели по каталогу', similar='Похожие марки',
               req='Запросить цену', brand='Торговая марка', grade='Марка', all='Все марки', sel='Подобрать по параметрам',
               title='{b} {g} — {c}, характеристики и цена | SUPULIDE',
               desc='{b} {g}: {p}. Цена и наличие по запросу, образцы и TDS. Поставка из Китая.',
               intro='Марка {g} ({b}) — {c}. Показатели по каталогу: {p}.',
               tail='Цену, наличие и условия поставки (EXW, FOB, CIF) уточняйте по запросу; по запросу предоставляем TDS, MSDS и образцы для испытаний.',
               home='Главная', prods='Продукты', sidx=0),
    'en': dict(h1sub='Grade properties and price request', props='Catalogue properties', similar='Similar grades',
               req='Request price', brand='Trade name', grade='Grade', all='All grades', sel='Find by properties',
               title='{b} {g} — {c}, properties and price | SUPULIDE',
               desc='{b} {g}: {p}. Price and availability on request, samples and TDS. Supplied from China.',
               intro='Grade {g} ({b}) is {c}. Catalogue properties: {p}.',
               tail='Price, availability and delivery terms (EXW, FOB, CIF) are given on request; we provide TDS, MSDS and test samples on request.',
               home='Home', prods='Products', sidx=1),
}


def slug(brand, grade):
    b = re.sub(r'[^a-z0-9]+', '-', re.sub(r'[™®]', '', brand).lower()).strip('-')
    g = re.sub(r'[^a-z0-9]+', '-', grade.lower()).strip('-')
    return f'grade-{b}-{g}'


def load():
    out = {}
    for lang in ('ru', 'en'):
        d = json.load(open(f'data/grades.{lang}.json', encoding='utf-8'))
        out[lang] = {p['id']: p for p in d['products']}
    return out


def similar(prod, idx, n=6):
    g0 = prod['grades'][idx]
    keys = [k for k, v in g0['num'].items() if v is not None]
    if not keys:
        return []
    spans = {}
    for k in keys:
        vals = [g['num'][k] for g in prod['grades'] if g['num'].get(k) is not None]
        spans[k] = (max(vals) - min(vals)) or 1
    sc = []
    for i, g in enumerate(prod['grades']):
        if i == idx:
            continue
        d, c = 0.0, 0
        for k in keys:
            v = g['num'].get(k)
            if v is not None:
                d += ((v - g0['num'][k]) / spans[k]) ** 2
                c += 1
        if c:
            sc.append((math.sqrt(d / c), i))
    sc.sort()
    return [i for _, i in sc[:n]]


def table(g, cols):
    rows = ''.join(f'<tr><th>{H.escape(k)}</th><td>{H.escape(g["props"][k])}</td></tr>' for k in cols)
    return f'<table class="grade-table"><tbody>{rows}</tbody></table>'


def main_html(lang, pid, prod, idx, feat_slugs):
    t = T[lang]
    g = prod['grades'][idx]
    cat = CAT[pid][t['sidx']]
    app = '' if (pid, g['grade']) in NOTES else CAT[pid][2 + t['sidx']]
    note = NOTES.get((pid, g['grade']))
    note_html = f'<p>{H.escape(note[t["sidx"]])}</p>' if note else ''
    cols = list(g['props'].keys())
    ptxt = '; '.join(f'{k}: {g["props"][k]}' for k in cols if g['props'][k] not in ('—', ''))
    brand, grade = g['brand'], g['grade']
    q = f'contact.html?product={H.escape(prod["name"])}&amp;grade={H.escape((brand + " " + grade).replace(" ", "%20"))}#contact-form'
    sim = similar(prod, idx)
    srows = ''
    for i in sim:
        s = prod['grades'][i]
        name = f'{H.escape(s["brand"])} <b>{H.escape(s["grade"])}</b>'
        key = (pid, s['grade'], s['brand'])
        if key in feat_slugs[lang]:
            name = f'<a href="{feat_slugs[lang][key]}.html">{name}</a>'
        srows += '<tr><td>' + name + '</td>' + ''.join(f'<td>{H.escape(s["props"].get(k, "—"))}</td>' for k in cols) + '</tr>'
    sim_html = ''
    if srows:
        sim_html = (f'<h2>{t["similar"]}</h2><div class="sel-scroll"><table class="sel-table"><thead><tr><th>{t["brand"]} / {t["grade"]}</th>'
                    + ''.join(f'<th>{H.escape(k)}</th>' for k in cols) + f'</tr></thead><tbody>{srows}</tbody></table></div>')
    sel = f'selector.html?p={pid}'
    prodpage = f'product-{pid}.html'
    intro = t['intro'].format(g=H.escape(grade), b=H.escape(brand), c=H.escape(cat), p=H.escape(ptxt))
    return f'''<section class="selector-section grade-section">
  <div class="container">
    <div class="grade-card">
      <p class="grade-lead">{intro} {H.escape(app)}</p>
      {note_html}
      <h2>{t["props"]}</h2>
      {table(g, cols)}
      <p>{H.escape(t["tail"])}</p>
      <a class="sel-btn grade-cta" href="{q}">{t["req"]}</a>
      <p class="grade-links"><a href="{prodpage}">{t["all"]} {H.escape(prod["name"])}</a> · <a href="{sel}">{t["sel"]}</a></p>
    </div>
    {sim_html}
  </div>
</section>'''


def shell(src, dst, cfg):
    s = open(src, encoding='utf-8').read()

    def sub(pat, rep, optional=False):
        nonlocal s
        s2, n = re.subn(pat, lambda m: rep, s, count=1, flags=re.S)
        assert n or optional, pat
        s = s2
    e = H.escape
    sub(r'<title>.*?</title>', f'<title>{e(cfg["title"])}</title>')
    sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{e(cfg["desc"])}">')
    sub(r'<meta name="keywords" content="[^"]*">', f'<meta name="keywords" content="{e(cfg["kw"])}">', True)
    sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{cfg["url"]}">')
    sub(r'<link rel="alternate" hreflang="ru" href="[^"]*">', f'<link rel="alternate" hreflang="ru" href="{cfg["ru"]}">')
    sub(r'<link rel="alternate" hreflang="en" href="[^"]*">', f'<link rel="alternate" hreflang="en" href="{cfg["en"]}">')
    sub(r'<link rel="alternate" hreflang="x-default" href="[^"]*">', f'<link rel="alternate" hreflang="x-default" href="{cfg["ru"]}">', True)
    sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{e(cfg["title"])}">', True)
    sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{e(cfg["desc"])}">', True)
    sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{cfg["url"]}">', True)
    sub(r'<h1 class="contact-hero-title">.*?</h1>', f'<h1 class="contact-hero-title">{e(cfg["h1"])}</h1>')
    sub(r'<p class="contact-hero-sub">.*?</p>', f'<p class="contact-hero-sub">{e(cfg["sub"])}</p>')
    # хлебные крошки в JSON-LD
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": cfg['crumb'][0], "item": SITE + ('en/' if cfg['lang'] == 'en' else '')},
        {"@type": "ListItem", "position": 2, "name": cfg['crumb'][1], "item": cfg['crumb'][2]},
        {"@type": "ListItem", "position": 3, "name": cfg['h1'], "item": cfg['url']}]}
    ld = '<script type="application/ld+json">' + json.dumps(crumbs, ensure_ascii=False) + '</script>\n'
    s = s.replace('</head>', ld + '</head>', 1)
    a = s.index('<!-- INFO SECTION -->')
    b = s.index('<footer class="main-footer"')
    s = s[:a] + cfg['main'] + '\n\n' + s[b:]
    s = re.sub(r'(<li><a href="contact.html")\s+class="active"', r'\1', s)
    open(dst, 'w', encoding='utf-8').write(s)


def main():
    data = load()
    feat = {'ru': {}, 'en': {}}
    plan = []
    for pid, grade, bfrag in FEATURED:
        prod = data['ru'][pid]
        idx = next(i for i, g in enumerate(prod['grades']) if g['grade'] == grade and bfrag.lower() in g['brand'].lower())
        g = prod['grades'][idx]
        sl = slug(g['brand'], g['grade'])
        feat['ru'][(pid, g['grade'], g['brand'])] = sl
        ge = data['en'][pid]['grades'][idx]
        feat['en'][(pid, ge['grade'], ge['brand'])] = sl
        plan.append((pid, idx, sl))
    for pid, idx, sl in plan:
        for lang, src in (('ru', 'contact.html'), ('en', 'en/contact.html')):
            prod = data[lang][pid]
            g = prod['grades'][idx]
            t = T[lang]
            cat = CAT[pid][t['sidx']]
            ptxt = '; '.join(f'{k}: {v}' for k, v in g['props'].items() if v not in ('—', ''))
            pre = 'en/' if lang == 'en' else ''
            cfg = dict(
                lang=lang, title=t['title'].format(b=g['brand'], g=g['grade'], c=cat),
                desc=t['desc'].format(b=g['brand'], g=g['grade'], p=ptxt)[:300],
                kw=f'{g["grade"]}, {g["brand"]} {g["grade"]}, {prod["name"]}',
                url=f'{SITE}{pre}{sl}.html', ru=f'{SITE}{sl}.html', en=f'{SITE}en/{sl}.html',
                h1=f'{g["brand"]} {g["grade"]}', sub=f'{t["h1sub"]}',
                crumb=(t['home'], t['prods'], f'{SITE}{pre}products.html'),
                main=main_html(lang, pid, prod, idx, feat))
            shell(src, f'{pre}{sl}.html', cfg)
    # ссылки из таблиц страниц продуктов
    linked = 0
    for lang, pre in (('ru', ''), ('en', 'en/')):
        for pid in {p for p, _, _ in plan}:
            path = f'{pre}product-{pid}.html'
            s = open(path, encoding='utf-8').read()
            for key, sl in feat[lang].items():
                if key[0] != pid:
                    continue
                _, grade, brand = key
                if pid == 'pes':
                    raw = re.escape(grade).replace('®', '<sup>®</sup>').replace(r'\ ', ' ')
                    pat = re.compile(r'(<td>)(' + raw + r')(</td>)')
                    if f'href="{sl}.html"' in s:
                        continue
                    s, n = pat.subn(lambda m: m.group(1) + f'<a href="{sl}.html">' + m.group(2) + '</a>' + m.group(3), s, count=1)
                    linked += n
                    if not n:
                        print('нет ссылки в таблице:', path, key)
                    continue
                pat = re.compile(r'(<tr[^>]*>(?:(?!</tr>).)*?>\s*' + re.escape(brand) + r'\s*</t[dh]>\s*<td[^>]*>)(\s*' + re.escape(grade) + r'\s*)(</td>)', re.S)
                if f'href="{sl}.html"' in s:
                    continue
                s, n = pat.subn(lambda m: m.group(1) + f'<a href="{sl}.html">' + m.group(2).strip() + '</a>' + m.group(3), s, count=1)
                linked += n
                if not n:
                    print('нет ссылки в таблице:', path, key)
            open(path, 'w', encoding='utf-8').write(s)
    # sitemap
    sm = open('sitemap.xml', encoding='utf-8').read()
    add = ''
    for pid, idx, sl in plan:
        if f'/{sl}.html' in sm:
            continue
        add += (f'  <url><loc>{SITE}{sl}.html</loc><lastmod>{TODAY}</lastmod><changefreq>monthly</changefreq><priority>0.6</priority>'
                f'<xhtml:link rel="alternate" hreflang="ru" href="{SITE}{sl}.html"/><xhtml:link rel="alternate" hreflang="en" href="{SITE}en/{sl}.html"/>'
                f'<xhtml:link rel="alternate" hreflang="x-default" href="{SITE}{sl}.html"/></url>\n'
                f'  <url><loc>{SITE}en/{sl}.html</loc><lastmod>{TODAY}</lastmod><changefreq>monthly</changefreq><priority>0.6</priority>'
                f'<xhtml:link rel="alternate" hreflang="ru" href="{SITE}{sl}.html"/><xhtml:link rel="alternate" hreflang="en" href="{SITE}en/{sl}.html"/>'
                f'<xhtml:link rel="alternate" hreflang="x-default" href="{SITE}{sl}.html"/></url>\n')
    if add:
        sm = sm.replace('</urlset>', add + '</urlset>')
        open('sitemap.xml', 'w', encoding='utf-8').write(sm)
    print('страниц:', len(plan) * 2, 'ссылок в таблицах:', linked)


if __name__ == '__main__':
    main()
