// =====================================================================================================================
// HATCH NIGHT Rebirth / Index / Settings (planner mockups 2026-10-21). Same recipe as ../popup_shop (engine.js copy).
// Plan: docs/plans/2026-10-21-hatch-night-rebirth-index-settings.md (every rect below = a plan table row).
// Stand-in art: tile icons from Desktop/SLINGSHOT Icons/out (the live tile icons differ), paw + red X drawn,
// Venom Basilisk = Storm Wyvern portrait, egg icons = egg.png hue-shifted, Settings gear = the old 3D gear.
// URL: ris.html?view=<view>&dev=pc|phone&qa=1
// =====================================================================================================================
BANDS.Rebirth = { band: 'linear-gradient(180deg,#CE78FF 0%,#A028FF 55%,#7000D6 100%)', tooth: '#7000D6' };
BANDS.Index = { band: 'linear-gradient(180deg,#6EE6FF 0%,#00BEFF 55%,#0078EB 100%)', tooth: '#0078EB' };
BANDS.Settings = { band: 'linear-gradient(180deg,#C4C0EC 0%,#968ED6 55%,#6860B0 100%)', tooth: '#6860B0' };
const LIME = 'var(--lime)', GOLD = 'var(--gold)', RED = 'var(--red)', LAV = 'var(--lav)', LAVD = 'var(--lav-dim)';

// H.segment / H.arrow (18 x 22, k = size factor; flip = the "<" arrow, Rotation 180)
function seg(parent, ax, ay, bx, by, th, color) {
  const dx = bx - ax, dy = by - ay, L = Math.hypot(dx, dy) + th / 2;
  const e = h('div', 'abs', parent); pos(e, (ax + bx) / 2 - L / 2, (ay + by) / 2 - th / 2, L, th);
  e.style.background = color; e.style.borderRadius = th / 2 + 'px';
  e.style.transform = `rotate(${Math.atan2(dy, dx) * 180 / Math.PI}deg)`;
}
function arrow(parent, x, y, k, name, flip) {
  k = k || 1;
  const a = h('div', 'abs', parent, { data: { ol: 0, name: name || 'Arrow' } }); pos(a, x, y, 18 * k, 22 * k);
  if (flip) a.style.transform = 'rotate(180deg)';
  const P = [[4, 4], [14, 11], [4, 18]].map(p => [p[0] * k, p[1] * k]);
  for (const [th, c] of [[7 * k, 'var(--ink)'], [3.2 * k, '#B8FF6A']]) { seg(a, ...P[0], ...P[1], th, c); seg(a, ...P[1], ...P[2], th, c); }
  return a;
}
// H.nowNext: "now" + lime chevron + "next" as one group (left or centred in w); returns the group width
function nowNext(parent, now, nxt, x, y, w, size, o) {
  o = o || {};
  const k = o.k || (size >= 24 ? 1 : 0.75);
  const t1 = measure(now, size), t2 = nxt ? measure(nxt, size) : 0; // (the builder measures with H.textWidth = the real font)
  const G = (t1 + 8) + (nxt ? 2 + 18 * k + 4 + t2 + 8 : 0);
  const x0 = o.align === 'left' ? x : x + (w - G) / 2;
  txt(parent, now, x0, y, t1 + 8, size, { align: 'left', color: o.c1, name: (o.name || 'NN') + '.Now' }).dataset.skipfill = 1;
  if (nxt) {
    arrow(parent, x0 + t1 + 10, y + (size + 2 - 22 * k) / 2, k, (o.name || 'NN') + '.Arrow');
    txt(parent, nxt, x0 + t1 + 14 + 18 * k, y, t2 + 8, size, { align: 'left', color: o.c2 || LIME, name: (o.name || 'NN') + '.Next' }).dataset.skipfill = 1;
  }
  return G;
}
// H.progressBar: recess trough (r = h/2) + lime gloss fill (min width h - 6, hidden at 0) + centred text
function bar(parent, x, y, w, hh, k, text, name, size) {
  size = size || 16;
  const r = recess(parent, x, y, w, hh, hh / 2, name);
  if (k > 0) {
    const f = h('div', 'abs', r, { data: { ol: 0, name: name + '.Fill' } });
    pos(f, 3, 3, Math.max(hh - 6, (w - 6) * Math.min(k, 1)), hh - 6);
    f.style.borderRadius = (hh - 6) / 2 + 'px';
    f.style.background = 'linear-gradient(180deg,#B4FF4A,#4FCB10)';
    f.style.boxShadow = 'inset 0 2px 0 rgba(255,255,255,.45)';
  }
  txt(r, text, 0, Math.round((hh - size - 2) / 2), w, size, { name: name + '.Text' });
  return r;
}
function canvas(F, name) { const c = h('div', 'abs', F, { data: { c: '1', name } }); pos(c, 0, 0, 740, 463); return c; }

