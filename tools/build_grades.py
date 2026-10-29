#!/usr/bin/env python3
"""Достаёт таблицы марок из страниц продуктов (RU и EN) в data/grades.{ru,en}.json для страницы «Подбор марки».

Запуск из корня репозитория:  python3 tools/build_grades.py
Источник — сами HTML-таблицы сайта (колонки «Торговая марка» / «Марка» и далее свойства).
"""
import glob
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRAND_HDR = re.compile(r'^(торговая марка|trade ?name|brand|trademark)', re.I)
GRADE_HDR = re.compile(r'^(марка|grade)', re.I)


def clean(x):
    x = re.sub(r'<[^>]+>', ' ', x)
    return re.sub(r'\s+', ' ', html.unescape(x)).strip()


def num(v):
    m = re.fullmatch(r'[<>≈~]?\s*(-?\d+(?:[.,]\d+)?)', v.replace(' ', '').strip())
    return float(m.group(1).replace(',', '.')) if m else None


def parse(path):
    s = open(path, encoding='utf-8').read()
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S)
    name = clean(h1.group(1)) if h1 else os.path.basename(path)
    grades = []
    for t in re.findall(r'<table.*?</table>', s, re.S):
        rows = re.findall(r'<tr.*?</tr>', t, re.S)
        if len(rows) < 2:
            continue
        hdr = [clean(c) for c in re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>', rows[0], re.S)]
        hdr = [h for h in hdr if h]
        if len(hdr) < 3 or not BRAND_HDR.match(hdr[0]) or not GRADE_HDR.match(hdr[1]):
            continue
        for r in rows[1:]:
            cells = [clean(c) for c in re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>', r, re.S)]
            cells = [c for c in cells] if len(cells) == len(hdr) else [c for c in cells if c != '']
            if len(cells) != len(hdr):
                continue
            props = {hdr[i]: cells[i] for i in range(2, len(hdr))}
            grades.append({
                'brand': cells[0], 'grade': cells[1], 'props': props,
                'num': {k: num(v) for k, v in props.items()},
            })
    return name, grades


def build(lang, pattern, url_prefix):
    products = []
    for path in sorted(glob.glob(os.path.join(ROOT, pattern))):
        slug = os.path.basename(path)[len('product-'):-len('.html')]
        name, grades = parse(path)
        name = {'pcabs': 'PC/ABS'}.get(slug, slug.upper())
        if grades:
            products.append({'id': slug, 'name': name, 'url': url_prefix + os.path.basename(path), 'grades': grades})
    out = os.path.join(ROOT, 'data', f'grades.{lang}.json')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w', encoding='utf-8') as f:
        json.dump({'products': products}, f, ensure_ascii=False, separators=(',', ':'))
    total = sum(len(p['grades']) for p in products)
    print(lang, len(products), 'products,', total, 'grades ->', os.path.relpath(out, ROOT))
    return products


if __name__ == '__main__':
    build('ru', 'product-*.html', '')
    build('en', 'en/product-*.html', '')
