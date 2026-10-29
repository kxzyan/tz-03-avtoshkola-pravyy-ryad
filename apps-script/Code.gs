/**
 * Приёмник заявок с сайта «Правый ряд» → Google Таблица «PravyyRyad — Leads», лист leads.
 * Развёртывание: Расширения → Apps Script → вставить код → Развернуть → Новое развёртывание →
 * Тип «Веб-приложение», «Выполнять от имени: я», «Доступ: все». URL /exec вставить в js/form.js (APP_URL).
 * Один раз запустить setup() — он создаст заголовки, проверку данных и условное форматирование.
 * Пароли и ключи в коде не хранятся; идентификатор таблицы — не секрет.
 */
var SHEET_ID = '1ExZck83w5phzmtiI822BFeT2oyZDHupcdBE0dBR8vJI'; // из адреса таблицы: docs.google.com/spreadsheets/d/<ID>/edit
var SHEET_NAME = 'leads';
var COLS = ['request_id', 'created_at', 'name', 'phone', 'email', 'category', 'branch',
            'utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'status'];
var CATS = ['b_manual', 'b_auto', 'a_moto', 'refresh'];
var BRANCHES = ['center', 'north', 'online'];
var STATUSES = ['new', 'contacted', 'consult_booked', 'contract', 'lost'];
var MAX_LEN = 200;

function out(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
}

function sheet() {
  return SpreadsheetApp.openById(SHEET_ID).getSheetByName(SHEET_NAME);
}

/** Проверка, что приёмник жив: открыть URL /exec в браузере. */
function doGet() {
  return out({ ok: true, service: 'pravyy-ryad-leads' });
}

function doPost(e) {
  var lock = LockService.getScriptLock();
  try {
    lock.waitLock(10000); // две одновременные заявки не запишутся в одну строку
  } catch (x) {
    return out({ ok: false, error: 'Сервер занят, повторите через минуту' });
  }
  try {
    var d;
    try { d = JSON.parse(e.postData.contents); } catch (x) { return out({ ok: false, error: 'Неверный формат данных' }); }

    var err = check(d);
    if (err) return out({ ok: false, error: err });

    var sh = sheet();
    var last = sh.getLastRow();
    if (last > 1) {
      var ids = sh.getRange(2, 1, last - 1, 1).getValues().map(function (r) { return String(r[0]); });
      if (ids.indexOf(d.request_id) !== -1) return out({ ok: false, error: 'Заявка с таким номером уже принята' });
    }

    var row = COLS.map(function (c) {
      if (c === 'created_at') return new Date();   // время ставит приёмник
      if (c === 'status') return 'new';             // статус из браузера игнорируется
      var v = String(d[c] == null ? '' : d[c]).trim();
      if (c === 'utm_source') return v || 'direct';
      if (c === 'utm_medium') return v || 'none';
      if (c === 'utm_campaign' || c === 'utm_content') return v || 'not_set';
      if (c === 'phone') return "'" + v;            // апостроф: таблица хранит +7… как текст, «+» не теряется
      return v;
    });
    sh.appendRow(row);
    return out({ ok: true, request_id: d.request_id });
  } catch (x) {
    return out({ ok: false, error: 'Ошибка сервера' });
  } finally {
    lock.releaseLock();
  }
}

/** Возвращает текст ошибки или null, если данные в порядке. */
function check(d) {
  if (!d || typeof d !== 'object') return 'Нет данных';
  for (var k in d) {
    if (String(d[k]).length > MAX_LEN) return 'Слишком длинное значение: ' + k;
  }
  if (!/^REQ-[0-9a-f-]{36}$/i.test(d.request_id || '')) return 'Нет номера заявки';
  var name = String(d.name || '').trim();
  if (name.length < 2 || name.length > 60) return 'Имя должно быть от 2 до 60 символов';
  if (!/^\+7\d{10}$/.test(d.phone || '')) return 'Телефон должен быть в формате +7 и 10 цифр';
  if (d.email && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(d.email)) return 'Некорректный e-mail';
  if (CATS.indexOf(d.category) === -1) return 'Недопустимая категория';
  if (BRANCHES.indexOf(d.branch) === -1) return 'Недопустимый филиал';
  return null;
}

/**
 * Один раз: заголовки, выпадающий список status, проверка category и branch,
 * подсветка пустых обязательных ячеек и повторяющихся request_id.
 */
function setup() {
  var ss = SpreadsheetApp.openById(SHEET_ID);
  var sh = ss.getSheetByName(SHEET_NAME) || ss.insertSheet(SHEET_NAME);
  sh.getRange(1, 1, 1, COLS.length).setValues([COLS]).setFontWeight('bold');
  sh.setFrozenRows(1);
  var n = sh.getMaxRows() - 1;

  function list(col, values) {
    var rule = SpreadsheetApp.newDataValidation().requireValueInList(values, true).setAllowInvalid(false).build();
    sh.getRange(2, COLS.indexOf(col) + 1, n, 1).setDataValidation(rule);
  }
  list('status', STATUSES);
  list('category', CATS);
  list('branch', BRANCHES);
  sh.getRange(2, COLS.indexOf('created_at') + 1, n, 1).setNumberFormat('dd.MM.yyyy HH:mm:ss');
  sh.getRange(2, COLS.indexOf('phone') + 1, n, 1).setNumberFormat('@'); // текст: +7… не станет числом

  var rules = [];
  // повторяющиеся request_id — красным
  rules.push(SpreadsheetApp.newConditionalFormatRule()
    .whenFormulaSatisfied('=AND($A2<>"",COUNTIF($A:$A,$A2)>1)')
    .setBackground('#f4c7c3').setRanges([sh.getRange(2, 1, n, 1)]).build());
  // формулы в Apps Script пишутся с запятыми, независимо от языка таблицы
  // пустые обязательные ячейки (все, кроме email) в заполненной строке — жёлтым
  COLS.forEach(function (c, i) {
    if (c === 'email') return;
    var letter = String.fromCharCode(65 + i);
    rules.push(SpreadsheetApp.newConditionalFormatRule()
      .whenFormulaSatisfied('=AND(COUNTA($A2:$L2)>0,' + letter + '2="")')
      .setBackground('#fce8b2').setRanges([sh.getRange(2, i + 1, n, 1)]).build());
  });
  sh.setConditionalFormatRules(rules);
}
