function changeCartQty(btn, delta) {
  const qtyEl = btn.parentElement.querySelector('.qty-val');
  let val = parseInt(qtyEl.textContent) + delta;
  if (val < 1) val = 1;
  qtyEl.textContent = val;
  updateCartTotal();
}

function removeItem(btn) {
  const item = btn.closest('.cart-item');
  item.style.opacity = '0';
  item.style.transition = 'opacity 0.3s';
  setTimeout(() => item.remove(), 300);
}

function updateCartTotal() {
  const items = document.querySelectorAll('.cart-item');
  let total = 0;
  items.forEach(item => {
    const price = parseFloat(item.querySelector('.cart-item-price').textContent.replace('$', ''));
    const qty = parseInt(item.querySelector('.qty-val').textContent);
    total += price * qty;
  });
  const totalEl = document.getElementById('cart-total');
  if (totalEl) totalEl.textContent = '$' + total.toFixed(2);
}
