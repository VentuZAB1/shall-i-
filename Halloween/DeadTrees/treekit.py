# SLINGSHOT Halloween garden - DeadTrees builder kit (2026-10-12).
# Recursive crooked branch skeleton -> HI: trunk/roots/limbs as ONE signed-distance field (smooth unions = seamless
# forks + root buttresses, bark furrows carved into the field along each branch's own axis/twist, knots, hollows, a
# carved face) meshed with OpenVDB (convertToQuads), thin branches + twigs as swept bark tubes, per-vertex colour +
# roughness -> GAME: the same SDF without furrows at a coarse voxel size, decimated; thin branches as 4-7 sided tubes
# with strip UVs -> Cycles bakes (normal, colour x AO, roughness) via hkit.bake_set. Webs = tube strands + RGBA silk.
# Units: 1 Blender m = 1 stud, +Z up, Blender +Y = Roblox -Z. Origin = trunk base on the ground.
import sys, os, math, random, json, time
sys.path.insert(0, r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween")
from hkit import *  # noqa  (read-only kit)
import bpy, bmesh
import numpy as np
from mathutils import Vector, Matrix, noise
from mathutils.bvhtree import BVHTree

OUT = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween\DeadTrees"
MAPS = os.path.join(OUT, "maps")
WIP = os.path.join(OUT, "wip")
for _d in (MAPS, WIP):
    os.makedirs(_d, exist_ok=True)
T0 = time.time()


def log(*a):
    print("[%7.1f] " % (time.time() - T0) + " ".join(str(x) for x in a), flush=True)


def V(a):
    return Vector((float(a[0]), float(a[1]), float(a[2])))


def sm(a, b, x):
    t = np.clip((x - a) / (b - a), 0.0, 1.0)
    return t * t * (3 - 2 * t)


# ================================================================== numpy Perlin noise
class PN:
    G = np.array([[1, 1, 0], [-1, 1, 0], [1, -1, 0], [-1, -1, 0], [1, 0, 1], [-1, 0, 1], [1, 0, -1], [-1, 0, -1],
                  [0, 1, 1], [0, -1, 1], [0, 1, -1], [0, -1, -1], [1, 1, 0], [0, -1, 1], [-1, 1, 0], [0, -1, -1]],
                 np.float32)

    def __init__(self, seed):
        p = np.random.default_rng(seed).permutation(256).astype(np.int32)
        self.p = np.concatenate([p, p])

    def __call__(self, x, y, z):
        x = np.asarray(x, np.float32)
        y = np.asarray(y, np.float32)
        z = np.asarray(z, np.float32)
        X, Y, Z = np.floor(x), np.floor(y), np.floor(z)
        xf, yf, zf = x - X, y - Y, z - Z
        X = X.astype(np.int32) & 255
        Y = Y.astype(np.int32) & 255
        Z = Z.astype(np.int32) & 255
        u = xf * xf * xf * (xf * (xf * 6 - 15) + 10)
        v = yf * yf * yf * (yf * (yf * 6 - 15) + 10)
        w = zf * zf * zf * (zf * (zf * 6 - 15) + 10)
        p, G = self.p, self.G
        A = p[X] + Y
        AA, AB = p[A] + Z, p[A + 1] + Z
        B = p[X + 1] + Y
        BA, BB = p[B] + Z, p[B + 1] + Z

        def gr(hh, a, b, c):
            g = G[p[hh] & 15]
            return g[..., 0] * a + g[..., 1] * b + g[..., 2] * c

        def lp(t, a, b):
            return a + t * (b - a)

        y1 = lp(v, lp(u, gr(AA, xf, yf, zf), gr(BA, xf - 1, yf, zf)),
                lp(u, gr(AB, xf, yf - 1, zf), gr(BB, xf - 1, yf - 1, zf)))
        y2 = lp(v, lp(u, gr(AA + 1, xf, yf, zf - 1), gr(BA + 1, xf - 1, yf, zf - 1)),
                lp(u, gr(AB + 1, xf, yf - 1, zf - 1), gr(BB + 1, xf - 1, yf - 1, zf - 1)))
        return lp(w, y1, y2)

    def fbm(self, x, y, z, octaves=3, lac=2.03, gain=0.5):
        s = 0.0
        a, f = 1.0, 1.0
        for o in range(octaves):
            s = s + a * self(x * f + 13.1 * o, y * f + 7.7 * o, z * f + 3.3 * o)
            a *= gain
            f *= lac
        return s


PNZ = PN(1234)


# ================================================================== SDF helpers
def smin(a, b, k):
    if k <= 0:
        return np.minimum(a, b)
    h = np.clip(0.5 + 0.5 * (b - a) / k, 0.0, 1.0)
    return b + (a - b) * h - k * h * (1 - h)


def smax(a, b, k):
    return -smin(-a, -b, k)


def frame_from(n):
    """3x3 matrix with rows (e1, e2, n): local axes for a primitive whose 'depth' axis is n."""
    n = Vector(n).normalized()
    up = Vector((0, 0, 1)) if abs(n.z) < 0.9 else Vector((1, 0, 0))
    e1 = up.cross(n).normalized()
    e2 = n.cross(e1).normalized()
    return np.array([e1, e2, n], np.float32)


def sd_ellipsoid(Q, c, R, rot):
    """Q (M,3); c centre; R (3,) radii along rot rows; rot 3x3 rows = local axes."""
    L = (Q - np.asarray(c, np.float32)) @ rot.T
    R = np.asarray(R, np.float32)
    k0 = np.linalg.norm(L / R, axis=1)
    k1 = np.linalg.norm(L / (R * R), axis=1)
    return k0 * (k0 - 1.0) / np.maximum(k1, 1e-6)


def sd_capsule(Q, a, b, ra, rb):
    a = np.asarray(a, np.float32)
    b = np.asarray(b, np.float32)
    D = b - a
    t = np.clip(((Q - a) @ D) / max(1e-9, float(D @ D)), 0, 1)
    C = a + t[:, None] * D
    return np.linalg.norm(Q - C, axis=1) - (ra + (rb - ra) * t)


def sd_torus(Q, c, n, R, r):
    rot = frame_from(n)
    L = (Q - np.asarray(c, np.float32)) @ rot.T
    q = np.sqrt(L[:, 0] ** 2 + L[:, 1] ** 2) - R
    return np.sqrt(q * q + L[:, 2] ** 2) - r


# ================================================================== the skeleton
class Br:
    _n = 0

    def __init__(self, pts, rads, level, kind, parent=None, ps=0.0, twist=0.0, seed=0, bark=None):
        self.P = np.array([tuple(p) for p in pts], np.float64)
        self.R = np.array(rads, np.float64)
        self.level, self.kind, self.parent, self.ps = level, kind, parent, ps
        self.twist = twist
        self.id = Br._n
        Br._n += 1
        self.seed = seed
        self.bark = dict(bark or {})
        self.children = []
        self.core = True
        self.k = 0.0          # smooth-union radius into what is already there
        self.update()

    def update(self):
        P = self.P
        d = np.diff(P, axis=0)
        L = np.linalg.norm(d, axis=1)
        self.seglen = np.maximum(L, 1e-6)
        self.S = np.concatenate([[0.0], np.cumsum(L)])
        self.length = float(self.S[-1])
        n = len(P)
        T = np.zeros((n, 3))
        T[0] = d[0] / self.seglen[0]
        T[-1] = d[-1] / self.seglen[-1]
        for i in range(1, n - 1):
            t = d[i - 1] / self.seglen[i - 1] + d[i] / self.seglen[i]
            T[i] = t / max(1e-9, np.linalg.norm(t))
        ref = np.array([1.0, 0, 0]) if abs(T[0][0]) < 0.9 else np.array([0, 1.0, 0])
        N = np.zeros((n, 3))
        nn = ref - T[0] * ref.dot(T[0])
        N[0] = nn / np.linalg.norm(nn)
        for i in range(1, n):
            nn = N[i - 1] - T[i] * N[i - 1].dot(T[i])
            ln = np.linalg.norm(nn)
            if ln < 1e-6:
                nn = ref - T[i] * ref.dot(T[i])
                ln = np.linalg.norm(nn)
            N[i] = nn / ln
        self.T, self.N = T, N
        self.B = np.cross(T, N)
        self.off = np.array([(self.seed * 7.13) % 97, (self.seed * 3.71) % 89, (self.seed * 5.37) % 83], np.float32)

    def at(self, s):
        """position, radius, tangent at arclength s."""
        s = min(max(s, 0.0), self.length)
        i = int(np.clip(np.searchsorted(self.S, s, side="right") - 1, 0, len(self.P) - 2))
        t = (s - self.S[i]) / self.seglen[i]
        p = self.P[i] * (1 - t) + self.P[i + 1] * t
        r = self.R[i] * (1 - t) + self.R[i + 1] * t
        T = self.T[i] * (1 - t) + self.T[i + 1] * t
        return p, r, T / max(1e-9, np.linalg.norm(T))

    def s_at_radius(self, rc):
        """first arclength where the radius drops below rc (length if never)."""
        if self.R[0] < rc:
            return 0.0
        for i in range(len(self.R) - 1):
            if self.R[i + 1] < rc <= self.R[i]:
                t = (self.R[i] - rc) / max(1e-9, self.R[i] - self.R[i + 1])
                return float(self.S[i] + t * self.seglen[i])
        return self.length

    def cut(self, s0, s1):
        """sub-polyline [s0, s1] as (P, R, S-offset)."""
        pts, rad = [], []
        p, r, _ = self.at(s0)
        pts.append(p)
        rad.append(r)
        for i in range(len(self.P)):
            if s0 < self.S[i] < s1:
                pts.append(self.P[i])
                rad.append(self.R[i])
        p, r, _ = self.at(s1)
        if s1 - s0 > 1e-4:
            pts.append(p)
            rad.append(r)
        return np.array(pts), np.array(rad)


def rot_about(v, axis, ang):
    return Matrix.Rotation(ang, 3, axis.normalized()) @ v


def grow_path(p0, d0, L, rng, crook=0.5, fq=0.4, kink_rate=0.25, kink_deg=(12, 28), trop=0.0, spread=0.0,
              ds=0.12, curl=0.0, zmin=0.8, droop=0.0, centre=(0.0, 0.0), rmax=99.0, zmax=99.0, avoid=None):
    """A crooked growth path: perpendicular noise wobble, zig-zag elbows, tropism, outward spread, tip curl."""
    off = Vector((rng.uniform(-90, 90), rng.uniform(-90, 90), rng.uniform(-90, 90)))
    n = max(3, int(math.ceil(L / ds)))
    ds = L / n
    p = Vector(p0)
    d = Vector(d0).normalized()
    pts = [p.copy()]
    zig = 1 if rng.random() < 0.5 else -1
    for i in range(n):
        t = (i + 0.5) / n
        q = p * fq + off
        w = Vector((noise.noise(q), noise.noise(q + Vector((17.1, 0, 0))), noise.noise(q + Vector((0, 23.7, 0)))))
        w -= d * w.dot(d)
        d = d + w * crook * ds * 2.2
        if trop:
            d.z += trop * ds
        if droop:
            d.z -= droop * ds * t
        o = Vector((p.x - centre[0], p.y - centre[1], 0.0))
        if spread and o.length > 1e-3:
            d += o.normalized() * spread * ds
        if curl and t > 0.55:
            d.z += curl * ds * (t - 0.55) / 0.45
        if p.z < zmin:
            d.z += (zmin - p.z) * 1.5 * ds
        if o.length > rmax:
            d += -o.normalized() * (o.length - rmax) * 1.2 * ds
            d.z += (o.length - rmax) * 0.6 * ds
        if p.z > zmax:
            d.z -= (p.z - zmax) * 1.5 * ds
        if avoid is not None and p.z < avoid[1] and o.length < avoid[0]:
            d += (o.normalized() if o.length > 1e-3 else Vector((1, 0, 0))) * (avoid[0] - o.length) * 4.0 * ds
        if d.z < -0.35:
            d.z += (-0.35 - d.z) * 0.8
        if rng.random() < kink_rate * ds and 0.08 < t < 0.92:
            side = d.cross(Vector((0, 0, 1)))
            if side.length < 1e-3:
                side = Vector((1, 0, 0))
            axis = (side.normalized() * 0.6 + d.cross(side).normalized() * zig * 0.8).normalized()
            d = rot_about(d, axis, math.radians(rng.uniform(*kink_deg)) * zig)
            zig = -zig
        d.normalize()
        p = p + d * ds
        pts.append(p.copy())
    return pts


def elbow_path(p0, az0, elevs, lens, rng, ds=0.13, wander=18.0, wob=0.07, smooth=4, hook=0.0):
    """Gnarled limb: straight runs joined by sharp-ish elbows (elevation zig-zag, azimuth wander), rounded by a few
    smoothing passes, plus a small perpendicular wobble."""
    ctrl = [Vector(p0)]
    az = math.radians(az0)
    sgn = 1 if rng.random() < 0.5 else -1
    for k, (e, L) in enumerate(zip(elevs, lens)):
        a = az + math.radians(wander * sgn * (0.6 + 0.4 * rng.random())) * (1 if k else 0)
        sgn = -sgn
        er = math.radians(e)
        ctrl.append(ctrl[-1] + Vector((math.cos(a) * math.cos(er), math.sin(a) * math.cos(er), math.sin(er))) * L)
    if hook:
        # the tip hooks over like a claw finger
        d = (ctrl[-1] - ctrl[-2]).normalized()
        hz = Vector((d.x, d.y, 0)).normalized() * 0.7 + Vector((0, 0, -0.25))
        ctrl.append(ctrl[-1] + hz.normalized() * hook)
    pts = []
    for k in range(len(ctrl) - 1):
        a, b = ctrl[k], ctrl[k + 1]
        n = max(2, int((b - a).length / ds))
        for j in range(n):
            pts.append(a.lerp(b, j / n))
    pts.append(ctrl[-1])
    for _ in range(smooth):
        pts = [pts[0]] + [(pts[j - 1] + pts[j] * 2 + pts[j + 1]) / 4 for j in range(1, len(pts) - 1)] + [pts[-1]]
    off = Vector((rng.uniform(-90, 90), rng.uniform(-90, 90), rng.uniform(-90, 90)))
    out = []
    for j, p in enumerate(pts):
        t = j / (len(pts) - 1)
        q = p * 0.6 + off
        w = Vector((noise.noise(q), noise.noise(q + Vector((17.1, 0, 0))), noise.noise(q + Vector((0, 23.7, 0)))))
        out.append(p + w * wob * min(1.0, t * 6))
    return out


def taper(n, r0, r1, pw=1.0):
    return [r1 + (r0 - r1) * (1 - i / (n - 1)) ** pw for i in range(n)]


def make_branch(tree, parent, s_on_parent, d0, L, r0, r1, level, kind, spec, rng, pw=1.0, p0=None):
    p_par = None
    if parent is not None:
        p_par, _, _ = parent.at(s_on_parent)
    start = Vector(p0) if p0 is not None else V(p_par)
    pts = grow_path(start, d0, L, rng, crook=spec.get("crook", 0.5), fq=spec.get("fq", 0.45),
                    kink_rate=spec.get("kink", 0.25), kink_deg=spec.get("kink_deg", (12, 28)),
                    trop=spec.get("trop", 0.0), spread=spec.get("spread", 0.0), ds=spec.get("ds", 0.12),
                    curl=spec.get("curl", 0.0), zmin=spec.get("zmin", 0.8), droop=spec.get("droop", 0.0),
                    rmax=spec.get("rmax", 99.0), zmax=spec.get("zmax", 99.0), avoid=spec.get("avoid"))
    rads = taper(len(pts), r0, r1, pw)
    b = Br(pts, rads, level, kind, parent, s_on_parent, twist=spec.get("twist", 0.0),
           seed=rng.randint(1, 10 ** 6), bark=spec.get("bark"))
    if parent is not None:
        parent.children.append(b)
    tree.append(b)
    return b


def child_dir(par, s, ang_deg, az, up_bias=0.25, out_bias=0.25):
    p, r, T = par.at(s)
    T = Vector(T)
    i = int(np.clip(np.searchsorted(par.S, s) - 1, 0, len(par.P) - 1))
    N = Vector(par.N[i])
    N = (N - T * N.dot(T)).normalized()
    perp = rot_about(N, T, az)
    d = (T * math.cos(math.radians(ang_deg)) + perp * math.sin(math.radians(ang_deg))).normalized()
    d.z += up_bias
    o = Vector((p[0], p[1], 0.0))
    if o.length > 1e-3:
        d += o.normalized() * out_bias
    d.normalize()
    if d.z < -0.12:
        d.z = -0.12
    return d.normalized()


def grow_children(tree, b, spec_levels, rng, max_level):
    """fork at the tip + side branches, recursively (level specs: spec_levels[level])."""
    lv = b.level + 1
    if lv > max_level:
        return
    S = spec_levels[lv]
    kids = []
    # tip fork
    if S.get("fork", 0) and b.length > 0.3:
        nf = S["fork"]
        p, r, T = b.at(b.length)
        T = Vector(T)
        az0 = rng.uniform(0, 2 * math.pi)
        for j in range(nf):
            ang = rng.uniform(*S["fork_ang"])
            az = az0 + 2 * math.pi * j / nf + rng.uniform(-0.4, 0.4)
            d = child_dir(b, b.length, ang, az, S.get("up", 0.2), S.get("out", 0.2))
            L = rng.uniform(*S["L"]) * (1.0 if j == 0 else rng.uniform(0.75, 0.95))
            r0 = r * rng.uniform(*S.get("fork_r", (0.8, 0.92)))
            r1 = max(S["tip_r"], r0 * S.get("end_k", 0.3))
            kids.append(make_branch(tree, b, b.length, d, L, r0, r1, lv, S["kind"], S, rng, S.get("pw", 1.0),
                                    p0=V(p) - V(T) * max(r * 1.4, 0.12)))
        # neck the parent's tip down inside its (thinner, 0.8-0.92 r) fork children, so the parent tube's flat end
        # cap never shows round them (review round 1: "flat cut ends")
        Lt = max(r * 1.4, 0.12)
        dd = b.length - b.S
        f = np.clip(1.0 - dd / Lt, 0.0, 1.0)
        b.R = b.R * (1.0 - 0.38 * f * f)
    # side branches
    ns = rng.randint(*S.get("side", (0, 0)))
    az = rng.uniform(0, 2 * math.pi)
    for j in range(ns):
        s = b.length * rng.uniform(*S["side_t"])
        az += math.radians(137.5 + rng.uniform(-25, 25))
        p, r, T = b.at(s)
        d = child_dir(b, s, rng.uniform(*S["side_ang"]), az, S.get("up", 0.2), S.get("out", 0.2))
        L = rng.uniform(*S["L"]) * S.get("side_L", 0.75) * (1 - 0.35 * s / max(1e-3, b.length))
        r0 = r * rng.uniform(*S.get("side_r", (0.5, 0.68)))
        r1 = max(S["tip_r"], r0 * S.get("end_k", 0.3))
        kids.append(make_branch(tree, b, s, d, L, r0, r1, lv, S["kind"], S, rng, S.get("pw", 1.0)))
    for k in kids:
        grow_children(tree, k, spec_levels, rng, max_level)


# ================================================================== bark (per branch, local coordinates)
def bark_eval(br, s, a, r, deflect=None):
    """s arclength, a angle around the axis, r local radius (arrays). Returns offset (studs) + attributes.
    Furrowed bark: narrow, deep, braided furrows along the (twisting) axis, broad plates with a few cross-cracks,
    and bare weathered-wood patches (bark fallen off) with long grain lines."""
    bk = br.bark
    R0 = np.maximum(r, 0.04).astype(np.float32)
    ang = a + br.twist * s
    u = None
    if deflect is not None:
        ang, s = deflect(br, ang, s, R0)
    X = np.cos(ang) * R0
    Y = np.sin(ang) * R0
    Z = s.astype(np.float32)
    o = br.off
    f = bk.get("f", 2.6) / np.maximum(0.3, R0) ** 0.2
    st = bk.get("stretch", 4.8)
    ax, ay, az = X * f + o[0], Y * f + o[1], Z * f / st + o[2]
    wv = PNZ(ax * 0.4 + 5.3, ay * 0.4, az * 0.4) * 0.55
    n1 = PNZ.fbm(ax + wv, ay - wv, az + 0.3 * wv, 2, gain=0.42)
    furrow = np.clip(1.0 - np.abs(n1) * bk.get("fw", 2.6), 0, 1) ** 1.5
    plate = PNZ.fbm(ax * 2.1 + 40, ay * 2.1, az * 2.6, 2)
    cr = PNZ(X * f * 0.8 + 90, Y * f * 0.8, Z * f * 1.8)
    cross = (np.clip(1 - np.abs(cr) * 7.0, 0, 1) ** 2) * sm(0.0, 0.25, plate)
    depth = bk.get("depth", 0.11) * np.clip(R0, 0.05, 0.95)
    off = depth * (0.4 - furrow - 0.15 * cross) + depth * 0.22 * plate
    pm = bk.get("patch", 0.0)
    if pm > 0:
        pv = PNZ.fbm(X * 0.55 + o[1], Y * 0.55 + 200, Z * 0.32 + o[0], 2)
        patch = sm(bk.get("patch_lo", 0.2), bk.get("patch_lo", 0.2) + 0.08, pv) * pm
        g = PNZ(X * 7.0 + 300, Y * 7.0, Z * 0.55 + o[2])
        grain = np.clip(1 - np.abs(g) * 3.5, 0, 1) ** 2.5
        off_w = -depth * 0.55 - 0.018 * grain * np.clip(R0 / 0.4, 0.3, 1.0)
        off = off * (1 - patch) + off_w * patch
    else:
        patch = np.zeros_like(off)
        grain = np.zeros_like(off)
    return off.astype(np.float32), dict(furrow=furrow, plate=plate, cross=cross, patch=patch, grain=grain)


# ================================================================== branch distance fields
def branch_seg_region(br, P, R, X, Y, Z, pad):
    """hard-min capsule distance on a grid region (axes X, Y, Z). Returns dmin, seg, t (3D arrays)."""
    shape = (len(X), len(Y), len(Z))
    dmin = np.full(shape, 9.0, np.float32)
    seg = np.full(shape, -1, np.int32)
    tt = np.zeros(shape, np.float32)
    for i in range(len(P) - 1):
        a, b = P[i], P[i + 1]
        ra, rb = R[i], R[i + 1]
        pd = max(ra, rb) + pad
        lo = np.minimum(a, b) - pd
        hi = np.maximum(a, b) + pd
        sl = []
        for k, ax in enumerate((X, Y, Z)):
            i0 = int(np.searchsorted(ax, lo[k]))
            i1 = int(np.searchsorted(ax, hi[k], side="right"))
            sl.append(slice(i0, i1))
        if any(s.stop <= s.start for s in sl):
            continue
        x = X[sl[0]][:, None, None].astype(np.float32)
        y = Y[sl[1]][None, :, None].astype(np.float32)
        z = Z[sl[2]][None, None, :].astype(np.float32)
        D = (b - a).astype(np.float32)
        L2 = float(D @ D)
        t = np.clip(((x - a[0]) * D[0] + (y - a[1]) * D[1] + (z - a[2]) * D[2]) / L2, 0, 1)
        dx = x - (a[0] + t * D[0])
        dy = y - (a[1] + t * D[1])
        dz = z - (a[2] + t * D[2])
        dist = np.sqrt(dx * dx + dy * dy + dz * dz) - (ra + t * (rb - ra))
        sub = dmin[tuple(sl)]
        m = dist < sub
        sub[m] = dist[m]
        seg[tuple(sl)][m] = i
        tt[tuple(sl)][m] = t[m] if t.shape == m.shape else np.broadcast_to(t, m.shape)[m]
    return dmin, seg, tt


def branch_seg_points(P, R, Q, pad):
    M = len(Q)
    dmin = np.full(M, 9.0, np.float32)
    seg = np.full(M, -1, np.int32)
    tt = np.zeros(M, np.float32)
    for i in range(len(P) - 1):
        a, b = P[i], P[i + 1]
        ra, rb = R[i], R[i + 1]
        pd = max(ra, rb) + pad
        lo = np.minimum(a, b) - pd
        hi = np.maximum(a, b) + pd
        m = np.all((Q >= lo) & (Q <= hi), axis=1)
        idx = np.nonzero(m)[0]
        if not len(idx):
            continue
        q = Q[idx]
        D = (b - a)
        t = np.clip(((q - a) @ D) / max(1e-12, D @ D), 0, 1)
        C = a + t[:, None] * D
        dist = np.linalg.norm(q - C, axis=1) - (ra + t * (rb - ra))
        better = dist < dmin[idx]
        ii = idx[better]
        dmin[ii] = dist[better]
        seg[ii] = i
        tt[ii] = t[better]
    return dmin, seg, tt


def local_coords(br, P, Sg, q, seg, t):
    """arclength s, angle a, local radius r for points q on their nearest segment (P = the branch's polyline).
    The incoming seg/t come from the radius-biased SDF search: on a tapered / bulging branch a point often 'belongs'
    to a thicker neighbour segment with t clamped to its end, which quantises s into steps (= stair-step bark).
    Re-pick the segment by plain distance to the AXIS among the +-2 neighbours, with unclamped-then-clamped t."""
    nseg = len(P) - 1
    soft = float(getattr(br, "soft_s", 0.0) or 0.0)
    if soft > 0:
        # points far from a bent axis (a burl): a hard nearest-segment pick quantises s on the inside of bends and
        # freezes it in the wedges on the outside -> dashed bark. Blend the UNCLAMPED arclengths of the +-2
        # neighbours, weighted by how far the projection falls outside each segment, so s varies smoothly.
        dl, sl_, ol = [], [], []
        for off in (-2, -1, 0, 1, 2):
            c = np.clip(seg + off, 0, nseg - 1)
            Dc = P[c + 1] - P[c]
            Lc = np.linalg.norm(Dc, axis=1)
            tu = np.sum((q - P[c]) * Dc, axis=1) / np.maximum(Lc * Lc, 1e-12)
            tc = np.clip(tu, 0, 1)
            dl.append(np.linalg.norm(q - (P[c] + tc[:, None] * Dc), axis=1))
            sl_.append(Sg[c] + tu * Lc)
            ol.append(np.maximum(0.0, np.maximum(-tu, tu - 1.0)) * Lc)
        dl, ol = np.array(dl), np.array(ol)
        w = np.exp(-(ol / soft) ** 2) * np.exp(-(dl - dl.min(0)) / 0.4) + 1e-12
        s = np.sum(w * np.array(sl_), 0) / np.sum(w, 0)
        s = np.clip(s, Sg[0], Sg[-1])
        C = np.stack([np.interp(s, Sg, P[:, k]) for k in range(3)], 1)
    else:
        bestd = np.full(len(q), np.inf)
        bseg = seg.copy()
        bt = t.copy()
        for off in (-2, -1, 0, 1, 2):
            c = np.clip(seg + off, 0, nseg - 1)
            Dc = P[c + 1] - P[c]
            tc = np.clip(np.sum((q - P[c]) * Dc, axis=1) / np.maximum(np.sum(Dc * Dc, axis=1), 1e-12), 0, 1)
            dc = np.linalg.norm(q - (P[c] + tc[:, None] * Dc), axis=1)
            m = dc < bestd
            bestd[m] = dc[m]
            bseg[m] = c[m]
            bt[m] = tc[m]
        seg, t = bseg, bt
        D = P[seg + 1] - P[seg]
        L = np.linalg.norm(D, axis=1)
        s = Sg[seg] + t * L
        C = P[seg] + t[:, None] * D
    # frames: interpolate the branch's node frames at the arclength s
    idx = np.clip(np.searchsorted(br.S, s, side="right") - 1, 0, len(br.P) - 2)
    u = ((s - br.S[idx]) / br.seglen[idx])[:, None]
    N = br.N[idx] * (1 - u) + br.N[idx + 1] * u
    T = br.T[idx] * (1 - u) + br.T[idx + 1] * u
    T /= np.maximum(1e-9, np.linalg.norm(T, axis=1))[:, None]
    N = N - T * np.sum(N * T, axis=1)[:, None]
    N /= np.maximum(1e-9, np.linalg.norm(N, axis=1))[:, None]
    B = np.cross(T, N)
    v = q - C
    a = np.arctan2(np.sum(v * B, axis=1), np.sum(v * N, axis=1))
    rr = br.R[idx] * (1 - u[:, 0]) + br.R[idx + 1] * u[:, 0]
    return s.astype(np.float32), a.astype(np.float32), rr.astype(np.float32)


# ================================================================== SDF grid (OpenVDB)
class SDF:
    def __init__(self, lo, hi, h, band):
        import openvdb as vdb
        self.vdb = vdb
        self.h, self.band = float(h), float(band)
        self.origin = np.floor(np.array(lo, np.float64) / h) * h
        self.dims = np.ceil((np.array(hi, np.float64) - self.origin) / h).astype(int) + 1
        self.grid = vdb.FloatGrid(self.band)

    def region(self, lo, hi):
        i0 = np.floor((np.array(lo) - self.origin) / self.h).astype(int)
        i1 = np.ceil((np.array(hi) - self.origin) / self.h).astype(int)
        i0 = np.maximum(i0, 0)
        i1 = np.minimum(i1, self.dims - 1)
        shape = tuple(int(v) for v in (i1 - i0 + 1))
        buf = np.full(shape, self.band, np.float32)
        self.grid.copyToArray(buf, ijk=tuple(int(v) for v in i0))
        axes = [self.origin[k] + (i0[k] + np.arange(shape[k])) * self.h for k in range(3)]
        return i0, buf, axes

    def write(self, i0, buf):
        np.clip(buf, -self.band, self.band, out=buf)
        self.grid.copyFromArray(np.ascontiguousarray(buf, np.float32), ijk=tuple(int(v) for v in i0), tolerance=0.0)

    def apply_points(self, lo, hi, fn):
        """fn(buf_flat, Q) -> new flat values, evaluated on a region."""
        i0, buf, axes = self.region(lo, hi)
        X, Y, Z = np.meshgrid(*axes, indexing="ij")
        Q = np.stack([X.ravel(), Y.ravel(), Z.ravel()], 1).astype(np.float32)
        out = fn(buf.ravel(), Q).reshape(buf.shape)
        self.write(i0, out.astype(np.float32))

    def mesh(self, name):
        pts, quads = self.grid.convertToQuads(isovalue=0.0)
        pts = self.origin + pts.astype(np.float64) * self.h
        me = bpy.data.meshes.new(name)
        me.vertices.add(len(pts))
        me.vertices.foreach_set("co", pts.astype(np.float32).ravel())
        nq = len(quads)
        me.loops.add(nq * 4)
        me.polygons.add(nq)
        me.loops.foreach_set("vertex_index", quads.astype(np.int32).ravel())
        me.polygons.foreach_set("loop_start", np.arange(0, nq * 4, 4, dtype=np.int32))
        me.update(calc_edges=True)
        me.validate()
        ob = link(bpy.data.objects.new(name, me))
        # outward normals: a closed level set mesh -> make the signed volume positive
        bm = bmesh.new()
        bm.from_mesh(me)
        if bm.calc_volume(signed=True) < 0:
            bmesh.ops.reverse_faces(bm, faces=bm.faces[:])
            bm.to_mesh(me)
        bm.free()
        for p in me.polygons:
            p.use_smooth = True
        return ob


def add_branch_sdf(sdf, br, P, R, groove, k, deflect=None):
    pad = sdf.band + 0.05
    lo = P.min(0) - R.max() - pad
    hi = P.max(0) + R.max() + pad
    i0, buf, (X, Y, Z) = sdf.region(lo, hi)
    dmin, seg, tt = branch_seg_region(br, P, R, X, Y, Z, pad)
    if groove:
        band = np.nonzero((np.abs(dmin) < 0.3) & (seg >= 0))
        if len(band[0]):
            q = np.stack([X[band[0]], Y[band[1]], Z[band[2]]], 1).astype(np.float64)
            Sg = np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))]) + _s_offset(br, P)
            s, a, r = local_coords(br, P, Sg, q, seg[band], tt[band].astype(np.float64))
            off, _ = bark_eval(br, s, a, r, deflect)
            dmin[band] -= off
    out = smin(buf, dmin, k) if k > 0 else np.minimum(buf, dmin)
    sdf.write(i0, out)


