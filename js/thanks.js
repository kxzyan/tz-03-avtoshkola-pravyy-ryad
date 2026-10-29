// thanks.html: показывает номер отправленной заявки (его сохраняет form.js).
(function () {
  var id = null;
  try { id = sessionStorage.getItem('last_request_id'); } catch (e) {}
  document.getElementById('rid').textContent = id || 'номер появится после отправки формы';
})();
