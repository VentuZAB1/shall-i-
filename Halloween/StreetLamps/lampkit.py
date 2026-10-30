# SLINGSHOT Halloween STREET LAMP - helper kit (2026-10-13).
# hkit.py / pumpkin.py are imported READ-ONLY. Helpers marked "copied from eggs/webs/treekit" are verbatim copies (or
# copies with output paths pointed at StreetLamps\) of PumpkinEggs\eggs.py, WebsSpiders\webs_spiders.py and
# DeadTrees\treekit.py - those files are not touched.
import sys, os, json, time, math, random
sys.path.insert(0, r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween")
from hkit import *  # noqa: F401,F403  (lin, smoothstep, fbm, mix, fresh, link, only, apply_mods, obj_from_bm, ...)
from pumpkin import SKIN, grin  # noqa: F401  read-only helpers
import bpy, bmesh
import numpy as np
from mathutils import Vector, Matrix, noise, geometry
from mathutils.bvhtree import BVHTree

OUT = os.path.join(HERE, "StreetLamps")
MAPS = os.path.join(OUT, "maps")
WIP = os.path.join(OUT, "wip")
for _d in (MAPS, WIP):
    os.makedirs(_d, exist_ok=True)
T0 = time.time()
CFG = {"fast": False, "debug": False}


def log(*a):
    print("[lamp %7.1fs]" % (time.time() - T0), *a, flush=True)


# ===================================================================== small math
def wrap(a):
    return (a + math.pi) % (2 * math.pi) - math.pi


def smax(a, b, k):
    h = max(k - abs(a - b), 0.0) / k
    return max(a, b) + h * h * k * 0.25


def sstep(a, b, x):
    """numpy smoothstep."""
    t = np.clip((x - a) / (b - a), 0.0, 1.0)
    return t * t * (3 - 2 * t)


def pal(**kw):
    return {k: lin(v) for k, v in kw.items()}


def catmull(pts, n_per, alpha=0.5):
    """Centripetal Catmull-Rom through pts (list of tuples/np rows), n_per samples per segment. Returns np array."""
    P = np.array(pts, float)
    P = np.vstack([2 * P[0] - P[1], P, 2 * P[-1] - P[-2]])
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]

        def tj(ti, a, b):
            return ti + max(np.linalg.norm(b - a), 1e-6) ** alpha
        t0 = 0.0
        t1 = tj(t0, p0, p1)
        t2 = tj(t1, p1, p2)
        t3 = tj(t2, p2, p3)
        ts = np.linspace(t1, t2, n_per, endpoint=False)[:, None]
        A1 = (t1 - ts) / (t1 - t0) * p0 + (ts - t0) / (t1 - t0) * p1
        A2 = (t2 - ts) / (t2 - t1) * p1 + (ts - t1) / (t2 - t1) * p2
        A3 = (t3 - ts) / (t3 - t2) * p2 + (ts - t2) / (t3 - t2) * p3
        B1 = (t2 - ts) / (t2 - t0) * A1 + (ts - t0) / (t2 - t0) * A2
        B2 = (t3 - ts) / (t3 - t1) * A2 + (ts - t1) / (t3 - t1) * A3
        out.append((t2 - ts) / (t2 - t1) * B1 + (ts - t1) / (t2 - t1) * B2)
    out.append(P[-2][None, :])
    return np.vstack(out)


def resample_poly(P, step=None, n=None):
    """Resample a polyline (np (k,d)) evenly by arc length."""
    P = np.asarray(P, float)
    d = np.linalg.norm(np.diff(P, axis=0), axis=1)
    s = np.concatenate([[0], np.cumsum(d)])
    if n is None:
        n = max(2, int(math.ceil(s[-1] / step)) + 1)
    t = np.linspace(0, s[-1], n)
    return np.stack([np.interp(t, s, P[:, k]) for k in range(P.shape[1])], 1), t


def adaptive_samples(P, R_local, sag=0.003, max_len=0.3, extra=(), max_turn=None):
    """Pick indices of a dense polyline P (np (k,d)) so that the chord sag stays <= sag (using the local radius of
    curvature R_local per dense point) and no segment is longer than max_len. extra = arc-length positions forced in.
    max_turn (deg): also cap the true turning of the dense polyline between two kept points."""
    d = np.linalg.norm(np.diff(P, axis=0), axis=1)
    s = np.concatenate([[0], np.cumsum(d)])
    tg = np.diff(P, axis=0) / np.maximum(d, 1e-12)[:, None]
    turn = np.concatenate([[0.0], np.degrees(np.arccos(np.clip(np.sum(tg[1:] * tg[:-1], axis=1), -1, 1))), [0.0]])
    keep = [0]
    acc_ang, last_s, acc_turn = 0.0, 0.0, 0.0
    for i in range(1, len(P)):
        R = max(R_local[i], 1e-4)
        dth_max = 2 * math.acos(max(-1.0, 1 - sag / R)) if R > sag else math.pi
        acc_ang += d[i - 1] / R
        acc_turn += turn[i - 1] if i - 1 < len(turn) else 0.0
        if acc_ang >= dth_max or s[i] - last_s >= max_len or (max_turn is not None and acc_turn >= max_turn):
            keep.append(i)
            acc_ang, last_s, acc_turn = 0.0, s[i], 0.0
    if keep[-1] != len(P) - 1:
        if s[-1] - s[keep[-1]] < 0.3 * max_len and len(keep) > 1:
            keep[-1] = len(P) - 1
        else:
            keep.append(len(P) - 1)
    for e in extra:
        i = int(np.argmin(abs(s - e)))
        if i not in keep:
            keep.append(i)
    return np.array(sorted(set(keep)))


def polyline_curv_radius(P, k=1):
    """Radius of curvature at each point of a dense polyline (circle through the points k before / k after)."""
    P = np.asarray(P, float)
    R = np.full(len(P), 1e6)
    if len(P) < 2 * k + 1:
        k = 1
    a, b, c = P[:-2 * k], P[k:-k], P[2 * k:]
    ab, bc, ca = (np.linalg.norm(b - a, axis=1), np.linalg.norm(c - b, axis=1), np.linalg.norm(a - c, axis=1))
    if P.shape[1] == 2:
        cr = np.abs((b - a)[:, 0] * (c - a)[:, 1] - (b - a)[:, 1] * (c - a)[:, 0])
    else:
        cr = np.linalg.norm(np.cross(b - a, c - a), axis=1)
    with np.errstate(divide="ignore", invalid="ignore"):
        r = ab * bc * ca / np.maximum(2 * cr, 1e-12)
    R[k:-k] = np.where(cr > 1e-12, r, 1e6)
    R[:k], R[-k:] = R[k], R[-k - 1]
    return R


def frames_planar(P, N_plane):
    """Tangents + in-plane normal B for a curve lying in a plane with normal N_plane. Returns T, N, B (N = plane
    normal, constant)."""
    P = np.asarray(P, float)
    T = np.gradient(P, axis=0)
    T /= np.linalg.norm(T, axis=1)[:, None]
    N = np.tile(np.asarray(N_plane, float), (len(P), 1))
    B = np.cross(T, N)
    B /= np.linalg.norm(B, axis=1)[:, None]
    return T, N, B


def frames_transport(P, ref=(0, 0, 1)):
    """Parallel-transport frames along a 3D polyline."""
    P = np.asarray(P, float)
    T = np.gradient(P, axis=0)
    T /= np.linalg.norm(T, axis=1)[:, None]
    ref = np.asarray(ref, float)
    n0 = ref - T[0] * ref.dot(T[0])
    if np.linalg.norm(n0) < 1e-3:
        ref = np.array([1.0, 0, 0])
        n0 = ref - T[0] * ref.dot(T[0])
    n0 /= np.linalg.norm(n0)
    N = [n0]
    for i in range(1, len(P)):
        n = N[-1] - T[i] * N[-1].dot(T[i])
        ln = np.linalg.norm(n)
        n = n / ln if ln > 1e-9 else N[-1]
        N.append(n)
    N = np.array(N)
    B = np.cross(T, N)
    return T, N, B


# ===================================================================== numpy mesh accumulator
ATTR_NAMES = ("Col", "Rough", "Wear")


