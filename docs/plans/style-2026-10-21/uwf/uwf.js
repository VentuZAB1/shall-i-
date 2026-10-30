// =====================================================================================================================
// HATCH NIGHT Upgrades / Welcome Back / Free Gift (planner mockups 2026-10-22). Same recipe as ../ris (engine.js copy +
// per-window logical sizes). Plan: docs/plans/2026-10-22-hatch-night-upgrades-welcome-freegift.md (every rect below = a
// plan table row). Stand-in art: the group icon (drawn), the thumbs-up (the system emoji, as today), the pack art from
// Downloads/Verctor (Roket / Bolt / Heart / Boost / Locked: the same pack the live ids come from).
// URL: uwf.html?view=<view>&dev=pc|phone|pc1050|phone667&qa=1
// =====================================================================================================================
const LIME = 'var(--lime)', GOLD = 'var(--gold)', RED = 'var(--red)', LAV = 'var(--lav)', LAVD = 'var(--lav-dim)';
const GROUP_SVG = 'data:image/svg+xml;utf8,' + encodeURIComponent(`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
<g stroke="#0D0B1C" stroke-width="5"><circle cx="30" cy="34" r="17" fill="#FFC83C"/><circle cx="70" cy="34" r="17" fill="#FFC83C"/>
<circle cx="30" cy="70" r="17" fill="#FFB020"/><circle cx="70" cy="70" r="17" fill="#FFB020"/></g>
<g fill="#0D0B1C"><circle cx="24" cy="32" r="3"/><circle cx="36" cy="32" r="3"/><circle cx="64" cy="32" r="3"/><circle cx="76" cy="32" r="3"/>
<circle cx="24" cy="68" r="3"/><circle cx="36" cy="68" r="3"/><circle cx="64" cy="68" r="3"/><circle cx="76" cy="68" r="3"/></g></svg>`);