def _s_offset(br, P):
    """arclength of P[0] along the branch (P may be a cut of the branch)."""
    d = np.linalg.norm(br.P - P[0], axis=1)
    i = int(np.argmin(d))
    return float(br.S[i]) if d[i] < 1e-6 else float(br.S[max(0, i - 1)] + np.linalg.norm(P[0] - br.P[max(0, i - 1)]))


# ================================================================== per-vertex bark colour
def core_vertex_attrs(items, Vt, deflect=None, kc=0.06):
    """items: list of (br, P, R). Soft-blended (by distance) bark attributes for the core mesh vertices."""
    M = len(Vt)
    keys = ("furrow", "plate", "cross", "patch", "grain", "level", "s", "r")
    acc = {k: np.zeros(M, np.float64) for k in keys}
    wsum = np.zeros(M, np.float64)
    best = np.full(M, 9.0)
    per = []
    for br, P, R in items:
        dmin, seg, tt = branch_seg_points(P, R, Vt, 0.6)
        per.append((br, P, R, dmin, seg, tt))
        best = np.minimum(best, dmin)
    for br, P, R, dmin, seg, tt in per:
        m = (seg >= 0) & (dmin < best + 6 * kc)
        idx = np.nonzero(m)[0]
        if not len(idx):
            continue
        w = np.exp(-(dmin[idx] - best[idx]) / kc)
        Sg = np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))]) + _s_offset(br, P)
        s, a, r = local_coords(br, P, Sg, Vt[idx].astype(np.float64), seg[idx], tt[idx].astype(np.float64))
        _, at = bark_eval(br, s, a, r, deflect if br.kind == "trunk" else None)
        at["level"] = np.full(len(idx), float(br.level))
        at["s"] = s
        at["r"] = r
        for k in keys:
            acc[k][idx] += w * at[k]
        wsum[idx] += w
    wsum = np.maximum(wsum, 1e-9)
    for k in keys:
        acc[k] /= wsum
    acc["dist"] = best
    return acc


