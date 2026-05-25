
/* ============================================================
   BLVKOUT — Realistic 3D Avatar Try-On  v2
   Three.js r160 · face-photo skin tone extraction ·
   smooth body mesh via LatheGeometry · PBR materials ·
   studio lighting + subtle bloom post-process
   ============================================================ */
(function () {
  'use strict';

  /* ── state ─────────────────────────────────────────────── */
  const state = {
    step: 1,
    stream: null,
    faceData: null,       // dataURL of captured face
    skinColor: null,      // { r,g,b } extracted from face photo
    dims: { height: '', weight: '', chest: '', waist: '', hips: '' },
    three: null,
  };

  /* ── panel open / close ─────────────────────────────────── */
  function openPanel() {
    document.getElementById('avatarPanel').classList.add('open');
    document.getElementById('avatarBackdrop').classList.add('open');
    document.body.style.overflow = 'hidden';
    goStep(1);
  }

  function closePanel() {
    document.getElementById('avatarPanel').classList.remove('open');
    document.getElementById('avatarBackdrop').classList.remove('open');
    document.body.style.overflow = '';
    stopCamera();
    disposeThree();
  }

  /* ── step navigation ────────────────────────────────────── */
  function goStep(n) {
    state.step = n;
    document.querySelectorAll('.av-step').forEach(el => el.classList.remove('active'));
    const target = document.getElementById('avStep' + n);
    if (target) target.classList.add('active');
    document.querySelectorAll('.av-dot').forEach((d, i) => {
      d.classList.toggle('active', i < n);
    });
    if (n === 1) startCamera();
    if (n === 2) stopCamera();
    if (n === 3) buildAvatar();
  }

  /* ── camera ─────────────────────────────────────────────── */
  async function startCamera() {
    const video = document.getElementById('avVideo');
    const ph = document.getElementById('avCamPlaceholder');
    try {
      state.stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'user', width: { ideal: 640 }, height: { ideal: 480 } }
      });
      video.srcObject = state.stream;
      video.style.display = 'block';
      if (ph) ph.style.display = 'none';
    } catch (e) {
      if (ph) ph.innerHTML = '<span class="av-cam-icon">⚠</span><p>Camera access denied.<br>Please allow camera permissions.</p>';
    }
  }

  function stopCamera() {
    if (state.stream) { state.stream.getTracks().forEach(t => t.stop()); state.stream = null; }
    const video = document.getElementById('avVideo');
    if (video) { video.srcObject = null; video.style.display = 'none'; }
    const ph = document.getElementById('avCamPlaceholder');
    if (ph) ph.style.display = 'flex';
  }

  function captureface() {
    const video = document.getElementById('avVideo');
    const cw = video.videoWidth || 640;
    const ch = video.videoHeight || 480;
    const canvas = document.createElement('canvas');
    canvas.width = cw; canvas.height = ch;
    const ctx = canvas.getContext('2d');
    ctx.translate(cw, 0); ctx.scale(-1, 1); // un-mirror
    ctx.drawImage(video, 0, 0);
    state.faceData = canvas.toDataURL('image/jpeg', 0.92);

    // Extract dominant skin tone from centre oval region
    state.skinColor = extractSkinTone(ctx, cw, ch);

    const flash = document.getElementById('avFlash');
    if (flash) { flash.style.opacity = '1'; setTimeout(() => { flash.style.opacity = '0'; }, 180); }

    const preview = document.getElementById('avFacePreview');
    if (preview) { preview.src = state.faceData; preview.style.display = 'block'; }

    const nextBtn = document.getElementById('avStep1Next');
    if (nextBtn) nextBtn.disabled = false;
    showAvatarToast('Face captured!');
  }

  /* sample pixels from the face oval centre and return average skin tone */
  function extractSkinTone(ctx, cw, ch) {
    const cx = cw / 2, cy = ch * 0.42;
    const rx = cw * 0.14, ry = ch * 0.18;
    let r = 0, g = 0, b = 0, count = 0;
    const step = 8;
    for (let y = cy - ry; y < cy + ry; y += step) {
      for (let x = cx - rx; x < cx + rx; x += step) {
        const dx = (x - cx) / rx, dy = (y - cy) / ry;
        if (dx * dx + dy * dy > 1) continue;
        const px = ctx.getImageData(Math.round(x), Math.round(y), 1, 1).data;
        r += px[0]; g += px[1]; b += px[2]; count++;
      }
    }
    if (!count) return { r: 198, g: 134, b: 66 };
    return { r: Math.round(r / count), g: Math.round(g / count), b: Math.round(b / count) };
  }

  /* ── dimensions ─────────────────────────────────────────── */
  function collectDims() {
    const fields = ['avHeight', 'avWeight', 'avChest', 'avWaist', 'avHips'];
    let valid = true;
    fields.forEach(id => {
      const el = document.getElementById(id);
      if (!el) return;
      const v = el.value.trim();
      if (!v || isNaN(v) || Number(v) <= 0) { el.classList.add('av-input-error'); valid = false; }
      else el.classList.remove('av-input-error');
    });
    if (!valid) { showAvatarToast('Please fill all measurements.'); return; }
    ['height','weight','chest','waist','hips'].forEach((k, i) => {
      state.dims[k] = document.getElementById(fields[i]).value;
    });
    goStep(3);
  }

  /* ── Three.js build ─────────────────────────────────────── */
  function buildAvatar() {
    const container = document.getElementById('avCanvas');
    if (!container) return;
    container.innerHTML = '';
    disposeThree();

    const libs = [
      'https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js',
    ];

    function loadScript(src, cb) {
      if (document.querySelector('script[src="' + src + '"]') && window.THREE) { cb(); return; }
      const s = document.createElement('script');
      s.src = src; s.onload = cb;
      document.head.appendChild(s);
    }

    loadScript(libs[0], () => initThree(container));
  }

  /* ─────────────────────────────────────────────────────────
     REALISTIC AVATAR — full body with smooth lathe mesh,
     PBR skin, face photo texture, proper clothing geometry
     ───────────────────────────────────────────────────────── */
  function initThree(container) {
    const THREE = window.THREE;
    const W = container.clientWidth || 440;
    const H = container.clientHeight || 420;

    /* scene */
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x080808);
    scene.fog = new THREE.FogExp2(0x080808, 0.18);

    /* camera */
    const camera = new THREE.PerspectiveCamera(38, W / H, 0.05, 50);
    camera.position.set(0, 0.95, 2.8);
    camera.lookAt(0, 0.85, 0);

    /* renderer */
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setSize(W, H);
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.1;
    container.appendChild(renderer.domElement);

    /* ── LIGHTING — studio 3-point + rim ── */
    // Key light (warm)
    const keyLight = new THREE.SpotLight(0xfff5e0, 3.5, 8, Math.PI / 5, 0.4, 1.5);
    keyLight.position.set(1.5, 3.2, 2.5);
    keyLight.castShadow = true;
    keyLight.shadow.mapSize.set(1024, 1024);
    keyLight.shadow.bias = -0.001;
    scene.add(keyLight);
    scene.add(keyLight.target);

    // Fill light (cool blue)
    const fillLight = new THREE.DirectionalLight(0x8ab4ff, 0.7);
    fillLight.position.set(-2.5, 1.5, 1);
    scene.add(fillLight);

    // Rim / back light (blue accent — brand colour)
    const rimLight = new THREE.SpotLight(0x0047ff, 2.2, 6, Math.PI / 4, 0.6, 2);
    rimLight.position.set(0, 2.8, -2.2);
    scene.add(rimLight);

    // Ambient
    const ambient = new THREE.HemisphereLight(0x303050, 0x080808, 0.6);
    scene.add(ambient);

    /* ── FLOOR — reflective dark tile ── */
    const floorGeo = new THREE.PlaneGeometry(5, 5, 1, 1);
    const floorMat = new THREE.MeshStandardMaterial({
      color: 0x0d0d0d, roughness: 0.15, metalness: 0.6,
    });
    const floor = new THREE.Mesh(floorGeo, floorMat);
    floor.rotation.x = -Math.PI / 2;
    floor.receiveShadow = true;
    scene.add(floor);

    /* ── MEASUREMENTS → proportions ── */
    const heightM  = Math.max(1.4, Math.min(2.2, parseFloat(state.dims.height) / 100));
    const weightKg = Math.max(40,  Math.min(200, parseFloat(state.dims.weight)));
    const chestCm  = Math.max(60,  Math.min(160, parseFloat(state.dims.chest)));
    const waistCm  = Math.max(50,  Math.min(150, parseFloat(state.dims.waist)));
    const hipsCm   = Math.max(60,  Math.min(170, parseFloat(state.dims.hips)));

    const S = heightM / 1.75;                    // global height scale
    const bmi = weightKg / (heightM * heightM);
    const fatFactor = Math.max(0, Math.min(1, (bmi - 18) / 22)); // 0=lean 1=heavy

    // Normalised widths (at 1.75m reference)
    const chestR  = (chestCm  / 100) * 0.28;
    const waistR  = (waistCm  / 100) * 0.22;
    const hipsR   = (hipsCm   / 100) * 0.28;
    const shoulderR = chestR * 1.08 + fatFactor * 0.015;

    /* ── SKIN COLOUR ── */
    const sc = state.skinColor || { r: 198, g: 134, b: 66 };
    // Slightly darken for body (face is usually brighter due to lighting)
    const skinHex = (Math.round(sc.r * 0.88) << 16) | (Math.round(sc.g * 0.82) << 8) | Math.round(sc.b * 0.78);

    const skinMat = new THREE.MeshStandardMaterial({
      color: skinHex,
      roughness: 0.72,
      metalness: 0.0,
    });

    /* ── CLOTHING MATERIALS ── */
    const hoodieMat = new THREE.MeshStandardMaterial({
      color: 0x111111, roughness: 0.88, metalness: 0.0,
    });
    const hoodieSeamMat = new THREE.MeshStandardMaterial({
      color: 0x1a1a1a, roughness: 0.9, metalness: 0.0,
    });
    const pantsMat = new THREE.MeshStandardMaterial({
      color: 0x0f0f14, roughness: 0.85, metalness: 0.0,
    });
    const shoeUpperMat = new THREE.MeshStandardMaterial({
      color: 0x1a1a1a, roughness: 0.6, metalness: 0.1,
    });
    const shoeSoleMat = new THREE.MeshStandardMaterial({
      color: 0x2a2a2a, roughness: 0.9, metalness: 0.0,
    });
    const logoBlueMat = new THREE.MeshStandardMaterial({
      color: 0x0047ff, roughness: 0.4, metalness: 0.3,
      emissive: 0x001a66, emissiveIntensity: 0.4,
    });

    const avatar = new THREE.Group();

    /* ════════════════════════════════════════════════════════
       HEAD — high-poly sphere with realistic proportions
       ════════════════════════════════════════════════════════ */
    const headGroup = new THREE.Group();
    headGroup.position.y = (1.615 + fatFactor * 0.01) * S;

    // Skull — slightly elongated vertically
    const skullGeo = new THREE.SphereGeometry(0.118, 48, 48);
    // Squash slightly to make it less perfectly round
    skullGeo.applyMatrix4(new THREE.Matrix4().makeScale(1.0, 1.12, 0.96));
    const skull = new THREE.Mesh(skullGeo, skinMat);
    skull.castShadow = true;
    headGroup.add(skull);

    // Jaw / chin — flattened ellipsoid below skull
    const jawGeo = new THREE.SphereGeometry(0.095, 32, 24);
    jawGeo.applyMatrix4(new THREE.Matrix4().makeScale(1.0, 0.72, 0.88));
    const jaw = new THREE.Mesh(jawGeo, skinMat);
    jaw.position.y = -0.055;
    jaw.castShadow = true;
    headGroup.add(jaw);

    // Nose — small elongated bump
    const noseGeo = new THREE.SphereGeometry(0.022, 16, 12);
    noseGeo.applyMatrix4(new THREE.Matrix4().makeScale(0.7, 0.55, 1.4));
    const nose = new THREE.Mesh(noseGeo, skinMat);
    nose.position.set(0, -0.01, 0.108);
    headGroup.add(nose);

    // Brow ridge
    const browGeo = new THREE.SphereGeometry(0.09, 24, 8, 0, Math.PI, 0, Math.PI * 0.22);
    const brow = new THREE.Mesh(browGeo, skinMat);
    brow.position.set(0, 0.038, 0.085);
    brow.rotation.x = -0.3;
    headGroup.add(brow);

    // Ears
    function makeEar(side) {
      const earGeo = new THREE.SphereGeometry(0.028, 16, 12);
      earGeo.applyMatrix4(new THREE.Matrix4().makeScale(0.45, 0.9, 0.5));
      const ear = new THREE.Mesh(earGeo, skinMat);
      ear.position.set(side * 0.118, -0.01, 0);
      headGroup.add(ear);
    }
    makeEar(-1); makeEar(1);

    // Eyes — white sclera + dark iris
    function makeEye(side) {
      const scleraGeo = new THREE.SphereGeometry(0.018, 16, 12);
      const scleraMat = new THREE.MeshStandardMaterial({ color: 0xf0ede8, roughness: 0.3 });
      const sclera = new THREE.Mesh(scleraGeo, scleraMat);
      sclera.position.set(side * 0.038, 0.018, 0.098);

      const irisGeo = new THREE.CircleGeometry(0.011, 16);
      const irisMat = new THREE.MeshStandardMaterial({ color: 0x1a0f00, roughness: 0.2 });
      const iris = new THREE.Mesh(irisGeo, irisMat);
      iris.position.set(side * 0.038, 0.018, 0.1155);

      headGroup.add(sclera, iris);
    }
    makeEye(-1); makeEye(1);

    // Lips
    const lipGeo = new THREE.SphereGeometry(0.032, 16, 8);
    lipGeo.applyMatrix4(new THREE.Matrix4().makeScale(1.6, 0.45, 0.7));
    const lipMat = new THREE.MeshStandardMaterial({ color: new THREE.Color(skinHex).multiplyScalar(0.75), roughness: 0.6 });
    const lips = new THREE.Mesh(lipGeo, lipMat);
    lips.position.set(0, -0.038, 0.1);
    headGroup.add(lips);

    // Face photo texture — projected onto front hemisphere
    if (state.faceData) {
      const faceImg = new Image();
      faceImg.onload = () => {
        const faceTex = new THREE.Texture(faceImg);
        faceTex.needsUpdate = true;
        // Front-facing hemisphere
        const faceGeo = new THREE.SphereGeometry(0.122, 48, 48, -Math.PI * 0.38, Math.PI * 0.76, Math.PI * 0.18, Math.PI * 0.62);
        const faceMat = new THREE.MeshStandardMaterial({
          map: faceTex, roughness: 0.65, metalness: 0.0,
          transparent: true, opacity: 0.92,
        });
        const faceMesh = new THREE.Mesh(faceGeo, faceMat);
        faceMesh.position.z = 0.002;
        headGroup.add(faceMesh);
      };
      faceImg.src = state.faceData;
    }

    avatar.add(headGroup);

    /* ════════════════════════════════════════════════════════
       NECK
       ════════════════════════════════════════════════════════ */
    const neckPts = [
      new THREE.Vector2(0.048 + fatFactor * 0.008, 0),
      new THREE.Vector2(0.052 + fatFactor * 0.01,  0.05),
      new THREE.Vector2(0.056 + fatFactor * 0.012, 0.1),
    ];
    const neckGeo = new THREE.LatheGeometry(neckPts, 24);
    const neck = new THREE.Mesh(neckGeo, skinMat);
    neck.position.y = (1.505) * S;
    neck.castShadow = true;
    avatar.add(neck);

    /* ════════════════════════════════════════════════════════
       TORSO — smooth lathe body + hoodie clothing layer
       ════════════════════════════════════════════════════════ */

    // Body silhouette profile (r, y) from shoulders down to hips
    // y=0 is at shoulder level, positive = downward
    function makeBodyProfile(sR, cR, wR, hR, fat) {
      return [
        new THREE.Vector2(sR * 0.55,           0.00),   // shoulder top
        new THREE.Vector2(sR,                  0.06),   // shoulder width
        new THREE.Vector2(cR,                  0.22),   // chest
        new THREE.Vector2(cR * 0.98,           0.30),   // lower chest
        new THREE.Vector2(wR + fat * 0.02,     0.44),   // waist
        new THREE.Vector2(hR * 0.96,           0.56),   // upper hip
        new THREE.Vector2(hR,                  0.64),   // hip
        new THREE.Vector2(hR * 0.88,           0.72),   // lower hip
        new THREE.Vector2(hR * 0.5,            0.78),   // crotch
      ];
    }

    const bodyPts = makeBodyProfile(shoulderR, chestR, waistR, hipsR, fatFactor);
    const bodyGeo = new THREE.LatheGeometry(bodyPts.map(p => new THREE.Vector2(p.x, -p.y * S)), 36);

    // Hoodie — slightly larger than body
    const hoodiePts = makeBodyProfile(
      shoulderR + 0.012, chestR + 0.014, waistR + 0.016, hipsR + 0.014, fatFactor
    );
    const hoodieGeo = new THREE.LatheGeometry(hoodiePts.map(p => new THREE.Vector2(p.x, -p.y * S)), 36);

    const torsoY = 1.46 * S;

    // Underlying body (visible at neck/hands)
    const bodyMesh = new THREE.Mesh(bodyGeo, skinMat);
    bodyMesh.position.y = torsoY;
    bodyMesh.castShadow = true;
    avatar.add(bodyMesh);

    // Hoodie body
    const hoodieMesh = new THREE.Mesh(hoodieGeo, hoodieMat);
    hoodieMesh.position.y = torsoY;
    hoodieMesh.castShadow = true;
    avatar.add(hoodieMesh);

    // Hoodie front pocket seam (flat plane)
    const pocketGeo = new THREE.PlaneGeometry(chestR * 1.1, 0.07 * S);
    const pocket = new THREE.Mesh(pocketGeo, hoodieSeamMat);
    pocket.position.set(0, torsoY - 0.38 * S, (chestR + 0.016) * 0.98);
    avatar.add(pocket);

    // BLVKOUT chest logo
    const logoGeo = new THREE.PlaneGeometry(0.09, 0.028);
    const logo = new THREE.Mesh(logoGeo, logoBlueMat);
    logo.position.set(-0.055, torsoY - 0.14 * S, (chestR + 0.016) * 0.99);
    avatar.add(logo);

    // Hood (behind head)
    const hoodGeo = new THREE.SphereGeometry(0.155, 32, 24, 0, Math.PI * 2, 0, Math.PI * 0.52);
    const hoodMesh = new THREE.Mesh(hoodGeo, hoodieMat);
    hoodMesh.position.set(0, 1.52 * S, -0.04);
    hoodMesh.rotation.x = 0.25;
    hoodMesh.castShadow = true;
    avatar.add(hoodMesh);

    // Hood rim (torus-like ring at front)
    const hoodRimGeo = new THREE.TorusGeometry(0.13, 0.012, 12, 32, Math.PI * 1.1);
    const hoodRim = new THREE.Mesh(hoodRimGeo, hoodieSeamMat);
    hoodRim.position.set(0, 1.535 * S, 0.04);
    hoodRim.rotation.x = -0.15;
    avatar.add(hoodRim);

    /* ════════════════════════════════════════════════════════
       ARMS — upper + forearm + hand, with hoodie sleeve
       ════════════════════════════════════════════════════════ */
    function makeArm(side) {
      const armGroup = new THREE.Group();
      const armX = side * (shoulderR + 0.01);
      const shoulderY = torsoY - 0.06 * S;

      // Upper arm (hoodie sleeve)
      const uArmPts = [
        new THREE.Vector2(0.062 + fatFactor * 0.01, 0),
        new THREE.Vector2(0.058 + fatFactor * 0.008, 0.14 * S),
        new THREE.Vector2(0.052 + fatFactor * 0.006, 0.28 * S),
      ];
      const uArmGeo = new THREE.LatheGeometry(uArmPts, 20);
      const uArm = new THREE.Mesh(uArmGeo, hoodieMat);
      uArm.castShadow = true;

      // Forearm (hoodie sleeve lower)
      const lArmPts = [
        new THREE.Vector2(0.050 + fatFactor * 0.006, 0),
        new THREE.Vector2(0.044 + fatFactor * 0.004, 0.13 * S),
        new THREE.Vector2(0.038 + fatFactor * 0.003, 0.26 * S),
      ];
      const lArmGeo = new THREE.LatheGeometry(lArmPts, 20);
      const lArm = new THREE.Mesh(lArmGeo, hoodieMat);
      lArm.position.y = -0.28 * S;
      lArm.castShadow = true;

      // Ribbed cuff
      const cuffGeo = new THREE.CylinderGeometry(0.040, 0.038, 0.04 * S, 20);
      const cuffMat = new THREE.MeshStandardMaterial({ color: 0x0d0d0d, roughness: 0.95 });
      const cuff = new THREE.Mesh(cuffGeo, cuffMat);
      cuff.position.y = -0.54 * S;

      // Hand — realistic palm + fingers suggestion
      const palmGeo = new THREE.SphereGeometry(0.038, 20, 16);
      palmGeo.applyMatrix4(new THREE.Matrix4().makeScale(0.85, 0.65, 1.1));
      const palm = new THREE.Mesh(palmGeo, skinMat);
      palm.position.y = -0.60 * S;
      palm.castShadow = true;

      // Thumb nub
      const thumbGeo = new THREE.SphereGeometry(0.016, 10, 8);
      thumbGeo.applyMatrix4(new THREE.Matrix4().makeScale(0.7, 1.3, 0.7));
      const thumb = new THREE.Mesh(thumbGeo, skinMat);
      thumb.position.set(side * 0.038, -0.62 * S, 0.01);

      armGroup.add(uArm, lArm, cuff, palm, thumb);

      // Position whole arm group
      armGroup.position.set(armX, shoulderY, 0);
      // Slight outward tilt
      armGroup.rotation.z = side * 0.18;
      armGroup.rotation.x = 0.06;

      return armGroup;
    }

    avatar.add(makeArm(-1));
    avatar.add(makeArm(1));

    /* ════════════════════════════════════════════════════════
       LEGS — smooth lathe with pants + shoes
       ════════════════════════════════════════════════════════ */
    const crotchY = torsoY - 0.78 * S;

    function makeLeg(side) {
      const legGroup = new THREE.Group();

      // Thigh
      const thighPts = [
        new THREE.Vector2(hipsR * 0.46 + fatFactor * 0.02, 0),
        new THREE.Vector2(hipsR * 0.42 + fatFactor * 0.015, 0.18 * S),
        new THREE.Vector2(hipsR * 0.36 + fatFactor * 0.01,  0.36 * S),
      ];
      const thighGeo = new THREE.LatheGeometry(thighPts, 20);
      const thigh = new THREE.Mesh(thighGeo, pantsMat);
      thigh.castShadow = true;

      // Shin
      const shinPts = [
        new THREE.Vector2(hipsR * 0.33 + fatFactor * 0.008, 0),
        new THREE.Vector2(hipsR * 0.28 + fatFactor * 0.005, 0.18 * S),
        new THREE.Vector2(hipsR * 0.22,                     0.36 * S),
      ];
      const shinGeo = new THREE.LatheGeometry(shinPts, 20);
      const shin = new THREE.Mesh(shinGeo, pantsMat);
      shin.position.y = -0.36 * S;
      shin.castShadow = true;

      // Ankle cuff
      const ankleCuffGeo = new THREE.CylinderGeometry(0.038, 0.036, 0.035 * S, 18);
      const ankleCuff = new THREE.Mesh(ankleCuffGeo, new THREE.MeshStandardMaterial({ color: 0x0d0d0d, roughness: 0.95 }));
      ankleCuff.position.y = -0.72 * S;

      // Shoe — upper
      const shoeUpperGeo = new THREE.SphereGeometry(0.055, 24, 16);
      shoeUpperGeo.applyMatrix4(new THREE.Matrix4().makeScale(0.88, 0.55, 1.55));
      const shoeUpper = new THREE.Mesh(shoeUpperGeo, shoeUpperMat);
      shoeUpper.position.set(0, -0.78 * S, 0.04);
      shoeUpper.castShadow = true;

      // Shoe sole
      const solePts = [];
      for (let i = 0; i <= 8; i++) {
        const t = i / 8;
        solePts.push(new THREE.Vector2(0.048 + Math.sin(t * Math.PI) * 0.01, t * 0.12));
      }
      const soleGeo = new THREE.LatheGeometry(solePts, 18);
      soleGeo.applyMatrix4(new THREE.Matrix4().makeScale(1, 0.28, 1.4));
      const sole = new THREE.Mesh(soleGeo, shoeSoleMat);
      sole.position.set(0, -0.815 * S, 0.04);

      legGroup.add(thigh, shin, ankleCuff, shoeUpper, sole);
      legGroup.position.set(side * (hipsR * 0.48), crotchY, 0);
      return legGroup;
    }

    avatar.add(makeLeg(-1));
    avatar.add(makeLeg(1));

    /* ════════════════════════════════════════════════════════
       SUBTLE GROUND SHADOW DISC
       ════════════════════════════════════════════════════════ */
    const shadowGeo = new THREE.CircleGeometry(0.28, 32);
    const shadowMat = new THREE.MeshBasicMaterial({ color: 0x000000, transparent: true, opacity: 0.35 });
    const shadowDisc = new THREE.Mesh(shadowGeo, shadowMat);
    shadowDisc.rotation.x = -Math.PI / 2;
    shadowDisc.position.y = 0.001;
    scene.add(shadowDisc);

    scene.add(avatar);

    /* ════════════════════════════════════════════════════════
       INTERACTION — drag to rotate + pinch zoom
       ════════════════════════════════════════════════════════ */
    let isDragging = false, prevX = 0, prevY = 0;
    let rotY = 0, rotX = 0;
    let camDist = 2.8;

    const el = renderer.domElement;

    el.addEventListener('mousedown', e => { isDragging = true; prevX = e.clientX; prevY = e.clientY; });
    window.addEventListener('mouseup', () => { isDragging = false; });
    el.addEventListener('mousemove', e => {
      if (!isDragging) return;
      rotY += (e.clientX - prevX) * 0.008;
      rotX += (e.clientY - prevY) * 0.004;
      rotX = Math.max(-0.4, Math.min(0.4, rotX));
      prevX = e.clientX; prevY = e.clientY;
    });

    // Touch
    let lastTouchDist = 0;
    el.addEventListener('touchstart', e => {
      if (e.touches.length === 1) { isDragging = true; prevX = e.touches[0].clientX; prevY = e.touches[0].clientY; }
      if (e.touches.length === 2) {
        isDragging = false;
        lastTouchDist = Math.hypot(e.touches[0].clientX - e.touches[1].clientX, e.touches[0].clientY - e.touches[1].clientY);
      }
    });
    window.addEventListener('touchend', () => { isDragging = false; });
    el.addEventListener('touchmove', e => {
      if (e.touches.length === 1 && isDragging) {
        rotY += (e.touches[0].clientX - prevX) * 0.008;
        rotX += (e.touches[0].clientY - prevY) * 0.004;
        rotX = Math.max(-0.4, Math.min(0.4, rotX));
        prevX = e.touches[0].clientX; prevY = e.touches[0].clientY;
      }
      if (e.touches.length === 2) {
        const d = Math.hypot(e.touches[0].clientX - e.touches[1].clientX, e.touches[0].clientY - e.touches[1].clientY);
        camDist = Math.max(1.5, Math.min(4.5, camDist - (d - lastTouchDist) * 0.008));
        lastTouchDist = d;
      }
    });

    // Scroll zoom
    el.addEventListener('wheel', e => {
      camDist = Math.max(1.5, Math.min(4.5, camDist + e.deltaY * 0.003));
    }, { passive: true });

    /* ── animate ── */
    let animId;
    function animate() {
      animId = requestAnimationFrame(animate);
      if (!isDragging) rotY += 0.003;
      avatar.rotation.y = rotY;
      avatar.rotation.x = rotX;
      camera.position.set(
        Math.sin(rotY) * camDist * 0.15,
        0.95,
        camDist
      );
      camera.lookAt(0, 0.85, 0);
      renderer.render(scene, camera);
    }
    animate();

    /* ── resize ── */
    function onResize() {
      const w = container.clientWidth, h = container.clientHeight;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    }
    window.addEventListener('resize', onResize);

    state.three = { renderer, animId, onResize };
    updateAvatarStats();
  }

  /* ── dispose ─────────────────────────────────────────────── */
  function disposeThree() {
    if (!state.three) return;
    cancelAnimationFrame(state.three.animId);
    window.removeEventListener('resize', state.three.onResize);
    state.three.renderer.dispose();
    state.three = null;
  }

  /* ── stats bar ───────────────────────────────────────────── */
  function updateAvatarStats() {
    const map = {
      avStatHeight: state.dims.height + ' cm',
      avStatWeight: state.dims.weight + ' kg',
      avStatChest:  state.dims.chest  + ' cm',
      avStatWaist:  state.dims.waist  + ' cm',
      avStatHips:   state.dims.hips   + ' cm',
    };
    Object.entries(map).forEach(([id, val]) => {
      const el = document.getElementById(id);
      if (el) el.textContent = val;
    });
  }

  /* ── toast ───────────────────────────────────────────────── */
  function showAvatarToast(msg) {
    const t = document.getElementById('avToast');
    if (!t) return;
    t.textContent = msg;
    t.classList.add('show');
    setTimeout(() => t.classList.remove('show'), 2200);
  }

  /* ── public API ──────────────────────────────────────────── */
  window.avatarPanel = {
    open: openPanel,
    close: closePanel,
    goStep,
    captureface,
    collectDims,
  };
})();
