// Shared mockup engine for the SLINGSHOT UI style mockups (2026-10-21).
// URL params: ?dev=pc|phone  &state=mid|next  &qa=1 (prints the containment report into #qa)
// The window is built in LOGICAL units (740 x 470) and scaled like a Roblox UIScale ("WindowScale").
const P = new URLSearchParams(location.search);
const DEV = P.get('dev') || 'pc';
const STATE = P.get('state') || (DEV === 'phone' ? 'next' : 'mid');
const DEVICES = {
  // inset = Roblox top bar (GuiService:GetGuiInset), safe = notch side insets (Studio phone emulator: 733 wide)
  pc:    { w: 1920, h: 1080, inset: 58, safeL: 0,  safeR: 0,  bg: 'assets/bg_pc.jpg' },
  phone: { w: 844,  h: 390,  inset: 44, safeL: 56, safeR: 56, bg: 'assets/bg_phone.jpg' },
};
const WIN = { w: 740, h: 470 };
const D = DEVICES[DEV];
// Window scale = fit the usable area (safe area minus the top bar, 6 px margins), capped at Check-UI's 1.18
const S = Math.min(1.18, (D.w - D.safeL - D.safeR - 16) / WIN.w, (D.h - D.inset - 12) / WIN.h);

// Reward copy: line 1 = big value (LuckiestGuy / GothamBlack 21-22), line 2 = <= 11 chars at 16 (minimum size)
const DAYS = [
  { d: 1, area: 'grass',     val: '$9K',       sub: '+1 POTION',  icons: [['cash', 64, 0, 0], ['potion_gold', 36, 30, 22, 'x1']], glow: '#6CFF5A' },
  { d: 2, area: 'water',     val: '+2M SPEED', sub: '+2 POTIONS', icons: [['potion_green', 50, -20, 4], ['potion_blue', 50, 20, 4], ['shoe', 34, 0, 26]], glow: '#55C8FF' },
  { d: 3, area: 'thunder',   val: '$18K',      sub: '+2 POTIONS', icons: [['cash', 64, 0, 0], ['potion_gold', 36, 30, 22, 'x2']], glow: '#FFE15A' },
  { d: 4, area: 'fire',      val: 'BIG EGG',   sub: '30K KG',     icons: [['egg_grass', 62, 0, 0]], glow: '#9CFF6A' },
  { d: 5, area: 'shadow',    val: '3x ALL',    sub: 'POTIONS',    icons: [['potion_gold', 42, -30, 8], ['potion_green', 42, 30, 8], ['potion_blue', 46, 0, 0]], glow: '#C78BFF' },
  { d: 6, area: 'celestial', val: '$36K',      sub: '+5M SPEED',  icons: [['cash', 62, -8, 0], ['shoe', 40, 30, 22]], glow: '#7FA0FF' },
];
const HERO = { d: 7, title: 'SECRET PET!', pet: 'THORNBLADE MANTIS', kg: '15K KG', chips: [['potions', 'x5 ALL'], ['cash', '$72K']] };

// state per day (1..7): claimed / claim / tomorrow / locked
const STATES = {
  mid:  ['claimed', 'claimed', 'claim', 'locked', 'locked', 'locked', 'locked'],
  next: ['claimed', 'claimed', 'claimed', 'tomorrow', 'locked', 'locked', 'locked'],
};
const ST = STATES[STATE];
const TIMER = '09:41:27';
const STREAK_DAY = STATE === 'mid' ? 3 : 3; // days done or today

function h(tag, cls, parent, props) {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (props) for (const k in props) {
    if (k === 'style') Object.assign(e.style, props.style);
    else if (k === 'data') Object.assign(e.dataset, props.data);
    else e[k] = props[k];
  }
  if (parent) parent.appendChild(e);
  return e;
}
function img(src, cls, parent, size, style) {
  const i = h('img', cls, parent);
  i.src = 'assets/' + src + '.png';
  if (size) { i.style.width = size + 'px'; i.style.height = size + 'px'; }
  if (style) Object.assign(i.style, style);
  return i;
}

// stage + device chrome (background crop, safe area guides on phone)
function stage() {
  document.documentElement.style.setProperty('--S', S);
  const st = h('div', 'stage', document.body);
  st.style.width = D.w + 'px';
  st.style.height = D.h + 'px';
  st.style.backgroundImage = `url(${D.bg})`;
  h('div', 'stage-dim', st);
  const win = h('div', 'win', st, { data: { c: '1', name: 'window' } });
  win.style.width = WIN.w + 'px';
  win.style.height = WIN.h + 'px';
  const cx = D.safeL + (D.w - D.safeL - D.safeR) / 2;
  const cy = D.inset + (D.h - D.inset) / 2;
  win.style.left = (cx - WIN.w / 2) + 'px';
  win.style.top = (cy - WIN.h / 2) + 'px';
  win.style.transform = `scale(${S})`;
  if (DEV === 'phone') {
    // notch side insets + top bar band (for the reviewer: the window must stay out of them)
    h('div', 'guide-safe', st, { style: { left: '0px', width: D.safeL + 'px' } });
    h('div', 'guide-safe', st, { style: { right: '0px', width: D.safeR + 'px' } });
  }
  return { st, win };
}

