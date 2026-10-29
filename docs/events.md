# Таблица событий GA4

Все вызовы `gtag('event', …)` — в `js/analytics.js` (функция `window.track`, строка 1). Кнопки и ссылки размечены атрибутами `data-event` и `data-*`; `analytics.js` ловит клик и отправляет событие с параметрами из атрибутов (`data-button-name` → `button_name`). Скрипты страниц вызывают `window.track()` там, где событие не привязано к клику.

Имена событий и параметров — snake_case, до 40 символов; значения обрезаются до 100 символов. Имя, телефон и e-mail в GA4 не передаются.

Таблица собирается скриптом `python3 tools/events_table.py`, номера строк актуальны для текущей версии файлов.

| № | Событие | Тип | Когда | Где отправляется (файл:строка) | Параметры и примеры значений |
|---|---|---|---|---|---|
| 1 | `page_view` | авто | Открытие любой страницы | тег gtag('config') в `<head>` каждой страницы | page_location = https://…/prices.html, page_title = «Цены и калькулятор стоимости — Правый ряд» |
| 2 | `scroll` | авто | Прокрутка страницы до 90 % | расширенная статистика GA4, без кода | percent_scrolled = 90 |
| 3 | `click` | авто | Переход по ссылке на внешний сайт | расширенная статистика GA4, без кода (ссылки на t.me, wa.me, соцсети, Яндекс Карты) | link_url = https://t.me/pravyy_ryad_nabor, outbound = true |
| 4 | `file_download` | авто | Скачивание PDF с сайта | расширенная статистика GA4: ссылка `files/price.pdf` в prices.html:88 | file_name = /files/price.pdf, file_extension = pdf |
| 5 | `form_start` | авто | Первое взаимодействие с формой заявки | расширенная статистика GA4 (взаимодействия с формами): форма `#lead` в contacts.html:41 | form_id = lead |
| 6 | `form_submit` | авто | Отправка формы заявки | расширенная статистика GA4 (взаимодействия с формами): форма `#lead` в contacts.html:41 | form_id = lead |
| 7 | `generate_lead` | рекоменд., ключевое | Приёмник заявок ответил ok: true | js/form.js:89 | lead_category = b_auto, lead_source = instagram |
| 8 | `cta_click` | своё | Клик по любой кнопке заявки | 404.html:45<br>branches.html:55,70<br>index.html:43,44,94<br>instructors.html:93<br>pdd-test.html:60<br>prices.html:89 | button_name = hero_trial, page_section = hero |
| 9 | `view_category` | своё | Клик по карточке категории | index.html:54,55,56,57 | category = b_manual |
| 10 | `price_calc` | своё | Расчёт в калькуляторе | js/calc.js:46 | category = b_auto, gearbox = auto, total_price = 51850 |
| 11 | `installment_click` | своё | Выбор срока рассрочки | js/calc.js:70 | months = 6 |
| 12 | `instructor_view` | своё | Фильтр или клик по карточке инструктора | instructors.html:41,42,43,44,54,61,68,75,82,89 | gearbox = auto, instructor_id = ins_04 (фильтр: filter_auto) |
| 13 | `pdd_test_start` | своё | Начало тренажёра ПДД | index.html:78<br>pdd-test.html:41,61 | page_section = pdd_page / home_teaser / pdd_retry |
| 14 | `pdd_test_complete` | своё | Ответ на 10-й вопрос тренажёра | js/pdd.js:81 | score = 7 |
| 15 | `contact_click` | своё, ключевое | Клик по телефону или e-mail | 404.html:31,51<br>branches.html:31,52,67,82<br>contacts.html:31,75,76,89<br>index.html:31,101<br>instructors.html:31,99<br>pdd-test.html:31,69<br>prices.html:31,96<br>privacy.html:31,85<br>thanks.html:31,40,63 | contact_type = phone / email |
| 16 | `messenger_click` | своё, ключевое | Клик по кнопке Telegram или WhatsApp | contacts.html:79,80 | messenger = telegram / whatsapp |
| 17 | `social_click` | своё | Клик по иконке соцсети в подвале или на thanks.html | 404.html:53,54,55,56<br>branches.html:84,85,86,87<br>contacts.html:91,92,93,94<br>index.html:103,104,105,106<br>instructors.html:101,102,103,104<br>pdd-test.html:71,72,73,74<br>prices.html:98,99,100,101<br>privacy.html:87,88,89,90<br>thanks.html:52,53,54,55,65,66,67,68 | network = vk, page_section = footer / thanks |
| 18 | `form_error` | своё | Форма не отправлена из-за ошибки поля | js/form.js:43 | field_name = phone, error_type = format / required / length / server |
| 19 | `map_open` | своё, по выбору | Клик по ссылке на карту | branches.html:54,69 | branch = center / north |
| 20 | `branch_select` | своё, по выбору | Переключение филиала | branches.html:41,42 | branch = center / north |

## Пользовательские параметры (Admin → Custom definitions, Event scope)

| Параметр | События | Вопрос отчёта |
|---|---|---|
| button_name | cta_click | Какая кнопка заявки сработала |
| page_section | cta_click, social_click | В каком блоке страницы был клик |
| category | view_category, price_calc | Какая категория интересует |
| gearbox | price_calc, instructor_view | Механика или автомат |
| score | pdd_test_complete | Как проходят тренажёр |
| lead_category | generate_lead | Категория в заявке |
| messenger | messenger_click | Какой мессенджер выбирают |

## Ключевые события (Key events)

`generate_lead`, `contact_click`, `messenger_click`. Других ключевых событий в ресурсе нет.

## Проверка в DebugView

Снимки — `screens/ga4/<имя_события>.png`. Режим отладки — расширение Google Analytics Debugger (в коде `debug_mode` не включён).
