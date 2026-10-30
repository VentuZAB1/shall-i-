# applies STYLE_BIBLE.md section 2 (kit spec) to blockkit.py
import sys, re
p = sys.argv[1]
t = open(p, encoding="utf-8").read()

# ---- 1. STYLE
a = t.index("STYLE = {")
b = t.index("}\n", a) + 2
t = t[:a] + '''STYLE = {   # numbers from STYLE_BIBLE.md section 2 (art director, 2026-10-08)
    # rounding by role: (bevel x h_min, segments, smooth). role auto: h_min >= .10 TH mass, >= .035 TH limb, else detail
    "roles": {"mass": (0.22, 3, True), "limb": (0.18, 2, True), "detail": (0.12, 1, False)},
    "smooth_angle": 30,          # edges between two smooth faces flatter than this shade smooth
    "cell_th": 0.18,             # plate grid cell = 0.18 x torso height (one cell size per pet)
    "plate_gap": 0.38,           # gap between plates, fraction of a cell (a 1x1 plate = 0.62 cell)
    "relief": 0.186,             # plate relief = 0.186 cell (= 0.30 x the 1x1 plate width), min 0.02
    "plate_margin": 0.30,        # plate keep-off from a face edge: bevel + 0.30 cell
    "fill": {1: .55, 2: .60, 3: .65, 4: .70, 5: .72, 6: .75, "S": .45},
    "mix": (0.60, 0.25, 0.15),   # 1x1 | 1x2 vertical | 2x1
    "mix2x2": 0.10, "big_tiers": (4, 5, 6),
    "plate_jit": 0.03,           # per-plate brightness jitter
    "plate_foot": 0.90, "plate_top": 1.08,   # fake light: plate foot darker, plate top lighter
    "eyes": {   # x HW. outline / iris / pupil (w, h), highlights (big, small), centre x, centre z (x HH), tilt deg,
                # wedge (top width factor), brow (w, h, deg) or None
        "lovely": {"outline": (0.30, 0.32), "iris": (0.22, 0.25), "pupil": (0.11, 0.14), "hl": (0.08, 0.04),
                   "x": 0.24, "z": 0.55, "tilt": 0, "wedge": 1.0, "brow": None},
        "bold": {"outline": (0.28, 0.28), "iris": (0.20, 0.21), "pupil": (0.10, 0.12), "hl": (0.07, 0.035),
                 "x": 0.25, "z": 0.58, "tilt": 0, "wedge": 1.0, "brow": (0.26, 0.05, 6)},
        "fierce": {"outline": (0.30, 0.20), "iris": (0.22, 0.13), "pupil": (0.05, 0.13), "hl": (0.06, 0.0),
                   "x": 0.25, "z": 0.62, "tilt": 14, "wedge": 0.72, "brow": (0.30, 0.06, 20)},
    },
}
''' + t[b:]

# ---- 2. Block: bevel None = auto, role, pvar
old = '''                 bevel=0.03, studs=None, density=0.5, glow=None, name="", R=None, rnd=None, pstyle=None):'''
new = '''                 bevel=None, studs=None, density=0.5, glow=None, name="", R=None, rnd=None, pstyle=None, role=None,
                 pvar=None):'''
assert old in t; t = t.replace(old, new)
old = '''        self.pstyle = pstyle        # plate layout: None/"scatter" (random 1x1..2x2) | "mason" (dense staggered bricks)
'''
new = '''        self.pstyle = pstyle        # (legacy, ignored by the bible plates)
        self.role = role            # "mass" | "limb" | "detail" | None (auto from size vs torso height)
        self.pvar = pvar            # plate variant: None | "diamond" (scales) | "flush" (fake inset squares)
        self._role, self._off, self._segs, self._smooth = "detail", 0.0, 1, False
'''
assert old in t; t = t.replace(old, new)

# ---- 3. _box_bm uses the resolved bevel
old = t[t.index("    mn = min(blk.h.x * min(blk.top[0], blk.bot[0])"):t.index("    return bm\n\n\ndef _stud(")]
new = '''    if blk._off > 0.004:
        bmesh.ops.bevel(bm, geom=list(bm.edges), offset=blk._off, offset_type="OFFSET", segments=blk._segs,
                        profile=0.5, affect="EDGES", clamp_overlap=True)
    for f in bm.faces:
        f.smooth = blk._smooth
'''
t = t.replace(old, new)

# ---- 4. new plate geometry
old = "def frame_from(p0, p1, n):"
new = '''def _plate(bm, L, ctr, u, v, n, a, b, hgt, color, jit=1.0, flush=False):
    """bible plate: straight wall for the lower half, chamfered top (inset 0.30 min(a, b)); foot ring darker, top
    lighter (fake light). Flat shaded."""
    ins = 0.30 * min(a, b)
    def col(m):
        return tuple(min(1.0, c * m * jit) for c in color[:3]) + tuple(color[3:])
    if flush:
        rings_def = ((a, b, -0.004, 0.80), (a, b, hgt, 0.80))
    else:
        rings_def = ((a, b, -0.006, STYLE["plate_foot"]), (a, b, hgt * 0.5, 1.0),
                     (a - ins, b - ins, hgt, STYLE["plate_top"]))
    rings = []
    for da, db, dz, m in rings_def:
        ring = []
        for su, sv in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
            vt = bm.verts.new(ctr + u * (su * da) + v * (sv * db) + n * dz)
            vt[L] = col(m)
            ring.append(vt)
        rings.append(ring)
    for i in range(len(rings) - 1):
        for j in range(4):
            f = bm.faces.new((rings[i][j], rings[i][(j + 1) % 4], rings[i + 1][(j + 1) % 4], rings[i + 1][j]))
            f.smooth = False
    f = bm.faces.new(rings[-1])
    f.smooth = False


def frame_from(p0, p1, n):'''
t = t.replace(old, new, 1)