PAL = dict(
    bark=lin((90, 79, 64)), bark2=lin((110, 97, 78)), ridge=lin((148, 137, 114)), furrow=lin((40, 32, 26)),
    wood=lin((152, 144, 124)), wood2=lin((118, 108, 89)), grainc=lin((74, 64, 52)),
    lichen=lin((142, 158, 130)), lichen2=lin((184, 196, 168)), lichen_y=lin((186, 180, 100)),
    damp=lin((58, 46, 38)), moss=lin((74, 96, 40)), hollow=lin((20, 13, 10)), hollow2=lin((72, 46, 30)),
    stubend=lin((196, 170, 128)),
)


def mixc(a, b, t):
    t = np.asarray(t, np.float64)[:, None]
    return a * (1 - t) + b * t


def bark_colours(at, Vw, Nw, pal=PAL, seed=0, lichen_amt=1.0, extra=None, lichen_fn=None):
    """vectorised colours + roughness. at: attribute arrays; Vw world positions; Nw normals."""
    M = len(Vw)
    fur, plate, cross, patch, grain = at["furrow"], at["plate"], at["cross"], at["patch"], at["grain"]
    base = mixc(np.tile(pal["bark"], (M, 1)), np.tile(pal["bark2"], (M, 1)), np.clip(plate * 0.8 + 0.5, 0, 1))
    tone = PNZ.fbm(Vw[:, 0] * 0.35 + seed, Vw[:, 1] * 0.35, Vw[:, 2] * 0.35, 2)
    base = base * (1.0 + 0.16 * tone[:, None])
    ridge = np.clip((1 - fur) * (0.45 + plate), 0, 1) ** 2
    col = mixc(base, np.tile(pal["ridge"], (M, 1)), 0.55 * ridge)
    col = mixc(col, np.tile(pal["furrow"], (M, 1)), np.clip(0.9 * fur + 0.25 * cross, 0, 1))
    wood = mixc(np.tile(pal["wood"], (M, 1)), np.tile(pal["wood2"], (M, 1)), np.clip(0.5 + 0.6 * tone, 0, 1))
    wood = mixc(wood, np.tile(pal["grainc"], (M, 1)), 0.75 * grain)
    col = mixc(col, wood, patch)
    rough = 0.88 - 0.1 * ridge + 0.06 * fur - 0.2 * patch
    # lichen: cool grey-green crusts on the upper sides, speckled edges (none in the furrows)
    up = np.clip(Nw[:, 2] * 0.6 + 0.45, 0, 1)
    ln = PNZ.fbm(Vw[:, 0] * 0.8 + 31 + seed, Vw[:, 1] * 0.8, Vw[:, 2] * 0.8, 3)
    sp = PNZ(Vw[:, 0] * 9 + seed, Vw[:, 1] * 9, Vw[:, 2] * 9)
    lich = sm(0.05, 0.4, ln + 0.2 * sp) * up * (1 - 0.8 * fur) * (1 - 0.7 * patch) * lichen_amt
    if lichen_fn is not None:
        lich = lich * lichen_fn(Vw)
    lich = lich * sm(0.4, 1.4, Vw[:, 2])
    lcol = mixc(np.tile(pal["lichen"], (M, 1)), np.tile(pal["lichen2"], (M, 1)), np.clip(0.5 + sp, 0, 1))
    yel = sm(0.45, 0.6, PNZ(Vw[:, 0] * 2.2 + 70, Vw[:, 1] * 2.2, Vw[:, 2] * 2.2))
    lcol = mixc(lcol, np.tile(pal["lichen_y"], (M, 1)), 0.6 * yel)
    col = mixc(col, lcol, 0.85 * lich)
    rough = rough + 0.06 * lich
    # damp, darker base + a little moss near the soil
    low = 1 - sm(0.0, 0.9, Vw[:, 2])
    col = mixc(col, np.tile(pal["damp"], (M, 1)), 0.55 * low)
    mz = sm(0.05, 0.3, PNZ(Vw[:, 0] * 1.3 + 9, Vw[:, 1] * 1.3, Vw[:, 2] * 1.3)) * (1 - sm(0.2, 1.1, Vw[:, 2]))
    col = mixc(col, np.tile(pal["moss"], (M, 1)), 0.6 * mz * up)
    if extra is not None:
        col, rough = extra(col, rough, Vw, Nw)
    return np.clip(col, 0, 1), np.clip(rough, 0.3, 1.0)


