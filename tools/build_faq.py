#!/usr/bin/env python3
"""Блок «Вопросы и ответы» (с разметкой FAQPage) на страницах основных категорий, RU и EN.

Ответы собираются только из того, что уже есть на сайте: описание применения со страницы «Применение»/мета-описаний
и диапазоны показателей, посчитанные по таблицам марок (data/grades.*.json). Вопросы повторяют реальные запросы из
Google Search Console («evoh density», «what is poe material», …). Запуск из корня: python3 tools/build_faq.py
(после tools/build_grades.py). Повторный запуск заменяет блок.
"""
import html as H
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

DEF = {
    'evoh': ('EVOH — этилен-виниловый спирт, барьерный полимер с высокой защитой от кислорода: применяется в многослойных плёнках для пищевой и медицинской упаковки, топливных баках и трубах.',
             'EVOH (ethylene vinyl alcohol copolymer) is a barrier polymer with a high oxygen barrier, used in multilayer films for food and medical packaging, fuel tanks and pipes.'),
    'poe': ('POE — полиолефиновый эластомер: сополимер этилена с α-олефином (в таблице марок указан сомономер C4 или C8). Применяется для инкапсуляции фотоэлектрических модулей, модификации PP, в кабелях и автомобильных деталях.',
            'POE (polyolefin elastomer) is a copolymer of ethylene and an α-olefin (the grade table shows a C4 or C8 comonomer). It is used for solar module encapsulation, PP modification, cables and automotive parts.'),
    'obc': ('OBC — блок-сополимер олефинов: сочетает термостойкость и эластичность; применяется в обуви, пенах, кабелях и уплотнителях.',
            'OBC (olefin block copolymer) combines heat resistance and elasticity; it is used in footwear, foam, cables and seals.'),
    'pa66': ('PA66 (полиамид 66, нейлон 66) — конструкционный полиамид с температурой плавления 262 °C для автомобильных и электротехнических деталей.',
             'PA66 (polyamide 66, nylon 66) is an engineering polyamide with a melting point of 262 °C for automotive and electrical parts.'),
    'eaa': ('EAA — сополимер этилена и акриловой кислоты: адгезия к металлам и полиамиду, применяется в ламинатах, экструзионном покрытии и упаковочной плёнке.',
            'EAA (ethylene acrylic acid copolymer) gives adhesion to metals and polyamide and is used in laminates, extrusion coating and packaging film.'),
    'xlpe': ('XLPE — сшитый полиэтилен для изоляции кабелей высокого и среднего напряжения и проводов.',
             'XLPE (cross-linked polyethylene) is used for HV/MV cable insulation and wire.'),
}
NAME = {'evoh': 'EVOH', 'poe': 'POE', 'obc': 'OBC', 'pa66': 'PA66', 'eaa': 'EAA', 'xlpe': 'XLPE'}
KEYS = [('density', re.compile(r'плотност|density', re.I), ('плотность', 'density'), 'г/см³ / g/cm³'),
        ('mfr', re.compile(r'птр|mfr', re.I), ('показатель текучести расплава (ПТР)', 'melt flow rate (MFR)'), 'г/10 мин / g/10 min'),
        ('shore', re.compile(r'shore|шор', re.I), ('твёрдость по Шору', 'Shore hardness'), '')]


def fmt(v, lang):
    s = f'{v:g}'
    return s.replace('.', ',') if lang == 'ru' else s


def stats(prod, lang):
    out = []
    for key, rx, names, unit in KEYS:
        labels = [k for k in prod['grades'][0]['props'] if rx.search(k)]
        if not labels:
            continue
        lab = labels[0]
        vals = [g['num'][lab] for g in prod['grades'] if g['num'].get(lab) is not None]
        if len(vals) < 3:
            continue
        u = unit.split(' / ')[0 if lang == 'ru' else 1] if unit else ''
        out.append((key, f'{names[0 if lang == "ru" else 1]}: {fmt(min(vals), lang)}–{fmt(max(vals), lang)}' + (f' {u}' if u else '')))
    return out