class Acc:
    """Accumulates verts (+ per-vertex Col / Rough / Wear) and faces (tris / quads) with per-loop UVs, material index
    and smooth flags; build() makes one Blender mesh object. UV islands: each add_* call can take an island offset so
    separate pieces never share UV coordinates."""

    def __init__(self, attrs=True):
        self.attrs = attrs
        self.V, self.A = [], {k: [] for k in ATTR_NAMES}
        self.faces = []      # (idx (nf,k), uv (nf,k,2), mat (nf,), smooth (nf,))
        self.n = 0
        self.isl = 0

    def new_island(self):
        self.isl += 1
        return np.array([self.isl * 3.0, 0.0])

    def add_v(self, P, at=None):
        P = np.asarray(P, float).reshape(-1, 3)
        base = self.n
        self.V.append(P)
        if self.attrs:
            k = len(P)
            for nm in ATTR_NAMES:
                if at is not None and nm in at:
                    self.A[nm].append(np.asarray(at[nm], float).reshape(k, 3))
                else:
                    dflt = {"Col": 0.03, "Rough": 0.6, "Wear": 0.0}[nm]
                    self.A[nm].append(np.full((k, 3), dflt))
        self.n += len(P)
        return base

    def add_faces(self, idx, uv, mat=0, smooth=True):
        idx = np.asarray(idx, np.int64)
        uv = np.asarray(uv, float)
        nf = len(idx)
        m = np.full(nf, mat, np.int64) if np.isscalar(mat) else np.asarray(mat, np.int64)
        sm = np.full(nf, bool(smooth)) if np.isscalar(smooth) else np.asarray(smooth, bool)
        self.faces.append((idx, uv, m, sm))

    def add_grid(self, G, uvg, at=None, closed_j=True, mat=0, smooth=True, centres=None, flip=None):
        """G (ni, nj, 3). uvg (ni, nj+1, 2) when closed_j (the last column = the seam copy) else (ni, nj, 2).
        centres (ni, 3): ring centres used to orient faces outward (if flip is None)."""
        ni, nj = G.shape[:2]
        flat_at = None if at is None else {k: v.reshape(-1, 3) for k, v in at.items()}
        base = self.add_v(G.reshape(-1, 3), flat_at)
        jn = nj if closed_j else nj - 1
        I, J = np.meshgrid(np.arange(ni - 1), np.arange(jn), indexing="ij")
        J1 = (J + 1) % nj
        a = base + I * nj + J
        b = base + I * nj + J1
        c = base + (I + 1) * nj + J1
        d = base + (I + 1) * nj + J
        q = np.stack([a, b, c, d], -1).reshape(-1, 4)
        uq = np.stack([uvg[I, J], uvg[I, J + 1], uvg[I + 1, J + 1], uvg[I + 1, J]], -2).reshape(-1, 4, 2)
        if flip is None and centres is not None:
            V = G.reshape(-1, 3)
            loc = q - base
            p0, p1, p2, p3 = (V[loc[:, k]] for k in range(4))
            nrm = np.cross(p2 - p0, p3 - p1)
            cen = (p0 + p1 + p2 + p3) / 4
            cc = np.asarray(centres, float)[I.ravel()]
            flip = float(np.sum(np.einsum("ij,ij->i", nrm, cen - cc))) < 0
        if flip:
            q = q[:, ::-1]
            uq = uq[:, ::-1]
        self.add_faces(q, uq, mat, smooth)
        return base, bool(flip)

    def add_fan(self, ring_idx, centre, uv_ring, uv_c, at_c=None, mat=0, smooth=True, outward=None):
        """Fan from a ring of existing vertex indices to a new centre vertex. outward: a direction the fan normal
        should point along."""
        c = self.add_v(np.asarray(centre, float)[None, :], at_c)
        k = len(ring_idx)
        tri = np.stack([ring_idx, np.roll(ring_idx, -1), np.full(k, c)], 1)
        uvr = np.asarray(uv_ring, float)
        uvt = np.stack([uvr, np.roll(uvr, -1, axis=0), np.tile(uv_c, (k, 1))], 1)
        if outward is not None:
            V = self._vcat()
            p0, p1, p2 = V[tri[0, 0]], V[tri[0, 1]], V[tri[0, 2]]
            if np.dot(np.cross(p1 - p0, p2 - p0), outward) < 0:
                tri = tri[:, ::-1]
                uvt = uvt[:, ::-1]
        self.add_faces(tri, uvt, mat, smooth)
        return c

    def _vcat(self):
        return np.vstack(self.V)

    def merge_mesh(self, V, F, UV, at=None, mat=0, smooth=True):
        """Add an arbitrary triangle/quad list (F: list of index lists local to V; UV per corner)."""
        base = self.add_v(V, at)
        tris = [(f, u) for f, u in zip(F, UV) if len(f) == 3]
        quads = [(f, u) for f, u in zip(F, UV) if len(f) == 4]
        for group, k in ((tris, 3), (quads, 4)):
            if group:
                idx = np.array([g[0] for g in group]) + base
                uv = np.array([g[1] for g in group], float).reshape(-1, k, 2)
                m = mat if np.isscalar(mat) else np.asarray(mat)
                self.add_faces(idx, uv, m, smooth)
        return base

    def tris(self):
        return int(sum(len(f[0]) * (f[0].shape[1] - 2) for f in self.faces))

    def build(self, name, mats=(), attrs=None):
        V = self._vcat()
        tri = [f for f in self.faces if f[0].shape[1] == 3]
        qua = [f for f in self.faces if f[0].shape[1] == 4]
        idx, uvs, mm, sm, sizes = [], [], [], [], []
        for group, k in ((tri, 3), (qua, 4)):
            for f in group:
                idx.append(f[0].ravel())
                uvs.append(f[1].reshape(-1, 2))
                mm.append(f[2])
                sm.append(f[3])
                sizes.append(np.full(len(f[0]), k))
        idx = np.concatenate(idx)
        uvs = np.concatenate(uvs)
        mm = np.concatenate(mm)
        sm = np.concatenate(sm)
        sizes = np.concatenate(sizes)
        me = bpy.data.meshes.new(name)
        me.vertices.add(len(V))
        me.vertices.foreach_set("co", V.astype(np.float32).ravel())
        me.loops.add(len(idx))
        me.loops.foreach_set("vertex_index", idx.astype(np.int32))
        me.polygons.add(len(sizes))
        starts = np.concatenate([[0], np.cumsum(sizes)[:-1]]).astype(np.int32)
        me.polygons.foreach_set("loop_start", starts)
        me.update(calc_edges=True)
        uv = me.uv_layers.new(name="UVMap")
        uv.data.foreach_set("uv", uvs.astype(np.float32).ravel())
        me.polygons.foreach_set("material_index", mm.astype(np.int32))
        try:
            me.polygons.foreach_set("use_smooth", sm)
        except Exception:
            sf = me.attributes.new("sharp_face", "BOOLEAN", "FACE")
            sf.data.foreach_set("value", ~sm)
        if self.attrs and (attrs is None or attrs):
            for nm in ATTR_NAMES:
                arr = np.ones((len(V), 4), np.float32)
                arr[:, :3] = np.vstack(self.A[nm])
                ca = me.color_attributes.new(nm, "FLOAT_COLOR", "POINT")
                ca.data.foreach_set("color", arr.ravel())
        for m in mats:
            me.materials.append(m)
        me.update()
        return link(bpy.data.objects.new(name, me))


# ===================================================================== sweeps
def sweep_grid(P, Nf, Bf, sections):
    """P (ni,3) path; Nf, Bf (ni,3) frame axes; sections (ni, nj, 2) local (a, b) offsets -> G (ni, nj, 3)."""
    S = np.asarray(sections, float)
    return P[:, None, :] + S[..., 0:1] * Nf[:, None, :] + S[..., 1:2] * Bf[:, None, :]


def section_uv(S, v, closed=True):
    """UVs for a sweep: u = cumulative section perimeter (studs) per ring, v = arc length. S (ni,nj,2) local section
    coords, v (ni,). Returns (ni, nj+1, 2) when closed."""
    S = np.asarray(S, float)
    if closed:
        Sc = np.concatenate([S, S[:, :1]], 1)
    else:
        Sc = S
    seg = np.linalg.norm(np.diff(Sc, axis=1), axis=2)
    u = np.concatenate([np.zeros((len(S), 1)), np.cumsum(seg, 1)], 1)
    # centre the u range per ring so tapering tubes stay symmetric islands
    u = u - u[:, -1:] / 2 + u[:, -1:].max() / 2
    return np.stack([u, np.repeat(np.asarray(v, float)[:, None], u.shape[1], 1)], -1)


def circle_section(r, n, phase=0.0):
    a = phase + 2 * math.pi * np.arange(n) / n
    r = np.asarray(r, float).reshape(-1, 1)
    return np.stack([r * np.cos(a)[None, :], r * np.sin(a)[None, :]], -1)


