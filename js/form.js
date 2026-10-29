// Форма заявки (contacts.html): проверка полей, скрытые поля, отправка в Apps Script через fetch.
// Адрес веб-приложения Apps Script (Развернуть → Веб-приложение → URL, оканчивается на /exec):
var APP_URL = 'https://script.google.com/macros/s/ВАШ_ID/exec';

(function () {
  var UTM = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content'];
  var form = document.getElementById('lead');
  var btn = document.getElementById('send');
  var q = new URLSearchParams(location.search);

  function store(k, v) { try { if (v === undefined) return sessionStorage.getItem(k); sessionStorage.setItem(k, v); } catch (e) { return null; } }
  function uuid() {
    if (window.crypto && crypto.randomUUID) return crypto.randomUUID();
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
      var r = Math.random() * 16 | 0; return (c === 'x' ? r : (r & 3 | 8)).toString(16);
    });
  }

  // предвыбор категории и филиала из ссылок сайта: contacts.html?cat=b_auto&branch=north
  if (q.get('cat') && form.category.querySelector('option[value="' + q.get('cat') + '"]')) form.category.value = q.get('cat');
  if (q.get('branch') && form.branch.querySelector('option[value="' + q.get('branch') + '"]')) form.branch.value = q.get('branch');

  // скрытые поля: номер заявки REQ-UUID и метки (из sessionStorage — их сохраняет utm.js на странице входа)
  function fillHidden() {
    var id = store('request_id');
    if (!id) { id = 'REQ-' + uuid(); store('request_id', id); }
    form.request_id.value = id;
    UTM.forEach(function (k) { form[k].value = store(k) || q.get(k) || ''; });
  }

  // +7 и 10 цифр; 8XXXXXXXXXX и номера с пробелами, скобками и дефисами приводятся к этому виду
  function normPhone(v) {
    var d = v.replace(/\D/g, '');
    if (d.length === 11 && (d[0] === '8' || d[0] === '7')) d = d.slice(1);
    return d.length === 10 ? '+7' + d : v.trim();
  }

  function showErr(field, type, text) {
    var s = form.querySelector('[data-for="' + field + '"]');
    if (s) s.textContent = text;
    var input = form.elements[field];
    if (input && input.classList) { input.classList.add('bad'); input.setAttribute('aria-invalid', 'true'); }
    window.track('form_error', { field_name: field, error_type: type });
  }

  function clearErr() {
    form.querySelectorAll('.err').forEach(function (s) { s.textContent = ''; });
    form.querySelectorAll('.bad').forEach(function (i) { i.classList.remove('bad'); i.removeAttribute('aria-invalid'); });
  }

  function validate() {
    clearErr();
    var ok = true;
    var name = form.name.value.trim(), email = form.email.value.trim();
    form.phone.value = normPhone(form.phone.value);
    var phone = form.phone.value;
    if (!name) { showErr('name', 'required', 'Введите имя'); ok = false; }
    else if (name.length < 2 || name.length > 60) { showErr('name', 'length', 'Имя — от 2 до 60 символов'); ok = false; }
    if (!phone) { showErr('phone', 'required', 'Введите телефон'); ok = false; }
    else if (!/^\+7\d{10}$/.test(phone)) { showErr('phone', 'format', 'Телефон в формате +7 и 10 цифр, например +79001234567'); ok = false; }
    if (email && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) { showErr('email', 'format', 'Проверьте адрес e-mail, например name@mail.ru'); ok = false; }
    if (!form.consent.checked) { showErr('consent', 'required', 'Отметьте согласие на обработку персональных данных'); ok = false; }
    if (!ok) { var first = form.querySelector('.bad'); if (first) first.focus(); }
    return ok;
  }

  fillHidden();

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (btn.disabled || !validate()) return;
    btn.disabled = true;
    btn.textContent = 'Отправляем…';
    var data = {};
    ['request_id', 'name', 'phone', 'email', 'category', 'branch'].concat(UTM).forEach(function (k) {
      data[k] = form[k].value.trim();
    });
    function fail(text) {
      showErr('server', 'server', text);
      btn.disabled = false;
      btn.textContent = 'Отправить заявку';
    }
    // text/plain — «простой» запрос без предварительного CORS-запроса, Apps Script его принимает
    fetch(APP_URL, { method: 'POST', headers: { 'Content-Type': 'text/plain;charset=utf-8' }, body: JSON.stringify(data) })
      .then(function (r) { return r.json(); })
      .then(function (res) {
        if (res.ok) {
          // в GA4 уходят только категория и источник — без имени, телефона и e-mail
          window.track('generate_lead', { lead_category: data.category, lead_source: data.utm_source || 'direct' });
          store('last_request_id', data.request_id);
          try { sessionStorage.removeItem('request_id'); } catch (x) {}
          setTimeout(function () { location.href = 'thanks.html'; }, 300); // время на отправку события
        } else {
          fail('Заявка не отправлена: ' + (res.error || 'ошибка приёмника') + '. Позвоните нам: +7 (900) 312-12-12');
        }
      })
      .catch(function () { fail('Ошибка связи. Проверьте интернет и попробуйте ещё раз или позвоните: +7 (900) 312-12-12'); });
  });
})();
