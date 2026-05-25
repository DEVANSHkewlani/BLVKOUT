function changeQty(delta) {
  const el = document.getElementById('qty');
  let val = parseInt(el.textContent) + delta;
  if (val < 1) val = 1;
  el.textContent = val;
}

// Size buttons
document.querySelectorAll('.size-btn').forEach(btn => {
  btn.addEventListener('click', function () {
    document.querySelectorAll('.size-btn').forEach(b => b.classList.remove('active'));
    this.classList.add('active');
  });
});

// Color buttons
document.querySelectorAll('.color-btn').forEach(btn => {
  btn.addEventListener('click', function () {
    document.querySelectorAll('.color-btn').forEach(b => b.classList.remove('active'));
    this.classList.add('active');
  });
});

// ── COMPLETE THE FIT ──────────────────────────────────────────────
// Reads fit data from localStorage (set by admin panel)
// Key: 'blvk_fits' → { [productSku]: [ {name, price, category, bg}, ... ] }
// For demo, we seed a default fit if none exists yet.

(function() {
  var FITS_KEY = 'blvk_fits';
  var CURRENT_SKU = 'BLV-MH-002'; // this product's SKU

  // Seed demo fit data if nothing saved yet
  function seedDemoFit() {
    var fits = JSON.parse(localStorage.getItem(FITS_KEY) || '{}');
    if (!fits[CURRENT_SKU]) {
      fits[CURRENT_SKU] = [
        { name: 'FRAGMENT PANTS',    price: 195, category: 'BOTTOMS',     bg: '#2a2a2a' },
        { name: 'PHANTOM BOOTS',     price: 280, category: 'FOOTWEAR',    bg: '#1a1a1a' },
        { name: 'VOID TURTLENECK',   price: 130, category: 'TOPS',        bg: '#333' }
      ];
      localStorage.setItem(FITS_KEY, JSON.stringify(fits));
    }
  }

  function renderFit() {
    seedDemoFit();
    var fits = JSON.parse(localStorage.getItem(FITS_KEY) || '{}');
    var fitItems = fits[CURRENT_SKU];
    if (!fitItems || fitItems.length === 0) return;

    var section = document.getElementById('completeFitSection');
    var piecesEl = document.getElementById('fitPieces');
    var totalEl  = document.getElementById('fitTotalPrice');
    if (!section || !piecesEl) return;

    section.style.display = '';

    var anchorPrice = 185; // this product's price
    var total = anchorPrice;

    piecesEl.innerHTML = '';
    fitItems.forEach(function(item) {
      total += item.price;
      var div = document.createElement('div');
      div.className = 'fit-piece';
      div.innerHTML =
        '<div class="fit-piece-img"><div class="img-placeholder" style="background:' + item.bg + ';height:100%;"></div></div>' +
        '<div class="fit-piece-category">' + item.category + '</div>' +
        '<div class="fit-piece-name">' + item.name + '</div>' +
        '<div class="fit-piece-price">$' + item.price.toFixed(2) + '</div>' +
        '<button class="fit-piece-add" onclick="window.showToast(\'✓ Added to cart\')">+ ADD TO CART</button>';
      div.addEventListener('click', function(e) {
        if (e.target.classList.contains('fit-piece-add')) return;
        location.href = 'product.html';
      });
      piecesEl.appendChild(div);
    });

    totalEl.textContent = '$' + total.toFixed(2);
  }

  // Add full fit to cart
  var addFitBtn = document.getElementById('addFitToCart');
  if (addFitBtn) {
    addFitBtn.addEventListener('click', function() {
      window.showToast && window.showToast('✓ Full fit added to cart');
    });
  }

  renderFit();
})();
