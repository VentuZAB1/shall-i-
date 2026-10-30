# SLINGSHOT Halloween - VineGrip: giant pumpkin-vine "fingers" gripping the top of the hub's back wall, as if the
# giant jack-o'-lantern behind the wall is holding on and peeking over.
# Headless:  blender.exe -b --factory-startup --python vines.py -- build preview | bake | render | export
#
# FRAME (Blender, studs): the wall's top INNER edge runs along X at y = 0, z = 0. The wall body is y in [-6, 0],
# z in [-25, 0] (top surface z = 0, hub floor z = -25). The giant head is behind it (-Y). Players are on +Y.
# Both game meshes keep their origin at the frame origin (0, 0, 0).
#
# Vines / tendrils / petioles = swept ridged tubes (parallel-transport frames, 5 twisting ridges, knots, taper) on
# paths that are pushed out of the wall slab (so they rest on the top and press on the inner face). Hi = 96-sided
# rings every 0.05 stud with per-vertex colour + a procedural hair/prickle bump; lo = 15/10/6-sided rings (ridge
# aligned, zippered where the count changes), tube-strip UVs in studs, packed.
# Leaves = constrained-Delaunay sheets of a 5-lobed serrated outline (lo samples the tooth tips/notches exactly),
# shaped by cup / fold / pleats / waves / droop / curl, pushed off the wall and the vines; hi has sunken veins and
# per-vertex autumn colour + a tertiary-vein bump. Lo leaves = top sheet (baked) + a flipped copy as the underside.
import sys, os, json, time, itertools
sys.path.insert(0, r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween")
from hkit import *  # noqa
from mathutils import Vector, Matrix, kdtree, geometry, noise
import numpy as np

OUT = os.path.join(HERE, "Vines")
MAPS = os.path.join(OUT, "maps")
BLEND = os.path.join(OUT, "vines.blend")
FBX = os.path.join(CDIMP, "Halloween_VineGrip.fbx")
LOG = []
T0 = time.time()


def log(*a):
    s = "[%6.1f] " % (time.time() - T0) + " ".join(str(x) for x in a)
    LOG.append(s)
    print(s, flush=True)


# ------------------------------------------------------------------ the wall slab (infinite along X)
WY0, WY1, WZ0, WZ1 = -6.0, 0.0, -25.0, 0.0


def wall_push(p, c):
    """Return p moved so that it is at least c away from the wall slab (rounded Minkowski push)."""
    y, z = p.y, p.z
    qy = min(max(y, WY0), WY1)
    qz = min(max(z, WZ0), WZ1)
    dy, dz = y - qy, z - qz
    d = math.hypot(dy, dz)
    if d > 1e-9:
        if d < c:
            k = c / d
            return Vector((p.x, qy + dy * k, qz + dz * k))
        return p
    cands = [(WZ1 - z, 0), (WY1 - y, 1), (y - WY0, 2)]
    _, f = min(cands)
    if f == 0:
        return Vector((p.x, y, WZ1 + c))
    if f == 1:
        return Vector((p.x, WY1 + c, z))
    return Vector((p.x, WY0 - c, z))


def wall_dist(p):
    qy = min(max(p.y, WY0), WY1)
    qz = min(max(p.z, WZ0), WZ1)
    return math.hypot(p.y - qy, p.z - qz)


def limit_curvature(pts, reff, clear, k=1.3, h=6, iters=80):
    """Relax free-space bends tighter than k * tube radius (they pinch the inside of the bend inside out).
    Points resting on the wall (within clear + 0.15) are left alone: the wall push owns them."""
    n = len(pts)
    for _ in range(iters):
        hit = []
        for i in range(h, n - h):
            if wall_dist(pts[i]) < clear[i] + 0.15:
                continue
            a, b, c = pts[i - h], pts[i], pts[i + h]
            cr = (b - a).cross(c - b).length
            if cr < 1e-9:
                continue
            R = (b - a).length * (c - b).length * (c - a).length / (2 * cr)
            if R < k * reff[i]:
                hit.append(i)
        if not hit:
            break
        new = pts[:]
        for i in hit:
            for j in range(max(1, i - 3), min(n - 1, i + 4)):
                new[j] = pts[j] * 0.5 + (pts[j - 1] + pts[j + 1]) * 0.25
        pts = [wall_push(q, clear[j]) for j, q in enumerate(new)]
    return pts


# ------------------------------------------------------------------ path helpers
def cr_chain(ctrl, step=0.05):
    """Centripetal Catmull-Rom through ctrl points, sampled ~step apart."""
    P = [ctrl[0] * 2 - ctrl[1]] + list(ctrl) + [ctrl[-1] * 2 - ctrl[-2]]
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        t0 = 0.0
        t1 = t0 + max(1e-4, (p1 - p0).length ** 0.5)
        t2 = t1 + max(1e-4, (p2 - p1).length ** 0.5)
        t3 = t2 + max(1e-4, (p3 - p2).length ** 0.5)
        n = max(2, int(math.ceil((p2 - p1).length / step)))
        for k in range(n):
            t = t1 + (t2 - t1) * k / n
            a1 = p0 * ((t1 - t) / (t1 - t0)) + p1 * ((t - t0) / (t1 - t0))
            a2 = p1 * ((t2 - t) / (t2 - t1)) + p2 * ((t - t1) / (t2 - t1))
            a3 = p2 * ((t3 - t) / (t3 - t2)) + p3 * ((t - t2) / (t3 - t2))
            b1 = a1 * ((t2 - t) / (t2 - t0)) + a2 * ((t - t0) / (t2 - t0))
            b2 = a2 * ((t3 - t) / (t3 - t1)) + a3 * ((t - t1) / (t3 - t1))
            out.append(b1 * ((t2 - t) / (t2 - t1)) + b2 * ((t - t1) / (t2 - t1)))
    out.append(ctrl[-1].copy())
    return out


def bezier3(p0, p1, p2, p3, n):
    out = []
    for i in range(n + 1):
        t = i / n
        u = 1 - t
        out.append(p0 * (u * u * u) + p1 * (3 * u * u * t) + p2 * (3 * u * t * t) + p3 * (t * t * t))
    return out


def arclen(pts):
    L = [0.0]
    for i in range(1, len(pts)):
        L.append(L[-1] + (pts[i] - pts[i - 1]).length)
    return L


def resample(pts, step):
    L = arclen(pts)
    total = L[-1]
    n = max(2, int(round(total / step)))
    out, j = [], 0
    for k in range(n + 1):
        s = total * k / n
        while j < len(pts) - 2 and L[j + 1] < s:
            j += 1
        seg = L[j + 1] - L[j]
        f = 0.0 if seg < 1e-9 else (s - L[j]) / seg
        out.append(pts[j].lerp(pts[j + 1], min(1.0, max(0.0, f))))
    return out


def smooth_path(pts, iters, w=0.5, lock0=1, lock1=1):
    n = len(pts)
    for _ in range(iters):
        new = pts[:]
        for i in range(lock0, n - lock1):
            new[i] = pts[i] * (1 - w) + (pts[i - 1] + pts[i + 1]) * (0.5 * w)
        pts = new
    return pts


def transport_frames(pts):
    n = len(pts)
    T = [(pts[min(i + 1, n - 1)] - pts[max(i - 1, 0)]).normalized() for i in range(n)]
    up = Vector((0, 0, 1))
    N0 = up - T[0] * T[0].dot(up)
    if N0.length < 1e-3:
        N0 = Vector((1, 0, 0)) - T[0] * T[0].x
    N = [N0.normalized()]
    for i in range(1, n):
        q = T[i - 1].rotation_difference(T[i])
        v = q @ N[-1]
        v = (v - T[i] * T[i].dot(v)).normalized()
        N.append(v)
    B = [T[i].cross(N[i]) for i in range(n)]
    return T, N, B


def nvec(seed):
    r = random.Random(seed)
    return Vector((r.uniform(-60, 60), r.uniform(-60, 60), r.uniform(-60, 60)))


# ------------------------------------------------------------------ the tubes
COL = dict(deep=lin((20, 48, 18)), mid=lin((42, 82, 28)), light=lin((88, 126, 48)), young=lin((70, 112, 36)),
           dry=lin((158, 128, 60)), dry2=lin((112, 84, 40)), old=lin((86, 74, 40)), knot=lin((70, 60, 30)),
           scar=lin((150, 136, 92)))


def knot_val(tb, s):
    v = 0.0
    for sk, A, w in tb["knots"]:
        d = s - sk
        v += A * math.exp(-(d / w) ** 2) - 0.32 * A * math.exp(-((abs(d) - 1.45 * w) / (0.35 * w)) ** 2)
    return v


def make_tube(kind, P, R, seed, knots=(), ridges=5, amp=0.14, twist=0.11, lumps=0.05, tmain=None, dry=0.0,
              cap0=True, tip=True, name=""):
    """P: dense centreline (~0.05 spacing), R: base radius per point (taper, no knots). knots: [(s, A, w)]."""
    S = arclen(P)
    T, N, B = transport_frames(P)
    rng = random.Random(seed)
    return dict(kind=kind, P=P, R=R, S=S, T=T, N=N, B=B, knots=list(knots), ridges=ridges, amp=amp, twist=twist,
                tw0=rng.uniform(0, 6.28), lumps=lumps, off=nvec(seed), off2=nvec(seed + 7),
                tmain=tmain or S[-1], dry=dry, cap0=cap0, tip=tip, name=name)


def tw_at(tb, s):
    return tb["twist"] * s + tb["tw0"] + 0.5 * noise.noise(Vector((s * 0.07, 1.3, 2.9)) + tb["off"])


def prof(tb, i, a, hi):
    """Radius at ring i, angle a -> (radius, crest 0..1, knot value)."""
    s, r = tb["S"][i], tb["R"][i]
    k = tb["ridges"]
    tw = tw_at(tb, s)
    amp = tb["amp"] * smoothstep(0.1, 0.42, r)
    if k:
        crest = (0.5 + 0.5 * math.cos(k * (a + tw))) ** 0.42
    else:
        crest = 0.5
    m = 1.0 - amp + amp * crest
    kn = knot_val(tb, s)
    ca, sa = math.cos(a), math.sin(a)
    q = Vector((ca * 0.7, sa * 0.7, s * 0.45)) + tb["off"]
    m *= 1.0 + kn * (0.8 + 0.45 * noise.noise(q * 3.1)) + tb["lumps"] * noise.noise(q)
    if hi:
        g = smoothstep(0.1, 0.4, r)
        m *= 1.0 + (0.03 * noise.noise(Vector((ca * 9, sa * 9, s * 0.8)) + tb["off2"])
                    + 0.016 * noise.noise(Vector((ca * 21, sa * 21, s * 1.7)) + tb["off2"] * 1.3)) * g
    return r * m, crest, kn


def tube_col(tb, i, a, crest, kn):
    s = tb["S"][i]
    t = min(1.0, s / tb["tmain"])
    k = tb["ridges"]
    off = tb["off"]
    if tb["kind"] == "tendril":
        col = mix(lin((70, 112, 38)), lin((112, 140, 58)), 0.5 + 0.5 * noise.noise(Vector((s * 0.6, a, 1.0)) + off))
        col = mix(col, mix(COL["dry"], COL["dry2"], 0.4), tb["dry"] * smoothstep(0.0, 0.8, t + 0.3 * noise.noise(Vector((s * 0.4, 2, 3)) + off)))
        r = 0.55 + 0.25 * tb["dry"]
        return col, r
    tw = tw_at(tb, s)
    rid = math.floor((a + tw) * k / (2 * math.pi) + 0.5) if k else 0
    col = mix(COL["deep"], COL["mid"], crest ** 0.8)
    hl = noise.noise(Vector((rid * 4.3, s * 0.5, 3.3)) + off)
    col = mix(col, COL["light"], 0.4 * crest * smoothstep(0.0, 0.5, hl))
    st = noise.noise(Vector((rid * 2.7 + 0.31, s * 0.16, 11.0)) + off)
    st2 = noise.noise(Vector((rid * 7.9 + a * 2.0, s * 0.55, 31.0)) + off)
    streak = smoothstep(0.18, 0.46, st) * crest ** 1.2
    thin = smoothstep(0.3, 0.5, st2) * crest ** 2 * 0.7
    col = mix(col, COL["dry"], 0.8 * max(streak, thin))
    g2 = noise.noise(Vector((rid * 5.1, s * 0.9, 21.0)) + off)
    col = mix(col, COL["dry2"], 0.35 * (1 - crest) * smoothstep(0.0, 0.5, g2))
    col = mix(col, lin((10, 26, 10)), 0.55 * (1 - crest) ** 2)
    if tb["kind"] == "vine":
        col = mix(col, COL["old"], 0.65 * (1 - smoothstep(0.0, 0.32, t)))
        col = mix(col, COL["young"], 0.35 * smoothstep(0.82, 1.0, t))
    kk = min(1.0, max(0.0, kn) * 2.4)
    col = mix(col, COL["knot"], 0.75 * kk)
    patch = smoothstep(0.1, 0.5, noise.noise(Vector((math.cos(a), math.sin(a), s * 0.6)) * 1.5 + off * 0.5))
    col = mix(col, COL["dry2"], 0.45 * patch * min(1.0, kk * 2.0))
    sc = smoothstep(0.35, 0.6, noise.noise(Vector((math.cos(a) * 2, math.sin(a) * 2, s * 1.4)) + off))
    col = mix(col, COL["scar"], 0.5 * sc * kk)
    rough = 0.6 + 0.22 * max(streak, thin) + 0.1 * (1 - crest) + 0.1 * kk
    return col, rough


class MeshAcc:
    """Accumulates vertices / faces / per-loop UVs / per-vertex colour+roughness."""

    def __init__(self, want_uv=True, want_col=False):
        self.V, self.F, self.UV, self.C, self.Rg, self.Tg = [], [], [], [], [], []
        self.want_uv, self.want_col = want_uv, want_col
        self.tag = 0

    def v(self, co, col=None, rough=None):
        self.V.append(tuple(co))
        if self.want_col:
            self.C.append(col)
            self.Rg.append((rough, rough, rough))
        return len(self.V) - 1

    def f(self, idx, uvs=None):
        self.F.append(tuple(idx))
        self.Tg.append(self.tag)
        if self.want_uv:
            self.UV.extend(uvs if uvs is not None else [(0.0, 0.0)] * len(idx))

    def build(self, name, smooth=True):
        me = bpy.data.meshes.new(name)
        V = np.asarray(self.V, np.float32)
        me.vertices.add(len(V))
        me.vertices.foreach_set("co", V.ravel())
        sizes = np.array([len(f) for f in self.F], np.int32)
        loops = np.fromiter(itertools.chain.from_iterable(self.F), np.int32, int(sizes.sum()))
        starts = np.concatenate([[0], np.cumsum(sizes)[:-1]]).astype(np.int32)
        me.loops.add(len(loops))
        me.loops.foreach_set("vertex_index", loops)
        me.polygons.add(len(self.F))
        me.polygons.foreach_set("loop_start", starts)
        me.update(calc_edges=True)
        if self.want_uv:
            uvl = me.uv_layers.new(name="UVMap")
            uvl.data.foreach_set("uv", np.asarray(self.UV, np.float32).ravel())
        if self.want_col:
            set_colors(me, "Col", self.C)
            set_colors(me, "Rough", self.Rg)
        at = me.attributes.new("part", "INT", "FACE")
        at.data.foreach_set("value", np.asarray(self.Tg, np.int32))
        me.validate()
        if smooth:
            me.shade_smooth()
        return link(bpy.data.objects.new(name, me))


def tube_hi(acc, tb, m=96):
    n = len(tb["P"])
    rings = []
    for i in range(n):
        ring = []
        for j in range(m):
            a = 2 * math.pi * j / m
            rr, crest, kn = prof(tb, i, a, True)
            col, rough = tube_col(tb, i, a, crest, kn)
            p = tb["P"][i] + (tb["N"][i] * math.cos(a) + tb["B"][i] * math.sin(a)) * rr
            ring.append(acc.v(p, col, rough))
        rings.append(ring)
    for i in range(n - 1):
        A, Bq = rings[i], rings[i + 1]
        for j in range(m):
            jj = (j + 1) % m
            acc.f((A[j], A[jj], Bq[jj], Bq[j]))
    if tb["cap0"]:
        c = acc.v(tb["P"][0] - tb["T"][0] * tb["R"][0] * 0.3, *tube_col(tb, 0, 0.0, 0.5, 0.0))
        for j in range(m):
            acc.f((c, rings[0][(j + 1) % m], rings[0][j]))
    e = n - 1
    tipd = 0.55 if tb["tip"] else 0.25
    c = acc.v(tb["P"][e] + tb["T"][e] * tb["R"][e] * tipd, *tube_col(tb, e, 0.0, 0.5, 0.0))
    for j in range(m):
        acc.f((c, rings[e][j], rings[e][(j + 1) % m]))


def lo_count(tb, r):
    if tb["ridges"] == 5:
        if r >= 0.5:
            return 15
        if r >= 0.23:
            return 10
        return 6
    return tb.get("m_lo", 6)


def pick_rings(tb, seg_k=0.8, seg_min=0.2, seg_max=0.85, ang=14.0):
    n = len(tb["P"])
    S, R, T = tb["S"], tb["R"], tb["T"]
    sel = [0]
    for i in range(1, n - 1):
        j = sel[-1]
        ds = S[i] - S[j]
        lim = min(seg_max, max(seg_min, seg_k * R[i]))
        angl = ang
        if tb["P"][i].y < WY0 - 0.6 and tb["P"][i].z < -0.8:   # hidden behind the wall
            lim, angl = 1.4, 24.0
        turn = math.degrees(T[j].angle(T[i], 0.0))
        dk = abs(knot_val(tb, S[i]) - knot_val(tb, S[j]))
        if ds >= lim or turn >= angl or dk > 0.07 or lo_count(tb, R[i]) != lo_count(tb, R[j]):
            if S[n - 1] - S[i] > 0.6 * lim:
                sel.append(i)
    sel.append(n - 1)
    return sel


def tube_lo(acc, tb, chunk=9.0, **pk):
    sel = pick_rings(tb, **pk)
    rings = []  # (vert idx list, m, s, circumference)
    for i in sel:
        m = lo_count(tb, tb["R"][i])
        tw = tw_at(tb, tb["S"][i]) if tb["ridges"] else 0.0
        ids = []
        for j in range(m):
            a = 2 * math.pi * j / m - tw
            rr, _, _ = prof(tb, i, a, False)
            ids.append(acc.v(tb["P"][i] + (tb["N"][i] * math.cos(a) + tb["B"][i] * math.sin(a)) * rr))
        circ = 2 * math.pi * tb["R"][i] * (1 + max(0.0, knot_val(tb, tb["S"][i])))
        rings.append((ids, m, tb["S"][i], circ))
    hidden = [tb["P"][i].y < WY0 - 0.6 and tb["P"][i].z < -0.8 for i in sel]
    s0 = rings[0][2]
    for q in range(len(rings) - 1):
        A, Bq = rings[q], rings[q + 1]
        k = 0.4 if hidden[q] else 1.0
        uva = lambda f, R_=A, k=k: ((f - 0.5) * R_[3] * k, (R_[2] - s0) * k)
        uvb = lambda f, R_=Bq, k=k: ((f - 0.5) * R_[3] * k, (R_[2] - s0) * k)
        ia = [(A[0][j % A[1]], j / A[1]) for j in range(A[1] + 1)]
        ib = [(Bq[0][j % Bq[1]], j / Bq[1]) for j in range(Bq[1] + 1)]
        if A[1] == Bq[1]:
            for j in range(A[1]):
                acc.f((ia[j][0], ia[j + 1][0], ib[j + 1][0], ib[j][0]),
                      [uva(ia[j][1]), uva(ia[j + 1][1]), uvb(ib[j + 1][1]), uvb(ib[j][1])])
        else:
            x = y = 0
            while x < A[1] or y < Bq[1]:
                if x < A[1] and (y >= Bq[1] or ia[x + 1][1] <= ib[y + 1][1]):
                    acc.f((ia[x][0], ia[x + 1][0], ib[y][0]), [uva(ia[x][1]), uva(ia[x + 1][1]), uvb(ib[y][1])])
                    x += 1
                else:
                    acc.f((ia[x][0], ib[y + 1][0], ib[y][0]), [uva(ia[x][1]), uvb(ib[y + 1][1]), uvb(ib[y][1])])
                    y += 1
        if Bq[2] - s0 > chunk or (q + 1 < len(hidden) and hidden[q + 1] != hidden[q]):
            s0 = Bq[2]
    # caps (own little islands)
    if tb["cap0"]:
        ids, m, s, circ = rings[0]
        c = acc.v(tb["P"][0] - tb["T"][0] * tb["R"][0] * 0.3)
        r0 = tb["R"][0]
        cu = lambda j: (math.cos(2 * math.pi * j / m) * r0, math.sin(2 * math.pi * j / m) * r0)
        for j in range(m):
            acc.f((c, ids[(j + 1) % m], ids[j]), [(0.0, 0.0), cu(j + 1), cu(j)])
    ids, m, s, circ = rings[-1]
    e = len(tb["P"]) - 1
    tipd = 0.55 if tb["tip"] else 0.25
    c = acc.v(tb["P"][e] + tb["T"][e] * tb["R"][e] * tipd)
    re = max(0.05, tb["R"][e])
    cu = lambda j: (math.cos(2 * math.pi * j / m) * re * 1.3, math.sin(2 * math.pi * j / m) * re * 1.3)
    for j in range(m):
        acc.f((c, ids[j], ids[(j + 1) % m]), [(0.0, 0.0), cu(j), cu(j + 1)])
    return len(sel)


# ------------------------------------------------------------------ the 4 vine "fingers"
# ctrl: centreline control points (x, y, z); r0 = base radius; curl = side the tip spiral curls to (+1 = +X);
# knots in t (fraction of the main length) = nodes where petioles / tendrils come out.
VINES = [
    # behind the wall -> over the back edge -> knuckle hump just before the inner edge -> over the edge -> pressed,
    # the middle joint standing out from the face, the claw tip digging back in -> tight tendril spiral.
    dict(name="A", r0=1.1, curl=1, seed=11, rho_k=3.8, ctrl=[
        (-3.0, -14.5, -10.5), (-4.6, -12.0, -6.0), (-6.3, -8.7, -1.6), (-7.4, -6.9, 0.6), (-8.4, -4.4, 1.0),
        (-9.4, -1.4, 2.9), (-10.0, 0.25, 1.8), (-10.5, 1.0, -0.4), (-11.0, 1.45, -2.6), (-11.8, 0.95, -4.4),
        (-12.3, 0.45, -5.6)]),
    dict(name="B", r0=1.15, curl=-1, seed=23, rho_k=3.5, ctrl=[
        (-1.2, -15.0, -11.0), (-1.8, -12.2, -6.5), (-2.5, -8.9, -1.9), (-3.0, -6.9, 0.7), (-3.4, -4.3, 1.1),
        (-3.7, -1.3, 3.2), (-3.8, 0.3, 2.0), (-3.9, 1.1, -0.5), (-3.7, 1.55, -3.0), (-3.3, 1.0, -5.4),
        (-3.1, 0.5, -6.9)]),
    dict(name="C", r0=1.0, curl=1, seed=37, end="helix", ctrl=[
        (0.6, -14.2, -10.0), (1.4, -11.6, -5.8), (2.4, -8.7, -1.7), (3.0, -6.8, 0.6), (3.4, -4.2, 1.0),
        (3.8, -1.3, 2.8), (4.0, 0.25, 1.7), (4.1, 1.0, -0.6), (4.5, 1.45, -2.7), (5.1, 0.9, -4.6),
        (5.5, 0.45, -5.8)]),
    dict(name="D", r0=0.86, curl=-1, seed=41, rho_k=3.6, ctrl=[
        (2.4, -13.6, -9.4), (4.4, -11.2, -5.4), (6.7, -8.5, -1.5), (8.2, -6.8, 0.55), (9.3, -4.3, 0.9),
        (10.1, -1.3, 2.4), (10.5, 0.2, 1.4), (10.8, 0.85, -0.5), (11.4, 1.25, -2.2), (12.0, 0.75, -3.7),
        (12.4, 0.4, -4.6)]),
]
EMBED = 0.14


def vine_taper(V, t):
    return V["r0"] * (1.0 - 0.34 * t ** 1.4) * (1.0 - 0.6 * smoothstep(0.8, 1.0, t))


def vine_knot_t(V, t, L):
    tb = dict(knots=[(tk * L, A, w) for tk, A, w in V["knots"]])
    return knot_val(tb, t * L)


def auto_knots(V, pts):
    """Nodes along the vine (t = fraction of the main length): 3 behind the wall, a big KNUCKLE at the top of
    the hump just before the inner edge, and a finger joint halfway down the inner face."""
    n = len(pts)
    top = [i for i in range(n) if -4.5 < pts[i].y < 0.5]
    i_h = max(top, key=lambda i: pts[i].z)
    i_c = min(range(n), key=lambda i: pts[i].y ** 2 + pts[i].z ** 2)
    face = [i for i in range(i_c, n) if pts[i].z < -1.0]
    i_j = max(face, key=lambda i: pts[i].y)
    t_h, t_c, t_j = i_h / (n - 1), i_c / (n - 1), i_j / (n - 1)
    k = V["r0"] / 1.05
    V["knots"] = [(0.13, 0.2, 0.7 * k), (0.29, 0.24, 0.7 * k), (0.45, 0.17, 0.55 * k), (t_h, 0.34, 0.6 * k),
                  (t_j, 0.21, 0.36 * k)]
    V["t_hump"], V["t_corner"], V["t_joint"] = t_h, t_c, t_j


def build_vine(V):
    rng = random.Random(V["seed"])
    pts = resample(cr_chain([Vector(c) for c in V["ctrl"]]), 0.05)
    auto_knots(V, pts)
    off = nvec(V["seed"] + 3)
    n = len(pts)
    S = arclen(pts)
    L = S[-1]
    for i in range(n):
        w = 0.32 * smoothstep(0.0, 2.0, S[i]) * smoothstep(0.0, 2.0, L - S[i])
        q = Vector((S[i] * 0.2, 0, 0)) + off
        pts[i] = pts[i] + Vector((noise.noise(q), noise.noise(q + Vector((0, 9.1, 0))),
                                  0.6 * noise.noise(q + Vector((0, 0, 17.3))))) * w
    for it in range(24):
        n = len(pts)
        for i in range(n):
            t = i / (n - 1)
            c = vine_taper(V, t) * (1 + max(0.0, vine_knot_t(V, t, L))) - EMBED
            pts[i] = wall_push(pts[i], c)
        if it < 23:
            pts = smooth_path(pts, 1, 0.45, 2, 2)
    pts = resample(pts, 0.05)
    n = len(pts)
    for i in range(n):
        t = i / (n - 1)
        pts[i] = wall_push(pts[i], vine_taper(V, t) * (1 + max(0.0, vine_knot_t(V, t, L))) - EMBED)
    L = arclen(pts)[-1]
    reff = [vine_taper(V, i / (n - 1)) * (1 + max(0.0, vine_knot_t(V, i / (n - 1), L))) for i in range(n)]
    pts = limit_curvature(pts, reff, [r - EMBED for r in reff], k=1.45)
    L = arclen(pts)[-1]
    main_n = len(pts)
    # --- the claw tip ends in a TIGHT tendril spiral: logarithmic, tilted 35 deg out of the wall plane and
    # pulled out into a shallow cone (like a real tendril coil), curling sideways.
    d = (pts[-1] - pts[-4]).normalized()
    r_e = vine_taper(V, 1.0)
    side = Vector((V["curl"], 0, 0))
    tilt = math.radians(35)
    curl = side * math.cos(tilt) + Vector((0, 1, 0)) * math.sin(tilt)
    curl = (curl - d * d.dot(curl)).normalized()
    rho0 = V.get("rho_k", 3.6) * r_e
    Phi = 2 * math.pi * 2.05
    rho_end = 0.27 * rho0
    k = math.log(rho0 / rho_end) / Phi
    c0 = pts[-1] + curl * rho0
    e1, e2 = -curl, d
    nrm = e1.cross(e2)
    if nrm.y < 0:
        nrm = -nrm
    phi = 0.0
    spiral, sr = [], []
    while phi < Phi:
        rho = rho0 * math.exp(-k * phi)
        phi += 0.04 / rho
        if phi >= Phi:
            break
        rho = rho0 * math.exp(-k * phi)
        p = c0 + (e1 * math.cos(phi) + e2 * math.sin(phi)) * rho + nrm * (0.75 * rho0 * (phi / Phi) ** 1.3)
        rr = max(0.055, r_e * (rho / rho0) ** 1.25)
        spiral.append(wall_push(p, rr - 0.03))
        sr.append(rr)
    if V.get("end") == "helix":
        axis = (side * 0.3 + Vector((0, 0.5, 0)) + d * 0.85).normalized()
        coil = resample(helix_points(pts[-1], d, axis, 0.44, 0.24, 0.62, 3.2, hand=V["curl"], ramp=0.35), 0.04)[1:]
        spiral, sr = [], []
        for q, p in enumerate(coil):
            f = q / max(1, len(coil) - 1)
            rr = r_e * (1 - f) + 0.06 * f
            spiral.append(wall_push(p, rr - 0.03))
            sr.append(rr)
    P = pts + spiral
    R = [vine_taper(V, i / (main_n - 1)) for i in range(main_n)] + sr
    P = smooth_path(P, 2, 0.4, 1, 1)
    knots = [(tk * L, A, w) for tk, A, w in V["knots"]]
    tb = make_tube("vine", P, R, V["seed"], knots=knots, ridges=5, amp=0.22, twist=0.28, lumps=0.09, tmain=L,
                   name=V["name"])
    tb["L_main"] = L
    tb["main_n"] = main_n
    return tb


def vine_point(tb, t):
    """Point / frame on a vine at main-length fraction t."""
    s = t * tb["L_main"]
    S = tb["S"]
    i = min(range(len(S)), key=lambda k: abs(S[k] - s))
    return i


# ------------------------------------------------------------------ tendrils
def helix_points(start, T0, axis, rho0, rho1, pitch, turns, hand=1, perversion=None, ramp=0.7):
    """Coil grown by integrating the Frenet frame with the curvature / torsion of a helix (radius rho, pitch):
    starts along T0 (curvature ramps in over `ramp` studs), coils around ~axis, radius rho0 -> rho1, and flips
    handedness at fraction `perversion` (the twist reversal real pumpkin tendrils show)."""
    c = pitch / (2 * math.pi)
    A = axis.normalized()
    T = T0.normalized()
    Bv = A - T * T.dot(A)
    if Bv.length < 1e-3:
        Bv = T.orthogonal()
    Bv.normalize()
    Nv = Bv.cross(T)
    rho_m = 0.5 * (rho0 + rho1)
    total = turns * 2 * math.pi * math.sqrt(rho_m * rho_m + c * c) + ramp
    ds = 0.03
    p = start.copy()
    pts = [p.copy()]
    s = 0.0
    flipped = False
    while s < total:
        f = s / total
        rho = rho0 + (rho1 - rho0) * f
        g = smoothstep(0.0, ramp, s)
        h = hand
        if perversion is not None:
            # a real perversion: the curvature fades to an inflection, then BOTH the bending direction and the
            # handedness flip, so the second coil grows away from the twist point instead of back over the first.
            g *= smoothstep(0.0, 0.05, abs(f - perversion))
            if f >= perversion and not flipped:
                Nv, Bv = -Nv, -Bv
                flipped = True
            if flipped:
                h = -hand
        den = rho * rho + c * c
        kap = g * rho / den
        tau = g * h * c / den
        T2 = T + Nv * (kap * ds)
        N2 = Nv + (-T * kap + Bv * tau) * ds
        p = p + (T + T2.normalized()) * (0.5 * ds)
        T = T2.normalized()
        Nv = (N2 - T * T.dot(N2)).normalized()
        Bv = T.cross(Nv)
        pts.append(p.copy())
        s += ds
    return pts


def build_tendril(TD, vines):
    tb_v = vines[TD["vine"]]
    t = TD["t"]
    if isinstance(t, str):
        t = VINES[TD["vine"]]["t_" + t]
    i = vine_point(tb_v, t)
    base = tb_v["P"][i]
    dirv = Vector(TD["dir"]).normalized()
    start = base + dirv * tb_v["R"][i] * 0.4
    if TD.get("wrap"):
        # coil around the host vine from t to t1
        i1 = vine_point(tb_v, TD["wrap"])
        pts = []
        phi = TD.get("phi0", 0.0)
        s0 = tb_v["S"][i]
        for k in range(i, i1, 1 if i1 > i else -1):
            s = tb_v["S"][k]
            rr = tb_v["R"][k] * (1 + max(0.0, knot_val(tb_v, s))) * 1.04 + 0.16
            ph = phi + 2 * math.pi * abs(s - s0) / TD["pitch"]
            pts.append(tb_v["P"][k] + (tb_v["N"][k] * math.cos(ph) + tb_v["B"][k] * math.sin(ph)) * rr)
        pts = [start] + pts
        T0 = (pts[-1] - pts[-3]).normalized()
        tail = helix_points(pts[-1], T0, Vector(TD["tail_dir"]), 0.34, 0.16, 0.42, TD.get("tail_turns", 1.6),
                            hand=TD.get("hand", 1), ramp=0.4)
        pts = pts + tail[1:]
    else:
        lead_end = start + dirv * TD["lead"]
        bend = Vector(TD.get("bend", (0, 0, 0)))
        lead = bezier3(start, start + dirv * TD["lead"] * 0.4, lead_end - dirv * TD["lead"] * 0.3 + bend,
                       lead_end + bend, 40)
        T0 = (lead[-1] - lead[-3]).normalized()
        coil = helix_points(lead[-1], T0, Vector(TD.get("axis", TD["dir"])), TD["rho"], TD["rho"] * 0.45,
                            TD["pitch"], TD["turns"], hand=TD.get("hand", 1), perversion=TD.get("perv"))
        pts = lead + coil[1:]
    pts = resample(pts, 0.05)
    pts = smooth_path(pts, 3, 0.5, 1, 1)
    n = len(pts)
    R = [0.17 - 0.09 * (k / (n - 1)) ** 0.8 for k in range(n)]
    pts = limit_curvature(pts, R, [r - 0.02 for r in R], k=1.5, h=4)
    pts = [wall_push(p, R[k] - 0.02) for k, p in enumerate(pts)]
    tb = make_tube("tendril", pts, R, TD["seed"], ridges=0, amp=0.0, twist=0.0, lumps=0.04, dry=TD.get("dry", 0.0),
                   cap0=False, name="T" + str(TD["seed"]))
    tb["m_lo"] = 6
    return tb


TENDRILS = [
    # vine index, t on the host vine ("hump" / "joint" = that vine's knuckle / finger-joint node)
    dict(vine=0, t="hump", dir=(-0.3, 0.8, 0.5), lead=1.5, rho=0.5, pitch=0.6, turns=3.6, hand=1, seed=101,
         axis=(-0.25, 0.7, -0.67)),
    dict(vine=1, t=0.3, dir=(0.25, 0.1, 0.97), lead=3.2, rho=0.6, pitch=0.7, turns=4.6, hand=-1, seed=102,
         perv=0.5, axis=(0.2, 0.25, 0.95), bend=(0.4, 0.6, 0.0), dry=0.6),
    dict(vine=2, t=0.47, wrap=0.6, pitch=1.5, tail_dir=(0.3, 0.8, 0.5), seed=103, dir=(0, 0, 1), tail_turns=1.8),
    dict(vine=3, t="hump", dir=(0.85, 0.45, 0.15), lead=2.0, rho=0.5, pitch=0.6, turns=3.6, hand=-1, seed=104,
         axis=(0.6, 0.35, -0.72), dry=0.3),
    dict(vine=0, t=0.32, dir=(-0.75, 0.1, 0.65), lead=2.4, rho=0.55, pitch=0.6, turns=4.0, hand=1, seed=105,
         axis=(-0.6, 0.15, 0.8), bend=(-0.3, 0.4, 0.3), dry=0.15),
    dict(vine=1, t="joint", dir=(0.55, 0.6, -0.55), lead=0.9, rho=0.42, pitch=0.5, turns=5.0, hand=1, seed=106,
         axis=(0.3, 0.35, -0.89), dry=0.1),
    dict(vine=2, t="hump", dir=(0.5, 0.6, 0.62), lead=1.6, rho=0.45, pitch=0.55, turns=3.2, hand=-1, seed=107,
         axis=(0.3, 0.5, 0.8), dry=0.45, perv=0.55),
]


# ------------------------------------------------------------------ leaves
def ang_diff(a, b):
    d = (a - b + math.pi) % (2 * math.pi) - math.pi
    return d


def smax(a, b, k):
    h = max(k - abs(a - b), 0.0) / k
    return max(a, b) + h * h * k * 0.25


def leaf_lobes(LP):
    rng = random.Random(LP["seed"])
    base = [(0.0, 1.0, 0.86), (1.3, 0.9, 0.82), (-1.3, 0.9, 0.82), (2.42, 0.7, 0.78), (-2.42, 0.7, 0.78)]
    out = []
    for th, Lk, w in base:
        out.append((th + rng.uniform(-0.08, 0.08), Lk * rng.uniform(0.92, 1.08), w * rng.uniform(0.92, 1.08)))
    return out


def leaf_R(th, LP):
    r = LP["core"]
    for tk, Lk, wk in LP["lobes"]:
        x = abs(ang_diff(th, tk)) / wk
        if x < 1:
            r = smax(r, Lk * (1 - x) ** 1.05, 0.12)
    sb = smoothstep(math.pi - 0.26, math.pi - 0.01, abs(th))
    r *= 1 - 0.9 * sb
    return r * LP["L"]


def leaf_outline(LP, hi):
    """Serrated outline (CCW in leaf 2D, x right, y forward). Lo = tooth tips + notches only."""
    L = LP["L"]
    rng = random.Random(LP["seed"] + 5)
    M = 4000
    th = [-math.pi + 2 * math.pi * (k + 0.5) / M for k in range(M)]
    sm = [Vector((leaf_R(t, LP) * math.sin(t), leaf_R(t, LP) * math.cos(t))) for t in th]
    # clockwise in (x,y) as theta grows from -pi..pi via sin/cos -> reverse later if needed
    S = arclen(sm + [sm[0]])
    total = S[-1]

    def at(s):
        s = s % total
        lo, hi_ = 0, len(S) - 1
        while hi_ - lo > 1:
            mid = (lo + hi_) // 2
            if S[mid] <= s:
                lo = mid
            else:
                hi_ = mid
        a, b = sm[lo % M], sm[(lo + 1) % M]
        f = (s - S[lo]) / max(1e-9, S[lo + 1] - S[lo])
        p = a.lerp(b, f)
        tg = (b - a).normalized()
        return p, tg

    period = LP.get("tooth", 0.058) * L
    amp = 0.02 * L
    pts = []
    s = rng.uniform(0, period)
    s_end = s + total
    while s < s_end - 0.3 * period:
        P_k = period * rng.uniform(0.7, 1.3)
        A_k = amp * (rng.uniform(0.4, 1.3) if rng.random() > 0.12 else rng.uniform(1.6, 2.2))
        sub = 5 if hi else 1
        for h in range(2 * sub):
            f = h / (2 * sub)
            ss = s + P_k * f
            p, tg = at(ss)
            inward = Vector((tg.y, -tg.x))  # sm runs clockwise -> the interior is on the right
            tooth = 1 - abs(1 - 2 * f)  # 0 at tip, 1 at notch
            rr = p.length
            mask = smoothstep(0.42 * L, 0.6 * L, rr)
            pts.append(p + inward * (A_k * tooth * mask))
        s += P_k
    # make CCW
    area = 0.0
    for i in range(len(pts)):
        a, b = pts[i], pts[(i + 1) % len(pts)]
        area += a.x * b.y - b.x * a.y
    if area < 0:
        pts.reverse()
    return pts


def poly_inside(poly, P):
    poly = np.asarray(poly, np.float64)
    x1, y1 = poly[:, 0][None, :], poly[:, 1][None, :]
    x2, y2 = np.roll(poly[:, 0], -1)[None, :], np.roll(poly[:, 1], -1)[None, :]
    out = np.zeros(len(P), bool)
    for c in range(0, len(P), 1500):
        x = P[c:c + 1500, 0][:, None]
        y = P[c:c + 1500, 1][:, None]
        cond = ((y1 > y) != (y2 > y)) & (x < (x2 - x1) * (y - y1) / (y2 - y1 + 1e-12) + x1)
        out[c:c + 1500] = cond.sum(1) % 2 == 1
    return out


def leaf_sheet2d(LP, hi):
    """2D triangulation of the leaf: returns (verts Nx2, faces, outline Kx2)."""
    L = LP["L"]
    outl = leaf_outline(LP, hi)
    h = 0.045 if hi else LP.get("lo_h", 0.078) * L
    ext = L * 1.1
    ys = np.arange(-ext, ext, h * 0.866)
    pts = []
    for k, y in enumerate(ys):
        xs = np.arange(-ext + (h * 0.5 if k % 2 else 0.0), ext, h)
        pts.append(np.stack([xs, np.full_like(xs, y)], 1))
    G = np.concatenate(pts)
    O = np.array([(p.x, p.y) for p in outl])
    G = G[poly_inside(O, G)]
    kd = kdtree.KDTree(len(O))
    for i, p in enumerate(O):
        kd.insert((p[0], p[1], 0.0), i)
    kd.balance()
    keep = np.array([kd.find((g[0], g[1], 0.0))[2] > 0.55 * h for g in G], bool)
    G = G[keep]
    allp = [Vector((p[0], p[1])) for p in O] + [Vector((g[0], g[1])) for g in G]
    res = geometry.delaunay_2d_cdt(allp, [], [list(range(len(O)))], 1, 1e-7)
    verts, faces = res[0], res[2]
    used = sorted(set(itertools.chain.from_iterable(faces)))
    remap = {o: n for n, o in enumerate(used)}
    V2 = np.array([(verts[o].x, verts[o].y) for o in used])
    F = [tuple(remap[i] for i in f) for f in faces]
    return V2, F, O


def leaf_veins(LP):
    """Vein segments in leaf 2D: list of (a, b, wa, wb, main)."""
    L = LP["L"]
    rng = random.Random(LP["seed"] + 9)
    segs = []
    for tk, Lk, wk in LP["lobes"]:
        tip_r = leaf_R(tk, LP) * 0.95
        tip = Vector((math.sin(tk), math.cos(tk))) * tip_r
        bend = Vector((math.cos(tk), -math.sin(tk))) * rng.uniform(-0.06, 0.06) * L
        prev = Vector((0, 0))
        main = []
        for q in range(1, 13):
            f = q / 12
            p = tip * f + bend * (4 * f * (1 - f))
            w0 = (0.05 - 0.036 * (q - 1) / 12) * L
            w1 = (0.05 - 0.036 * q / 12) * L
            segs.append((prev, p, w0, w1, 1))
            main.append(p)
            prev = p
        # secondary veins, alternating sides, toward the margin and the lobe tip
        for q, f in enumerate([0.22, 0.34, 0.46, 0.58, 0.7, 0.82]):
            base = tip * f + bend * (4 * f * (1 - f))
            for side in (-1, 1):
                if (q + (side > 0)) % 2 and f < 0.3:
                    continue
                ang = tk + side * rng.uniform(0.75, 0.95)
                d = Vector((math.sin(ang), math.cos(ang)))
                # length: until near the margin along d
                ln = 0.0
                for st in range(60):
                    ln += 0.025 * L
                    p = base + d * ln
                    th = math.atan2(p.x, p.y)
                    if p.length > leaf_R(th, LP) * 0.9:
                        break
                prev = base
                for u in range(1, 5):
                    g = u / 4
                    cur = base + d * (ln * g) + (tip - base).normalized() * (0.12 * ln * g * g)
                    segs.append((prev, cur, (0.017 - 0.0028 * (u - 1)) * L, (0.017 - 0.0028 * u) * L, 0))
                    prev = cur
    return segs


def vein_field(P2, segs, L):
    """P2: (K,2). Returns (vein 0..1, near-main 0..1)."""
    A = np.array([(s[0].x, s[0].y) for s in segs])
    Bv = np.array([(s[1].x, s[1].y) for s in segs])
    WA = np.array([s[2] for s in segs])
    WB = np.array([s[3] for s in segs])
    MN = np.array([s[4] for s in segs], bool)
    vein = np.zeros(len(P2))
    near = np.zeros(len(P2))
    AB = Bv - A
    ab2 = (AB ** 2).sum(1) + 1e-12
    for c in range(0, len(P2), 4000):
        p = P2[c:c + 4000][:, None, :]
        t = np.clip(((p - A[None]) * AB[None]).sum(2) / ab2[None], 0, 1)
        q = A[None] + AB[None] * t[..., None]
        d = np.sqrt(((p - q) ** 2).sum(2))
        w = WA[None] + (WB - WA)[None] * t
        v = np.clip(1 - d / w, 0, 1) ** 0.8
        vein[c:c + 4000] = v.max(1)
        dm = np.where(MN[None], d, 1e9).min(1)
        near[c:c + 4000] = np.exp(-(dm / (0.1 * L)) ** 2)
    return vein, near


def leaf_frame(LP):
    Z = Vector(LP["up"]).normalized()
    Y = Vector(LP["fwd"])
    Y = (Y - Z * Y.dot(Z)).normalized()
    X = Y.cross(Z)
    return X, Y, Z


def leaf_h(LP, x, y):
    L = LP["L"]
    r = math.hypot(x, y)
    th = math.atan2(x, y)
    Rs = max(1e-3, leaf_R(th, LP))
    rho = min(1.25, r / Rs)
    rl = r / L
    h = LP["cup"] * L * rl * rl
    h += LP["fold"] * abs(x) * smoothstep(0.0, 0.4 * L, y + 0.2 * L)
    h -= LP["droop"] * L * max(0.0, y / L) ** 2
    g = min(abs(ang_diff(th, tk)) for tk, _, _ in LP["lobes"]) / 0.62
    h += LP["pleat"] * L * rl * min(1.0, g) ** 1.5
    h += LP["wave"] * L * rho ** 3 * math.sin(LP["wn"] * th + LP["wph"])
    off = LP["off"]
    h += LP["crinkle"] * L * rho ** 2 * fbm(Vector((x, y, 0.0)) * (2.2 / L) + off, 3)
    h += LP["curl"] * L * smoothstep(0.65, 1.05, rho) ** 2
    return h


LEAF_PALETTE = dict(g1=lin((22, 56, 20)), g2=lin((48, 92, 32)), pale=lin((132, 152, 100)), vein_g=lin((128, 152, 80)),
                    yel=lin((210, 170, 48)), ora=lin((214, 124, 34)), vein_y=lin((230, 210, 132)),
                    br1=lin((116, 76, 36)), br2=lin((78, 52, 26)), spot=lin((70, 48, 24)))


def leaf_colors(LP, P2, vein, near, dedge):
    L = LP["L"]
    sea = LP["season"]
    off = LP["off"]
    C = LEAF_PALETTE
    cols, rough = [], []
    for k in range(len(P2)):
        x, y = P2[k]
        q = Vector((x, y, 0.0)) / L
        r = math.hypot(x, y)
        th = math.atan2(x, y)
        rho = min(1.2, r / max(1e-3, leaf_R(th, LP)))
        mot = smoothstep(-0.35, 0.45, fbm(q * 4.0 + off, 3))
        col = mix(C["g1"], C["g2"], mot)
        bl = near[k] * smoothstep(-0.1, 0.4, noise.noise(q * 9.0 + off * 1.3)) * (1 - rho) * (1 - sea) ** 2
        col = mix(col, C["pale"], 0.55 * bl)
        ny = noise.noise(q * 3.0 + off * 0.7)
        ylw = sea * 1.7 - 0.35 + 0.5 * (rho - 0.5) - 0.45 * near[k] + 0.3 * ny
        yc = mix(C["yel"], C["ora"], smoothstep(0.45, 1.0, sea) * smoothstep(-0.2, 0.5, noise.noise(q * 2.3 + off * 1.7)))
        col = mix(col, yc, smoothstep(0.0, 1.0, ylw))
        bw = (0.03 + 0.3 * sea ** 1.6) * L * (0.6 + 0.8 * smoothstep(-0.5, 0.5, noise.noise(q * 5.0 + off * 0.3)))
        e = 1 - smoothstep(bw * 0.75, bw, dedge[k])
        brown = mix(C["br1"], C["br2"], smoothstep(-0.3, 0.5, noise.noise(q * 14.0 + off)))
        if sea > 0.12:
            col = mix(col, brown, e)
            col = tuple(c * (1 - 0.5 * math.exp(-((dedge[k] - bw) / (0.02 * L)) ** 2)) for c in col)
        spot = smoothstep(0.42, 0.55, fbm(q * 7.0 + off * 2.1, 3)) * smoothstep(0.2, 0.8, sea)
        col = mix(col, C["spot"], 0.85 * spot)
        vc = mix(C["vein_g"], C["vein_y"], smoothstep(0.2, 0.8, sea))
        col = mix(col, vc, 0.62 * vein[k] * (1 - 0.7 * e))
        rr = 0.5 + 0.22 * smoothstep(0.0, 1.0, ylw) + 0.25 * max(e, spot) - 0.08 * vein[k]
        cols.append(col)
        rough.append((rr, rr, rr))
    return cols, rough


class Pusher:
    """Keeps leaves off the main vines. Leaf vertices only move along their leaf's normal Z (a height-field
    move: it can never flip a triangle), up or down depending on which side of the vine axis they are."""

    def __init__(self, vines):
        pts = []
        for tb in vines:
            for i in range(0, len(tb["P"]), 2):
                rr = tb["R"][i] * (1 + max(0.0, knot_val(tb, tb["S"][i])))
                pts.append((tb["P"][i], rr, tb["T"][i]))
        self.pts = pts
        self.kd = kdtree.KDTree(len(pts))
        for i, (p, r, t) in enumerate(pts):
            self.kd.insert(p, i)
        self.kd.balance()

    def push(self, p, Z, clear=0.07):
        for _ in range(3):
            moved = False
            for (co, idx, dist) in self.kd.find_range(p, 1.8):
                c, r, T = self.pts[idx]
                need = r * 1.06 + clear
                if dist >= need:
                    continue
                v = p - c
                vp = v - T * v.dot(T)
                Zp = Z - T * Z.dot(T)
                a = Zp.dot(Zp)
                if a < 0.09:     # leaf normal nearly along the vine: a normal-direction push would explode
                    continue
                b = vp.dot(Zp)
                cc = vp.dot(vp) - need * need
                disc = b * b - a * cc
                if disc < 0:
                    continue
                sq = math.sqrt(disc)
                t = (-b + sq) / a if b >= 0 else (-b - sq) / a
                if abs(t) > 0.9 * need:   # deep inside: leave it tucked into the vine (hidden) - no spikes
                    continue
                p = p + Z * t
                moved = True
            if not moved:
                break
        return p


def leaf_wall(p, c=0.07):
    """Wall push for leaf vertices: inside the slab -> out through the top or the inner face only."""
    if WY0 <= p.y <= WY1 and WZ0 <= p.z <= WZ1:
        if (WZ1 - p.z) <= (WY1 - p.y) or p.y < WY0 + 1.0:
            return Vector((p.x, p.y, WZ1 + c))
        return Vector((p.x, WY1 + c, p.z))
    return wall_push(p, c)


def place_leaf(LP, P2, pusher, hi):
    X, Y, Z = leaf_frame(LP)
    base = Vector(LP["base"])
    out = []
    for x, y in P2:
        h = leaf_h(LP, x, y)
        p = base + X * x + Y * y + Z * h
        p = leaf_wall(pusher.push(leaf_wall(p), Z, 0.07))
        out.append(p)
    return out


def leaf_hi_extra(LP, P2, vein):
    """Sunken veins (hi only): offset along the leaf normal."""
    X, Y, Z = leaf_frame(LP)
    return [-Z * (0.045 * LP["L"] / 6.0 + 0.012) * v for v in vein]


def init_leaf(LP):
    rng = random.Random(LP["seed"])
    LP.setdefault("core", 0.58)
    LP["lobes"] = leaf_lobes(LP)
    LP.setdefault("cup", 0.2)
    LP.setdefault("fold", 0.12)
    LP.setdefault("droop", 0.25)
    LP.setdefault("pleat", 0.05)
    LP.setdefault("wave", 0.07)
    LP.setdefault("wn", 9.0)
    LP["wph"] = rng.uniform(0, 6.28)
    LP.setdefault("crinkle", 0.02 + 0.06 * LP["season"] ** 2)
    LP.setdefault("curl", 0.25 * max(0.0, LP["season"] - 0.55))
    LP["off"] = nvec(LP["seed"] + 11)
    return LP


LEAVES = [
    # big leaves rising from BEHIND the wall (lower halves hidden behind it), faces toward the hub, tips leaning over
    dict(name="BackL", L=5.6, season=0.12, seed=201, base=(-6.6, -7.5, 2.4), fwd=(-0.1, 0.16, 0.98),
         up=(0.05, 0.98, -0.18), droop=-0.22, cup=0.17),
    dict(name="BackR", L=6.0, season=0.55, seed=202, base=(7.0, -7.4, 2.2), fwd=(0.16, 0.2, 0.97),
         up=(-0.08, 0.97, -0.22), droop=-0.2, cup=0.17),
    dict(name="FarL", L=5.0, season=0.4, seed=206, base=(-14.0, -7.8, 1.8), fwd=(-0.45, 0.15, 0.88),
         up=(0.3, 0.95, -0.05), droop=-0.18, cup=0.12),
    dict(name="FarR", L=4.2, season=0.97, seed=207, base=(13.8, -7.8, 1.6), fwd=(0.45, 0.15, 0.88),
         up=(-0.3, 0.95, -0.05), droop=-0.12, cup=0.14),
    # on the wall top, raised on their stalks between the knuckles
    dict(name="TopC", L=3.6, season=0.3, seed=203, base=(0.1, -3.5, 3.1), fwd=(0.02, 0.3, 0.95),
         up=(0.0, 0.95, -0.3), droop=-0.14),
    dict(name="SmallTop", L=3.0, season=0.9, seed=209, base=(-13.0, -1.6, 2.1), fwd=(-0.35, 0.45, 0.82),
         up=(0.2, 0.87, -0.45), droop=-0.1),
    # hanging over the inner edge between the fingers
    dict(name="HangL", L=2.9, season=0.05, seed=204, base=(-7.3, 1.3, 0.5), fwd=(0.05, 0.3, -0.95),
         up=(0.0, 0.95, 0.3), cup=0.12, droop=0.12),
    dict(name="HangR", L=3.0, season=0.82, seed=205, base=(7.8, 0.9, 0.6), fwd=(-0.1, 0.5, -0.86),
         up=(0.0, 0.86, 0.5), cup=0.12, droop=0.1),
    dict(name="FingerB", L=2.7, season=0.7, seed=208, base=(-2.0, 1.4, -3.4), fwd=(0.55, 0.35, -0.76),
         up=(0.0, 1.0, 0.3), cup=0.1, droop=0.05),
]


def nearest_vine_point(vines, p):
    best = None
    for vi, tb in enumerate(vines):
        for i in range(0, tb["main_n"], 2):
            d = (tb["P"][i] - p).length - tb["R"][i]
            if best is None or d < best[0]:
                best = (d, vi, i)
    return best


def build_petiole(LP, vines):
    X, Y, Z = leaf_frame(LP)
    base = Vector(LP["base"])
    _, vi, i = nearest_vine_point(vines, base - Y * 1.2 - Z * 0.6)
    tb = vines[vi]
    c = tb["P"][i]
    d0 = (base - c)
    D = d0.length
    out = d0 - tb["T"][i] * tb["T"][i].dot(d0)
    out = out.normalized() if out.length > 1e-4 else d0.normalized()
    p0 = c + out * tb["R"][i] * 0.35
    t_end = (Y * 0.6 + Z * 0.5).normalized()
    r0 = 0.07 * LP["L"] / 1.6 + 0.08
    p3 = base + Y * 0.1 - Z * r0 * 0.75
    pts = bezier3(p0, p0 + out * D * 0.45, p3 - t_end * D * 0.4, p3, 60)
    pts = resample(pts, 0.05)
    n = len(pts)
    r0 = 0.07 * LP["L"] / 1.6 + 0.08
    R = []
    for k in range(n):
        f = k / (n - 1)
        R.append(r0 * (1.0 - 0.3 * f) * (1 + 0.35 * math.exp(-(f / 0.08) ** 2)) * (1 + 0.3 * math.exp(-((1 - f) / 0.06) ** 2)))
    for _ in range(4):
        pts = [wall_push(p, R[k] - 0.03) for k, p in enumerate(pts)]
        pts = smooth_path(pts, 1, 0.4, 2, 2)
    tb_p = make_tube("petiole", pts, R, LP["seed"] + 50, ridges=5, amp=0.12, twist=0.05, lumps=0.03, cap0=False,
                     tip=False, name="Pet" + LP["name"])
    return tb_p


# ------------------------------------------------------------------ materials (hi)
def mat_vine_hi():
    m = mat_vc("VineHi")
    nt = m.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    vor = nt.nodes.new("ShaderNodeTexVoronoi")
    vor.voronoi_dimensions = "3D"
    vor.feature = "F1"
    vor.inputs["Scale"].default_value = 7.5
    vor.inputs["Randomness"].default_value = 1.0
    nt.links.new(tc.outputs["Object"], vor.inputs["Vector"])
    mr = nt.nodes.new("ShaderNodeMapRange")
    mr.interpolation_type = "SMOOTHSTEP"
    mr.inputs["From Min"].default_value = 0.0
    mr.inputs["From Max"].default_value = 0.34
    mr.inputs["To Min"].default_value = 1.0
    mr.inputs["To Max"].default_value = 0.0
    nt.links.new(vor.outputs["Distance"], mr.inputs["Value"])
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 22.0
    nz.inputs["Detail"].default_value = 4.0
    nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
    add = nt.nodes.new("ShaderNodeMath")
    add.operation = "MULTIPLY_ADD"
    nt.links.new(nz.outputs["Fac"], add.inputs[0])
    add.inputs[1].default_value = 0.25
    nt.links.new(mr.outputs["Result"], add.inputs[2])
    bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.5
    bump.inputs["Distance"].default_value = 0.04
    nt.links.new(add.outputs["Value"], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    # pale hair tips over the colour
    vc = [n for n in nt.nodes if n.type == "VERTEX_COLOR" and n.layer_name == "Col"][0]
    mul = nt.nodes.new("ShaderNodeMath")
    mul.operation = "MULTIPLY"
    nt.links.new(mr.outputs["Result"], mul.inputs[0])
    mul.inputs[1].default_value = 0.14
    color_mix(nt, mul.outputs["Value"], vc.outputs["Color"], lin((176, 184, 128)), bsdf.inputs["Base Color"])
    return m


def color_mix(nt, fac_out, a_out, b_col, to_socket):
    mx = nt.nodes.new("ShaderNodeMix")
    mx.data_type = "RGBA"
    mx.blend_type = "MIX"
    fac = [s for s in mx.inputs if s.name == "Factor" and s.type == "VALUE"][0]
    a = [s for s in mx.inputs if s.name == "A" and s.type == "RGBA"][0]
    b = [s for s in mx.inputs if s.name == "B" and s.type == "RGBA"][0]
    res = [s for s in mx.outputs if s.name == "Result" and s.type == "RGBA"][0]
    nt.links.new(fac_out, fac)
    nt.links.new(a_out, a)
    b.default_value = (*b_col, 1)
    nt.links.new(res, to_socket)
    return mx


def mat_leaf_hi():
    m = mat_vc("LeafHi")
    nt = m.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    uv = nt.nodes.new("ShaderNodeUVMap")
    uv.uv_map = "UVMap"
    vor = nt.nodes.new("ShaderNodeTexVoronoi")
    vor.voronoi_dimensions = "2D"
    vor.feature = "DISTANCE_TO_EDGE"
    vor.inputs["Scale"].default_value = 6.5
    nt.links.new(uv.outputs["UV"], vor.inputs["Vector"])
    mr = nt.nodes.new("ShaderNodeMapRange")
    mr.interpolation_type = "SMOOTHSTEP"
    mr.inputs["From Min"].default_value = 0.0
    mr.inputs["From Max"].default_value = 0.035
    nt.links.new(vor.outputs["Distance"], mr.inputs["Value"])
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 9.0
    nz.inputs["Detail"].default_value = 5.0
    nt.links.new(uv.outputs["UV"], nz.inputs["Vector"])
    add = nt.nodes.new("ShaderNodeMath")
    add.operation = "MULTIPLY_ADD"
    nt.links.new(nz.outputs["Fac"], add.inputs[0])
    add.inputs[1].default_value = 0.35
    nt.links.new(mr.outputs["Result"], add.inputs[2])
    bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.18
    bump.inputs["Distance"].default_value = 0.02
    nt.links.new(add.outputs["Value"], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    # tertiary veins: slightly paler lines over the vertex colour
    vc = [n for n in nt.nodes if n.type == "VERTEX_COLOR" and n.layer_name == "Col"][0]
    inv = nt.nodes.new("ShaderNodeMath")
    inv.operation = "SUBTRACT"
    inv.inputs[0].default_value = 1.0
    nt.links.new(mr.outputs["Result"], inv.inputs[1])
    mul = nt.nodes.new("ShaderNodeMath")
    mul.operation = "MULTIPLY"
    nt.links.new(inv.outputs["Value"], mul.inputs[0])
    mul.inputs[1].default_value = 0.05
    color_mix(nt, mul.outputs["Value"], vc.outputs["Color"], lin((190, 196, 120)), bsdf.inputs["Base Color"])
    return m


# ------------------------------------------------------------------ build
def build():
    sc = fresh(samples=16)
    vines = [build_vine(V) for V in VINES]
    log("vines", [(tb["name"], round(tb["L_main"], 1), len(tb["P"])) for tb in vines])
    tendrils = [build_tendril(TD, vines) for TD in TENDRILS]
    leaves = [init_leaf(dict(LP)) for LP in LEAVES]
    petioles = [build_petiole(LP, vines) for LP in leaves]
    tubes = vines + tendrils + petioles
    # --- hi tubes
    acc = MeshAcc(want_uv=False, want_col=True)
    for ti, tb in enumerate(tubes):
        acc.tag = ti
        m = 96 if tb["kind"] == "vine" else (40 if tb["kind"] == "petiole" else 20)
        tube_hi(acc, tb, m)
    vhi = acc.build("VineGrip_Vines_hi")
    vhi.data.materials.append(mat_vine_hi())
    log("vines hi", len(vhi.data.polygons))
    # --- lo tubes
    acc = MeshAcc(want_uv=True)
    rings = {}
    for ti, tb in enumerate(tubes):
        acc.tag = ti
        if tb["kind"] == "vine":
            rings[tb["name"]] = tube_lo(acc, tb)
        elif tb["kind"] == "petiole":
            rings[tb["name"]] = tube_lo(acc, tb, seg_k=1.6, seg_min=0.35, seg_max=0.7, ang=18)
        else:
            rings[tb["name"]] = tube_lo(acc, tb, seg_k=2.0, seg_min=0.25, seg_max=0.5, ang=24)
    vlo = acc.build("VineGrip_Vines")
    tri = vlo.modifiers.new("Tri", "TRIANGULATE")
    apply_mods(vlo)
    log("vines lo tris", len(vlo.data.polygons), rings)
    # --- leaves
    pusher = Pusher(vines)
    acc_hi = MeshAcc(want_uv=True, want_col=True)
    acc_lo = MeshAcc(want_uv=True)
    for li, LP in enumerate(leaves):
        acc_hi.tag = acc_lo.tag = li
        segs = leaf_veins(LP)
        # hi
        P2, F, O = leaf_sheet2d(LP, True)
        vein, near = vein_field(P2, segs, LP["L"])
        kd = kdtree.KDTree(len(O))
        for i, p in enumerate(O):
            kd.insert((p[0], p[1], 0.0), i)
        kd.balance()
        dedge = [kd.find((x, y, 0.0))[2] for x, y in P2]
        cols, rough = leaf_colors(LP, P2, vein, near, dedge)
        X, Y, Z = leaf_frame(LP)
        base = Vector(LP["base"])
        W = []
        for k, (x, y) in enumerate(P2):
            h = leaf_h(LP, x, y) - (0.04 * LP["L"] / 6.0 + 0.012) * vein[k]
            W.append(base + X * x + Y * y + Z * h)
        W = [leaf_wall(pusher.push(leaf_wall(p), Z, 0.07)) for p in W]
        o = len(acc_hi.V)
        for k, p in enumerate(W):
            acc_hi.v(p, cols[k], rough[k][0])
        for f in F:
            acc_hi.f([o + i for i in f], [tuple(P2[i]) for i in f])
        # lo (same function, no veins)
        P2l, Fl, _ = leaf_sheet2d(LP, False)
        Wl = place_leaf(LP, P2l, pusher, False)
        o = len(acc_lo.V)
        for p in Wl:
            acc_lo.v(p)
        for f in Fl:
            acc_lo.f([o + i for i in f], [tuple(P2l[i]) for i in f])
        log("leaf", LP["name"], "hi v", len(P2), "lo tris", len(Fl))
    lhi = acc_hi.build("VineGrip_Leaves_hi")
    lhi.data.materials.append(mat_leaf_hi())
    llo = acc_lo.build("VineGrip_Leaves_top")
    log("leaves lo top tris", len(llo.data.polygons), "-> both sides", 2 * len(llo.data.polygons))
    log("normal check: vines inward faces", check_tube_normals(vlo, tubes), "| leaves faces against Z",
        check_leaf_normals(llo, leaves))
    bpy.ops.wm.save_as_mainfile(filepath=BLEND)
    return {"vines_lo": len(vlo.data.polygons), "leaves_lo_2sided": 2 * len(llo.data.polygons),
            "vines_hi": len(vhi.data.polygons), "leaves_hi": len(lhi.data.polygons)}


def check_tube_normals(ob, tubes):
    """Faces whose normal points toward their own centreline (= inside out). Caps are skipped."""
    kds = []
    for tb in tubes:
        kd = kdtree.KDTree(len(tb["P"]))
        for i, p in enumerate(tb["P"]):
            kd.insert(p, i)
        kd.balance()
        kds.append(kd)
    part = ob.data.attributes["part"].data
    bad = 0
    for f in ob.data.polygons:
        c = f.center
        co, i, d = kds[part[f.index].value].find(c)
        if d > 0.04 and f.normal.dot(c - co) < 0:
            bad += 1
    return bad


def check_leaf_normals(ob, leaves):
    part = ob.data.attributes["part"].data
    bad = 0
    for f in ob.data.polygons:
        X, Y, Z = leaf_frame(leaves[part[f.index].value])
        if f.normal.dot(Z) < -0.2:
            bad += 1
    return bad


# ------------------------------------------------------------------ review helpers
def wall_box(x0=-40, x1=40):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co = Vector(((x0 + x1) / 2 + v.co.x * (x1 - x0), (WY0 + WY1) / 2 + v.co.y * (WY1 - WY0),
                       (WZ0 + WZ1) / 2 + v.co.z * (WZ1 - WZ0)))
    ob = obj_from_bm(bm, "WallBox", smooth=False)
    ob.data.materials.append(mat_flat("WallMat", lin((96, 132, 170)), rough=0.8))
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=60)
    for v in bm.verts:
        v.co.z = WZ0
        v.co.y += 40
    fl = obj_from_bm(bm, "Floor", smooth=False)
    fl.data.materials.append(mat_flat("FloorMat", lin((92, 98, 104)), rough=0.9))
    return ob, fl


def review_light(front=True):
    sc = review_setup()
    sun = bpy.data.objects["Sun"]
    if front:
        sun.rotation_euler = (math.radians(-48), 0, math.radians(-28))
    sun.data.angle = math.radians(3)
    return sc


def preview():
    bpy.ops.wm.open_mainfile(filepath=BLEND)
    for n in ("VineGrip_Vines", "VineGrip_Leaves_top"):
        if n in bpy.data.objects:
            bpy.data.objects[n].hide_render = True
    review_light()
    wall_box()
    out = []
    out.append(shoot(os.path.join(OUT, "pre_hub.png"), (0, 0, -2.0), (0.12, 1, -0.42), 42, lens=40))
    out.append(shoot(os.path.join(OUT, "pre_close.png"), (-4, 0, -1.0), (0.35, 1, 0.1), 15, lens=40))
    out.append(shoot(os.path.join(OUT, "pre_top.png"), (0, -3, 0), (0.5, 0.5, 1.0), 30, lens=40))
    out.append(shoot(os.path.join(OUT, "pre_side.png"), (0, -4, -2), (1, 0.15, 0.25), 30, lens=40))
    return out


# ------------------------------------------------------------------ game meshes: UVs, bakes, underside
def pack_uv(ob, margin=0.004):
    only(ob)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.select_all(action="SELECT")
    bpy.ops.uv.pack_islands(rotate=True, rotate_method="ANY", scale=True, margin_method="SCALED", margin=margin,
                            shape_method="CONCAVE")
    bpy.ops.object.mode_set(mode="OBJECT")


def uv_usage(ob, size=256):
    """Fraction of the 0..1 UV square covered by triangles (rough raster)."""
    me = ob.data
    uv = np.zeros(len(me.loops) * 2, np.float32)
    me.uv_layers.active.data.foreach_get("uv", uv)
    uv = uv.reshape(-1, 2)
    img = np.zeros((size, size), bool)
    for p in me.polygons:
        ls = list(p.loop_indices)
        t = uv[ls] * size
        x0, y0 = np.floor(t.min(0)).astype(int)
        x1, y1 = np.ceil(t.max(0)).astype(int)
        xs, ys = np.meshgrid(np.arange(max(0, x0), min(size, x1 + 1)) + 0.5, np.arange(max(0, y0), min(size, y1 + 1)) + 0.5)
        if xs.size == 0:
            continue
        a, b, c = t[0], t[1], t[2]
        d = (b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])
        if abs(d) < 1e-12:
            continue
        l1 = ((b[1] - c[1]) * (xs - c[0]) + (c[0] - b[0]) * (ys - c[1])) / d
        l2 = ((c[1] - a[1]) * (xs - c[0]) + (a[0] - c[0]) * (ys - c[1])) / d
        inside = (l1 >= 0) & (l2 >= 0) & (l1 + l2 <= 1)
        img[ys[inside].astype(int), xs[inside].astype(int)] = True
    return round(float(img.mean()), 3)


def add_underside(ob, thick=0.04):
    """Leaves: a flipped copy of the (baked) top sheet, `thick` under it, sharing its UVs -> both faces render
    in Roblox without DoubleSided."""
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    bm.normal_update()
    orig = set(bm.verts)
    ret = bmesh.ops.duplicate(bm, geom=list(bm.faces) + list(bm.edges) + list(bm.verts))
    for k, v in ret["vert_map"].items():
        if k in orig:
            v.co = k.co - k.normal * thick
    newf = [g for g in ret["geom"] if isinstance(g, bmesh.types.BMFace)]
    bmesh.ops.reverse_faces(bm, faces=newf)
    bm.to_mesh(ob.data)
    bm.free()
    ob.data.shade_smooth()


def bake_box():
    """The wall, render-visible during the bakes so the AO darkens where vines and leaves touch it."""
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co = Vector((v.co.x * 90, (WY0 + WY1) / 2 + v.co.y * (WY1 - WY0), (WZ0 + WZ1) / 2 + v.co.z * (WZ1 - WZ0)))
    return obj_from_bm(bm, "_BakeWall", smooth=False)


def bake():
    bpy.ops.wm.open_mainfile(filepath=BLEND)
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = 48
    O = bpy.data.objects
    vlo, vhi = O["VineGrip_Vines"], O["VineGrip_Vines_hi"]
    llo, lhi = O["VineGrip_Leaves_top"], O["VineGrip_Leaves_hi"]
    rep = {}
    for ob in (vlo, llo):
        pack_uv(ob)
        rep["uv_used_" + ob.name] = uv_usage(ob)
    log("uv packed", rep)
    wall = bake_box()
    llo.hide_render = True
    t = time.time()
    imgs = bake_set(vlo, [vhi], 1024, "VineGrip_Vines", cage=0.12, maxray=0.42, ao_strength=0.6, ao_dist=1.6,
                    outdir=MAPS)
    rep["vines_miss"] = round(imgs["miss_fraction"], 4)
    log("vines baked", round(time.time() - t, 1), "s, miss", rep["vines_miss"])
    pbr_material(vlo, "VineGrip_Vines_PBR", imgs)
    llo.hide_render = False
    vlo.hide_render = True
    t = time.time()
    imgs2 = bake_set(llo, [lhi], 1024, "VineGrip_Leaves", cage=0.1, maxray=0.32, ao_strength=0.5, ao_dist=1.6,
                     outdir=MAPS)
    rep["leaves_miss"] = round(imgs2["miss_fraction"], 4)
    log("leaves baked", round(time.time() - t, 1), "s, miss", rep["leaves_miss"])
    vlo.hide_render = False
    add_underside(llo)
    llo.name = "VineGrip_Leaves"
    llo.data.name = "VineGrip_Leaves"
    pbr_material(llo, "VineGrip_Leaves_PBR", imgs2)
    bpy.data.objects.remove(wall)
    for o in (vhi, lhi):
        o.hide_render = True
        o.hide_viewport = True
    for o in (vlo, llo):
        if "part" in o.data.attributes:
            o.data.attributes.remove(o.data.attributes["part"])
        rep["tris_" + o.name] = len(o.data.polygons)
        rep["bbox_" + o.name] = bbox(o)
    bpy.ops.wm.save_as_mainfile(filepath=BLEND)
    return rep


def bbox(o):
    V = np.zeros(len(o.data.vertices) * 3, np.float32)
    o.data.vertices.foreach_get("co", V)
    V = V.reshape(-1, 3)
    return {"min": [round(float(x), 2) for x in V.min(0)], "max": [round(float(x), 2) for x in V.max(0)]}


def render():
    bpy.ops.wm.open_mainfile(filepath=BLEND)
    review_light()
    wall_box()
    out = []
    out.append(shoot(os.path.join(OUT, "review_hub.png"), (0, 0, -2.0), (0.12, 1, -0.42), 42, lens=40))
    out.append(shoot(os.path.join(OUT, "review_close.png"), (-4.5, 0.5, -1.2), (0.45, 1, 0.02), 12.5, lens=40))
    out.append(shoot(os.path.join(OUT, "review_34.png"), (0, -2.5, 0.0), (0.85, 1, 0.45), 33, lens=40))
    # the same hub view with the kit's default sun (from behind the wall): the inner face in shade
    bpy.data.objects["Sun"].rotation_euler = (math.radians(50), 0, math.radians(30))
    out.append(shoot(os.path.join(OUT, "review_hub_backlit.png"), (0, 0, -2.0), (0.12, 1, -0.42), 42, lens=40))
    return out


def export():
    bpy.ops.wm.open_mainfile(filepath=BLEND)
    objs = [bpy.data.objects[n] for n in ("VineGrip_Vines", "VineGrip_Leaves")]
    return export_fbx(objs, FBX)


FBX_M = os.path.join(CDIMP, "Halloween_VineGripMirror.fbx")


def mirror_copies():
    """True X-mirror (Roblox cannot mirror a MeshPart). Same maps: the flipped UV winding makes the tangent
    handedness flip, so the normal map still reads right."""
    out = []
    for n in ("VineGrip_Vines", "VineGrip_Leaves"):
        src = bpy.data.objects[n]
        me = src.data.copy()
        me.transform(Matrix.Scale(-1.0, 4, (1.0, 0.0, 0.0)))
        me.flip_normals()
        me.name = n.replace("VineGrip_", "VineGripM_")
        ob = link(bpy.data.objects.new(me.name, me))
        out.append(ob)
    return out


def export_mirror():
    bpy.ops.wm.open_mainfile(filepath=BLEND)
    objs = mirror_copies()
    return export_fbx(objs, FBX_M)


def render_pair():
    """Both grips on a long wall with backface culling ON (like Roblox): checks the mirror is not inside out."""
    bpy.ops.wm.open_mainfile(filepath=BLEND)
    review_light()
    wall_box(-60, 60)
    O = bpy.data.objects
    m = mirror_copies()
    for o in (O["VineGrip_Vines"], O["VineGrip_Leaves"]):
        o.location.x += 22
    for o in m:
        o.location.x -= 22
    for mat in bpy.data.materials:
        mat.use_backface_culling = True
    return [shoot(os.path.join(OUT, "review_pair_culled.png"), (0, 0, -3.0), (0.0, 1, -0.38), 78, lens=40)]


def attach_points():
    fresh(4)
    pts = {}
    for V in VINES:
        tb = build_vine(V)
        n = tb["main_n"]
        L = tb["L_main"]
        ih = int(V["t_hump"] * (n - 1))
        ij = int(V["t_joint"] * (n - 1))
        pts[V["name"]] = {"knuckle_top": tuple(round(c, 2) for c in tb["P"][ih] + Vector((0, 0, tb["R"][ih] * 1.3))),
                          "finger_joint": tuple(round(c, 2) for c in tb["P"][ij]),
                          "claw_tip": tuple(round(c, 2) for c in tb["P"][n - 1]),
                          "coil_end": tuple(round(c, 2) for c in tb["P"][-1])}
    return pts


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else ["build"]
    rep = {}
    for step in argv:
        if step == "build":
            rep["build"] = build()
        elif step == "preview":
            rep["preview"] = preview()
        elif step == "bake":
            rep["bake"] = bake()
        elif step == "render":
            rep["render"] = render()
        elif step == "export":
            rep["export"] = export()
        elif step == "mirror":
            rep["mirror"] = export_mirror()
        elif step == "pair":
            rep["pair"] = render_pair()
        elif step == "points":
            rep["points"] = attach_points()
    print("HW_REPORT " + json.dumps(rep))
    with open(os.path.join(OUT, "build_log.txt"), "a") as fh:
        fh.write("\n".join(LOG) + "\nHW_REPORT " + json.dumps(rep) + "\n")
