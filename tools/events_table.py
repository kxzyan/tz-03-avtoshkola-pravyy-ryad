#!/usr/bin/env python3
"""Собирает docs/events.md: для каждого события — где оно отправляется (файл:строка) и параметры.
Запуск из корня репозитория после любых правок разметки: python3 tools/events_table.py"""
import re, glob, collections

EVENTS = [
    # (№, событие, тип, когда, параметры с примерами)
    (1, 'page_view', 'авто', 'Открытие любой страницы', 'page_location = https://…/prices.html, page_title = «Цены и калькулятор стоимости — Правый ряд»'),
    (2, 'scroll', 'авто', 'Прокрутка страницы до 90 %', 'percent_scrolled = 90'),
    (3, 'click', 'авто', 'Переход по ссылке на внешний сайт', 'link_url = https://t.me/pravyy_ryad_nabor, outbound = true'),
    (4, 'file_download', 'авто', 'Скачивание PDF с сайта', 'file_name = /files/price.pdf, file_extension = pdf'),
    (5, 'form_start', 'авто', 'Первое взаимодействие с формой заявки', 'form_id = lead'),
    (6, 'form_submit', 'авто', 'Отправка формы заявки', 'form_id = lead'),
    (7, 'generate_lead', 'рекоменд., ключевое', 'Приёмник заявок ответил ok: true', 'lead_category = b_auto, lead_source = instagram'),
    (8, 'cta_click', 'своё', 'Клик по любой кнопке заявки', 'button_name = hero_trial, page_section = hero'),
    (9, 'view_category', 'своё', 'Клик по карточке категории', 'category = b_manual'),
    (10, 'price_calc', 'своё', 'Расчёт в калькуляторе', 'category = b_auto, gearbox = auto, total_price = 51850'),
    (11, 'installment_click', 'своё', 'Выбор срока рассрочки', 'months = 6'),
    (12, 'instructor_view', 'своё', 'Фильтр или клик по карточке инструктора', 'gearbox = auto, instructor_id = ins_04 (фильтр: filter_auto)'),
    (13, 'pdd_test_start', 'своё', 'Начало тренажёра ПДД', 'page_section = pdd_page / home_teaser / pdd_retry'),
    (14, 'pdd_test_complete', 'своё', 'Ответ на 10-й вопрос тренажёра', 'score = 7'),
    (15, 'contact_click', 'своё, ключевое', 'Клик по телефону или e-mail', 'contact_type = phone / email'),
    (16, 'messenger_click', 'своё, ключевое', 'Клик по кнопке Telegram или WhatsApp', 'messenger = telegram / whatsapp'),
    (17, 'social_click', 'своё', 'Клик по иконке соцсети в подвале или на thanks.html', 'network = vk, page_section = footer / thanks'),
    (18, 'form_error', 'своё', 'Форма не отправлена из-за ошибки поля', 'field_name = phone, error_type = format / required / length / server'),
    (19, 'map_open', 'своё, по выбору', 'Клик по ссылке на карту', 'branch = center / north'),
    (20, 'branch_select', 'своё, по выбору', 'Переключение филиала', 'branch = center / north'),
]

AUTO_WHERE = {
    'page_view': 'тег gtag(\'config\') в `<head>` каждой страницы',
    'scroll': 'расширенная статистика GA4, без кода',
    'click': 'расширенная статистика GA4, без кода (ссылки на t.me, wa.me, соцсети, Яндекс Карты)',
    'file_download': 'расширенная статистика GA4: ссылка `files/price.pdf` в prices.html:{line}',
    'form_start': 'расширенная статистика GA4 (взаимодействия с формами): форма `#lead` в contacts.html:{line}',
    'form_submit': 'расширенная статистика GA4 (взаимодействия с формами): форма `#lead` в contacts.html:{line}',
}