// H.segment / H.arrow (18 x 22, k = size factor)
function seg(parent, ax, ay, bx, by, th, color) {
  const dx = bx - ax, dy = by - ay, L = Math.hypot(dx, dy) + th / 2;
  const e = h('div', 'abs', parent); pos(e, (ax + bx) / 2 - L / 2, (ay + by) / 2 - th / 2, L, th);
  e.style.background = color; e.style.borderRadius = th / 2 + 'px';
  e.style.transform = `rotate(${Math.atan2(dy, dx) * 180 / Math.PI}deg)`;
}
function arrow(parent, x, y, k, name) {
  k = k || 1;
  const a = h('div', 'abs', parent, { data: { ol: 0, name: name || 'Arrow' } }); pos(a, x, y, 18 * k, 22 * k);
  const P = [[4, 4], [14, 11], [4, 18]].map(p => [p[0] * k, p[1] * k]);
  for (const [th, c] of [[7 * k, 'var(--ink)'], [3.2 * k, '#B8FF6A']]) { seg(a, ...P[0], ...P[1], th, c); seg(a, ...P[1], ...P[2], th, c); }
  return a;
}
// H.nowNext (left-aligned): Now + lime chevron + Next as one group; nxt null = Now only (MAX); steps down to 16 if wider
function nowNext(parent, now, nxt, x, y, w, size, o) {
  o = o || {};
  let z = size, t1, t2, G, k;
  for (z = size; z >= 16; z--) {
    k = o.k || (z >= 24 ? 1 : 0.75);
    t1 = measure(now, z); t2 = nxt ? measure(nxt, z) : 0; // (Montserrat: conservative hug boxes)
    G = (t1 + 8) + (nxt ? 2 + 18 * k + 4 + t2 + 8 : 0);
    if (G <= w) break;
  }
  const x0 = o.align === 'left' ? x : x + (w - G) / 2, ly = y + (size - z) / 2;
  txt(parent, now, x0, ly, t1 + 8, z, { align: 'left', color: o.c1, name: (o.name || 'NN') + '.Now' }).dataset.skipfill = 1;
  if (nxt) {
    arrow(parent, x0 + t1 + 10, ly + (z + 2 - 22 * k) / 2, k, (o.name || 'NN') + '.Arrow');
    txt(parent, nxt, x0 + t1 + 14 + 18 * k, ly, t2 + 8, z, { align: 'left', color: o.c2 || LIME, name: (o.name || 'NN') + '.Next' }).dataset.skipfill = 1;
  }
  return G;
}
// H.progressBar: recess trough (r = h/2) + gloss fill (min width h - 6, hidden at 0) + centred text; fill = 2 colours
function bar(parent, x, y, w, hh, k, text, name, size, fill) {
  size = size || 16;
  const r = recess(parent, x, y, w, hh, hh / 2, name);
  if (k > 0) {
    const f = h('div', 'abs', r, { data: { ol: 0, name: name + '.Fill' } });
    pos(f, 3, 3, Math.max(hh - 6, (w - 6) * Math.min(k, 1)), hh - 6);
    f.style.borderRadius = (hh - 6) / 2 + 'px';
    f.style.background = `linear-gradient(180deg,${(fill || ['#B4FF4A', '#4FCB10'])[0]},${(fill || ['#B4FF4A', '#4FCB10'])[1]})`;
    f.style.boxShadow = 'inset 0 2px 0 rgba(255,255,255,.45)';
  }
  txt(r, text, 0, Math.round((hh - size - 2) / 2), w, size, { name: name + '.Text' });
  return r;
}
function hex(c) { return [1, 3, 5].map(i => parseInt(c.slice(i, i + 2), 16)); }
function mix(a, b, t) { const A = hex(a), B = hex(b); return 'rgb(' + A.map((v, i) => Math.round(v + (B[i] - v) * t)).join(',') + ')'; }
function emoji(parent, ch, x, y, size, name) { // the 👍 TextLabel (as today: no thumbs-up art exists in either pack)
  const e = h('div', 'abs', parent, { textContent: ch, data: { ol: 0, name: name || 'Emoji' } }); pos(e, x, y, size, size);
  Object.assign(e.style, { fontFamily: '"Segoe UI Emoji"', fontSize: size * 0.82 + 'px', lineHeight: size + 'px', textAlign: 'center' });
  return e;
}
function shards(parent, cx, cy) { // H.shards stand-in: 6 gold shell shards + 3 sparkles, mid-flight
  [[-52, -30], [48, -36], [-60, 20], [58, 18], [-20, -52], [22, 50]].forEach(([dx, dy], i) => {
    const s = h('div', 'abs', parent, { data: { ol: 0, name: 'Shard' + i } }); pos(s, cx + dx - 3, cy + dy - 3, 6, 6);
    s.style.background = ['#FFE680', '#FFB000', '#FFFFFF'][i % 3]; s.style.transform = 'rotate(45deg)';
  });
  [[-36, 40], [40, -54], [70, -6]].forEach(([dx, dy], i) => sticker('A:star', parent, cx + dx - 6, cy + dy - 6, 12, 0, 'Star' + i));
}

