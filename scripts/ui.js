/* ============================================
   BLVKOUT — UI / Aesthetic JS
   ============================================ */

// ---- SCROLL PROGRESS ----
const progressBar = document.getElementById('scrollProgress');
if (progressBar) {
  window.addEventListener('scroll', () => {
    const pct = (window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100;
    progressBar.style.width = pct + '%';
  }, { passive: true });
}

// ---- SCROLL TO TOP ----
const scrollTopBtn = document.getElementById('scrollTop');
if (scrollTopBtn) {
  window.addEventListener('scroll', () => {
    scrollTopBtn.classList.toggle('visible', window.scrollY > 400);
  }, { passive: true });
}

// ---- CUSTOM CURSOR (dot only, no ring) ----
const dot  = document.getElementById('cursorDot');
const ring = document.getElementById('cursorRing');

// Always hide the ring
if (ring) ring.style.display = 'none';

if (dot && window.matchMedia('(pointer:fine)').matches) {
  document.addEventListener('mousemove', e => {
    dot.style.left = e.clientX + 'px';
    dot.style.top  = e.clientY + 'px';
  });

  document.querySelectorAll('a, button, .product-card, .print-lib-item').forEach(el => {
    el.addEventListener('mouseenter', () => {
      dot.style.width  = '12px';
      dot.style.height = '12px';
    });
    el.addEventListener('mouseleave', () => {
      dot.style.width  = '8px';
      dot.style.height = '8px';
    });
  });
} else {
  if (dot) dot.style.display = 'none';
}

// ---- HAMBURGER / MOBILE DRAWER ----
const hamburger = document.getElementById('hamburger');
const navDrawer = document.getElementById('navDrawer');

if (hamburger && navDrawer) {
  hamburger.addEventListener('click', () => {
    const open = hamburger.classList.toggle('open');
    navDrawer.classList.toggle('open', open);
    document.body.style.overflow = open ? 'hidden' : '';
  });

  // Close on link click
  navDrawer.querySelectorAll('a').forEach(a => {
    a.addEventListener('click', () => {
      hamburger.classList.remove('open');
      navDrawer.classList.remove('open');
      document.body.style.overflow = '';
    });
  });
}

// ---- SCROLL REVEAL ----
const reveals = document.querySelectorAll('.reveal');
if (reveals.length) {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('visible');
        observer.unobserve(e.target);
      }
    });
  }, { threshold: 0.1 });

  reveals.forEach(el => observer.observe(el));
}

// ---- TOAST HELPER ----
window.showToast = function(msg, duration = 2800) {
  const t = document.getElementById('toast');
  if (!t) return;
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), duration);
};

// ---- ADD TO CART TOAST ----
document.querySelectorAll('.btn-blue').forEach(btn => {
  if (btn.textContent.includes('ADD TO CART') || btn.textContent.includes('ADD TO BAG')) {
    btn.addEventListener('click', () => {
      btn.classList.add('loading');
      setTimeout(() => {
        btn.classList.remove('loading');
        window.showToast('✓  Added to cart');
      }, 900);
    });
  }
});

// ---- WISHLIST TOAST ----
document.querySelectorAll('.btn-outline').forEach(btn => {
  if (btn.textContent.trim() === '♡') {
    btn.addEventListener('click', () => {
      btn.textContent = '♥';
      btn.style.color = 'var(--blue)';
      btn.style.borderColor = 'var(--blue)';
      window.showToast('♥  Saved to wishlist');
    });
  }
});
