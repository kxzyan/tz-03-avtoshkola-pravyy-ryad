// Переключатель филиалов (branches.html). Событие branch_select отправляет analytics.js по data-event.
(function () {
  var tabs = Array.prototype.slice.call(document.querySelectorAll('[data-branch-tab]'));

  function select(tab, focus) {
    tabs.forEach(function (t) {
      var on = t === tab;
      t.setAttribute('aria-selected', on);
      t.setAttribute('aria-pressed', on);
      t.tabIndex = on ? 0 : -1;
      document.getElementById(t.getAttribute('aria-controls')).hidden = !on;
    });
    if (focus) tab.focus();
  }

  tabs.forEach(function (t, n) {
    t.addEventListener('click', function () { select(t); });
    // стрелки влево/вправо переключают вкладки с клавиатуры
    t.addEventListener('keydown', function (e) {
      if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
      var next = tabs[(n + (e.key === 'ArrowRight' ? 1 : tabs.length - 1)) % tabs.length];
      next.click();
      next.focus();
    });
  });

  // branches.html#north открывает Северный филиал
  var start = tabs.filter(function (t) { return '#' + t.dataset.branchTab === location.hash; })[0] || tabs[0];
  select(start);
})();
