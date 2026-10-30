#!/usr/bin/env python3
"""Материалы для соцсетей: сторис U-04 (1080×1920 PNG) и Shorts U-09 «Параллельная парковка» (MP4).
Запуск из корня репозитория: python3 tools/make_social.py"""
import os, subprocess, tempfile, sys
sys.path.insert(0, os.path.dirname(__file__))
from make_reel import frame, block, f, B, Y, D, W

OUT = 'docs/social'


def stories():
    path = os.path.join(OUT, 'u04-stories.png')
    frame(B, lambda d: (
        block(d, 470, 'Сколько стоят права?', f(96), W),
        block(d, 760, 'B — от 49\u00a0000\u00a0₽, автомат — 52\u00a0000\u00a0₽, A — 28\u00a0000\u00a0₽', f(54), W),
        block(d, 980, 'Студентам −15 % до 30 ноября', f(64), Y),
        block(d, 1180, 'Рассрочка без переплаты на 3, 6 или 10 месяцев', f(46, False), W),
    ), path)
    print(path)


SHORTS = [
    (B, lambda d: (block(d, 560, 'Параллельная парковка', f(104), W),
                   block(d, 830, 'за 4 шага', f(104), Y),
                   block(d, 1060, 'Как на экзамене в ГИБДД', f(48, False), W))),
    (D, lambda d: (block(d, 480, '1', f(220), Y),
                   block(d, 760, 'Встаньте параллельно', f(76), W),
                   block(d, 980, 'Остановитесь рядом с машиной, за которой будете парковаться, на расстоянии около метра. Задние бамперы — примерно на одной линии.', f(44, False), '#cfd5dc'))),
    (D, lambda d: (block(d, 480, '2', f(220), Y),
                   block(d, 760, 'Задний ход и руль до упора', f(76), W),
                   block(d, 980, 'Включите указатель поворота и задний ход. Медленно назад — и поверните руль до упора в сторону парковки.', f(44, False), '#cfd5dc'))),
    (D, lambda d: (block(d, 480, '3', f(220), Y),
                   block(d, 760, 'Под углом — руль прямо', f(76), W),
                   block(d, 980, 'Когда машина встанет под углом около 45°, выровняйте колёса и продолжайте двигаться назад, следя за зеркалами.', f(44, False), '#cfd5dc'))),
    (D, lambda d: (block(d, 480, '4', f(220), Y),
                   block(d, 760, 'Руль в обратную сторону', f(76), W),
                   block(d, 980, 'Когда передний бампер пройдёт задний бампер соседней машины — руль до упора в обратную сторону и выровняйтесь.', f(44, False), '#cfd5dc'))),
    (Y, lambda d: (block(d, 520, 'Отработайте с инструктором', f(92), D),
                   block(d, 820, 'на МКПП или АКПП на автодроме', f(60), D),
                   block(d, 1080, 'Ссылка — в описании', f(64), B),
                   block(d, 1260, 'Студентам до 30 ноября — скидка 15 %', f(52), D))),
]


def shorts():
    tmp = tempfile.mkdtemp()
    paths = []
    for i, (bg, fn) in enumerate(SHORTS):
        p = os.path.join(tmp, f's{i}.png'); frame(bg, fn, p); paths.append(p)
    dur, fade = 3.8, 0.5
    inputs, filters, prev = [], [], '[0:v]'
    for p in paths:
        inputs += ['-loop', '1', '-t', str(dur), '-i', p]
    for i in range(1, len(paths)):
        filters.append(f'{prev}[{i}:v]xfade=transition=fade:duration={fade}:offset={round(i * (dur - fade), 2)}[v{i}]')
        prev = f'[v{i}]'
    filters.append(f'{prev}format=yuv420p[out]')
    total = round(len(paths) * dur - (len(paths) - 1) * fade, 2)
    video = os.path.join(OUT, 'u09-shorts-parking.mp4')
    subprocess.run(['ffmpeg', '-y', *inputs, '-f', 'lavfi', '-t', str(total), '-i', 'anullsrc=r=44100:cl=stereo',
                    '-filter_complex', ';'.join(filters), '-map', '[out]', '-map', f'{len(paths)}:a',
                    '-c:v', 'libx264', '-preset', 'veryfast', '-tune', 'stillimage', '-crf', '26', '-r', '30',
                    '-c:a', 'aac', '-b:a', '32k', '-shortest', '-movflags', '+faststart', video],
                   check=True, capture_output=True)
    print(video)


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    stories(); shorts()