def rrect(w, h, n_corner=1, cr=None):
    """Rounded rectangle section points (a along w, b along h), counter-clockwise. n_corner = points per corner
    (1 -> chamfer: 8 verts)."""
    cr = cr if cr is not None else min(w, h) * 0.3
    hw, hh = w / 2, h / 2
    pts = []
    for cx, cy, a0 in ((hw - cr, hh - cr, 0.0), (-hw + cr, hh - cr, 90.0), (-hw + cr, -hh + cr, 180.0),
                       (hw - cr, -hh + cr, 270.0)):
        for k in range(n_corner + 1):
            a = math.radians(a0 + 90.0 * k / n_corner)
            pts.append((cx + cr * math.cos(a), cy + cr * math.sin(a)))
    return np.array(pts)


def grid_curvature(G, closed_j=True, flipped=False):
    """Principal-ish curvature of a structured grid along i and along j (signed: + = convex). Returns (k_i, k_j,
    normals)."""
    G = np.asarray(G, float)
    if closed_j:
        Gj_p, Gj_m = np.roll(G, -1, 1), np.roll(G, 1, 1)
    else:
        Gj_p = np.concatenate([G[:, 1:], G[:, -1:]], 1)
        Gj_m = np.concatenate([G[:, :1], G[:, :-1]], 1)
    Gi_p = np.concatenate([G[1:], G[-1:]], 0)
    Gi_m = np.concatenate([G[:1], G[:-1]], 0)
    dj = Gj_p - Gj_m
    di = Gi_p - Gi_m
    n = np.cross(dj, di)
    ln = np.linalg.norm(n, axis=2, keepdims=True)
    n = n / np.maximum(ln, 1e-12)
    if flipped:
        n = -n

    def k2(pp, p, pm):
        d1 = np.linalg.norm(p - pm, axis=2, keepdims=True)
        d2 = np.linalg.norm(pp - p, axis=2, keepdims=True)
        sec = 2 * (d1 * pp + d2 * pm - (d1 + d2) * p) / np.maximum(d1 * d2 * (d1 + d2), 1e-12)
        return -np.einsum("ijk,ijk->ij", sec, n)
    kj = k2(Gj_p, G, Gj_m)
    ki = k2(Gi_p, G, Gi_m)
    ki[0] = ki[1]
    ki[-1] = ki[-2]
    if not closed_j:
        kj[:, 0] = kj[:, 1]
        kj[:, -1] = kj[:, -2]
    return ki, kj, n


def blur_grid(A, closed_j=True, it=1):
    A = np.asarray(A, float)
    for _ in range(it):
        if closed_j:
            Aj = (np.roll(A, 1, 1) + np.roll(A, -1, 1) + 2 * A) / 4
        else:
            Aj = A.copy()
            Aj[:, 1:-1] = (A[:, :-2] + A[:, 2:] + 2 * A[:, 1:-1]) / 4
        Ai = Aj.copy()
        Ai[1:-1] = (Aj[:-2] + Aj[2:] + 2 * Aj[1:-1]) / 4
        A = Ai
    return A


# ===================================================================== iron shading (per-vertex, hi only)
IRON = pal(base=(40, 43, 50), hi=(52, 55, 62), deep=(24, 25, 30), wear=(96, 101, 112), rust=(92, 50, 30),
           rust2=(150, 80, 40))


def noise_fields(P, seed=0):
    """Per-vertex noise fields (python loop over mathutils noise): tone, wear breakup, rust breakup, bloom."""
    off = Vector((seed * 13.1, seed * 7.7, seed * 3.3))
    n = len(P)
    tone, wb, rb, bloom = (np.empty(n) for _ in range(4))
    for i in range(n):
        p = Vector(P[i])
        q = p + off
        tone[i] = fbm(q * 1.3, 3)
        wb[i] = noise.noise(q * 9.0 + Vector((3.1, 0.0, 0.0)))
        rb[i] = fbm(q * 4.2 + Vector((0.0, 5.3, 0.0)), 3)
        bloom[i] = noise.noise(q * 13.0 + Vector((0.0, 0.0, 7.7)))
    return tone, wb, rb, bloom


def iron_shade(P, conv, conc, seed=0, wear_extra=None, rust_extra=None, wear_k=(14.0, 40.0), crev_k=(10.0, 35.0),
               rust_amt=0.8, wear_amt=0.85, rust_mask=None):
    """P (n,3); conv/conc (n,) convex / concave curvature magnitudes (1/stud). Returns Col, Rough, Wear (n,3)."""
    tone, wb, rb, bloom = noise_fields(P, seed)
    edge = sstep(wear_k[0], wear_k[1], conv)
    if wear_extra is not None:
        edge = np.maximum(edge, wear_extra)
    wear = edge * sstep(-0.25, 0.35, wb) * wear_amt
    crev = sstep(crev_k[0], crev_k[1], conc)
    rust = crev * sstep(0.0, 0.45, rb) * rust_amt
    if rust_extra is not None:
        rust = np.maximum(rust, rust_extra * sstep(-0.2, 0.4, rb))
    if rust_mask is not None:
        rust = rust * np.asarray(rust_mask, float)
    rust = np.clip(rust, 0, 1)
    base = np.array(IRON["base"])[None, :]
    hi = np.array(IRON["hi"])[None, :]
    t = np.clip(0.5 + 0.55 * tone, 0, 1)[:, None]
    col = base * (1 - t) + hi * t
    col = col * (1 - 0.55 * crev[:, None]) + np.array(IRON["deep"])[None, :] * 0.55 * crev[:, None]
    rustc = np.array(IRON["rust"])[None, :] * (1 - 0.45 * sstep(0.2, 0.7, bloom))[:, None] + \
        np.array(IRON["rust2"])[None, :] * 0.45 * sstep(0.2, 0.7, bloom)[:, None]
    col = col * (1 - rust[:, None]) + rustc * rust[:, None]
    col = col * (1 - wear[:, None]) + np.array(IRON["wear"])[None, :] * wear[:, None]
    rough = np.clip(0.62 + 0.05 * tone - 0.26 * wear + 0.25 * rust + 0.08 * crev, 0.3, 0.95)
    return col, np.repeat(rough[:, None], 3, 1), np.repeat(np.clip(wear * 1.15, 0, 1)[:, None], 3, 1)


# ===================================================================== copied from PumpkinEggs\eggs.py
def egg_field(P, pl):
    """(copied from eggs.py) surface point / colour / roughness for a unit direction d."""
    rng = random.Random(P["seed"])
    off = Vector((rng.uniform(-50, 50), rng.uniform(-50, 50), rng.uniform(-50, 50)))
    off2 = Vector((rng.uniform(-50, 50), rng.uniform(-50, 50), rng.uniform(-50, 50)))
    N = P["N"]
    ribvar = [rng.uniform(-1, 1) for _ in range(N)]
    phase = rng.uniform(0, 1)
    phase = P.get("phase", phase)
    R, Rz, eg = P["R"], P["Rz"], P.get("egg", 0.0)
    zb = -P.get("flat", 9.0) * Rz
    fk = P.get("flat_k", 0.2) * Rz
    micro, scrape = P.get("micro", 0.0), P.get("scrape", 0.0)
    streak, samt = P.get("streak"), P.get("streak_amt", 0.0)
    radd = P.get("rough_add", 0.0)

    def f(d):
        th = math.acos(max(-1.0, min(1.0, d.z)))
        ph = math.atan2(d.y, d.x)
        s = math.sin(th)
        u = N * ph / (2 * math.pi) + phase
        k = math.floor(u + 0.5)
        fr = u - k
        kk = int(k) % N
        rv = ribvar[kk]
        bulge = max(0.0, math.cos(math.pi * fr)) ** P["crest"]
        depth = P["depth"] * (s ** 0.7) * (1 + 0.3 * rv)
        m = 1.0 - depth * (1.0 - bulge)
        m *= 1.0 + 0.03 * rv * s
        m *= 1.0 + P["lumps"] * fbm(d * 1.4 + off, 3)
        if micro:
            stri = noise.noise(Vector((fr * 10.0 + kk * 3.7, th * 2.4, 1.7)))
            m *= 1.0 + micro * (0.9 * stri * s + 0.6 * fbm(d * 24.0 + off2, 3))
        if scrape:
            q = Vector((math.cos(ph) * 2.2 * N, math.sin(ph) * 2.2 * N, th * 1.3)) + off2
            m *= 1.0 + scrape * (noise.noise(q) + 0.5 * noise.noise(q * 2.7))
        w = 1 - eg * d.z
        x, y = d.x * m * R * w, d.y * m * R * w
        z = d.z * Rz * (1 + 0.45 * (m - 1))
        z -= P["dtop"] * Rz * math.exp(-(th / P["dtop_w"]) ** 2)
        if zb > -Rz:
            z = smax(z, zb, fk)
        z += P["dbot"] * Rz * math.exp(-((math.pi - th) / 0.5) ** 2)
        col = mix(pl["groove"], pl["crest"], bulge ** 0.55)
        sk = noise.noise(Vector((fr * 16.0 + kk * 5.1, th * 3.3, 9.1)))
        col = mix(col, pl["light"], 0.42 * smoothstep(0.1, 0.6, sk) * bulge)
        tone = fbm(d * 1.1 + off2, 2)
        col = mix(col, pl["red"] if tone < 0 else pl["gold"], min(1.0, abs(tone) * 0.9))
        col = mix(col, pl["bottom"], 0.45 * smoothstep(2.3, 3.0, th))
        col = mix(col, pl["top"], 0.85 * math.exp(-(th / (P["dtop_w"] * 0.85)) ** 2))
        if streak:
            sn = 0.5 + 0.5 * noise.noise(Vector((fr * 5.0 + kk * 2.3, th * 4.0, 3.3)) + off)
            col = mix(col, streak, samt * (1 - bulge) ** 1.2 * smoothstep(0.3, 0.7, sn) * s)
        bl = smoothstep(0.55, 0.75, fbm(d * 9.0 + off2 * 0.7, 3)) * P.get("blemish", 1.0)
        col = mix(col, pl["blemish"], 0.3 * bl)
        r = 0.38 + 0.22 * (1 - bulge) + 0.32 * bl + radd
        return Vector((x, y, z)), col, (r, r, r)
    return f


