/* ============================================================
   SUPULIDE Russia — main.js
   ============================================================ */

/* --- WeChat: копировать ID + toast + открыть на мобиле --- */
(function () {
  var WX_ID = 'Leo_Li81';

  function showToast() {
    var toast = document.getElementById('wechat-toast');
    if (!toast) {
      toast = document.createElement('div');
      toast.id = 'wechat-toast';
      toast.innerHTML = '<i class="fab fa-weixin"></i>&nbsp;WeChat ID скопирован: <strong>' + WX_ID + '</strong>';
      document.body.appendChild(toast);
    }
    toast.classList.add('show');
    clearTimeout(toast._t);
    toast._t = setTimeout(function () { toast.classList.remove('show'); }, 3000);
  }

  window.handleWechat = function (e) {
    e.preventDefault();
    // Копируем в буфер
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(WX_ID).then(showToast).catch(showToast);
    } else {
      var el = document.createElement('textarea');
      el.value = WX_ID;
      el.style.position = 'fixed'; el.style.opacity = '0';
      document.body.appendChild(el);
      el.focus(); el.select();
      try { document.execCommand('copy'); } catch (err) {}
      document.body.removeChild(el);
      showToast();
    }
    // На мобиле дополнительно пробуем открыть WeChat
    if (/mobile|android|iphone|ipad/i.test(navigator.userAgent)) {
      setTimeout(function () { window.location.href = 'weixin://dl/chat?' + WX_ID; }, 200);
    }
  };
})();

/* --- Dropdown toggle (стрелка отдельно от ссылки) --- */
(function () {
  document.addEventListener('click', function (e) {
    var btn = e.target.closest('.dd-toggle');
    if (btn) {
      e.stopPropagation();
      var li = btn.closest('li');
      var isOpen = li.classList.contains('dd-open');
      // Закрываем все открытые дропдауны
      document.querySelectorAll('.main-nav li.dd-open').forEach(function (el) {
        el.classList.remove('dd-open');
      });
      if (!isOpen) li.classList.add('dd-open');
      return;
    }
    // Клик вне nav — закрываем всё
    if (!e.target.closest('.main-nav')) {
      document.querySelectorAll('.main-nav li.dd-open').forEach(function (el) {
        el.classList.remove('dd-open');
      });
    }
  });
})();

/* --- Mobile burger menu --- */
(function () {
  var burger = document.getElementById('burger');
  var nav    = document.getElementById('mainNav');
  if (!burger || !nav) return;
  burger.addEventListener('click', function () {
    nav.classList.toggle('open');
    var s = burger.querySelectorAll('span');
    if (nav.classList.contains('open')) {
      s[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
      s[1].style.opacity   = '0';
      s[2].style.transform = 'rotate(-45deg) translate(5px, -5px)';
    } else {
      s[0].style.transform = s[2].style.transform = '';
      s[1].style.opacity   = '';
    }
  });
  document.addEventListener('click', function (e) {
    if (!nav.contains(e.target) && !burger.contains(e.target)) {
      nav.classList.remove('open');
      var s = burger.querySelectorAll('span');
      s[0].style.transform = s[2].style.transform = '';
      s[1].style.opacity = '';
    }
  });
})();

/* --- Hero slider --- */
(function () {
  var slides = document.querySelectorAll('.hero-slide');
  var dots   = document.querySelectorAll('.hero-dot');
  if (!slides.length) return;
  var cur = 0;
  var timer;

  function goTo(n) {
    slides[cur].classList.remove('active');
    if (dots[cur]) dots[cur].classList.remove('active');
    cur = (n + slides.length) % slides.length;
    slides[cur].classList.add('active');
    if (dots[cur]) dots[cur].classList.add('active');
  }

  function next() { goTo(cur + 1); }
  function prev() { goTo(cur - 1); }

  function startAuto() { timer = setInterval(next, 5000); }
  function resetAuto()  { clearInterval(timer); startAuto(); }

  var btnL = document.querySelector('.hero-arrow-left');
  var btnR = document.querySelector('.hero-arrow-right');
  if (btnL) btnL.addEventListener('click', function () { prev(); resetAuto(); });
  if (btnR) btnR.addEventListener('click', function () { next(); resetAuto(); });

  dots.forEach(function (d, i) {
    d.addEventListener('click', function () { goTo(i); resetAuto(); });
  });

  // Touch swipe
  var touchX = null;
  var hero = document.querySelector('.hero');
  if (hero) {
    hero.addEventListener('touchstart', function (e) { touchX = e.touches[0].clientX; }, { passive: true });
    hero.addEventListener('touchend', function (e) {
      if (touchX === null) return;
      var dx = e.changedTouches[0].clientX - touchX;
      if (Math.abs(dx) > 40) { dx < 0 ? next() : prev(); resetAuto(); }
      touchX = null;
    }, { passive: true });
  }

  goTo(0);
  startAuto();
})();

/* --- Applications carousel --- */
(function () {
  var track = document.querySelector('.apps-track');
  if (!track) return;
  var cards = track.querySelectorAll('.app-card');
  if (!cards.length) return;

  var perView = window.innerWidth >= 900 ? 4 : window.innerWidth >= 550 ? 2 : 1;
  var total   = cards.length;
  var maxIdx  = Math.max(0, total - perView);
  var idx     = 0;

  function slide(n) {
    idx = Math.max(0, Math.min(maxIdx, n));
    var pct = (100 + 20) / perView; // approx card+gap
    track.style.transform = 'translateX(-' + (idx * (100 / perView)) + '%)';
    // simpler: use px
    var cardW = cards[0].offsetWidth + 20;
    track.style.transform = 'translateX(-' + (idx * cardW) + 'px)';
  }

  var btnP = document.querySelector('.apps-prev');
  var btnN = document.querySelector('.apps-next');
  if (btnP) btnP.addEventListener('click', function () { slide(idx - perView); });
  if (btnN) btnN.addEventListener('click', function () { slide(idx + perView); });
})();

/* --- Scroll counter animation --- */
(function () {
  function animateCount(el, target, suffix) {
    var start = 0;
    var step = Math.max(1, Math.ceil(target / 80));
    var id = setInterval(function () {
      start = Math.min(start + step, target);
      el.textContent = start + suffix;
      if (start >= target) clearInterval(id);
    }, 16);
  }

  var obs = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      var el  = e.target;
      var txt = el.getAttribute('data-target') || el.textContent;
      var num = parseInt(txt.replace(/\D/g, ''), 10);
      var suf = txt.replace(/\d/g, '');
      if (!isNaN(num)) animateCount(el, num, suf);
      obs.unobserve(el);
    });
  }, { threshold: 0.5 });

  document.querySelectorAll('.stat-num').forEach(function (el) { obs.observe(el); });
})();