// ---------------------------------------------------------------- FREE GIFT (plan 4.1; window 560 x 460, face 453)
function freegift(mode) { // join (not in the group yet) | joined (claim ready) | claimed | refusal
  setup(560, 460);
  const { F } = stage();
  const cv = canvasOf(F, 'FreeGiftCanvas');
  // the art: rays (radially faded, 12 deg/s while open) + potion glow + 3 potion stickers in Art (PopScale 1.12 on claim)
  const rays = img('A:rays', cv, 42, 74, 164, 164, { opacity: .5, filter: 'sepia(1) hue-rotate(220deg) saturate(2.2) brightness(1.15)' });
  rays.dataset.ol = 0; rays.dataset.name = 'Rays';
  glow(cv, 14, 76, 220, 160, '#C78BFF', .35);
  const art = h('div', 'abs', cv, { data: { c: '1', name: 'Art' } }); pos(art, 10, 66, 228, 168);
  sticker('A:potion_gold', art, 20, 56, 84, -14, 'PotionMoney');
  sticker('A:potion_blue', art, 124, 56, 84, 14, 'PotionSpeed');
  sticker('A:potion_green', art, 60, 20, 108, 0, 'PotionHatch');
  // the headline block (x 246..550, centre 398)
  const tw = measure('ONE-TIME GIFT!', 16) * GE, tagW = Math.ceil((tw / 0.83 + 5) / 2) * 2;
  tag(cv, 'ONE-TIME GIFT!', 398 - tagW / 2, 72, tagW, 'Tag');
  gradTxt(cv, '3 POTIONS!', 246, 100, 304, 34, 'linear-gradient(180deg,#00E1FF,#28F082)', { name: 'Headline' });
  [['A:potion_gold', 'x2 MONEY', '#FFD73C'], ['A:potion_green', 'x2 HATCH', '#78F05A'], ['A:potion_blue', 'x2 SPEED', '#5AC8FF']].forEach(([ic, s, c], i) => {
    sticker(ic, cv, 345, 141 + 22 * i, 20, 0, 'ListIcon' + (i + 1));
    txt(cv, s, 371, 142 + 22 * i, 110, 16, { align: 'left', color: c, name: 'List' + (i + 1) });
  });
  fitTxt(cv, ['30 MIN EACH • USE ANYTIME!', '30 MIN EACH!'], 246, 212, 304, 16, { color: '#E1EBF5', name: 'Each' });
  // the two steps (shell cards 266 x 130, face 125; title @18 + a recessed well 250 x 82)
  const like = card(cv, 10, 240, 266, 130, 'Like', { tile: 'steps' });
  fitTxt(like, ['1. LIKE THE GAME!', '1. LIKE US!'], 8, 8, 250, 18, { name: 'LikeTitle' });
  const lw = recess(like, 8, 34, 250, 82, 14, 'LikeWell');
  emoji(lw, '👍', 8, 17, 48, 'Thumb');
  txt(lw, 'CLICK LIKE ON', 62, 20, 180, 16, { align: 'left', name: 'How1' });
  txt(lw, 'THE GAME PAGE!', 62, 42, 180, 16, { align: 'left', name: 'How2' });
  const grp = card(cv, 284, 240, 266, 130, 'Group', { tile: 'steps' });
  fitTxt(grp, ['2. JOIN THE GROUP!', '2. JOIN GROUP!'], 8, 8, 250, 18, { name: 'GroupTitle' });
  const gw = recess(grp, 8, 34, 250, 82, 14, 'GroupWell');
  const gi = img('A:egg', gw, 8, 17, 48, 48); gi.src = GROUP_SVG; gi.dataset.ol = 0; gi.dataset.name = 'GroupIcon';
  gi.style.filter = 'drop-shadow(0 3px 0 rgba(6,4,20,.55))';
  if (mode === 'join' || mode === 'refusal') {
    button(gw, 'violet', 'JOIN', 100, 19, 134, 44, { d: 4, r: 12, size: 22, name: 'Join' });
  } else {
    txt(gw, 'JOINED!', 64, 30, 136, 22, { align: 'left', color: LIME, name: 'Joined' });
    sticker('A:check', gw, 206, 27, 28, 0, 'Done');
  }
  // CLAIM (260 x 60, d 4): off (not in the group: still pressable, the server's reason shows) / lime breathing / silver / red
  const st = { join: ['off', 'CLAIM!', LAVD], joined: ['lime', 'CLAIM!'], claimed: ['silver', 'CLAIMED!'], refusal: ['red', ['JOIN THE GROUP FIRST!', 'JOIN FIRST!']] }[mode];
  button(cv, st[0], st[1], 150, 382, 260, 60, { d: 4, r: 12, size: 30, color: st[2], name: 'Claim' });
  chrome(F, 'FreeGift', 'FREE GIFT!', 'A:gift');
  qa([`state ${mode}`]);
}