# ================================================================== tubes (thin branches)
def tube_rings(P, R, step, ramp_in=0.0):
    """resample a polyline at ~step; returns points, radii, arclengths."""
    d = np.linalg.norm(np.diff(P, axis=0), axis=1)
    S = np.concatenate([[0.0], np.cumsum(d)])
    L = S[-1]
    n = max(2, int(math.ceil(L / step)) + 1)
    ss = np.linspace(0, L, n)
    pts = np.stack([np.interp(ss, S, P[:, k]) for k in range(3)], 1)
    rr = np.interp(ss, S, R)
    if ramp_in > 0:
        rr = rr * (0.97 + 0.03 * np.clip(ss / ramp_in, 0, 1))
    return pts, rr, ss


def frames_along(pts, N0=None):
    n = len(pts)
    T = np.zeros((n, 3))
    for i in range(n):
        t = pts[min(n - 1, i + 1)] - pts[max(0, i - 1)]
        T[i] = t / max(1e-9, np.linalg.norm(t))
    if N0 is None:
        ref = np.array([0, 0, 1.0]) if abs(T[0][2]) < 0.9 else np.array([1.0, 0, 0])
        N0 = ref
    N = np.zeros((n, 3))
    nn = N0 - T[0] * np.dot(N0, T[0])
    N[0] = nn / max(1e-9, np.linalg.norm(nn))
    for i in range(1, n):
        nn = N[i - 1] - T[i] * np.dot(N[i - 1], T[i])
        N[i] = nn / max(1e-9, np.linalg.norm(nn))
    return T, N, np.cross(T, N)


class MeshAcc:
    """accumulates verts / faces / per-vertex colour + rough + per-loop uv islands."""

    def __init__(self):
        self.V, self.F, self.C, self.Rg, self.Bu = [], [], [], [], []
        self.UV = []        # per face: list of uv tuples
        self.nv = 0

    def add_verts(self, pts, cols=None, rough=None, buried=None):
        i0 = self.nv
        self.Bu.append(np.asarray(buried, np.float32) if buried is not None else np.zeros(len(pts), np.float32))
        self.V.append(np.asarray(pts, np.float32))
        n = len(pts)
        self.C.append(np.asarray(cols, np.float32) if cols is not None else np.full((n, 3), 0.5, np.float32))
        self.Rg.append(np.asarray(rough, np.float32) if rough is not None else np.full(n, 0.8, np.float32))
        self.nv += n
        return i0

    def face(self, idx, uv=None):
        self.F.append(tuple(int(i) for i in idx))
        self.UV.append(uv)

    def build(self, name, smooth=True, colors=True, uvs=False):
        Vt = np.concatenate(self.V) if self.V else np.zeros((0, 3), np.float32)
        me = bpy.data.meshes.new(name)
        me.from_pydata(Vt.tolist(), [], self.F)
        me.update()
        if colors and len(Vt):
            Ct = np.concatenate(self.C)
            Rt = np.concatenate(self.Rg)
            set_colors(me, "Col", [tuple(c) for c in Ct])
            set_colors(me, "Rough", [(r, r, r) for r in Rt])
            Bt = np.concatenate(self.Bu)
            if Bt.any():
                set_colors(me, "Buried", [(b, b, b) for b in Bt])
        if uvs:
            uvl = me.uv_layers.new(name="UVMap")
            data = []
            for p, uvf in zip(me.polygons, self.UV):
                data.extend([c for uvp in uvf for c in uvp])
            uvl.data.foreach_set("uv", data)
        for p in me.polygons:
            p.use_smooth = smooth
        return link(bpy.data.objects.new(name, me))


