// Калькулятор стоимости обучения (prices.html). Цены — из раздела 2 ТЗ.
(function () {
  var BASE = { b_manual: 49000, b_auto: 52000, a_moto: 28000, refresh: 17000 };
  var HOUR = 1800;            // дополнительный час вождения
  var DISC = 0.15;            // скидка студентам очной формы
  var MONTHS = [3, 6, 10];    // сроки рассрочки

  var $ = function (id) { return document.getElementById(id); };
  var catSel = $('c-cat'), gearBox = $('c-gear-box'), hours = $('c-hours'), stud = $('c-stud');
  var chosenMonths = 0, state = {};

  function fmt(n) { return n.toLocaleString('ru-RU') + ' ₽'; }

  // код категории для таблицы заявок и GA4: b_manual, b_auto, a_moto, refresh
  function category() {
    var c = catSel.value;
    if (c === 'a') return 'a_moto';
    if (c === 'refresh') return 'refresh';
    return gear() === 'auto' ? 'b_auto' : 'b_manual';
  }
  function gear() {
    if (catSel.value === 'a') return 'none';
    return document.querySelector('input[name="gear"]:checked').value;
  }

  function calc() {
    gearBox.hidden = catSel.value === 'a';
    var h = Math.min(20, Math.max(0, parseInt(hours.value, 10) || 0));
    $('c-hours-out').textContent = h;
    var cat = category();
    var sum = BASE[cat] + h * HOUR;
    var total = stud.checked ? Math.round(sum * (1 - DISC)) : sum;

    $('c-total').textContent = fmt(total);
    $('c-detail').textContent = fmt(BASE[cat]) + ' + ' + h + ' ч × ' + fmt(HOUR) +
      (stud.checked ? ' − 15 % скидки студенту' : '');
    $('c-inst').innerHTML = MONTHS.map(function (m) {
      var line = m + ' мес.: ' + fmt(Math.round(total / m)) + ' в месяц';
      return m === chosenMonths ? '<b>' + line + ' — выбранный срок</b>' : line;
    }).join('<br>');
    state = { category: cat, gearbox: gear(), total_price: total };
  }

  function calcAndTrack() {
    calc();
    window.track('price_calc', state);
  }

  // предвыбор из ссылки: prices.html?cat=b_auto или prices.html#auto (ветка «АВТОМАТ» в Instagram)
  var q = new URLSearchParams(location.search).get('cat');
  if (location.hash === '#auto') q = 'b_auto';
  if (q === 'a_moto') catSel.value = 'a';
  else if (q === 'refresh') catSel.value = 'refresh';
  else if (q === 'b_auto' || q === 'b_manual') {
    catSel.value = 'b';
    document.querySelector('input[name="gear"][value="' + (q === 'b_auto' ? 'auto' : 'manual') + '"]').checked = true;
  }

  catSel.addEventListener('change', calcAndTrack);
  stud.addEventListener('change', calcAndTrack);
  document.querySelectorAll('input[name="gear"]').forEach(function (r) { r.addEventListener('change', calcAndTrack); });
  hours.addEventListener('input', calc);          // число обновляется при движении ползунка
  hours.addEventListener('change', calcAndTrack); // событие — когда ползунок отпущен

  document.querySelectorAll('[data-m]').forEach(function (b) {
    b.addEventListener('click', function () {
      chosenMonths = Number(b.dataset.m);
      document.querySelectorAll('[data-m]').forEach(function (x) { x.setAttribute('aria-pressed', x === b); });
      calc();
      window.track('installment_click', { months: chosenMonths });
    });
  });

  calc(); // первый расчёт без события: price_calc — только после действия посетителя
})();