// ---------------------------------------------------------------- WELCOME BACK (plan 5.1; window 540 x 430, face 423)
function welcome(mode) { // normal | big (huge amount + a 4-digit regional price) | x5 (after CLAIM x5) | refusal (dry run)
  setup(540, 430);
  const { F } = stage();
  const cv = canvasOf(F, 'WelcomeCanvas');
  txt(cv, 'OFFLINE EARNINGS', 10, 70, 520, 26, { stroke: 's3', name: 'Heading' });
  const rays = img('A:rays', cv, 155, 67, 230, 230, { opacity: .45, filter: 'sepia(1) saturate(3) brightness(1.1)' });
  rays.dataset.ol = 0; rays.dataset.name = 'Rays';
  glow(cv, 150, 102, 240, 160, '#6CFF5A', .35);
  const hero = h('div', 'abs', cv, { data: { c: '1', name: 'Hero' } }); pos(hero, 186, 98, 168, 168);
  sticker('A:cash', hero, 9, 9, 150, 0, 'Cash');
  const amt = { normal: '$547K', big: '$12.5Qa', x5: '$2.73M', refusal: '$547K' }[mode];
  gradTxt(cv, amt, 10, 262, 520, 52, 'linear-gradient(180deg,#B4FF19,#3CCD00)', { stroke: 's4', name: 'Amount' });
  if (mode === 'x5') shards(cv, 270, 182);
  if (mode === 'refusal') button(cv, 'red', ['TEST SAVE ONLY', 'TRY AGAIN'], 20, 336, 276, 64, { d: 4, r: 12, size: 26, name: 'ClaimX5', tile: 'btns' });
  else button(cv, 'gold', mode === 'big' ? '1499' : '39', 20, 336, 276, 64, { d: 4, r: 12, size: 26, glyph: 'robux_white', glyphSize: 28, pre: 'CLAIM x5!', name: 'ClaimX5', tile: 'btns' });
  button(cv, 'lime', 'CLAIM!', 304, 336, 216, 64, { d: 4, r: 12, size: 30, name: 'Claim', tile: 'btns' });
  chrome(F, 'HatchGold', 'WELCOME BACK!', 'A:cash');
  qa([`state ${mode}`]);
}

