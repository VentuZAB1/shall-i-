// HATCH NIGHT mockup engine for the Starter Pack popup + Shop (2026-10-21, planner).
// Same recipe as ../common.js + ../dirB_hatchnight.html: everything in LOGICAL px (window 740 x 470, face 740 x 463),
// one CSS scale = the Roblox UIScale. URL: ?view=<view>&dev=pc|phone&qa=1
// Fit = BrickUI.Hatch.fitWindow (the Gift plan's section 3): the Shop clears the left HUD (shifted right on phones),
// the popup is modal (centred in the safe area, leftClear 0).
const P = new URLSearchParams(location.search);
const DEV = P.get('dev') || 'pc';
const VIEW = P.get('view') || 'popup';
const DEVICES = {
  pc:    { w: 1920, h: 1080, inset: 58, safeL: 0,  safeR: 0,  bg: '../assets/bg_pc.jpg',    leftClear: 412.1 },
  phone: { w: 844,  h: 390,  inset: 44, safeL: 56, safeR: 56, bg: '../assets/bg_phone.jpg', leftClear: 144.3 },
};
const D = DEVICES[DEV];
const WIN = { w: 740, h: 470 };
const GE = 0.889; // GothamBlack (in-engine) width / Montserrat Black width: max of 24 measured strings (mean 0.858)
function fitWindow(guiW, guiH, leftClear) { // = H.fitWindow
  const left = Math.max(8, leftClear || 0), right = guiW - 8;
  const s = Math.min(Math.max(Math.min(1.18, (right - left) / 740, (guiH - 12) / 470), 0.5), 1.18);
  const w = 740 * s, lo = left + w / 2;
  const cx = Math.min(Math.max(guiW / 2, lo), Math.max(lo, right - w / 2));
  return { s, cx, cy: guiH / 2 };
}
const MODAL = VIEW.startsWith('popup');
const GUI = { x: D.safeL, y: D.inset, w: D.w - D.safeL - D.safeR, h: D.h - D.inset };
const FIT = fitWindow(GUI.w, GUI.h, MODAL ? 0 : D.leftClear);
const S = FIT.s;
let QS = S; // the scale the QA uses for outlines (the long view renders at x1, the sheet at x1.25)

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
function pos(e, x, y, w, hh) { Object.assign(e.style, { left: x + 'px', top: y + 'px', width: w + 'px', height: hh + 'px' }); return e; }
// src: 'A:name' = ../assets/name.png (the art director's set), otherwise assets/name.png (this folder)
function src(s) { return s.startsWith('A:') ? '../assets/' + s.slice(2) + '.png' : 'assets/' + s + '.png'; }
function img(s, parent, x, y, w, hh, style) {
  const i = h('img', 'abs', parent); i.src = src(s); pos(i, x, y, w, hh === undefined ? w : hh);
  i.style.objectFit = 'contain';
  if (style) Object.assign(i.style, style);
  return i;
}
// H.sticker: frameless art + an ink drop shadow (+3 px, black 0.55); rot = degrees about the centre
function sticker(s, parent, x, y, size, rot, name, extra) {
  const i = img(s, parent, x, y, size, size, Object.assign({ filter: 'drop-shadow(0 3px 0 rgba(6,4,20,.55))' }, extra || {}));
  if (rot) i.style.transform = `rotate(${rot}deg)`;
  i.dataset.ol = 0; i.dataset.name = name || s;
  return i;
}
// H.text: box (x, y, w, size + 2), fixed size, ink stroke (s25 = 2.5, s2 = 2, s3 = 3)
function txt(parent, s, x, y, w, size, o) {
  o = o || {};
  const t = h('div', 'txt ' + (o.stroke || 's25'), parent, { textContent: s });
  pos(t, x, y, w, size + 2); t.style.lineHeight = (size + 2) + 'px'; t.style.fontSize = size + 'px';
  if (o.color) t.style.color = o.color;
  if (o.align) t.style.textAlign = o.align;
  t.dataset.room = w - 2 * ({ s2: 2, s25: 2.5, s3: 3, s15: 1.5 }[o.stroke || 's25']);
  if (o.name) t.dataset.name = o.name;
  return t;
}
// stroked text with a gradient fill (two layers: ink stroke under, gradient fill over) - the timers, SECRET PET! style
function gradTxt(parent, s, x, y, w, size, grad, o) {
  o = o || {};
  const a = txt(parent, s, x, y, w, size, { stroke: o.stroke || 's3', align: o.align, color: '#0D0B1C', name: (o.name || s) + '_ink' });
  const b = txt(parent, s, x, y, w, size, { stroke: 'none', align: o.align, name: o.name || s });
  b.classList.add('gfill'); b.style.backgroundImage = grad;
  b.dataset.skipfill = 1;
  return [a, b];
}
// H.glossButton: holder{side (depth d), face (gradient, top highlight, gloss band)}
function gbtn(parent, pal, x, y, w, hh, o) {
  o = o || {};
  const d = o.d || 3, r = o.r || 9, ol = o.ol || 2.5;
  const b = h('div', 'gb p-' + pal, parent, { data: { ol: ol, name: o.name || ('btn_' + pal) } });
  if (o.tile) b.dataset.tile = o.tile;
  pos(b, x, y, w, hh);
  b.style.setProperty('--d', d + 'px'); b.style.setProperty('--r', r + 'px'); b.style.setProperty('--ol', ol + 'px');
  h('div', 'side', b);
  const face = h('div', 'face', b, { data: { c: '1', name: (o.name || 'btn') + '.face' } });
  return { b, face, w, fh: hh - d };
}
// a labelled gloss button: optional Robux glyph (white hex + ink shadow) before the label, centred as one group
function button(parent, pal, label, x, y, w, hh, o) {
  o = o || {};
  const B = gbtn(parent, pal, x, y, w, hh, o);
  const size = o.size || 18;
  const ly = Math.round((B.fh - size) / 2) - 1;
  if (o.robux) {
    const gs = o.glyph || Math.round(size * 1.05);
    const tw = measure(label, size) + 4; // label box = its glyph width + 4 (the builder measures with TextService)
    const pre = o.pre ? measure(o.pre, size) + 8 : 0; // e.g. "BUY " before the glyph
    const gw = pre + gs + 6 + tw;
    const x0 = Math.round((w - gw) / 2);
    if (o.pre) txt(B.face, o.pre, x0, ly, pre, size, { align: 'left', color: o.color, name: B.b.dataset.name + '.pre' }).dataset.skipfill = 1;
    sticker('robux_white', B.face, x0 + pre, Math.round((B.fh - gs) / 2), gs, 0, 'robux');
    txt(B.face, label, x0 + pre + gs + 6, ly, tw + 6, size, { align: 'left', color: o.color, name: B.b.dataset.name + '.price' }).dataset.skipfill = 1;
  } else {
    txt(B.face, label, 0, ly, w, size, { color: o.color, name: B.b.dataset.name + '.label' });
  }
  return B;
}
let _cv;
function measure(s, size) { // Montserrat Black width in logical px
  _cv = _cv || document.createElement('canvas').getContext('2d');
  _cv.font = `${size}px GB`; return _cv.measureText(s).width;
}
function glow(parent, x, y, w, hh, color, a) {
  const g = h('div', 'abs', parent); pos(g, x, y, w, hh);
  g.style.borderRadius = '50%';
  g.style.background = `radial-gradient(closest-side, ${color} 0%, ${color} 45%, transparent 100%)`;
  g.style.opacity = a;
  return g;
}
function recess(parent, x, y, w, hh, r, name) {
  const f = h('div', 'recess', parent, { data: { ol: 2, name: name, c: '1' } }); pos(f, x, y, w, hh);
  f.style.borderRadius = (r === undefined ? hh / 2 : r) + 'px';
  return f;
}
function chip(parent, x, y, w, hh, name, tile) {
  const f = h('div', 'chip', parent, { data: { ol: 2, name: name, c: '1' } }); pos(f, x, y, w, hh);
  if (tile) f.dataset.tile = tile;
  return f;
}
function tag(parent, s, x, y, w, name) {
  const f = h('div', 'tag', parent, { data: { ol: 2, name: name || 'tag', c: '1' } }); pos(f, x, y, w, 22);
  txt(f, s, 0, 2, w, 16, { name: (name || 'tag') + '.label' });
  return f;
}
// H.shellCard: holder{side (depth 5), face (gradient, top highlight)}; returns the face (a [data-c] container)
function card(parent, x, y, w, hh, name, o) {
  o = o || {};
  const C = h('div', 'card', parent, { data: { ol: 2.5, name: name, c: '1' } });
  if (o.tile) C.dataset.tile = o.tile;
  pos(C, x, y, w, hh);
  h('div', 'side', C);
  const f = h('div', 'face', C, { data: { c: '1', name: name + '.face' } });
  if (o.face) f.style.background = o.face;
  return f;
}
// the window: night shell + band with the cracked-shell edge + title (+ ink copy) + header sticker + red X
const BANDS = {
  Shop: { band: 'linear-gradient(180deg,#FF60C4 0%,#FF2496 55%,#DC0064 100%)', tooth: '#DC0064' },
  Pumpkin: { band: 'linear-gradient(180deg,#FFB43C 0%,#FF8A1C 55%,#F2620A 100%)', tooth: '#F2620A' },
};
function stage() {
  document.documentElement.style.setProperty('--S', S);
  const st = h('div', 'stage', document.body);
  st.style.width = D.w + 'px'; st.style.height = D.h + 'px'; st.style.backgroundImage = `url(${D.bg})`;
  h('div', MODAL ? 'stage-modal' : 'stage-dim', st);
  const win = h('div', 'win', st, { data: { c: '1', name: 'window' } });
  pos(win, GUI.x + FIT.cx - WIN.w / 2, GUI.y + FIT.cy - WIN.h / 2, WIN.w, WIN.h);
  win.style.transform = `scale(${S})`;
  if (DEV === 'phone') {
    h('div', 'guide-safe', st, { style: { left: '0px', width: D.safeL + 'px' } });
    h('div', 'guide-safe', st, { style: { right: '0px', width: D.safeR + 'px' } });
  }
  h('div', 'side', win);
  const F = h('div', 'face', win, { data: { c: '1', name: 'winface' } });
  return { st, win, F };
}
function chrome(F, theme, title, icon) {
  const th = BANDS[theme];
  for (let i = 0; i < 37; i++) { // H.HEADER_TEETH: 37 teeth, centres x 16..724, sizes 11 + ((i*7+3)%5)*1.6, ink +5
    const cx = 16 + i * 708 / 36, s = 11 + ((i * 7 + 3) % 5) * 1.6;
    const ink = h('div', 'tooth', F); pos(ink, cx - (s + 5) / 2, 46 - (s + 5) / 2, s + 5, s + 5); ink.style.background = 'var(--ink)';
    const t = h('div', 'tooth', F); pos(t, cx - s / 2, 46 - s / 2, s, s); t.style.background = th.tooth;
  }
  const band = h('div', 'hdr', F); band.style.background = th.band;
  h('div', 'hdr-gloss', F);
  sticker(icon, F, 12, 4, 38, 0, 'headerIcon');
  txt(F, title, 58, 13, 400, 26, { stroke: 's3', align: 'left', color: 'var(--ink)', name: 'TitleShadow' });
  txt(F, title, 58, 10, 400, 26, { stroke: 's3', align: 'left', name: 'Title' });
  const X = gbtn(F, 'red', 694, 6, 34, 34, { d: 4, r: 9, ol: 2, name: 'Close' });
  txt(X.face, 'X', 0, 4, 34, 21, { name: 'X' });
}
// QA (same rules as ../common.js qa(), plus the GothamBlack width estimate)
function qa(extra) {
  const out = [];
  const pad = 0.5;
  document.querySelectorAll('[data-ol]').forEach(el => {
    if (el.closest('[data-noqa]')) return;
    const ol = parseFloat(el.dataset.ol) * QS;
    const r = el.getBoundingClientRect();
    const c = el.parentElement && el.parentElement.closest('[data-c]');
    if (!c) return;
    const cr = c.getBoundingClientRect();
    if (r.left - ol < cr.left - pad || r.top - ol < cr.top - pad || r.right + ol > cr.right + pad || r.bottom + ol > cr.bottom + pad)
      out.push(`OUT  ${el.dataset.name || el.className} (ol ${el.dataset.ol}) not inside ${c.dataset.name}: ` +
        `[${((r.left - ol - cr.left) / QS).toFixed(1)}, ${((r.top - ol - cr.top) / QS).toFixed(1)}, ${((cr.right - r.right - ol) / QS).toFixed(1)}, ${((cr.bottom - r.bottom - ol) / QS).toFixed(1)}] logical`);
  });
  const groups = new Map();
  document.querySelectorAll('[data-tile]').forEach(el => {
    const g = el.dataset.tile + '@' + (el.parentElement ? el.parentElement.dataset.name : '');
    if (!groups.has(g)) groups.set(g, []);
    groups.get(g).push(el);
  });
  let gapMin = 999, gapWho = '';
  for (const [g, els] of groups) {
    for (let i = 0; i < els.length; i++) for (let j = i + 1; j < els.length; j++) {
      const a = els[i].getBoundingClientRect(), b = els[j].getBoundingClientRect();
      const oa = parseFloat(els[i].dataset.ol || 0) * QS, ob = parseFloat(els[j].dataset.ol || 0) * QS;
      if (a.left - oa < b.right + ob && b.left - ob < a.right + oa && a.top - oa < b.bottom + ob && b.top - ob < a.bottom + oa)
        out.push(`OVERLAP ${g}: ${els[i].dataset.name} x ${els[j].dataset.name}`);
      const gap = Math.max(b.left - a.right, a.left - b.right, b.top - a.bottom, a.top - b.bottom) / QS;
      if (gap < gapMin) { gapMin = gap; gapWho = `${els[i].dataset.name} / ${els[j].dataset.name}`; }
    }
  }
  if (gapMin < 8 - 0.05) out.push(`GAP < 8: ${gapMin.toFixed(1)} (${gapWho})`);
  let minPx = 999, minTxt = '';
  const fills = [];
  document.querySelectorAll('.txt').forEach(el => {
    if (el.closest('[data-noqa]') || !el.textContent.trim()) return;
    if (el.scrollWidth > el.clientWidth + 1) out.push(`TEXT OVERFLOW "${el.textContent}" ${el.scrollWidth}>${el.clientWidth}`);
    const fs = parseFloat(getComputedStyle(el).fontSize) * QS;
    if (fs < minPx) { minPx = fs; minTxt = el.textContent; }
    if (el.dataset.skipfill) return;
    const size = parseFloat(getComputedStyle(el).fontSize);
    const room = parseFloat(el.dataset.room || el.clientWidth);
    fills.push([measure(el.textContent, size) * GE / room, el.textContent, size]);
  });
  fills.sort((x, y) => y[0] - x[0]);
  out.push('tightest est. GothamBlack fill (glyph x 0.889 / box - 2 x stroke): ' + fills.slice(0, 5).map(w => `${(w[0] * 100).toFixed(0)}% "${w[1]}"@${w[2]}`).join(', '));
  const over = fills.filter(f => f[0] > 0.83);
  out.push(over.length ? 'FILL > 83%: ' + over.map(w => `"${w[1]}"@${w[2]} ${(w[0] * 100).toFixed(0)}%`).join(', ') : 'fill <= 83% everywhere');
  out.push(`view ${VIEW} dev ${DEV}: scale ${S.toFixed(4)}  window ${Math.round(WIN.w * S)}x${Math.round(WIN.h * S)} at gui cx ${FIT.cx.toFixed(2)}  min text ${minPx.toFixed(1)} px ("${minTxt}")`);
  if (extra) out.push(...extra);
  const q = h('pre', '', document.body, { id: 'qa' });
  q.textContent = out.join('\n');
  q.style.display = P.get('qa') ? 'block' : 'none';
}
