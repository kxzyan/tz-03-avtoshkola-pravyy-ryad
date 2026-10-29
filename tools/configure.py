#!/usr/bin/env python3
"""Подставляет в сайт настоящие идентификаторы — один раз, когда они появятся.

  python3 tools/configure.py --ga G-ABC123XYZ
  python3 tools/configure.py --app https://script.google.com/macros/s/AKfy.../exec
  python3 tools/configure.py --site https://moy-sayt.vercel.app

--ga    идентификатор потока GA4 → тег gtag.js в <head> всех 9 страниц
--app   URL веб-приложения Apps Script → js/form.js
--site  адрес на Vercel → og:image/og:url всех страниц, затем пересоздать реестр, QR и афишу:
        SITE=<адрес> python3 tools/make_files.py
"""
import argparse, glob, re

PAGES = sorted(glob.glob('*.html'))


def sub_files(files, pattern, repl):
    n = 0
    for f in files:
        s = open(f, encoding='utf-8').read()
        s2, k = re.subn(pattern, repl, s)
        if k:
            open(f, 'w', encoding='utf-8').write(s2)
            n += k
    return n


ap = argparse.ArgumentParser()
ap.add_argument('--ga'); ap.add_argument('--app'); ap.add_argument('--site')
a = ap.parse_args()

if a.ga:
    assert re.fullmatch(r'G-[A-Z0-9]{6,12}', a.ga), 'идентификатор вида G-XXXXXXXXXX'
    print('GA4:', sub_files(PAGES, r'G-[A-Z0-9]{6,12}', a.ga), 'замен в', len(PAGES), 'страницах')
if a.app:
    assert a.app.startswith('https://script.google.com/macros/s/') and a.app.endswith('/exec'), 'URL должен оканчиваться на /exec'
    print('Apps Script:', sub_files(['js/form.js'], r"var APP_URL = '[^']*';", f"var APP_URL = '{a.app}';"), 'замена')
if a.site:
    site = a.site.rstrip('/')
    assert re.fullmatch(r'https://[a-z0-9-]+\.vercel\.app', site), 'адрес вида https://<имя>.vercel.app'
    print('Сайт:', sub_files(PAGES, r'https://[a-z0-9-]+\.vercel\.app', site), 'замен; README.md поправьте вручную')
    print('Теперь выполните: SITE=' + site + ' python3 tools/make_files.py')
