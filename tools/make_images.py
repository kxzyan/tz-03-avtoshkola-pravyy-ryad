#!/usr/bin/env python3
"""Рисует иллюстрации сайта в фирменных цветах (Pillow): img/*.webp и img/og.jpg.
Фотографии и картинки из экзаменационных билетов не используются.
Запуск из корня репозитория: python3 tools/make_images.py"""
from PIL import Image, ImageDraw, ImageFont
import os

B, Y, D, G, W = '#1F6FD1', '#F5C518', '#1E2329', '#f2f4f7', '#ffffff'
FONT = '/usr/share/fonts/opentype/inter/Inter-Bold.otf'
FONT_R = '/usr/share/fonts/opentype/inter/Inter-Regular.otf'
OUT = 'img'


def font(size, bold=True):
    try:
        return ImageFont.truetype(FONT if bold else FONT_R, size)
    except OSError:
        return ImageFont.load_default()


def road(d, w, h, top):
    d.rectangle([0, top, w, h], fill='#3a414a')
    for x in range(0, w, 120):
        d.rectangle([x + 20, top + (h - top) // 2 - 6, x + 80, top + (h - top) // 2 + 6], fill=Y)


def car(d, x, y, s, body=W, text=None):
    """Простой учебный автомобиль, вид сбоку. x,y — левый нижний угол кузова, s — масштаб."""
    d.rounded_rectangle([x, y - 60 * s, x + 300 * s, y], radius=int(18 * s), fill=body, outline=D, width=max(2, int(4 * s)))
    d.polygon([(x + 70 * s, y - 60 * s), (x + 110 * s, y - 110 * s), (x + 210 * s, y - 110 * s), (x + 250 * s, y - 60 * s)],
              fill=body, outline=D)
    d.polygon([(x + 90 * s, y - 62 * s), (x + 118 * s, y - 100 * s), (x + 155 * s, y - 100 * s), (x + 155 * s, y - 62 * s)], fill='#bcd6f5')
    d.polygon([(x + 165 * s, y - 62 * s), (x + 165 * s, y - 100 * s), (x + 205 * s, y - 100 * s), (x + 235 * s, y - 62 * s)], fill='#bcd6f5')
    # табличка «У» учебного автомобиля
    d.polygon([(x + 140 * s, y - 112 * s), (x + 180 * s, y - 112 * s), (x + 160 * s, y - 140 * s)], fill=W, outline='#c0392b', width=max(2, int(4 * s)))
    d.text((x + 160 * s, y - 120 * s), 'У', fill=D, font=font(int(18 * s)), anchor='mm')
    for cx in (x + 70 * s, x + 230 * s):
        d.ellipse([cx - 32 * s, y - 32 * s, cx + 32 * s, y + 32 * s], fill=D)
        d.ellipse([cx - 13 * s, y - 13 * s, cx + 13 * s, y + 13 * s], fill='#9aa3ad')
    d.rectangle([x + 280 * s, y - 45 * s, x + 298 * s, y - 32 * s], fill=Y)
    if text:
        d.text((x + 150 * s, y - 32 * s), text, fill=D, font=font(int(22 * s)), anchor='mm')


def moto(d, x, y, s):
    for cx in (x, x + 170 * s):
        d.ellipse([cx - 45 * s, y - 45 * s, cx + 45 * s, y + 45 * s], outline=D, width=int(12 * s))
    d.line([(x, y), (x + 70 * s, y - 70 * s), (x + 140 * s, y - 70 * s), (x + 170 * s, y)], fill=B, width=int(14 * s))
    d.rounded_rectangle([x + 50 * s, y - 100 * s, x + 130 * s, y - 70 * s], radius=int(10 * s), fill=B)
    d.line([(x + 140 * s, y - 70 * s), (x + 150 * s, y - 120 * s)], fill=D, width=int(10 * s))


def cones(d, xs, y, s=1):
    for x in xs:
        d.polygon([(x, y - 50 * s), (x - 18 * s, y), (x + 18 * s, y)], fill='#f08c00')
        d.rectangle([x - 11 * s, y - 28 * s, x + 11 * s, y - 20 * s], fill=W)


def save(img, name, q=78):
    path = os.path.join(OUT, name)
    if name.endswith('.webp'):
        img.save(path, 'WEBP', quality=q, method=6)
    else:
        img.convert('RGB').save(path, 'JPEG', quality=q, optimize=True, progressive=True)
    print(name, img.size, os.path.getsize(path) // 1024, 'КБ')


def hero():
    w, h = 1120, 800
    im = Image.new('RGB', (w, h), '#cfe2f8'); d = ImageDraw.Draw(im)
    d.ellipse([820, 60, 980, 220], fill=Y)
    d.rectangle([0, 470, w, h], fill='#7fb069')
    road(d, w, h, 560)
    cones(d, [140, 300, 820, 980], 560, 1.4)
    car(d, 260, 700, 2.0)
    save(im, 'hero.webp')


def og():
    w, h = 1200, 630
    im = Image.new('RGB', (w, h), B); d = ImageDraw.Draw(im)
    d.rectangle([0, 470, w, h], fill='#3a414a')
    for x in range(0, w, 120):
        d.rectangle([x + 20, 544, x + 80, 556], fill=Y)
    d.text((60, 60), 'ПРАВЫЙ РЯД', fill=Y, font=font(64))
    d.text((60, 150), 'автошкола категорий A и B', fill=W, font=font(36, False))
    d.text((60, 240), 'Студентам — скидка 15 %', fill=W, font=font(58))
    d.text((60, 315), 'до 30 ноября 2026 · рассрочка без переплаты', fill=W, font=font(32, False))
    car(d, 760, 520, 1.3)
    save(im, 'og.jpg', 82)


def instructor(name, kind, label):
    w, h = 800, 600
    bg = {'manual': '#dbe8f8', 'auto': '#dcf0e4', 'moto': '#e4e6ea'}[kind]
    im = Image.new('RGB', (w, h), bg); d = ImageDraw.Draw(im)
    road(d, w, h, 430)
    if kind == 'moto':
        moto(d, 280, 450, 1.3)
        cones(d, [120, 680], 430, 1.2)
    else:
        car(d, 130, 470, 1.8, body=W if kind == 'manual' else '#fdf6d8')
    d.rounded_rectangle([30, 30, 30 + 26 * len(label) + 40, 100], radius=20, fill=D)
    d.text((50, 65), label, fill=Y, font=font(36), anchor='lm')
    save(im, name)


def branch(name, title, extra):
    w, h = 900, 600
    im = Image.new('RGB', (w, h), '#cfe2f8'); d = ImageDraw.Draw(im)
    d.rectangle([0, 380, w, h], fill='#7fb069')
    # здание
    d.rectangle([90, 140, 520, 420], fill=W, outline=D, width=4)
    for r in range(2):
        for c in range(4):
            d.rectangle([120 + c * 100, 170 + r * 100, 190 + c * 100, 240 + r * 100], fill='#bcd6f5', outline=D, width=2)
    d.rectangle([90, 100, 520, 145], fill=B)
    d.text((305, 122), 'ПРАВЫЙ РЯД', fill=Y, font=font(30), anchor='mm')
    d.rectangle([280, 340, 330, 420], fill=D)
    if extra == 'autodrom':
        d.rectangle([560, 400, 880, 580], fill='#3a414a')
        for i in range(4):
            d.rectangle([580 + i * 75, 420, 586 + i * 75, 470], fill=W)
        cones(d, [600, 700, 800], 560, 0.9)
        car(d, 600, 540, 0.6)
    else:
        car(d, 580, 520, 0.9)
    d.rounded_rectangle([30, 30, 60 + 22 * len(title), 86], radius=18, fill=D)
    d.text((48, 58), title, fill=Y, font=font(30), anchor='lm')
    save(im, name)


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    hero(); og()
    instructor('ins-manual.webp', 'manual', 'МКПП')
    instructor('ins-auto.webp', 'auto', 'АКПП')
    instructor('ins-moto.webp', 'moto', 'Мотоцикл')
    branch('branch-center.webp', 'Центральный', 'autodrom')
    branch('branch-north.webp', 'Северный', 'class')