// ---------------------------------------------------------------- SETTINGS (plan 4.1)
function settings(mode) {
  const { F } = stage();
  const cv = canvas(F, 'SettingsPage');
  const off = mode === 'off';
  const rows = [
    ['music', 'MUSIC', 'BACKGROUND MUSIC', 'toggle', off ? ['off', 'OFF'] : ['lime', 'ON']],
    ['volume', 'VOLUME', 'MUSIC LOUDNESS', 'volume', off ? 0 : 0.7],
    ['song', 'SONG', 'PICK THE MUSIC', 'song', off ? 'RACE TO FINISH' : 'ALL SONGS'],
    ['sfx', 'SOUNDS', 'SOUND EFFECTS', 'toggle', off ? ['off', 'OFF'] : ['lime', 'ON']],
    ['night', 'TIME', 'DAY OR NIGHT SKY', 'toggle', off ? ['violet', 'NIGHT'] : ['gold', 'DAY']],
  ];
  rows.forEach(([key, title, sub, kind, val], i) => {
    const f = card(cv, 10, 66 + i * 78, 720, 70, 'Row_' + key, { tile: 'rows' });
    txt(f, title, 22, 10, 300, 22, { align: 'left', name: key + '.Title' });
    txt(f, sub, 22, 36, 300, 16, { align: 'left', color: LAVD, name: key + '.Sub' });
    if (kind === 'toggle') {
      button(f, val[0], val[1], 524, 9, 188, 48, { d: 4, r: 12, size: 20, color: val[0] === 'off' ? LAVD : undefined, name: key + '.Toggle' });
    } else if (kind === 'volume') {
      // "-" / "+" are drawn lime bars with an ink edge (H.segment), not glyphs: a GothamBlack "-" is a thin dash
      const mi = gbtn(f, 'dusk', 420, 9, 48, 48, { d: 4, r: 12, name: 'Minus', tile: 'ctl' });
      seg(mi.face, 15, 22, 33, 22, 8, 'var(--ink)'); seg(mi.face, 15, 22, 33, 22, 4, '#B8FF6A');
      bar(f, 476, 15, 180, 36, val, Math.round(val * 100) + '%', 'VolBar', 18);
      const pl = gbtn(f, 'dusk', 664, 9, 48, 48, { d: 4, r: 12, name: 'Plus', tile: 'ctl' });
      for (const [th, c] of [[8, 'var(--ink)'], [4, '#B8FF6A']]) { seg(pl.face, 15, 22, 33, 22, th, c); seg(pl.face, 24, 13, 24, 31, th, c); }
    } else {
      const pv = gbtn(f, 'dusk', 420, 9, 48, 48, { d: 4, r: 12, name: 'Prev', tile: 'ctl' }); arrow(pv.face, 15, 11, 1, 'PrevArrow', true);
      const nb = recess(f, 476, 15, 180, 36, 18, 'NameBox'); txt(nb, val, 0, 8, 180, 18, { name: 'SongName' });
      const nx = gbtn(f, 'dusk', 664, 9, 48, 48, { d: 4, r: 12, name: 'Next', tile: 'ctl' }); arrow(nx.face, 15, 11, 1, 'NextArrow');
    }
  });
  chrome(F, 'Settings', 'SETTINGS', 'settings');
  qa();
}