def qa(pid, lang, prod):
    ru = lang == 'ru'
    n = NAME[pid]
    items = []
    items.append((f'Что такое {n}?' if ru else f'What is {n}?', DEF[pid][0 if ru else 1]))
    if prod:
        st = stats(prod, lang)
        if st:
            cnt = len(prod['grades'])
            a = (f'В каталоге {cnt} марок {n}. Диапазоны по таблице: ' if ru else f'The catalogue lists {cnt} {n} grades. Ranges in the table: ') + '; '.join(t for _, t in st) + '. ' \
                + ('Точные значения для каждой марки — в таблице выше и на страницах марок.' if ru else 'Exact values for each grade are in the table above and on the grade pages.')
            ks = {k for k, _ in st}
            qru = {'density': 'плотность', 'mfr': 'ПТР', 'shore': 'твёрдость'}
            qen = {'density': 'density', 'mfr': 'melt flow', 'shore': 'hardness'}
            order = [k for k in ('density', 'mfr', 'shore') if k in ks]
            names_ru = ' и '.join([', '.join(qru[k] for k in order[:-1])] + [qru[order[-1]]]) if len(order) > 1 else qru[order[0]]
            names_en = ' and '.join([', '.join(qen[k] for k in order[:-1])] + [qen[order[-1]]]) if len(order) > 1 else qen[order[0]]
            items.append((f'Какие {names_ru} у {n}?' if ru else (f'What is the {names_en} of {n}?' if len(order) == 1 else f'What are the {names_en} of {n}?'), a))
    items.append((f'Как получить цену и техническое описание {n}?' if ru else f'How do I get a price and datasheet for {n}?',
                  ('Цена и наличие — по запросу: отправьте форму на странице или напишите на export@pldpolymer.com. Предоставляем TDS, MSDS и образцы для испытаний; условия поставки EXW, FOB, CIF.' if ru else
                   'Price and availability are given on request: use the form on this page or write to export@pldpolymer.com. We provide TDS, MSDS and test samples; delivery terms EXW, FOB, CIF.')))
    return items


def build():
    data = {l: {p['id']: p for p in json.load(open(f'data/grades.{l}.json', encoding='utf-8'))['products']} for l in ('ru', 'en')}
    done = 0
    for lang, pre in (('ru', ''), ('en', 'en/')):
        for pid in NAME:
            path = f'{pre}product-{pid}.html'
            s = open(path, encoding='utf-8').read()
            items = qa(pid, lang, data[lang].get(pid))
            ru = lang == 'ru'
            body = ''.join(f'<details class="faq-item"><summary>{H.escape(q)}</summary><p>{H.escape(a)}</p></details>' for q, a in items)
            sec = ('<!-- faq -->\n      <div class="proddet-body faq-block"><h2>' + ('Вопросы и ответы' if ru else 'Questions and answers')
                   + f'</h2>{body}</div>\n      <!-- /faq -->\n')
            s = re.sub(r'<!-- faq -->.*?<!-- /faq -->\n?', '', s, flags=re.S)
            s = re.sub(r'<script type="application/ld\+json" id="faq-ld">.*?</script>\n?', '', s, flags=re.S)
            anchor = next((a for a in ('<!-- RELATED PRODUCTS -->', '<div class="proddet-related"', '<!-- CONTACT FORM -->') if a in s), None)
            if not anchor:
                print('нет места вставки:', path)
                continue
            i = s.index(anchor)
            s = s[:i] + sec + '      ' + s[i:]
            ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}
            s = s.replace('</head>', '<script type="application/ld+json" id="faq-ld">' + json.dumps(ld, ensure_ascii=False) + '</script>\n</head>', 1)
            open(path, 'w', encoding='utf-8').write(s)
            done += 1
    print('страниц с FAQ:', done)


if __name__ == '__main__':
    build()
