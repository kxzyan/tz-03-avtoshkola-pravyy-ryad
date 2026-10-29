var PRICE = { b_manual: 49000, b_auto: 52000, a_moto: 28000, refresh: 17000 };
var HOUR = 1800, DISC = 0.15, total = 0, cat, hours;
var fmt = function (n) { return n.toLocaleString('ru-RU') + ' ₽'; };
function gearbox(c) { return c === 'b_auto' ? 'auto' : c === 'b_manual' ? 'manual' : 'none'; }
function calc() {
  cat = document.getElementById('c-cat').value;
  hours = Math.min(20, Math.max(0, parseInt(document.getElementById('c-hours').value, 10) || 0));
  total = PRICE[cat] + hours * HOUR;
  if (document.getElementById('c-stud').checked) total = Math.round(total * (1 - DISC));
  document.getElementById('c-total').textContent = fmt(total);
  document.getElementById('c-inst').innerHTML = [3, 6, 10].map(function (m) {
    return m + ' мес.: ' + fmt(Math.round(total / m)) + ' в месяц';
  }).join('<br>');
  window.track('price_calc', { category: cat, gearbox: gearbox(cat), total_price: total });
}
['c-cat', 'c-hours', 'c-stud'].forEach(function (id) {
  document.getElementById(id).addEventListener('change', calc);
});
document.querySelectorAll('[data-m]').forEach(function (b) {
  b.addEventListener('click', function () { window.track('installment_click', { months: Number(b.dataset.m) }); });
});
calc();
