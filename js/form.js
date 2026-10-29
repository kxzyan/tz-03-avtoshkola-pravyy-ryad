var APP_URL = 'https://script.google.com/macros/s/ВАШ_ID/exec'; // TODO: адрес веб-приложения Apps Script
var UTM = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content'];
var form = document.getElementById('lead');
// метки из адреса сохраняем в sessionStorage, чтобы не потерять при переходах
var q = new URLSearchParams(location.search);
try { UTM.forEach(function (k) { if (q.get(k)) sessionStorage.setItem(k, q.get(k)); }); } catch (e) {}
function fillHidden() {
  var id = sessionStorage.getItem('request_id');
  if (!id) { id = 'REQ-' + crypto.randomUUID(); sessionStorage.setItem('request_id', id); }
  form.request_id.value = id;
  UTM.forEach(function (k) { form[k].value = sessionStorage.getItem(k) || ''; });
}
function showErr(field, type, text) {
  var s = form.querySelector('[data-for="' + field + '"]');
  if (s) s.textContent = text;
  if (form[field] && form[field].classList) form[field].classList.add('bad');
  window.track('form_error', { field_name: field, error_type: type });
}
function validate() {
  var ok = true, d = form;
  form.querySelectorAll('.err').forEach(function (s) { s.textContent = ''; });
  form.querySelectorAll('.bad').forEach(function (i) { i.classList.remove('bad'); });
  var name = d.name.value.trim(), phone = d.phone.value.trim(), email = d.email.value.trim();
  if (name.length < 2 || name.length > 60) { showErr('name', 'length', 'Введите имя от 2 до 60 символов'); ok = false; }
  if (!/^\+7\d{10}$/.test(phone)) { showErr('phone', 'format', 'Телефон в формате +79001234567'); ok = false; }
  if (email && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) { showErr('email', 'format', 'Проверьте адрес e-mail'); ok = false; }
  if (!d.consent.checked) { showErr('consent', 'required', 'Нужно согласие на обработку данных'); ok = false; }
  return ok;
}
fillHidden();
form.addEventListener('submit', function (e) {
  e.preventDefault();
  if (!validate()) return;
  var btn = document.getElementById('send');
  btn.disabled = true;
  var data = {};
  ['request_id', 'name', 'phone', 'email', 'category', 'branch'].concat(UTM).forEach(function (k) { data[k] = form[k].value.trim(); });
  fetch(APP_URL, { method: 'POST', headers: { 'Content-Type': 'text/plain;charset=utf-8' }, body: JSON.stringify(data) })
    .then(function (r) { return r.json(); })
    .then(function (res) {
      if (res.ok) {
        // в GA4 уходят только категория и источник, без имени, телефона и e-mail
        window.track('generate_lead', { lead_category: data.category, lead_source: data.utm_source || 'direct' });
        sessionStorage.setItem('last_request_id', data.request_id);
        sessionStorage.removeItem('request_id');
        location.href = 'thanks.html';
      } else { showErr('server', 'server', 'Не удалось отправить: ' + res.error); btn.disabled = false; }
    })
    .catch(function () { showErr('server', 'server', 'Ошибка связи. Попробуйте ещё раз'); btn.disabled = false; });
});