def inner_params(P, t):
    """(copied from eggs.py)"""
    R, Rz = P["R"], P["Rz"]
    Ri, Rzi = R - t, Rz - t
    zb = -P["flat"] * Rz
    return dict(P, R=Ri, Rz=Rzi, depth=P["depth"] * 0.55, lumps=P["lumps"] * 0.8, micro=0.0,
                dtop=P["dtop"] * Rz / Rzi, flat=(-zb - t) / Rzi, dbot=0.0)


def grooves_az(N, phase, useg):
    out = []
    for j in range(useg):
        u = N * j / useg + phase
        if abs((u - math.floor(u)) - 0.5) < 1e-6:
            out.append(round(360.0 * j / useg, 4))
    return out


def pick_seams(N, phase, usegs, wants):
    common = set(grooves_az(N, phase, usegs[0]))
    for u in usegs[1:]:
        common &= set(grooves_az(N, phase, u))
    common = sorted(common)
    assert common, "no groove sits on a vertex column"
    return [min(common, key=lambda a: abs((a - w + 180) % 360 - 180)) for w in wants]


def sphere_surface(field, useg, vseg, flip=False):
    """(copied from eggs.py)"""
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
        ring = []
        for j in range(useg):
            ph = 2 * math.pi * j / useg
            ring.append(add(Vector((math.sin(th) * math.cos(ph), math.sin(th) * math.sin(ph), math.cos(th)))))
        rings.append(ring)
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
    if flip:
        F = [tuple(reversed(f)) for f in F]
    return V, F, C, Rr


def make_obj(name, V, F, C=None, Rr=None, mats=(), fmat=None, recalc=False, smooth=True, extra=None):
    """(copied from eggs.py)"""
    me = bpy.data.meshes.new(name)
    me.from_pydata([tuple(v) for v in V], [], [tuple(f) for f in F])
    me.update()
    if C:
        set_colors(me, "Col", C)
    if Rr:
        set_colors(me, "Rough", Rr)
    for nm, vals in (extra or {}).items():
        set_colors(me, nm, vals)
    for m in mats:
        me.materials.append(m)
    if fmat is not None:
        me.polygons.foreach_set("material_index", fmat)
    ob = link(bpy.data.objects.new(name, me))
    if recalc:
        bm = bmesh.new()
        bm.from_mesh(me)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bm.to_mesh(me)
        bm.free()
    if smooth:
        me.shade_smooth()
    return ob


def build_mesh(name, parts, mats):
    """(copied from eggs.py)"""
    V, F, C, Rr, fm, D = [], [], [], [], [], []
    for pv, pf, pc, pr, mi, dep in parts:
        o = len(V)
        V += pv
        C += pc
        Rr += pr
        D += [(dep, dep, dep)] * len(pv)
        F += [tuple(i + o for i in f) for f in pf]
        fm += [mi] * len(pf)
    return make_obj(name, V, F, C, Rr, mats=mats, fmat=fm, extra={"Depth": D})


def knife(ob, wall=2):
    """(copied from eggs.py)"""
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    for f in bm.faces:
        f.smooth = f.material_index != wall
    for e in bm.edges:
        lf = e.link_faces
        if len(lf) == 2 and lf[0].material_index != lf[1].material_index:
            e.smooth = False
    bm.to_mesh(ob.data)
    bm.free()


def repair_attrs(ob, wall=2, names=("Col", "Rough", "Depth")):
    """(copied from eggs.py) refill the colour attributes the EXACT boolean leaves at 0 on new cut vertices."""
    me = ob.data
    arrs = {}
    for nm in names:
        a = me.color_attributes.get(nm)
        if a is not None:
            arr = np.empty(len(a.data) * 4, np.float32)
            a.data.foreach_get("color", arr)
            arrs[nm] = arr.reshape(-1, 4)
    valid = arrs["Col"][:, 3] > 0.5
    nbad = int((~valid).sum())
    if nbad:
        bm = bmesh.new()
        bm.from_mesh(me)
        bm.verts.ensure_lookup_table()
        nb = {}
        for i in np.nonzero(~valid)[0]:
            v = bm.verts[int(i)]
            nb[int(i)] = [e.other_vert(v).index for e in v.link_edges
                          if any(f.material_index != wall for f in e.link_faces)]
        bm.free()
        for _ in range(12):
            todo = [i for i in nb if not valid[i]]
            if not todo:
                break
            done = []
            for i in todo:
                good = [j for j in nb[i] if valid[j]]
                if good:
                    for arr in arrs.values():
                        arr[i] = arr[good].mean(0)
                    done.append(i)
            for i in done:
                valid[i] = True
        for nm, arr in arrs.items():
            arr[:, 3] = 1.0
            me.color_attributes[nm].data.foreach_set("color", arr.ravel())
    return nbad, int((~valid).sum())


def carve2(ob, cut):
    """(copied from eggs.py)"""
    b = ob.modifiers.new("Carve", "BOOLEAN")
    b.operation = "DIFFERENCE"
    b.solver = "EXACT"
    b.object = cut
    b.material_mode = "TRANSFER"
    apply_mods(ob)
    knife(ob)
    return ob


def euler_holes(ob, shells=2):
    me = ob.data
    chi = len(me.vertices) - len(me.edges) + len(me.polygons)
    return (2 * shells - chi) / 2.0


def triangulate(ob):
    t = ob.modifiers.new("Tri", "TRIANGULATE")
    t.quad_method = "BEAUTY"
    t.ngon_method = "BEAUTY"
    apply_mods(ob)


def join(objs, name):
    for o in bpy.context.scene.objects:
        o.select_set(False)
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.join()
    ob = objs[0]
    ob.name = name
    ob.data.name = name
    return ob


def split_copy(ob, name, keep):
    """(copied from eggs.py)"""
    names = [m.name if m else "" for m in ob.data.materials]
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    dead = [f for f in bm.faces if not keep(f, names)]
    bmesh.ops.delete(bm, geom=dead, context="FACES")
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    for m in ob.data.materials:
        me.materials.append(m)
    o = link(bpy.data.objects.new(name, me))
    o.matrix_world = ob.matrix_world.copy()
    return o


def strip_colors(ob):
    for a in list(ob.data.color_attributes):
        ob.data.color_attributes.remove(a)


def tube(pts, radii, nside, cols, rough):
    """(copied from eggs.py) closed tube along a polyline."""
    n = len(pts)
    T = [(pts[min(n - 1, i + 1)] - pts[max(0, i - 1)]).normalized() for i in range(n)]
    ref = Vector((0, 0, 1)) if abs(T[0].z) < 0.9 else Vector((1, 0, 0))
    Nn = T[0].cross(ref).normalized()
    V, F, C, Rr, rings = [], [], [], [], []
    for i in range(n):
        Nn = (Nn - T[i] * Nn.dot(T[i])).normalized()
        B = T[i].cross(Nn)
        ring = []
        for j in range(nside):
            a = 2 * math.pi * j / nside
            V.append(pts[i] + (Nn * math.cos(a) + B * math.sin(a)) * radii[i])
            C.append(cols[i])
            Rr.append((rough, rough, rough))
            ring.append(len(V) - 1)
        rings.append(ring)
    for i in range(n - 1):
        for j in range(nside):
            jn = (j + 1) % nside
            F.append((rings[i][j], rings[i][jn], rings[i + 1][jn], rings[i + 1][j]))
    V.append(pts[0] - T[0] * radii[0] * 0.5)
    C.append(cols[0])
    Rr.append((rough,) * 3)
    s0 = len(V) - 1
    V.append(pts[-1] + T[-1] * radii[-1] * 0.8)
    C.append(cols[-1])
    Rr.append((rough,) * 3)
    s1 = len(V) - 1
    for j in range(nside):
        jn = (j + 1) % nside
        F.append((rings[0][jn], rings[0][j], s0))
        F.append((rings[-1][j], rings[-1][jn], s1))
    return V, F, C, Rr


