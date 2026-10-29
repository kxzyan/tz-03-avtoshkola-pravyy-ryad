// Фильтр МКПП / АКПП / мотоцикл и раскрытие карточек (instructors.html).
// Событие instructor_view отправляет analytics.js по атрибутам data-event у кнопок фильтра и «Подробнее».
(function () {
  var cards = document.querySelectorAll('.inst-card');
  var count = document.getElementById('ins-count');

  function word(n) { return n === 1 ? 'карточка' : n > 1 && n < 5 ? 'карточки' : 'карточек'; }

  document.querySelectorAll('[data-filter]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var f = btn.dataset.filter, shown = 0;
      document.querySelectorAll('[data-filter]').forEach(function (b) { b.setAttribute('aria-pressed', b === btn); });
      cards.forEach(function (c) {
        var on = f === 'all' || c.dataset.gear === f;
        c.hidden = !on;
        if (on) shown++;
      });
      count.textContent = 'Показано: ' + shown + ' ' + word(shown);
    });
  });

  document.querySelectorAll('.more-btn').forEach(function (b) {
    b.addEventListener('click', function () {
      var open = b.getAttribute('aria-expanded') !== 'true';
      b.setAttribute('aria-expanded', open);
      b.textContent = open ? 'Скрыть' : 'Подробнее';
      document.getElementById(b.getAttribute('aria-controls')).hidden = !open;
    });
  });
})();
