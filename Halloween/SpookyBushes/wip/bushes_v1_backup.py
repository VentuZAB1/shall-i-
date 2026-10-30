# SLINGSHOT Halloween garden - SPOOKY BUSHES (2026-10-12)
#   Bush_Thorn  : a dark bramble mound (purple-green leaves), twisted thorny arching canes, glossy blackberries and a
#                 fake cobweb draped over the top (strand tubes "Web" + RGBA silk "WebSilk"), 1 spider thread point
#   Bush_Autumn : a dense clumpy autumn bush (crimson / orange / gold) with a warty mini pumpkin and a warty goblin
#                 gourd at its base (part "Gourds")
#   Bramble     : a small dead shrub: crooked tangled twigs, a few curled dead leaves hanging
# Headless (one step per run is safest):
#   blender.exe -b --factory-startup --python bushes.py -- [fast] thorn | autumn | bramble | preview <asset> | render | export
# Pipeline: hi = voxel-union clump body (sub-clumps + lumps) covered by thousands of real leaves (veins = shader bump,
# baked into the normal map) + full canes / stems / twigs / berries; game mesh = the decimated clump body pushed out into
# the leaf layer + REAL two-sided protruding leaves on the silhouette + the exposed canes, thorns, berries; per-group
# Cycles bakes (tangent normal, colour x AO, roughness) into one atlas. FBX origin = base centre on the ground (Z = 0).
import sys, os, json, time
sys.path.insert(0, r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween")
from hkit import *  # noqa: F401,F403  (read-only shared kit)
from mathutils import Matrix, Quaternion
from mathutils.bvhtree import BVHTree

OUT = os.path.join(HERE, "SpookyBushes")
MAPS = os.path.join(OUT, "maps")
WIP = os.path.join(OUT, "wip")
for _d in (MAPS, WIP):
    os.makedirs(_d, exist_ok=True)
T0 = time.time()
CFG = {"fast": False}
TAU = 2 * math.pi
UP = Vector((0.0, 0.0, 1.0))
DOWN = Vector((0.0, 0.0, -1.0))


def log(*a):
    print("[bush %6.1fs]" % (time.time() - T0), *a, flush=True)


def sk(socks, ident):
    return next(s for s in socks if s.identifier == ident)


def rb(v):
    """Blender (x, y, z) -> Roblox (X, Y, Z): Blender +Z = Roblox +Y, Blender +Y = Roblox -Z."""
    return [round(float(v[0]), 3), round(float(v[2]), 3), round(-float(v[1]), 3)]


def tris_of(ob):
    return sum(len(p.vertices) - 2 for p in ob.data.polygons)


def tris_by_mat(ob):
    out = {}
    names = [m.name for m in ob.data.materials]
    for p in ob.data.polygons:
        k = names[p.material_index] if p.material_index < len(names) else str(p.material_index)
        out[k] = out.get(k, 0) + len(p.vertices) - 2
    return out


def bbox_of(objs):
    vs = []
    for o in objs:
        a = np.empty(len(o.data.vertices) * 3, np.float32)
        o.data.vertices.foreach_get("co", a)
        a = a.reshape(-1, 3)
        M = np.array(o.matrix_world)
        vs.append(a @ M[:3, :3].T + M[:3, 3])
    vs = np.concatenate(vs)
    return vs.min(0), vs.max(0)


def ramp(stops, t):
    t = max(stops[0][0], min(stops[-1][0], t))
    for (p0, c0), (p1, c1) in zip(stops[:-1], stops[1:]):
        if t <= p1:
            return mix(c0, c1, (t - p0) / max(1e-6, p1 - p0))
    return stops[-1][1]


def kcol(c, k):
    return tuple(max(0.0, min(1.0, x * k)) for x in c)


def clamp01(x):
    return max(0.0, min(1.0, x))


def cyl(r, az, z):
    a = math.radians(az)
    return Vector((r * math.cos(a), r * math.sin(a), z))


# ================================================================== mesh builder
class MB:
    """Vertices (+ per-vertex Col / Rough) and faces (+ material index, optional per-corner UVs)."""

    def __init__(self):
        self.V, self.C, self.R = [], [], []
        self.F, self.FM, self.FUV = [], [], []
        self.copies = []         # (face, source face, reversed): faces that reuse another face's texels (leaf
        self.skipf = set()       # bottoms, repeated thorns); they stay out of the packing
        self.cx = self.cy = self.rowh = 0.0

    def v(self, co, col=(0.5, 0.5, 0.5), r=0.6):
        self.V.append(Vector(co))
        self.C.append(tuple(col[:3]))
        self.R.append(float(r))
        return len(self.V) - 1

    def f(self, idx, mat=0, uv=None):
        self.F.append(tuple(idx))
        self.FM.append(mat)
        self.FUV.append(uv)
        return len(self.F) - 1

    def alloc(self, w, h):
        """A free pre-pack UV spot (studs) beyond 0..1 (a smart-UV island set may live there): no overlaps."""
        if self.cx + w > 80.0:
            self.cx = 0.0
            self.cy += self.rowh + 0.5
            self.rowh = 0.0
        o = (self.cx + 2.0, self.cy + 2.0)
        self.cx += w + 0.5
        self.rowh = max(self.rowh, h)
        return o

    def add_object_mesh(self, ob, mat, uv=True):
        me = ob.data
        base = len(self.V)
        M = ob.matrix_world
        for v in me.vertices:
            self.v(M @ v.co)
        uvl = me.uv_layers.active.data if uv else None
        for p in me.polygons:
            self.f([base + i for i in p.vertices], mat,
                   [tuple(uvl[li].uv) for li in p.loop_indices] if uv else None)

    def obj(self, name, mats=(), uv="UVMap", smooth=True):
        me = bpy.data.meshes.new(name)
        me.from_pydata([tuple(v) for v in self.V], [], self.F)
        set_colors(me, "Col", self.C)
        set_colors(me, "Rough", [(r, r, r) for r in self.R])
        if uv and any(x is not None for x in self.FUV):
            lay = me.uv_layers.new(name=uv)
            data = []
            for i, p in enumerate(me.polygons):
                u = self.FUV[i] or [(0.0, 0.0)] * p.loop_total
                for q in u:
                    data.extend((q[0], q[1]))
            lay.data.foreach_set("uv", data)
        me.polygons.foreach_set("material_index", self.FM)
        for m in mats:
            me.materials.append(m)
        if smooth:
            me.shade_smooth()
        return link(bpy.data.objects.new(name, me))


# ================================================================== leaves
def leaf_w(v, kind="ovate"):
    if kind == "lance":
        return math.sin(math.pi * v ** 0.72) ** 1.1
    if kind == "broad":
        return math.sin(math.pi * v ** 0.95) ** 0.7
    return math.sin(math.pi * v ** 0.85) ** 0.8


def leaf_frame(n, t, tilt, roll=0.0):
    """Leaf axis d (base -> tip), blade normal up, side = d x up."""
    d = (t * math.cos(tilt) + n * math.sin(tilt)).normalized()
    up = n - d * n.dot(d)
    if up.length < 1e-6:
        up = UP - d * d.z
    up.normalize()
    if roll:
        up = Quaternion(d, roll) @ up
    return d, up, d.cross(up)


def leaf_point(B, fr, P, u, v):
    """u -1..1 across the blade, v 0..1 base -> tip."""
    d, up, side = fr
    L, W = P["L"], P["W"]
    w = W * leaf_w(v, P.get("kind", "ovate"))
    x = u * w
    h = P["cup"] * abs(u) ** 1.5 * w - P["bend"] * v * v * L
    c = P.get("curl", 0.0)
    if c:
        k = c / W
        h += (1 - math.cos(k * x)) / k
        x = math.sin(k * x) / k
    tw = P.get("twist", 0.0) * v
    s2 = side * math.cos(tw) + up * math.sin(tw)
    u2 = up * math.cos(tw) - side * math.sin(tw)
    p = B + d * (v * L) + s2 * x + u2 * h
    cr = P.get("crinkle", 0.0)
    if cr:
        p += u2 * (cr * W * noise.noise(Vector((u * 2.3, v * 3.7, P.get("seed", 0.0)))) * min(1.0, 4 * v))
    return p


def leaf_hi(mb, B, fr, P, cfn, rough, mat=0, nu=5, nv=7):
    """Bake-source leaf: a fine single-sided blade facing `up`, LeafUV = (u, v) for the vein shader."""
    us = [-1.0 + 2.0 * k / (nu - 1) for k in range(nu)]
    vs = [((i + 1) / (nv + 1)) ** 0.9 for i in range(nv)]
    b = mb.v(leaf_point(B, fr, P, 0.0, 0.0), cfn(0.0, 0.0), rough)
    t = mb.v(leaf_point(B, fr, P, 0.0, 1.0), cfn(0.0, 1.0), rough)
    rows = [[mb.v(leaf_point(B, fr, P, u, v), cfn(u, v), rough) for u in us] for v in vs]
    for k in range(nu - 1):
        mb.f((b, rows[0][k + 1], rows[0][k]), mat, [(0.0, 0.0), (us[k + 1], vs[0]), (us[k], vs[0])])
    for i in range(nv - 1):
        for k in range(nu - 1):
            mb.f((rows[i][k], rows[i][k + 1], rows[i + 1][k + 1], rows[i + 1][k]), mat,
                 [(us[k], vs[i]), (us[k + 1], vs[i]), (us[k + 1], vs[i + 1]), (us[k], vs[i + 1])])
    for k in range(nu - 1):
        mb.f((t, rows[-1][k], rows[-1][k + 1]), mat, [(0.0, 1.0), (us[k], vs[-1]), (us[k + 1], vs[-1])])


def leaf_lo(mb, B, fr, P, mat_top, mat_bot, vs=(0.15, 0.38, 0.62, 0.85), thick=0.028):
    """Game leaf: two real sheets (top + bottom, separate vertices so the normals stay crisp). The midrib of the bottom
    sheet sits `thick` lower; the outline is shared in position. The bottom sheet reuses the top's UVs (copied after
    packing) -> pairs."""
    up = fr[1]
    L, W, kind = P["L"], P["W"], P.get("kind", "ovate")
    us = (-1.0, 0.0, 1.0)
    ox, oy = mb.alloc(2 * W + 0.05, L + 0.05)

    def UV(u, v):
        return (ox + W + u * W * leaf_w(v, kind), oy + v * L)

    pts = {(u, v): leaf_point(B, fr, P, u, v) for v in vs for u in us}
    pb, pt = leaf_point(B, fr, P, 0.0, 0.0), leaf_point(B, fr, P, 0.0, 1.0)
    faces = {}
    for sign, mat in ((1, mat_top), (-1, mat_bot)):
        off = -up * thick
        b, t = mb.v(pb), mb.v(pt)
        rows = [[mb.v(pts[(u, v)] + (off if (sign < 0 and u == 0.0) else Vector())) for u in us] for v in vs]
        quads = [((b, rows[0][1], rows[0][0]), (UV(0, 0), UV(0, vs[0]), UV(-1, vs[0]))),
                 ((b, rows[0][2], rows[0][1]), (UV(0, 0), UV(1, vs[0]), UV(0, vs[0])))]
        for i in range(len(vs) - 1):
            for k in range(2):
                quads.append(((rows[i][k], rows[i][k + 1], rows[i + 1][k + 1], rows[i + 1][k]),
                              (UV(us[k], vs[i]), UV(us[k + 1], vs[i]), UV(us[k + 1], vs[i + 1]), UV(us[k], vs[i + 1]))))
        quads.append(((t, rows[-1][0], rows[-1][1]), (UV(0, 1), UV(-1, vs[-1]), UV(0, vs[-1]))))
        quads.append(((t, rows[-1][1], rows[-1][2]), (UV(0, 1), UV(0, vs[-1]), UV(1, vs[-1]))))
        out = []
        for vi, uvs in quads:
            if sign > 0:
                out.append(mb.f(vi, mat, list(uvs)))
            else:
                out.append(mb.f(tuple(reversed(vi)), mat, list(reversed(uvs))))
        faces[sign] = out
    for bf, tf in zip(faces[-1], faces[1]):
        mb.copies.append((bf, tf, True))
        mb.skipf.add(bf)


def tangent_dir(n, rng, down_bias=0.7):
    ref = UP if abs(n.z) < 0.95 else Vector((1.0, 0.0, 0.0))
    t1 = n.cross(ref).normalized()
    t2 = n.cross(t1)
    a = rng.uniform(0, TAU)
    tr = t1 * math.cos(a) + t2 * math.sin(a)
    td = DOWN - n * DOWN.dot(n)
    if td.length > 0.15:
        tr = (tr + td.normalized() * down_bias).normalized()
    return tr


# ================================================================== tubes (canes, stems, twigs, strands)
def frames(pts):
    n = len(pts)
    T = []
    for i in range(n):
        t = pts[min(n - 1, i + 1)] - pts[max(0, i - 1)]
        T.append(t.normalized() if t.length > 1e-9 else UP.copy())
    ref = UP if abs(T[0].z) < 0.9 else Vector((1.0, 0.0, 0.0))
    N = T[0].cross(ref).normalized()
    Ns, Bs = [], []
    for i in range(n):
        N = N - T[i] * N.dot(T[i])
        if N.length < 1e-6:
            N = T[i].orthogonal()
        N.normalize()
        Ns.append(N.copy())
        Bs.append(T[i].cross(N))
    return T, Ns, Bs


def arclen(pts):
    s = [0.0]
    for i in range(1, len(pts)):
        s.append(s[-1] + (pts[i] - pts[i - 1]).length)
    return s


def resample(pts, step, keep_end=True):
    """Resample a 3D polyline at ~step spacing (first and last points kept)."""
    s = arclen(pts)
    n = max(1, int(round(s[-1] / step)))
    out, j = [], 0
    for k in range(n + 1):
        t = s[-1] * k / n
        while j < len(s) - 2 and s[j + 1] < t:
            j += 1
        f = (t - s[j]) / max(1e-9, s[j + 1] - s[j])
        out.append(pts[j].lerp(pts[j + 1], min(1.0, max(0.0, f))))
    return out


def interp_radii(pts_src, radii_src, pts_dst):
    s = arclen(pts_src)
    d = arclen(pts_dst)
    out, j = [], 0
    for k in range(len(pts_dst)):
        t = d[k] / max(1e-9, d[-1]) * s[-1]
        while j < len(s) - 2 and s[j + 1] < t:
            j += 1
        f = (t - s[j]) / max(1e-9, s[j + 1] - s[j])
        out.append(radii_src[j] + (radii_src[j + 1] - radii_src[j]) * min(1.0, max(0.0, f)))
    return out


def tube(mb, pts, radii, sides, mat=0, cfn=None, rfn=None, rough=0.6, cap_tip=True, cap_base=False, tipk=1.0,
         uv=True, t0=0.0, t1=1.0):
    """Closed-ish tube. cfn(t, a) -> colour, rfn(t, a) -> radius factor (t along the WHOLE branch: t0..t1 here).
    Explicit cylindrical UV island (u around, v along)."""
    n = len(pts)
    T, Ns, Bs = frames(pts)
    s = arclen(pts)
    rmean = sum(radii) / n
    C = TAU * rmean
    ox, oy = mb.alloc(C + 0.02, s[-1] + 2.5 * rmean + 0.02) if uv else (0.0, 0.0)
    oy += rmean
    rings = []
    for i in range(n):
        t = t0 + (t1 - t0) * s[i] / max(1e-9, s[-1])
        ring = []
        for j in range(sides):
            a = TAU * j / sides
            k = rfn(t, a) if rfn else 1.0
            p = pts[i] + (Ns[i] * math.cos(a) + Bs[i] * math.sin(a)) * radii[i] * k
            ring.append(mb.v(p, cfn(t, a) if cfn else (0.5, 0.5, 0.5), rough))
        rings.append(ring)

    def UV(j, i):
        return (ox + C * j / sides, oy + s[i])

    for i in range(n - 1):
        for j in range(sides):
            jn = (j + 1) % sides
            mb.f((rings[i][j], rings[i][jn], rings[i + 1][jn], rings[i + 1][j]), mat,
                 [UV(j, i), UV(j + 1, i), UV(j + 1, i + 1), UV(j, i + 1)] if uv else None)
    if cap_tip:
        tv = mb.v(pts[-1] + T[-1] * radii[-1] * tipk, cfn(t1, 0.0) if cfn else (0.5, 0.5, 0.5), rough)
        for j in range(sides):
            jn = (j + 1) % sides
            mb.f((rings[-1][j], rings[-1][jn], tv), mat,
                 [UV(j, n - 1), UV(j + 1, n - 1), (ox + C * (j + 0.5) / sides, oy + s[-1] + radii[-1] * tipk)]
                 if uv else None)
    if cap_base:
        bv = mb.v(pts[0] - T[0] * radii[0] * 0.4, cfn(t0, 0.0) if cfn else (0.5, 0.5, 0.5), rough)
        for j in range(sides):
            jn = (j + 1) % sides
            mb.f((rings[0][jn], rings[0][j], bv), mat,
                 [UV(j + 1, 0), UV(j, 0), (ox + C * (j + 0.5) / sides, oy - radii[0] * 0.4)] if uv else None)
    return rings


def sphere_mesh(mb, c, r, nu, nv, mat=0, col=(0.5, 0.5, 0.5), rough=0.5, uv=True, sq=1.0, cfn=None):
    C = TAU * r
    ox, oy = mb.alloc(C + 0.02, math.pi * r + 0.02) if uv else (0.0, 0.0)

    def cc(d):
        return cfn(d) if cfn else col

    top = mb.v(c + Vector((0, 0, r * sq)), cc(UP), rough)
    rings = []
    for i in range(1, nv):
        th = math.pi * i / nv
        ring = []
        for j in range(nu):
            ph = TAU * j / nu
            d = Vector((math.sin(th) * math.cos(ph), math.sin(th) * math.sin(ph), math.cos(th)))
            ring.append(mb.v(c + Vector((d.x * r, d.y * r, d.z * r * sq)), cc(d), rough))
        rings.append(ring)
    bot = mb.v(c - Vector((0, 0, r * sq)), cc(DOWN), rough)

    def UV(j, i):
        return (ox + C * j / nu, oy + math.pi * r * (1 - i / nv))

    for j in range(nu):
        jn = (j + 1) % nu
        mb.f((top, rings[0][j], rings[0][jn]), mat,
             [(ox + C * (j + 0.5) / nu, oy + math.pi * r), UV(j, 1), UV(j + 1, 1)] if uv else None)
        for i in range(nv - 2):
            mb.f((rings[i][j], rings[i + 1][j], rings[i + 1][jn], rings[i][jn]), mat,
                 [UV(j, i + 1), UV(j, i + 2), UV(j + 1, i + 2), UV(j + 1, i + 1)] if uv else None)
        mb.f((bot, rings[-1][jn], rings[-1][j]), mat,
             [(ox + C * (j + 0.5) / nu, oy), UV(j + 1, nv - 1), UV(j, nv - 1)] if uv else None)


def catenary(a, b, n, sag, k=2.2, side=None):
    c0 = math.cosh(k / 2)
    out = []
    for i in range(n + 1):
        t = i / n
        s = (math.cosh(k * (t - 0.5)) - c0) / (1 - c0)
        p = a.lerp(b, t) + Vector((0, 0, -sag * s))
        if side is not None:
            p += side * s
        out.append(p)
    return out


# ================================================================== the clump body
def clump_balls(B, seed):
    """Core ellipsoid + mid clumps on an irregular envelope + small puffs ON the mid clumps (cauliflower sub-clumps
    with real crevices between them)."""
    rng = random.Random(seed)
    A, zc = B["A"], B["zc"]
    cen = Vector((0.0, 0.0, zc))
    lobes = [(Vector(d).normalized(), a, w) for d, a, w in B["lobes"]]

    def env(d):
        k = 1.0
        for ld, amp, w in lobes:
            ang = math.acos(max(-1.0, min(1.0, d.dot(ld))))
            k += amp * math.exp(-(ang / w) ** 2)
        k *= 1 - B["under"] * smoothstep(0.0, -0.8, d.z)
        return Vector((d.x * A[0], d.y * A[1], d.z * A[2])) * k

    def rdir(zmin):
        while True:
            d = Vector((rng.gauss(0, 1), rng.gauss(0, 1), rng.gauss(0, 1)))
            if d.length > 1e-6:
                d.normalize()
                if d.z > zmin:
                    return d

    balls = [(cen.copy(), 1.0, (A[0] * B.get("core", 0.8), A[1] * B.get("core", 0.8), A[2] * B.get("core", 0.8)))]
    mids = []
    for _ in range(B["n_mid"]):
        d = rdir(-0.55)
        r = B["r_mid"] * rng.uniform(0.78, 1.22)
        c = cen + env(d) * rng.uniform(0.6, 0.72)
        mids.append((c, r, d))
        balls.append((c, r, (1.0, 1.0, rng.uniform(0.8, 0.98))))
    for c, r, d in mids:
        for _ in range(rng.randint(*B["per_mid"])):
            e = (d + Vector((rng.gauss(0, 0.55), rng.gauss(0, 0.55), rng.gauss(0, 0.55) + 0.25))).normalized()
            rs = B["r_small"] * rng.uniform(0.72, 1.28)
            balls.append((c + e * r * rng.uniform(0.62, 0.8), rs, (1.0, 1.0, 1.0)))
    return balls


def clump_body(name, B, seed, voxel, mat, col_fn):
    rng = random.Random(seed)
    bm = bmesh.new()
    for c, r, sq in clump_balls(B, seed):
        o = Vector((rng.uniform(-60, 60), rng.uniform(-60, 60), rng.uniform(-60, 60)))
        ret = bmesh.ops.create_icosphere(bm, subdivisions=3, radius=1.0)
        for v in ret["verts"]:
            d = v.co.normalized()
            k = 1 + 0.2 * fbm(d * 1.5 + o, 2)
            v.co = c + Vector((d.x * r * sq[0], d.y * r * sq[1], d.z * r * sq[2])) * k
    ob = obj_from_bm(bm, name)
    rm = ob.modifiers.new("Remesh", "REMESH")
    rm.mode = "VOXEL"
    rm.voxel_size = voxel
    rm.adaptivity = 0.0
    apply_mods(ob)
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    for _ in range(B.get("smooth", 2)):
        bmesh.ops.smooth_vert(bm, verts=bm.verts, factor=0.5, use_axis_x=True, use_axis_y=True, use_axis_z=True)
    bm.normal_update()
    off = Vector((seed * 1.7, seed * 0.3, 11.0))
    off2 = Vector((seed * 0.9, 5.0, seed * 1.3))
    a1, f1, a2, f2 = B["disp"]
    for v in bm.verts:
        p = v.co
        v.co = p + v.normal * (a1 * fbm(p * f1 + off, 3) + a2 * fbm(p * f2 + off2, 2))
    # flat underside (hidden), then fit to the target size (centred on the trunk axis)
    zf = B["zflat"]
    for v in bm.verts:
        if v.co.z < zf:
            v.co.z = zf
    xs = [v.co.x for v in bm.verts]
    ys = [v.co.y for v in bm.verts]
    zs = [v.co.z for v in bm.verts]
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    W, D, H = B["dims"]
    sx, sy = W / (max(xs) - min(xs)), D / (max(ys) - min(ys))
    sz = (H - zf) / (max(zs) - zf)
    for v in bm.verts:
        v.co = Vector(((v.co.x - cx) * sx, (v.co.y - cy) * sy, zf + (v.co.z - zf) * sz))
    bm.normal_update()
    bm.to_mesh(ob.data)
    bm.free()
    me = ob.data
    cols, rgh = [], []
    for v in me.vertices:
        c, r = col_fn(v.co, v.normal)
        cols.append(c)
        rgh.append((r, r, r))
    set_colors(me, "Col", cols)
    set_colors(me, "Rough", rgh)
    me.shade_smooth()
    me.materials.append(mat)
    return ob


def decimate_to(hi, name, tris, inflate=0.0):
    lo = link(bpy.data.objects.new(name, hi.data.copy()))
    t0 = tris_of(hi)
    ratio = min(1.0, tris / t0)
    d = lo.modifiers.new("D", "DECIMATE")
    d.ratio = ratio
    lo.modifiers.new("T", "TRIANGULATE")
    apply_mods(lo)
    got = tris_of(lo)
    if abs(got - tris) > 0.06 * tris and got > 0:
        bpy.data.objects.remove(lo)
        lo = link(bpy.data.objects.new(name, hi.data.copy()))
        d = lo.modifiers.new("D", "DECIMATE")
        d.ratio = min(1.0, ratio * tris / got)
        lo.modifiers.new("T", "TRIANGULATE")
        apply_mods(lo)
    me = lo.data
    me.name = name
    for a in list(me.color_attributes):
        me.color_attributes.remove(a)
    if inflate:
        bm = bmesh.new()
        bm.from_mesh(me)
        bm.normal_update()
        for v in bm.verts:
            v.co += v.normal * inflate
        bm.to_mesh(me)
        bm.free()
    me.shade_smooth()
    return lo


def surface_samples(ob, n, rng):
    """Area-weighted points + interpolated normals on ob (world = local here)."""
    me = ob.data
    me.calc_loop_triangles()
    tri = np.empty(len(me.loop_triangles) * 3, np.int32)
    me.loop_triangles.foreach_get("vertices", tri)
    tri = tri.reshape(-1, 3)
    co = np.empty(len(me.vertices) * 3, np.float32)
    me.vertices.foreach_get("co", co)
    co = co.reshape(-1, 3)
    vn = np.empty(len(me.vertices) * 3, np.float32)
    me.vertices.foreach_get("normal", vn)
    vn = vn.reshape(-1, 3)
    a, b, c = co[tri[:, 0]], co[tri[:, 1]], co[tri[:, 2]]
    area = 0.5 * np.linalg.norm(np.cross(b - a, c - a), axis=1)
    idx = rng.choice(len(tri), n, p=area / area.sum())
    r1, r2 = rng.random(n), rng.random(n)
    s = np.sqrt(r1)
    w0, w1, w2 = 1 - s, s * (1 - r2), s * r2
    P = a[idx] * w0[:, None] + b[idx] * w1[:, None] + c[idx] * w2[:, None]
    N = vn[tri[idx, 0]] * w0[:, None] + vn[tri[idx, 1]] * w1[:, None] + vn[tri[idx, 2]] * w2[:, None]
    N /= np.linalg.norm(N, axis=1)[:, None] + 1e-9
    return [Vector(p) for p in P], [Vector(q) for q in N], float(area.sum())


def bvh_of(objs):
    bm = bmesh.new()
    for o in objs:
        tmp = o.data.copy()
        tmp.transform(o.matrix_world)
        bm.from_mesh(tmp)
        bpy.data.meshes.remove(tmp)
    bm.normal_update()
    return BVHTree.FromBMesh(bm), bm


def inside(bvh, p):
    loc, nrm, idx, dist = bvh.find_nearest(p)
    if loc is None:
        return False
    return (p - loc).dot(nrm) < 0


def dart(cands, mind, limit):
    out = []
    m2 = mind * mind
    for p, n in cands:
        if all((p - q).length_squared > m2 for q, _ in out):
            out.append((p, n))
            if len(out) >= limit:
                break
    return out


# ================================================================== materials
def mat_leaf(name, vein_light=0.5, edge_dark=0.3, bump=0.6, freq=6.0, edge_col=None):
    """Hi-leaf shader: vertex colour + rough, veins (midrib + angled laterals) lighter, darker margin, vein grooves as a
    Bump (the Cycles NORMAL bake picks it up)."""
    m = mat_vc(name)
    nt = m.node_tree
    L = nt.links
    bsdf = nt.nodes["Principled BSDF"]
    vc = next(n for n in nt.nodes if n.bl_idname == "ShaderNodeVertexColor" and n.layer_name == "Col")
    uvn = nt.nodes.new("ShaderNodeUVMap")
    uvn.uv_map = "LeafUV"
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    L.new(uvn.outputs["UV"], sep.inputs["Vector"])

    def M(op, a, b=None, c=None):
        n = nt.nodes.new("ShaderNodeMath")
        n.operation = op
        for i, x in enumerate((a, b, c)):
            if x is None:
                continue
            if isinstance(x, (int, float)):
                n.inputs[i].default_value = float(x)
            else:
                L.new(x, n.inputs[i])
        return n.outputs[0]

    def SS(x, a, b):
        n = nt.nodes.new("ShaderNodeMapRange")
        n.interpolation_type = "SMOOTHSTEP"
        n.clamp = True
        L.new(x, n.inputs["Value"])
        n.inputs["From Min"].default_value = a
        n.inputs["From Max"].default_value = b
        n.inputs["To Min"].default_value = 0.0
        n.inputs["To Max"].default_value = 1.0
        return n.outputs["Result"]

    U, V = sep.outputs["X"], sep.outputs["Y"]
    au = M("ABSOLUTE", U)
    mid = M("SUBTRACT", 1.0, SS(au, 0.0, 0.09))
    mid = M("MULTIPLY", mid, M("SUBTRACT", 1.0, SS(V, 0.82, 1.0)))
    s = M("MULTIPLY_ADD", au, -0.5, V)
    lat = M("POWER", M("MULTIPLY_ADD", M("COSINE", M("MULTIPLY", s, TAU * freq)), 0.5, 0.5), 8.0)
    lat = M("MULTIPLY", lat, SS(au, 0.06, 0.16))
    lat = M("MULTIPLY", lat, M("SUBTRACT", 1.0, SS(au, 0.66, 0.95)))
    vein = M("MAXIMUM", mid, M("MULTIPLY", lat, 0.8))
    edge = SS(au, 0.74, 1.0)
    h1 = nt.nodes.new("ShaderNodeHueSaturation")
    h1.inputs["Saturation"].default_value = 1.0
    h1.inputs["Value"].default_value = 1.0 + vein_light
    L.new(vein, h1.inputs["Fac"])
    L.new(vc.outputs["Color"], h1.inputs["Color"])
    if edge_col is None:
        h2 = nt.nodes.new("ShaderNodeHueSaturation")
        h2.inputs["Value"].default_value = 1.0 - edge_dark
        L.new(edge, h2.inputs["Fac"])
        L.new(h1.outputs["Color"], h2.inputs["Color"])
        L.new(h2.outputs["Color"], bsdf.inputs["Base Color"])
    else:                                           # margin tinted toward a deep saturated hue (no khaki / mud)
        mx = nt.nodes.new("ShaderNodeMix")
        mx.data_type = "RGBA"
        L.new(M("MULTIPLY", edge, edge_dark), sk(mx.inputs, "Factor_Float"))
        L.new(h1.outputs["Color"], sk(mx.inputs, "A_Color"))
        sk(mx.inputs, "B_Color").default_value = (*edge_col, 1.0)
        L.new(sk(mx.outputs, "Result_Color"), bsdf.inputs["Base Color"])
    height = M("SUBTRACT", M("MULTIPLY", M("SUBTRACT", 1.0, au), 0.35), vein)
    bp = nt.nodes.new("ShaderNodeBump")
    bp.inputs["Strength"].default_value = bump
    bp.inputs["Distance"].default_value = 0.012
    L.new(height, bp.inputs["Height"])
    L.new(bp.outputs["Normal"], bsdf.inputs["Normal"])
    return m


def mat_tex(name, col_img, rough=0.6, alpha=False):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    t = nt.nodes.new("ShaderNodeTexImage")
    t.image = col_img
    nt.links.new(t.outputs["Color"], b.inputs["Base Color"])
    if alpha:
        nt.links.new(t.outputs["Alpha"], b.inputs["Alpha"])
        try:
            m.surface_render_method = "DITHERED"
        except Exception:
            pass
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = 0.0
    return m


def placeholder_mats(names):
    return [mat_flat("_" + n, (0.5, 0.5, 0.5)) for n in names]


# ================================================================== UV layout + bakes
def pack_uvs(ob, prio, skipf=(), margin=0.002):
    """Equal texel density, then priorities ({mat index: scale}), then pack. Faces in skipf stay out (two-sided leaf
    bottoms, repeated thorns: they get their source face's UVs afterwards, copy_uvs)."""
    me = ob.data
    sc = bpy.context.scene
    sc.tool_settings.use_uv_select_sync = True
    sc.tool_settings.mesh_select_mode = (False, False, True)
    only(ob)
    skipf = set(skipf)

    def select():
        bpy.ops.object.mode_set(mode="EDIT")
        bm = bmesh.from_edit_mesh(me)
        bm.faces.ensure_lookup_table()
        for f in bm.faces:
            f.select_set(False)
        for f in bm.faces:
            if f.index not in skipf:
                f.select_set(True)
        bmesh.update_edit_mesh(me)

    select()
    bpy.ops.uv.average_islands_scale()
    bpy.ops.object.mode_set(mode="OBJECT")
    uv = me.uv_layers.active.data
    for p in me.polygons:
        k = prio.get(p.material_index, 1.0)
        if k != 1.0 and p.index not in skipf:
            for li in p.loop_indices:
                uv[li].uv = uv[li].uv * k
    select()
    bpy.ops.uv.pack_islands(rotate=True, rotate_method="ANY", margin_method="FRACTION", margin=margin,
                            shape_method="CONCAVE", merge_overlap=False)
    bpy.ops.object.mode_set(mode="OBJECT")


def copy_uvs(ob, copies):
    me = ob.data
    uv = me.uv_layers.active.data
    for b, t, rev in copies:
        pb, pt = me.polygons[b], me.polygons[t]
        tl = [uv[li].uv.copy() for li in pt.loop_indices]
        n = len(tl)
        for k, li in enumerate(pb.loop_indices):
            uv[li].uv = tl[n - 1 - k] if rev else tl[k]


def split_mats(ob, name, keep):
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    bmesh.ops.delete(bm, geom=[f for f in bm.faces if f.material_index not in keep], context="FACES")
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    for m in ob.data.materials:
        me.materials.append(m)
    o = link(bpy.data.objects.new(name, me))
    o.matrix_world = ob.matrix_world.copy()
    return o


SAMPLES = {"NORMAL": 6, "AO": 40, "DIFFUSE": 6, "ROUGHNESS": 2, "EMIT": 1}


def bake_groups(groups, size, prefix, ao_strength, ao_dist, ao_tint=None):
    """(Copied + adapted from PumpkinEggs/eggs.py.) groups: [(lo part, [hi parts], cage, maxray)]; the lo parts share
    one UV layout. Each lo part only matches rays against ITS OWN hi parts. Coverage (EMIT of the lo itself) and hit
    masks (EMIT of white hi) are baked with margin 0; covered texels that missed get values grown from their own
    group's hits; the margin is dilated at the end. AO sees the whole scene (every hi part renders; the lo parts are
    invisible to rays). Few samples for the deterministic passes, more for AO."""
    sc = bpy.context.scene
    sc.world.light_settings.distance = ao_dist
    shp = (size, size, 4)
    acc = {k: np.zeros(shp, np.float32) for k in ("albedo", "normal", "rough", "ao")}
    owned = np.zeros((size, size), bool)
    zero = np.zeros(size * size * 4, np.float32)
    t_lin = bpy.data.images.new(prefix + "_tmpL", size, size, alpha=False)
    t_lin.colorspace_settings.name = "Non-Color"
    t_rgb = bpy.data.images.new(prefix + "_tmpC", size, size, alpha=False)
    bmat = bpy.data.materials.new(prefix + "_bake")
    bmat.use_nodes = True
    tex = bmat.node_tree.nodes.new("ShaderNodeTexImage")
    bmat.node_tree.nodes.active = tex
    cmat = bpy.data.materials.new(prefix + "_cov")
    cmat.use_nodes = True
    nt = cmat.node_tree
    nt.nodes.remove(nt.nodes["Principled BSDF"])
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = (1, 1, 1, 1)
    em.inputs["Strength"].default_value = 1.0
    nt.links.new(em.outputs["Emission"], nt.nodes["Material Output"].inputs["Surface"])
    ctex = nt.nodes.new("ShaderNodeTexImage")
    ctex.image = t_lin
    nt.nodes.active = ctex
    fast = CFG["fast"]

    def bake(node, img, kind, s2a, cage=0.0, maxray=0.0, **kw):
        sc.cycles.samples = max(1, SAMPLES.get(kind, 4) // (4 if fast else 1))
        node.image = img
        img.pixels.foreach_set(zero)
        bpy.ops.object.bake(type=kind, use_selected_to_active=s2a, cage_extrusion=cage, max_ray_distance=maxray,
                            margin=0, use_clear=False, **kw)
        a = np.empty(size * size * 4, np.float32)
        img.pixels.foreach_get(a)
        return a.reshape(shp)

    def emit_white(his, on, saved):
        if on:
            for h in his:
                for m in h.data.materials:
                    if m and m.use_nodes:
                        for n in m.node_tree.nodes:
                            if n.type == "BSDF_PRINCIPLED":
                                ls = [l for l in m.node_tree.links if l.to_socket == n.inputs["Emission Color"]]
                                saved.append((m, n, tuple(n.inputs["Emission Color"].default_value),
                                              n.inputs["Emission Strength"].default_value,
                                              [(l.from_socket, l.to_socket) for l in ls]))
                                for l in ls:
                                    m.node_tree.links.remove(l)
                                n.inputs["Emission Color"].default_value = (1, 1, 1, 1)
                                n.inputs["Emission Strength"].default_value = 1.0
        else:
            for m, n, col, st, ls in saved:
                n.inputs["Emission Color"].default_value = col
                n.inputs["Emission Strength"].default_value = st
                for a, b in ls:
                    m.node_tree.links.new(a, b)
            saved.clear()

    stats = {}
    for lo, his, cage, maxray in groups:
        for attr in ("visible_shadow", "visible_diffuse", "visible_glossy", "visible_transmission",
                     "visible_camera"):
            setattr(lo, attr, False)
    for lo, his, cage, maxray in groups:
        t_g = time.time()
        for o in sc.objects:
            o.select_set(False)
        lo.select_set(True)
        bpy.context.view_layer.objects.active = lo
        lo.data.materials.clear()
        lo.data.materials.append(cmat)
        cov = bake(ctex, t_lin, "EMIT", False)[..., 0] > 0.5
        lo.data.materials.clear()
        lo.data.materials.append(bmat)
        for h in his:
            h.hide_render = False
            h.select_set(True)
        out = {"normal": bake(tex, t_lin, "NORMAL", True, cage, maxray, normal_space="TANGENT"),
               "ao": bake(tex, t_lin, "AO", True, cage, maxray),
               "albedo": bake(tex, t_rgb, "DIFFUSE", True, cage, maxray, pass_filter={"COLOR"}),
               "rough": bake(tex, t_lin, "ROUGHNESS", True, cage, maxray)}
        saved = []
        emit_white(his, True, saved)
        hit = bake(tex, t_lin, "EMIT", True, cage, maxray)[..., 0] > 0.5
        emit_white(his, False, saved)
        hit &= cov
        for k, arr in out.items():
            filled = fill_misses(arr, hit, iters=6)
            acc[k][cov] = filled[cov]
        owned |= cov
        stats[lo.name] = {"texels": int(cov.sum()), "miss": round(float(1 - hit.sum() / max(1, cov.sum())), 4),
                          "s": round(time.time() - t_g, 1)}
        log("  baked", lo.name, stats[lo.name])
    for k in acc:
        acc[k] = fill_misses(acc[k], owned, iters=10)
    ao = acc["ao"][..., :1]
    if ao_tint is None:
        acc["albedo"][..., :3] *= (1 - ao_strength) + ao_strength * ao
    else:      # occluded foliage keeps a warm / deep hue instead of going grey-olive (light through the leaves)
        tint = np.array(ao_tint, np.float32)[None, None, :]
        acc["albedo"][..., :3] *= (1 - ao_strength) + ao_strength * (ao + (1 - ao) * tint)
    imgs = {}
    for k, cs in (("albedo", "sRGB"), ("normal", "Non-Color"), ("rough", "Non-Color"), ("ao", "Non-Color")):
        acc[k][..., 3] = 1.0
        img = bpy.data.images.new(prefix + "_" + k, size, size, alpha=False)
        img.colorspace_settings.name = cs
        img.pixels.foreach_set(acc[k].ravel())
        save_png(img, os.path.join(MAPS, f"{prefix}_{k}.png"))
        imgs[k] = img
    for i in (t_lin, t_rgb):
        bpy.data.images.remove(i)
    imgs["stats"] = stats
    imgs["coverage"] = round(float(owned.mean()), 3)
    return imgs


def finish_lo(lo, name, imgs):
    lo.hide_render = False
    lo.data.polygons.foreach_set("material_index", [0] * len(lo.data.polygons))
    pbr_material(lo, name + "_PBR", imgs)
    for a in list(lo.data.color_attributes):
        lo.data.color_attributes.remove(a)


def hide(*objs):
    for o in objs:
        o.hide_render = True
        o.hide_viewport = True


# ================================================================== textures for webs (adapted from WebsSpiders)
def mnoise(n, scale, seed, octaves=3, aspect=(1.0, 1.0)):
    out = np.empty((n, n), np.float32)
    off = Vector((seed * 13.17, seed * 7.31, seed * 3.77))
    sx, sy = scale * aspect[0] / n, scale * aspect[1] / n
    for j in range(n):
        for i in range(n):
            out[j, i] = fbm(Vector((i * sx, j * sy, 0.0)) + off, octaves)
    lo, hi = np.percentile(out, 1), np.percentile(out, 99)
    return np.clip((out - lo) / max(1e-6, hi - lo), 0, 1)


def make_image(name, arr, colorspace, path):
    h, w = arr.shape[:2]
    img = bpy.data.images.new(name, w, h, alpha=True)
    img.colorspace_settings.name = colorspace
    img.pixels.foreach_set(np.ascontiguousarray(arr, dtype=np.float32).ravel())
    img.filepath_raw = path
    img.file_format = "PNG"
    img.save()
    img.alpha_mode = "STRAIGHT"
    return img


def srgb(c):
    return np.array([v / 255.0 for v in c], np.float32)


def strand_texture(prefix, size=128, seed=3):
    nz = mnoise(size, 5.0, seed, 3)
    dm = np.clip((nz - 0.5) * 1.6, 0, 1) * 0.45
    col = np.zeros((size, size, 4), np.float32)
    base, dust = srgb((218, 220, 228)), srgb((180, 174, 166))
    col[..., :3] = base[None, None, :] * (1 - dm[..., None]) + dust[None, None, :] * dm[..., None]
    col[..., 3] = 1
    return make_image(prefix + "_albedo", col, "sRGB", os.path.join(MAPS, prefix + "_albedo.png"))


# ================================================================== shared review helpers
def shoot_fov(path, loc, target, vfov=70.0, lens=None):
    sc = bpy.context.scene
    cd = bpy.data.cameras.new("Cam")
    cam = link(bpy.data.objects.new("Cam", cd))
    cam.location = Vector(loc)
    cam.rotation_euler = (Vector(target) - cam.location).to_track_quat("-Z", "Y").to_euler()
    if lens:
        cd.lens = lens
    else:
        cd.sensor_fit = "VERTICAL"
        cd.sensor_height = 24.0
        cd.lens = 12.0 / math.tan(math.radians(vfov / 2))
    cd.clip_start = 0.05
    cd.clip_end = 5000
    sc.camera = cam
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(cam)
    return path


def ground_set(beds=((0.0, 0.0),)):
    g = mat_noise("Grass", lin((92, 168, 58)), lin((70, 142, 44)), nscale=0.35, detail=6, rough=0.95, lo=0.3, hi=0.7)
    s = mat_noise("Soil", lin((112, 80, 54)), lin((82, 58, 40)), nscale=1.6, detail=6, rough=0.95, lo=0.3, hi=0.7,
                  bump=0.3)
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=300.0)
    o = obj_from_bm(bm, "Ground", smooth=False)
    o.data.materials.append(g)
    for k, (x, y) in enumerate(beds):
        bm = bmesh.new()
        bmesh.ops.create_circle(bm, cap_ends=True, radius=4.4, segments=64)
        b = obj_from_bm(bm, "Bed%d" % k, smooth=False)
        b.location = (x, y, 0.01)
        b.data.materials.append(s)


def review_scene():
    sc = review_setup()
    sc.eevee.taa_render_samples = 64
    return sc


# ================================================================== BUSH_THORN
TH_BODY = dict(A=(2.3, 2.2, 1.6), zc=1.45, core=0.8, n_mid=12, per_mid=(2, 4), r_mid=0.98, r_small=0.5, under=0.12,
               lobes=[((-0.5, 0.6, 0.6), 0.16, 0.7), ((0.7, -0.4, 0.2), 0.1, 0.6), ((0.2, 0.9, 0.1), -0.08, 0.5)],
               disp=(0.2, 0.8, 0.05, 2.8), zflat=0.14, dims=(5.35, 5.15, 3.8), smooth=2)
TH_G = [(0.0, lin((30, 72, 44))), (0.5, lin((40, 94, 58))), (1.0, lin((28, 86, 78)))]
TH_P = [(0.0, lin((136, 30, 60))), (0.35, lin((122, 38, 92))), (0.7, lin((100, 46, 122))), (1.0, lin((84, 40, 108)))]
TH_CANE = dict(base=lin((84, 92, 44)), mid=lin((96, 30, 60)), dark=lin((62, 20, 40)), bloom=lin((156, 124, 156)),
               tip=lin((136, 42, 62)))
# arching canes: (start r, az, z), (apex r, az, z), (tip r, az, z), r0, r1
TH_ARCHES = [((0.45, 140, -0.05), (1.05, 134, 5.35), (2.55, 150, 4.0), 0.105, 0.042),
             ((0.5, 18, -0.05), (1.0, 24, 5.05), (2.75, 8, 3.55), 0.1, 0.04),
             ((0.6, 302, -0.05), (1.55, 292, 4.75), (3.05, 300, 3.8), 0.098, 0.038),     # the spider cane
             ((0.5, 226, -0.05), (1.3, 218, 4.45), (2.95, 233, 3.05), 0.094, 0.036),
             ((0.35, 82, -0.05), (0.75, 86, 5.5), (2.35, 70, 4.5), 0.105, 0.042)]
TH_SIDE = [((0.8, 8, 1.7), (3.15, 352, 2.15)), ((0.8, 66, 2.2), (3.0, 58, 2.75)), ((0.9, 124, 1.5), (3.1, 118, 1.9)),
           ((0.8, 182, 2.3), (3.05, 190, 2.6)), ((0.9, 248, 1.4), (3.1, 256, 1.75)), ((0.8, 334, 1.2), (3.2, 330, 1.55))]
TH_LOW = [((0.5, 268, 0.15), (3.05, 262, 0.18)), ((0.6, 160, 0.2), (3.1, 168, 0.22)), ((0.6, 40, 0.2), (3.05, 30, 0.2))]
SPIDER_CANE = 2


def bez(p0, p1, p2, p3, t):
    a = 1 - t
    return p0 * (a * a * a) + p1 * (3 * a * a * t) + p2 * (3 * a * t * t) + p3 * (t * t * t)


def cane_path(c0, c1, c2, c3, rng, twist=0.07, period=1.0, wob=0.1, step=0.04):
    raw = [bez(c0, c1, c2, c3, i / 300) for i in range(301)]
    pts = resample(raw, step)
    T, Ns, Bs = frames(pts)
    s = arclen(pts)
    o = Vector((rng.uniform(-40, 40), rng.uniform(-40, 40), rng.uniform(-40, 40)))
    ph = rng.uniform(0, TAU)
    out = []
    for i, p in enumerate(pts):
        t = s[i] / s[-1]
        env = math.sin(math.pi * min(1.0, t * 1.15)) ** 0.5
        a = TAU * s[i] / period + ph
        q = p + (Ns[i] * math.cos(a) + Bs[i] * math.sin(a)) * twist * env
        q += Vector((noise.noise(o + Vector((s[i] * 0.6, 0, 0))), noise.noise(o + Vector((0, s[i] * 0.6, 3.1))),
                     noise.noise(o + Vector((7.7, 0, s[i] * 0.6))))) * wob * env
        out.append(q)
    return out


def arch_ctrl(st, ap, tp):
    p0, pa, p3 = cyl(*st), cyl(*ap), cyl(*tp)
    out = (pa - p0)
    out.z = 0
    outd = out.normalized() if out.length > 1e-6 else Vector((1, 0, 0))
    lo_s, hi_s = 0.5, 3.0
    for _ in range(40):                       # scale the control heights so the arch peaks at the apex height
        k = (lo_s + hi_s) / 2
        p1 = p0 + Vector((0, 0, (pa.z - p0.z) * 0.85 * k))
        p2 = pa + outd * 0.9 + Vector((0, 0, (pa.z - p0.z) * 0.18 * k))
        top = max(bez(p0, p1, p2, p3, i / 100).z for i in range(101))
        if top > pa.z:
            hi_s = k
        else:
            lo_s = k
    return p0, p1, p2, p3


def side_ctrl(st, tp, rng):
    p0, p3 = cyl(*st), cyl(*tp)
    d = p3 - p0
    p1 = p0 + d * 0.33 + Vector((0, 0, rng.uniform(0.35, 0.7)))
    p2 = p0 + d * 0.7 + Vector((0, 0, rng.uniform(0.4, 0.75)))
    return p0, p1, p2, p3


def low_ctrl(st, tp, rng):
    p0, p3 = cyl(*st), cyl(*tp)
    d = p3 - p0
    side = Vector((-d.y, d.x, 0)).normalized() * rng.uniform(-0.5, 0.5)
    p1 = p0 + d * 0.3 + Vector((0, 0, rng.uniform(0.5, 0.8))) + side
    p2 = p0 + d * 0.7 + Vector((0, 0, rng.uniform(0.35, 0.6))) - side
    return p0, p1, p2, p3


def thorn_cfn(rng, p, n, off):
    """Regional colour (coherent patches), small per-leaf variation: green centre turning purple / wine at the margin
    and tip; more purple on top and in some patches."""
    g = ramp(TH_G, 0.5 + 0.7 * fbm(p * 0.6 + off * 1.3, 2) + rng.gauss(0, 0.08))
    pu = ramp(TH_P, 0.5 + 0.7 * fbm(p * 0.5 + off * 0.7, 2) + rng.gauss(0, 0.08))
    k = max(0.0, 0.5 + 0.85 * fbm(p * 0.42 + off, 2) + 0.15 * (p.z - 2.0) / 2.0 + rng.gauss(0, 0.12))
    lift = rng.uniform(0.94, 1.08)

    def f(u, v):
        e = max(abs(u), v ** 1.5)
        c = mix(g, pu, clamp01(k * (0.3 + 0.8 * e)))
        return kcol(mix(kcol(c, 0.85), c, smoothstep(0.0, 0.5, v)), lift)
    return f


def cane_cfn(o):
    C = TH_CANE

    def f(t, a):
        c = mix(C["base"], C["mid"], smoothstep(0.0, 0.22, t))
        c = mix(c, C["tip"], smoothstep(0.7, 1.0, t))
        g = noise.noise(Vector((math.cos(a) * 1.4, math.sin(a) * 1.4, t * 16.0)) + o)
        c = mix(c, C["dark"], 0.45 * smoothstep(0.0, 0.5, g))
        c = mix(c, C["bloom"], 0.4 * smoothstep(0.25, 0.65, -g))
        return c
    return f


def cane_rfn(o, period_k):
    def f(t, a):
        r = 1 + 0.09 * math.cos(4 * a + t * period_k)
        r *= 1 + 0.04 * noise.noise(Vector((math.cos(a) * 2, math.sin(a) * 2, t * 40)) + o)
        return r
    return f


def thorn_spots(pts, radii, rng, spacing=(0.2, 0.3)):
    """Thorns along a cane: (base point, direction, length, base radius, ring index)."""
    T, Ns, Bs = frames(pts)
    s = arclen(pts)
    out = []
    nxt = rng.uniform(0.15, 0.3)
    ang = rng.uniform(0, TAU)
    for i in range(1, len(pts) - 2):
        if s[i] < nxt:
            continue
        nxt = s[i] + rng.uniform(*spacing)
        ang += 2.4 + rng.uniform(-0.3, 0.3)
        nrm = Ns[i] * math.cos(ang) + Bs[i] * math.sin(ang)
        d = (nrm * 0.78 - T[i] * 0.62).normalized()
        L = (0.11 + 0.11 * radii[i] / 0.1) * rng.uniform(0.85, 1.2)
        out.append((pts[i] + nrm * radii[i] * 0.75, d, L, min(0.055, radii[i] * 0.55), i, nrm))
    return out


def cone(mb, base, d, L, r0, sides, ts=(0.0,), mat=0, cfn=None, rough=0.5, uv=True, shared=None):
    """A straight cone from base along d: rings at fractions ts (radius r0 (1-t)^0.9), then the tip. shared = a dict:
    every cone given the same dict maps onto ONE UV template (tiny repeated parts, e.g. thorns)."""
    d = d.normalized()
    n1 = d.orthogonal().normalized()
    n2 = d.cross(n1)
    first = False
    if uv and shared is not None:
        if "o" not in shared:
            shared["C"], shared["L"] = TAU * r0, L
            shared["o"] = mb.alloc(shared["C"] + 0.02, L + 0.04)
            first = True
        C, L_uv, (ox, oy) = shared["C"], shared["L"], shared["o"]
    else:
        C, L_uv = TAU * r0, L
        ox, oy = mb.alloc(C + 0.02, L + 0.04) if uv else (0.0, 0.0)
    rings = []
    for t in ts:
        r = r0 * (1 - t) ** 0.9
        rings.append([mb.v(base + d * (L * t) + (n1 * math.cos(TAU * j / sides) + n2 * math.sin(TAU * j / sides)) * r,
                           cfn(t, 0.0) if cfn else (0.5, 0.5, 0.5), rough) for j in range(sides)])
    tip = mb.v(base + d * L, cfn(1.0, 0.0) if cfn else (0.5, 0.5, 0.5), rough)
    f0 = len(mb.F)
    for k in range(len(ts) - 1):
        for j in range(sides):
            jn = (j + 1) % sides
            mb.f((rings[k][j], rings[k][jn], rings[k + 1][jn], rings[k + 1][j]), mat,
                 [(ox + C * j / sides, oy + L_uv * ts[k]), (ox + C * (j + 1) / sides, oy + L_uv * ts[k]),
                  (ox + C * (j + 1) / sides, oy + L_uv * ts[k + 1]), (ox + C * j / sides, oy + L_uv * ts[k + 1])]
                 if uv else None)
    for j in range(sides):
        jn = (j + 1) % sides
        mb.f((rings[-1][j], rings[-1][jn], tip), mat,
             [(ox + C * j / sides, oy + L_uv * ts[-1]), (ox + C * (j + 1) / sides, oy + L_uv * ts[-1]),
              (ox + C * (j + 0.5) / sides, oy + L_uv)] if uv else None)
    if uv and shared is not None:
        fids = list(range(f0, len(mb.F)))
        if first:
            shared["faces"] = fids
        else:
            for a, b in zip(fids, shared["faces"]):
                mb.copies.append((a, b, False))
                mb.skipf.add(a)


def thorn_mesh(mb, base, d, L, r0, sides, hi, mat, cane_col, rough, uv=True, shared=None):
    ivory, dark = lin((228, 206, 174)), lin((92, 28, 30))

    def cf(t, a):
        c = mix(cane_col, ivory, smoothstep(0.1, 0.55, t))
        return mix(c, dark, smoothstep(0.75, 1.0, t))
    cone(mb, base, d, L, r0, sides, (0.0, 0.3, 0.6, 0.82) if hi else (0.0,), mat, cf, rough, uv, shared)


def berry_hi(mb, c, r, kind, rng, mat):
    ripe = {"black": (lin((30, 14, 40)), lin((10, 6, 14)), 0.14), "red": (lin((196, 26, 44)), lin((120, 10, 24)), 0.22),
            "purple": (lin((112, 20, 58)), lin((50, 8, 28)), 0.18)}[kind]
    hi_c, lo_c, rgh = ripe
    sphere_mesh(mb, c, r * 0.82, 16, 10, mat, lo_c, rgh, uv=False, sq=1.1)
    n = 30
    ga = math.pi * (3 - math.sqrt(5))
    for i in range(n):
        z = 0.82 - 1.7 * (i + 0.5) / n
        rr = math.sqrt(max(0.0, 1 - z * z))
        d = Vector((rr * math.cos(ga * i), rr * math.sin(ga * i), z))
        dc = mix(hi_c, lo_c, rng.uniform(0.0, 0.35))
        sphere_mesh(mb, c + Vector((d.x * r * 0.74, d.y * r * 0.74, d.z * r * 0.82)), r * 0.33, 10, 7, mat, dc, rgh,
                    uv=False, cfn=lambda q, dc=dc, d=d: mix(dc, lo_c, 0.6 * smoothstep(0.2, -0.6, q.dot(d))))
    # calyx: 5 small dry sepals on the top
    for k in range(5):
        a = TAU * k / 5 + rng.uniform(-0.2, 0.2)
        t = Vector((math.cos(a), math.sin(a), 0.0))
        fr = leaf_frame(UP, t, math.radians(-15))
        P = dict(L=r * 0.7, W=r * 0.16, cup=0.2, bend=0.3, kind="lance")
        leaf_hi(mb, c + Vector((0, 0, r * 0.95)), fr, P, lambda u, v: lin((84, 78, 40)), 0.7, mat, nu=3, nv=3)


def build_thorn():
    fast = CFG["fast"]
    size = 256 if fast else 1024
    fresh(8)
    rng = random.Random(1307)
    nrng = np.random.default_rng(1307)
    off = Vector((3.3, 9.1, 4.4))
    m_body = mat_vc("ThornBodyHi")
    m_leaf = mat_leaf("ThornLeafHi", vein_light=0.55, edge_dark=0.4, bump=0.6, freq=6.5, edge_col=lin((70, 18, 64)))
    m_wood = mat_vc("ThornWoodHi")
    m_berry = mat_vc("ThornBerryHi")

    def body_col(p, n):
        t = 0.5 + 0.5 * fbm(p * 0.8 + off, 2)
        return mix(lin((22, 16, 30)), lin((28, 46, 32)), t), 0.8

    hi = clump_body("ThornBody_hi", TH_BODY, 17, 0.1 if fast else 0.055, m_body, body_col)
    log("thorn body hi", tris_of(hi))
    body_lo = decimate_to(hi, "ThornBody_lo", 2550, inflate=0.1)
    smart_uv(body_lo)
    log("thorn body lo", tris_of(body_lo))
    bvh, bvh_bm = bvh_of([body_lo])
    # ---------------------------------------------------------------- canes (full paths, hi + exposed lo)
    canes = []
    for st, ap, tp, r0, r1 in TH_ARCHES:
        pts = cane_path(*arch_ctrl(st, ap, tp), rng, twist=0.04, period=1.5, wob=0.09)
        canes.append(dict(pts=pts, r0=r0, r1=r1, kind="arch"))
    for st, tp in TH_SIDE:
        pts = cane_path(*side_ctrl(st, tp, rng), rng, twist=0.06, period=0.9, wob=0.08)
        canes.append(dict(pts=pts, r0=0.075, r1=0.032, kind="side"))
    for st, tp in TH_LOW:
        pts = cane_path(*low_ctrl(st, tp, rng), rng, twist=0.06, period=0.9, wob=0.06)
        canes.append(dict(pts=pts, r0=0.08, r1=0.034, kind="low"))
    for c in canes:
        n = len(c["pts"])
        c["radii"] = [c["r0"] + (c["r1"] - c["r0"]) * (i / (n - 1)) ** 0.9 for i in range(n)]
        c["o"] = Vector((rng.uniform(-30, 30), rng.uniform(-30, 30), rng.uniform(-30, 30)))
        c["thorns"] = thorn_spots(c["pts"], c["radii"], rng)
        out = [not inside(bvh, p) and p.z > 0.02 for p in c["pts"]]
        c["out"] = out
    mbh_w = MB()          # hi wood (canes + thorns + berry stalks)
    mbh_b = MB()          # hi berries
    mbh_l = MB()          # hi clump leaves
    mbh_p = MB()          # hi twins of the protruding leaves
    mbl = MB()            # the game mesh
    mbl.add_object_mesh(body_lo, 0)
    MAT_BODY, MAT_TOP, MAT_BOT, MAT_WOOD, MAT_BERRY = 0, 1, 2, 3, 4
    thorn_uv = {}
    for c in canes:
        cf, rf = cane_cfn(c["o"]), cane_rfn(c["o"], 22.0)
        tube(mbh_w, c["pts"], c["radii"], 6 if fast else 12, 0, cfn=cf, rfn=rf, rough=0.45, cap_tip=True, tipk=2.0,
             uv=False)
        for base, d, L, r0, i, nrm in c["thorns"]:
            thorn_mesh(mbh_w, base - nrm * 0.01, d, L, r0, 8, True, 0, cf(i / len(c["pts"]), 0.0), 0.42, uv=False)
        # exposed part for the game mesh
        idx = [i for i, o in enumerate(c["out"]) if o]
        if not idx:
            continue
        i0 = max(0, idx[0] - 10)
        sub = c["pts"][i0:]
        lo_pts = resample(sub, 0.26 if c["kind"] == "arch" else 0.3)
        lo_r = interp_radii(sub, c["radii"][i0:], lo_pts)
        t0 = i0 / (len(c["pts"]) - 1)
        tube(mbl, lo_pts, lo_r, 5 if c["kind"] == "arch" else 4, MAT_WOOD, cap_tip=True, tipk=2.0, t0=t0)
        for base, d, L, r0, i, nrm in c["thorns"]:
            if c["out"][i]:
                thorn_mesh(mbl, base - nrm * 0.012, d, L, r0, 3, False, MAT_WOOD, (0.5,) * 3, 0.42, shared=thorn_uv)
    # ---------------------------------------------------------------- the clump leaves (bake source)
    P_s, N_s, area = surface_samples(hi, int(30 * 82 * (0.35 if fast else 1.0)), nrng)
    nleaf = 0
    for p, n in zip(P_s, N_s):
        if p.z < TH_BODY["zflat"] + 0.06:
            continue
        L = rng.uniform(0.34, 0.52)
        P = dict(L=L, W=L * rng.uniform(0.27, 0.33), cup=rng.uniform(0.2, 0.45), bend=rng.uniform(0.1, 0.32),
                 twist=rng.uniform(-0.4, 0.4), kind="broad" if rng.random() < 0.5 else "ovate")
        fr = leaf_frame(n, tangent_dir(n, rng), math.radians(rng.uniform(8, 36)), rng.uniform(-0.45, 0.45))
        leaf_hi(mbh_l, p + n * rng.uniform(-0.05, 0.1), fr, P, thorn_cfn(rng, p, n, off), 0.76, 0,
                nu=5, nv=5 if fast else 7)
        nleaf += 1
    log("thorn hi leaves", nleaf, "area", round(area, 1))
    # ---------------------------------------------------------------- protruding leaves (game mesh + hi twins)
    P_l, N_l, _ = surface_samples(body_lo, 1400, nrng)
    cands = [(p, n) for p, n in zip(P_l, N_l) if n.z > -0.35 and p.z > 0.45]
    prot = dart(cands, 0.43, 76)
    for p, n in prot:
        L = rng.uniform(0.5, 0.68)
        P = dict(L=L, W=L * rng.uniform(0.27, 0.32), cup=rng.uniform(0.25, 0.4), bend=rng.uniform(0.18, 0.38),
                 twist=rng.uniform(-0.35, 0.35), kind="broad" if rng.random() < 0.5 else "ovate")
        tilt = rng.uniform(14, 36) if rng.random() < 0.6 else rng.uniform(36, 58)
        fr = leaf_frame(n, tangent_dir(n, rng, 0.6), math.radians(tilt), rng.uniform(-0.4, 0.4))
        B = p - n * 0.07
        leaf_lo(mbl, B, fr, P, MAT_TOP, MAT_BOT)
        leaf_hi(mbh_p, B, fr, P, thorn_cfn(rng, p, n, off), 0.76, 0, nu=5, nv=7)
    # small leaves along the exposed canes
    ncl = 0
    for c in canes:
        pts = c["pts"]
        T, Ns, Bs = frames(pts)
        s = arclen(pts)
        nxt = 0.0
        for i in range(len(pts) - 6):
            if not c["out"][i] or s[i] < nxt or ncl >= 24 or (c["kind"] != "arch" and rng.random() < 0.5):
                continue
            nxt = s[i] + rng.uniform(0.7, 1.1)
            a = rng.uniform(0, TAU)
            nrm = Ns[i] * math.cos(a) + Bs[i] * math.sin(a)
            nrm = (nrm + UP * 0.6).normalized()
            L = rng.uniform(0.42, 0.56)
            P = dict(L=L, W=L * 0.3, cup=0.3, bend=rng.uniform(0.2, 0.35), twist=rng.uniform(-0.3, 0.3), kind="ovate")
            fr = leaf_frame(nrm, (T[i] + nrm * 0.2).normalized(), math.radians(rng.uniform(35, 60)),
                            rng.uniform(-0.5, 0.5))
            B = pts[i] + nrm * c["radii"][i] * 0.5
            leaf_lo(mbl, B, fr, P, MAT_TOP, MAT_BOT)
            leaf_hi(mbh_p, B, fr, P, thorn_cfn(rng, pts[i], nrm, off), 0.76, 0, nu=5, nv=7)
            ncl += 1
    log("thorn protruding leaves", len(prot), "cane leaves", ncl)
    # ---------------------------------------------------------------- berries (3 clusters)
    berries = []
    for ci, nb in ((3, 3), (10, 3)):                 # under the tip of the front-left arch, a front-right side cane
        tip = canes[ci]["pts"][-1]
        for k in range(nb):
            a = TAU * k / nb + rng.uniform(-0.3, 0.3)
            berries.append((tip + Vector((0.13 * math.cos(a), 0.13 * math.sin(a), -0.2 - 0.06 * k)), tip))
    hit = bvh.ray_cast(cyl(4.0, 255, 2.35), (Vector((0, 0, 2.35)) - cyl(4.0, 255, 2.35)).normalized())
    if hit[0] is not None:
        fp, fn = hit[0], hit[1]
        for k in range(4):
            a = TAU * k / 4 + 0.4
            berries.append((fp + fn * 0.17 + Vector((0.16 * math.cos(a), 0, 0.16 * math.sin(a))), fp + fn * 0.02))
    kinds = ["black", "black", "red", "black", "black", "purple", "black", "red", "black", "black"]
    for k, (c, anchor) in enumerate(berries):
        r = rng.uniform(0.13, 0.15)
        kind = kinds[k % len(kinds)]
        berry_hi(mbh_b, c, r, kind, rng, 0)
        sphere_mesh(mbl, c, r * 1.02, 7, 5, MAT_BERRY, sq=1.1)
        stalk = [anchor, anchor.lerp(c, 0.5) + Vector((0, 0, 0.03)), c + Vector((0, 0, r * 0.9))]
        tube(mbh_w, stalk, [0.022, 0.02, 0.018], 6, 0, cfn=lambda t, a: lin((70, 76, 36)), rough=0.6, cap_tip=False,
             uv=False)
        tube(mbl, stalk, [0.026, 0.024, 0.022], 3, MAT_WOOD, cap_tip=False)
    # ---------------------------------------------------------------- objects
    wood_hi = mbh_w.obj("ThornWood_hi", [m_wood], uv=None)
    berry_hi_o = mbh_b.obj("ThornBerries_hi", [m_berry], uv=None)
    leaves_hi = mbh_l.obj("ThornLeaves_hi", [m_leaf], uv="LeafUV")
    prot_hi = mbh_p.obj("ThornProt_hi", [m_leaf], uv="LeafUV")
    bush = mbl.obj("Bush", placeholder_mats(["Body", "LeafTop", "LeafBot", "Wood", "Berry"]))
    log("thorn game mesh by material", tris_by_mat(bush))
    log("thorn game mesh tris", tris_of(bush), "hi:", tris_of(leaves_hi), tris_of(prot_hi), tris_of(wood_hi),
        tris_of(berry_hi_o))
    hide(body_lo)
    pack_uvs(bush, {MAT_TOP: 1.25, MAT_BERRY: 1.6, MAT_WOOD: 1.1}, mbl.skipf)
    copy_uvs(bush, mbl.copies)
    bush.hide_render = True
    groups = []
    for nm, keep, his, cage, maxray in (("G_Body", (MAT_BODY,), [hi, leaves_hi, wood_hi, berry_hi_o], 0.36, 0.7),
                                        ("G_Leaf", (MAT_TOP,), [prot_hi], 0.03, 0.08),
                                        ("G_Wood", (MAT_WOOD,), [wood_hi], 0.05, 0.12),
                                        ("G_Berry", (MAT_BERRY,), [berry_hi_o], 0.05, 0.12)):
        groups.append((split_mats(bush, nm, keep), his, cage, maxray))
    imgs = bake_groups(groups, size, "BushThorn", ao_strength=0.55, ao_dist=0.7, ao_tint=(0.22, 0.06, 0.26))
    for g in groups:
        bpy.data.objects.remove(g[0])
    finish_lo(bush, "BushThorn", imgs)
    hide(hi, leaves_hi, prot_hi, wood_hi, berry_hi_o)
    # ---------------------------------------------------------------- the cobweb
    poles = []
    for i in (0, 1, SPIDER_CANE):                    # the veil snags on each cane ~0.55 above the foliage below it
        pts = canes[i]["pts"]
        top = max(range(len(pts)), key=lambda k: pts[k].z)
        pick = pts[top]
        for k in range(top):
            loc = bvh.ray_cast(pts[k] + Vector((0, 0, 0.01)), DOWN)[0]
            if loc is not None and pts[k].z - loc.z > 0.55 and not inside(bvh, pts[k]):
                pick = pts[k]
                break
        poles.append(pick)
    spider_tip = canes[SPIDER_CANE]["pts"][-1]
    web, silk, web_info = build_thorn_web(bvh, poles, spider_tip, rng, canes)
    rep = {"tris": {o.name: tris_of(o) for o in (bush, web, silk)}, "texture": size,
           "bake": imgs["stats"], "atlas_coverage": imgs["coverage"], "hi_leaves": nleaf,
           "protruding_leaves": len(prot) + ncl, "berries": len(berries)}
    rep.update(web_info)
    mn, mx = bbox_of([bush, web, silk])
    rep["bbox_blender"] = [[round(float(v), 3) for v in mn], [round(float(v), 3) for v in mx]]
    rep["size_roblox_XYZ"] = [round(float(mx[0] - mn[0]), 3), round(float(mx[2] - mn[2]), 3),
                              round(float(mx[1] - mn[1]), 3)]
    bvh_bm.free()
    finish("thorn", rep)
    return rep


VEIL = dict(cx=0.15, cy=-0.3, rx=2.2, ry=2.0, uvk=1.22)


def veil_rho_max(phi):
    o = Vector((3.1, 7.7, 0.4))
    return 1.0 + 0.17 * noise.noise(Vector((math.cos(phi) * 1.3, math.sin(phi) * 1.3, 0.0)) + o)


def veil_texture(prefix, size, seed, pole_uvs):
    """RGBA fake-cobweb veil (UV = top-down xy around the veil centre): a thin gauzy film with torn holes, a random
    fibre tangle, fibres fanning out from the tent poles, dust; alpha fades to 0 exactly at the veil's ragged rim."""
    V = VEIL
    rng = np.random.default_rng(seed)
    n = size
    fib = np.zeros((n, n), np.float32)

    def walk(x, y, ang, L, w, curl):
        steps = int(L / 0.5)
        xs, ys = np.empty(steps), np.empty(steps)
        for st in range(steps):
            ang += rng.normal(0, curl)
            x += 0.5 * math.cos(ang)
            y += 0.5 * math.sin(ang)
            xs[st], ys[st] = x, y
        ok = (xs >= 0) & (xs < n - 1) & (ys >= 0) & (ys < n - 1)
        xs, ys = xs[ok], ys[ok]
        if len(xs) == 0:
            return
        x0, y0 = np.floor(xs).astype(int), np.floor(ys).astype(int)
        fx, fy = xs - x0, ys - y0
        for dx, dy, ww in ((0, 0, (1 - fx) * (1 - fy)), (1, 0, fx * (1 - fy)), (0, 1, (1 - fx) * fy), (1, 1, fx * fy)):
            np.add.at(fib, (y0 + dy, x0 + dx), ww * w)

    sc = n / 512.0
    for _ in range(int(650 * sc * sc)):
        walk(rng.uniform(0, n), rng.uniform(0, n), rng.uniform(0, TAU), rng.uniform(40, 200) * sc,
             rng.uniform(0.25, 0.7), 0.025)
    for pu, pv in pole_uvs:
        for _ in range(int(150 * sc)):
            walk(pu * n + rng.normal(0, 3 * sc), pv * n + rng.normal(0, 3 * sc), rng.uniform(0, TAU),
                 rng.uniform(80, 320) * sc, rng.uniform(0.35, 0.85), 0.01)
    fib = np.clip(fib, 0, 1)
    uu = (np.arange(n) + 0.5) / n
    U, Vv = np.meshgrid(uu, uu)
    X = (U - 0.5) * 2 * V["uvk"]          # in units of the veil radii
    Y = (Vv - 0.5) * 2 * V["uvk"]
    phi = np.arctan2(Y, X)
    rmax = np.vectorize(veil_rho_max)(phi)
    rr = np.sqrt(X * X + Y * Y) / rmax
    film = 0.1 + 0.3 * mnoise(n, 3.0, seed + 1, 4)
    holes = mnoise(n, 3.4, seed + 2, 3)
    keep = np.clip((0.64 - holes) / 0.07, 0, 1)
    pole = np.zeros_like(U)
    for pu, pv in pole_uvs:
        pole += np.exp(-((U - pu) ** 2 + (Vv - pv) ** 2) / 0.004)
    film = np.clip(film * keep + 0.45 * pole, 0, 1)
    fib = fib * (0.4 + 0.6 * keep)
    alpha = 1 - (1 - film) * (1 - fib)
    rag = mnoise(n, 8.0, seed + 3, 3)
    edge = np.clip((1.0 - rr - 0.12 * rag) / 0.3, 0, 1)
    alpha = np.clip(alpha * edge * 1.12, 0, 1)
    dust = np.clip((mnoise(n, 4.5, seed + 4, 4) - 0.5) * 2.0, 0, 1) * 0.4
    silk_c, dust_c, bright = srgb((230, 228, 234)), srgb((176, 168, 158)), srgb((250, 250, 254))
    col = silk_c[None, None, :] * (1 - dust[..., None]) + dust_c[None, None, :] * dust[..., None]
    col = col * (1 - 0.5 * fib[..., None]) + bright[None, None, :] * 0.5 * fib[..., None]
    atlas = np.zeros((n, n, 4), np.float32)
    atlas[..., :3] = col
    atlas[..., 3] = alpha
    return make_image(prefix + "_albedo", atlas, "sRGB", os.path.join(MAPS, prefix + "_albedo.png"))


def build_thorn_web(bvh, poles, C, rng, cane_list):
    """A fake cobweb veil draped over the crown: a polar grid over the top, resting on the foliage and tented up by
    three arching cane tops (the poles), two-sided, RGBA silk. Real strands: fans from every pole down over the veil
    and onto the foliage, broken rings around the crown, pole-to-pole threads, threads to the spider cane tip C and a
    few loose hanging threads."""
    V = VEIL
    cx, cy, rx, ry = V["cx"], V["cy"], V["rx"], V["ry"]
    nr, ns = (5, 16) if CFG["fast"] else (7, 22)

    def surf_z(x, y):
        loc, nrm, idx, dist = bvh.ray_cast(Vector((x, y, 12.0)), DOWN)
        return loc.z if loc is not None else None

    def tent(x, y):
        z = -9.0
        for p in poles:
            z = max(z, p.z - 0.05 - 1.2 * math.hypot(x - p.x, y - p.y) ** 1.15)
        return z

    def xy(k_f, phi):
        rho = (k_f / nr) * veil_rho_max(phi)
        return cx + rx * rho * math.cos(phi), cy + ry * rho * math.sin(phi)

    G = [[None] * ns for _ in range(nr + 1)]
    lim = [[None] * ns for _ in range(nr + 1)]
    for k in range(nr + 1):
        for j in range(ns):
            x, y = xy(k, TAU * j / ns)
            fz = surf_z(x, y)
            lim[k][j] = max(fz + 0.15 if fz is not None else 0.2, tent(x, y))
            G[k][j] = Vector((x, y, lim[k][j]))
    for it in range(5):                              # smooth the valleys between the tent poles (cloth drape)
        new = [[G[k][j].z for j in range(ns)] for k in range(nr + 1)]
        for k in range(1, nr):
            for j in range(ns):
                nb = [G[k - 1][j].z, G[k + 1][j].z, G[k][(j + 1) % ns].z, G[k][(j - 1) % ns].z]
                new[k][j] = 0.5 * G[k][j].z + 0.125 * sum(nb)
        for k in range(1, nr):
            for j in range(ns):
                G[k][j].z = max(new[k][j], lim[k][j])
    for k in range(1, nr):
        for j in range(ns):
            G[k][j].z += 0.04 * noise.noise(Vector((k * 0.8, j * 0.6, 4.4)))

    def uvof(p):
        return (0.5 + 0.5 * (p.x - cx) / (rx * V["uvk"]), 0.5 + 0.5 * (p.y - cy) / (ry * V["uvk"]))

    mbs = MB()
    for side in (1, -1):
        c0 = mbs.v(G[0][0])
        ids = [[c0] * ns] + [[mbs.v(G[k][j]) for j in range(ns)] for k in range(1, nr + 1)]
        faces = []
        for j in range(ns):
            faces.append((c0, ids[1][j], ids[1][(j + 1) % ns]))          # centre fan
        for k in range(1, nr):
            for j in range(ns):
                jn = (j + 1) % ns
                faces.append((ids[k][j], ids[k + 1][j], ids[k + 1][jn], ids[k][jn]))
        for f in faces:
            pts = [mbs.V[i] for i in f]
            nz = (pts[1] - pts[0]).cross(pts[2] - pts[0]).z
            if (nz < 0) == (side > 0):
                f = tuple(reversed(f))
            mbs.f(f, 0, [uvof(mbs.V[i]) for i in f])
    silk_img = veil_texture("BushThornSilk", 256 if CFG["fast"] else 512, 9, [uvof(p) for p in poles])
    silk = mbs.obj("WebSilk", [mat_tex("BushThornSilk_Mat", silk_img, rough=0.8, alpha=True)])
    for a in list(silk.data.color_attributes):
        silk.data.color_attributes.remove(a)

    def veil_at(x, y, lift=0.035):
        dx, dy = (x - cx) / rx, (y - cy) / ry
        phi = math.atan2(dy, dx)
        rr = math.hypot(dx, dy) / veil_rho_max(phi)
        if rr >= 1.0:
            return None
        kf = rr * nr
        jf = (phi % TAU) / TAU * ns
        k0, j0 = min(nr - 1, int(kf)), int(jf) % ns
        fk, fj = kf - k0, jf - int(jf)
        j1 = (j0 + 1) % ns
        z = (G[k0][j0].z * (1 - fk) * (1 - fj) + G[k0][j1].z * (1 - fk) * fj + G[k0 + 1][j0].z * fk * (1 - fj)
             + G[k0 + 1][j1].z * fk * fj)
        return Vector((x, y, z + lift))

    def on_surface(x, y, lift=0.05):
        v = veil_at(x, y)
        if v is not None:
            return v
        z = surf_z(x, y)
        return Vector((x, y, z + lift)) if z is not None else None

    def path_xy(a, b, step=0.28):
        n = max(2, int((b - a).length / step))
        out = []
        for t in range(n + 1):
            q = on_surface(a.x + (b.x - a.x) * t / n, a.y + (b.y - a.y) * t / n)
            if q is None or (out and out[-1].z - q.z > 0.45):     # ran off the foliage / over a drop: stop
                break
            out.append(q)
        return out

    def keep_above(pts):
        out = []
        for q in pts:
            s_ = on_surface(q.x, q.y)
            out.append(q if (s_ is None or q.z > s_.z) else s_)
        return out

    mbw = MB()
    lines = []
    R = 0.04

    def anchor(x, y, lift=0.07):
        z = surf_z(x, y)
        v = veil_at(x, y, 0.0)
        if z is None:
            return None
        z = max(z, v.z if v is not None else -9.0)
        return Vector((x, y, z + lift))

    def air(a, b, sag):
        """A smooth hanging thread: the sag shrinks until the whole curve clears the veil / foliage (no kinks)."""
        n = max(8, int((b - a).length / 0.16))
        for k in range(8):
            pts = catenary(a, b, n, sag * (1 - k / 8))
            if all(on_surface(q.x, q.y) is None or q.z > on_surface(q.x, q.y).z - 0.03 for q in pts[1:-1]):
                return pts
        return catenary(a, b, n, 0.0)

    for a, b in ((poles[0], poles[1]), (poles[1], poles[2]), (poles[2], poles[0])):   # pole to pole
        lines.append((air(a, b, 0.15 + 0.05 * (a - b).length), 0.045))
    hi_pts = [max(c_["pts"], key=lambda q: q.z) for c_ in cane_list]
    for i, j in ((0, 4), (4, 1)):                    # high threads between the cane arches
        lines.append((air(hi_pts[i], hi_pts[j], 0.1 + 0.08 * (hi_pts[i] - hi_pts[j]).length), R))
    for j in (3, 1):                                 # the spider cane tip to two other arch tops (open-air spans)
        lines.append((air(C + Vector((0, 0, 0.02)), hi_pts[j], 0.12 + 0.06 * (C - hi_pts[j]).length), R))
    for pts, r in lines:
        tube(mbw, pts, [r] * len(pts), 3, 0, cap_tip=False, uv=False)
    web = mbw.obj("Web", [], uv=None)
    mn, mx = bbox_of([web])
    sz = max(mx[0] - mn[0], mx[1] - mn[1])
    lay = web.data.uv_layers.new(name="UVMap")
    data = []
    for lp in web.data.loops:
        co = web.data.vertices[lp.vertex_index].co
        data.extend(((co.x - mn[0]) / sz, (co.y - mn[1]) / sz))
    lay.data.foreach_set("uv", data)
    web.data.materials.append(mat_tex("BushThornWeb_Mat", strand_texture("BushThornWeb", 128), rough=0.55))
    for a in list(web.data.color_attributes):
        web.data.color_attributes.remove(a)
    sp = C + Vector((0, 0, -0.06))
    loc, nrm, idx, dist = bvh.ray_cast(sp + Vector((0, 0, -0.05)), DOWN)
    drop = (sp.z - loc.z) if loc is not None else sp.z
    info = {"spider_point_blender": [round(v, 3) for v in sp], "spider_point_roblox": rb(sp),
            "spider_free_drop": round(min(drop, sp.z), 3), "web_poles_roblox": [rb(p) for p in poles],
            "web_lines": len(lines)}
    return web, silk, info


# ================================================================== BUSH_AUTUMN
AU_BODY = dict(A=(2.35, 2.35, 2.05), zc=2.3, core=0.8, n_mid=14, per_mid=(2, 4), r_mid=1.05, r_small=0.56, under=0.3,
               lobes=[((-0.4, 0.5, 0.75), 0.14, 0.7), ((0.75, -0.3, 0.3), 0.09, 0.6), ((0.1, -0.9, -0.1), -0.06, 0.5)],
               disp=(0.2, 0.8, 0.05, 2.8), zflat=0.34, dims=(5.45, 5.35, 4.72), smooth=2)
AUT = [(0.0, lin((112, 8, 16))), (0.2, lin((166, 14, 16))), (0.4, lin((206, 40, 8))), (0.6, lin((226, 86, 6))),
       (0.8, lin((236, 132, 8))), (1.0, lin((240, 170, 18)))]


def autumn_cfn(rng, p, n, off, H=4.7):
    tone = 0.48 + 0.6 * fbm(p * 0.4 + off, 2) + 0.22 * (p.z / H - 0.5) + 0.05 * (p.x - p.y) + rng.gauss(0, 0.07)
    base, tip = ramp(AUT, tone - 0.14), ramp(AUT, tone + 0.1)
    lift = rng.uniform(0.95, 1.06)
    green = False

    def f(u, v):
        c = mix(base, tip, smoothstep(0.05, 0.95, v))
        if green:
            c = mix(lin((150, 150, 40)), c, smoothstep(0.1, 0.8, max(abs(u), v)))
        return kcol(c, lift)
    return f


PUMPKIN = dict(kind="pumpkin", N=9, R=0.6, Rz=0.43, depth=0.12, crest=0.5, lumps=0.025, micro=0.004, dtop=0.16,
               dtop_w=0.36, flat=0.82, flat_k=0.12, seed=71, warts=30, wz=-0.3, wr=(0.08, 0.15), wh=(0.06, 0.13),
               pal=dict(crest=(238, 112, 22), light=(252, 160, 52), groove=(170, 56, 10), top=(108, 96, 36),
                        wart=(216, 190, 118), wart2=(150, 150, 70), bottom=(236, 140, 46)))
GOURD = dict(kind="gourd", N=6, R=0.44, Rz=0.6, depth=0.06, crest=0.7, lumps=0.03, micro=0.004, dtop=0.05,
             dtop_w=0.3, flat=0.86, flat_k=0.1, seed=83, warts=55, wz=-0.7, wr=(0.07, 0.13), wh=(0.07, 0.14),
             pal=dict(crest=(250, 178, 22), light=(254, 212, 70), groove=(34, 96, 36), top=(236, 128, 22),
                      wart=(232, 214, 120), wart2=(170, 196, 70), bottom=(28, 84, 34)))


def smax(a, b, k):
    h = max(k - abs(a - b), 0.0) / k
    return max(a, b) + h * h * k * 0.25


def gourd_field(G, detail=True):
    rng = random.Random(G["seed"])
    off = Vector((rng.uniform(-50, 50), rng.uniform(-50, 50), rng.uniform(-50, 50)))
    off2 = Vector((rng.uniform(-50, 50), rng.uniform(-50, 50), rng.uniform(-50, 50)))
    N, R, Rz = G["N"], G["R"], G["Rz"]
    pl = {k: lin(v) for k, v in G["pal"].items()}
    warts = []
    while len(warts) < G["warts"]:
        d = Vector((rng.gauss(0, 1), rng.gauss(0, 1), rng.gauss(0, 1))).normalized()
        if d.z > G["wz"] and d.z < 0.85:
            warts.append((d, rng.uniform(*G["wr"]), rng.uniform(*G["wh"]), rng.random()))
    zb = -G["flat"] * Rz
    fk = G["flat_k"] * Rz

    def f(d):
        th = math.acos(max(-1.0, min(1.0, d.z)))
        ph = math.atan2(d.y, d.x)
        s = math.sin(th)
        u = N * ph / TAU
        k = math.floor(u + 0.5)
        fr = u - k
        bulge = max(0.0, math.cos(math.pi * fr)) ** G["crest"]
        m = 1.0 - G["depth"] * (s ** 0.7) * (1.0 - bulge)
        m *= 1.0 + G["lumps"] * fbm(d * 1.4 + off, 3)
        wb, wc = 0.0, 0.0
        if detail:
            m *= 1.0 + G["micro"] * fbm(d * 22.0 + off2, 2)
            for wd, wr, wh, wk in warts:
                dd = (d - wd).length_squared
                if dd < 9 * wr * wr:
                    e = math.exp(-dd / (wr * wr))
                    wb += wh * e
                    wc = max(wc, e)
        if G["kind"] == "gourd":
            prof = 1.0 - 0.36 * smoothstep(-0.2, 0.95, d.z)          # pear: narrow neck on top
        else:
            prof = 1.0
        x, y = d.x * m * R * prof, d.y * m * R * prof
        z = d.z * Rz * (1 + 0.45 * (m - 1))
        x += d.x * wb * R
        y += d.y * wb * R
        z += d.z * wb * R
        z -= G["dtop"] * Rz * math.exp(-(th / G["dtop_w"]) ** 2)
        z = smax(z, zb, fk)
        col = mix(pl["groove"], pl["crest"], bulge ** 0.6)
        sk_ = noise.noise(Vector((fr * 14.0 + k * 5.1, th * 3.3, 9.1)))
        col = mix(col, pl["light"], 0.4 * smoothstep(0.1, 0.6, sk_) * bulge)
        if G["kind"] == "gourd":
            col = mix(col, pl["bottom"], smoothstep(-0.1, -0.7, d.z) * 0.85)
            col = mix(col, pl["top"], smoothstep(0.5, 0.95, d.z) * 0.6)
        else:
            col = mix(col, pl["bottom"], 0.35 * smoothstep(2.3, 3.0, th))
            col = mix(col, pl["top"], 0.8 * math.exp(-(th / (G["dtop_w"] * 0.8)) ** 2))
        if wc > 0:
            col = mix(col, mix(pl["wart"], pl["wart2"], 0.5 + 0.5 * noise.noise(d * 9.0 + off)), 0.85 * wc)
        r = 0.42 + 0.2 * (1 - bulge) + 0.25 * wc
        return Vector((x, y, z)), col, (r, r, r)
    return f


def sphere_surface(field, useg, vseg):
    """(Copied from PumpkinEggs/eggs.py.) Own UV-sphere sampling -> (V, F, C, Rr)."""
    V, C, Rr = [], [], []

    def add(d):
        p, c, r = field(d)
        V.append(p)
        C.append(c)
        Rr.append(r)
        return len(V) - 1

    top = add(Vector((0.0, 0.0, 1.0)))
    rings = []
    for i in range(1, vseg):
        th = math.pi * i / vseg
        rings.append([add(Vector((math.sin(th) * math.cos(TAU * j / useg), math.sin(th) * math.sin(TAU * j / useg),
                                  math.cos(th)))) for j in range(useg)])
    bot = add(Vector((0.0, 0.0, -1.0)))
    F = []
    for j in range(useg):
        F.append((top, rings[0][j], rings[0][(j + 1) % useg]))
    for a, b in zip(rings[:-1], rings[1:]):
        for j in range(useg):
            jn = (j + 1) % useg
            F.append((a[j], b[j], b[jn], a[jn]))
    for j in range(useg):
        F.append((bot, rings[-1][(j + 1) % useg], rings[-1][j]))
    return V, F, C, Rr


def gnarly_stem(L, r0, seed, base, detail, az=None):
    """(Adapted from PumpkinEggs/eggs.py gnarly_stem.) A bent, twisted, knotted stem with 5 spiralling ridges, a flared
    foot and a dry broken top."""
    sp = {k: lin(v) for k, v in dict(base=(66, 86, 34), mid=(108, 100, 52), top=(148, 126, 80), hi=(196, 180, 124),
                                     lo=(48, 44, 22), cap=(206, 184, 130)).items()}
    rng = random.Random(seed)
    off = Vector((rng.uniform(-40, 40), rng.uniform(-40, 40), rng.uniform(-40, 40)))
    az = rng.uniform(0, TAU) if az is None else az
    lean, wob, tw = rng.uniform(0.3, 0.45), rng.uniform(0.05, 0.09), rng.uniform(0.8, 1.6)
    ld = Vector((math.cos(az), math.sin(az), 0.0))
    sd = Vector((-math.sin(az), math.cos(az), 0.0))
    base = Vector(base)

    def path(t):
        return base + ld * (lean * L * t * t) + sd * (wob * L * math.sin(2.4 * math.pi * t)) + Vector((0, 0, L * t))

    ts, m = ([i / 60 for i in range(61)], 32) if detail else ([0.0, 0.08, 0.2, 0.4, 0.6, 0.8, 1.0], 6)
    V, C, Rr, F, rings = [], [], [], [], []
    for t in ts:
        c = path(t)
        T = (path(min(1.0, t + 0.01)) - path(max(0.0, t - 0.01))).normalized()
        Nn = Vector((0, 1, 0)).cross(T).normalized()
        B = T.cross(Nn)
        r = r0 * (1 + 0.95 * math.exp(-(t / 0.11) ** 2)) * (1 - 0.25 * t)
        amp = 0.2 + 0.2 * math.exp(-(t / 0.12) ** 2)
        bc = mix(mix(sp["base"], sp["mid"], smoothstep(0.05, 0.6, t)), sp["top"], smoothstep(0.55, 1.0, t))
        ring = []
        for j in range(m):
            a = TAU * j / m
            ridge = (0.5 + 0.5 * math.cos(5 * a + tw * t * 2.2)) ** 0.6
            grain = noise.noise(Vector((math.cos(a) * 3, math.sin(a) * 3, t * 30)) + off) if detail else 0.0
            V.append(c + (Nn * math.cos(a) + B * math.sin(a)) * r * (1 - amp + amp * ridge) * (1 + 0.035 * grain))
            col = mix(bc, mix(bc, sp["hi"], 0.5), 0.45 * ridge)
            C.append(mix(col, sp["lo"], 0.35 * (1 - ridge) + 0.2 * max(0.0, grain)))
            Rr.append((0.8, 0.8, 0.8))
            ring.append(len(V) - 1)
        rings.append(ring)
    for i in range(len(rings) - 1):
        for j in range(m):
            jn = (j + 1) % m
            F.append((rings[i][j], rings[i][jn], rings[i + 1][jn], rings[i + 1][j]))
    T1 = (path(1.0) - path(0.98)).normalized()
    V.append(path(1.0) - T1 * r0 * 0.3)
    C.append(sp["cap"])
    Rr.append((0.85, 0.85, 0.85))
    vt = len(V) - 1
    for j in range(m):
        F.append((rings[-1][j], rings[-1][(j + 1) % m], vt))
    V.append(path(0.0) - Vector((0, 0, r0 * 0.6)))
    C.append(sp["base"])
    Rr.append((0.8, 0.8, 0.8))
    vb = len(V) - 1
    for j in range(m):
        F.append((rings[0][(j + 1) % m], rings[0][j], vb))
    return V, F, C, Rr


def mb_add(mb, V, F, C, Rr, mat, M=None):
    base = len(mb.V)
    for p, c, r in zip(V, C, Rr):
        mb.v(M @ p if M else p, c, r[0])
    for f in F:
        mb.f([base + i for i in f], mat)


def stem_col(t, a):
    return mix(lin((88, 70, 56)), lin((120, 100, 82)), 0.5 + 0.5 * math.cos(5 * a + t * 9))


def build_autumn():
    fast = CFG["fast"]
    size = 256 if fast else 1024
    fresh(8)
    rng = random.Random(2203)
    nrng = np.random.default_rng(2203)
    off = Vector((7.7, 1.3, 2.9))
    m_body = mat_vc("AutBodyHi")
    m_leaf = mat_leaf("AutLeafHi", vein_light=0.18, edge_dark=0.45, bump=0.55, freq=6.0, edge_col=lin((140, 14, 10)))
    m_wood = mat_vc("AutWoodHi")
    m_gourd = mat_vc("GourdHi")

    def body_col(p, n):
        t = 0.5 + 0.5 * fbm(p * 0.7 + off, 2)
        return mix(lin((66, 14, 10)), lin((100, 36, 12)), t), 0.85

    hi = clump_body("AutBody_hi", AU_BODY, 29, 0.1 if fast else 0.055, m_body, body_col)
    log("autumn body hi", tris_of(hi))
    body_lo = decimate_to(hi, "AutBody_lo", 3100, inflate=0.1)
    smart_uv(body_lo)
    bvh, bvh_bm = bvh_of([body_lo])
    MAT_BODY, MAT_TOP, MAT_BOT, MAT_WOOD = 0, 1, 2, 3
    mbh_w, mbh_l, mbh_p, mbl = MB(), MB(), MB(), MB()
    mbl.add_object_mesh(body_lo, MAT_BODY)
    # ---------------------------------------------------------------- woody stems under the canopy
    for k in range(6):
        az = 60 * k + rng.uniform(-14, 14)
        p0 = cyl(rng.uniform(0.05, 0.3), az, -0.12)
        p3 = cyl(rng.uniform(1.0, 1.6), az + rng.uniform(-25, 25), rng.uniform(1.6, 2.2))
        p1 = p0 + Vector((0, 0, 0.5)) + (p3 - p0) * Vector((0.15, 0.15, 0))
        p2 = p0.lerp(p3, 0.65) + Vector((0, 0, -0.15))
        pts = resample([bez(p0, p1, p2, p3, i / 100) for i in range(101)], 0.05)
        n = len(pts)
        radii = [0.13 - 0.06 * (i / (n - 1)) for i in range(n)]
        o = Vector((k * 3.1, 1.0, 2.0))
        tube(mbh_w, pts, radii, 10, 0, cfn=stem_col,
             rfn=lambda t, a, o=o: 1 + 0.07 * math.cos(6 * a + 3 * noise.noise(o + Vector((t * 9, 0, 0)))), rough=0.85,
             cap_tip=True, uv=False)
        out = [not inside(bvh, p) for p in pts]
        idx = [i for i, ok in enumerate(out) if ok]
        if idx:
            i1 = min(n - 1, idx[-1] + 6)
            sub = pts[:i1 + 1]
            lo_pts = resample(sub, 0.25)
            tube(mbl, lo_pts, interp_radii(sub, radii[:i1 + 1], lo_pts), 5, MAT_WOOD, cap_tip=False, t1=i1 / (n - 1))
    # ---------------------------------------------------------------- clump leaves (bake source)
    P_s, N_s, area = surface_samples(hi, int(31 * 100 * (0.35 if fast else 1.0)), nrng)
    nleaf = 0
    for p, n in zip(P_s, N_s):
        if p.z < AU_BODY["zflat"] + 0.06:
            continue
        L = rng.uniform(0.36, 0.56)
        P = dict(L=L, W=L * rng.uniform(0.24, 0.3), cup=rng.uniform(0.2, 0.45), bend=rng.uniform(0.1, 0.34),
                 twist=rng.uniform(-0.45, 0.45), kind="ovate" if rng.random() < 0.7 else "lance")
        fr = leaf_frame(n, tangent_dir(n, rng), math.radians(rng.uniform(8, 36)), rng.uniform(-0.45, 0.45))
        leaf_hi(mbh_l, p + n * rng.uniform(-0.05, 0.1), fr, P, autumn_cfn(rng, p, n, off), 0.82, 0, nu=5,
                nv=5 if fast else 7)
        nleaf += 1
    log("autumn hi leaves", nleaf, "area", round(area, 1))
    # ---------------------------------------------------------------- protruding leaves
    P_l, N_l, _ = surface_samples(body_lo, 2400, nrng)
    cands = [(p, n) for p, n in zip(P_l, N_l) if n.z > -0.4 and p.z > 0.6]
    prot = dart(cands, 0.36, 143)
    for p, n in prot:
        L = rng.uniform(0.5, 0.72)
        P = dict(L=L, W=L * rng.uniform(0.25, 0.3), cup=rng.uniform(0.25, 0.4), bend=rng.uniform(0.18, 0.4),
                 twist=rng.uniform(-0.4, 0.4), kind="ovate" if rng.random() < 0.7 else "lance")
        tilt = rng.uniform(14, 36) if rng.random() < 0.6 else rng.uniform(36, 58)
        fr = leaf_frame(n, tangent_dir(n, rng, 0.6), math.radians(tilt), rng.uniform(-0.4, 0.4))
        B = p - n * 0.07
        leaf_lo(mbl, B, fr, P, MAT_TOP, MAT_BOT)
        leaf_hi(mbh_p, B, fr, P, autumn_cfn(rng, p, n, off), 0.82, 0, nu=5, nv=7)
    # fallen leaves on the soil (not under the gourds)
    nf = 0
    for k in range(40):
        if nf >= 8:
            break
        az = rng.uniform(0, 360)
        if 215 < az < 325:
            continue
        p = cyl(rng.uniform(2.3, 3.05), az, 0.0)
        if inside(bvh, p + Vector((0, 0, 0.35))):
            continue
        L = rng.uniform(0.5, 0.65)
        P = dict(L=L, W=L * 0.28, cup=0.0, bend=-0.12, curl=rng.uniform(0.4, 0.8), twist=rng.uniform(-0.3, 0.3),
                 kind="ovate")
        fr = leaf_frame(UP, cyl(1.0, rng.uniform(0, 360), 0.0), 0.0)
        B = p + Vector((0, 0, 0.03))
        leaf_lo(mbl, B, fr, P, MAT_TOP, MAT_BOT, thick=0.02)
        cf = autumn_cfn(rng, p + Vector((0, 0, 1.0)), UP, off)
        leaf_hi(mbh_p, B, fr, P, lambda u, v, cf=cf: kcol(cf(u, v), 0.85), 0.82, 0, nu=5, nv=7)
        nf += 1
    log("autumn protruding leaves", len(prot), "fallen", nf)
    wood_hi = mbh_w.obj("AutWood_hi", [m_wood], uv=None)
    leaves_hi = mbh_l.obj("AutLeaves_hi", [m_leaf], uv="LeafUV")
    prot_hi = mbh_p.obj("AutProt_hi", [m_leaf], uv="LeafUV")
    bush = mbl.obj("Bush", placeholder_mats(["Body", "LeafTop", "LeafBot", "Wood"]))
    # ---------------------------------------------------------------- the two warty gourds (own part + texture)
    mg_h, mg_l = MB(), MB()
    gdefs = [(PUMPKIN, cyl(2.55, 243, 0.0), rng.uniform(0, 360), 0.0, 0.34, 0.08, 13),
             (GOURD, cyl(2.62, 291, 0.0), rng.uniform(0, 360), 24.0, 0.24, 0.055, 19)]
    gourd_tops = []
    for G, pos, yaw, tilt, sL, sr, sseed in gdefs:
        Rm = (Matrix.Rotation(math.radians(yaw), 4, "Z") @ Matrix.Rotation(math.radians(tilt), 4, "Y"))
        fh, fl = gourd_field(G, True), gourd_field(G, False)
        hu, hv = (64, 40) if fast else (200, 128)
        lu, lv = (32, 14) if G["kind"] == "pumpkin" else (20, 14)
        Vh, Fh, Ch, Rh = sphere_surface(fh, hu, hv)
        Vl, Fl, Cl, Rl = sphere_surface(fl, lu, lv)
        top = fl(Vector((0, 0, 1)))[0]
        Vs, Fs, Cs, Rs = gnarly_stem(sL, sr, sseed, (0, 0, top.z - 0.03), True)
        Vsl, Fsl, Csl, Rsl = gnarly_stem(sL, sr, sseed, (0, 0, top.z - 0.03), False)
        zmin = min((Rm @ v).z for v in Vl)
        az = math.atan2(pos.y, pos.x)
        r_ok = 3.4
        for k in range(40):                          # tuck it in: the innermost spot with <= 4% of it inside
            r = 3.4 - 0.05 * k
            Mt = Matrix.Translation(Vector((r * math.cos(az), r * math.sin(az), -zmin - 0.03))) @ Rm
            inside_n = sum(1 for v in Vl[::3] if inside(bvh, Mt @ v))
            if inside_n > 0.04 * len(Vl[::3]):
                break
            r_ok = r
        pos = Vector((r_ok * math.cos(az), r_ok * math.sin(az), 0.0))
        M = Matrix.Translation(pos + Vector((0, 0, -zmin - 0.03))) @ Rm
        mb_add(mg_h, Vh, Fh, Ch, Rh, 0, M)
        mb_add(mg_h, Vs, Fs, Cs, Rs, 0, M)
        mb_add(mg_l, Vl, Fl, Cl, Rl, 0, M)
        mb_add(mg_l, Vsl, Fsl, Csl, Rsl, 0, M)
        gourd_tops.append(M @ Vector((0, 0, top.z)))
    gourd_hi = mg_h.obj("Gourds_hi", [m_gourd], uv=None)
    gourds = mg_l.obj("Gourds", [mat_flat("_G", (0.5, 0.5, 0.5))], uv=None)
    tri = gourds.modifiers.new("T", "TRIANGULATE")
    apply_mods(gourds)
    smart_uv(gourds, angle=60)
    log("autumn game mesh by material", tris_by_mat(bush))
    log("autumn game mesh tris", tris_of(bush), "gourds", tris_of(gourds), "hi:", tris_of(leaves_hi),
        tris_of(prot_hi), tris_of(wood_hi), tris_of(gourd_hi))
    hide(body_lo)
    pack_uvs(bush, {MAT_TOP: 1.25, MAT_WOOD: 1.0}, mbl.skipf)
    copy_uvs(bush, mbl.copies)
    bush.hide_render = True
    gourds.hide_render = True
    groups = []
    for nm, keep, his, cage, maxray in (("G_Body", (MAT_BODY,), [hi, leaves_hi, wood_hi], 0.36, 0.7),
                                        ("G_Leaf", (MAT_TOP,), [prot_hi], 0.03, 0.08),
                                        ("G_Wood", (MAT_WOOD,), [wood_hi], 0.05, 0.12)):
        groups.append((split_mats(bush, nm, keep), his, cage, maxray))
    imgs = bake_groups(groups, size, "BushAutumn", ao_strength=0.55, ao_dist=0.7, ao_tint=(0.4, 0.07, 0.02))
    for g in groups:
        bpy.data.objects.remove(g[0])
    gl = split_mats(gourds, "G_Gourds", (0,))
    gimgs = bake_groups([(gl, [gourd_hi], 0.12, 0.26)], 256 if fast else 512, "BushAutumnGourds", ao_strength=0.5,
                        ao_dist=0.5)
    bpy.data.objects.remove(gl)
    finish_lo(bush, "BushAutumn", imgs)
    finish_lo(gourds, "BushAutumnGourds", gimgs)
    hide(hi, leaves_hi, prot_hi, wood_hi, gourd_hi)
    rep = {"tris": {o.name: tris_of(o) for o in (bush, gourds)}, "texture": {"Bush": size, "Gourds": 512},
           "bake": imgs["stats"], "bake_gourds": gimgs["stats"], "atlas_coverage": imgs["coverage"],
           "hi_leaves": nleaf, "protruding_leaves": len(prot), "fallen_leaves": nf,
           "gourd_stem_tops_roblox": [rb(p) for p in gourd_tops]}
    mn, mx = bbox_of([bush, gourds])
    rep["bbox_blender"] = [[round(float(v), 3) for v in mn], [round(float(v), 3) for v in mx]]
    rep["size_roblox_XYZ"] = [round(float(mx[0] - mn[0]), 3), round(float(mx[2] - mn[2]), 3),
                              round(float(mx[1] - mn[1]), 3)]
    bvh_bm.free()
    finish("autumn", rep)
    return rep


# ================================================================== BRAMBLE (dead shrub)
BR_TWIG = dict(base=lin((98, 84, 72)), mid=lin((128, 112, 96)), tip=lin((160, 146, 128)), groove=lin((44, 36, 30)),
               lichen=lin((150, 166, 118)), young=lin((128, 74, 52)))
BR_LEAF = [lin((156, 72, 30)), lin((120, 74, 42)), lin((186, 132, 56)), lin((140, 52, 26)), lin((108, 60, 34))]


def twig_rot(d, rng, lo, hi):
    ax = Quaternion(d, rng.uniform(0, TAU)) @ d.orthogonal().normalized()
    return (Quaternion(ax, math.radians(rng.uniform(lo, hi))) @ d).normalized()


def grow_bramble(rng):
    br = []
    ENV = Vector((2.05, 2.05, 3.05))

    def grow(p0, d0, L, r0, r1, depth, node):
        pts, d, s = [p0.copy()], d0.normalized(), 0.0
        nxt = rng.uniform(0.5, 1.0) * node
        step = 0.045
        bend_ax = d.orthogonal().normalized()
        bend_ax = Quaternion(d, rng.uniform(0, TAU)) @ bend_ax
        bend = math.radians(rng.uniform(0.4, 1.6)) if depth else 0.0     # twigs curl (tangle)
        while s < L:
            s += step
            if s >= nxt:
                d = twig_rot(d, rng, 16, 38 if depth else 22)
                nxt += rng.uniform(0.7, 1.25) * node
            if bend:
                d = (Quaternion(bend_ax, bend) @ d).normalized()
            q = pts[-1]
            e = Vector((q.x / ENV.x, q.y / ENV.y, (q.z - 0.2) / ENV.z))
            if e.length > 0.9:                               # steer back into the envelope (tangle inward)
                d = (d - e.normalized() * 0.12).normalized()
            if depth == 0:
                d = (d + UP * 0.02).normalized()
            if q.z < 0.25 and d.z < 0.2:
                d = (d + UP * 0.15).normalized()
            nq = q + d * step
            if depth and nq.z < 0.08:
                nq.z = 0.08
            pts.append(nq)
        n = len(pts)
        radii = [max(0.04, r0 + (r1 - r0) * (i / (n - 1)) ** 0.85) for i in range(n)]
        br.append(dict(pts=pts, radii=radii, depth=depth))
        if depth < 3:
            nk = (rng.randint(3, 4) if depth == 0 else rng.randint(1, 3)) if depth < 2 else rng.randint(0, 2)
            for _ in range(nk):
                t = rng.uniform(0.3, 0.88)
                i = max(1, min(n - 2, int(t * (n - 1))))
                pd = (pts[i + 1] - pts[i - 1]).normalized()
                cd = twig_rot(pd, rng, 30, 72)
                grow(pts[i], cd, L * rng.uniform(0.48, 0.7), radii[i] * 0.78, max(0.04, radii[i] * 0.45),
                     depth + 1, node * 0.72)

    nmain = 6
    for k in range(nmain):
        az = 360.0 * k / nmain + rng.uniform(-18, 18)
        el = math.radians(rng.uniform(38, 66))
        d = Vector((math.cos(math.radians(az)) * math.cos(el), math.sin(math.radians(az)) * math.cos(el), math.sin(el)))
        p0 = cyl(rng.uniform(0.0, 0.12), az, -0.1)
        grow(p0, d, rng.uniform(1.9, 2.6), 0.088, 0.05, 0, 0.4)
    return br


def pick_bramble(seed0, tries=14):
    """Grow a few shrubs, keep the one whose footprint is most centred on the root crown (the FBX origin)."""
    best = None
    for k in range(tries):
        rng = random.Random(seed0 + k)
        br = grow_bramble(rng)
        allp = [p for b in br for p in b["pts"]]
        xs, ys = [p.x for p in allp], [p.y for p in allp]
        off = math.hypot((max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2)
        asp = abs((max(xs) - min(xs)) - (max(ys) - min(ys)))
        score = off + 0.3 * asp
        if best is None or score < best[0]:
            best = (score, seed0 + k, br)
    log("bramble seed", best[1], "centring score", round(best[0], 3))
    return random.Random(best[1] + 1000), best[2]


def twig_cfn(o, depth):
    C = BR_TWIG

    def f(t, a):
        c = mix(C["base"], C["mid"], smoothstep(0.0, 0.6, t))
        c = mix(c, C["tip"], smoothstep(0.6, 1.0, t) * (0.25 + 0.1 * depth))
        if depth >= 2:
            c = mix(c, C["young"], 0.25 * (0.5 + 0.5 * noise.noise(o + Vector((t * 3, 0, 0)))))
        g = 0.5 + 0.5 * math.cos(5 * a + 2.0 * noise.noise(o + Vector((t * 10, a, 0))))
        c = mix(c, C["groove"], 0.6 * (1 - g) ** 1.5)
        lk = noise.noise(Vector((math.cos(a) * 2.0, math.sin(a) * 2.0, t * 9.0)) + o * 1.7)
        c = mix(c, C["lichen"], 0.55 * smoothstep(0.32, 0.55, lk) * (1 if depth < 2 else 0.4))
        return c
    return f


def twig_rfn(o):
    def f(t, a):
        g = 0.5 + 0.5 * math.cos(5 * a + 2.0 * noise.noise(o + Vector((t * 10, a, 0))))
        return (1 - 0.1 + 0.1 * g) * (1 + 0.04 * noise.noise(Vector((math.cos(a) * 3, math.sin(a) * 3, t * 30)) + o))
    return f


def dead_leaf_cfn(rng):
    a, b = rng.choice(BR_LEAF), rng.choice(BR_LEAF)
    sp = rng.random() < 0.6
    o = Vector((rng.uniform(-30, 30), rng.uniform(-30, 30), 0))

    def f(u, v):
        c = mix(a, b, smoothstep(0.2, 1.0, max(abs(u), v)))
        if sp:
            c = mix(c, lin((70, 44, 26)), 0.6 * smoothstep(0.35, 0.6, noise.noise(Vector((u * 2.2, v * 3.5, 0)) + o)))
        return c
    return f


def build_bramble():
    fast = CFG["fast"]
    size = 256 if fast else 512
    fresh(8)
    m_wood = mat_vc("BrWoodHi")
    m_leaf = mat_leaf("BrLeafHi", vein_light=0.35, edge_dark=0.35, bump=0.7, freq=5.0)
    rng, br = pick_bramble(4409)
    allp = [p for b in br for p in b["pts"]]
    xs, ys, zs = [p.x for p in allp], [p.y for p in allp], [p.z for p in allp]
    sx = 3.75 / (max(xs) - min(xs))
    sy = 3.75 / (max(ys) - min(ys))
    sz = 2.88 / max(zs)
    cx, cy = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
    for b in br:
        b["pts"] = [Vector((p.x * sx, p.y * sy, p.z * sz if p.z > 0 else p.z)) for p in b["pts"]]
    MAT_WOOD, MAT_TOP, MAT_BOT = 0, 1, 2
    mbh_w, mbh_l, mbl = MB(), MB(), MB()
    sides_lo = {0: 6, 1: 5, 2: 4, 3: 3}
    step_lo = {0: 0.26, 1: 0.24, 2: 0.22, 3: 0.2}
    for k, b in enumerate(br):
        o = Vector((k * 1.37, k * 0.71, 3.3))
        cf, rf = twig_cfn(o, b["depth"]), twig_rfn(o)
        tube(mbh_w, b["pts"], b["radii"], (6 if fast else 10) if b["depth"] < 2 else (5 if fast else 8), 0, cfn=cf,
             rfn=rf, rough=0.85, cap_tip=True, tipk=2.5, uv=False)
        lo_pts = resample(b["pts"], step_lo[b["depth"]])
        tube(mbl, lo_pts, interp_radii(b["pts"], b["radii"], lo_pts), sides_lo[b["depth"]], MAT_WOOD, cap_tip=True,
             tipk=2.5)
    # dead leaves: most hang from twig tips, a few caught in forks
    tips = [b for b in br if b["depth"] >= 2]
    rng.shuffle(tips)
    nleaf = 0
    for b in tips[:9]:
        tp = b["pts"][-1]
        stalk_end = tp + Vector((rng.uniform(-0.03, 0.03), rng.uniform(-0.03, 0.03), -0.1))
        for mb_, sides in ((mbh_w, 5), (mbl, 3)):
            tube(mb_, [tp, stalk_end], [0.022, 0.018], sides, 0 if mb_ is mbh_w else MAT_WOOD,
                 cfn=lambda t, a: lin((96, 70, 44)), rough=0.8, cap_tip=False, uv=(mb_ is mbl))
        L = rng.uniform(0.48, 0.62)
        P = dict(L=L, W=L * rng.uniform(0.26, 0.32), cup=0.1, bend=rng.uniform(-0.15, 0.2), curl=rng.uniform(0.6, 1.1),
                 twist=rng.uniform(-0.9, 0.9), crinkle=0.18, seed=rng.uniform(0, 50), kind="ovate")
        t = (DOWN + Vector((rng.uniform(-0.35, 0.35), rng.uniform(-0.35, 0.35), 0))).normalized()
        nrm = Vector((rng.uniform(-1, 1), rng.uniform(-1, 1), 0)).normalized()
        fr = leaf_frame(nrm, t, 0.0, 0.0)
        leaf_lo(mbl, stalk_end, fr, P, MAT_TOP, MAT_BOT, thick=0.022)
        leaf_hi(mbh_l, stalk_end, fr, P, dead_leaf_cfn(rng), 0.75, 0, nu=5, nv=7)
        nleaf += 1
    forks = [b for b in br if b["depth"] in (1, 2)]
    rng.shuffle(forks)
    for b in forks[:4]:
        p = b["pts"][0] + Vector((0, 0, 0.06))
        L = rng.uniform(0.45, 0.58)
        P = dict(L=L, W=L * 0.3, cup=0.15, bend=-0.1, curl=rng.uniform(0.6, 1.0), twist=rng.uniform(-0.5, 0.5),
                 crinkle=0.2, seed=rng.uniform(0, 50), kind="ovate")
        fr = leaf_frame(UP, cyl(1.0, rng.uniform(0, 360), 0.0), math.radians(rng.uniform(-10, 15)))
        leaf_lo(mbl, p, fr, P, MAT_TOP, MAT_BOT, thick=0.022)
        leaf_hi(mbh_l, p, fr, P, dead_leaf_cfn(rng), 0.75, 0, nu=5, nv=7)
        nleaf += 1
    wood_hi = mbh_w.obj("BrWood_hi", [m_wood], uv=None)
    leaves_hi = mbh_l.obj("BrLeaves_hi", [m_leaf], uv="LeafUV")
    lo = mbl.obj("Bramble", placeholder_mats(["Wood", "LeafTop", "LeafBot"]))
    log("bramble branches", len(br), "game tris", tris_of(lo), "hi", tris_of(wood_hi), tris_of(leaves_hi))
    pack_uvs(lo, {MAT_TOP: 1.3}, mbl.skipf, margin=0.004)
    copy_uvs(lo, mbl.copies)
    lo.hide_render = True
    groups = [(split_mats(lo, "G_Wood", (MAT_WOOD,)), [wood_hi], 0.035, 0.09),
              (split_mats(lo, "G_Leaf", (MAT_TOP,)), [leaves_hi], 0.03, 0.08)]
    imgs = bake_groups(groups, size, "Bramble", ao_strength=0.5, ao_dist=0.4)
    for g in groups:
        bpy.data.objects.remove(g[0])
    finish_lo(lo, "Bramble", imgs)
    hide(wood_hi, leaves_hi)
    rep = {"tris": {lo.name: tris_of(lo)}, "texture": size, "bake": imgs["stats"], "atlas_coverage": imgs["coverage"],
           "branches": len(br), "dead_leaves": nleaf}
    mn, mx = bbox_of([lo])
    rep["bbox_blender"] = [[round(float(v), 3) for v in mn], [round(float(v), 3) for v in mx]]
    rep["size_roblox_XYZ"] = [round(float(mx[0] - mn[0]), 3), round(float(mx[2] - mn[2]), 3),
                              round(float(mx[1] - mn[1]), 3)]
    finish("bramble", rep)
    return rep


# ================================================================== save / preview / render / export
ASSETS = {"thorn": ("Halloween_Bush_Thorn", ["Bush", "Web", "WebSilk"]),
          "autumn": ("Halloween_Bush_Autumn", ["Bush", "Gourds"]),
          "bramble": ("Halloween_Bramble", ["Bramble"])}


def blend_path(key):
    return os.path.join(OUT, key + ("_fast" if CFG["fast"] else "") + ".blend")


def finish(key, rep):
    bpy.ops.wm.save_as_mainfile(filepath=blend_path(key))
    with open(os.path.join(OUT, key + ("_fast" if CFG["fast"] else "") + "_report.json"), "w") as fh:
        json.dump(rep, fh, indent=1)
    log(key, "done", json.dumps(rep))


def preview(key, tag="p"):
    bpy.ops.wm.open_mainfile(filepath=blend_path(key))
    review_scene()
    ground_set()
    t = Vector((0, 0, 2.0 if key != "bramble" else 1.3))
    pre = os.path.join(WIP, "%s_%s" % (key, tag))
    out = [shoot_fov(pre + "_25.png", t + Vector((0.42, -1, 0.33)).normalized() * 25, t, vfov=70),
           shoot_fov(pre + "_12.png", t + Vector((0.42, -1, 0.42)).normalized() * 12, t, vfov=70),
           shoot_fov(pre + "_close.png", t + Vector((0.3, -1, 0.3)).normalized() * 11, t, lens=50),
           shoot_fov(pre + "_back.png", t + Vector((-0.6, 1, 0.5)).normalized() * 13, t, lens=50)]
    return out


def load_objs(key, names, dx):
    path = blend_path(key)
    with bpy.data.libraries.load(path, link=False) as (src, dst):
        dst.objects = [n for n in src.objects if n in names]
    objs = []
    for o in dst.objects:
        link(o)
        o.location.x += dx
        o.hide_render = False
        o.hide_viewport = False
        objs.append(o)
    return objs


def render_all():
    fresh(8)
    review_scene()
    xs = {"thorn": -8.5, "autumn": 0.0, "bramble": 8.0}
    for key, dx in xs.items():
        load_objs(key, ASSETS[key][1], dx)
    ground_set(beds=[(x, 0.0) for x in xs.values()])
    out = []
    t = Vector((0, 0, 2.2))
    out.append(shoot_fov(os.path.join(OUT, "review_lineup_25.png"), t + Vector((0.12, -1, 0.42)).normalized() * 25, t,
                         vfov=70))
    out.append(shoot_fov(os.path.join(OUT, "review_lineup_50.png"), t + Vector((0.2, -1, 0.5)).normalized() * 50, t,
                         vfov=70))
    for key, dx in xs.items():
        tk = Vector((dx, 0, 2.2 if key != "bramble" else 1.35))
        d = Vector((0.35, -1, 0.32)).normalized()
        out.append(shoot_fov(os.path.join(OUT, "review_%s_close.png" % key), tk + d * (11 if key != "bramble" else 8),
                             tk, lens=50))
    tb = Vector((xs["thorn"], 0, 2.4))
    out.append(shoot_fov(os.path.join(OUT, "review_thorn_back34.png"), tb + Vector((-0.8, 1, 0.55)).normalized() * 13,
                         tb, lens=50))
    return out


def export_all():
    rep = {}
    for key, (fname, names) in ASSETS.items():
        bpy.ops.wm.open_mainfile(filepath=blend_path(key))
        objs = [bpy.data.objects[n] for n in names]
        for o in objs:
            assert tuple(o.location) == (0.0, 0.0, 0.0), o.name
        rep[key] = export_fbx(objs, os.path.join(CDIMP, fname + ".fbx"))
        rep[key]["tris"] = {o.name: tris_of(o) for o in objs}
        log("exported", rep[key])
    return rep


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    if argv and argv[0] == "fast":
        CFG["fast"] = True
        argv = argv[1:]
    rep = {}
    i = 0
    while i < len(argv):
        st = argv[i]
        if st == "thorn":
            rep["thorn"] = build_thorn()
        elif st == "autumn":
            rep["autumn"] = build_autumn()
        elif st == "bramble":
            rep["bramble"] = build_bramble()
        elif st == "preview":
            i += 1
            rep["preview"] = preview(argv[i])
        elif st == "render":
            rep["render"] = render_all()
        elif st == "export":
            rep["export"] = export_all()
        i += 1
    print("BUSH_REPORT " + json.dumps(rep))