def gnarly_stem(L, r0, seed, base, sp, detail, lean_scale=1.0):
    """(copied from eggs.py; + lean_scale so the stem tip stays inside the cage-cap clearance at every 90-degree
    turn of the pumpkin)"""
    sp = {k: lin(v) for k, v in sp.items()}
    rng = random.Random(seed)
    off = Vector((rng.uniform(-40, 40), rng.uniform(-40, 40), rng.uniform(-40, 40)))
    az = rng.uniform(0, 2 * math.pi)
    lean = rng.uniform(0.30, 0.45) * lean_scale
    wob = rng.uniform(0.05, 0.09) * lean_scale
    tw = rng.uniform(0.8, 1.6)
    knots = [(rng.uniform(0.3, 0.72), rng.uniform(0.08, 0.14), rng.uniform(0, 6.283)) for _ in range(2)]
    ld = Vector((math.cos(az), math.sin(az), 0.0))
    sd = Vector((-math.sin(az), math.cos(az), 0.0))
    base = Vector(base)

    def path(t):
        return (base + ld * (lean * L * t * t) + sd * (wob * L * math.sin(2.4 * math.pi * t))
                + Vector((0.0, 0.0, L * t * (1 - 0.12 * t))))

    if detail:
        ts, m = [i / 110 for i in range(111)], 56
    else:
        ts, m = [0.0, 0.05, 0.11, 0.19, 0.3, 0.42, 0.55, 0.68, 0.8, 0.9, 0.97, 1.0], 10
    V, C, Rr, F, rings = [], [], [], [], []
    for t in ts:
        c = path(t)
        T = (path(min(1.0, t + 0.01)) - path(max(0.0, t - 0.01))).normalized()
        Nn = Vector((0, 1, 0)).cross(T).normalized()
        B = T.cross(Nn)
        r = (r0 * (1 + 0.95 * math.exp(-(t / 0.11) ** 2)) * (1 - 0.25 * t)
             * (1 + 0.1 * math.exp(-((t - 0.97) / 0.04) ** 2)))
        amp = 0.2 + 0.2 * math.exp(-(t / 0.12) ** 2)
        bc = mix(sp["base"], sp["mid"], smoothstep(0.05, 0.6, t))
        bc = mix(bc, sp["top"], smoothstep(0.55, 1.0, t))
        ring = []
        for j in range(m):
            a = 2 * math.pi * j / m
            kn = 1.0 + sum(ka * math.exp(-((t - tk) / 0.05) ** 2) * (0.55 + 0.45 * math.cos(a - pa))
                           for tk, ka, pa in knots)
            ridge = (0.5 + 0.5 * math.cos(5 * a + tw * t * 2.2 + 0.4 * math.sin(8 * t))) ** 0.6
            grain = noise.noise(Vector((math.cos(a) * 3, math.sin(a) * 3, t * 30)) + off) if detail else 0.0
            rr = r * kn * (1 - amp + amp * ridge) * (1 + 0.035 * grain)
            V.append(c + (Nn * math.cos(a) + B * math.sin(a)) * rr)
            col = mix(bc, mix(bc, sp["hi"], 0.5), 0.45 * ridge)
            col = mix(col, sp["lo"], 0.35 * (1 - ridge) + 0.2 * max(0.0, grain))
            if detail:
                spk = smoothstep(0.3, 0.6, noise.noise(Vector((math.cos(a) * 6, math.sin(a) * 6, t * 40)) + off * 1.3))
                col = mix(col, sp["lo"], 0.5 * spk)
            C.append(col)
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
    return V, F, C, Rr, path(1.0)


def chain(*segs):
    out = []
    for s in segs:
        out += s[:-1]
    return out


def mirror(pts):
    return [(-x, z) for x, z in reversed(pts)]


def clean(pts, eps=2e-3):
    out = []
    for p in pts:
        if not out or abs(p[0] - out[-1][0]) + abs(p[1] - out[-1][1]) > eps:
            out.append(p)
    while len(out) > 3 and abs(out[0][0] - out[-1][0]) + abs(out[0][1] - out[-1][1]) <= eps:
        out.pop()
    return out


def cutter_planar(name, outlines, R, Rz, flesh, egg=0.0):
    """(copied from eggs.py) radial knife walls with PLANAR caps."""
    bm = bmesh.new()
    for pts in outlines.values():
        P = []
        for vx, vz in pts:
            x, z = -vx, vz
            w = 1 - egg * max(-1.0, min(1.0, z / Rz))
            q = 1 - (x / (R * w)) ** 2 - (z / Rz) ** 2
            P.append(Vector((x, R * w * math.sqrt(max(0.02, q)), z)))
        yi, yo = 0.5 * min(p.y for p in P), 1.35 * max(p.y for p in P)
        b = bmesh.new()
        inner = [b.verts.new(p * (yi / p.y)) for p in P]
        outer = [b.verts.new(p * (yo / p.y)) for p in P]
        n = len(P)
        b.faces.new(inner)
        b.faces.new(list(reversed(outer)))
        for i in range(n):
            j = (i + 1) % n
            b.faces.new((inner[i], outer[i], outer[j], inner[j]))
        bmesh.ops.triangulate(b, faces=b.faces, quad_method="BEAUTY", ngon_method="EAR_CLIP")
        bmesh.ops.recalc_face_normals(b, faces=b.faces)
        if b.calc_volume(signed=True) < 0:
            bmesh.ops.reverse_faces(b, faces=b.faces)
        tmp = bpy.data.meshes.new("_island")
        b.to_mesh(tmp)
        b.free()
        bm.from_mesh(tmp)
        bpy.data.meshes.remove(tmp)
    ob = obj_from_bm(bm, name, smooth=False)
    ob.data.materials.append(flesh)
    return ob


def mat_inner():
    """Round 2: the cavity (inner wall + ceiling) is a pale warm yellow, about sRGB (250, 215, 140) on average, so the
    holes read as lit openings in daylight, not as more orange skin."""
    return mat_noise("Inner", lin((255, 232, 166)), lin((246, 212, 136)), scale=(9.0, 9.0, 1.4), nscale=1.0,
                     detail=6, rough=0.72, lo=0.3, hi=0.72, bump=0.35)


def mat_flesh():
    """(copied from eggs.py) cut walls: pale fibrous flesh + rind line from 'Depth'."""
    # round 2: the knife walls are a deeper warm flesh, never brighter than the cavity fill
    m = mat_noise("Flesh", lin((232, 178, 98)), lin((214, 150, 66)), scale=(14.0, 14.0, 14.0), nscale=1.0,
                  detail=5, rough=0.55, lo=0.32, hi=0.7, bump=0.15)
    nt = m.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    base = bsdf.inputs["Base Color"].links[0].from_socket
    at = nt.nodes.new("ShaderNodeVertexColor")
    at.layer_name = "Depth"
    sep = nt.nodes.new("ShaderNodeSeparateColor")
    nt.links.new(at.outputs["Color"], sep.inputs["Color"])
    rind = nt.nodes.new("ShaderNodeMapRange")
    rind.inputs["From Min"].default_value = 0.80
    rind.inputs["From Max"].default_value = 0.93
    rind.interpolation_type = "SMOOTHSTEP"
    nt.links.new(sep.outputs["Red"], rind.inputs["Value"])
    deep = nt.nodes.new("ShaderNodeMapRange")
    deep.inputs["From Min"].default_value = 0.25
    deep.inputs["From Max"].default_value = 0.0
    nt.links.new(sep.outputs["Red"], deep.inputs["Value"])

    def sk(socks, ident):
        return [s for s in socks if s.identifier == ident][0]
    m1 = nt.nodes.new("ShaderNodeMix")
    m1.data_type = "RGBA"
    nt.links.new(deep.outputs["Result"], sk(m1.inputs, "Factor_Float"))
    nt.links.new(base, sk(m1.inputs, "A_Color"))
    sk(m1.inputs, "B_Color").default_value = (*lin((222, 140, 50)), 1)
    m2 = nt.nodes.new("ShaderNodeMix")
    m2.data_type = "RGBA"
    nt.links.new(rind.outputs["Result"], sk(m2.inputs, "Factor_Float"))
    nt.links.new(sk(m1.outputs, "Result_Color"), sk(m2.inputs, "A_Color"))
    sk(m2.inputs, "B_Color").default_value = (*lin((214, 104, 22)), 1)
    nt.links.new(sk(m2.outputs, "Result_Color"), bsdf.inputs["Base Color"])
    return m


