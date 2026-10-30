# Сайт автошколы «Правый ряд» (ТЗ-03/2026)

Исполнитель: Лийвак Александр, группа ____

| Что | Ссылка |
|---|---|
| Сайт на Vercel | https://tz-03-avtoshkola-pravyy-ryad-nine.vercel.app |
| Таблица заявок «PravyyRyad — Leads» | https://docs.google.com/spreadsheets/d/1ExZck83w5phzmtiI822BFeT2oyZDHupcdBE0dBR8vJI/edit |
| Дашборд DataLens «ПРАВЫЙ РЯД — students_nov_2026» | ____ |
| Instagram — профиль / Reel с автоответами (ManyChat: «IG · Students Nov 2026 · Exam Reel», «… · АВТОМАТ») | https://www.instagram.com/axaxaxaxaxaxaxaxaxaxaxaxv/ / https://www.instagram.com/p/DfGLO3UhuaM/ |
| ВКонтакте — пост U-05 / пост колледжа U-06 | ____ / ____ |
| Telegram — разбор билета U-07 / закреп U-08 | ____ / ____ |
| YouTube — Shorts «Параллельная парковка» U-09 | ____ |
| Блогер 1 (U-10) / Блогер 2 (U-11) | ____ / ____ |

Идентификатор ресурса GA4: G-MTKHK71P7G (ресурс «ПРАВЫЙ РЯД — сайт», поток «Сайт Правый ряд (Vercel)»)

Доступ Viewer к ресурсу GA4 выдан: ____ (e-mail Заказчика)

## Состояние по разделам ТЗ

| Раздел | Сделано | Не сделано / в работе |
|---|---|---|
| 3. Сайт | 9 страниц, калькулятор (И-13 → 51 850 ₽), тренажёр ПДД, форма, адаптив 375/768/1280, OG-теги, WebP, публикация на Vercel с автодеплоем из `main` | снимок Lighthouse |
| 4. GA4 | ресурс «ПРАВЫЙ РЯД — сайт» (Москва, ₽), веб-поток с Enhanced measurement и формами, тег на всех 9 страницах, 20 событий в коде (`docs/events.md`), 7 пользовательских параметров (Event scope), лишние ключевые события `close_convert_lead` и `qualify_lead` сняты | отметка 3 ключевых событий (GA4 показывает новые события в списке через сутки), снимки DebugView |
| 5. UTM | реестр `docs/utm.csv` (все ячейки «заполнить» заполнены), QR `docs/qr-u-12.png`, афиша `docs/afisha.pdf`, ссылки U-02 и U-03 опубликованы в автоответах Instagram и проверены переходом | публикации ВКонтакте, Telegram, YouTube, у блогеров, короткие ссылки, отчёт через 24–48 ч |
| 6. Заявки | таблица «PravyyRyad — Leads» (12 столбцов, выпадающие списки, подсветка пустых и повторов), приёмник Apps Script (проверка полей, защита от повтора — И-05 пройдено), форма с ошибками у полей и `form_error` | проводка заявок по статусам `contract` / `lost` |
| 7. Instagram | Reel, две автоматизации ManyChat в Live (ТЕСТ → U-02, АВТОМАТ → U-03), ответы в комментариях и Direct, заявка из ветки АВТОМАТ дошла с метками U-03 (`screens/instagram/`) | снимки Direct, заявка по кнопке ветки ТЕСТ |
| 8. Отчёты | шаблон записки `docs/report.md` | отчёты, исследования, DataLens — нужны данные за 24–48 ч |

## Структура

