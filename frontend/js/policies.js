function showPolicy(e, id) {
  e.preventDefault();
  document.querySelectorAll('.policy-section').forEach(s => s.classList.remove('active'));
  document.querySelectorAll('.policy-nav-item').forEach(n => n.classList.remove('active'));
  document.getElementById(id).classList.add('active');
  e.currentTarget.classList.add('active');
  window.scrollTo({ top: document.querySelector('.policies-page').offsetTop - 80, behavior: 'smooth' });
}