def uv_layout(ob, seam_az, abf_mats, shrink, angle=55, centre_xy=(0.0, 0.0)):
    """(copied from eggs.py; + centre_xy: the pumpkin's own axis, it no longer sits at the origin)"""
    me = ob.data
    names = [m.name for m in me.materials]
    abf_idx = {i for i, n in enumerate(names) if n in abf_mats}
    bm = bmesh.new()
    bm.from_mesh(me)
    cx, cy = centre_xy

    def on(v, s):
        x, y = v.co.x - cx, v.co.y - cy
        if x * x + y * y < 1e-10:
            return True
        a = math.degrees(math.atan2(y, x))
        return abs((a - s + 180) % 360 - 180) < 0.05

    nseam = 0
    for e in bm.edges:
        mats = {f.material_index for f in e.link_faces}
        e.seam = False
        if len(mats) > 1:
            e.seam = True
        elif mats and mats <= abf_idx:
            for s in seam_az:
                if on(e.verts[0], s) and on(e.verts[1], s):
                    e.seam = True
                    nseam += 1
                    break
    bm.to_mesh(me)
    bm.free()
    sc = bpy.context.scene
    sc.tool_settings.use_uv_select_sync = True
    only(ob)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.smart_project(angle_limit=math.radians(angle), island_margin=0.004)
    bpy.ops.object.mode_set(mode="OBJECT")
    if abf_idx:
        for p in me.polygons:
            p.select = p.material_index in abf_idx
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.uv.unwrap(method="ANGLE_BASED", margin=0.004)
        bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.average_islands_scale()
    bpy.ops.object.mode_set(mode="OBJECT")
    if shrink:
        uv = me.uv_layers.active.data
        for p in me.polygons:
            k = shrink.get(names[p.material_index])
            if k:
                for li in p.loop_indices:
                    uv[li].uv = uv[li].uv * k
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.pack_islands(rotate=True, rotate_method="CARDINAL", margin_method="FRACTION", margin=0.006,
                            shape_method="CONVEX")
    bpy.ops.object.mode_set(mode="OBJECT")
    return nseam


def pack_uv(ob, margin=0.005):
    """Pack the (pre-scaled, explicit) UV islands of ob into 0-1, keeping relative island scale."""
    only(ob)
    bpy.context.scene.tool_settings.use_uv_select_sync = True
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.pack_islands(rotate=True, rotate_method="ANY", scale=True, margin_method="FRACTION", margin=margin,
                            shape_method="CONVEX")
    bpy.ops.object.mode_set(mode="OBJECT")


def uv_usage(ob, size=256):
    """Fraction of the 0-1 square covered by UV triangles (rasterised coarsely)."""
    me = ob.data
    uv = np.empty(len(me.loops) * 2, np.float32)
    me.uv_layers.active.data.foreach_get("uv", uv)
    uv = uv.reshape(-1, 2)
    img = np.zeros((size, size), bool)
    for p in me.polygons:
        li = list(p.loop_indices)
        pts = uv[li] * size
        mn = np.floor(pts.min(0)).astype(int).clip(0, size - 1)
        mx = np.ceil(pts.max(0)).astype(int).clip(0, size - 1)
        img[mn[1]:mx[1] + 1, mn[0]:mx[0] + 1] = True
    return float(img.mean())


def texel_density(ob, size):
    """Mean px per stud: sqrt(UV area * size^2 / world area)."""
    me = ob.data
    uv = np.empty(len(me.loops) * 2, np.float32)
    me.uv_layers.active.data.foreach_get("uv", uv)
    uv = uv.reshape(-1, 2)
    co = np.empty(len(me.vertices) * 3, np.float32)
    me.vertices.foreach_get("co", co)
    co = co.reshape(-1, 3)
    lv = np.empty(len(me.loops), np.int32)
    me.loops.foreach_get("vertex_index", lv)
    ua, wa = 0.0, 0.0
    for p in me.polygons:
        li = list(p.loop_indices)
        for k in range(1, len(li) - 1):
            a, b, c = li[0], li[k], li[k + 1]
            ua += 0.5 * abs((uv[b, 0] - uv[a, 0]) * (uv[c, 1] - uv[a, 1]) - (uv[b, 1] - uv[a, 1]) * (uv[c, 0] - uv[a, 0]))
            wa += 0.5 * np.linalg.norm(np.cross(co[lv[b]] - co[lv[a]], co[lv[c]] - co[lv[a]]))
    return math.sqrt(ua * size * size / max(wa, 1e-9)), ua


# ------------------------------------------------------------------ bakes (copied from eggs.py bake_groups; maps dir
# is StreetLamps\maps; + an optional METAL pass = the hi 'Wear' attribute baked as emission)
def bake_groups(groups, size, prefix, ao_strength, ao_dist, metal=False, ss=1, ids_path=None):
    """groups: (lo, his, cage, maxray[, ao_strength of this group]). ss: bake at size*ss and box-filter down
    (round 2: crisper small relief). ids_path: also save a group-id map (R = (index + 1) / 16)."""
    out_size = size
    size = size * ss
    sc = bpy.context.scene
    sc.world.light_settings.distance = ao_dist
    shp = (size, size, 4)
    keys = ["albedo", "normal", "rough", "ao"] + (["metal"] if metal else [])
    acc = {k: np.zeros(shp, np.float32) for k in keys}
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

    def bake(node, img, kind, s2a, cage=0.0, maxray=0.0, **kw):
        node.image = img
        img.pixels.foreach_set(zero)
        bpy.ops.object.bake(type=kind, use_selected_to_active=s2a, cage_extrusion=cage, max_ray_distance=maxray,
                            margin=0, use_clear=False, **kw)
        a = np.empty(size * size * 4, np.float32)
        img.pixels.foreach_get(a)
        return a.reshape(shp)

    def emit_set(his, on, saved, attr=None):
        if on:
            for h in his:
                for m in h.data.materials:
                    if m and m.use_nodes:
                        for n in m.node_tree.nodes:
                            if n.type == "BSDF_PRINCIPLED":
                                ls = [l for l in m.node_tree.links if l.to_socket == n.inputs["Emission Color"]]
                                saved.append((m, n, tuple(n.inputs["Emission Color"].default_value),
                                              n.inputs["Emission Strength"].default_value,
                                              [(l.from_socket, l.to_socket) for l in ls], []))
                                for l in ls:
                                    m.node_tree.links.remove(l)
                                if attr:
                                    vc = m.node_tree.nodes.new("ShaderNodeVertexColor")
                                    vc.layer_name = attr
                                    m.node_tree.links.new(vc.outputs["Color"], n.inputs["Emission Color"])
                                    saved[-1][5].append(vc)
                                else:
                                    n.inputs["Emission Color"].default_value = (1, 1, 1, 1)
                                n.inputs["Emission Strength"].default_value = 1.0
        else:
            for m, n, col, st, ls, extra in saved:
                for x in extra:
                    m.node_tree.nodes.remove(x)
                n.inputs["Emission Color"].default_value = col
                n.inputs["Emission Strength"].default_value = st
                for a, b in ls:
                    m.node_tree.links.new(a, b)
            saved.clear()

    stats = {}
    aostr = np.full(shp, ao_strength, np.float32)
    ids = np.zeros(shp, np.float32)
    groups = [tuple(g) + ((ao_strength,) if len(g) == 4 else ()) for g in groups]
    for lo, his, cage, maxray, ao_g in groups:
        for attr in ("visible_shadow", "visible_diffuse", "visible_glossy", "visible_transmission"):
            setattr(lo, attr, False)
    for gi_, (lo, his, cage, maxray, ao_g) in enumerate(groups):
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
        if metal:
            emit_set(his, True, saved, attr="Wear")
            out["metal"] = bake(tex, t_lin, "EMIT", True, cage, maxray)
            emit_set(his, False, saved)
        emit_set(his, True, saved)
        hit = bake(tex, t_lin, "EMIT", True, cage, maxray)[..., 0] > 0.5
        emit_set(his, False, saved)
        hit &= cov
        for k, arr in out.items():
            filled = fill_misses(arr, hit, iters=6)
            acc[k][cov] = filled[cov]
        owned |= cov
        aostr[cov] = ao_g
        ids[cov] = (gi_ + 1) / 16.0
        stats[lo.name] = {"texels": int(cov.sum()) // (ss * ss),
                          "miss": round(float(1 - hit.sum() / max(1, cov.sum())), 4), "ao": ao_g}
        log("  baked", lo.name, stats[lo.name])
    for k in acc:
        acc[k] = fill_misses(acc[k], owned, iters=10 * ss)
    aostr = fill_misses(aostr, owned, iters=10 * ss)
    acc["albedo"][..., :3] *= (1 - aostr[..., :1]) + aostr[..., :1] * acc["ao"][..., :1]
    if ss > 1:
        def down(a):
            return a.reshape(out_size, ss, out_size, ss, a.shape[-1]).mean(axis=(1, 3))
        for k in keys:
            if k == "normal":
                n = acc[k][..., :3] * 2 - 1
                n = down(np.concatenate([n, acc[k][..., 3:]], -1))[..., :3]
                n /= np.maximum(np.linalg.norm(n, axis=-1, keepdims=True), 1e-6)
                acc[k] = np.concatenate([n * 0.5 + 0.5, np.ones((out_size, out_size, 1), np.float32)], -1)
            else:
                acc[k] = down(acc[k])
        ids = ids[::ss, ::ss]
        size = out_size
    if ids_path:
        ids[..., 3] = 1.0
        im = bpy.data.images.new(prefix + "_ids", size, size, alpha=False)
        im.colorspace_settings.name = "Non-Color"
        im.pixels.foreach_set(ids.ravel())
        save_png(im, ids_path)
        bpy.data.images.remove(im)
    imgs = {}
    for k in keys:
        cs = "sRGB" if k == "albedo" else "Non-Color"
        acc[k][..., 3] = 1.0
        img = bpy.data.images.new(prefix + "_" + k, size, size, alpha=False)
        img.colorspace_settings.name = cs
        img.pixels.foreach_set(acc[k].ravel())
        save_png(img, os.path.join(MAPS, f"{prefix}_{k}.png"))
        imgs[k] = img
    for i in (t_lin, t_rgb):
        bpy.data.images.remove(i)
    imgs["stats"] = stats
    return imgs