// ---------------------------------------------------------------- INDEX (plan 5.1)
const AREAS = [
  { name: 'GRASS', c: '#78E65A', egg: 'WOOD EGG', f: 'none', prog: '3/5' },
  { name: 'WATER', c: '#5AC8FF', egg: 'TIDE EGG', f: 'hue-rotate(110deg)', prog: '5/5', star: true },
  { name: 'THUNDER', c: '#FFE650', egg: 'STORM EGG', f: 'hue-rotate(-50deg) saturate(1.4)', prog: '5/5', dot: true },
  { name: 'FIRE', c: '#FF8C3C', egg: 'MAGMA EGG', f: 'hue-rotate(-95deg) saturate(1.6)', prog: '0/5' },
  { name: 'SHADOW', c: '#AA64F0', egg: 'VOID EGG', f: 'hue-rotate(170deg) brightness(.8)', prog: '0/5' },
  { name: 'CELESTIAL', c: '#FFF0AA', egg: 'CELESTIAL EGG', f: 'hue-rotate(-40deg) brightness(1.3) saturate(.6)', prog: '0/5' },
];
const GRASS = [
  { pet: 'pet_MossbackTortoise', name: 'MOSSBACK TORTOISE', pct: '52%' },
  { pet: 'pet_ForestStag', name: 'FOREST STAG', pct: '28%' },
  { pet: 'pet_Treant', name: 'TREANT', pct: '13%' },
  { pet: 'pet_StormWyvern', name: 'VENOM BASILISK', pct: '5%' },
  { pet: 'A:mantis', name: 'THORNBLADE MANTIS', pct: '2%', secret: true },
];
function index(mode) {
  const { F } = stage();
  const cv = canvas(F, 'IndexPage');
  const all = mode === 'claim';
  const known = all ? [1, 1, 1, 1, 1] : [1, 1, 1, 0, 0];
  const sel = all ? 4 : 2;
  // left rail: recess 10, 66, 116, 342; 6 slots of 56 (T = 3 + 56 (i-1)); the lime pill on the active slot
  const rail = recess(cv, 10, 66, 116, 342, 20, 'Rail');
  AREAS.forEach((a, i) => {
    const T = 3 + 56 * i, on = i === 0;
    if (on) gbtn(rail, 'lime', 3, T, 110, 56, { d: 3, r: 16, ol: 2, name: 'Pill' });
    txt(rail, a.name, 2, T + 8, 112, 16, { color: on ? '#fff' : a.c, name: 'Name' + (i + 1) });
    sticker('A:egg', rail, 12, T + 29, 22, 0, 'Egg' + (i + 1), { filter: a.f + ' drop-shadow(0 3px 0 rgba(6,4,20,.55))' });
    const pr = on && all ? '5/5' : a.prog;
    txt(rail, pr, 38, T + 31, 48, 16, { align: 'left', color: on ? '#fff' : LAV, name: 'Prog' + (i + 1) });
    if (a.star && !on) sticker('A:star', rail, 88, T + 30, 20, 0, 'Star' + (i + 1));
    if ((a.dot && !on) || (on && all)) {
      const d = h('div', 'dot', rail, { data: { ol: 2, name: 'Dot' + (i + 1) } }); pos(d, 88, T + 30, 20, 20);
      txt(d, '!', 0, 1.5, 20, 15, { stroke: 's15', name: 'Mark' }).dataset.skipfill = 1;
    }
  });
  // centre column x 134..500
  const head = card(cv, 134, 66, 366, 50, 'AreaHead');
  glow(head, 4, 2, 46, 41, AREAS[0].c, .45);
  sticker('A:egg_grass', head, 8, 3, 36, 0, 'HeadEgg');
  txt(head, 'GRASS', 52, 3, 170, 20, { align: 'left', color: AREAS[0].c, name: 'AreaTitle' });
  txt(head, 'WOOD EGG', 52, 24, 170, 16, { align: 'left', color: LAVD, name: 'AreaSub' });
  bar(head, 226, 10, 130, 26, all ? 1 : 0.6, all ? '5 / 5' : '3 / 5', 'AreaBar');
  GRASS.forEach((c, i) => {
    const x = 134 + i * 74.8, k = known[i];
    const cf = card(cv, x, 124, 66.8, 142, 'Card' + (i + 1), { tile: 'cards',
      face: c.secret ? (k ? 'linear-gradient(180deg,#8A6A1E,#5A3A10)' : 'linear-gradient(180deg,#4A3A22,#2E2414)') : undefined });
    if (k) glow(cf, 3.4, 18, 60, 64, c.secret ? '#FFD65A' : AREAS[0].c, .45);
    const pd = h('div', 'ped', cf); pos(pd, 8.4, 76, 50, 10);
    if (c.secret) sticker('A:star', cf, 24.4, 2, 18, 0, 'SecretStar');
    sticker(c.pet, cf, 4.4, 22, 58, 0, 'Portrait', k ? {} : { filter: 'brightness(0) opacity(.85) drop-shadow(0 3px 0 rgba(6,4,20,.55))' });
    if (!k) txt(cf, '?', 4.4, 38, 58, 26, { name: 'Q' }).dataset.skipfill = 1;
    txt(cf, c.pct, 0, 102, 66.8, 16, { name: 'Pct' });
    if (i === sel) { const r = h('div', 'sel-ring', cf, { data: { ol: 0, name: 'Ring' } }); pos(r, 3, 3, 60.8, 131); }
  });
  const st = card(cv, 134, 274, 366, 134, 'Reward');
  txt(st, 'COMPLETE GRASS:', 12, 10, 342, 18, { align: 'left', color: GOLD, name: 'RewardTitle' });
  [['A:cash', '+5%'], ['A:shoe', '+5%'], ['A:potion_gold', 'x1'], ['A:potion_green', 'x1']].forEach(([ic, t], i) => {
    const ch = chip(st, 11 + i * 88, 38, 80, 32, 'Chip' + (i + 1), 'chips'); ch.style.borderRadius = '16px';
    sticker(ic, ch, 6, 2, 24, 0, 'Icon');
    txt(ch, t, 32, 7, 44, 16, { align: 'left', name: 'ChipText' });
  });
  if (all) button(st, 'lime', 'CLAIM!', 12, 82, 342, 40, { d: 4, r: 12, size: 20, name: 'Claim' });
  else button(st, 'off', '2 LEFT', 12, 82, 342, 40, { d: 4, r: 12, size: 20, color: LAVD, name: 'Claim' });
  const tot = recess(cv, 10, 416, 490, 38, 19, 'Total');
  sticker('book', tot, 8, 2, 30, 0, 'Book');
  bar(tot, 46, 8, 272, 22, all ? 15 / 30 : 13 / 30, all ? 'DISCOVERED 15 / 30' : 'DISCOVERED 13 / 30', 'TotalBar');
  button(tot, 'gold', all ? 'CLAIM ALL (2)' : 'CLAIM ALL (1)', 326, 3, 160, 32, { d: 3, r: 14, ol: 2, size: 16, name: 'ClaimAll' });
  // inspect panel 508, 66, 222, 388 (face 383)
  const c = GRASS[sel], k = known[sel];
  const ins = card(cv, 508, 66, 222, 388, 'Inspect', { face: '#1F1852' });
  const ped = h('div', 'ped', ins); pos(ped, 51, 146, 120, 14);
  if (k) glow(ins, 21, 4, 180, 160, c.secret ? '#FFD65A' : AREAS[0].c, .45);
  sticker(c.pet, ins, 36, 6, 150, 0, 'BigPortrait', k ? {} : { filter: 'brightness(0) opacity(.85)' });
  const badges = [];
  if (c.secret) badges.push(['tag', 92]);
  badges.push(['bonus', 76]);
  let bx = (222 - badges.reduce((s, b) => s + b[1], 0) - 8 * (badges.length - 1)) / 2;
  badges.forEach(([kind, w]) => {
    if (kind === 'tag') tag(ins, 'SECRET!', bx, 164, w, 'SecretTag');
    else {
      const ch = chip(ins, bx, 164, w, 22, 'Bonus', 'badges'); ch.style.borderRadius = '11px';
      sticker('A:cash', ch, 6, 0, 20, 0, 'BonusIcon');
      txt(ch, c.secret ? 'x3.1' : 'x1.6', 30, 2, 42, 16, { align: 'left', color: LIME, name: 'BonusText' });
    }
    bx += w + 8;
  });
  const parts = c.name.length > 14 ? c.name.split(' ') : [c.name];
  if (parts.length > 1) {
    txt(ins, parts.slice(0, -1).join(' '), 8, 194, 206, 18, { name: 'Name1' });
    txt(ins, parts[parts.length - 1], 8, 214, 206, 18, { name: 'Name2' });
  } else txt(ins, k ? c.name : '???', 8, 204, 206, 18, { name: 'Name1' });
  const stats = c.secret ? [['INCOME', '$4.8K/s'], ['BEST KG', '1.2K KG'], ['HATCHED', 'x1'], ['CHANCE', '2%']]
                         : [['INCOME', '$1.6K/s'], ['BEST KG', '2.4K KG'], ['HATCHED', 'x3'], ['CHANCE', '13%']];
  stats.forEach(([l, v], i) => {
    const r = chip(ins, 8, 240 + i * 34, 206, 26, 'Stat' + (i + 1), 'stats'); r.style.borderRadius = '13px';
    txt(r, l, 8, 4, 100, 16, { align: 'left', color: LAVD, name: 'L' });
    txt(r, v, 104, 4, 94, 16, { align: 'right', color: i === 0 ? LIME : '#fff', name: 'V' });
  });
  chrome(F, 'Index', 'CREATURE INDEX', 'index');
  qa();
}