def tube_hi(acc, br, P, R, s0, step=0.04, colfn=None, tip_cap=True, start_cap=True, buried_fn=None):
    """dense round bark tube with furrow displacement + per-vertex colour."""
    pts, rr, ss = tube_rings(P, R, step)
    ss = ss + s0
    T, N, B = frames_along(pts)
    rmax = float(rr.max())
    sides = int(np.clip(round(2 * math.pi * rmax / 0.022), 8, 40))
    ang = np.linspace(0, 2 * math.pi, sides, endpoint=False)
    n = len(pts)
    S_ = np.repeat(ss, sides)
    A_ = np.tile(ang, n)
    R_ = np.repeat(rr, sides)
    off, at = bark_eval(br, S_.astype(np.float32), A_.astype(np.float32), R_.astype(np.float32))
    rad = R_ + off * np.clip(R_ / 0.06, 0.2, 1.0)
    Nr = np.repeat(N, sides, 0)
    Br_ = np.repeat(B, sides, 0)
    dirs = Nr * np.cos(A_)[:, None] + Br_ * np.sin(A_)[:, None]
    Pv = np.repeat(pts, sides, 0) + dirs * rad[:, None]
    at["level"] = np.full(len(Pv), float(br.level))
    col, rough = colfn(at, Pv, dirs) if colfn else (np.full((len(Pv), 3), 0.4), np.full(len(Pv), 0.8))
    bur = buried_fn(Pv) if buried_fn is not None else None
    i0 = acc.add_verts(Pv, col, rough, bur)
    for i in range(n - 1):
        for j in range(sides):
            k = (j + 1) % sides
            acc.face((i0 + i * sides + j, i0 + i * sides + k, i0 + (i + 1) * sides + k, i0 + (i + 1) * sides + j))
    if tip_cap:
        tip = pts[-1] + T[-1] * rr[-1] * 0.8
        c = acc.add_verts([tip], col[-1:], rough[-1:])
        for j in range(sides):
            k = (j + 1) % sides
            acc.face((i0 + (n - 1) * sides + j, i0 + (n - 1) * sides + k, c))
    if start_cap:
        bot = pts[0] - T[0] * rr[0] * 0.3
        c = acc.add_verts([bot], col[:1], rough[:1], [1.0] if buried_fn is not None else None)
        for j in range(sides):
            k = (j + 1) % sides
            acc.face((i0 + k, i0 + j, c))
    return len(Pv)


def pick_rings(pts, rr, ang_deg=11.0, max_len=0.7, min_len=0.08):
    """indices of the polyline points to keep for a low-poly tube (bends + length + radius change)."""
    keep = [0]
    last = 0
    for i in range(1, len(pts) - 1):
        d0 = pts[i] - pts[last]
        d1 = pts[i + 1] - pts[i]
        L = np.linalg.norm(d0)
        if L < min_len:
            continue
        c = np.dot(d0, d1) / max(1e-9, L * np.linalg.norm(d1))
        bend = math.degrees(math.acos(np.clip(c, -1, 1)))
        if bend > ang_deg or L > max_len or abs(rr[i] - rr[last]) > 0.3 * rr[last]:
            keep.append(i)
            last = i
    keep.append(len(pts) - 1)
    return keep


def tube_lo(acc, P, R, sides, uv_scale=1.0, tip_cap=True, start_cap=False, ang_deg=11.0, max_len=0.7):
    """low-poly tube with strip UVs (u around in studs, v along in studs); one UV island per tube."""
    pts, rr, ss = tube_rings(P, R, 0.05)
    keep = pick_rings(pts, rr, ang_deg, max_len)
    pts, rr, ss = pts[keep], rr[keep], ss[keep]
    T, N, B = frames_along(pts)
    n = len(pts)
    # the polygon's flat faces sit inside the round hi surface: push out so the faces straddle it
    kfit = 1.0 / math.cos(math.pi / sides) ** 0.5
    ang = np.linspace(0, 2 * math.pi, sides, endpoint=False)
    rows = []
    for i in range(n):
        ring = pts[i] + (N[i] * np.cos(ang)[:, None] + B[i] * np.sin(ang)[:, None]) * (rr[i] * kfit)
        rows.append(ring)
    i0 = acc.add_verts(np.concatenate(rows))
    circ = 2 * math.pi * float(rr.max()) * uv_scale
    for i in range(n - 1):
        for j in range(sides):
            k = (j + 1) % sides
            u0, u1 = circ * j / sides, circ * (j + 1) / sides
            v0, v1 = ss[i] * uv_scale, ss[i + 1] * uv_scale
            acc.face((i0 + i * sides + j, i0 + i * sides + k, i0 + (i + 1) * sides + k, i0 + (i + 1) * sides + j),
                     [(u0, v0), (u1, v0), (u1, v1), (u0, v1)])
    if tip_cap:
        tip = pts[-1] + T[-1] * rr[-1] * 0.8
        c = acc.add_verts([tip])
        vt = ss[-1] * uv_scale + rr[-1] * uv_scale
        for j in range(sides):
            k = (j + 1) % sides
            u0, u1 = circ * j / sides, circ * (j + 1) / sides
            acc.face((i0 + (n - 1) * sides + j, i0 + (n - 1) * sides + k, c),
                     [(u0, ss[-1] * uv_scale), (u1, ss[-1] * uv_scale), ((u0 + u1) / 2, vt)])
    if start_cap:
        c = acc.add_verts([pts[0] - T[0] * rr[0] * 0.3])
        for j in range(sides):
            k = (j + 1) % sides
            u0, u1 = circ * j / sides, circ * (j + 1) / sides
            acc.face((i0 + k, i0 + j, c), [(u1, 0), (u0, 0), ((u0 + u1) / 2, -rr[0] * uv_scale)])
    return n


def cyl_uv(ob, items, ndot=0.3, inner_tol=0.12, margin=0.004):
    """UVs for the SDF game mesh: every face goes to its nearest branch; outward-facing faces get that branch's
    cylindrical coordinates (u = angle x radius, v = arclength, in studs) = long continuous bark strips with the
    seam on the wrap line; faces inside cavities / end caps / steep crotch saddles get Smart UV. Then all islands are
    scaled to equal texel density and packed."""
    me = ob.data
    nF = len(me.polygons)
    C = np.empty(nF * 3, np.float32)
    me.polygons.foreach_get("center", C)
    C = C.reshape(-1, 3).astype(np.float64)
    Nf = np.empty(nF * 3, np.float32)
    me.polygons.foreach_get("normal", Nf)
    Nf = Nf.reshape(-1, 3).astype(np.float64)
    nV = len(me.vertices)
    Vc = np.empty(nV * 3, np.float32)
    me.vertices.foreach_get("co", Vc)
    Vc = Vc.reshape(-1, 3).astype(np.float64)
    best = np.full(nF, 9.0)
    bid = np.full(nF, -1)
    for k, (br, P, R) in enumerate(items):
        d, seg, t = branch_seg_points(P, R, C, 1.2)
        m = (seg >= 0) & (d < best)
        best[m] = d[m]
        bid[m] = k
    side = np.zeros(nF, bool)
    ls = np.empty(len(me.loops), np.int32)
    me.loops.foreach_get("vertex_index", ls)
    lstart = np.empty(nF, np.int32)
    me.polygons.foreach_get("loop_start", lstart)
    ltot = np.empty(nF, np.int32)
    me.polygons.foreach_get("loop_total", ltot)
    uv = np.zeros((len(me.loops), 2), np.float64)
    for k, (br, P, R) in enumerate(items):
        fi = np.nonzero(bid == k)[0]
        if not len(fi):
            continue
        Sg = np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))]) + _s_offset(br, P)
        d, seg, t = branch_seg_points(P, R, C[fi], 3.0)
        ok = seg >= 0
        fi, seg, t = fi[ok], seg[ok], t[ok]
        D = P[seg + 1] - P[seg]
        A = P[seg] + t[:, None] * D
        rad = C[fi] - A
        rl = np.linalg.norm(rad, axis=1)
        dot = np.sum(Nf[fi] * rad, axis=1) / np.maximum(rl, 1e-9)
        rr = R[seg] + t * (R[seg + 1] - R[seg])
        good = (dot > ndot) & (rr - rl < inner_tol)
        fs = fi[good]
        side[fs] = True
        if not len(fs):
            continue
        # per-loop coordinates (wrt this branch)
        loops = np.concatenate([np.arange(lstart[f], lstart[f] + ltot[f]) for f in fs])
        vids = ls[loops]
        uvid, inv = np.unique(vids, return_inverse=True)
        d2, seg2, t2 = branch_seg_points(P, R, Vc[uvid], 3.0)
        seg2 = np.maximum(seg2, 0)
        s, a, r = local_coords(br, P, Sg, Vc[uvid], seg2, t2.astype(np.float64))
        a_l = a[inv].astype(np.float64)
        s_l = s[inv].astype(np.float64)
        # wrap fix per face
        pos = 0
        for f in fs:
            n = ltot[f]
            seg_a = a_l[pos:pos + n]
            if seg_a.max() - seg_a.min() > math.pi:
                seg_a[seg_a < 0] += 2 * math.pi
            pos += n
        r_ref = np.interp(s_l, br.S, br.R)
        uv[loops, 0] = a_l * r_ref
        uv[loops, 1] = s_l
    # cylindrical coords are in studs: a good face has UV area ~ its 3D area. Degenerate (end caps, crotch
    # saddles) or stretched faces would make average_islands_scale blow their islands up -> send them to Smart UV.
    a3 = np.empty(nF, np.float32)
    me.polygons.foreach_get("area", a3)
    bad = 0
    for f in np.nonzero(side)[0]:
        lo_ = lstart[f]
        P2 = uv[lo_:lo_ + ltot[f]]
        x, y = P2[:, 0], P2[:, 1]
        a2 = 0.5 * abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))
        ext = np.ptp(P2, axis=0).max()
        if not (0.33 < a2 / max(a3[f], 1e-9) < 3.0) or ext > 6.0 * math.sqrt(max(a3[f], 1e-9)):
            side[f] = False
            bad += 1
    uvl = me.uv_layers.new(name="UVMap") if not me.uv_layers else me.uv_layers[0]
    uvl.data.foreach_set("uv", uv.astype(np.float32).ravel())
    # the rest: Smart UV on those faces only
    sel = ~side
    me.polygons.foreach_set("select", sel)
    only(ob)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.context.tool_settings.mesh_select_mode = (False, False, True)
    if sel.any():
        bpy.ops.uv.smart_project(angle_limit=math.radians(66), island_margin=margin)
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.select_all(action="SELECT")
    bpy.ops.uv.average_islands_scale()
    bpy.ops.object.mode_set(mode="OBJECT")
    # the flat ground cut under the trunk / roots is never seen: give it almost no texels
    hidden = (Nf[:, 2] < -0.85) & (C[:, 2] < -0.1)
    if hidden.any():
        uvd = np.empty(len(me.loops) * 2, np.float32)
        me.uv_layers[0].data.foreach_get("uv", uvd)
        uvd = uvd.reshape(-1, 2)
        loops = np.concatenate([np.arange(lstart[f], lstart[f] + ltot[f]) for f in np.nonzero(hidden)[0]])
        uvd[loops] *= 0.06
        me.uv_layers[0].data.foreach_set("uv", uvd.ravel())
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.select_all(action="SELECT")
    bpy.ops.uv.pack_islands(rotate=True, rotate_method="ANY", margin_method="FRACTION", margin=margin,
                            shape_method="CONCAVE")
    bpy.ops.object.mode_set(mode="OBJECT")
    return dict(side_faces=int(side.sum()), misc_faces=int(sel.sum()), hidden_faces=int(hidden.sum()), bad_faces=bad)