/* --- Fade-up on scroll --- */
(function () {
  var style = document.createElement('style');
  style.textContent = '.fade-up{opacity:0;transform:translateY(28px);transition:opacity .6s ease,transform .6s ease}.fade-up.visible{opacity:1;transform:none}';
  document.head.appendChild(style);

  document.querySelectorAll('.app-card,.news-big-card,.news-small-card,.adv-card,.stat-box').forEach(function (el) {
    el.classList.add('fade-up');
  });

  function check() {
    document.querySelectorAll('.fade-up:not(.visible)').forEach(function (el) {
      if (el.getBoundingClientRect().top < window.innerHeight - 50) el.classList.add('visible');
    });
  }
  window.addEventListener('scroll', check, { passive: true });
  check();
})();

/* --- Contact form (fallback only — skip if Web3Forms inline handler present) --- */
(function () {
  var form = document.getElementById('contactForm');
  if (!form) return;
  /* If form has Web3Forms access_key — it has its own handler, don't interfere */
  if (form.querySelector('[name="access_key"]')) return;
  var ok   = document.getElementById('formSuccess');
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (ok) { ok.style.display = 'block'; }
    form.reset();
    setTimeout(function () { if (ok) ok.style.display = 'none'; }, 6000);
  });
})();

/* --- Аналитика: события GA4 + Яндекс.Метрика --- */
window.trackEvent = function (name, goal) {
  try { if (window.gtag) gtag('event', name, { page_location: location.href }); } catch (e) {}
  try { if (window.ym) ym(111389593, 'reachGoal', goal || name); } catch (e) {}
};
document.addEventListener('click', function (e) {
  var a = e.target.closest && e.target.closest('a');
  if (!a) return;
  var href = a.getAttribute('href') || '';
  if (href.indexOf('mailto:') === 0) trackEvent('click_email');
  else if (href.indexOf('tel:') === 0) trackEvent('click_phone');
  else if (/fn-social-wechat|float-wechat/.test(a.className)) trackEvent('click_wechat');
  else if (/float-telegram/.test(a.className)) trackEvent('click_telegram');
  else if (/float-whatsapp/.test(a.className)) trackEvent('click_whatsapp');
  else if (/\.pdf($|\?)/i.test(href)) trackEvent('download_doc');
});