// ---------------------------------------------------------------- UPGRADES (plan 6.1; window 740 x 470, face 463)
const ROWS = [
  { kind: 'Sling', icon: 'roket', name: 'SLINGSHOT POWER', desc: 'LAUNCH FURTHER', c: '#FF9628', fill: ['#FFC066', '#F07A10'] },
  { kind: 'Grab', icon: 'bolt', name: 'FAST GRAB', desc: 'GRAB EGGS FASTER', c: '#50C8FF', fill: ['#8CDCFF', '#1E96E6'] },
  { kind: 'Shield', icon: 'heart', name: 'WAVE SHIELD', desc: 'SURVIVE 1 WAVE HIT', c: '#AA6EFF', fill: ['#C8A0FF', '#7C3CE6'] },
];
const AREA_C = { WATER: '#50C3FF', THUNDER: '#FAF05A', FIRE: '#FF8C32', SHADOW: '#BE6EFF', CELESTIAL: '#FFCD5F' };
// per row: [lv, max, area, now, next, money state, money text, robux state, robux text]
const U_STATES = {
  mid: { reb: 2, rows: [
    [6, 25, 'THUNDER', '833', '910 STUDS', 'lime', '$150K', 'gold', '15'],
    [1, 5, null, '1.2S', '0.9S', 'lock', 'REBIRTH 3', 'gold', '15'],
    [0, 1, null, '0 HITS', '1 HIT', 'lock', 'REBIRTH 10', 'gold', '50']] },
  free: { reb: 0, arrow: true, rows: [
    [0, 25, 'WATER', '370', '447 STUDS', 'free', 'FREE!', 'hide', ''],
    [0, 5, null, '1.5S', '1.2S', 'lock', 'REBIRTH 1', 'gold', '10'],
    [0, 1, null, '0 HITS', '1 HIT', 'lock', 'REBIRTH 10', 'gold', '50']],
    guide: { title: 'Press FREE on SLINGSHOT POWER!', sub: 'Your slingshot will fly further', done: 7 } },
  step10: { reb: 0, arrow: true, rows: [
    [1, 25, 'WATER', '447', '524 STUDS', 'lime', '$1.3K', 'hide', ''],
    [0, 5, null, '1.5S', '1.2S', 'lock', 'REBIRTH 1', 'gold', '10'],
    [0, 1, null, '0 HITS', '1 HIT', 'lock', 'REBIRTH 10', 'gold', '50']],
    guide: { title: 'Upgrade SLINGSHOT POWER!', sub: 'Press the green $1.3K button', done: 9 } },
  max: { reb: 20, rows: [
    [25, 25, 'CELESTIAL', '2300 STUDS', null, 'max', 'MAX', 'hide', ''],
    [4, 5, null, '0.4S', '0.2S', 'off', '$500B', 'gold', '50'],
    [0, 1, null, '0 HITS', '1 HIT', 'lime', '$25B', 'refusal', ['TEST SAVE ONLY', 'TEST ONLY', 'TEST!']]] },
  refusal: { reb: 13, rows: [
    [24, 25, 'CELESTIAL', '2223', '2300 STUDS', 'refusal', ['NEED MORE $!', 'NEED $!'], 'gold', '1499'],
    [3, 5, null, '0.6S', '0.4S', 'lock', 'REBIRTH 13', 'gold', '40'],
    [0, 1, null, '0 HITS', '1 HIT', 'off', '$25B', 'gold', '50']] },
};
function upgrades(mode) {
  const S0 = U_STATES[mode];
  setup(740, 470, { capR: 0.6718, guide: S0.guide });
  const { F } = stage();
  const cv = canvasOf(F, 'UpgradesCanvas');
  ROWS.forEach((r, i) => {
    const [lv, max, area, now, nxt, ms, mt, rs, rt] = S0.rows[i];
    const f = card(cv, 10, 66 + 122 * i, 720, 114, 'Row_' + r.kind, { tile: 'rows', face: `linear-gradient(180deg,${mix('#3A3082', r.c, 0.15)},#29215F)` });
    glow(f, 6, 6, 88, 96, r.c, .4);
    sticker(r.icon, f, 18, 20, 64, 0, 'Icon');
    txt(f, r.name, 100, 10, 330, 22, { align: 'left', name: r.kind + '.Name' });
    txt(f, r.desc, 100, 38, 216, 16, { align: 'left', color: LAVD, name: r.kind + '.Desc' });
    if (area) txt(f, area, 308, 38, 112, 16, { align: 'right', color: AREA_C[area], name: r.kind + '.Area' });
    bar(f, 100, 64, 128, 30, lv / max, `LV ${lv}/${max}`, r.kind + '.Bar', 16, r.fill);
    if (nxt) nowNext(f, now, nxt, 236, 69, 184, 18, { align: 'left', name: r.kind + '.Stat' });
    else txt(f, now, 236, 69, 184, 18, { align: 'left', color: GOLD, name: r.kind + '.Stat' });
    const o = { d: 4, r: 12, size: 22, name: r.kind + '.Buy', tile: 'btns' }; // (hoverScale 1: 8 px from the Robux button)
    if (ms === 'lime') button(f, 'lime', mt, 428, 25, 156, 60, Object.assign(o, { glyph: 'A:cash', glyphSize: 26 }));
    else if (ms === 'off') button(f, 'off', mt, 428, 25, 156, 60, Object.assign(o, { glyph: 'A:cash', glyphSize: 26 }));
    else if (ms === 'lock') button(f, 'off', mt, 428, 25, 156, 60, Object.assign(o, { glyph: 'locked', glyphSize: 24 }));
    else if (ms === 'max') button(f, 'silver', mt, 428, 25, 156, 60, o);
    else if (ms === 'free') button(f, 'lime', mt, 428, 25, 156, 60, Object.assign(o, { size: 26 }));
    else if (ms === 'refusal') button(f, 'red', mt, 428, 25, 156, 60, o);
    const ro = { d: 4, r: 12, size: 20, top: '+1 LV', topSize: 16, name: r.kind + '.Robux', tile: 'btns' };
    if (rs === 'gold') button(f, 'gold', rt, 592, 25, 118, 60, Object.assign(ro, { glyph: 'robux_white', glyphSize: 20 }));
    else if (rs === 'refusal') button(f, 'red', rt, 592, 25, 118, 60, Object.assign(ro, { top: null, size: 20 }));
    if (i === 0 && S0.arrow) { // the tutorial arrow in the (hidden) Robux slot, pointing left at the money button; bob +12 px
      const a = img('tut_arrow', f, 622, 31, 48, 48); a.dataset.ol = 0; a.dataset.name = 'FreeArrow'; // (bob +12 -> 682 < 710)
      a.style.transform = 'rotate(180deg)'; // (stand-in = the right arrow; the build: the down arrow 93838363576146, Rotation 90)
    }
  });
  txt(cv, 'UPGRADES ARE YOURS FOREVER - EVEN AFTER A REBIRTH!', 10, 432, 720, 16, { color: LAVD, name: 'Foot' });
  chrome(F, 'Upgrades', 'UPGRADES', 'boost');
  // the REBIRTH n pill in the band (HatchFront, not a button: flat violet, no depth / gloss)
  const pill = h('div', 'abs', F, { data: { ol: 2, name: 'RebirthPill', c: '1' } }); pos(pill, 520, 9, 160, 28);
  Object.assign(pill.style, { borderRadius: '14px', background: 'linear-gradient(180deg,#D680FF,#9632DC)', boxShadow: '0 0 0 2px var(--ink), inset 0 1.5px 0 #F0C8FF' });
  fitTxt(pill, ['REBIRTH ' + S0.reb, 'R ' + S0.reb], 0, 4, 160, 18, { name: 'RebirthPill.Label' });
  qa([`state ${mode}`]);
}