def pack_uv(ob, margin=0.004, rotate=True):
    only(ob)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.select_all(action="SELECT")
    bpy.ops.uv.average_islands_scale()
    bpy.ops.uv.pack_islands(rotate=rotate, margin_method="FRACTION", margin=margin)
    bpy.ops.object.mode_set(mode="OBJECT")


def uv_usage(ob, size=256):
    """fraction of the UV square covered (rough raster of triangle bounding boxes is too coarse: rasterise)."""
    img = np.zeros((size, size), bool)
    uvl = ob.data.uv_layers.active.data
    for p in ob.data.polygons:
        uv = np.array([uvl[li].uv for li in p.loop_indices]) * size
        for k in range(1, len(uv) - 1):
            tri = np.array([uv[0], uv[k], uv[k + 1]])
            x0, y0 = np.floor(tri.min(0)).astype(int)
            x1, y1 = np.ceil(tri.max(0)).astype(int)
            x0, y0 = max(0, x0), max(0, y0)
            x1, y1 = min(size, x1), min(size, y1)
            if x1 <= x0 or y1 <= y0:
                continue
            xs, ys = np.meshgrid(np.arange(x0, x1) + 0.5, np.arange(y0, y1) + 0.5)
            a, b, c = tri
            d = (b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])
            if abs(d) < 1e-12:
                continue
            l1 = ((b[1] - c[1]) * (xs - c[0]) + (c[0] - b[0]) * (ys - c[1])) / d
            l2 = ((c[1] - a[1]) * (xs - c[0]) + (a[0] - c[0]) * (ys - c[1])) / d
            inside = (l1 >= 0) & (l2 >= 0) & (l1 + l2 <= 1)
            img[y0:y1, x0:x1] |= inside
    return float(img.mean())


def tris_of(ob):
    return sum(len(p.vertices) - 2 for p in ob.data.polygons)


def bbox_of(objs):
    vs = np.concatenate([np.array([o.matrix_world @ v.co for v in o.data.vertices]) for o in objs])
    return vs.min(0), vs.max(0)


# ================================================================== hi material with micro bark bump
def mat_bark_hi(name, bump=0.35, scale=22.0):
    m = mat_vc(name)
    nt = m.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = scale
    nz.inputs["Detail"].default_value = 6.0
    nz.inputs["Roughness"].default_value = 0.6
    nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
    vo = nt.nodes.new("ShaderNodeTexVoronoi")
    vo.feature = "DISTANCE_TO_EDGE"
    vo.inputs["Scale"].default_value = scale * 0.45
    nt.links.new(tc.outputs["Object"], vo.inputs["Vector"])
    mth = nt.nodes.new("ShaderNodeMath")
    mth.operation = "MULTIPLY_ADD"
    nt.links.new(vo.outputs["Distance"], mth.inputs[0])
    mth.inputs[1].default_value = 2.5
    nt.links.new(nz.outputs["Fac"], mth.inputs[2])
    bp = nt.nodes.new("ShaderNodeBump")
    bp.inputs["Strength"].default_value = bump
    bp.inputs["Distance"].default_value = 0.02
    nt.links.new(mth.outputs["Value"], bp.inputs["Height"])
    nt.links.new(bp.outputs["Normal"], bsdf.inputs["Normal"])
    return m


# ================================================================== bakes
def clean_mesh(ob, min_faces=60, hole_edges=16, closed=False):
    """delete loose bits (fewer than min_faces faces) and fill small holes (boundary loops of <= hole_edges edges).
    closed=True: the mesh should be watertight (a fresh level-set / decimated mesh), so every opening is a defect."""
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    # decimation pinches: an edge shared by > 2 faces. Cut out a small disc of faces round each one (and round any
    # opening, on a mesh that should be closed) and cap the hole; widen the disc until it closes cleanly.
    n_pinch = 0
    for it in range(6):
        cen = [(e.verts[0].co + e.verts[1].co) * 0.5 for e in bm.edges if len(e.link_faces) > 2]
        if closed:
            cen += [(e.verts[0].co + e.verts[1].co) * 0.5 for e in bm.edges if e.is_boundary]
        if not cen:
            break
        if it > 0 or any(len(e.link_faces) > 2 for e in bm.edges):
            rad = 0.08 * (it + 1)
            kill = [f for f in bm.faces if any((f.calc_center_median() - c).length < rad for c in cen)]
            n_pinch += len(kill)
            bmesh.ops.delete(bm, geom=kill, context="FACES")
            bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context="VERTS")
        rim = [e for e in bm.edges if e.is_boundary
               and (closed or any(((e.verts[0].co + e.verts[1].co) * 0.5 - c).length < 0.08 * (it + 1) + 0.25
                                  for c in cen))]
        if rim:
            r = bmesh.ops.holes_fill(bm, edges=rim, sides=max(80, hole_edges))
            if r["faces"]:
                bmesh.ops.triangulate(bm, faces=r["faces"])
    bm.faces.ensure_lookup_table()
    bm.faces.index_update()
    seen = np.zeros(len(bm.faces), bool)
    small = []
    for f in bm.faces:
        if seen[f.index]:
            continue
        comp, stack = [], [f]
        seen[f.index] = True
        while stack:
            g = stack.pop()
            comp.append(g)
            for e in g.edges:
                for h in e.link_faces:
                    if not seen[h.index]:
                        seen[h.index] = True
                        stack.append(h)
        if len(comp) < min_faces:
            small.extend(comp)
    n_small = len(small)
    if small:
        bmesh.ops.delete(bm, geom=small, context="FACES")
    loose_v = [v for v in bm.verts if not v.link_faces]
    if loose_v:
        bmesh.ops.delete(bm, geom=loose_v, context="VERTS")
    bnd = [e for e in bm.edges if e.is_boundary]
    filled = 0
    if bnd and hole_edges > 0:
        r = bmesh.ops.holes_fill(bm, edges=bnd, sides=hole_edges)
        filled = len(r["faces"])
        if r["faces"]:
            bmesh.ops.triangulate(bm, faces=r["faces"])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    bm.to_mesh(ob.data)
    bm.free()
    for p in ob.data.polygons:
        p.use_smooth = True
    return dict(removed_faces=n_small, filled_faces=filled, pinch_faces=n_pinch)


