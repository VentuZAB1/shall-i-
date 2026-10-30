// HATCH NIGHT mockup engine for Upgrades / Welcome Back / Free Gift (planner, 2026-10-22).
// A copy of ../ris/engine.js with two additions the plan needs (docs/plans/2026-10-22-hatch-night-upgrades-welcome-freegift.md):
//   * per-window LOGICAL sizes (Free Gift 560 x 460, Welcome Back 540 x 430, Upgrades 740 x 470) = H.windowChrome opts.w/h
//     + H.fitWindow(guiW, guiH, leftClear, cap, lw, lh) + H.headerTeeth(w)
//   * the Upgrades big-PC cap (H.pageCap "Upgrades", R 0.6718 = today's 0.62-of-screen window in Studio) and the tutorial
//     guide clearance (H.tutorialFit with the window's own lh).
// Everything is in logical px under one CSS scale (= the Roblox UIScale). URL: ?view=<view>&dev=pc|phone|pc1050|phone667&qa=1
const P = new URLSearchParams(location.search);
const DEV = P.get('dev') || 'pc';
const VIEW = P.get('view') || 'freegift';
const DEVICES = {
  // rightClear (plan section 3, ESTIMATES until Task 0 measures PetsEggsUI.RightTiles): gui right edge - the right tile
  // column's left edge + 6. The walk-in windows are not MainMenu windows, so the right tiles do NOT slide away for them.
  pc:       { w: 1920, h: 1080, inset: 58, safeL: 0,  safeR: 0,  bg: '../assets/bg_pc.jpg',    leftClear: 412.1, rightClear: 126,  guideK: 1.18 },
  phone:    { w: 844,  h: 390,  inset: 44, safeL: 56, safeR: 56, bg: '../assets/bg_phone.jpg', leftClear: 144.3, rightClear: 57.3, guideK: 0.629 * 0.8 },
  pc1050:   { w: 1050, h: 620,  inset: 58, safeL: 0,  safeR: 0,  bg: '../assets/bg_pc.jpg',    leftClear: 229.3, rightClear: 72.3, guideK: 1.0 },
  phone667: { w: 667,  h: 375,  inset: 44, safeL: 0,  safeR: 0,  bg: '../assets/bg_phone.jpg', leftClear: 137.9, rightClear: 55,   guideK: 0.605 * 0.8 },
};
const D = DEVICES[DEV];
const GE = 0.889; // GothamBlack (in-engine) width / Montserrat Black width: max of 24 measured strings (mean 0.858)
const GUI = { x: D.safeL, y: D.inset, w: D.w - D.safeL - D.safeR, h: D.h - D.inset };
// = H.fitWindow(guiW, guiH, leftClear, cap, lw, lh) (plan 7.1 item 4; lw/lh default 740/470 = today's function)
function fitWindow(guiW, guiH, leftClear, cap, lw, lh) {
  cap = cap || 1.18; lw = lw || 740; lh = lh || 470;
  const left = Math.max(8, leftClear || 0), right = guiW - 8;
  const s = Math.min(Math.max(Math.min(cap, (right - left) / lw, (guiH - 12) / lh), 0.5), cap);
  const w = lw * s, lo = left + w / 2;
  const cx = Math.min(Math.max(guiW / 2, lo), Math.max(lo, right - w / 2));
  return { s, cx, cy: guiH / 2 };
}
// = H.tutorialFit(s, cx, cy, guiH, topClear, lw, lh): shift down under the guide first, shrink only by what is missing
function tutorialFit(F, guiH, topClear, lh) {
  let s = F.s, h = lh * s;
  const avail = guiH - topClear - 6;
  if (h > avail) { s = Math.max(0.5, avail / lh); h = lh * s; }
  return { s, cx: F.cx, cy: Math.max(F.cy, topClear + h / 2) };
}
let WIN = { w: 740, h: 470 }, FIT, S, QS, GUIDE = null;
// o.capR: H.PAGE_CAP_R (big-PC cap = max(1.18, R x guiH / 470)); o.guide: the tutorial guide {title, sub} drawn at the top
function setup(lw, lh, o) {
  o = o || {};
  WIN = { w: lw, h: lh };
  const cap = o.capR ? Math.max(1.18, o.capR * GUI.h / 470) : 1.18;
  // = H.fitStandalone (plan 7.1 item 9): fitWindow on the width left of the right tiles, then centred on the gui when it can be
  FIT = fitWindow(GUI.w - D.rightClear + 8, GUI.h, D.leftClear, cap, lw, lh);
  { const w = lw * FIT.s, lo = Math.max(8, D.leftClear) + w / 2, hi = GUI.w - D.rightClear - w / 2;
    FIT.cx = Math.max(lo, Math.min(GUI.w / 2, hi)); }
  if (o.guide) {
    // TutorialUI.Guide: 720 x 118 at y 0.015 (screen), UIScale deviceScale x phoneFactor; the Pips row's bottom = 112 logical
    GUIDE = o.guide;
    GUIDE.k = D.guideK;
    GUIDE.top = GUI.y + 0.015 * GUI.h; // (screen px; TutorialUI uses the same below-inset space as MainMenu: RIS ledger run C)
    const bottomScreen = GUIDE.top + 112 * GUIDE.k;
    FIT = tutorialFit(FIT, GUI.h, bottomScreen - GUI.y + 6, lh);
  }
  S = FIT.s; QS = S;
}

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
  if (rot) i.dataset.rot = rot;
  return i;
}
// H.text: box (x, y, w, size + 2), fixed size, ink stroke (s25 = 2.5, s2 = 2, s3 = 3, s4 = 4)
function txt(parent, s, x, y, w, size, o) {
  o = o || {};
  const t = h('div', 'txt ' + (o.stroke || 's25'), parent, { textContent: s });
  pos(t, x, y, w, size + 2); t.style.lineHeight = (size + 2) + 'px'; t.style.fontSize = size + 'px';
  if (o.color) t.style.color = o.color;
  if (o.align) t.style.textAlign = o.align;
  t.dataset.room = w - 2 * ({ s2: 2, s25: 2.5, s3: 3, s15: 1.5, s4: 4 }[o.stroke || 's25'] || 0);
  if (o.name) t.dataset.name = o.name;
  return t;
}
// stroked text with a gradient fill (ink stroke layer under, gradient fill over)
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
  if (o.faceBg) b.style.setProperty('--faceBg', o.faceBg);
  h('div', 'side', b);
  const face = h('div', 'face', b, { data: { c: '1', name: (o.name || 'btn') + '.face' } });
  if (o.faceBg) face.style.background = o.faceBg;
  return { b, face, w, fh: hh - d };
}
let _cv;
function measure(s, size) { // Montserrat Black width in logical px
  _cv = _cv || document.createElement('canvas').getContext('2d');
  _cv.font = `${size}px GB`; return _cv.measureText(s).width;
}
// a labelled gloss button; o.glyph = an image key ('robux_white' default, 'A:cash', 'locked'): [pre] glyph price as one
// centred group (= H.priceButton.setPrice); o.top = a fixed top line over the group (= priceButton opts.top, plan 7.1 item 6)
function button(parent, pal, label, x, y, w, hh, o) {
  o = o || {};
  const B = gbtn(parent, pal, x, y, w, hh, o);
  const size = o.size || 18;
  let areaTop = 0;
  if (o.top) {
    const ts = o.topSize || 16;
    txt(B.face, o.top, 8, 5, w - 16, ts, { color: o.topColor, name: B.b.dataset.name + '.top' });
    areaTop = 5 + ts + 2;
  }
  if (o.glyph) {
    // setPrice: the group (pre, 8, glyph, 6, price) steps down from size to max(16, size - 8) until it fits w - 16
    const gs = o.glyphSize || Math.round(size * 1.05);
    let sz = size, tw = 0, pre = 0, gw = 0;
    for (sz = size; sz >= Math.max(16, size - 8); sz--) {
      tw = measure(label, sz); pre = o.pre ? measure(o.pre, sz) + 8 : 0; gw = pre + gs + 6 + tw; // (Montserrat widths: conservative; the build measures GothamBlack)
      if (gw <= w - 16) break;
    }
    sz = Math.max(sz, Math.max(16, size - 8));
    const ly = areaTop + Math.round((B.fh - areaTop - sz) / 2) - 1;
    const x0 = Math.round((w - gw) / 2);
    if (o.pre) txt(B.face, o.pre, x0, ly, pre, sz, { align: 'left', color: o.color, name: B.b.dataset.name + '.pre' }).dataset.skipfill = 1;
    sticker(o.glyph, B.face, x0 + pre, areaTop + Math.round((B.fh - areaTop - gs) / 2), gs, 0, B.b.dataset.name + '.glyph');
    txt(B.face, label, x0 + pre + gs + 6, ly, tw + 6, sz, { align: 'left', color: o.color, name: B.b.dataset.name + '.price' }).dataset.skipfill = 1;
    B.size = sz;
  } else {
    // setWord: the 8 px padded box; the first variant (largest size >= 16) whose glyphs use <= 83 % of the room
    const vs = Array.isArray(label) ? label : [label];
    const room = w - 16 - 5;
    let pick = vs[vs.length - 1], sz = Math.min(size, 16);
    outer: for (const v of vs) for (let z = size; z >= Math.min(size, 16); z--) if (measure(v, z) * GE <= 0.83 * room) { pick = v; sz = z; break outer; }
    const ly = areaTop + Math.round((B.fh - areaTop - sz) / 2) - 1;
    txt(B.face, pick, 8, ly, w - 16, sz, { color: o.color, name: B.b.dataset.name + '.label' });
    B.size = sz; B.word = pick;
  }
  return B;
}
// H.fit with HatchFill 0.83: the first variant at the largest size (base down to 16) that fits 83 % of the room
function fitTxt(parent, variants, x, y, w, size, o) {
  o = o || {};
  const room = w - 2 * ({ s2: 2, s25: 2.5, s3: 3, s15: 1.5, s4: 4 }[o.stroke || 's25'] || 0);
  for (const v of variants) for (let z = size; z >= Math.min(size, 16); z--)
    if (measure(v, z) * GE <= 0.83 * room) { const t = txt(parent, v, x, y + (size - z) / 2, w, z, o); return t; }
  return txt(parent, variants[variants.length - 1], x, y, w, Math.min(size, 16), o);
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
const BANDS = {
  Pumpkin: { band: 'linear-gradient(180deg,#FFB43C 0%,#FF8A1C 55%,#F2620A 100%)', tooth: '#F2620A' },
  HatchGold: { band: 'linear-gradient(180deg,#FFD84A 0%,#FFA800 100%)', tooth: '#FFA800' },
  // (plan 7.1 item 1) the two new bands
  FreeGift: { band: 'linear-gradient(180deg,#78F5A0 0%,#1ED778 55%,#00A05A 100%)', tooth: '#00A05A' },
  Upgrades: { band: 'linear-gradient(180deg,#82AFFF 0%,#3C6EFF 55%,#1E3CDC 100%)', tooth: '#1E3CDC' },
};
// = H.headerTeeth(w): n = round(36 (w - 32) / 708) gaps, centres 16 .. w - 16, sizes 11 + ((i*7+3)%5)*1.6 (740 -> H.HEADER_TEETH)
function headerTeeth(w) {
  const n = Math.round(36 * (w - 32) / 708), out = [];
  for (let i = 0; i <= n; i++) out.push([16 + i * (w - 32) / n, 11 + ((i * 7 + 3) % 5) * 1.6]);
  return out;
}
function stage() {
  const st = h('div', 'stage', document.body);
  st.style.width = D.w + 'px'; st.style.height = D.h + 'px'; st.style.backgroundImage = `url(${D.bg})`;
  h('div', 'stage-dim', st);
  if (GUIDE) drawGuide(st);
  const win = h('div', 'win', st, { data: { c: '1', name: 'window' } });
  pos(win, GUI.x + FIT.cx - WIN.w / 2, GUI.y + FIT.cy - WIN.h / 2, WIN.w, WIN.h);
  win.style.transform = `scale(${S})`;
  if (DEV === 'phone') {
    h('div', 'guide-safe', st, { style: { left: '0px', width: D.safeL + 'px' } });
    h('div', 'guide-safe', st, { style: { right: '0px', width: D.safeR + 'px' } });
  }
  h('div', 'side', win);
  const F = h('div', 'face', win, { data: { c: '1', name: 'winface' } });
  F.style.height = (WIN.h - 7) + 'px';
  return { st, win, F };
}
// the tutorial guide (TutorialClient Check-UI floating text: title @~30, sub @~19, 11 pips) - stand-in for the overlap check
function drawGuide(st) {
  const g = h('div', 'abs', st, { data: { noqa: 1 } });
  pos(g, GUI.x + GUI.w / 2 - 360, GUIDE.top, 720, 118);
  g.style.transformOrigin = '50% 0'; g.style.transform = `scale(${GUIDE.k})`;
  txt(g, GUIDE.title, 0, 12, 720, 30, { stroke: 's3' });
  const sub = txt(g, GUIDE.sub, 50, 59, 620, 19, { color: '#E1ECF2' });
  const pips = h('div', 'abs', g); pos(pips, 360 - 11 * 13, 94, 11 * 26, 18);
  for (let i = 0; i < 11; i++) {
    const p = h('div', 'abs', pips); pos(p, i * 24 + 2, 1.5, 15, 15);
    p.style.borderRadius = '4px'; p.style.boxShadow = '0 0 0 2.2px #000';
    p.style.background = i < (GUIDE.done || 7) ? '#FFD000' : i === (GUIDE.done || 7) ? '#B4FF4A' : '#3A4660';
  }
}
function chrome(F, theme, title, icon) {
  const th = BANDS[theme], W = WIN.w;
  for (const [cx, s] of headerTeeth(W)) {
    const ink = h('div', 'tooth', F); pos(ink, cx - (s + 5) / 2, 46 - (s + 5) / 2, s + 5, s + 5); ink.style.background = 'var(--ink)';
    const t = h('div', 'tooth', F); pos(t, cx - s / 2, 46 - s / 2, s, s); t.style.background = th.tooth;
  }
  const band = h('div', 'hdr', F); band.style.background = th.band; band.style.width = W + 'px';
  h('div', 'hdr-gloss', F).style.width = W + 'px';
  sticker(icon, F, 12, 4, 38, 0, 'headerIcon');
  const tw = Math.min(400, W - 58 - 70);
  txt(F, title, 58, 13, tw, 26, { stroke: 's3', align: 'left', color: 'var(--ink)', name: 'TitleShadow' });
  txt(F, title, 58, 10, tw, 26, { stroke: 's3', align: 'left', name: 'Title' });
  const X = gbtn(F, 'red', W - 46, 6, 34, 34, { d: 4, r: 9, ol: 2, name: 'Close' });
  txt(X.face, 'X', 0, 4, 34, 21, { name: 'X' });
}
function canvasOf(F, name) { const c = h('div', 'abs', F, { data: { c: '1', name } }); pos(c, 0, 0, WIN.w, WIN.h - 7); return c; }
// QA (same rules as ../ris/engine.js qa(): outlines inside the parent, tile siblings no overlap + gaps >= 8, no text
// overflow, the GothamBlack fill estimate <= 83 %), plus: rotated stickers use their rotated bounding box
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
  const winTop = GUI.y + FIT.cy - WIN.h * S / 2;
  out.push(`view ${VIEW} dev ${DEV}: logical ${WIN.w}x${WIN.h} scale ${S.toFixed(4)}  window ${Math.round(WIN.w * S)}x${Math.round(WIN.h * S)} at gui (cx ${FIT.cx.toFixed(2)}, cy ${FIT.cy.toFixed(2)}) left ${(FIT.cx - WIN.w * S / 2).toFixed(1)} (HUD clear ${D.leftClear})  right ${(FIT.cx + WIN.w * S / 2).toFixed(1)} (tiles clear ${(GUI.w - D.rightClear).toFixed(1)})  min text ${minPx.toFixed(1)} px ("${minTxt}")`);
  if (GUIDE) out.push(`guide bottom (screen) ${(GUIDE.top + 112 * GUIDE.k).toFixed(1)}  window top (screen) ${winTop.toFixed(1)}  clear ${(winTop - GUIDE.top - 112 * GUIDE.k).toFixed(1)}`);
  if (extra) out.push(...extra);
  const q = h('pre', '', document.body, { id: 'qa' });
  q.textContent = out.join('\n');
  q.style.display = P.get('qa') ? 'block' : 'none';
}
