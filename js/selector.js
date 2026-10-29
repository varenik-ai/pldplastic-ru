/* Подбор марки по параметрам: данные из data/grades.{ru,en}.json (собираются из таблиц страниц продуктов, tools/build_grades.py) */
(function () {
  var root = document.getElementById('selector');
  if (!root) return;
  var en = root.getAttribute('data-lang') === 'en';
  var L = en ? {
    product: 'Polymer', brand: 'Trade name', search: 'Grade / keyword', any: 'Any', from: 'from', to: 'to',
    found: 'Grades found: ', none: 'Nothing matches these filters. Widen the ranges or ask us for an equivalent.',
    pick: 'Choose a polymer to see its grades.', req: 'Request price', page: 'Product page', more: 'Showing first ',
    reset: 'Reset filters', grade: 'Grade', ask: 'Need a different grade or an equivalent? Write to us and we will match it.'
  } : {
    product: 'Полимер', brand: 'Торговая марка', search: 'Марка / слово', any: 'Любая', from: 'от', to: 'до',
    found: 'Найдено марок: ', none: 'По этим условиям ничего не найдено. Расширьте диапазоны или напишите — подберём эквивалент.',
    pick: 'Выберите полимер, чтобы увидеть марки.', req: 'Запросить цену', page: 'Страница продукта', more: 'Показаны первые ',
    reset: 'Сбросить', grade: 'Марка', ask: 'Нужна другая марка или эквивалент? Напишите — подберём.'
  };
  var LIMIT = 150;
  var data = null, cur = null, tracked = false;

  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function track(name) { if (window.trackEvent) trackEvent(name); }

  function build() {
    var opts = data.products.map(function (p) {
      return '<option value="' + esc(p.id) + '">' + esc(p.name) + ' (' + p.grades.length + ')</option>';
    }).join('');
    root.innerHTML =
      '<div class="sel-row">' +
      '<label>' + L.product + '<select id="selProduct"><option value="">—</option>' + opts + '</select></label>' +
      '<label>' + L.brand + '<select id="selBrand"><option value="">' + L.any + '</option></select></label>' +
      '<label>' + L.search + '<input id="selText" type="text" autocomplete="off"></label>' +
      '</div><div id="selFilters" class="sel-row"></div><div id="selOut" class="sel-out"><p class="sel-hint">' + L.pick + '</p></div>';
    var q = new URLSearchParams(location.search).get('p');
    var sp = document.getElementById('selProduct');
    if (q && data.products.some(function (p) { return p.id === q; })) sp.value = q;
    sp.addEventListener('change', function () { touch(); pickProduct(sp.value); });
    document.getElementById('selBrand').addEventListener('change', function () { touch(); render(); });
    document.getElementById('selText').addEventListener('input', function () { touch(); render(); });
    if (sp.value) pickProduct(sp.value);
  }

  function touch() { if (!tracked) { tracked = true; track('selector_use'); } }

  function numericLabels(p) {
    var labels = Object.keys(p.grades[0].props);
    return labels.filter(function (k) {
      var n = p.grades.filter(function (g) { return g.num[k] !== null && g.num[k] !== undefined; }).length;
      return n / p.grades.length >= 0.6;
    });
  }

  function pickProduct(id) {
    cur = data.products.filter(function (p) { return p.id === id; })[0] || null;
    var br = document.getElementById('selBrand');
    var fl = document.getElementById('selFilters');
    br.innerHTML = '<option value="">' + L.any + '</option>';
    fl.innerHTML = '';
    if (!cur) { render(); return; }
    var brands = {};
    cur.grades.forEach(function (g) { brands[g.brand] = 1; });
    Object.keys(brands).sort().forEach(function (b) { br.innerHTML += '<option value="' + esc(b) + '">' + esc(b) + '</option>'; });
    cur.nl = numericLabels(cur);
    cur.nl.forEach(function (k, i) {
      var vals = cur.grades.map(function (g) { return g.num[k]; }).filter(function (v) { return v !== null && v !== undefined; });
      var mn = Math.min.apply(null, vals), mx = Math.max.apply(null, vals);
      fl.innerHTML += '<div class="sel-range"><span>' + esc(k) + '</span>' +
        '<input type="number" step="any" data-k="' + i + '" data-b="min" placeholder="' + L.from + ' ' + mn + '">' +
        '<input type="number" step="any" data-k="' + i + '" data-b="max" placeholder="' + L.to + ' ' + mx + '"></div>';
    });
    fl.querySelectorAll('input').forEach(function (el) { el.addEventListener('input', function () { touch(); render(); }); });
    render();
  }

  function render() {
    var out = document.getElementById('selOut');
    if (!cur) { out.innerHTML = '<p class="sel-hint">' + L.pick + '</p>'; return; }
    var brand = document.getElementById('selBrand').value;
    var text = document.getElementById('selText').value.trim().toLowerCase();
    var rng = {};
    document.querySelectorAll('#selFilters input').forEach(function (el) {
      if (el.value === '') return;
      var k = cur.nl[+el.getAttribute('data-k')];
      rng[k] = rng[k] || {};
      rng[k][el.getAttribute('data-b')] = parseFloat(el.value);
    });
    var rows = cur.grades.filter(function (g) {
      if (brand && g.brand !== brand) return false;
      if (text && (g.grade + ' ' + g.brand).toLowerCase().indexOf(text) < 0) return false;
      for (var k in rng) {
        var v = g.num[k];
        if (v === null || v === undefined) return false;
        if (rng[k].min !== undefined && v < rng[k].min) return false;
        if (rng[k].max !== undefined && v > rng[k].max) return false;
      }
      return true;
    });
    var labels = Object.keys(cur.grades[0].props);
    var head = '<th>' + L.brand + '</th><th>' + L.grade + '</th>' + labels.map(function (k) { return '<th>' + esc(k) + '</th>'; }).join('') + '<th></th>';
    var body = rows.slice(0, LIMIT).map(function (g) {
      var href = 'contact.html?product=' + encodeURIComponent(cur.name) + '&grade=' + encodeURIComponent(g.brand + ' ' + g.grade) + '#contact-form';
      return '<tr><td>' + esc(g.brand) + '</td><td><b>' + esc(g.grade) + '</b></td>' +
        labels.map(function (k) { return '<td>' + esc(g.props[k]) + '</td>'; }).join('') +
        '<td><a class="sel-btn" data-sel="1" href="' + href + '">' + L.req + '</a></td></tr>';
    }).join('');
    out.innerHTML = '<div class="sel-count">' + L.found + rows.length + ' · <a href="' + esc(cur.url) + '">' + L.page + ' ' + esc(cur.name) + '</a></div>' +
      (rows.length ? '<div class="sel-scroll"><table class="sel-table"><thead><tr>' + head + '</tr></thead><tbody>' + body + '</tbody></table></div>' +
        (rows.length > LIMIT ? '<p class="sel-hint">' + L.more + LIMIT + '</p>' : '') : '<p class="sel-hint">' + L.none + '</p>') +
      '<p class="sel-ask">' + L.ask + ' <a href="contact.html#contact-form">' + L.req + '</a></p>';
    out.querySelectorAll('a[data-sel]').forEach(function (a) { a.addEventListener('click', function () { track('selector_request'); }); });
  }

  fetch(root.getAttribute('data-src')).then(function (r) { return r.json(); }).then(function (d) { data = d; build(); })
    .catch(function () { root.innerHTML = '<p class="sel-hint">…</p>'; });
})();
