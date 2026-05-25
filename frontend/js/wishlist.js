function removeWishItem(btn) {
  const card = btn.closest('.wishlist-card');
  card.style.opacity = '0';
  card.style.transform = 'scale(0.95)';
  card.style.transition = 'all 0.3s';
  setTimeout(() => {
    card.remove();
    updateWishlistCount();
  }, 300);
}

function updateWishlistCount() {
  const count = document.querySelectorAll('.wishlist-card').length;
  const el = document.querySelector('.wishlist-count');
  if (el) el.textContent = count + ' ITEMS SAVED';
}