# ---- 5. Blocks init
old = '''    def __init__(self, k, cell=0.105, stud_h=0.03, seed=7):
        self.k = k
        self.items = []
        self.cell = cell
        self.stud_h = stud_h
        self.rnd = random.Random(seed)
        self.stud_count = 0'''
new = '''    def __init__(self, k, cell=0.105, stud_h=0.03, seed=7, th=None, tier=None):
        """th = torso height (auto: the biggest torso block), tier = 1..6 or "S" (plate fill, 2x2 plates).
        cell / stud_h are legacy (the bible derives both from th)."""
        self.k = k
        self.items = []
        self.cell = cell
        self.stud_h = stud_h
        self.th = th
        self.tier = tier if tier is not None else getattr(k, "tier", 2)
        self.rnd = random.Random(seed)
        self.stud_count = 0'''
assert old in t; t = t.replace(old, new)

# ---- 6. replace the old plate layout + keep eye(); insert bible plates + face_eyes
a = t.index("    def _studs_for(self, blk, bm, L):")
b = t.index("    def eye(self, c, normal")
t = t[:a] + open(sys.argv[2], encoding="utf-8").read() + "\n" + t[b:]

# ---- 7. eye(): blocks it makes are details with explicit bevels (bevel arg already passed), nothing to change

# ---- 8. head xf: bevel may be None
old = '''                    blk.h = blk.h * sc
                    blk.bevel *= sc'''
new = '''                    blk.h = blk.h * sc
                    if blk.bevel is not None:
                        blk.bevel *= sc'''
assert old in t; t = t.replace(old, new)

# ---- 9. build(): resolve TH, roles, bevels, plate cell; smooth flags
old = '''    def build(self):
        """one rigid part per (bone, glow) -> k.parts / k.glow"""
        self._apply_head_xf()'''
new = '''    TORSO_BONES = ("Spine", "Chest", "Body", "Hips", "Torso", "Pelvis")

    def _resolve(self):
        """torso height TH -> plate cell / relief; per block role, bevel offset, segments, smoothing"""
        boxes = [b for b in self.items if not isinstance(b, Poly)]
        if self.th is None:
            cand = [b for b in boxes if b.bone in self.TORSO_BONES] or boxes
            tor = max(cand, key=lambda b: b.h.x * b.h.y * b.h.z)
            zs = [tor.world(tor.local(sx, sy, sz)).z for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)]
            self.th = max(zs) - min(zs)
        TH = self.th
        self.pcell = STYLE["cell_th"] * TH
        self.pstud_h = max(STYLE["relief"] * self.pcell, 0.02)
        for b in boxes:
            mn = min(b.h.x * min(b.top[0], b.bot[0]), b.h.y * min(b.top[1], b.bot[1]), b.h.z)
            role = b.role or ("mass" if mn >= 0.10 * TH else "limb" if mn >= 0.035 * TH else "detail")
            frac, segs, smooth = STYLE["roles"][role]
            if b.rnd is not None:
                frac = b.rnd
            off = frac * mn
            if b.bevel is not None:
                off = max(off, b.bevel) if role != "detail" else b.bevel
            b._role, b._off, b._segs, b._smooth = role, min(off, mn * 0.45), segs, smooth
            if b._off <= 0.025 and segs > 1 and role != "mass":
                b._segs = 1

    def build(self):
        """one rigid part per (bone, glow) -> k.parts / k.glow"""
        self._apply_head_xf()
        self._resolve()'''
assert old in t; t = t.replace(old, new)
old = '''                    for f in tmp.faces:
                        try:
                            bm.faces.new([m[vt] for vt in f.verts])
                        except ValueError:
                            pass'''
new = '''                    for f in tmp.faces:
                        try:
                            nf = bm.faces.new([m[vt] for vt in f.verts])
                            nf.smooth = f.smooth
                        except ValueError:
                            pass'''
assert old in t; t = t.replace(old, new)
old = '''                if STYLE.get("smooth_angle"):      # rounded edges shade smooth, hard creases (plates, corners) stay sharp
                    lim = math.radians(STYLE["smooth_angle"])
                    for e in bm.edges:
                        if len(e.link_faces) == 2 and e.calc_face_angle(0.0) > lim:
                            e.smooth = False'''
new = '''                lim = math.radians(STYLE["smooth_angle"])    # soft masses, crisp details
                for e in bm.edges:
                    fs = e.link_faces
                    e.smooth = len(fs) == 2 and fs[0].smooth and fs[1].smooth and e.calc_face_angle(0.0) < lim'''
assert old in t; t = t.replace(old, new)
old = '''                o = self.k.part(name, build, bone, smooth_shade=bool(STYLE.get("smooth_angle")))'''
new = '''                o = self.k.part(name, build, bone, smooth_shade=False)'''
assert old in t; t = t.replace(old, new)

# ---- 10. header comment
t = t.replace('''# Style rules (from the user's 25+ reference images):
#   - built BIG: real proportions (long legs, real neck, moderate head) so a heavy KG pet looks huge, not a giant baby
#   - chunky blocks with small chamfered edges, flat shading, bright solid colours in clear zones
#   - small raised square studs scattered over the surfaces (fixed size -> they read as scale cues on big pets)
#   - small simple faces (square eyes / plates), rare pets get glow cracks, crystals, floating bits''',
'''# Style rules: STYLE_BIBLE.md (art director, 2026-10-08): soft rounded masses + crisp brick-grid plates, big heads,
# layered eyes (face_eyes), 4-5 colour zones, rarity by design (no glow; VFX = Roblox particles).''')
open(p, "w", encoding="utf-8").write(t)
print("ok")
