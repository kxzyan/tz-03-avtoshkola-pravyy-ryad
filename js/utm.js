// Сохраняет UTM-метки из адреса страницы в sessionStorage,
// чтобы они не потерялись, пока посетитель ходит по сайту до формы заявки.
// Подключён на всех страницах: посетитель из соцсети может прийти на любую из них.
(function () {
  var UTM = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content'];
  var q = new URLSearchParams(location.search);
  var hasNew = UTM.some(function (k) { return q.get(k); });
  if (!hasNew) return;
  try {
    // пришёл новый переход с метками — заменяем все четыре, чтобы не смешать два источника
    UTM.forEach(function (k) {
      var v = (q.get(k) || '').trim().slice(0, 100);
      if (v) sessionStorage.setItem(k, v); else sessionStorage.removeItem(k);
    });
  } catch (e) { /* sessionStorage недоступен (приватный режим) — метки возьмёт form.js из адреса */ }
})();