// QA: every [data-ol] element (incl. its outline / stroke) must sit inside its nearest [data-c] container,
// siblings marked [data-tile] must not overlap, and no .txt may overflow its own box.
function qa() {
  const out = [];
  const pad = 0.5;
  document.querySelectorAll('[data-ol]').forEach(el => {
    const ol = parseFloat(el.dataset.ol) * S;
    const r = el.getBoundingClientRect();
    const c = el.parentElement && el.parentElement.closest('[data-c]');
    if (!c) return;
    const cr = c.getBoundingClientRect();
    if (r.left - ol < cr.left - pad || r.top - ol < cr.top - pad || r.right + ol > cr.right + pad || r.bottom + ol > cr.bottom + pad)
      out.push(`OUT  ${el.dataset.name || el.className} (ol ${el.dataset.ol}) not inside ${c.dataset.name}: ` +
        `[${(r.left - ol - cr.left).toFixed(1)}, ${(r.top - ol - cr.top).toFixed(1)}, ${(cr.right - r.right - ol).toFixed(1)}, ${(cr.bottom - r.bottom - ol).toFixed(1)}]`);
  });
  const groups = new Map();
  document.querySelectorAll('[data-tile]').forEach(el => {
    const g = el.dataset.tile;
    if (!groups.has(g)) groups.set(g, []);
    groups.get(g).push(el);
  });
  for (const [g, els] of groups) {
    for (let i = 0; i < els.length; i++) for (let j = i + 1; j < els.length; j++) {
      const a = els[i].getBoundingClientRect(), b = els[j].getBoundingClientRect();
      const oa = parseFloat(els[i].dataset.ol || 0) * S, ob = parseFloat(els[j].dataset.ol || 0) * S;
      if (a.left - oa < b.right + ob && b.left - ob < a.right + oa && a.top - oa < b.bottom + ob && b.top - ob < a.bottom + oa)
        out.push(`OVERLAP ${g}: ${els[i].dataset.name} x ${els[j].dataset.name}`);
    }
  }
  document.querySelectorAll('.txt').forEach(el => {
    if (el.scrollWidth > el.clientWidth + 1) out.push(`TEXT OVERFLOW "${el.textContent}" ${el.scrollWidth}>${el.clientWidth}`);
  });
  // minimum on-screen text size
  let minPx = 999, minTxt = '';
  document.querySelectorAll('.txt').forEach(el => {
    const fs = parseFloat(getComputedStyle(el).fontSize) * S;
    if (fs < minPx) { minPx = fs; minTxt = el.textContent; }
  });
  // tightest text: glyph width / box width (GothamBlack is ~5% wider than the Montserrat Black stand-in)
  let worst = [];
  document.querySelectorAll('.txt').forEach(el => {
    if (!el.textContent.trim()) return;
    const r = document.createRange(); r.selectNodeContents(el);
    const tw = r.getBoundingClientRect().width, bw = el.getBoundingClientRect().width;
    const pl = parseFloat(getComputedStyle(el).paddingLeft) * S;
    worst.push([(tw) / (bw - pl), el.textContent]);
  });
  worst.sort((x, y) => y[0] - x[0]);
  out.push('tightest text fill: ' + worst.slice(0, 4).map(w => `${(w[0] * 100).toFixed(0)}% "${w[1]}"`).join(', '));
  out.push(`scale ${S.toFixed(3)}  window ${Math.round(WIN.w * S)}x${Math.round(WIN.h * S)}  min text ${minPx.toFixed(1)} px ("${minTxt}")`);
  const q = h('pre', '', document.body, { id: 'qa' });
  q.textContent = out.join('\n');
  q.style.display = P.get('qa') ? 'block' : 'none';
}

// Component style sheet stage (?view=sheet): logical 1200 x 820 at 1.25x on a neutral dark board
const SHEET = P.get('view') === 'sheet';
function sheetStage(title, sub) {
  const k = 1.25;
  const st = h('div', 'stage sheet', document.body);
  st.style.width = (1200 * k) + 'px'; st.style.height = (820 * k) + 'px';
  st.style.background = 'radial-gradient(ellipse at 50% 0%,#3a3f55,#1c1e29 75%)';
  const board = h('div', '', st, { data: { c: '1', name: 'board' } });
  Object.assign(board.style, { position: 'absolute', left: 0, top: 0, width: '1200px', height: '820px', transform: `scale(${k})`, transformOrigin: '0 0' });
  const t = h('div', 'note', board, { textContent: title }); Object.assign(t.style, { left: '24px', top: '14px', fontSize: '22px', color: '#fff' });
  const s = h('div', 'note', board, { textContent: sub }); Object.assign(s.style, { left: '24px', top: '42px', fontSize: '13px', color: '#aab' });
  return board;
}
function note(parent, s, x, y, w) {
  const n = h('div', 'note', parent, { textContent: s });
  Object.assign(n.style, { left: x + 'px', top: y + 'px', width: (w || 200) + 'px' });
  return n;
}