// ---------------------------------------------------------------- the button / state sheet (all three windows)
function sheet() {
  setup(740, 470);
  const { F } = stage();
  const cv = canvasOf(F, 'Sheet');
  const L = (s, x, y) => txt(cv, s, x, y, 360, 16, { align: 'left', color: LAVD, name: 'L_' + s });
  L('UPGRADES $ BUY', 14, 64); L('+1 LV ROBUX', 14, 236);
  const states = [['lime', '$150K', 'A:cash'], ['off', '$500B', 'A:cash'], ['off', 'REBIRTH 13', 'locked'], ['silver', 'MAX'], ['lime', 'FREE!'], ['red', ['NEED MORE $!', 'NEED $!']]];
  states.forEach((s, i) => {
    const x = 14 + (i % 4) * 178, y = 88 + Math.floor(i / 4) * 72;
    button(cv, s[0], s[1], x, y, 156, 60, Object.assign({ d: 4, r: 12, size: s[1] === 'FREE!' ? 26 : 22, name: 'S' + i, tile: 'sheet1' }, s[2] ? { glyph: s[2], glyphSize: s[2] === 'locked' ? 24 : 26 } : {}));
  });
  button(cv, 'gold', '15', 14, 260, 118, 60, { d: 4, r: 12, size: 20, top: '+1 LV', glyph: 'robux_white', glyphSize: 20, name: 'R1', tile: 'sheet2' });
  button(cv, 'gold', '1499', 142, 260, 118, 60, { d: 4, r: 12, size: 20, top: '+1 LV', glyph: 'robux_white', glyphSize: 20, name: 'R2', tile: 'sheet2' });
  button(cv, 'red', ['TEST SAVE ONLY', 'TEST ONLY', 'TEST!'], 270, 260, 118, 60, { d: 4, r: 12, size: 20, name: 'R3', tile: 'sheet2' });
  L('FREE GIFT JOIN', 400, 236);
  button(cv, 'violet', 'JOIN', 400, 260, 134, 44, { d: 4, r: 12, size: 22, name: 'J', tile: 'sheet2' });
  L('WELCOME BACK x5 (OWNER CALL)', 14, 336);
  button(cv, 'gold', '39', 14, 360, 276, 64, { d: 4, r: 12, size: 26, glyph: 'robux_white', glyphSize: 28, pre: 'CLAIM x5!', name: 'X1', tile: 'sheet3' });
  const rb = button(cv, 'gold', '39', 302, 360, 276, 64, { d: 4, r: 12, size: 26, glyph: 'robux_white', glyphSize: 28, pre: 'CLAIM x5!', name: 'X2', tile: 'sheet3' });
  rb.face.style.background = 'linear-gradient(110deg,#FF1E50,#FF8C00,#FFE600,#28E632,#00D2FF,#5A3CFF,#DC00E6)';
  txt(cv, 'GOLD (DEFAULT)', 14, 432, 276, 16, { color: GOLD, name: 'LG' });
  txt(cv, 'RAINBOW (X5_STYLE)', 302, 432, 276, 16, { color: LAVD, name: 'LR' });
  chrome(F, 'Upgrades', 'BUTTON STATES', 'boost');
  qa();
}

const VIEWS = {
  freegift: () => freegift('join'), freegift_joined: () => freegift('joined'), freegift_claimed: () => freegift('claimed'),
  freegift_refusal: () => freegift('refusal'),
  welcome: () => welcome('normal'), welcome_big: () => welcome('big'), welcome_x5: () => welcome('x5'), welcome_refusal: () => welcome('refusal'),
  upgrades: () => upgrades('mid'), upgrades_free: () => upgrades('free'), upgrades_step10: () => upgrades('step10'),
  upgrades_max: () => upgrades('max'), upgrades_refusal: () => upgrades('refusal'), sheet,
};
document.fonts.load('20px GB').then(() => (VIEWS[VIEW] || VIEWS.freegift)());
