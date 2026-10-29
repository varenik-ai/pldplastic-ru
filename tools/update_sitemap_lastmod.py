#!/usr/bin/env python3
"""Проставляет в sitemap.xml реальные <lastmod>: дата последнего коммита файла (или сегодня, если файл изменён и не закоммичен)."""
import datetime
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
SITE = 'https://pldpolymer.com/'
today = datetime.date.today().isoformat()
dirty = {l[3:].strip().strip('"') for l in subprocess.check_output(['git', 'status', '--porcelain']).decode().splitlines()}


def file_for(loc):
    rel = loc[len(SITE):]
    if rel == '':
        return 'index.html'
    if rel == 'en/':
        return 'en/index.html'
    return rel


def last_date(path):
    if not os.path.exists(path):
        return None
    if path in dirty:
        return today
    d = subprocess.check_output(['git', 'log', '-1', '--format=%cs', '--', path]).decode().strip()
    return d or None


sm = open('sitemap.xml', encoding='utf-8').read()
changed = 0


def fix(m):
    global changed
    loc = m.group(1)
    d = last_date(file_for(loc))
    if not d or d == m.group(2):
        return m.group(0)
    changed += 1
    return f'<loc>{loc}</loc><lastmod>{d}</lastmod>'


sm = re.sub(r'<loc>([^<]+)</loc><lastmod>([^<]+)</lastmod>', fix, sm)
open('sitemap.xml', 'w', encoding='utf-8').write(sm)
print('lastmod обновлён у', changed, 'URL')