def mat_iron_hi(name="IronHi"):
    """Principled from the per-vertex Col / Rough attributes (hkit.mat_vc)."""
    return mat_vc(name)


# ------------------------------------------------------------------ candles (copied from eggs.py)
CANDLE_S1, CANDLE_S2, CANDLE_S3, CANDLE_S4 = 0.60, 0.78, 0.86, 0.90
CANDLE_LIP = 0.045


def candle_field(K):
    """(copied from eggs.py) a melted pillar candle as f(theta, s)."""
    S1, S2, S3, S4, LIP = CANDLE_S1, CANDLE_S2, CANDLE_S3, CANDLE_S4, CANDLE_LIP
    rng = random.Random(K["seed"])
    H, R = K["H"], K["R"]
    cx, cy = K["pos"]
    off = Vector((rng.uniform(-30, 30), rng.uniform(-30, 30), rng.uniform(-30, 30)))
    lr = LIP
    slant, ths = rng.uniform(0.015, 0.04), rng.uniform(0, 2 * math.pi)
    notches = K["notches"]

    def rim(th):
        v = H - slant + slant * math.cos(th - ths)
        v += 0.03 * noise.noise(Vector((math.cos(th) * 1.8, math.sin(th) * 1.8, 0.5)) + off)
        v += 0.012 * noise.noise(Vector((math.cos(th) * 7, math.sin(th) * 7, 2.5)) + off)
        for tn, dn, wn in notches:
            v -= dn * math.exp(-(wrap(th - tn) / wn) ** 2)
        return v

    zf = min(rim(2 * math.pi * i / 720) for i in range(720)) - lr - 0.012
    drips = []
    for tn, dn, wn in notches:
        zs = rim(tn) - lr
        drips.append((tn + rng.uniform(-0.04, 0.04), zs, zs - rng.uniform(0.0, 0.06), rng.uniform(0.10, 0.13),
                      rng.uniform(0.05, 0.065)))
        t2 = tn + rng.choice((-1, 1)) * rng.uniform(0.2, 0.32)
        zs2 = rim(t2) - lr
        drips.append((t2, zs2, rng.uniform(0.25, 0.6) * zs2, rng.uniform(0.06, 0.08), rng.uniform(0.03, 0.04)))
    for _ in range(K["extra"]):
        t2 = rng.uniform(0, 2 * math.pi)
        zs2 = rim(t2) - lr
        drips.append((t2, zs2, rng.uniform(0.12, 0.5) * zs2, rng.uniform(0.05, 0.08), rng.uniform(0.028, 0.04)))

    def drip(th, z):
        best, tint = 0.0, 0.0
        for t0, zs, L, w0, k0 in drips:
            x = wrap(th - t0) * R
            if abs(x) > 2.0 * w0 or z > zs + 0.03:
                continue
            ze = zs - L
            if z >= ze:
                u = (zs - z) / max(L, 1e-3)
                bul = math.exp(-((z - ze) / (w0 * 0.9)) ** 2)
                w = w0 * (1 - 0.35 * u) * (1 + 0.35 * bul)
                k = k0 * (0.6 + 0.4 * u) * (1 + 0.4 * bul) * smoothstep(zs + 0.03, zs - 0.02, z)
                q = 1 - (x / w) ** 2
            else:
                w = w0 * 0.65 * 1.35
                k = k0 * 1.4
                q = 1 - (math.sqrt(x * x + 1.3 * (ze - z) ** 2) / w) ** 2
            if q > 0:
                v = k * q ** 0.55
                best = max(best, v)
                tint = max(tint, min(1.0, v / (k0 * 0.5)))
        return best, tint

    def side_r(th, z, h):
        r = R * (1 + 0.010 * noise.noise(Vector((math.cos(th) * 2.0, math.sin(th) * 2.0, z * 1.6)) + off))
        r += 0.028 * math.exp(-max(z, 0.0) / 0.09)
        r += 0.010 * math.exp(-max(0.0, h - z) / 0.07)
        dv, tint = drip(th, z)
        return r + dv, tint

    wax = lin(K["wax"])
    # round 2: amber wax + a soot ring round the wick (no white chip in the mouth in daylight)
    amber, dust = lin((190, 120, 46)), lin((150, 120, 84))
    drip_c, soot = lin((222, 164, 86)), lin((34, 28, 24))

    def f(th, s):
        h = rim(th)
        ct, st = math.cos(th), math.sin(th)
        rt, _ = side_r(th, h - lr, h)
        rc = rt - lr
        tint, zone = 0.0, 0
        if s <= S1:
            z = (h - lr) * s / S1
            r, tint = side_r(th, z, h)
        elif s <= S2:
            a = math.pi * (s - S1) / (S2 - S1)
            r, z, zone = rc + lr * math.cos(a), h - lr + lr * math.sin(a), 1
        elif s <= S3:
            q = (s - S2) / (S3 - S2)
            r, z, zone = rc - lr - 0.03 * q, (h - lr) + (zf + 0.022 - (h - lr)) * q, 2
        elif s <= S4:
            q = (s - S3) / (S4 - S3)
            r, z, zone = rc - lr - 0.03 - 0.055 * q, zf + 0.022 * (1 - q) ** 2, 3
        else:
            q = (s - S4) / (1 - S4)
            r, z, zone = (rc - lr - 0.085) * (1 - q), zf - 0.006 * q * q, 3
        p = Vector((cx + r * ct, cy + r * st, z))
        n1 = noise.noise(Vector((ct * 3, st * 3, z * 4)) + off)
        n2 = noise.noise(Vector((ct * 9, st * 9, z * 14)) + off * 0.7)
        col = mix(wax, dust, 0.35 * math.exp(-max(z, 0.0) / 0.22))
        col = tuple(cc * (0.965 + 0.035 * n1 + 0.02 * n2) for cc in col)
        rough = 0.46
        if zone == 0:
            col = mix(col, mix(wax, drip_c, 0.5), 0.3 * smoothstep(h - 0.3, h - lr, z))
            col = mix(col, drip_c, 0.75 * tint)
            rough = 0.46 - 0.2 * tint
        elif zone == 1:
            col, rough = mix(col, drip_c, 0.3), 0.36
        elif zone == 2:
            col, rough = mix(wax, amber, 0.3), 0.32
        else:
            col, rough = mix(wax, amber, 0.62 + 0.08 * n1), 0.15
            col = mix(col, soot, 0.85 * math.exp(-(r / 0.12) ** 2))
        return p, col, (rough, rough, rough)

    return f, zf


