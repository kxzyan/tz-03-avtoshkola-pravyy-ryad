# Сайт автошколы «Правый ряд» (ТЗ-03/2026)

Исполнитель: Лийвак Александр, группа ____

| Что | Ссылка |
|---|---|
| Сайт на Vercel | https://tz-03-avtoshkola-pravyy-ryad-nine.vercel.app |
| Таблица заявок «PravyyRyad — Leads» | https://docs.google.com/spreadsheets/d/1ExZck83w5phzmtiI822BFeT2oyZDHupcdBE0dBR8vJI/edit |
| Дашборд DataLens «ПРАВЫЙ РЯД — students_nov_2026» | ____ |
| Instagram — профиль и Reel с автоответами | ____ |
| ВКонтакте — пост U-05 / пост колледжа U-06 | ____ / ____ |
| Telegram — разбор билета U-07 / закреп U-08 | ____ / ____ |
| YouTube — Shorts «Параллельная парковка» U-09 | ____ |
| Блогер 1 (U-10) / Блогер 2 (U-11) | ____ / ____ |

Идентификатор ресурса GA4: G-MTKHK71P7G (ресурс «ПРАВЫЙ РЯД — сайт», поток «Сайт Правый ряд (Vercel)»)

Доступ Viewer к ресурсу GA4 выдан: ____ (e-mail Заказчика)

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

Не получилось: ____

Нейросеть использовалась для: ____
