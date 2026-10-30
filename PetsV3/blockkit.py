# blockkit: Steal-an-Egg style pets for SLINGSHOT (PetsV3, 2026-10-08).
# Style rules: STYLE_BIBLE.md (art director, 2026-10-08): soft rounded masses + crisp brick-grid plates, big heads,
# layered eyes (face_eyes), 4-5 colour zones, rarity by design (no glow; VFX = Roblox particles).
# Every block is rigid on ONE bone (no rubbery skinning).
import math
import os, random
import bmesh, bpy
from mathutils import Vector, Matrix, Euler
import petkit as pk

NO_GLOW = True   # user 2026-10-08: glowing (Neon) parts look ugly -> every part is a normal solid colour
# PRO pass (2026-10-08, user: "should not look this LOW QUALITY"): rounded faceted base forms + Steal-an-Egg plates
STYLE = {   # numbers from STYLE_BIBLE.md section 2 (art director, 2026-10-08)
    # rounding by role: (bevel x h_min, segments, smooth). role auto: h_min >= .10 TH mass, >= .035 TH limb, else detail
    "roles": {"mass": (0.22, 3, True), "limb": (0.18, 2, True), "detail": (0.12, 1, False)},
    "smooth_angle": 30,          # edges between two smooth faces flatter than this shade smooth
    "cell_th": 0.19,             # plate grid cell = 0.18 x torso height (one cell size per pet)
    "plate_gap": 0.30,           # gap between plates, fraction of a cell (a 1x1 plate = 0.62 cell)
    "relief": 0.30,              # plate relief = 0.186 cell (= 0.30 x the 1x1 plate width), min 0.02
    "plate_margin": 0.15,        # plate keep-off from a face edge: bevel + 0.15 cell (bible 0.30 starved legs)
    "fill": {1: .55, 2: .60, 3: .65, 4: .70, 5: .72, 6: .75, "S": .45},
    "mix": (0.60, 0.25, 0.15),   # 1x1 | 1x2 vertical | 2x1
    "mix2x2": 0.10, "big_tiers": (4, 5, 6),
    "plate_jit": 0.03,           # per-plate brightness jitter
    "plate_foot": 0.84, "plate_top": 1.14,   # fake light: plate foot darker, plate top lighter
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
FACES = {"+x": (0, 1), "-x": (0, -1), "+y": (1, 1), "-y": (1, -1), "+z": (2, 1), "-z": (2, -1)}


def rgb(c):
    return pk.lin(c) if isinstance(c, tuple) else c


class Block:
    def __init__(self, center, half, color, bone, rot=(0, 0, 0), top=(1, 1), bot=(1, 1), top_shift=(0, 0),
                 bevel=None, studs=None, density=0.5, glow=None, name="", R=None, rnd=None, pstyle=None, role=None,
                 pvar=None, pmix=None, prelief=1.0, p2x2=None, nostud=False):
        self.c = Vector(center)
        self.h = Vector(half)
        self.color = rgb(color)
        self.bone = bone
        self.R = R.copy() if R is not None else Euler([math.radians(a) for a in rot], "XYZ").to_matrix()
        self.top, self.bot, self.ts = top, bot, top_shift
        self.bevel = bevel
        self.studs = studs          # None = all faces except -z ; [] = none ; list of face keys
        self.density = density
        self.glow = None if NO_GLOW else glow   # hex string -> Neon part
        self.name = name
        self.rnd = rnd              # edge rounding override (fraction of the smallest half-size); None = STYLE
        self.pstyle = pstyle        # (legacy, ignored by the bible plates)
        self.role = role            # "mass" | "limb" | "detail" | None (auto from size vs torso height)
        self.pvar = pvar            # plate variant: None | "diamond" (scales) | "flush" (fake inset squares)
        self.pmix = pmix            # plate size mix (1x1, 1x2, 2x1) for this block; None = STYLE["mix"]
        self.prelief = prelief      # plate relief multiplier (e.g. 1.5 for chunky rock slabs)
        self.nostud = nostud        # True = no stud skin on this block (role "detail" blocks never get studs)
        self.p2x2 = p2x2            # share of 2x2 plates on big faces; None = STYLE (tiers 4-6 only)
        self._role, self._off, self._segs, self._smooth = "detail", 0.0, 1, False

    # local corner for signs (sx, sy, sz) in {-1, 1}
    def local(self, sx, sy, sz):
        sc = self.top if sz > 0 else self.bot
        sh = self.ts if sz > 0 else (0, 0)
        return Vector((sx * self.h.x * sc[0] + sh[0], sy * self.h.y * sc[1] + sh[1], sz * self.h.z))

    def world(self, p):
        return self.c + self.R @ Vector(p)

    def contains(self, p, pad=0.0):
        q = self.R.transposed() @ (Vector(p) - self.c)
        if abs(q.z) > self.h.z + pad:
            return False
        t = (q.z / self.h.z + 1) / 2 if self.h.z > 0 else 0.5
        sx = self.bot[0] + (self.top[0] - self.bot[0]) * t
        sy = self.bot[1] + (self.top[1] - self.bot[1]) * t
        ox, oy = self.ts[0] * t, self.ts[1] * t
        return abs(q.x - ox) <= self.h.x * sx + pad and abs(q.y - oy) <= self.h.y * sy + pad

    def face_corners(self, key):
        ax, s = FACES[key]
        # 4 corners of that face in a consistent (u, v) order, world space
        if ax == 2:
            cs = [(-1, -1, s), (1, -1, s), (1, 1, s), (-1, 1, s)]
        elif ax == 0:
            cs = [(s, -1, -1), (s, 1, -1), (s, 1, 1), (s, -1, 1)]
        else:
            cs = [(-1, s, -1), (1, s, -1), (1, s, 1), (-1, s, 1)]
        return [self.world(self.local(*c)) for c in cs]


class Poly:
    """thin prism through N points (fan from pts[0], so pts must be star-shaped around it): wing membranes, fins"""
    def __init__(self, pts, thick, color, bone, glow=None):
        self.pts = [Vector(p) for p in pts]
        self.thick = thick
        self.color = rgb(color)
        self.bone = bone
        self.glow = None if NO_GLOW else glow
        self.studs = []
        self.c = sum(self.pts, Vector()) / len(self.pts)

    def contains(self, p, pad=0.0):
        return False


def _poly_bm(pl):
    bm = bmesh.new()
    P = pl.pts
    n = Vector()
    for i in range(1, len(P) - 1):
        n += (P[i] - P[0]).cross(P[i + 1] - P[0])
    n.normalize()
    top = [bm.verts.new(p + n * pl.thick / 2) for p in P]
    bot = [bm.verts.new(p - n * pl.thick / 2) for p in P]
    N = len(P)
    for i in range(1, N - 1):
        bm.faces.new((top[0], top[i], top[i + 1]))
        bm.faces.new((bot[0], bot[i + 1], bot[i]))
    for i in range(N):
        j = (i + 1) % N
        bm.faces.new((top[i], bot[i], bot[j], top[j]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return bm


class Tube(Poly):
    """2026-10-14 (Abyssal Orca review 2): lofted solid through cross-section rings - smooth hulls with no seg joints.
    closed=True: rings = [[Vector, ...], ...] closed convex loops (end caps fanned from the ring centre).
    closed=False ("band" / shell): rings = [(outer_arc, inner_arc), ...], open arcs of equal length (a thick strip:
    outer + inner surfaces, the two arc-end walls and strip end caps). Studded unless nostud."""
    def __init__(self, rings, color, bone, glow=None, closed=True, nostud=False):
        self.closed = closed
        if closed:
            self.rings = [[Vector(p) for p in r] for r in rings]
            pts = [p for r in self.rings for p in r]
        else:
            self.rings = [([Vector(p) for p in o], [Vector(p) for p in i]) for o, i in rings]
            pts = [p for o, i in self.rings for p in o + i]
        super().__init__(pts, 0.0, color, bone, glow)
        self.nostud = nostud

    def map(self, fn):
        if self.closed:
            self.rings = [[fn(p) for p in r] for r in self.rings]
        else:
            self.rings = [([fn(p) for p in o], [fn(p) for p in i]) for o, i in self.rings]
        self.pts = [fn(p) for p in self.pts]
        self.c = sum(self.pts, Vector()) / len(self.pts)


def _tube_bm(t):
    bm = bmesh.new()
    faces = []
    if t.closed:
        R = [[bm.verts.new(p) for p in r] for r in t.rings]
        n = len(R[0])
        for a, b in zip(R, R[1:]):
            for i in range(n):
                j = (i + 1) % n
                faces.append(bm.faces.new((a[i], a[j], b[j], b[i])))
        for r in (R[0], R[-1]):
            c = bm.verts.new(sum((v.co for v in r), Vector()) / n)
            for i in range(n):
                f = bm.faces.new((c, r[i], r[(i + 1) % n]))
                f.smooth = False
    else:
        O = [[bm.verts.new(p) for p in o] for o, _ in t.rings]
        I = [[bm.verts.new(p) for p in i] for _, i in t.rings]
        n = len(O[0])
        for k in range(len(O) - 1):
            for i in range(n - 1):
                faces.append(bm.faces.new((O[k][i], O[k][i + 1], O[k + 1][i + 1], O[k + 1][i])))
                faces.append(bm.faces.new((I[k][i + 1], I[k][i], I[k + 1][i], I[k + 1][i + 1])))
            for i in (0, n - 1):                                     # arc-end walls (the pattern edges)
                f = bm.faces.new((O[k][i], O[k + 1][i], I[k + 1][i], I[k][i]))
                f.smooth = False
        for k in (0, len(O) - 1):                                    # strip end caps
            for i in range(n - 1):
                f = bm.faces.new((O[k][i], I[k][i], I[k][i + 1], O[k][i + 1]))
                f.smooth = False
    for f in faces:
        f.smooth = True
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return bm


def superellipse(hw, hh, zc, y, n=2.6, seg=28, a0=0.0, a1=2 * math.pi, x0=0.0):
    """points of a superellipse cross-section at y (x = side, z up), angles a0..a1 (0 = +x, pi/2 = top)"""
    out = []
    closed = abs((a1 - a0) - 2 * math.pi) < 1e-6
    cnt = seg if closed else seg + 1
    for i in range(cnt):
        a = a0 + (a1 - a0) * i / seg
        c, s = math.cos(a), math.sin(a)
        out.append(Vector((x0 + hw * math.copysign(abs(c) ** (2.0 / n), c), y,
                           zc + hh * math.copysign(abs(s) ** (2.0 / n), s))))
    return out


def part_bm(blk):
    """bmesh of any part (box / poly / tube), world space - for ray hits on the built shapes"""
    if isinstance(blk, Tube):
        return _tube_bm(blk)
    if isinstance(blk, Poly):
        return _poly_bm(blk)
    return _box_bm(blk)


def _box_bm(blk):
    """chamfered (tapered) box in its own bmesh, world space"""
    bm = bmesh.new()
    vs = {}
    for sx in (-1, 1):
        for sy in (-1, 1):
            for sz in (-1, 1):
                vs[(sx, sy, sz)] = bm.verts.new(blk.world(blk.local(sx, sy, sz)))
    quads = [((-1, -1, -1), (-1, 1, -1), (1, 1, -1), (1, -1, -1)),   # -z
             ((-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)),       # +z
             ((-1, -1, -1), (1, -1, -1), (1, -1, 1), (-1, -1, 1)),   # -y
             ((-1, 1, -1), (-1, 1, 1), (1, 1, 1), (1, 1, -1)),       # +y
             ((-1, -1, -1), (-1, -1, 1), (-1, 1, 1), (-1, 1, -1)),   # -x
             ((1, -1, -1), (1, 1, -1), (1, 1, 1), (1, -1, 1))]       # +x
    for q in quads:
        bm.faces.new([vs[c] for c in q])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    if blk._off > 0.004:
        bmesh.ops.bevel(bm, geom=list(bm.edges), offset=blk._off, offset_type="OFFSET", segments=blk._segs,
                        profile=0.5, affect="EDGES", clamp_overlap=True)
    for f in bm.faces:
        f.smooth = blk._smooth
    return bm


def _stud(bm, L, ctr, u, v, n, a, b, hgt, color):
    """raised plate: straight sides, then a two-step chamfered top (a, b = half extents along u, v)"""
    c = min(a, b) * 0.34
    rings = []
    for (da, db, dz) in ((a, b, -0.006), (a, b, hgt * 0.45), (a - c * 0.45, b - c * 0.45, hgt * 0.85),
                         (a - c, b - c, hgt)):
        ring = []
        for (su, sv) in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
            vt = bm.verts.new(ctr + u * (su * da) + v * (sv * db) + n * dz)
            vt[L] = color
            ring.append(vt)
        rings.append(ring)
    for i in range(3):
        for j in range(4):
            bm.faces.new((rings[i][j], rings[i][(j + 1) % 4], rings[i + 1][(j + 1) % 4], rings[i + 1][j]))
    bm.faces.new(rings[3])


def _plate(bm, L, ctr, u, v, n, a, b, hgt, color, jit=1.0, flush=False):
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


def frame_from(p0, p1, n):
    """rotation whose local z runs p0 -> p1 and local x is the surface normal n"""
    z = (Vector(p1) - Vector(p0)).normalized()
    x = Vector(n)
    x = (x - z * x.dot(z)).normalized()
    y = z.cross(x)
    return Matrix((x, y, z)).transposed()


class Blocks:
    def __init__(self, k, cell=0.105, stud_h=0.03, seed=7, th=None, tier=None, plates=True):
        """th = torso height (auto: the biggest torso block), tier = 1..6 or "S" (plate fill, 2x2 plates).
        cell / stud_h are legacy (the bible derives both from th)."""
        self.k = k
        self.items = []
        self.cell = cell
        self.stud_h = stud_h
        self.th = th
        self.tier = tier if tier is not None else getattr(k, "tier", 2)
        self.rnd = random.Random(seed)
        self.stud_count = 0
        self.plates = plates        # False = no raised plates (2026-10-09 fierce style: stud_skin texture instead)

    def add(self, *a, **kw):
        b = Block(*a, **kw)
        self.items.append(b)
        return b

    def seg(self, p0, p1, hw, hd, color, bone, side=(1, 0, 0), ext=0.0, ext1=0.0, **kw):
        """block from p0 to p1 (local z along it), half width hw (along `side`), half depth hd; ext/ext1 extend the
        start/end (to bury the ends in neighbouring parts)"""
        p0, p1 = Vector(p0), Vector(p1)
        d = (p1 - p0).normalized()
        p0, p1 = p0 - d * ext, p1 + d * ext1
        return self.add((p0 + p1) / 2, (hw, hd, (p1 - p0).length / 2), color, bone, R=frame_from(p0, p1, side), **kw)

    def poly(self, pts, thick, color, bone, glow=None):
        pl = Poly(pts, thick, color, bone, glow)
        self.items.append(pl)
        return pl

    def tube(self, rings, color, bone, glow=None, closed=True, nostud=False):
        t = Tube(rings, color, bone, glow, closed, nostud)
        self.items.append(t)
        return t

    def on_face(self, blk, key, u, v, hu, hv, thick, color, bone=None, **kw):
        """plate lying on face `key` of an (untapered) block at face coords (u, v) in local units"""
        ax, sg = FACES[key]
        h = blk.h
        if ax == 1:
            loc, half = Vector((u, sg * (h.y + thick / 2 + 0.002), v)), (hu, thick / 2, hv)
        elif ax == 0:
            loc, half = Vector((sg * (h.x + thick / 2 + 0.002), u, v)), (thick / 2, hu, hv)
        else:
            loc, half = Vector((u, v, sg * (h.z + thick / 2 + 0.002))), (hu, hv, thick / 2)
        kw.setdefault("studs", [])
        kw.setdefault("bevel", min(0.012, thick * 0.6))
        return self.add(blk.world(loc), half, color, bone or blk.bone, R=blk.R, **kw)

    def spike(self, base, direction, length, w, color, bone, side=(1, 0, 0), **kw):
        """pointed block from base along direction (horns, crystals, claws, teeth)"""
        base = Vector(base)
        tip = base + Vector(direction).normalized() * length
        kw.setdefault("studs", [])
        kw.setdefault("top", (0.12, 0.12))
        return self.add((base + tip) / 2, (w, w, length / 2), color, bone, R=frame_from(base, tip, side), **kw)

    def bar(self, p0, p1, n, width, thick, color, bone, **kw):
        """flat bar from p0 to p1 lying on a surface with normal n (thin side along n)"""
        p0, p1 = Vector(p0), Vector(p1)
        return self.add((p0 + p1) / 2, (thick, width / 2, (p1 - p0).length / 2), color, bone,
                        R=frame_from(p0, p1, n), **kw)

    def mirror(self, *a, **kw):
        """add a block for x > 0 and its mirror; rot (rx, ry, rz) flips ry, rz; bone names *_L / *_R or Leg_?L"""
        center, half, color, bone = a[0], a[1], a[2], a[3]
        rot = kw.pop("rot", (0, 0, 0))
        ts = kw.pop("top_shift", (0, 0))
        out = []
        for s, side in ((1, "L"), (-1, "R")):
            bn = bone.replace("{s}", side) if bone else bone
            out.append(self.add((s * center[0], center[1], center[2]), half, color, bn,
                                rot=(rot[0], s * rot[1], s * rot[2]), top_shift=(s * ts[0], ts[1]), **kw))
        return out

    # ------------------------------------------------------------------ style-bible plates (STYLE_BIBLE.md 2b)
    def _plate_faces(self, blk):
        """faces that get plates: explicit blk.studs, else all but the bottom; limbs only outer side + front"""
        out = []
        for key in (blk.studs if blk.studs is not None else ["+x", "-x", "+y", "-y", "+z"]):
            P = blk.face_corners(key)
            n = (P[1] - P[0]).cross(P[3] - P[0])
            if n.length < 1e-9:
                continue
            n.normalize()
            ctr = sum(P, Vector()) / 4
            if (ctr - blk.c).dot(n) < 0:
                n = -n
            if blk.studs is None:
                if n.z < -0.5:
                    continue
                if blk._role == "limb":
                    sx = 1 if blk.c.x > 0.02 else -1 if blk.c.x < -0.02 else 0
                    if not ((sx and n.x * sx > 0.5) or n.y < -0.5 or (not sx and abs(n.x) > 0.5)):
                        continue
            out.append((P, n))
        return out

    def _studs_for(self, blk, bm, L):
        if blk._role == "detail":
            return
        cell = self.pcell
        fill = STYLE["fill"].get(self.tier, 0.60) * blk.density / 0.5
        others = [o for o in self.items if o is not blk and not o.glow]
        stud_h = self.pstud_h
        for P, n in self._plate_faces(blk):
            lu = ((P[1] - P[0]).length + (P[2] - P[3]).length) / 2
            lv = ((P[3] - P[0]).length + (P[2] - P[1]).length) / 2
            margin = blk._off + STYLE["plate_margin"] * cell
            ua, uc = lu - 2 * margin, lv - 2 * margin
            along_u = ua >= uc
            if not along_u:
                ua, uc = uc, ua
            N = int((ua - 0.5 * cell) / cell)
            R_ = int(uc / cell)
            if N < 1 or R_ < 1 or N + R_ < 3:       # narrow faces (legs) still get a single column of plates
                continue
            a0 = (ua - (N + 0.5) * cell) / 2               # along-start of row 0 (rows shift by half a cell)
            c0 = (uc - R_ * cell) / 2
            big = N >= 4 and R_ >= 4 and (self.tier in STYLE["big_tiers"] or blk.p2x2)
            used = set()

            def span(r, i):
                s = (r % 2) * 0.5
                return a0 + (i + s) * cell, a0 + (i + 1 + s) * cell

            def cells_over(r, lo, hi):
                s = (r % 2) * 0.5
                return [i for i in range(N) if a0 + (i + s) * cell < hi - 1e-6 and a0 + (i + 1 + s) * cell > lo + 1e-6]

            for r in range(R_):
                for i in range(N):
                    if (r, i) in used or self.rnd.random() > fill:
                        continue
                    x = self.rnd.random()
                    if big and x < (blk.p2x2 if blk.p2x2 is not None else STYLE["mix2x2"]):
                        kind = "2x2"
                    else:
                        x = self.rnd.random()
                        mix = blk.pmix or STYLE["mix"]
                        kind = "1x1" if x < mix[0] else "1x2" if x < mix[0] + mix[1] else "2x1"
                    lo, hi = span(r, i)
                    rows = [r]
                    if kind in ("2x1", "2x2"):
                        if i + 1 >= N or (r, i + 1) in used:
                            kind = "1x1"
                        else:
                            hi = span(r, i + 1)[1]
                    if kind in ("1x2", "2x2"):
                        nxt = cells_over(r + 1, lo, hi) if r + 1 < R_ else []
                        if not nxt or any((r + 1, j) in used for j in nxt):
                            kind = "1x1" if kind == "1x2" else "2x1"
                            if kind == "2x1" and (i + 1 >= N or (r, i + 1) in used):
                                kind = "1x1"
                                hi = span(r, i)[1]
                        else:
                            rows = [r, r + 1]
                    occ = [(r, j) for j in cells_over(r, lo, hi)]
                    if len(rows) == 2:
                        occ += [(r + 1, j) for j in cells_over(r + 1, lo, hi)]
                    # plate centre in face coordinates
                    am = (lo + hi) / 2 + margin
                    cm_ = c0 + (r + len(rows) / 2) * cell + margin
                    ha = (hi - lo - STYLE["plate_gap"] * cell) / 2
                    hc = (len(rows) * cell - STYLE["plate_gap"] * cell) / 2
                    s0, t0 = (am / lu, cm_ / lv) if along_u else (cm_ / lu, am / lv)
                    p = (P[0].lerp(P[1], s0)).lerp(P[3].lerp(P[2], s0), t0)
                    u = (P[1] - P[0]).lerp(P[2] - P[3], t0).normalized()
                    v = n.cross(u).normalized()
                    a, b = (ha, hc) if along_u else (hc, ha)
                    if blk.pvar == "diamond":
                        u, v = ((u + v).normalized(), (v - u).normalized())
                        a = b = min(a, b) * 0.78
                    if any(o.contains(p + n * 0.02 + u * su * a + v * sv * b, pad=0.01) for o in others
                           for su, sv in ((0, 0), (1, 1), (-1, -1), (1, -1), (-1, 1))):
                        continue
                    used.update(occ)
                    jit = 1.0 + (self.rnd.random() * 2 - 1) * STYLE["plate_jit"]
                    hgt = stud_h * (0.25 if blk.pvar == "flush" else 1.0) * blk.prelief
                    _plate(bm, L, p, u, v, n, a, b, hgt, blk.color, jit, flush=blk.pvar == "flush")
                    self.stud_count += 1

    def face_eyes(self, head, mood, iris, base=None, brow=None, lids=0.0, look=(0.0, 0.0), z=None, x=None,
                  scale=1.0, highlight=(250, 250, 255), pupil=(16, 12, 24), outline=None, key="-y", sclera=False,
                  pupil_size=None, hl_size=None, brow_spec=None, brow_angles=None, hl_on_pupil=False):
        """STYLE_BIBLE 2c eyes on the FRONT face of `head` (a Block): mood 'lovely' | 'bold' | 'fierce'.
        Sizes are fractions of HW (head width). base = head colour (dark-face rule + lids). brow = rgb or None.
        Returns {"L": centre, "R": centre, "top": outline top v, "HW": HW}."""
        spec = dict(STYLE["eyes"][mood])
        if pupil_size is not None:
            spec["pupil"] = pupil_size          # (w, h) x HW
        if hl_size is not None:
            spec["hl"] = hl_size                # (big, small) x HW
        if brow_spec is not None:
            spec["brow"] = brow_spec            # (w, h, deg)
        HW = 2 * head.h.x
        HH = 2 * head.h.z
        if outline is None:
            outline = (24, 20, 34)
            if base is not None and max(base) / 255.0 < 0.30:
                outline = (232, 226, 255)
        ow, oh = spec["outline"][0] * HW * scale, spec["outline"][1] * HW * scale
        iw, ih = spec["iris"][0] * HW * scale, spec["iris"][1] * HW * scale
        pw, ph = spec["pupil"][0] * HW * scale, spec["pupil"][1] * HW * scale
        cx = (x if x is not None else spec["x"]) * HW
        cz = -head.h.z + (z if z is not None else spec["z"]) * HH
        t0, st = 0.011 * HW, 0.0045 * HW
        res = {"HW": HW}
        ax, sg = FACES[key]
        for s, side in ((1, "L"), (-1, "R")):
            # face point: local (u, sg * face_y(v), v); account for the block taper at that height
            v = cz
            f = (v / head.h.z + 1) / 2
            sy = head.bot[1] + (head.top[1] - head.bot[1]) * f
            fy = sg * head.h.y * sy + head.ts[1] * f
            ang = -s * spec["tilt"]                         # inner corner down
            Rl = head.R @ Euler((0, math.radians(ang), 0), "XYZ").to_matrix()
            def lay(du, dv, hu, hv, thick, col, **kw):
                loc = Vector((s * cx + du, fy + sg * (thick / 2 + 0.002), cz + dv))
                kw.setdefault("studs", [])
                kw.setdefault("rnd", 0.0)
                kw.setdefault("bevel", min(hu, hv) * 0.22)
                return self.add(head.world(loc), (hu, thick / 2, hv), col, head.bone, R=Rl, **kw)
            wedge = dict(top=(spec["wedge"], 1.0)) if spec["wedge"] < 1 else {}
            lay(0, 0, ow / 2, oh / 2, t0, outline, **wedge)
            if sclera:
                lay(0, 0, iw / 2 * 1.12, ih / 2 * 1.08, t0 + st * 0.5, (246, 244, 250), **wedge)
            lay(0, 0, iw / 2, ih / 2, t0 + st, iris, **wedge)
            pdx = (-s * 0.02 + look[0] * 0.04) * HW
            pdz = (-0.02 + look[1] * 0.03) * HW
            lay(pdx, pdz, pw / 2, ph / 2, t0 + 2 * st, pupil)
            h1, h2 = spec["hl"][0] * HW * scale, spec["hl"][1] * HW * scale
            ins = 0.02 * HW
            # highlight 1 upper-LEFT as seen from the front (-x) on BOTH eyes, highlight 2 lower-right
            if hl_on_pupil:     # glint ON the pupil's upper-left corner (fierce eyes: no glyph shapes)
                h1 = min(h1, pw * 0.62, ph * 0.62)
                lay(pdx - pw / 2 + h1 / 2 + 0.1 * pw, pdz + ph / 2 - h1 / 2 - 0.1 * ph, h1 / 2, h1 / 2, t0 + 3 * st,
                    highlight, rnd=0.1)
            else:
                lay(-(iw / 2 - ins - h1 / 2), ih / 2 - ins - h1 / 2, h1 / 2, h1 / 2, t0 + 3 * st, highlight, rnd=0.1)
            if h2 > 0:      # lower-right, but never cutting a notch into the pupil (skip it if it would)
                hx, hz = (iw / 2 - ins - h2 / 2), -(ih / 2 - ins - h2 / 2)
                if not (abs(hx - pdx) < (pw + h2) / 2 + 0.004 and abs(hz - pdz) < (ph + h2) / 2 + 0.004):
                    lay(hx, hz, h2 / 2, h2 / 2, t0 + 3 * st, highlight, rnd=0.1)
            if lids > 0 and base is not None:
                lh = oh * lids
                lay(0, oh / 2 - lh / 2 + 0.004, ow / 2 * 1.04, lh / 2, t0 + 3.6 * st, base)
            if brow is not None:
                bw, bh, bang = spec["brow"] or (0.24, 0.045, 6)     # lovely: soft default brow when asked for
                if brow_angles is not None:                          # (left, right) degrees, inner corner down = +
                    bang = brow_angles[0] if s > 0 else brow_angles[1]
                Rb = head.R @ Euler((0, math.radians(-s * bang), 0), "XYZ").to_matrix()
                loc = Vector((s * cx, fy + sg * (0.03 * HW / 2 + 0.002), cz + oh / 2 + 0.03 * HW + bh * HW / 2))
                self.add(head.world(loc), (bw * HW / 2, 0.03 * HW / 2, bh * HW / 2), brow, head.bone, R=Rb, studs=[],
                         rnd=0.15, bevel=bh * HW * 0.2)
            res[side] = head.world(Vector((s * cx, fy, cz)))
        res["top"] = cz + oh / 2
        return res

    def eye(self, c, normal, hw, hh, iris, bone="Head", up=(0, 0, 1), pupil=(14, 14, 26), outline=(14, 14, 26),
            shine=(255, 255, 255), look=(0.0, 0.0), pupil_frac=0.56, slit=False, border=0.16, t=None, white=None):
        """glossy cartoon eye on a surface: dark outline plate, (optional white sclera) iris, pupil, two highlight
        squares. c = centre on the surface, normal = outward, hw / hh = iris half width / height, look = pupil shift"""
        n = Vector(normal).normalized()
        z = Vector(up)
        z = (z - n * z.dot(n)).normalized()
        y = z.cross(n)
        R = Matrix((n, y, z)).transposed()
        c = Vector(c)
        t = t or max(0.006, min(hw, hh) * 0.09)
        kw = dict(studs=[], R=R, rnd=0.0)
        out = [self.add(c, (t, hw * (1 + border), hh * (1 + border)), outline, bone, bevel=min(hw, hh) * 0.18, **kw)]
        lay = c + n * t * 1.1
        if white is not None:      # white sclera with a smaller coloured iris
            out.append(self.add(lay, (t, hw, hh), white, bone, bevel=min(hw, hh) * 0.15, **kw))
            lay = lay + n * t * 1.1 + y * look[0] * hw * 0.25 + z * look[1] * hh * 0.2
            hw2, hh2 = hw * 0.7, hh * 0.78
            out.append(self.add(lay, (t, hw2, hh2), iris, bone, bevel=min(hw2, hh2) * 0.2, **kw))
        else:
            hw2, hh2 = hw, hh
            out.append(self.add(lay, (t, hw2, hh2), iris, bone, bevel=min(hw2, hh2) * 0.15, **kw))
        lay = lay + n * t * 1.1
        pc = lay + y * look[0] * hw2 * 0.3 + z * look[1] * hh2 * 0.25
        pw = hw2 * (0.2 if slit else pupil_frac)
        ph = hh2 * (0.9 if slit else pupil_frac * 1.08)
        out.append(self.add(pc, (t, pw, ph), pupil, bone, bevel=min(pw, ph) * 0.2, **kw))
        lay = lay + n * t * 1.1
        s1 = min(hw2, hh2) * 0.26
        out.append(self.add(lay + y * hw2 * 0.38 + z * hh2 * 0.4, (t * 0.7, s1, s1), shine, bone, bevel=s1 * 0.2, **kw))
        s2 = s1 * 0.5
        out.append(self.add(lay - y * hw2 * 0.3 - z * hh2 * 0.42, (t * 0.7, s2, s2), shine, bone, bevel=s2 * 0.2, **kw))
        return out

    def _apply_head_xf(self):
        """HEAD_XF: [(pivot, scale, bones)] - grow whole head groups about their neck junction (2026-10-08 user: heads
        were far too small for the big bodies). Joints of those bones are transformed the same way (BlockPet.joint)."""
        for xf in getattr(self.k, "head_xf", []):
            pivot, sc, bones = xf[0], xf[1], xf[2]
            off = Vector(xf[3]) if len(xf) > 3 else Vector()
            for blk in self.items:
                if blk.bone not in bones:
                    continue
                if isinstance(blk, Tube):
                    blk.map(lambda p: pivot + (p - pivot) * sc + off)
                elif isinstance(blk, Poly):
                    blk.pts = [pivot + (p - pivot) * sc + off for p in blk.pts]
                    blk.thick *= sc
                    blk.c = sum(blk.pts, Vector()) / len(blk.pts)
                else:
                    blk.c = pivot + (blk.c - pivot) * sc + off
                    blk.h = blk.h * sc
                    if blk.bevel is not None:
                        blk.bevel *= sc

    TORSO_BONES = ("Spine", "Chest", "Body", "Hips", "Torso", "Pelvis")
    LIMB_PREFIX = ("Leg", "Shin", "Foot", "Arm", "Forearm", "Hand", "UpperArm", "Thigh", "Tail", "Ear", "Toe", "Finger",
                   "Wing", "WingTip", "Tent", "Tentacle", "Fin", "Claw")

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
            limbish = b.bone.split("_")[0].rstrip("0123456789") in self.LIMB_PREFIX
            role = b.role or ("detail" if mn < 0.035 * TH else "limb" if (limbish or mn < 0.10 * TH) else "mass")
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
        self._resolve()
        self.k.blocks = self            # export reads TH (AO distance) from here
        groups = {}
        for blk in self.items:
            groups.setdefault((blk.bone, blk.glow), []).append(blk)
        objs = []
        for (bone, glow), blks in groups.items():
            def build(bm, L, blks=blks):
                SM = bm.verts.layers.float.get("StudMask") or bm.verts.layers.float.new("StudMask")
                for blk in blks:
                    tmp = part_bm(blk)
                    m = {}
                    # stud skin mask (2026-10-09): small details (eyes, teeth, claws, spikes, thin inlays) stay smooth
                    if isinstance(blk, Tube):
                        smask = 0.0 if blk.nostud else 1.0
                    else:
                        smask = 0.0 if (isinstance(blk, Poly) or blk._role == "detail" or blk.nostud) else 1.0
                    for vt in tmp.verts:
                        nv = bm.verts.new(vt.co)
                        nv[L] = blk.color
                        nv[SM] = smask
                        m[vt] = nv
                    for f in tmp.faces:
                        try:
                            nf = bm.faces.new([m[vt] for vt in f.verts])
                            nf.smooth = f.smooth
                        except ValueError:
                            pass
                    tmp.free()
                    if self.plates and not glow and blk.studs != [] and not isinstance(blk, Poly):
                        self._studs_for(blk, bm, L)
                lim = math.radians(STYLE["smooth_angle"])    # soft masses, crisp details
                for e in bm.edges:
                    fs = e.link_faces
                    e.smooth = len(fs) == 2 and fs[0].smooth and fs[1].smooth and e.calc_face_angle(0.0) < lim
            name = ("G_" + glow if glow else "P") + "_" + bone
            if glow:
                o = pk.glow_part(self.k, name, glow, build, bone)
            else:
                o = self.k.part(name, build, bone, smooth_shade=False)
            if glow:
                for p in o.data.polygons:
                    p.use_smooth = False
            objs.append(o)
        return objs


STUD_TILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_tools", "stud_tile.png")


def stud_nodes(nt, color_socket, stud):
    """color_socket x (box-projected stud tile x gain) -> returns the output socket. stud = dict(path, pitch, gain,
    blend). Object-space box projection: one stud every `pitch` Blender units on every surface (Roblox studs)."""
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = (1 / stud["pitch"],) * 3
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
    im = nt.nodes.new("ShaderNodeTexImage")
    im.image = bpy.data.images.load(stud["path"], check_existing=True)
    im.image.colorspace_settings.name = "Non-Color"
    im.projection = "BOX"
    im.projection_blend = stud.get("blend", 0.2)
    im.interpolation = "Cubic"
    nt.links.new(mp.outputs["Vector"], im.inputs["Vector"])
    sep = nt.nodes.new("ShaderNodeSeparateColor")
    nt.links.new(im.outputs["Color"], sep.inputs["Color"])
    mul = nt.nodes.new("ShaderNodeMath")                  # R = multiplier / gain (shadow, cap, dark rim)
    mul.operation = "MULTIPLY"
    mul.inputs[1].default_value = stud.get("gain", 2.0)
    nt.links.new(sep.outputs[0], mul.inputs[0])
    sc = nt.nodes.new("ShaderNodeVectorMath")
    sc.operation = "SCALE"
    nt.links.new(color_socket, sc.inputs[0])
    nt.links.new(mul.outputs[0], sc.inputs["Scale"])
    addk = nt.nodes.new("ShaderNodeMath")                 # G = additive light rim (visible on dark colours)
    addk.operation = "MULTIPLY"
    addk.inputs[1].default_value = stud.get("add", 0.10)
    nt.links.new(sep.outputs[1], addk.inputs[0])
    cmb = nt.nodes.new("ShaderNodeCombineXYZ")
    for i in range(3):
        nt.links.new(addk.outputs[0], cmb.inputs[i])
    mx = nt.nodes.new("ShaderNodeVectorMath")
    mx.operation = "ADD"
    nt.links.new(sc.outputs["Vector"], mx.inputs[0])
    nt.links.new(cmb.outputs["Vector"], mx.inputs[1])
    att = nt.nodes.new("ShaderNodeAttribute")             # StudMask: 1 = studded, 0 = smooth detail
    att.attribute_name = "StudMask"
    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type = "RGBA"
    nt.links.new(att.outputs["Fac"], mix.inputs["Factor"])
    nt.links.new(color_socket, mix.inputs[6])
    nt.links.new(mx.outputs["Vector"], mix.inputs[7])
    return mix.outputs[2]


def stud_skin(k, pitch, gain=2.0, blend=0.2, roughness=0.42, add=0.10):
    """2026-10-09 fierce style: cover the whole pet in small Roblox studs (preview material now, baked into the
    texture by petkit.bake_and_export(stud=k.stud) at export)."""
    k.stud = {"path": STUD_TILE, "pitch": pitch, "gain": gain, "blend": blend, "add": add}
    nt = k.mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    vc = nt.nodes.new("ShaderNodeVertexColor")
    vc.layer_name = "Col"
    nt.links.new(stud_nodes(nt, vc.outputs["Color"], k.stud), bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = roughness
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    return k.stud


def head_point(k, bone, p):
    """transform a rest-space point carried by `bone` with the pet's head scaling (identity if none)"""
    p = Vector(p)
    for xf in getattr(k, "head_xf", []):
        pivot, sc, bones = xf[0], xf[1], xf[2]
        if bone in bones:
            off = Vector(xf[3]) if len(xf) > 3 else Vector()
            return pivot + (p - pivot) * sc + off, sc
    return p, 1.0


class BlockPet(pk.Pet):
    """Pet whose mesh is all rigid blocks: no bone-heat body, every part weighted to its own bone.
    Optional 2-bone legs: add_leg2("Leg_L", "Shin_L", "Foot_L", knee=(0, -1, 0)); then solve_leg("Leg_L", f, T)
    plants the foot (ankle above ground point T, foot kept flat) with the knee bending toward `knee`."""

    def joint(self, name, pos, parent, tail=None):
        pos, sc = head_point(self, name, pos)
        if tail is not None and sc != 1.0:
            tail = Vector(tail) * sc
        return super().joint(name, pos, parent, tail)

    def _clip_loops(self, loop=None):
        name = self.arm.animation_data.action.name
        return self.clips[name][1] if loop is None else loop

    def bake_bezier_now(self):
        """petkit's version put a CYCLES modifier on every curve - also in one-shot clips, where a channel keyed over
        only part of the clip then repeated (builder B: trident dropped at frame 70). Cycles only for looping clips."""
        loop = self._clip_loops()
        for fc in self.fcurves():
            for kp in fc.keyframe_points:
                kp.interpolation = "BEZIER"
                kp.handle_left_type = kp.handle_right_type = "AUTO_CLAMPED"
            cyc = [m for m in fc.modifiers if m.type == "CYCLES"]
            if loop and not cyc:
                fc.modifiers.new("CYCLES")
            elif not loop:
                for m in cyc:
                    fc.modifiers.remove(m)
            fc.update()

    def finish(self, loop=None):
        self._quat_continuity()
        if not self._clip_loops(loop):           # one-shots hold their first / last key, never repeat
            for fc in self.fcurves():
                for m in [m for m in fc.modifiers if m.type == "CYCLES"]:
                    fc.modifiers.remove(m)
        return super().finish(loop)

    def _quat_continuity(self):
        """flip quaternion keys whose sign jumps against the previous key (q and -q are the same pose, but
        interpolating between them swings the bone through a full turn - e.g. an IK key after a keyed pose)"""
        by = {}
        for fc in self.fcurves():
            if fc.data_path.endswith("rotation_quaternion"):
                by.setdefault(fc.data_path, {})[fc.array_index] = fc
        for chans in by.values():
            if len(chans) != 4:
                continue
            idx = [{round(kp.co.x, 3): kp for kp in chans[i].keyframe_points} for i in range(4)]
            prev = None
            for f in sorted(idx[0]):
                if not all(f in idx[i] for i in range(4)):
                    continue
                q = [idx[i][f].co.y for i in range(4)]
                if prev is not None and sum(a * b for a, b in zip(prev, q)) < 0:
                    for i in range(4):
                        kp = idx[i][f]
                        kp.co.y = -kp.co.y
                        kp.handle_left.y = -kp.handle_left.y
                        kp.handle_right.y = -kp.handle_right.y
                    q = [-v for v in q]
                prev = q
            for fc in chans.values():
                fc.update()

    def add_leg2(self, leg, shin, foot, knee=(0, -1, 0)):
        if not hasattr(self, "legs2"):
            self.legs2 = {}
        self.legs2[leg] = {"shin": shin, "foot": foot, "knee": Vector(knee)}

    def _aim(self, bone, f, q_world):
        """key `bone` so its armature-space orientation = q_world @ rest (q_world = rotation delta in armature space)"""
        arm = self.arm
        pb = arm.pose.bones[bone]
        pb.rotation_quaternion = (1, 0, 0, 0)
        bpy.context.view_layer.update()
        par = pb.parent
        Rp = par.matrix.to_quaternion() @ arm.data.bones[par.name].matrix_local.to_quaternion().inverted()
        R0 = arm.data.bones[bone].matrix_local.to_quaternion()
        pb.rotation_quaternion = R0.inverted() @ (Rp.inverted() @ q_world) @ R0
        pb.keyframe_insert("rotation_quaternion", frame=f, group=bone)
        bpy.context.view_layer.update()

    def solve_leg(self, leg, f, T, foot_z=0.0, toe=None):
        L = getattr(self, "legs2", {}).get(leg)
        if L is None:
            return super().solve_leg(leg, f, T, foot_z)
        from mathutils import Quaternion
        arm, J = self.arm, self.J
        hipR, kneeR, ankR = J[leg], J[L["shin"]], J[L["foot"]]
        L1, L2 = (kneeR - hipR).length, (ankR - kneeR).length
        T = Vector(T)
        A = Vector((T.x + ankR.x - hipR.x, T.y + ankR.y - hipR.y, T.z - foot_z + ankR.z))
        pb = arm.pose.bones[leg]
        pb.rotation_quaternion = (1, 0, 0, 0)
        pb.location = (0, 0, 0)
        bpy.context.view_layer.update()
        H = pb.head.copy()
        par = pb.parent
        Rp = par.matrix.to_quaternion() @ arm.data.bones[par.name].matrix_local.to_quaternion().inverted()
        d = A - H
        dist = min(max(d.length, abs(L1 - L2) * 1.02 + 1e-4), (L1 + L2) * 0.999)
        dn = d.normalized()
        kd = Rp @ L["knee"]
        pole = kd - dn * kd.dot(dn)
        pole = pole.normalized() if pole.length > 1e-6 else Vector((0, -1, 0))
        ca = max(-1.0, min(1.0, (L1 * L1 + dist * dist - L2 * L2) / (2 * L1 * dist)))
        a = math.acos(ca)
        K = H + dn * math.cos(a) * L1 + pole * math.sin(a) * L1
        A2 = H + dn * dist
        self._aim(leg, f, (kneeR - hipR).rotation_difference(K - H))
        pb.keyframe_insert("location", frame=f, group=leg)
        self._aim(L["shin"], f, (ankR - kneeR).rotation_difference(A2 - K))
        lift = max(0.0, T.z - foot_z)
        tdeg = (35.0 * min(1.0, lift / 0.12)) if toe is None else toe
        self._aim(L["foot"], f, Quaternion((1, 0, 0), math.radians(tdeg)))

    def foot_world(self, leg, foot_z=0.0):
        L = getattr(self, "legs2", {}).get(leg)
        if L is None:
            return super().foot_world(leg, foot_z)
        return self.arm.matrix_world @ self.arm.pose.bones[L["foot"]].head

    def build_rig(self):
        mn, mx = self.bounds()
        self.J["Root"] = Vector(((mn.x + mx.x) / 2, (mn.y + mx.y) / 2, 0.0))
        ad = bpy.data.armatures.new("Armature")
        arm = bpy.data.objects.new("Armature", ad)
        self.coll.objects.link(arm)
        bpy.context.view_layer.update()
        for o in bpy.context.scene.objects:
            if o is not None:
                o.select_set(False)
        arm.select_set(True)
        bpy.context.view_layer.objects.active = arm
        bpy.ops.object.mode_set(mode="EDIT")
        kids = {}
        for b, p in self.P.items():
            kids.setdefault(p, []).append(b)
        order = ["Root"]
        i = 0
        while i < len(order):
            order += kids.get(order[i], [])
            i += 1
        for b in order:
            e = ad.edit_bones.new(b)
            e.head = self.J[b]
            if b in self.tail:
                tl = self.tail[b]
            elif b in kids and len(kids[b]) == 1 and (self.J[kids[b][0]] - self.J[b]).length > 0.05:
                tl = self.J[kids[b][0]] - self.J[b]
            else:
                tl = Vector((0, 0, 0.15))
            if tl.length < 0.03:
                tl = tl.normalized() * 0.1 if tl.length > 0 else Vector((0, 0, 0.1))
            e.tail = self.J[b] + tl
            e.roll = 0
            if b in self.P:
                e.parent = ad.edit_bones[self.P[b]]
        bpy.ops.object.mode_set(mode="OBJECT")
        self.arm = arm
        for pb in arm.pose.bones:
            pb.rotation_mode = "QUATERNION"
        for o, w in self.parts + self.glow:
            self._weight(o, w)
        main = self._join([o for o, _ in self.parts], "Body")
        glows = {}
        for o, _ in self.glow:
            glows.setdefault(o.get("glow_hex", "ffc840"), []).append(o)
        self.glowobjs = {}
        for hexs, objs in glows.items():
            self.glowobjs[hexs] = self._join(objs, "Glow_" + hexs)
        for o in [main] + list(self.glowobjs.values()):
            o.parent = arm
            mod = o.modifiers.get("Armature") or o.modifiers.new("Armature", "ARMATURE")
            mod.object = arm
        self.main = main
        self.bodyobj = main
        return arm


def _seg_dist(p, a, b):
    ab = b - a
    t = 0.0 if ab.length_squared < 1e-12 else max(0.0, min(1.0, (p - a).dot(ab) / ab.length_squared))
    return (p - (a + ab * t)).length


def _tri_hits(A, B):
    """points where the edges of triangle A cross triangle B and vice versa"""
    from mathutils import geometry
    pts = []
    for T, U in ((A, B), (B, A)):
        for i in range(3):
            p, q = T[i], T[(i + 1) % 3]
            d = q - p
            L = d.length
            if L < 1e-9:
                continue
            for o, r in ((p, d), (q, -d)):
                x = geometry.intersect_ray_tri(U[0], U[1], U[2], r, o, True)
                if x is not None and (x - o).length <= L + 1e-6:
                    pts.append(x)
                    break
    return pts


def overlap_report(k, pairs, step=2, clips=None, joints=None, frames=None, detail=False):
    """For each clip, frames where the parts of two bones really CUT THROUGH each other.
    pairs: [(boneA, boneB)]. joints: [(p0, p1, r, bone)] rest-space hinge/knuckle segments carried by `bone`:
    an intersection whose crossing points all lie within r of a (posed) joint segment is a hinge sliver, ignored.
    Contacts already present in the rest pose are ignored too. frames: {clip: [f, ...]}.
    Returns {clip: {"A|B": (colliding_triangle_pairs, worst_frame)}}."""
    from mathutils.bvhtree import BVHTree
    sc = bpy.context.scene
    arm = k.arm
    body = k.main
    me = body.data
    names = {g.index: g.name for g in body.vertex_groups}
    owner = [names[max(v.groups, key=lambda g: g.weight).group] if len(v.groups) else None for v in me.vertices]
    want = sorted(set(a for pr in pairs for a in pr))
    J = []
    for a, b, r, bn in (joints or []):
        a2, hs = head_point(k, bn, a)
        b2, _ = head_point(k, bn, b)
        J.append((a2, b2, r * hs, bn))

    def posed_joints():
        out = []
        for a, b, r, bn in J:
            pbn = arm.pose.bones[bn]
            M = arm.matrix_world @ pbn.matrix @ arm.data.bones[bn].matrix_local.inverted()
            out.append((M @ a, M @ b, r))
        return out

    def trees():
        dg = bpy.context.evaluated_depsgraph_get()
        ev = body.evaluated_get(dg)
        em = ev.to_mesh()
        em.calc_loop_triangles()
        co = [ev.matrix_world @ v.co for v in em.vertices]
        tris = {}
        for t in em.loop_triangles:
            g = owner[t.vertices[0]]
            if g in want:
                tris.setdefault(g, []).append(tuple(t.vertices))
        T = {}
        for g in want:
            tl = tris.get(g, [])
            T[g] = (BVHTree.FromPolygons(co, [list(t) for t in tl], all_triangles=True), tl)
        ev.to_mesh_clear()
        return T, co

    def hits(T, co, a, b, pj):
        ta, la = T[a]
        tb, lb = T[b]
        out = set()
        for x, y in ta.overlap(tb):
            A = [co[i] for i in la[x]]
            B = [co[i] for i in lb[y]]
            pts = _tri_hits(A, B)
            if not pts:
                continue
            if pj and all(any(_seg_dist(p, j0, j1) < r for j0, j1, r in pj) for p in pts):
                continue
            out.add((la[x], lb[y]))
        return out

    arm.data.pose_position = "REST"
    bpy.context.view_layer.update()
    T, co = trees()
    pj = posed_joints()
    base = {pr: hits(T, co, pr[0], pr[1], pj) for pr in pairs}
    arm.data.pose_position = "POSE"
    rep = {}
    for clip, (n, loop) in k.clips.items():
        if clips and clip not in clips:
            continue
        k.set_action(clip)
        worst = {}
        for f in (frames or {}).get(clip, range(0, n + 1, step)):
            sc.frame_set(f)
            T, co = trees()
            pj = posed_joints()
            for pr in pairs:
                c = len(hits(T, co, pr[0], pr[1], pj) - base[pr])
                if c > worst.get(pr, (0, -1))[0]:
                    worst[pr] = (c, f)
        rep[clip] = {a + "|" + b: v for (a, b), v in worst.items()}
    return rep
