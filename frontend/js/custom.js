// Print method tabs
document.querySelectorAll('.print-tab').forEach(tab => {
  tab.addEventListener('click', function () {
    document.querySelectorAll('.print-tab').forEach(t => t.classList.remove('active'));
    this.classList.add('active');
  });
});

// Print library selection
function selectPrint(el) {
  document.querySelectorAll('.print-lib-item').forEach(i => i.classList.remove('active'));
  el.classList.add('active');
  // Mirror selected print to canvas overlay
  const printImg = document.getElementById('printImg');
  const bg = el.querySelector('div').style.background || '#333';
  printImg.querySelector('div').style.background = bg;
}

// Upload zone
const uploadZone = document.getElementById('uploadZone');
const fileInput = document.getElementById('fileInput');

uploadZone.addEventListener('click', () => fileInput.click());

uploadZone.addEventListener('dragover', e => {
  e.preventDefault();
  uploadZone.style.borderColor = 'var(--blue)';
});

uploadZone.addEventListener('dragleave', () => {
  uploadZone.style.borderColor = 'rgba(255,255,255,0.2)';
});

uploadZone.addEventListener('drop', e => {
  e.preventDefault();
  uploadZone.style.borderColor = 'rgba(255,255,255,0.2)';
  const file = e.dataTransfer.files[0];
  if (file && file.type.startsWith('image/')) applyUpload(file);
});

fileInput.addEventListener('change', () => {
  if (fileInput.files[0]) applyUpload(fileInput.files[0]);
});

function applyUpload(file) {
  const reader = new FileReader();
  reader.onload = e => {
    const printImg = document.getElementById('printImg');
    printImg.innerHTML = `<img src="${e.target.result}" style="width:100%;height:100%;object-fit:contain;" />`;
    uploadZone.querySelector('.upload-text').textContent = file.name;
  };
  reader.readAsDataURL(file);
}

// Draggable print overlay
const overlay = document.getElementById('printOverlay');
let isDragging = false, startX, startY, origLeft, origTop;

overlay.addEventListener('mousedown', e => {
  if (e.target.classList.contains('canvas-resize-handle')) return;
  isDragging = true;
  startX = e.clientX;
  startY = e.clientY;
  const rect = overlay.getBoundingClientRect();
  const parentRect = overlay.parentElement.getBoundingClientRect();
  origLeft = rect.left - parentRect.left;
  origTop = rect.top - parentRect.top;
  overlay.style.transform = 'none';
  overlay.style.left = origLeft + 'px';
  overlay.style.top = origTop + 'px';
  e.preventDefault();
});

document.addEventListener('mousemove', e => {
  if (!isDragging) return;
  const dx = e.clientX - startX;
  const dy = e.clientY - startY;
  overlay.style.left = (origLeft + dx) + 'px';
  overlay.style.top = (origTop + dy) + 'px';
});

document.addEventListener('mouseup', () => { isDragging = false; });

// Resizable
const handle = overlay.querySelector('.canvas-resize-handle');
let isResizing = false, resizeStartX, resizeStartY, origW, origH;

handle.addEventListener('mousedown', e => {
  isResizing = true;
  resizeStartX = e.clientX;
  resizeStartY = e.clientY;
  origW = overlay.offsetWidth;
  origH = overlay.offsetHeight;
  e.stopPropagation();
  e.preventDefault();
});

document.addEventListener('mousemove', e => {
  if (!isResizing) return;
  const dw = e.clientX - resizeStartX;
  const dh = e.clientY - resizeStartY;
  overlay.style.width = Math.max(60, origW + dw) + 'px';
  overlay.style.height = Math.max(60, origH + dh) + 'px';
});

document.addEventListener('mouseup', () => { isResizing = false; });

// Zoom
let zoom = 1;
function zoomCanvas(dir) {
  zoom = Math.min(2, Math.max(0.5, zoom + dir * 0.1));
  document.querySelector('.canvas-product-preview').style.transform = `scale(${zoom})`;
}

// View toggle
function setView(btn, view) {
  document.querySelectorAll('.view-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
}

// Save draft
function saveDraft() {
  const btn = document.querySelector('.btn-save-draft');
  btn.textContent = 'DRAFT SAVED ✓';
  btn.style.color = 'rgba(100,255,100,0.7)';
  setTimeout(() => {
    btn.textContent = 'SAVE DRAFT';
    btn.style.color = '';
  }, 2000);
}
