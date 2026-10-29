#!/usr/bin/env python3
"""Генерирует файлы проекта из одного места:
  docs/utm.csv       — реестр ссылок (полная ссылка собрана из меток, как формула в Google Таблице)
  docs/qr-u-12.png   — QR-код полной ссылки строки U-12 (листовки)
  docs/afisha.pdf    — афиша A4 с этим QR-кодом
  files/price.pdf    — прайс-лист для скачивания на prices.html
Запуск из корня репозитория:  SITE=https://<имя>.vercel.app python3 tools/make_files.py
Нужны пакеты reportlab и Pillow. Короткие ссылки, адреса и даты публикаций дописываются в CSV вручную
(или выгружаются из Google Таблицы, лист utm) после публикации.
"""
import csv, os, sys
from PIL import Image, ImageDraw
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode.qr import QrCodeWidget

SITE = os.environ.get('SITE', 'https://tz-03-avtoshkola-pravyy-ryad.vercel.app').rstrip('/')
BLUE, YELLOW, DARK = HexColor('#1F6FD1'), HexColor('#F5C518'), HexColor('#1E2329')

pdfmetrics.registerFont(TTFont('Sans', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('Sans-Bold', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))

# номер, канал, размещение, source, medium, campaign, content, страница, комментарий
# Ники блогеров (U-10, U-11) — ники двух студентов-партнёров латиницей: заменить blogger1_nick / blogger2_nick.
ROWS = [
    ('U-01', 'Instagram', 'ссылка в шапке профиля', 'instagram', 'social', 'students_nov_2026', 'bio', 'index.html', ''),
    ('U-02', 'Instagram', 'автоответ под Reel (ManyChat)', 'instagram', 'social', 'students_nov_2026', 'reel_exam_01', 'pdd-test.html', 'кнопка «Пройти тренажёр» в Direct'),
    ('U-03', 'Instagram', 'автоответ, ветка «АВТОМАТ»', 'instagram', 'social', 'auto_nov_2026', 'reel_exam_01_auto', 'prices.html#auto', 'метки стоят до якоря #auto'),
    ('U-04', 'Instagram', 'ссылка-стикер в Stories', 'instagram', 'social', 'students_nov_2026', 'stories_01', 'prices.html', ''),
    ('U-05', 'ВКонтакте', 'пост в сообществе', 'vk', 'social', 'students_nov_2026', 'post_01', 'index.html', 'короткая ссылка vk.cc'),
    ('U-06', 'ВКонтакте', 'пост в сообществе колледжа (по договорённости)', 'vk', 'social', 'students_nov_2026', 'college_post_01', 'prices.html', 'короткая ссылка vk.cc'),
    ('U-07', 'Telegram', 'разбор билета в канале', 'telegram', 'social', 'students_nov_2026', 'ticket_review', 'pdd-test.html', 'короткая ссылка clck.ru'),
    ('U-08', 'Telegram', 'закреплённое сообщение', 'telegram', 'social', 'students_nov_2026', 'pinned', 'index.html', 'короткая ссылка clck.ru'),
    ('U-09', 'YouTube', 'описание Shorts «Параллельная парковка»', 'youtube', 'social', 'students_nov_2026', 'shorts_parking', 'instructors.html',
     'видео о практическом вождении: зрителю важно, кто и на какой машине учит парковке — ведём на инструкторов и автомобили (МКПП/АКПП)'),
    ('U-10', 'Блогер 1', 'ссылка у партнёра', 'blogger1_nick', 'affiliate', 'students_nov_2026', 'stories_01', 'index.html', 'ник партнёра латиницей; сторис'),
    ('U-11', 'Блогер 2', 'ссылка у партнёра', 'blogger2_nick', 'affiliate', 'students_nov_2026', 'post_01', 'prices.html', 'ник партнёра латиницей; пост'),
    ('U-12', 'Листовки', 'QR-код на листовке у колледжа', 'leaflet_qr', 'qr', 'students_nov_2026', 'leaflet_a4_01', 'prices.html', 'QR docs/qr-u-12.png, афиша docs/afisha.pdf'),
]

HEADER = ['номер', 'канал', 'размещение', 'utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'страница',
          'полная ссылка', 'короткая ссылка', 'адрес публикации', 'дата публикации', 'комментарий']


def full_link(page, src, med, camp, cont):
    """Как формула в таблице: метки после ? и до #."""
    path, _, anchor = page.partition('#')
    url = f'{SITE}/{path}?utm_source={src}&utm_medium={med}&utm_campaign={camp}&utm_content={cont}'
    return url + (f'#{anchor}' if anchor else '')


def check_tag(v):
    import re
    assert re.fullmatch(r'[a-z0-9_]+', v), f'метка нарушает правило 5.1: {v}'


def write_csv():
    old = {}
    if os.path.exists('docs/utm.csv'):  # не затираем вручную внесённые короткие ссылки и публикации
        with open('docs/utm.csv', encoding='utf-8-sig') as f:
            for r in csv.DictReader(f):
                old[r['номер']] = r
    with open('docs/utm.csv', 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f)
        w.writerow(HEADER)
        for n, ch, pl, s, m, c, ct, page, note in ROWS:
            for t in (s, m, c, ct):
                check_tag(t)
            assert m in ('social', 'affiliate', 'qr', 'email', 'cpc', 'referral')
            o = old.get(n, {})
            w.writerow([n, ch, pl, s, m, c, ct, page, full_link(page, s, m, c, ct),
                        o.get('короткая ссылка', ''), o.get('адрес публикации', ''), o.get('дата публикации', ''), note])
    print('docs/utm.csv', len(ROWS), 'строк')


def qr_matrix(data):
    w = QrCodeWidget(data, barLevel='M')
    w.draw()
    q = w.qr
    n = q.getModuleCount()
    return [[q.isDark(r, c) for c in range(n)] for r in range(n)]


def qr_png(data, path, box=12, border=4):
    m = qr_matrix(data)
    n = len(m)
    size = (n + 2 * border) * box
    im = Image.new('L', (size, size), 255)
    d = ImageDraw.Draw(im)
    for r in range(n):
        for c in range(n):
            if m[r][c]:
                x, y = (c + border) * box, (r + border) * box
                d.rectangle([x, y, x + box - 1, y + box - 1], fill=0)
    im.save(path, optimize=True)
    print(path, im.size)


def afisha(link, qr_path):
    c = canvas.Canvas('docs/afisha.pdf', pagesize=A4)
    c.setTitle('Афиша: Студентам — 15 % скидки. Автошкола «Правый ряд»')
    W, H = A4
    c.setFillColor(BLUE); c.rect(0, H - 120 * mm, W, 120 * mm, fill=1, stroke=0)
    c.setFillColor(YELLOW); c.setFont('Sans-Bold', 30); c.drawString(20 * mm, H - 28 * mm, 'ПРАВЫЙ РЯД')
    c.setFillColor(white); c.setFont('Sans', 14); c.drawString(20 * mm, H - 37 * mm, 'автошкола категорий A и B · г. Новоозёрск')
    c.setFont('Sans-Bold', 40); c.drawString(20 * mm, H - 65 * mm, 'Студентам —')
    c.drawString(20 * mm, H - 82 * mm, 'скидка 15 %')
    c.setFont('Sans', 16)
    c.drawString(20 * mm, H - 98 * mm, 'до 30 ноября 2026 года при предъявлении')
    c.drawString(20 * mm, H - 106 * mm, 'студенческого билета очной формы')

    c.setFillColor(DARK); c.setFont('Sans-Bold', 18); c.drawString(20 * mm, H - 138 * mm, 'Стоимость обучения')
    c.setFont('Sans', 13)
    y = H - 150 * mm
    for t, p in [('Категория B, механика — теория 3 мес. + 56 ч вождения', '49 000 ₽'),
                 ('Категория B, автомат — 54 ч вождения', '52 000 ₽'),
                 ('Категория A — мотоцикл', '28 000 ₽'),
                 ('Восстановление навыков — 10 ч вождения', '17 000 ₽')]:
        c.drawString(20 * mm, y, t); c.drawRightString(W - 20 * mm, y, p); y -= 8 * mm
    c.drawString(20 * mm, y - 2 * mm, 'Рассрочка без переплаты на 3, 6 или 10 месяцев.')

    qs = 62 * mm
    c.drawImage(qr_path, 20 * mm, 30 * mm, qs, qs)
    c.setFont('Sans-Bold', 16); c.drawString(90 * mm, 80 * mm, 'Наведите камеру на QR-код,')
    c.drawString(90 * mm, 72 * mm, 'чтобы рассчитать стоимость')
    c.setFont('Sans', 12)
    c.drawString(90 * mm, 60 * mm, 'Калькулятор цены и рассрочки на сайте')
    c.drawString(90 * mm, 50 * mm, 'Теория: пн, ср, пт 18:30–21:00 или онлайн')
    c.drawString(90 * mm, 42 * mm, 'ул. Автомобилистов, 22 · ул. Полярная, 5')
    c.setFont('Sans-Bold', 14); c.drawString(90 * mm, 32 * mm, '+7 (900) 312-12-12')
    c.setFillColor(HexColor('#4a525c'))
    fs = 7
    while pdfmetrics.stringWidth(link, 'Sans', fs) > W - 40 * mm:
        fs -= 0.25
    c.setFont('Sans', fs); c.drawString(20 * mm, 15 * mm, link)
    c.setFont('Sans', 7)
    c.drawString(20 * mm, 10 * mm, 'ЧУ ДПО «Автошкола „Правый ряд“», ИНН 9903 225 914. С первой попытки экзамен сдали 68 % учеников за 2025 год.')
    c.showPage(); c.save()
    print('docs/afisha.pdf')


def price_pdf():
    c = canvas.Canvas('files/price.pdf', pagesize=A4)
    c.setTitle('Прайс-лист автошколы «Правый ряд»')
    W, H = A4
    c.setFillColor(DARK); c.rect(0, H - 40 * mm, W, 40 * mm, fill=1, stroke=0)
    c.setFillColor(YELLOW); c.setFont('Sans-Bold', 24); c.drawString(20 * mm, H - 22 * mm, 'ПРАВЫЙ РЯД')
    c.setFillColor(white); c.setFont('Sans', 12); c.drawString(20 * mm, H - 31 * mm, 'Прайс-лист на обучение · ноябрь 2026')
    c.setFillColor(DARK); c.setFont('Sans-Bold', 12)
    y = H - 60 * mm
    c.drawString(20 * mm, y, 'Услуга'); c.drawString(92 * mm, y, 'Что входит'); c.drawRightString(W - 20 * mm, y, 'Цена')
    c.setStrokeColor(BLUE); c.setLineWidth(1.5); c.line(20 * mm, y - 3 * mm, W - 20 * mm, y - 3 * mm)
    c.setFont('Sans', 11); c.setLineWidth(.5); c.setStrokeColor(HexColor('#d5dae0'))
    y -= 12 * mm
    for s, what, p in [('Категория B, механика', 'Теория 3 месяца + 56 ч вождения', '49 000 ₽'),
                       ('Категория B, автомат', '54 часа вождения', '52 000 ₽'),
                       ('Категория A', 'Обучение на мотоцикл', '28 000 ₽'),
                       ('Восстановление навыков', '10 часов вождения', '17 000 ₽'),
                       ('Дополнительный час вождения', '1 час', '1 800 ₽')]:
        c.drawString(20 * mm, y, s); c.drawString(92 * mm, y, what); c.drawRightString(W - 20 * mm, y, p)
        c.line(20 * mm, y - 4 * mm, W - 20 * mm, y - 4 * mm); y -= 11 * mm
    y -= 6 * mm
    c.setFont('Sans-Bold', 12); c.drawString(20 * mm, y, 'Оплата'); y -= 7 * mm
    c.setFont('Sans', 11)
    for t in ['Сразу или в рассрочку без переплаты на 3, 6 или 10 месяцев.',
              'Студентам очной формы — скидка 15 % до 30 ноября 2026 года',
              'при предъявлении студенческого билета.']:
        c.drawString(20 * mm, y, t); y -= 6 * mm
    y -= 6 * mm
    c.setFont('Sans-Bold', 12); c.drawString(20 * mm, y, 'Филиалы'); y -= 7 * mm
    c.setFont('Sans', 11)
    for t in ['Центральный: ул. Автомобилистов, 22 (классы, автодром)',
              'Северный: ул. Полярная, 5 (класс)',
              'Теория — пн, ср, пт с 18:30 до 21:00 или онлайн.']:
        c.drawString(20 * mm, y, t); y -= 6 * mm
    c.setFont('Sans', 9); c.setFillColor(HexColor('#4a525c'))
    c.drawString(20 * mm, 20 * mm, 'ЧУ ДПО «Автошкола „Правый ряд“» · 614 133, г. Новоозёрск, ул. Автомобилистов, д. 22')
    c.drawString(20 * mm, 15 * mm, 'ИНН 9903 225 914 · +7 (900) 312-12-12 · info@pravyy-ryad.example')
    c.showPage(); c.save()
    print('files/price.pdf')


if __name__ == '__main__':
    os.makedirs('docs', exist_ok=True); os.makedirs('files', exist_ok=True)
    write_csv()
    u12 = [r for r in ROWS if r[0] == 'U-12'][0]
    link = full_link(u12[7], *u12[3:7])
    qr_png(link, 'docs/qr-u-12.png')
    afisha(link, 'docs/qr-u-12.png')
    price_pdf()
