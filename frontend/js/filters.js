/* ============================================================
   BLVKOUT — Collections Filter Panel
   ============================================================ */
(function () {
  'use strict';

  const state = {
    category: 'ALL',
    sizes: new Set(),
    colors: new Set(),
    priceMin: 0,
    priceMax: 600,
    availability: 'all',   // all | instock | sale
    sort: 'featured',
  };

  /* ── open / close ─────────────────────────────────────────── */
  function openPanel() {
    document.getElementById('filterPanel').classList.add('open');
    document.getElementById('filterBackdrop').classList.add('open');
    document.body.style.overflow = 'hidden';
    syncUI();
  }

  function closePanel() {
    document.getElementById('filterPanel').classList.remove('open');
    document.getElementById('filterBackdrop').classList.remove('open');
    document.body.style.overflow = '';
  }

  /* ── sync UI to state ─────────────────────────────────────── */
  function syncUI() {
    // category pills
    document.querySelectorAll('.fp-cat-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.cat === state.category);
    });
    // sizes
    document.querySelectorAll('.fp-size-btn').forEach(btn => {
      btn.classList.toggle('active', state.sizes.has(btn.dataset.size));
    });
    // colors
    document.querySelectorAll('.fp-color-btn').forEach(btn => {
      btn.classList.toggle('active', state.colors.has(btn.dataset.color));
    });
    // price
    const minEl = document.getElementById('fpPriceMin');
    const maxEl = document.getElementById('fpPriceMax');
    if (minEl) minEl.value = state.priceMin;
    if (maxEl) maxEl.value = state.priceMax;
    updatePriceTrack();
    // availability
    document.querySelectorAll('.fp-avail-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.avail === state.availability);
    });
    // sort
    const sortEl = document.getElementById('fpSort');
    if (sortEl) sortEl.value = state.sort;
    // badge
    updateBadge();
  }

  /* ── price range track fill ───────────────────────────────── */
  function updatePriceTrack() {
    const track = document.getElementById('fpPriceTrack');
    if (!track) return;
    const min = state.priceMin, max = state.priceMax, total = 600;
    const left  = (min / total) * 100;
    const right = 100 - (max / total) * 100;
    track.style.left  = left  + '%';
    track.style.right = right + '%';
    const minLbl = document.getElementById('fpPriceMinLbl');
    const maxLbl = document.getElementById('fpPriceMaxLbl');
    if (minLbl) minLbl.textContent = '$' + min;
    if (maxLbl) maxLbl.textContent = max >= 600 ? '$600+' : '$' + max;
  }

  /* ── active filter count badge ────────────────────────────── */
  function updateBadge() {
    let count = 0;
    if (state.category !== 'ALL') count++;
    count += state.sizes.size;
    count += state.colors.size;
    if (state.priceMin > 0 || state.priceMax < 600) count++;
    if (state.availability !== 'all') count++;
    if (state.sort !== 'featured') count++;

    const badge = document.getElementById('filterBadge');
    if (!badge) return;
    badge.textContent = count;
    badge.style.display = count > 0 ? 'flex' : 'none';

    // also update result count label
    applyFilters();
  }

  /* ── apply filters to product cards ──────────────────────── */
  function applyFilters() {
    const cards = document.querySelectorAll('.product-card[data-category]');
    let visible = 0;
    cards.forEach(card => {
      const cat   = card.dataset.category || 'ALL';
      const price = parseFloat(card.dataset.price || 0);
      const avail = card.dataset.avail || 'instock';
      const sizes = (card.dataset.sizes || '').split(',');
      const colors = (card.dataset.colors || '').split(',');

      let show = true;
      if (state.category !== 'ALL' && cat !== state.category) show = false;
      if (price < state.priceMin || price > state.priceMax) show = false;
      if (state.availability === 'instock' && avail === 'soldout') show = false;
      if (state.availability === 'sale' && avail !== 'sale') show = false;
      if (state.sizes.size > 0 && !sizes.some(s => state.sizes.has(s))) show = false;
      if (state.colors.size > 0 && !colors.some(c => state.colors.has(c))) show = false;

      card.style.display = show ? '' : 'none';
      if (show) visible++;
    });

    const countEl = document.getElementById('fpResultCount');
    if (countEl) countEl.textContent = visible + ' ITEM' + (visible !== 1 ? 'S' : '');
  }

  /* ── reset ────────────────────────────────────────────────── */
  function resetFilters() {
    state.category = 'ALL';
    state.sizes.clear();
    state.colors.clear();
    state.priceMin = 0;
    state.priceMax = 600;
    state.availability = 'all';
    state.sort = 'featured';
    syncUI();
    applyFilters();
  }

  /* ── event wiring (called once DOM is ready) ──────────────── */
  function wire() {
    // Category pills
    document.querySelectorAll('.fp-cat-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        state.category = btn.dataset.cat;
        syncUI();
      });
    });

    // Size toggles
    document.querySelectorAll('.fp-size-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const s = btn.dataset.size;
        state.sizes.has(s) ? state.sizes.delete(s) : state.sizes.add(s);
        syncUI();
      });
    });

    // Color toggles
    document.querySelectorAll('.fp-color-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const c = btn.dataset.color;
        state.colors.has(c) ? state.colors.delete(c) : state.colors.add(c);
        // update label
        const lbl = document.getElementById('fpColorLabel');
        if (lbl) {
          const selected = [...state.colors];
          lbl.textContent = selected.length ? selected.map(s => s.charAt(0).toUpperCase() + s.slice(1)).join(', ') : 'Select a color';
        }
        syncUI();
      });
    });

    // Price range sliders
    const minSlider = document.getElementById('fpPriceMin');
    const maxSlider = document.getElementById('fpPriceMax');
    if (minSlider) {
      minSlider.addEventListener('input', () => {
        state.priceMin = Math.min(parseInt(minSlider.value), state.priceMax - 20);
        minSlider.value = state.priceMin;
        updatePriceTrack();
        updateBadge();
      });
    }
    if (maxSlider) {
      maxSlider.addEventListener('input', () => {
        state.priceMax = Math.max(parseInt(maxSlider.value), state.priceMin + 20);
        maxSlider.value = state.priceMax;
        updatePriceTrack();
        updateBadge();
      });
    }

    // Availability
    document.querySelectorAll('.fp-avail-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        state.availability = btn.dataset.avail;
        syncUI();
      });
    });

    // Sort
    const sortEl = document.getElementById('fpSort');
    if (sortEl) {
      sortEl.addEventListener('change', () => {
        state.sort = sortEl.value;
        updateBadge();
      });
    }

    // Reset
    const resetBtn = document.getElementById('fpResetBtn');
    if (resetBtn) resetBtn.addEventListener('click', resetFilters);

    // Apply / close
    const applyBtn = document.getElementById('fpApplyBtn');
    if (applyBtn) applyBtn.addEventListener('click', closePanel);

    // Backdrop
    const backdrop = document.getElementById('filterBackdrop');
    if (backdrop) backdrop.addEventListener('click', closePanel);

    // Existing category filter buttons in header — sync with panel
    document.querySelectorAll('.collections-filters .filter-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const cat = btn.textContent.trim();
        state.category = cat;
        syncUI();
      });
    });

    // Section accordion toggles
    document.querySelectorAll('.fp-section-toggle').forEach(toggle => {
      toggle.addEventListener('click', () => {
        const section = toggle.closest('.fp-section');
        section.classList.toggle('collapsed');
      });
    });
  }

  document.addEventListener('DOMContentLoaded', wire);

  window.filterPanel = { open: openPanel, close: closePanel, reset: resetFilters };
})();
