var SHEET_ID = 'ВАШ_ID_ТАБЛИЦЫ'; // идентификатор таблицы «PravyyRyad — Leads»
var COLS = ['request_id','created_at','name','phone','email','category','branch','utm_source','utm_medium','utm_campaign','utm_content','status'];
var CATS = ['b_manual','b_auto','a_moto','refresh'], BRANCHES = ['center','north','online'];

function out(o) { return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }

function doPost(e) {
  var lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    var d = JSON.parse(e.postData.contents);
    var err = check(d);
    if (err) return out({ ok: false, error: err });
    var sh = SpreadsheetApp.openById(SHEET_ID).getSheetByName('leads');
    var ids = sh.getRange(2, 1, Math.max(sh.getLastRow() - 1, 1), 1).getValues().flat();
    if (ids.indexOf(d.request_id) !== -1) return out({ ok: false, error: 'Заявка уже принята' });
    var row = COLS.map(function (c) {
      if (c === 'created_at') return new Date();
      if (c === 'status') return 'new';               // статус из браузера игнорируется
      var v = String(d[c] || '').trim();
      if (c === 'utm_source') return v || 'direct';
      if (c === 'utm_medium') return v || 'none';
      if (c === 'utm_campaign' || c === 'utm_content') return v || 'not_set';
      return v;
    });
    sh.appendRow(row);
    return out({ ok: true });
  } catch (x) {
    return out({ ok: false, error: 'Ошибка сервера' });
  } finally { lock.releaseLock(); }
}

function check(d) {
  if (!d.request_id || d.request_id.indexOf('REQ-') !== 0) return 'Нет номера заявки';
  if (!d.name || d.name.trim().length < 2 || d.name.trim().length > 60) return 'Некорректное имя';
  if (!/^\+7\d{10}$/.test(d.phone || '')) return 'Некорректный телефон';
  if (d.email && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(d.email)) return 'Некорректный e-mail';
  if (CATS.indexOf(d.category) === -1) return 'Некорректная категория';
  if (BRANCHES.indexOf(d.branch) === -1) return 'Некорректный филиал';
  for (var k in d) { if (String(d[k]).length > 200) return 'Слишком длинное значение: ' + k; }
  return null;
}