def _bake_set_masked(lo, hi_list, size, prefix, cage, maxray, ao_strength, ao_dist, outdir, buried_attr=None):
    """hkit.bake_set (copied: the kit is read-only) + an extra mask: hi points flagged in the colour attribute
    `buried_attr` (bark buried inside the parent branch) are treated like ray misses, i.e. their colour, roughness
    and AO are grown in from the visible bark around them and their normal is flat. Without it the dark, occluded
    buried base of a branch tube showed as pale bands with black notches where the low tube pokes out."""
    sc = bpy.context.scene
    os.makedirs(outdir, exist_ok=True)
    imgs = {}
    for key, cs in (("albedo", "sRGB"), ("normal", "Non-Color"), ("rough", "Non-Color"), ("ao", "Non-Color")):
        img = bpy.data.images.new(prefix + "_" + key, size, size, alpha=False)
        img.colorspace_settings.name = cs
        imgs[key] = img
    mat = bpy.data.materials.new(prefix + "_bake")
    mat.use_nodes = True
    nt = mat.node_tree
    tex = nt.nodes.new("ShaderNodeTexImage")
    lo.data.materials.clear()
    lo.data.materials.append(mat)
    sc.world.light_settings.distance = ao_dist
    for o in sc.objects:
        o.select_set(False)
    for h in hi_list:
        h.hide_render = False
        h.select_set(True)
    lo.select_set(True)
    bpy.context.view_layer.objects.active = lo

    def run(kind, img, **kw):
        tex.image = img
        nt.nodes.active = tex
        bpy.ops.object.bake(type=kind, use_selected_to_active=True, cage_extrusion=cage,
                            max_ray_distance=maxray, margin=6, **kw)

    run("NORMAL", imgs["normal"], normal_space="TANGENT")
    run("AO", imgs["ao"])
    run("DIFFUSE", imgs["albedo"], pass_filter={"COLOR"})
    run("ROUGHNESS", imgs["rough"])

    def emit_pass(name, attr):
        """bake EMIT with the Principled emission = white (attr None) or = the colour attribute attr."""
        m_img = bpy.data.images.new(prefix + "_" + name, size, size, alpha=False)
        m_img.colorspace_settings.name = "Non-Color"
        saved, added = [], []
        for h in hi_list:
            for m in h.data.materials:
                if not (m and m.use_nodes):
                    continue
                mt = m.node_tree
                for n in mt.nodes:
                    if n.type != "BSDF_PRINCIPLED":
                        continue
                    ls = [l for l in mt.links if l.to_socket == n.inputs["Emission Color"]]
                    saved.append((m, n, tuple(n.inputs["Emission Color"].default_value),
                                  n.inputs["Emission Strength"].default_value,
                                  [(l.from_socket, l.to_socket) for l in ls]))
                    for l in ls:
                        mt.links.remove(l)
                    n.inputs["Emission Strength"].default_value = 1.0
                    if attr is None:
                        n.inputs["Emission Color"].default_value = (1, 1, 1, 1)
                    elif h.data.color_attributes.get(attr) is not None:
                        vc = mt.nodes.new("ShaderNodeVertexColor")
                        vc.layer_name = attr
                        mt.links.new(vc.outputs["Color"], n.inputs["Emission Color"])
                        added.append((mt, vc))
                    else:
                        n.inputs["Emission Color"].default_value = (0, 0, 0, 1)
        run("EMIT", m_img)
        for mt, vc in added:
            mt.nodes.remove(vc)
        for m, n, col, st, ls in saved:
            n.inputs["Emission Color"].default_value = col
            n.inputs["Emission Strength"].default_value = st
            for a_, b_ in ls:
                m.node_tree.links.new(a_, b_)
        arr = np.array(m_img.pixels[:], dtype=np.float32).reshape(size, size, 4)[..., 0]
        bpy.data.images.remove(m_img)
        return arr

    hit = emit_pass("mask", None) > 0.5
    buried_frac = 0.0
    if buried_attr:
        bur = emit_pass("buried", buried_attr) > 0.5
        buried_frac = float((bur & hit).mean())
        hit &= ~bur
    shp = (size, size, 4)
    nrm = np.array(imgs["normal"].pixels[:], dtype=np.float32).reshape(shp)
    nrm[~hit] = (0.5, 0.5, 1.0, 1.0)
    imgs["normal"].pixels[:] = nrm.ravel()
    ao = np.array(imgs["ao"].pixels[:], dtype=np.float32).reshape(shp)
    ao = fill_misses(ao, hit, iters=48)
    imgs["ao"].pixels[:] = ao.ravel()
    for key in ("albedo", "rough"):
        arr = fill_misses(np.array(imgs[key].pixels[:], dtype=np.float32).reshape(shp), hit, iters=48)
        imgs[key].pixels[:] = arr.ravel()
    a_ = np.array(imgs["albedo"].pixels[:], dtype=np.float32).reshape(-1, 4)
    o_ = ao.reshape(-1, 4)
    a_[:, :3] *= (1 - ao_strength) + ao_strength * o_[:, :1]
    imgs["albedo"].pixels[:] = a_.ravel()
    imgs["miss_fraction"] = float(1 - hit.mean())
    imgs["buried_fraction"] = buried_frac
    for key in ("albedo", "normal", "rough", "ao"):
        save_png(imgs[key], os.path.join(outdir, f"{prefix}_{key}.png"))
    return imgs


def bake_part(lo, his, size, prefix, cage, maxray, ao_strength, ao_dist, all_lows, samples=24, buried_attr=None):
    """bake with the OTHER game meshes hidden from render (they must not occlude the AO / be hit) and every game
    mesh invisible to secondary rays (no self-occlusion in the AO)."""
    sc = bpy.context.scene
    sc.cycles.samples = samples
    saved = []
    for o in all_lows:
        saved.append((o, o.hide_render))
        for attr in ("visible_shadow", "visible_diffuse", "visible_glossy", "visible_transmission"):
            setattr(o, attr, False)
        if o is not lo:
            o.hide_render = True
    lo.hide_render = False
    imgs = _bake_set_masked(lo, his, size, prefix, cage, maxray, ao_strength, ao_dist, MAPS, buried_attr)
    for o, hr in saved:
        o.hide_render = hr
    return imgs


# ================================================================== webs
def catenary(a, b, n, sag, down=Vector((0, 0, -1)), side=None):
    out = []
    for i in range(n + 1):
        t = i / n
        s = 4 * t * (1 - t)
        p = a.lerp(b, t) + down * sag * s
        if side is not None:
            p += side * s
        out.append(p)
    return out


class Strands:
    def __init__(self):
        self.acc = MeshAcc()
        self.uvfn = None

    def tube(self, pts, r, sides=3):
        pts = [Vector(p) for p in pts]
        n = len(pts)
        if n < 2:
            return
        T = []
        for i in range(n):
            t = pts[min(n - 1, i + 1)] - pts[max(0, i - 1)]
            T.append(t.normalized() if t.length > 1e-9 else Vector((1, 0, 0)))
        ref = Vector((0, 0, 1)) if abs(T[0].z) < 0.9 else Vector((1, 0, 0))
        N = (ref - T[0] * ref.dot(T[0])).normalized()
        rows = []
        for i in range(n):
            N = N - T[i] * N.dot(T[i])
            if N.length < 1e-6:
                N = ref - T[i] * ref.dot(T[i])
            N.normalize()
            B = T[i].cross(N)
            rr = r[i] if isinstance(r, (list, tuple)) else r
            rows.append([pts[i] + (N * math.cos(2 * math.pi * j / sides) + B * math.sin(2 * math.pi * j / sides)) * rr
                         for j in range(sides)])
        flat = [p for row in rows for p in row]
        i0 = self.acc.add_verts([tuple(p) for p in flat])
        for i in range(n - 1):
            for j in range(sides):
                k = (j + 1) % sides
                self.acc.face((i0 + i * sides + j, i0 + i * sides + k, i0 + (i + 1) * sides + k,
                               i0 + (i + 1) * sides + j))

    def blob(self, c, rx, ry, rz, nu=7, nv=5):
        c = Vector(c)
        verts = [c + Vector((0, 0, rz))]
        for i in range(1, nv):
            th = math.pi * i / nv
            for j in range(nu):
                a = 2 * math.pi * j / nu
                k = 1 + 0.12 * math.sin(3 * a + i)
                verts.append(c + Vector((rx * math.sin(th) * math.cos(a) * k, ry * math.sin(th) * math.sin(a) * k,
                                         rz * math.cos(th))))
        verts.append(c - Vector((0, 0, rz)))
        i0 = self.acc.add_verts([tuple(v) for v in verts])
        top, bot = i0, i0 + len(verts) - 1
        for j in range(nu):
            k = (j + 1) % nu
            self.acc.face((top, i0 + 1 + k, i0 + 1 + j))
            for i in range(nv - 2):
                a0 = i0 + 1 + i * nu
                a1 = i0 + 1 + (i + 1) * nu
                self.acc.face((a0 + j, a0 + k, a1 + k, a1 + j))
            a0 = i0 + 1 + (nv - 2) * nu
            self.acc.face((a0 + j, a0 + k, bot))


def hanging(p0, d0, length, n, rng):
    pts = [Vector(p0)]
    d = Vector(d0).normalized()
    d.z = min(d.z, -0.3)
    d.normalize()
    seg = length / n
    for _ in range(n):
        d = (d.lerp(Vector((0, 0, -1)), 0.45) + Vector((rng.uniform(-0.1, 0.1), rng.uniform(-0.1, 0.1), 0))).normalized()
        pts.append(pts[-1] + d * seg)
    return pts


def poly_hit(o, d, poly):
    """ray (2D) vs closed polyline -> (t, segment index, u)."""
    best = None
    n = len(poly)
    for i in range(n):
        p, q = poly[i], poly[(i + 1) % n]
        e = (q[0] - p[0], q[1] - p[1])
        den = d[0] * e[1] - d[1] * e[0]
        if abs(den) < 1e-12:
            continue
        w = (p[0] - o[0], p[1] - o[1])
        t = (w[0] * e[1] - w[1] * e[0]) / den
        u = (w[0] * d[1] - w[1] * d[0]) / den
        if t > 1e-6 and -1e-6 <= u <= 1 + 1e-6 and (best is None or t < best[0]):
            best = (t, i, u)
    return best