def grid_surface(field, thetas, ss, pole_s=None):
    """(copied from eggs.py)"""
    V, C, Rr, F, rows = [], [], [], [], []
    m = len(thetas)
    for s in ss:
        row = []
        for th in thetas:
            p, c, r = field(th, s)
            V.append(p)
            C.append(c)
            Rr.append(r)
            row.append(len(V) - 1)
        rows.append(row)
    for a, b in zip(rows[:-1], rows[1:]):
        for j in range(m):
            jn = (j + 1) % m
            F.append((a[j], a[jn], b[jn], b[j]))
    if pole_s is not None:
        p, c, r = field(0.0, pole_s)
        V.append(p)
        C.append(c)
        Rr.append(r)
        pv = len(V) - 1
        for j in range(m):
            F.append((rows[-1][j], rows[-1][(j + 1) % m], pv))
    return V, F, C, Rr


def wick_pts(K, zf, n):
    """(copied from eggs.py)"""
    rng = random.Random(K["seed"] + 7)
    cx, cy = K["pos"]
    phi = rng.uniform(0, 2 * math.pi)
    P0 = Vector((cx, cy, zf - 0.03))
    P1 = Vector((cx, cy, zf + 0.25))
    P2 = Vector((cx + 0.10 * math.cos(phi), cy + 0.10 * math.sin(phi), zf + 0.18))
    return [P0 * (1 - t) ** 2 + P1 * 2 * (1 - t) * t + P2 * t * t for t in (i / (n - 1) for i in range(n))]


def wick_mesh(pts, nside, rscale=1.0):
    """(copied from eggs.py; + rscale)"""
    n = len(pts)
    radii, cols = [], []
    for i in range(n):
        t = i / (n - 1)
        radii.append(rscale * (0.04 - 0.008 * t) * (1 + 0.35 * math.exp(-((1 - t) / 0.08) ** 2)))
        c = mix(lin((214, 204, 182)), lin((26, 23, 21)), smoothstep(0.1, 0.2, t))
        cols.append(mix(c, lin((86, 78, 70)), smoothstep(0.82, 1.0, t)))
    return tube(pts, radii, nside, cols, 0.85)


def flame(name, loc, w, h, strength=30.0):
    """(copied from eggs.py) review-only stand-in for the Studio flame particles (NOT exported)."""
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=16, v_segments=12, radius=1.0)
    for v in bm.verts:
        x, y, z = v.co
        k = 1 - 0.55 * max(0.0, z)
        v.co = Vector((x * w * k, y * w * k, (z + 0.35 * (1 - z * z)) * h))
    ob = obj_from_bm(bm, name)
    ob.location = loc
    em = bpy.data.materials.new(name + "_m")
    em.use_nodes = True
    nt = em.node_tree
    nt.nodes.remove(nt.nodes["Principled BSDF"])
    e = nt.nodes.new("ShaderNodeEmission")
    e.inputs["Color"].default_value = (1.0, 0.62, 0.22, 1)
    e.inputs["Strength"].default_value = strength
    nt.links.new(e.outputs["Emission"], nt.nodes["Material Output"].inputs["Surface"])
    ob.data.materials.append(em)
    ob.visible_shadow = False
    return ob


def point(name, loc, energy, col=(1.0, 0.55, 0.2), radius=0.12, shadow=True):
    ld = bpy.data.lights.new(name, "POINT")
    ld.energy, ld.color, ld.shadow_soft_size = energy, col, radius
    ld.use_shadow = shadow
    ob = link(bpy.data.objects.new(name, ld))
    ob.location = loc
    return ob


def spot(name, loc, energy, angle_deg, col, blend=0.6, shadow=False, radius=0.1):
    ld = bpy.data.lights.new(name, "SPOT")
    ld.energy, ld.color, ld.spot_size, ld.spot_blend = energy, col, math.radians(angle_deg), blend
    ld.use_shadow = shadow
    ld.shadow_soft_size = radius
    ob = link(bpy.data.objects.new(name, ld))
    ob.location = loc
    ob.rotation_euler = (0, 0, 0)          # a spot points along its local -Z = straight down
    return ob


# ===================================================================== copied from WebsSpiders\webs_spiders.py
def srgb(c):
    return tuple(v / 255.0 for v in c)


def mnoise(n, scale, seed, octaves=3, aspect=(1.0, 1.0)):
    out = np.empty((n, n), np.float32)
    off = Vector((seed * 13.17, seed * 7.31, seed * 3.77))
    sx, sy = scale * aspect[0] / n, scale * aspect[1] / n
    for j in range(n):
        for i in range(n):
            out[j, i] = fbm(Vector((i * sx, j * sy, 0.0)) + off, octaves)
    lo, hi = np.percentile(out, 1), np.percentile(out, 99)
    return np.clip((out - lo) / max(1e-6, hi - lo), 0, 1)


def make_image(name, arr, colorspace, path, alpha=True):
    h, w = arr.shape[:2]
    img = bpy.data.images.new(name, w, h, alpha=alpha)
    img.colorspace_settings.name = colorspace
    img.pixels.foreach_set(np.ascontiguousarray(arr, dtype=np.float32).ravel())
    img.filepath_raw = path
    img.file_format = "PNG"
    img.save()
    img.alpha_mode = "STRAIGHT"
    return img


def mat_tex(name, col_img, rough_img=None, alpha=False, rough=0.6):
    """(copied from webs_spiders.py; the roughness map is linked STRAIGHT into Roughness so the FBX embeds it)"""
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
    if rough_img:
        tr = nt.nodes.new("ShaderNodeTexImage")
        tr.image = rough_img
        nt.links.new(tr.outputs["Color"], b.inputs["Roughness"])
    b.inputs["Metallic"].default_value = 0.0
    return m


def shoot_fov(path, loc, target, vfov=70.0, lens=None, res=None, ortho=None):
    sc = bpy.context.scene
    if res:
        sc.render.resolution_x, sc.render.resolution_y = res
    cd = bpy.data.cameras.new("Cam")
    cam = link(bpy.data.objects.new("Cam", cd))
    cam.location = Vector(loc)
    cam.rotation_euler = (Vector(target) - cam.location).to_track_quat("-Z", "Y").to_euler()
    if ortho:
        cd.type = "ORTHO"
        cd.ortho_scale = ortho
    elif lens:
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


def sag2(a, b, n, sv, k=2.4):
    c0 = math.cosh(k / 2)
    out = []
    for i in range(n + 1):
        t = i / n
        s = (math.cosh(k * (t - 0.5)) - c0) / (1 - c0)
        out.append((a[0] + (b[0] - a[0]) * t + sv[0] * s, a[1] + (b[1] - a[1]) * t + sv[1] * s))
    return out


def hanging(p0, d0, length, n, rng, drift=0.04):
    pts = [p0.copy()]
    d = Vector(d0).normalized()
    d.z = min(d.z, -0.25)
    d.normalize()
    seg = length / n
    down = Vector((0, 0, -1))
    for _ in range(n):
        d = (d.lerp(down, 0.42) + Vector((rng.uniform(-0.02, drift), rng.uniform(-0.1, 0.1), 0))).normalized()
        pts.append(pts[-1] + d * seg)
    return pts


def poly_hit(o, d, poly):
    """(copied from treekit.py) ray (2D) vs closed polyline -> (t, segment index, u)."""
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


# ===================================================================== checks
def bvh_of(objs):
    """World-space BVH of several mesh objects (evaluated)."""
    dg = bpy.context.evaluated_depsgraph_get()
    V, F = [], []
    for ob in objs:
        me = ob.evaluated_get(dg).to_mesh()
        mw = ob.matrix_world
        o = len(V)
        V += [mw @ v.co for v in me.vertices]
        F += [tuple(o + i for i in p.vertices) for p in me.polygons]
        ob.evaluated_get(dg).to_mesh_clear()
    return BVHTree.FromPolygons(V, F, all_triangles=False), V


def min_dist(objs_a, objs_b, sample=4):
    """Min distance from vertices of A (every `sample`-th) to the surface of B."""
    bvh, _ = bvh_of(objs_b)
    best, where = 1e9, None
    for ob in objs_a:
        mw = ob.matrix_world
        vs = ob.data.vertices
        for i in range(0, len(vs), sample):
            p = mw @ vs[i].co
            hit = bvh.find_nearest(p)
            if hit[0] is not None and hit[3] < best:
                best, where = hit[3], tuple(round(x, 3) for x in p)
    return best, where


def components(ob):
    """Connected components (vertex labels) of a mesh via union-find on edges."""
    me = ob.data
    ev = np.empty(len(me.edges) * 2, np.int64)
    me.edges.foreach_get("vertices", ev)
    ev = ev.reshape(-1, 2)
    parent = np.arange(len(me.vertices))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for a, b in ev:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
    return np.array([find(i) for i in range(len(parent))])
