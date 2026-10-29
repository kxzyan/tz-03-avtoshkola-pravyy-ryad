#!/usr/bin/env python3
"""Ролик для Reel «3 ошибки, на которых валят на экзамене в ГИБДД» (1080×1920, ~18 с).
Кадры рисует Pillow, склейку с плавными переходами делает ffmpeg.
Запуск: python3 tools/make_reel.py <папка_для_вывода>"""
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

B, Y, D, W = '#1F6FD1', '#F5C518', '#1E2329', '#FFFFFF'
BOLD = '/usr/share/fonts/opentype/inter/Inter-Bold.otf'
REG = '/usr/share/fonts/opentype/inter/Inter-Regular.otf'
WIDTH, HEIGHT = 1080, 1920


def f(size, bold=True):
    return ImageFont.truetype(BOLD if bold else REG, size)


def wrap(d, text, font, width):
    words, lines, cur = text.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=font) <= width:
            cur = t
        else:
            lines.append(cur); cur = w
    lines.append(cur)
    return lines


def block(d, y, text, font, fill, width=920, gap=1.25):
    for line in wrap(d, text, font, width):
        d.text((80, y), line, font=font, fill=fill)
        y += int(font.size * gap)
    return y


def frame(bg, draw_fn, path):
    im = Image.new('RGB', (WIDTH, HEIGHT), bg)
    d = ImageDraw.Draw(im)
    d.text((80, 110), 'ПРАВЫЙ РЯД', font=f(56), fill=D if bg == Y else Y)
    d.text((80, 185), 'автошкола категорий A и B', font=f(36, False), fill=D if bg == Y else W)
    draw_fn(d)
    # дорожная разметка внизу
    d.rectangle([0, HEIGHT - 220, WIDTH, HEIGHT], fill='#3a414a')
    for x in range(0, WIDTH, 180):
        d.rectangle([x + 30, HEIGHT - 118, x + 120, HEIGHT - 100], fill=Y)
    im.save(path)


SLIDES = [
    (B, lambda d: (
        block(d, 520, '3 ошибки,', f(110), W),
        block(d, 660, 'на которых валят на экзамене в ГИБДД', f(92), W),
        block(d, 1180, 'Проверьте себя до экзамена', f(48, False), Y))),
    (D, lambda d: (
        block(d, 480, '1', f(220), Y),
        block(d, 760, 'Перестроение без взгляда в зеркала', f(76), W),
        block(d, 1060, 'Перед перестроением нужно убедиться, что это безопасно, и уступить тем, кто едет попутно. Пункты 8.1 и 8.4 ПДД.', f(44, False), '#cfd5dc'))),
    (D, lambda d: (
        block(d, 480, '2', f(220), Y),
        block(d, 760, 'Не уступили пешеходу на переходе', f(76), W),
        block(d, 1060, 'На нерегулируемом пешеходном переходе водитель обязан уступить дорогу пешеходам. Пункт 14.1 ПДД.', f(44, False), '#cfd5dc'))),
    (D, lambda d: (
        block(d, 480, '3', f(220), Y),
        block(d, 760, 'Проехали знак «STOP» без остановки', f(76), W),
        block(d, 1060, 'Знак 2.5 «Движение без остановки запрещено» требует полной остановки перед стоп-линией или краем пересекаемой дороги.', f(44, False), '#cfd5dc'))),
    (Y, lambda d: (
        block(d, 470, 'Напишите', f(100), D),
        block(d, 600, '«ТЕСТ»', f(170), B),
        block(d, 820, 'в комментариях — пришлём тренажёр: 10 вопросов по ПДД с разбором', f(64), D),
        block(d, 1230, 'Студентам до 30 ноября — скидка 15\u00a0%', f(52), D))),
]

if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else '.'
    os.makedirs(out, exist_ok=True)
    paths = []
    for i, (bg, fn) in enumerate(SLIDES):
        p = os.path.join(out, f'reel_{i}.png')
        frame(bg, fn, p)
        paths.append(p)
    dur, fade = 3.8, 0.5
    inputs, filters = [], []
    for p in paths:
        inputs += ['-loop', '1', '-t', str(dur), '-i', p]
    prev = '[0:v]'
    for i in range(1, len(paths)):
        off = round(i * (dur - fade), 2)
        filters.append(f'{prev}[{i}:v]xfade=transition=fade:duration={fade}:offset={off}[v{i}]')
        prev = f'[v{i}]'
    filters.append(f'{prev}format=yuv420p[out]')
    video = os.path.join(out, 'reel_3_oshibki.mp4')
    subprocess.run(['ffmpeg', '-y', *inputs, '-f', 'lavfi', '-t', '18', '-i', 'anullsrc=r=44100:cl=stereo',
                    '-filter_complex', ';'.join(filters), '-map', '[out]', '-map', f'{len(paths)}:a',
                    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '23', '-r', '30', '-c:a', 'aac', '-shortest',
                    '-movflags', '+faststart', video], check=True, capture_output=True)
    print(video)