```
tz-03-avtoshkola-pravyy-ryad/
├── index.html  prices.html  instructors.html  pdd-test.html  branches.html  contacts.html  thanks.html
│   privacy.html  404.html
├── css/style.css
├── js/analytics.js      все вызовы gtag('event', …), обработка data-event
├── js/utm.js            сохранение UTM-меток в sessionStorage на любой странице
├── js/form.js           форма заявки → Apps Script
├── js/calc.js  js/pdd.js  js/instructors.js  js/branches.js  js/thanks.js
├── img/                 иллюстрации WebP, og.jpg, favicon.svg
├── files/price.pdf      прайс-лист
├── apps-script/Code.gs  приёмник заявок doPost(e) + setup() для таблицы
├── docs/
│   ├── prompts.md       запросы к нейросети
│   ├── events.md        таблица событий
│   ├── utm.csv          реестр ссылок
│   ├── images.md        источники изображений
│   ├── report.md        аналитическая записка
│   ├── reports/         traffic-acquisition.csv, free-form.csv
│   └── afisha.pdf, qr-u-12.png
├── screens/ga4/  utm/  instagram/  reports/  explore/  datalens/  lighthouse/
└── tools/               скрипты для генерации файлов (на работу сайта не влияют)
```

Сайт — статические HTML, CSS и JavaScript, открываются без сборки. Vercel публикует папку как есть при каждом push в `main`.

## Как подключить сервисы

1. **Vercel.** vercel.com → Add New → Project → импортировать этот репозиторий, Framework Preset — *Other*, без команды сборки. После деплоя проверить адрес; если он отличается от указанного выше: `python3 tools/configure.py --site https://<имя>.vercel.app`, затем `SITE=https://<имя>.vercel.app python3 tools/make_files.py` (пересоберёт реестр, QR и афишу).
2. **GA4.** Ресурс «ПРАВЫЙ РЯД — сайт», часовой пояс (GMT+03:00) Москва, валюта — российский рубль; веб-поток с адресом Vercel, Enhanced measurement включён вместе с взаимодействиями с формами. Затем `python3 tools/configure.py --ga G-…` и push. Пользовательские параметры и ключевые события — по `docs/events.md`.
3. **Таблица и приёмник.** Создать таблицу «PravyyRyad — Leads», в Расширения → Apps Script вставить `apps-script/Code.gs`, указать `SHEET_ID`, запустить `setup()`, развернуть как веб-приложение (выполнять от имени владельца, доступ — все). URL `/exec`: `python3 tools/configure.py --app <URL>` и push.
4. **Реестр ссылок.** Загрузить `docs/utm.csv` в ту же таблицу на лист `utm`; полную ссылку собрать формулой (столбец I), например:
   `="https://tz-03-avtoshkola-pravyy-ryad-nine.vercel.app/"&ЕСЛИОШИБКА(ЛЕВСИМВ(H2;НАЙТИ("#";H2)-1);H2)&"?utm_source="&D2&"&utm_medium="&E2&"&utm_campaign="&F2&"&utm_content="&G2&ЕСЛИОШИБКА(ПСТР(H2;НАЙТИ("#";H2);100);"")`
   В U-10 и U-11 вместо `blogger1_nick` / `blogger2_nick` вписать ники партнёров латиницей. После публикаций заполнить короткие ссылки (vk.cc, clck.ru), адреса и даты и снова выгрузить лист в `docs/utm.csv`.

## Проверки

Локально: `python3 -m http.server` в корне репозитория и открыть http://localhost:8000. Калькулятор: B, автомат, 5 доп. часов, «Я студент» → 51 850 ₽ (испытание И-13).

Не получилось: к сроку сдачи не накопились данные за 24–48 часов для отчётов GA4 и DataLens (раздел 8); ключевые события GA4 нельзя отметить до появления событий в списке ресурса; публикации в ВКонтакте, Telegram, YouTube и у блогеров не выполнены.

Нейросеть использовалась для: генерации и доработки всех страниц, CSS и JavaScript сайта; кода приёмника Apps Script; иллюстраций, прайс-листа, QR-кода, афиши и ролика Reel (скрипты в `tools/`); реестра UTM и таблицы событий; настройки Vercel, GA4, таблицы заявок и ManyChat через браузер по моим запросам (см. `docs/prompts.md`).
