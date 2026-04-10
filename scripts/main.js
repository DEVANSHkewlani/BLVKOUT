// Filter buttons
document.querySelectorAll('.filter-btn').forEach(btn => {
  btn.addEventListener('click', function () {
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    this.classList.add('active');
  });
});

// Thumb gallery
document.querySelectorAll('.thumb').forEach(thumb => {
  thumb.addEventListener('click', function () {
    document.querySelectorAll('.thumb').forEach(t => t.classList.remove('active'));
    this.classList.add('active');
  });
});

// Profile nav
document.querySelectorAll('.profile-nav-item').forEach(item => {
  item.addEventListener('click', function (e) {
    document.querySelectorAll('.profile-nav-item').forEach(i => i.classList.remove('active'));
    this.classList.add('active');
  });
});

// ---- CAROUSEL ----
const carouselState = {};

function scrollCarousel(id, dir) {
  const track = document.getElementById(id);
  if (!track) return;

  const outer = track.parentElement;
  const card  = track.querySelector('.product-card');
  if (!card) return;

  const cardW   = card.offsetWidth + 20; // card + gap
  const visible = 4;
  const total   = track.children.length;
  const maxStep = total - visible;

  if (!carouselState[id]) carouselState[id] = 0;
  carouselState[id] = Math.max(0, Math.min(carouselState[id] + dir, maxStep));

  track.style.transform = `translateX(-${carouselState[id] * cardW}px)`;
}