def find():
    where = collections.defaultdict(list)
    files = sorted(glob.glob('*.html')) + sorted(glob.glob('js/*.js'))
    for f in files:
        for n, line in enumerate(open(f, encoding='utf-8'), 1):
            if line.lstrip().startswith('//'):
                continue  # примеры в комментариях не считаем
            for m in re.finditer(r'data-event="(\w+)"', line):
                where[m.group(1)].append(f'{f}:{n}')
            for m in re.finditer(r"track\('(\w+)'", line):
                where[m.group(1)].append(f'{f}:{n}')
    return where


def line_of(f, pat):
    for n, line in enumerate(open(f, encoding='utf-8'), 1):
        if pat in line:
            return n
    return '?'


def compress(locs):
    """Строки подвала и шапки повторяются на всех страницах — сворачиваем."""
    by_file = collections.OrderedDict()
    for l in locs:
        f, n = l.split(':')
        if n not in by_file.setdefault(f, []):
            by_file[f].append(n)
    return '<br>'.join(f'{f}:{",".join(ns)}' for f, ns in by_file.items())


def main():
    w = find()
    out = ['# Таблица событий GA4', '',
           'Все вызовы `gtag(\'event\', …)` — в `js/analytics.js` (функция `window.track`, строка '
           f'{line_of("js/analytics.js", "gtag(")}). Кнопки и ссылки размечены атрибутами `data-event` и `data-*`; '
           '`analytics.js` ловит клик и отправляет событие с параметрами из атрибутов (`data-button-name` → `button_name`). '
           'Скрипты страниц вызывают `window.track()` там, где событие не привязано к клику.', '',
           'Имена событий и параметров — snake_case, до 40 символов; значения обрезаются до 100 символов. '
           'Имя, телефон и e-mail в GA4 не передаются.', '',
           'Таблица собирается скриптом `python3 tools/events_table.py`, номера строк актуальны для текущей версии файлов.', '',
           '| № | Событие | Тип | Когда | Где отправляется (файл:строка) | Параметры и примеры значений |',
           '|---|---|---|---|---|---|']
    for num, ev, typ, when, params in EVENTS:
        if ev in AUTO_WHERE:
            loc = AUTO_WHERE[ev].format(line=line_of('prices.html' if ev == 'file_download' else 'contacts.html',
                                                     'files/price.pdf' if ev == 'file_download' else 'id="lead"'))
        else:
            loc = compress(w.get(ev, [])) or '—'
        out.append(f'| {num} | `{ev}` | {typ} | {when} | {loc} | {params} |')
    out += ['', '## Пользовательские параметры (Admin → Custom definitions, Event scope)', '',
            '| Параметр | События | Вопрос отчёта |', '|---|---|---|',
            '| button_name | cta_click | Какая кнопка заявки сработала |',
            '| page_section | cta_click, social_click | В каком блоке страницы был клик |',
            '| category | view_category, price_calc | Какая категория интересует |',
            '| gearbox | price_calc, instructor_view | Механика или автомат |',
            '| score | pdd_test_complete | Как проходят тренажёр |',
            '| lead_category | generate_lead | Категория в заявке |',
            '| messenger | messenger_click | Какой мессенджер выбирают |', '',
            '## Ключевые события (Key events)', '',
            '`generate_lead`, `contact_click`, `messenger_click`. Других ключевых событий в ресурсе нет.', '',
            '## Проверка в DebugView', '',
            'Снимки — `screens/ga4/<имя_события>.png`. Режим отладки — расширение Google Analytics Debugger '
            '(в коде `debug_mode` не включён).', '']
    open('docs/events.md', 'w', encoding='utf-8').write('\n'.join(out))
    missing = [e for _, e, t, *_ in EVENTS if e not in AUTO_WHERE and e not in w]
    print('docs/events.md готов', 'НЕТ В КОДЕ: ' + ', '.join(missing) if missing else '— все 14 своих событий найдены в коде')


if __name__ == '__main__':
    main()
