// Все вызовы gtag('event', ...) сайта находятся только в этом файле.
// Элементы описываются атрибутами: data-event="cta_click" data-button-name="hero_trial".
// Остальные скрипты (calc.js, form.js, pdd.js) вызывают window.track(), которая определена здесь.
// Имя, телефон и e-mail посетителя в GA4 не передаются.
(function () {
  var MAX_NAME = 40, MAX_VALUE = 100;

  window.track = function (name, params) {
    if (typeof gtag !== 'function') return;
    var clean = {};
    Object.keys(params || {}).forEach(function (k) {
      var v = params[k];
      clean[k.slice(0, MAX_NAME)] = typeof v === 'number' ? v : String(v).slice(0, MAX_VALUE);
    });
    gtag('event', String(name).slice(0, MAX_NAME), clean);
  };

  // data-button-name -> dataset.buttonName -> button_name
  function toSnake(s) { return s.replace(/[A-Z]/g, function (c) { return '_' + c.toLowerCase(); }); }

  document.addEventListener('click', function (e) {
    var el = e.target.closest('[data-event]');
    if (!el) return;
    var params = {};
    Object.keys(el.dataset).forEach(function (k) {
      if (k !== 'event') params[toSnake(k)] = el.dataset[k];
    });
    window.track(el.dataset.event, params);
  });
})();
