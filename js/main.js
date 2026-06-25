/* ============================================================
   SUPULIDE Russia — main.js
   ============================================================ */

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

/* --- Contact form --- */
(function () {
  var form = document.getElementById('contactForm');
  if (!form) return;
  var ok   = document.getElementById('formSuccess');
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (ok) { ok.style.display = 'block'; }
    form.reset();
    setTimeout(function () { if (ok) ok.style.display = 'none'; }, 6000);
  });
})();