def build_web(S, frame3, hub_frac, radials, rings, rng, r_frame=0.066, r_rad=0.056, r_spi=0.046, broken=0.08,
              loose=3, bow=0.22):
    """Orb web in the plane of the fork: the frame polygon (frame3, points on / along the branches) is projected onto
    its best-fit plane, spokes run from the hub to that planar frame, catch rings are polygons between the spokes
    (sagging a little toward the hub), short anchor threads tie the planar frame back to the real branch surface.
    The whole web bellies out of its plane (bow) and sags slightly. Returns info (hub, normal, anchors)."""
    c = sum(frame3, Vector()) / len(frame3)
    A = np.array([tuple(p - c) for p in frame3])
    _, _, vt = np.linalg.svd(A)
    nrm = Vector(vt[2]).normalized()
    e1 = Vector(vt[0]).normalized()
    e2 = nrm.cross(e1).normalized()
    proj = [p - nrm * (p - c).dot(nrm) for p in frame3]
    to2 = lambda p: ((p - c).dot(e1), (p - c).dot(e2))
    poly2 = [to2(p) for p in proj]
    # hub: area centroid of the planar frame, pulled toward the crotch
    ax = sum(p[0] for p in poly2) / len(poly2)
    ay = sum(p[1] for p in poly2) / len(poly2)
    f0 = poly2[0]
    hx, hy = ax + (f0[0] - ax) * hub_frac, ay + (f0[1] - ay) * hub_frac
    hub = c + e1 * hx + e2 * hy
    Rmax = max(math.hypot(p[0] - hx, p[1] - hy) for p in poly2)

    def lift(p):
        q = p - c
        rr = math.hypot(q.dot(e1) - hx, q.dot(e2) - hy) / Rmax
        return p + nrm * bow * max(0.0, 1 - rr * rr) + Vector((0, 0, -0.06 * rr))

    ends = []
    a0 = rng.uniform(0, 2 * math.pi)
    for i in range(radials):
        th = a0 + 2 * math.pi * i / radials + rng.uniform(-0.1, 0.1)
        hit = poly_hit((hx, hy), (math.cos(th), math.sin(th)), poly2)
        if hit is None:
            continue
        t, si, u = hit
        p = proj[si].lerp(proj[(si + 1) % len(proj)], u)
        ends.append((th, p, t))
    ends.sort(key=lambda e: e[0])
    for th, p, L in ends:
        n = max(4, int(L / 0.3))
        pts = [lift(hub.lerp(p, k / n)) for k in range(n + 1)]
        S.tube(pts, r_rad, 4)
    for k in range(rings):
        f = 0.14 + 0.8 * (k / max(1, rings - 1)) ** 1.05
        row = []
        for th, p, L in ends:
            ff = min(0.97, f * (1 + 0.035 * rng.uniform(-1, 1)))
            row.append(lift(hub.lerp(p, ff)))
        for i in range(len(row)):
            a, b = row[i], row[(i + 1) % len(row)]
            span_ang = (ends[(i + 1) % len(ends)][0] - ends[i][0]) % (2 * math.pi)
            if span_ang > math.radians(75):
                continue                       # never bridge a gap where no spoke reached the frame
            if rng.random() < broken * (0.4 + f):
                if rng.random() < 0.6:
                    S.tube(hanging(a, b - a, rng.uniform(0.35, 0.8), 4, rng), r_spi * 0.85, 3)
                continue
            mid_to_hub = hub - (a + b) * 0.5
            span = (b - a).length
            pts = catenary(a, b, 2, 0.04 * span, side=mid_to_hub.normalized() * 0.07 * span)
            S.tube(pts, r_spi, 3)
    # the planar frame thread + anchor threads back to the bark
    S.tube([lift(p) for p in proj] + [lift(proj[0])], r_frame, 4)
    for i in range(0, len(frame3), 2):
        if (frame3[i] - proj[i]).length > 0.04:
            S.tube([lift(proj[i]), frame3[i]], r_frame * 0.8, 3)
    for _ in range(loose):
        p = lift(rng.choice(proj[len(proj) // 3:]))
        S.tube(hanging(p, Vector((rng.uniform(-0.3, 0.3), rng.uniform(-0.3, 0.3), -1)), rng.uniform(0.8, 1.8), 7,
                       rng), 0.034, 3)
    S.blob(lift(hub), 0.15, 0.15, 0.15, 7, 4)
    return dict(hub=tuple(lift(hub)), normal=tuple(nrm), centre=tuple(c), radius=round(Rmax, 2),
                spokes=len(ends), lift=lift)


def two_sided_sheet(acc, grid, uvgrid, keep):
    rows, cols = len(grid), len(grid[0])
    used = set()
    for i, j in keep:
        used |= {(i, j), (i + 1, j), (i, j + 1), (i + 1, j + 1)}
    front, back = {}, {}
    order = sorted(used)
    i0 = acc.add_verts([tuple(grid[i][j]) for i, j in order])
    for n, ij in enumerate(order):
        front[ij] = i0 + n
    i1 = acc.add_verts([tuple(grid[i][j]) for i, j in order])
    for n, ij in enumerate(order):
        back[ij] = i1 + n
    for i, j in keep:
        q = [(i, j), (i, j + 1), (i + 1, j + 1), (i + 1, j)]
        acc.face([front[x] for x in q], [uvgrid[x[0]][x[1]] for x in q])
        acc.face([back[x] for x in reversed(q)], [uvgrid[x[0]][x[1]] for x in reversed(q)])


def silk_texture(size, n_islands, seed, path):
    """RGBA gauze atlas (2x2 islands): fibre tangle + film with torn holes + dust, frayed toward the free edges
    (island v=1 edge = attached side)."""
    rng = np.random.default_rng(seed)
    n = size // 2
    atlas = np.zeros((size, size, 4), np.float32)
    uu = (np.arange(n) + 0.5) / n
    U, Vv = np.meshgrid(uu, uu)
    pn = PN(seed)
    for isl in range(n_islands):
        fib = np.zeros((n, n), np.float32)
        for f in range(420):
            ang = rng.uniform(0, math.pi) if rng.random() < 0.6 else math.pi / 2 + rng.normal(0, 0.3)
            L = rng.uniform(25, 170)
            steps = int(L / 0.5)
            x, y = rng.uniform(0, n), rng.uniform(0, n)
            wgt = rng.uniform(0.35, 0.85)
            xs = np.empty(steps)
            ys = np.empty(steps)
            for st in range(steps):
                ang += rng.normal(0, 0.03)
                x += 0.5 * math.cos(ang)
                y += 0.5 * math.sin(ang)
                xs[st], ys[st] = x, y
            ok = (xs >= 0) & (xs < n - 1) & (ys >= 0) & (ys < n - 1)
            xs, ys = xs[ok], ys[ok]
            if not len(xs):
                continue
            x0, y0 = np.floor(xs).astype(int), np.floor(ys).astype(int)
            fx, fy = xs - x0, ys - y0
            for dx, dy, ww in ((0, 0, (1 - fx) * (1 - fy)), (1, 0, fx * (1 - fy)), (0, 1, (1 - fx) * fy),
                               (1, 1, fx * fy)):
                np.add.at(fib, (y0 + dy, x0 + dx), ww * wgt)
        fib = np.clip(fib, 0, 1)
        sd = isl * 17.3
        film = 0.05 + 0.32 * (pn.fbm(U * 3 + sd, Vv * 1.5, sd, 4) * 0.5 + 0.5)
        holes = pn.fbm(U * 3.6 + sd + 9, Vv * 3.6, sd + 3, 3) * 0.5 + 0.5
        keep = np.clip((0.56 - holes) / 0.06, 0, 1)
        film = film * keep
        fib = fib * (0.4 + 0.6 * keep)
        alpha = 1 - (1 - film) * (1 - fib)
        rag = pn.fbm(U * 7 + sd, Vv * 7, sd + 5, 3) * 0.5 + 0.5
        if isl == 3:
            # dense hub patch: the web's centre mat, fading out radially with a ragged rim
            rad = np.sqrt((U - 0.5) ** 2 + (Vv - 0.5) ** 2) * 2
            edge = np.clip((0.95 - rad - 0.15 * rag) / 0.45, 0, 1)
            film = np.maximum(film, 0.45 * np.clip(1 - rad / 0.7, 0, 1))
            alpha = 1 - (1 - film) * (1 - fib)
        else:
            edge = np.clip(np.minimum(U, 1 - U) / 0.12, 0, 1) * np.clip((Vv - 0.08 * rag) / 0.35, 0, 1)
        alpha = np.clip(alpha * edge * 1.2, 0, 1)
        dust = np.clip((pn.fbm(U * 4.5 + sd, Vv * 4.5, sd + 7, 4) * 0.5 + 0.5 - 0.45) * 2.2, 0, 1) * 0.6
        silk = np.array([228, 225, 218]) / 255.0
        dustc = np.array([150, 140, 122]) / 255.0
        bright = np.array([250, 249, 246]) / 255.0
        col = silk[None, None] * (1 - dust[..., None]) + dustc[None, None] * dust[..., None]
        col = col * (1 - 0.5 * fib[..., None]) + bright[None, None] * 0.5 * fib[..., None]
        oy, ox = (isl // 2) * n, (isl % 2) * n
        atlas[oy:oy + n, ox:ox + n, :3] = col
        atlas[oy:oy + n, ox:ox + n, 3] = alpha
    img = bpy.data.images.new(os.path.basename(path)[:-4], size, size, alpha=True)
    img.colorspace_settings.name = "sRGB"
    img.pixels.foreach_set(atlas.ravel())
    img.filepath_raw = path
    img.file_format = "PNG"
    img.save()
    img.alpha_mode = "STRAIGHT"
    return img


def strand_texture(size, seed, path):
    rng = np.random.default_rng(seed)
    pn = PN(seed)
    u = (np.arange(size) + 0.5) / size
    U, Vv = np.meshgrid(u, u)
    dm = np.clip((pn.fbm(U * 4, Vv * 4, 0.5, 4) * 0.5 + 0.5 - 0.42) * 2.0, 0, 1) * 0.7
    hi = np.clip((pn.fbm(U * 9 + 4, Vv * 9, 2.5, 3) * 0.5 + 0.5 - 0.55) * 3, 0, 1) * (1 - dm)
    base = np.array([238, 240, 244]) / 255.0
    dust = np.array([176, 168, 156]) / 255.0
    bright = np.array([250, 251, 255]) / 255.0
    col = base * (1 - dm[..., None]) + dust * dm[..., None]
    col = col * (1 - 0.35 * hi[..., None]) + bright * 0.35 * hi[..., None]
    arr = np.ones((size, size, 4), np.float32)
    arr[..., :3] = col
    img = bpy.data.images.new(os.path.basename(path)[:-4], size, size, alpha=False)
    img.pixels.foreach_set(arr.ravel())
    img.filepath_raw = path
    img.file_format = "PNG"
    img.save()
    return img


def mat_img(name, img, alpha=False, rough=0.6, rough_img=None):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    t = nt.nodes.new("ShaderNodeTexImage")
    t.image = img
    nt.links.new(t.outputs["Color"], b.inputs["Base Color"])
    if alpha:
        nt.links.new(t.outputs["Alpha"], b.inputs["Alpha"])
        try:
            m.surface_render_method = "DITHERED"
        except Exception:
            pass
    b.inputs["Roughness"].default_value = rough
    if rough_img is not None:
        tr = nt.nodes.new("ShaderNodeTexImage")
        tr.image = rough_img
        nt.links.new(tr.outputs["Color"], b.inputs["Roughness"])
    b.inputs["Metallic"].default_value = 0.0
    return m


# ================================================================== review
def shoot_fov(path, loc, target, vfov=70.0, lens=None, res=None):
    sc = bpy.context.scene
    if res:
        sc.render.resolution_x, sc.render.resolution_y = res
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


def garden_set(bed_r=7.0):
    """green lawn + a round soil bed (the hub's garden beds) + sunny key light."""
    g = mat_noise("Lawn", lin((96, 168, 64)), lin((70, 138, 48)), nscale=0.35, detail=6, rough=0.9, lo=0.3, hi=0.7,
                  bump=0.15)
    bpy.ops.mesh.primitive_plane_add(size=300, location=(0, 0, -0.02))
    bpy.context.active_object.data.materials.append(g)
    s = mat_noise("Soil", lin((96, 70, 50)), lin((70, 50, 36)), nscale=2.5, detail=6, rough=0.95, lo=0.3, hi=0.7,
                  bump=0.4)
    bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=bed_r, depth=0.2, location=(0, 0, -0.08))
    bpy.context.active_object.data.materials.append(s)