// ---------------------------------------------------------------- REBIRTH (plan 6.1)
const TILES = [
  { key: 'slots', name: 'PET SLOT', icon: 'paw', c: '#FFBA46' },
  { key: 'speed', name: 'SPEED', icon: 'A:shoe', c: '#FF78E1' },
  { key: 'money', name: 'MONEY', icon: 'A:cash', c: '#82EB5F' },
  { key: 'base', name: 'BASE SIZE', icon: 'house', c: '#64C8FF' },
];
const R_STATES = {
  pc: { r: 0, nr: 1, vals: [['+1', '3', '4'], ['x1.25', 'x1', 'x1.25'], ['x1.25', 'x1', 'x1.25'], ['+1', '0/5', '1/5']],
    pet: null, money: [0.48, '$12K / $25K', false], ready: false },
  ready: { r: 0, nr: 1, vals: [['+1', '3', '4'], ['x1.25', 'x1', 'x1.25'], ['x1.25', 'x1', 'x1.25'], ['+1', '0/5', '1/5']],
    pet: null, money: [1, '$25K / $25K', true], ready: true, arrow: true },
  need: { r: 3, nr: 4, vals: [['+1', '6', '7'], ['x2', 'x1.75', 'x2'], ['x2', 'x1.75', 'x2'], ['+1', '3/5', '4/5']],
    pet: ['THUNDER PET', '#FFE650', 'NEEDS 1K+ KG', false], money: [0.62, '$11.2M / $18M', false], ready: false },
  confirm: { r: 3, nr: 4, vals: [['+1', '6', '7'], ['x2', 'x1.75', 'x2'], ['x2', 'x1.75', 'x2'], ['+1', '3/5', '4/5']],
    pet: ['THUNDER PET', '#FFE650', 'YOU HAVE ONE: 12.5K KG', true], money: [1, '$18M / $18M', true], ready: true, confirm: true },
  max: { r: 20, nr: 20, max: true, vals: [['23', 'MAX'], ['x6', 'MAX'], ['x6', 'MAX'], ['MAX', 'BIGGEST BASE']] },
};
function rebirth(mode) {
  const { F } = stage();
  const cv = canvas(F, 'RebirthPage');
  const S0 = R_STATES[mode];
  // hero: rays + glow + gold medallion (84, round, depth 4) with the next rebirth number
  const rays = img('A:rays', cv, 26, 64, 120, 120, { opacity: .55, filter: 'sepia(1) saturate(3) brightness(1.1)' });
  rays.dataset.ol = 0; rays.dataset.name = 'Rays';
  glow(cv, 36, 74, 100, 100, '#FFD65A', .35);
  const med = gbtn(cv, 'gold', 44, 82, 84, 88, { d: 4, r: 42, ol: 3, name: 'Medallion' });
  const ring = h('div', 'coin-ring', med.face, { data: { ol: 0, name: 'CoinRing' } }); pos(ring, 7, 7, 70, 70);
  txt(med.face, S0.max ? 'MAX' : String(S0.nr), 0, S0.max ? 28 : 20, 84, S0.max ? 24 : 40, { stroke: 's3', name: 'MedNum' });
  if (S0.max) nowNext(cv, 'MAX REBIRTH', '20', 148, 80, 560, 28, { align: 'left', c2: GOLD, name: 'Head', k: 1 });
  else nowNext(cv, 'REBIRTH ' + S0.r, String(S0.nr), 148, 80, 560, 28, { align: 'left', name: 'Head', k: 1 });
  const lines = S0.max ? [['YOU REACHED THE TOP!', GOLD], ['LEGEND!', LIME]]
    : S0.confirm ? [['TAP AGAIN TO REBIRTH!', GOLD], ['MONEY + SPEED RESET!', RED]]
    : [['MONEY + SPEED RESET!', RED], ['YOU KEEP EVERYTHING ELSE!', LIME]];
  txt(cv, lines[0][0], 148, 116, 560, 18, { align: 'left', color: lines[0][1], name: 'LineA' });
  txt(cv, lines[1][0], 148, 138, 560, 18, { align: 'left', color: lines[1][1], name: 'LineB' });
  // YOU WILL GET (centred, faint lines both sides)
  const gl = S0.max ? 'YOUR REWARDS' : 'YOU WILL GET', gw = measure(gl, 18) * GE;
  txt(cv, gl, 270, 176, 200, 18, { color: GOLD, name: 'GetLabel' });
  for (const [x0, x1, n] of [[10, 370 - gw / 2 - 14, 'GetLineL'], [370 + gw / 2 + 14, 730, 'GetLineR']]) {
    const l = h('div', 'abs', cv, { data: { ol: 0, name: n } }); pos(l, x0, 184, x1 - x0, 2);
    l.style.background = 'rgba(140,125,255,.35)'; l.style.borderRadius = '1px';
  }
  // 4 reward cards (174 x 122, face 117)
  TILES.forEach((t, i) => {
    const f = card(cv, 10 + i * 182, 200, 174, 122, 'Reward_' + t.key, { tile: 'rewards' });
    glow(f, 6, 4, 68, 68, t.c, .45);
    sticker(t.icon, f, 14, 12, 52, 0, 'Icon');
    const v = S0.vals[i];
    txt(f, v[0], 74, 14, 92, 28, { align: 'left', name: 'Value' });
    txt(f, t.name, 8, 68, 158, 16, { color: t.c, name: 'Name' });
    if (S0.max) txt(f, v[1], 8, 90, 158, 16, { color: GOLD, name: 'Line' });
    else nowNext(f, v[1], v[2], 8, 90, 158, 16, { name: 'Line' });
  });
  // needs row: pet card (if the level needs one) + the money card, 356 x 56 chips
  if (!S0.max) {
    let mx = 192;
    if (S0.pet) {
      mx = 374;
      const pc = chip(cv, 10, 330, 356, 56, 'NeedPet', 'needs'); pc.style.borderRadius = '16px';
      const rg = h('div', 'ring', pc, { data: { ol: 2, name: 'Ring', c: '1' } }); pos(rg, 8, 6, 44, 44);
      rg.style.background = 'linear-gradient(180deg,#FFE650,#D28214)';
      sticker('pet_StormWyvern', rg, 2, 1, 40, 0, 'Pet', S0.pet[3] ? {} : { filter: 'brightness(0.12) drop-shadow(0 3px 0 rgba(6,4,20,.55))' });
      txt(pc, S0.pet[0], 60, 8, 248, 18, { align: 'left', color: S0.pet[1], name: 'PetTitle' });
      txt(pc, S0.pet[2], 60, 30, 248, 16, { align: 'left', color: LAV, name: 'PetSub' });
      sticker(S0.pet[3] ? 'A:check' : 'x_red', pc, 314, 12, 32, 0, 'PetStatus');
    }
    const mc = chip(cv, mx, 330, 356, 56, 'NeedMoney', 'needs'); mc.style.borderRadius = '16px';
    sticker('A:cash', mc, 8, 6, 40, 0, 'Cash');
    bar(mc, 56, 14, 248, 28, S0.money[0], S0.money[1], 'CostBar');
    sticker(S0.money[2] ? 'A:check' : 'x_red', mc, 314, 12, 32, 0, 'MoneyStatus');
  }
  // buttons
  if (S0.max) button(cv, 'silver', 'MAX', 120, 394, 500, 60, { d: 4, r: 12, size: 26, name: 'Rebirth' });
  else if (S0.ready) {
    const b = button(cv, 'lime', S0.confirm ? 'TAP AGAIN!' : 'REBIRTH!', 120, 394, 500, 60, { d: 4, r: 12, size: 26, name: 'Rebirth' });
    const sh = h('div', 'abs', b.face); pos(sh, 0, 0, 500, 56);
    sh.style.background = 'linear-gradient(110deg,transparent 40%,rgba(255,255,255,.45) 50%,transparent 60%)';
    if (S0.arrow) {
      const a = img('tut_arrow', cv, 640, 400, 48, 48); a.dataset.ol = 0; a.dataset.name = 'TutorialArrow'; // x 640: clear of the 1.04 pulse (110..630) + 12 px bob
      a.style.transform = 'rotate(180deg)';
    }
  } else {
    button(cv, 'gold', '20', 10, 394, 236, 60, { d: 4, r: 12, size: 26, robux: true, glyph: 28, pre: 'SKIP', name: 'Skip', tile: 'btns' });
    button(cv, 'off', 'REBIRTH!', 254, 394, 476, 60, { d: 4, r: 12, size: 26, color: LAVD, name: 'Rebirth', tile: 'btns' });
  }
  chrome(F, 'Rebirth', 'REBIRTH', 'rebirth');
  qa();
}

const VIEWS = {
  settings: () => settings('on'), settings_off: () => settings('off'),
  index: () => index('pc'), index_claim: () => index('claim'),
  rebirth: () => rebirth('pc'), rebirth_ready: () => rebirth('ready'), rebirth_need: () => rebirth('need'),
  rebirth_confirm: () => rebirth('confirm'), rebirth_max: () => rebirth('max'),
};
document.fonts.load('20px GB').then(() => (VIEWS[VIEW] || VIEWS.settings)());