/* --- Форма запроса КП на страницах продуктов: отправка через Web3Forms (как на contact.html) --- */
(function () {
  var form = document.querySelector('.proddet-form form');
  if (!form) return;
  var en = (document.documentElement.lang || '').toLowerCase().indexOf('en') === 0;
  var T = en
    ? { sending: 'Sending…', send: 'Send Request', ok: 'Thank you! We have received your request and will reply within 24 hours.', errNet: 'Network error. Please write to export@pldpolymer.com', err: 'Error: ' }
    : { sending: 'Отправляем…', send: 'Отправить запрос', ok: 'Спасибо! Ваш запрос получен. Мы ответим в течение 24 часов.', errNet: 'Ошибка сети. Напишите нам на export@pldpolymer.com', err: 'Ошибка: ' };
  var btn = form.querySelector('button[type="submit"]');
  var btnHtml = btn ? btn.innerHTML : '';
  /* Поля для квалификации запроса: объём, страна, нужен ли TDS/COA/образец */
  if (btn && !form.querySelector('[name="volume"]')) {
    var extra = document.createElement('div');
    extra.className = 'form-row';
    extra.innerHTML = en
      ? '<input type="text" name="volume" placeholder="Volume, t/month"><input type="text" name="country" placeholder="Country of delivery">'
      : '<input type="text" name="volume" placeholder="Объём, т/мес"><input type="text" name="country" placeholder="Страна / город поставки">';
    var docs = document.createElement('label');
    docs.style.cssText = 'display:block;margin:8px 0 12px;font-size:14px;cursor:pointer';
    docs.innerHTML = '<input type="checkbox" name="need_docs" value="' + (en ? 'Yes' : 'Да') + '" style="margin-right:8px">'
      + (en ? 'I need TDS / COA / a test sample' : 'Нужны TDS / COA / образец для испытаний');
    btn.parentNode.insertBefore(extra, btn);
    btn.parentNode.insertBefore(docs, btn);
  }
  function key(el) {
    if (el.name) return el.name;
    if (el.tagName === 'TEXTAREA') return 'message';
    if (el.type === 'email') return 'email';
    if (el.type === 'tel' || /тел|phone|whats/i.test(el.placeholder || '')) return 'phone';
    return el.placeholder || 'field';
  }
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var h1 = document.querySelector('h1');
    var product = h1 ? h1.textContent.replace(/\s+/g, ' ').trim() : document.title;
    var data = {
      access_key: 'c44e2f6b-8071-42af-947a-a1ea99ed12dc',
      subject: (en ? 'Quote request: ' : 'Запрос КП: ') + product,
      from_name: 'SUPULIDE Website',
      page_url: location.href,
      product: product
    };
    Array.prototype.forEach.call(form.elements, function (el) {
      if (el.tagName === 'BUTTON' || el.type === 'hidden' || !el.value) return;
      if (el.type === 'checkbox' && !el.checked) return;
      data[key(el)] = el.value;
    });
    if (btn) { btn.disabled = true; btn.textContent = T.sending; }
    fetch('https://api.web3forms.com/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: JSON.stringify(data)
    }).then(function (r) { return r.json(); }).then(function (res) {
      if (res.success) {
        if (window.trackEvent) trackEvent('form_submit');
        form.innerHTML = '<p style="text-align:center;font-size:18px;padding:32px 0">' + T.ok + '</p>';
      } else {
        if (btn) { btn.disabled = false; btn.innerHTML = btnHtml; }
        alert(T.err + (res.message || ''));
      }
    }).catch(function () {
      if (btn) { btn.disabled = false; btn.innerHTML = btnHtml; }
      alert(T.errNet);
    });
  });
})();

/* --- Контакты для кнопок связи ---
   Заполните нужные поля — кнопки появятся на всех страницах (боковая панель).
   phone: '+7 495 000-00-00' | telegram: 'username' или полная ссылка | whatsapp: '79990000000' (цифры, с кодом страны) */
window.SITE_CONTACTS = { phone: '', telegram: '', whatsapp: '' };

(function () {
  var c = window.SITE_CONTACTS || {};
  var bar = document.querySelector('.float-sidebar');
  if (!bar) return;
  var en = (document.documentElement.lang || '').toLowerCase().indexOf('en') === 0;
  function add(cls, href, icon, label, title, external) {
    var a = document.createElement('a');
    a.href = href;
    a.className = 'float-btn ' + cls;
    a.title = title;
    if (external) { a.target = '_blank'; a.rel = 'noopener nofollow'; }
    a.innerHTML = '<i class="' + icon + '"></i><span class="float-label">' + label + '</span>';
    bar.insertBefore(a, bar.firstChild);
  }
  if (c.phone) {
    var tel = String(c.phone).replace(/[^\d+]/g, '');
    add('float-phone', 'tel:' + tel, 'fas fa-phone', en ? 'Call' : 'Позвонить', c.phone, false);
  }
  if (c.whatsapp) {
    add('float-whatsapp', 'https://wa.me/' + String(c.whatsapp).replace(/\D/g, ''), 'fab fa-whatsapp', 'WhatsApp', 'WhatsApp', true);
  }
  if (c.telegram) {
    var t = String(c.telegram);
    add('float-telegram', /^https?:/.test(t) ? t : 'https://t.me/' + t.replace(/^@/, ''), 'fab fa-telegram-plane', 'Telegram', 'Telegram', true);
  }
})();

/* --- Предзаполнение формы на contact.html из ссылки (?product=…&grade=…), например из «Подбора марки» --- */
(function () {
  var form = document.getElementById('contactForm');
  if (!form) return;
  var q = new URLSearchParams(location.search);
  var product = (q.get('product') || '').slice(0, 80);
  var grade = (q.get('grade') || '').slice(0, 120);
  var ta = form.querySelector('textarea');
  if (!ta || ta.value || (!product && !grade)) return;
  var en = (document.documentElement.lang || '').toLowerCase().indexOf('en') === 0;
  ta.value = (en ? 'Request for: ' : 'Запрос по марке: ') + [product, grade].filter(Boolean).join(' — ') + '\n';
})();
