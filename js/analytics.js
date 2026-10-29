// Все вызовы gtag('event', ...) находятся только здесь.
// Элементы описываются атрибутами: data-event="cta_click" data-button-name="hero_trial".
window.track = function (name, params) {
  if (typeof gtag === 'function') gtag('event', name, params || {});
};
// data-button-name -> button_name
function toSnake(s) { return s.replace(/[A-Z]/g, function (c) { return '_' + c.toLowerCase(); }); }
document.addEventListener('click', function (e) {
  var el = e.target.closest('[data-event]');
  if (!el) return;
  var params = {};
  Object.keys(el.dataset).forEach(function (k) {
    if (k !== 'event') params[toSnake(k)] = String(el.dataset[k]).slice(0, 100);
  });
  window.track(el.dataset.event, params);
});
