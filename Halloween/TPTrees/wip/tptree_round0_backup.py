# SLINGSHOT Halloween garden - TOILET-PAPER-PRANKED autumn TREE + TP BUSH (2026-10-12, TPTrees builder).
# Headless (one step per run, each opens/saves its own .blend):
#   blender.exe -b --factory-startup --python tptree.py -- build tree | bake tree | render tree | export tree
#   (same with "bush"); "quick" before the step = fewer leaves for a fast shape test; "preview tree" renders the hi.
#
# Pipeline (hkit): dense procedural sculpts with per-vertex colour "Col" + roughness "Rough" -> game meshes -> Cycles
# bakes (tangent normal, colour x AO, roughness) -> FBX with embedded textures.
#   Canopy : clumps of spheres + sub-blobs -> voxel union -> smoothed -> noise. HI = that base (dark gap colour) plus
#            ~13k sculpted leaves (pointed, mid-rib fold, tilted like shingles, autumn colour per clump/leaf).
#            LO = the base pushed out to the mean leaf height, decimated. Leaf shapes live in the normal map.
#   Trunk  : skeleton of tapered tubes (trunk, root flare + roots, limbs to the clumps, twigs, stubs) -> voxel union
#            -> smoothed (branch collars). HI = + bark fissures (nearest-skeleton coordinates). LO = decimated, the
#            parts hidden inside the canopy deleted.
#   TP     : every streamer is a rope simulated with Verlet (gravity, length + bending constraints, collisions with
#            the LO canopy / LO trunk / ground / ribbons already placed, friction, pinned snag points), then a ribbon
#            frame (lies flat on the surface it touches, twists when hanging free). LO = 0.45 x 0.06 box section
#            (both faces + edges, adaptive spacing), HI = 9+9 section with cup, wavy edges, crumple folds and
#            perforation creases. Rolls (paper + cardboard core with a real hole) are in the same TP object.
# 1 Blender m = 1 stud, +Z up, Blender +Y = Roblox -Z. FBX origin = trunk base on the ground (z = 0).
import sys, os, json, time, math, random
sys.path.insert(0, r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween")
from hkit import *  # noqa: F401,F403  (read-only kit)
import bpy, bmesh
import numpy as np
from mathutils import Vector, Matrix, noise
from mathutils.bvhtree import BVHTree

OUT = os.path.join(HERE, "TPTrees")
MAPS = os.path.join(OUT, "maps")
WIP = os.path.join(OUT, "wip")
os.makedirs(MAPS, exist_ok=True)
os.makedirs(WIP, exist_ok=True)
T0 = time.time()
CFG = {"quick": False}


def log(*a):
    print("[tp %7.1fs]" % (time.time() - T0), *a, flush=True)


# ================================================================== numpy mesh helpers
def mesh_np(name, V, F, smooth=True):
    V = np.asarray(V, np.float32).reshape(-1, 3)
    F = np.asarray(F, np.int32)
    k = F.shape[1]
    me = bpy.data.meshes.new(name)
    me.vertices.add(len(V))
    me.vertices.foreach_set("co", V.ravel())
    me.loops.add(F.size)
    me.loops.foreach_set("vertex_index", F.ravel())
    me.polygons.add(len(F))
    me.polygons.foreach_set("loop_start", np.arange(0, F.size, k, dtype=np.int32))
    me.update(calc_edges=True)
    if smooth:
        me.shade_smooth()
    return link(bpy.data.objects.new(name, me))


def obj_arrays(ob):
    me = ob.data
    nv = len(me.vertices)
    V = np.empty(nv * 3, np.float32)
    me.vertices.foreach_get("co", V)
    me.calc_loop_triangles()
    T = np.empty(len(me.loop_triangles) * 3, np.int32)
    me.loop_triangles.foreach_get("vertices", T)
    N = np.empty(nv * 3, np.float32)
    me.vertex_normals.foreach_get("vector", N)
    return V.reshape(-1, 3), T.reshape(-1, 3), N.reshape(-1, 3)


def set_co(ob, V):
    ob.data.vertices.foreach_set("co", np.asarray(V, np.float32).ravel())
    ob.data.update()


def bvh_np(V, T):
    return BVHTree.FromPolygons([tuple(map(float, v)) for v in V], [tuple(map(int, t)) for t in T])


def bvh_ob(ob):
    V, T, _ = obj_arrays(ob)
    return bvh_np(V, T)


def nrm(a):
    a = np.asarray(a, np.float64)
    return a / np.maximum(1e-12, np.linalg.norm(a, axis=-1, keepdims=True))


def tri_count(ob):
    ob.data.calc_loop_triangles()
    return len(ob.data.loop_triangles)


def delete_faces(ob, pred_mask):
    """Delete the faces whose mask entry is True (mask over polygons)."""
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    bm.faces.ensure_lookup_table()
    kill = [f for f in bm.faces if pred_mask[f.index]]
    bmesh.ops.delete(bm, geom=kill, context="FACES")
    loose = [v for v in bm.verts if not v.link_faces]
    bmesh.ops.delete(bm, geom=loose, context="VERTS")
    bm.to_mesh(ob.data)
    bm.free()
    ob.data.update()


def face_centers(ob):
    me = ob.data
    C = np.empty(len(me.polygons) * 3, np.float32)
    me.polygons.foreach_get("center", C)
    return C.reshape(-1, 3)


# ================================================================== curves
def cr_dense(P, k=12):
    """Uniform Catmull-Rom through the rows of P (any number of columns), k samples per span."""
    P = np.asarray(P, np.float64)
    if len(P) == 2:
        t = np.linspace(0, 1, k + 1)[:, None]
        return P[0] * (1 - t) + P[1] * t
    Pp = np.vstack([2 * P[0] - P[1], P, 2 * P[-1] - P[-2]])
    out = []
    t = np.linspace(0, 1, k, endpoint=False)[:, None]
    for i in range(1, len(Pp) - 2):
        p0, p1, p2, p3 = Pp[i - 1], Pp[i], Pp[i + 1], Pp[i + 2]
        out.append(0.5 * (2 * p1 + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t ** 2
                          + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    out.append(P[-1:])
    return np.vstack(out)


def arc_param(D):
    seg = np.linalg.norm(np.diff(D[:, :3], axis=0), axis=1)
    return np.concatenate([[0.0], np.cumsum(seg)])


def resample_at(D, s_src, s_new):
    return np.stack([np.interp(s_new, s_src, D[:, c]) for c in range(D.shape[1])], 1)


def arc_resample(D, step):
    s = arc_param(D)
    L = s[-1]
    n = max(2, int(round(L / step)) + 1)
    si = np.linspace(0, L, n)
    return resample_at(D, s, si), si


def transport_frames(P, n0=None):
    P = np.asarray(P, np.float64)
    T = nrm(np.gradient(P, axis=0))
    if n0 is None:
        ref = np.array([0.0, 0.0, 1.0]) if abs(T[0, 2]) < 0.9 else np.array([1.0, 0.0, 0.0])
        n0 = np.cross(T[0], ref)
    N = np.zeros_like(P)
    cur = np.asarray(n0, np.float64)
    for i in range(len(P)):
        cur = cur - T[i] * np.dot(cur, T[i])
        cur = cur / max(1e-12, np.linalg.norm(cur))
        N[i] = cur
    B = np.cross(T, N)
    return T, N, B


def tube_arrays(P, R, nside):
    """Closed tube (tris) along P with radii R. Returns V, F."""
    T, N, B = transport_frames(P)
    n = len(P)
    a = 2 * np.pi * np.arange(nside) / nside
    ring = (N[:, None, :] * np.cos(a)[None, :, None] + B[:, None, :] * np.sin(a)[None, :, None]) * R[:, None, None]
    V = (P[:, None, :] + ring).reshape(-1, 3)
    i = np.arange(n - 1)[:, None]
    j = np.arange(nside)[None, :]
    jn = (j + 1) % nside
    a0 = i * nside + j
    b0 = i * nside + jn
    c0 = (i + 1) * nside + jn
    d0 = (i + 1) * nside + j
    F = np.concatenate([np.stack([a0, b0, c0], -1).reshape(-1, 3), np.stack([a0, c0, d0], -1).reshape(-1, 3)])
    s0 = len(V)
    V = np.vstack([V, P[0] - T[0] * R[0] * 0.3, P[-1] + T[-1] * R[-1] * 0.6])
    jj = np.arange(nside)
    cap0 = np.stack([np.full(nside, s0), (jj + 1) % nside, jj], -1)
    cap1 = np.stack([np.full(nside, s0 + 1), (n - 1) * nside + jj, (n - 1) * nside + (jj + 1) % nside], -1)
    return V, np.vstack([F, cap0, cap1])


def remesh(ob, voxel, smooth_iter=0, smooth_fac=0.6):
    rm = ob.modifiers.new("R", "REMESH")
    rm.mode = "VOXEL"
    rm.voxel_size = voxel
    rm.adaptivity = 0.0
    if smooth_iter:
        sm = ob.modifiers.new("S", "SMOOTH")
        sm.factor = smooth_fac
        sm.iterations = smooth_iter
    apply_mods(ob)
    ob.data.shade_smooth()
    return ob


def noise_field(V, freq, octaves, off, amp=1.0):
    out = np.empty(len(V), np.float64)
    o = Vector(off)
    for i, p in enumerate(V):
        out[i] = fbm(Vector((float(p[0]), float(p[1]), float(p[2]))) * freq + o, octaves)
    return out * amp


def L(c):
    return np.array(lin(c), np.float64)


# ================================================================== canopy (clumps -> voxel union)
def blob_mesh(name, blobs, voxel, smooth_iter, namp, nfreq, seed, zfloor=None):
    bm = bmesh.new()
    for c, r, sqb, sqt in blobs:
        ret = bmesh.ops.create_icosphere(bm, subdivisions=4, radius=1.0)
        for v in ret["verts"]:
            x, y, z = v.co
            z = z * (sqb if z < 0 else sqt)
            v.co = Vector((x * r + c[0], y * r + c[1], z * r + c[2]))
    ob = obj_from_bm(bm, name)
    remesh(ob, voxel, smooth_iter, 0.7)
    V, T, N = obj_arrays(ob)
    rng = random.Random(seed)
    off = (rng.uniform(-60, 60), rng.uniform(-60, 60), rng.uniform(-60, 60))
    d = noise_field(V, nfreq, 3, off, namp)
    V = V + N * d[:, None].astype(np.float32)
    if zfloor is not None:
        V[:, 2] = np.maximum(V[:, 2], zfloor)
    set_co(ob, V)
    return ob


def tree_clumps(seed):
    """(centre, radius, hue) of the big leaf clumps + the sub-blob list for the union."""
    rng = random.Random(seed)
    clumps = [(Vector((0.15, -0.1, 12.45)), 3.0, 0.55)]
    hues = [0.15, 0.7, 0.35, 0.9, 0.5, 0.25, 0.8, 0.05, 0.6, 0.4, 0.75, 0.3]
    for k in range(5):
        a = math.radians(18 + 72 * k + rng.uniform(-11, 11))
        rr = 3.8 + rng.uniform(-0.35, 0.3)
        clumps.append((Vector((rr * math.cos(a), rr * math.sin(a), 10.85 + rng.uniform(-0.5, 0.5))),
                       2.7 + rng.uniform(-0.3, 0.25), hues[k]))
    for k in range(5):
        a = math.radians(54 + 72 * k + rng.uniform(-11, 11))
        rr = 4.4 + rng.uniform(-0.3, 0.2)
        clumps.append((Vector((rr * math.cos(a), rr * math.sin(a), 8.8 + rng.uniform(-0.45, 0.4))),
                       2.42 + rng.uniform(-0.25, 0.2), hues[5 + k]))
    # two extra clumps break the ring silhouette (one bulging out at mid height, one high on a shoulder)
    a = math.radians(160)
    clumps.append((Vector((5.0 * math.cos(a), 5.0 * math.sin(a), 9.9)), 1.95, hues[10]))
    a = math.radians(-40)
    clumps.append((Vector((2.3 * math.cos(a), 2.3 * math.sin(a), 13.3)), 2.05, hues[11]))
    centre = Vector((0, 0, 10.0))
    blobs = []
    for c, r, _h in clumps:
        blobs.append((c, r, 0.74, 1.0))
        out = c - centre
        out = out.normalized() if out.length > 1e-6 else Vector((0, 0, 1))
        for j in range(rng.randint(7, 10)):
            for _ in range(40):
                d = Vector((rng.gauss(0, 1), rng.gauss(0, 1), rng.gauss(0, 1))).normalized()
                if d.dot(out) * 0.7 + d.z * 0.6 > 0.15:
                    break
            rs = r * rng.uniform(0.36, 0.56)
            blobs.append((c + d * (r - rs * 0.62), rs, 0.8, 1.0))
    return clumps, blobs


def bush_clumps(seed):
    rng = random.Random(seed)
    clumps = [(Vector((0.0, 0.05, 2.25)), 2.2, 0.5)]
    for k in range(6):
        a = math.radians(10 + 60 * k + rng.uniform(-10, 10))
        rr = 1.3 + rng.uniform(-0.08, 0.08)
        clumps.append((Vector((rr * math.cos(a), rr * math.sin(a), 1.2 + rng.uniform(-0.12, 0.15))),
                       1.37 + rng.uniform(-0.07, 0.08), rng.random()))
    for k in range(3):
        a = math.radians(40 + 120 * k + rng.uniform(-15, 15))
        clumps.append((Vector((0.85 * math.cos(a), 0.85 * math.sin(a), 3.0 + rng.uniform(-0.1, 0.15))),
                       1.3 + rng.uniform(-0.1, 0.1), rng.random()))
    centre = Vector((0, 0, 1.8))
    blobs = []
    for c, r, _h in clumps:
        blobs.append((c, r, 0.7, 1.0))
        out = c - centre
        out = out.normalized() if out.length > 1e-6 else Vector((0, 0, 1))
        for j in range(rng.randint(6, 8)):
            for _ in range(40):
                d = Vector((rng.gauss(0, 1), rng.gauss(0, 1), rng.gauss(0, 1))).normalized()
                if d.dot(out) * 0.7 + d.z * 0.6 > 0.1 and (c + d * r).z > 0.6:
                    break
            rs = r * rng.uniform(0.36, 0.52)
            blobs.append((c + d * (r - rs * 0.64), rs, 0.8, 1.0))
    return clumps, blobs


# ================================================================== leaves
LEAF_U = np.array([0.0, 0.18, 0.4, 0.62, 0.82])
LEAF_V = np.array([-1.0, 0.0, 1.0])


def leaf_template():
    F = []
    for r in range(4):
        for c in range(2):
            a, b = r * 3 + c, r * 3 + c + 1
            cc, d = (r + 1) * 3 + c + 1, (r + 1) * 3 + c
            F += [(a, d, cc), (a, cc, b)]
    F += [(12, 15, 13), (13, 15, 14)]
    return np.array(F, np.int32)


def scatter_leaves(name, base, n_leaves, P, colour_fn, seed):
    """Sculpted leaves over the base surface. P: dict(L=(lo,hi), wk=(lo,hi), tilt=(lo,hi), sink, fold, curl,
    centre). colour_fn(pos, nrm, rng) -> (per-leaf base colour (n,3), tip colour (n,3), roughness (n,))."""
    V, T, N = obj_arrays(base)
    A, B, C = V[T[:, 0]], V[T[:, 1]], V[T[:, 2]]
    area = 0.5 * np.linalg.norm(np.cross(B - A, C - A), axis=1)
    rng = np.random.default_rng(seed)
    idx = rng.choice(len(T), n_leaves, p=area / area.sum())
    r1 = np.sqrt(rng.random(n_leaves))
    r2 = rng.random(n_leaves)
    wa, wb, wc = 1 - r1, r1 * (1 - r2), r1 * r2
    pos = A[idx] * wa[:, None] + B[idx] * wb[:, None] + C[idx] * wc[:, None]
    n = nrm(N[T[idx, 0]] * wa[:, None] + N[T[idx, 1]] * wb[:, None] + N[T[idx, 2]] * wc[:, None])
    # leaf direction: down-slope mixed with outward from the canopy centre, random yaw
    g = np.array([0.0, 0.0, -1.0])
    down = g[None, :] - n * (n @ g)[:, None]
    radial = pos - np.asarray(P["centre"])[None, :]
    radial[:, 2] *= 0.3
    radial = radial - n * np.sum(radial * n, 1)[:, None]
    d = nrm(nrm(down) * 0.6 + nrm(radial) * 0.55 + 1e-4 * rng.standard_normal((n_leaves, 3)))
    yaw = rng.uniform(-1.0, 1.0, n_leaves)
    s2 = np.cross(n, d)
    d = nrm(d * np.cos(yaw)[:, None] + s2 * np.sin(yaw)[:, None])
    tilt = rng.uniform(*P["tilt"], n_leaves)
    dp = nrm(d * np.cos(tilt)[:, None] + n * np.sin(tilt)[:, None])
    side = nrm(np.cross(n, dp))
    up = nrm(np.cross(dp, side))
    Ls = rng.uniform(*P["L"], n_leaves)
    Ws = Ls * rng.uniform(*P["wk"], n_leaves)
    fold = rng.uniform(*P["fold"], n_leaves)
    curl = rng.uniform(*P["curl"], n_leaves)
    base_pt = pos - n * P["sink"] - dp * (0.12 * Ls)[:, None]
    u = np.concatenate([np.repeat(LEAF_U, 3), [1.0]])
    v = np.concatenate([np.tile(LEAF_V, 5), [0.0]])
    w = 0.5 * np.sin(np.pi * np.clip(u, 0, 1) ** 0.85) ** 0.8
    w[0:3] = 0.05  # narrow stalk end
    # (n, 16, 3)
    X = (base_pt[:, None, :] + dp[:, None, :] * (u[None, :, None] * Ls[:, None, None])
         + side[:, None, :] * (v[None, :, None] * w[None, :, None] * Ws[:, None, None])
         + up[:, None, :] * ((fold[:, None] * np.abs(v)[None, :] * w[None, :] * Ws[:, None]
                              + curl[:, None] * Ls[:, None] * u[None, :] ** 2)[:, :, None]))
    tmpl = leaf_template()
    # orientation check on leaf 0: the face normal must agree with `up`
    p0, p1, p2 = X[0, tmpl[0, 0]], X[0, tmpl[0, 1]], X[0, tmpl[0, 2]]
    if np.dot(np.cross(p1 - p0, p2 - p0), up[0]) < 0:
        tmpl = tmpl[:, [0, 2, 1]]
    F = (tmpl[None, :, :] + 16 * np.arange(n_leaves)[:, None, None]).reshape(-1, 3)
    cb, ct, rough = colour_fn(pos, n, rng)
    # per-vertex: dark at the stalk, tip colour toward the tip, mid-rib a touch lighter
    k_tip = np.clip(u, 0, 1) ** 1.4
    col = cb[:, None, :] * (1 - k_tip)[None, :, None] + ct[:, None, :] * k_tip[None, :, None]
    shade = 0.72 + 0.28 * np.clip(u / 0.4, 0, 1)
    rib = np.where(v == 0, 1.1, 1.0)
    col = col * (shade * rib)[None, :, None]
    ob = mesh_np(name, X.reshape(-1, 3), F)
    set_colors(ob.data, "Col", np.clip(col.reshape(-1, 3), 0, 1))
    rr = np.repeat(rough[:, None], 16, 1).reshape(-1)
    set_colors(ob.data, "Rough", np.stack([rr, rr, rr], 1))
    return ob, pos, n


def autumn_ramp(t):
    """t in [0,1]: deep crimson -> red -> red-orange -> orange -> amber."""
    stops = [(0.0, (128, 20, 16)), (0.22, (184, 34, 20)), (0.45, (218, 72, 22)), (0.68, (236, 118, 26)),
             (0.86, (240, 152, 34)), (1.0, (236, 178, 52))]
    t = np.clip(t, 0, 1)
    out = np.zeros((len(t), 3))
    for (t0, c0), (t1, c1) in zip(stops[:-1], stops[1:]):
        m = (t >= t0) & (t <= t1)
        k = ((t[m] - t0) / (t1 - t0))[:, None]
        out[m] = L(c0) * (1 - k) + L(c1) * k
    return out


def tree_leaf_colours(clumps):
    cc = np.array([tuple(c) for c, r, h in clumps])
    cr = np.array([r for c, r, h in clumps])
    ch = np.array([h for c, r, h in clumps])

    def fn(pos, n, rng):
        m = len(pos)
        dist = np.linalg.norm(pos[:, None, :] - cc[None, :, :], axis=2) / cr[None, :]
        owner = np.argmin(dist, 1)
        mott = noise_field(pos, 0.35, 2, (11.0, 3.0, 7.0), 0.55)
        t = ch[owner] * 0.75 + 0.12 + mott + rng.normal(0, 0.1, m)
        cb = autumn_ramp(t)
        ct = autumn_ramp(t - 0.12 + rng.normal(0, 0.05, m))        # tips a little redder
        rnd = rng.random(m)
        yel = rnd < 0.05
        cb[yel] = L((236, 196, 74))
        ct[yel] = L((226, 170, 52))
        brn = (rnd > 0.96)
        cb[brn] = L((150, 70, 32))
        ct[brn] = L((116, 52, 26))
        # light from above: top leaves a bit brighter, underside leaves duller/darker
        up = np.clip(n[:, 2], -1, 1)
        k = (0.78 + 0.22 * (up * 0.5 + 0.5))[:, None]
        cb *= k
        ct *= k
        rough = rng.uniform(0.5, 0.68, m)
        return cb, ct, rough
    return fn


def bush_leaf_colours(clumps, centre, rmax, zmax):
    """Deep green body; the autumn colour climbs in from the top and the outer bulges, strongest at each leaf's
    tip (green stalk end -> orange / red / gold tip)."""
    def fn(pos, n, rng):
        m = len(pos)
        rel = pos - np.asarray(centre)[None, :]
        outer = np.clip(np.linalg.norm(rel[:, :2], axis=1) / rmax, 0, 1)
        height = np.clip(pos[:, 2] / zmax, 0, 1)
        patch = noise_field(pos, 0.55, 2, (5.0, 9.0, 2.0), 1.0)
        fac = 0.25 * outer + 0.85 * height + 0.45 * patch + rng.normal(0, 0.04, m)
        a = sstep(0.45, 0.85, fac)
        g_t = rng.random(m)
        greens = L((22, 70, 26)) * (1 - g_t)[:, None] + L((56, 116, 38)) * g_t[:, None]
        greens *= (0.82 + 0.3 * np.clip(n[:, 2] * 0.5 + 0.5, 0, 1))[:, None]
        olive = L((104, 132, 40))
        pick = rng.random(m)
        warm = np.where((pick < 0.42)[:, None], L((230, 116, 28)),
                        np.where((pick < 0.75)[:, None], L((196, 46, 24)), L((232, 172, 44))))
        warm *= rng.uniform(0.85, 1.05, m)[:, None]
        # stalk end: green, a touch warmer where the leaf is turning
        cb = greens * (1 - 0.35 * a)[:, None] + olive * (0.35 * a)[:, None]
        full = 0.85 * sstep(0.5, 1.0, a)               # fully turned leaves on the crown: warm stalk to tip
        cb = cb * (1 - full)[:, None] + warm * 0.78 * full[:, None]
        # tip: olive on the green leaves, the warm colour on the turning ones
        k = np.clip(0.15 + 1.05 * a, 0, 1)
        ct = (greens * 0.75 + olive * 0.25) * (1 - k)[:, None] + warm * k[:, None]
        rough = rng.uniform(0.5, 0.66, m)
        return cb, ct, rough
    return fn


# ================================================================== trunk (skeleton -> tubes -> voxel union)
def add_branch(br, ctrl, radii, kind, step=0.08):
    D = np.hstack([np.asarray(ctrl, np.float64), np.asarray(radii, np.float64)[:, None]])
    Dd = cr_dense(D, 14)
    Ps, s = arc_resample(Dd, step)
    br.append(dict(P=Ps[:, :3], R=Ps[:, 3], s=s, kind=kind))
    return br[-1]


def point_on(b, f):
    i = int(round(f * (len(b["P"]) - 1)))
    return Vector(b["P"][i]), float(b["R"][i]), i


def tree_skeleton(clumps, seed):
    rng = random.Random(seed)
    br = []
    ctrl = [(0, 0, -0.45), (0.03, 0.0, 0.5), (0.2, 0.08, 1.7), (0.4, 0.2, 2.9), (0.26, 0.32, 4.0),
            (0.0, 0.28, 4.9), (-0.1, 0.22, 5.7)]
    radii = [1.15, 1.04, 0.95, 0.88, 0.82, 0.74, 0.62]
    tr = add_branch(br, ctrl, radii, "trunk")
    z = tr["P"][:, 2]
    tr["R"] = tr["R"] * (1 + 0.5 * np.exp(-np.maximum(0, z + 0.45) / 0.55))
    # roots
    for k in range(6):
        a = math.radians(25 + 60 * k + rng.uniform(-12, 12))
        d = Vector((math.cos(a), math.sin(a), 0))
        ln = rng.uniform(2.3, 2.8)
        side = Vector((-d.y, d.x, 0)) * rng.uniform(-0.25, 0.25)
        add_branch(br, [tuple(d * 0.25 + Vector((0, 0, 0.9))), tuple(d * 1.0 + Vector((0, 0, 0.28))),
                        tuple(d * 1.7 + side + Vector((0, 0, -0.02))), tuple(d * ln + side * 1.6 + Vector((0, 0, -0.2)))],
                   [0.5, 0.36, 0.22, 0.09], "root")
    trunk_P = tr["P"]

    def trunk_at(zq):
        i = int(np.argmin(np.abs(trunk_P[:, 2] - zq)))
        return Vector(trunk_P[i])
    limbs = []
    lower = clumps[6:11]
    for k, (c, r, h) in enumerate(lower):
        S = trunk_at(4.55 + 0.22 * k)
        hdir = Vector((c.x - S.x, c.y - S.y, 0)).normalized()
        perp = Vector((-hdir.y, hdir.x, 0)) * rng.uniform(-0.35, 0.35)
        p1 = S + hdir * 0.85 + Vector((0, 0, 0.75))
        p2 = S + hdir * 2.0 + Vector((0, 0, 1.45)) + perp
        p3 = c + (S - c).normalized() * r * 0.45
        limbs.append(add_branch(br, [tuple(S), tuple(p1), tuple(p2), tuple(p3), tuple(c)],
                                [0.56, 0.46, 0.36, 0.26, 0.19], "limb"))
    lead = add_branch(br, [tuple(trunk_at(5.6)), (-0.25, 0.12, 7.4), (0.1, -0.1, 9.6), tuple(clumps[0][0])],
                      [0.58, 0.44, 0.32, 0.19], "limb")
    # secondary branches: each upper clump from the nearest limb
    for c, r, h in clumps[1:6]:
        best = min(limbs, key=lambda b: (Vector(b["P"][int(len(b["P"]) * 0.5)]) - c).length)
        p, rr, i = point_on(best, 0.5)
        add_branch(br, [tuple(p), tuple(p + (c - p) * 0.45 + Vector((0, 0, 0.35))), tuple(c)],
                   [min(rr, 0.27), 0.19, 0.12], "sec")
    # twigs poking out of the gaps between the lower clumps (TP snag points)
    twigs = []
    for k in (0, 2, 3):
        b = limbs[k]
        p, rr, i = point_on(b, 0.62)
        c1 = lower[k][0]
        c2 = lower[(k + 1) % 5][0]
        mid = Vector(((c1.x + c2.x) / 2, (c1.y + c2.y) / 2, 0))
        hd = (mid - Vector((p.x, p.y, 0))).normalized()
        out = mid.normalized() * 6.2
        tip = Vector((out.x, out.y, 7.55 + rng.uniform(-0.2, 0.25)))
        m1 = p + hd * 1.0 + Vector((0, 0, 0.25))
        twigs.append(add_branch(br, [tuple(p), tuple(m1), tuple((m1 + tip) * 0.5 + Vector((0, 0, 0.15))),
                                     tuple(tip)], [min(rr, 0.2), 0.15, 0.11, 0.075], "twig"))
    # two sawn-off stubs on the trunk
    for zq, a in ((2.2, 200.0), (3.5, 320.0)):
        p = trunk_at(zq)
        d = Vector((math.cos(math.radians(a)), math.sin(math.radians(a)), 0.18)).normalized()
        add_branch(br, [tuple(p), tuple(p + d * 1.05)], [0.24, 0.19], "stub")
    return br, limbs, twigs, lead


def skeleton_mesh(name, br, nside_fn):
    Vs, Fs, off = [], [], 0
    for b in br:
        V, F = tube_arrays(b["P"], b["R"], nside_fn(b))
        Vs.append(V)
        Fs.append(F + off)
        off += len(V)
    return mesh_np(name, np.vstack(Vs), np.vstack(Fs))


def skeleton_segments(br):
    A, Bv, R0, R1, S0, NN, BB, BID = [], [], [], [], [], [], [], []
    for k, b in enumerate(br):
        P = b["P"]
        T, N, Bn = transport_frames(P)
        A.append(P[:-1])
        Bv.append(P[1:])
        R0.append(b["R"][:-1])
        R1.append(b["R"][1:])
        S0.append(b["s"][:-1] + 37.0 * k)
        NN.append(N[:-1])
        BB.append(Bn[:-1])
        BID.append(np.full(len(P) - 1, k))
    return dict(A=np.vstack(A), B=np.vstack(Bv), R0=np.concatenate(R0), R1=np.concatenate(R1),
                S0=np.concatenate(S0), N=np.vstack(NN), Bn=np.vstack(BB), bid=np.concatenate(BID))


def nearest_skeleton(V, sk, chunk=800):
    """Per vertex: owning segment (min distance - radius), param t, local angle, radius, arc length."""
    A, B = sk["A"], sk["B"]
    AB = B - A
    l2 = np.maximum(1e-12, np.sum(AB * AB, 1))
    out_seg = np.empty(len(V), np.int64)
    out_t = np.empty(len(V))
    for i0 in range(0, len(V), chunk):
        P = V[i0:i0 + chunk].astype(np.float64)
        AP = P[:, None, :] - A[None, :, :]
        t = np.clip(np.einsum("ijk,jk->ij", AP, AB) / l2[None, :], 0, 1)
        Q = A[None, :, :] + t[:, :, None] * AB[None, :, :]
        d = np.linalg.norm(P[:, None, :] - Q, axis=2)
        rr = sk["R0"][None, :] * (1 - t) + sk["R1"][None, :] * t
        j = np.argmin(d - rr, 1)
        out_seg[i0:i0 + chunk] = j
        out_t[i0:i0 + chunk] = t[np.arange(len(P)), j]
    j, t = out_seg, out_t
    Q = A[j] + AB[j] * t[:, None]
    rv = V - Q
    x = np.sum(rv * sk["N"][j], 1)
    y = np.sum(rv * sk["Bn"][j], 1)
    ang = np.arctan2(y, x)
    s = sk["S0"][j] + t * np.sqrt(l2[j])
    rloc = sk["R0"][j] * (1 - t) + sk["R1"][j] * t
    return j, ang, s, rloc


def bark(V, sk, seed):
    """Displacement (along the normal) + colour + roughness for stylised bark: long wavy fissures, rounded plates,
    a faint spiral, lichen speckles and moss at the root collar."""
    j, ang, s, rloc = nearest_skeleton(V, sk)
    rng = random.Random(seed)
    o1 = Vector((rng.uniform(-50, 50), rng.uniform(-50, 50), rng.uniform(-50, 50)))
    o2 = Vector((rng.uniform(-50, 50), rng.uniform(-50, 50), rng.uniform(-50, 50)))
    n = len(V)
    disp = np.empty(n)
    fis = np.empty(n)
    lich = np.empty(n)
    for i in range(n):
        r = rloc[i]
        kr = 0.55 + 1.3 * min(r, 1.1)
        a = ang[i] + 0.22 * s[i]
        q = Vector((math.cos(a) * kr, math.sin(a) * kr, s[i] * 0.62)) + o1
        nz = noise.noise(q * 1.6)
        f = 1.0 - smoothstep(0.0, 0.2, abs(nz))
        plate = noise.noise(q * 4.5 + o2) * 0.5 + noise.noise(q * 11.0) * 0.25
        depth = 0.022 + 0.055 * min(1.0, r / 0.8)
        disp[i] = -depth * f ** 0.8 + depth * 0.18 * plate
        fis[i] = f
        lich[i] = noise.noise(Vector((float(V[i, 0]), float(V[i, 1]), float(V[i, 2]))) * 1.7 + o2)
    base = L((112, 84, 62))
    ridge = L((150, 124, 98))
    deep = L((44, 30, 24))
    col = base[None, :] * np.ones((n, 1))
    col = col + (ridge - base)[None, :] * np.clip(1 - fis * 1.6, 0, 1)[:, None] * 0.55
    col = col * (1 - 0.8 * fis)[:, None] + deep[None, :] * (0.8 * fis)[:, None]
    lk = np.clip((lich - 0.28) / 0.2, 0, 1) * (1 - fis)
    col = col * (1 - 0.45 * lk)[:, None] + L((150, 156, 128))[None, :] * (0.45 * lk)[:, None]
    z = V[:, 2]
    moss = np.clip(1 - (z - 0.1) / 0.9, 0, 1) * np.clip((lich + 0.2) / 0.4, 0, 1)
    col = col * (1 - 0.6 * moss)[:, None] + L((70, 92, 38))[None, :] * (0.6 * moss)[:, None]
    rough = 0.8 + 0.12 * fis
    return disp, col, rough


def build_trunk(br, canopy_base, hi_voxel, lo_tris, seed):
    nside = lambda b: 28 if b["kind"] in ("trunk",) else (18 if b["kind"] in ("limb", "root") else 12)
    raw = skeleton_mesh("TrunkRaw", br, nside)
    base = remesh(raw, hi_voxel, 4, 0.6)
    base.name = "TrunkBase"
    V, T, N = obj_arrays(base)
    V[:, 2] = np.maximum(V[:, 2], -0.3)
    set_co(base, V)
    sk = skeleton_segments(br)
    # HI: bark
    hi = link(bpy.data.objects.new("TrunkHi", base.data.copy()))
    V, T, N = obj_arrays(hi)
    disp, col, rough = bark(V, sk, seed)
    V = V + N * disp[:, None].astype(np.float32)
    set_co(hi, V)
    set_colors(hi.data, "Col", col)
    set_colors(hi.data, "Rough", np.stack([rough] * 3, 1))
    hi.data.materials.append(mat_vc("BarkHi"))
    # LO: delete what hides inside the canopy and under the ground, then decimate
    cb = bvh_ob(canopy_base)
    C = face_centers(base)
    kill = np.zeros(len(C), bool)
    for i, c in enumerate(C):
        loc, nr, idx, dist = cb.find_nearest(Vector(c.tolist()))
        if loc is not None and (Vector(c.tolist()) - loc).dot(nr) < -0.35:
            kill[i] = True
    kill |= C[:, 2] < -0.14
    delete_faces(base, kill)
    lo = decimate_to(base, "Trunk", lo_tris)
    bpy.data.objects.remove(base)
    return hi, lo, sk


def decimate_to(src, name, tris):
    """Copy of src decimated (collapse) to about `tris` triangles, triangulated, attributes stripped."""
    lo = link(bpy.data.objects.new(name, src.data.copy()))
    have = tri_count(lo)
    dec = lo.modifiers.new("Decimate", "DECIMATE")
    dec.ratio = min(1.0, tris / max(1, have))
    lo.modifiers.new("Tri", "TRIANGULATE")
    apply_mods(lo)
    lo.data.name = name
    for a in list(lo.data.color_attributes):
        lo.data.color_attributes.remove(a)
    lo.data.shade_smooth()
    return lo


# ================================================================== TP: rope simulation
TP_W = 0.45
TP_T = 0.06
HW = TP_W / 2
PERIM = 2 * TP_W + 2 * TP_T          # 1.02: TL->TR (top) ->BR (edge) ->BL (bottom) ->TL (edge)
TP_RGB = (236, 232, 220)


def sstep(a, b, x):
    t = np.clip((np.asarray(x, np.float64) - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


class Colliders:
    def __init__(self, zg):
        self.items = []
        self.zg = zg

    def add(self, bvh, r, kind):
        self.items.append((bvh, r, kind))

    def push(self, p):
        contact = None
        for bvh, r, kind in self.items:
            loc, nr, idx, dist = bvh.find_nearest(p, r + 0.6)
            if loc is None:
                continue
            d = (p - loc).dot(nr)
            if d < r:
                p = p + nr * (r - d)
                contact = nr
        if p.z < self.zg:
            p = Vector((p.x, p.y, self.zg))
            contact = Vector((0, 0, 1))
        return p, contact

    def nearest(self, p, kinds=None):
        best = (9e9, None, None)
        for bvh, r, kind in self.items:
            if kinds and kind not in kinds:
                continue
            loc, nr, idx, dist = bvh.find_nearest(p, 3.0)
            if loc is None:
                continue
            d = (p - loc).dot(nr) - r
            if d < best[0]:
                best = (d, nr, kind)
        dg = p.z - self.zg
        if dg < best[0]:
            best = (dg, Vector((0, 0, 1)), "ground")
        return best

    def ray_outer(self, origin, direction, kinds=None):
        best = None
        for bvh, r, kind in self.items:
            if kinds and kind not in kinds:
                continue
            loc, nr, idx, dist = bvh.ray_cast(origin, direction, 200.0)
            if loc is not None and (best is None or dist < best[3]):
                if nr.dot(direction) > 0:
                    nr = -nr
                best = (loc, nr, r, dist)
        return best


def simulate(X0, rest, pinned, col, steps=320, iters=20, grav=0.003, fric=0.88, bend_min=1.5, ds=0.1):
    X = X0.copy()
    Xp = X0.copy()
    n = len(X)
    w = np.ones(n)
    w[pinned] = 0.0
    ev = np.arange(0, n - 1, 2)
    od = np.arange(1, n - 1, 2)
    bgroups = [np.arange(c, n - 1, 4) for c in (1, 2, 3, 4)]
    bmin = bend_min * ds
    for step in range(steps):
        damp = 0.94 if step < steps - 80 else 0.75
        Vv = (X - Xp) * damp
        sp = np.linalg.norm(Vv, axis=1)
        big = sp > 0.045
        Vv[big] *= (0.045 / sp[big])[:, None]
        Xp = X.copy()
        X = X + Vv
        X[:, 2] -= grav * w
        for it in range(iters):
            for S in (ev, od):
                a, b = S, S + 1
                d = X[b] - X[a]
                ln = np.maximum(1e-9, np.linalg.norm(d, axis=1))
                ws = w[a] + w[b]
                k = np.where(ws > 0, (ln - rest[S]) / ln / np.maximum(ws, 1e-9), 0.0)[:, None] * d
                X[a] += k * w[a][:, None]
                X[b] -= k * w[b][:, None]
            if it % 3 == 0:
                for G in bgroups:
                    if len(G) == 0:
                        continue
                    a, b = G - 1, G + 1
                    d = X[b] - X[a]
                    ln = np.maximum(1e-9, np.linalg.norm(d, axis=1))
                    short = ln < bmin
                    if not short.any():
                        continue
                    ws = w[a] + w[b]
                    k = np.where(short & (ws > 0), (ln - bmin) / ln / np.maximum(ws, 1e-9), 0.0)[:, None] * d * 0.5
                    X[a] += k * w[a][:, None]
                    X[b] -= k * w[b][:, None]
        for i in range(n):
            if w[i] == 0:
                continue
            q, c = col.push(Vector(X[i].tolist()))
            if c is not None:
                X[i] = (q.x, q.y, q.z)
                Xp[i] = X[i] - (X[i] - Xp[i]) * (1 - fric)
    return X


def surf_dir(col, centre, az, el, kinds=("canopy",)):
    d = Vector((math.cos(math.radians(el)) * math.cos(math.radians(az)),
                math.cos(math.radians(el)) * math.sin(math.radians(az)), math.sin(math.radians(el))))
    hit = col.ray_outer(Vector(centre) + d * 40.0, -d, kinds)
    if hit is None:
        raise RuntimeError("no canopy hit at az %s el %s" % (az, el))
    loc, nr, r, dist = hit
    return loc + nr * (r + 0.02), nr


def branch_top(b, f, extra):
    P = b["P"]
    i = int(round(f * (len(P) - 1)))
    i = max(1, min(len(P) - 2, i))
    t = Vector((P[i + 1] - P[i - 1]).tolist()).normalized()
    up = Vector((0, 0, 1)) - t * t.z
    up = up.normalized() if up.length > 1e-6 else Vector((1, 0, 0))
    side = t.cross(Vector((0, 0, 1)))
    side = side.normalized() if side.length > 1e-6 else Vector((1, 0, 0))
    return Vector(P[i].tolist()) + up * (float(b["R"][i]) + extra), up, side


def init_tail(start, first_dir, length, col, ds):
    """Walk down from `start`: gravity plus a little of the incoming direction; pushed out of everything."""
    pts = []
    p = Vector(start)
    dv = Vector(first_dir).normalized() if Vector(first_dir).length > 1e-6 else Vector((0, 0, -1))
    n = max(1, int(round(length / ds)))
    for i in range(n):
        k = max(0.0, 1.0 - i / 6.0)
        step = (dv * (0.4 + 0.8 * k) + Vector((0, 0, -1.0))).normalized() * ds
        q, c = col.push(p + step)
        q, c = col.push(q)
        q = p + (q - p).normalized() * ds
        pts.append(q)
        dv = (q - p).normalized()
        p = q
    return pts


def resolve_nodes(spec, ctx):
    col, centre = ctx["col"], ctx["centre"]
    out = []
    for nd in spec["nodes"]:
        if nd[0] == "dir":
            p, n = surf_dir(col, centre, nd[1], nd[2])
            out.append((p, n, None))
        elif nd[0] in ("limb", "twig"):
            b = ctx["limbs"][nd[1]] if nd[0] == "limb" else ctx["twigs"][nd[1]]
            p, up, side = branch_top(b, nd[2], 0.075)
            out.append((p, up, side))
        elif nd[0] == "pt":
            out.append((Vector(nd[1]), Vector(nd[2]) if len(nd) > 2 else Vector((0, 0, 1)), None))
    return out


def init_ribbon(spec, ctx, ds):
    """Initial polyline (array), rest lengths, pinned indices."""
    col, centre = ctx["col"], Vector(ctx["centre"])
    nodes = resolve_nodes(spec, ctx)
    pts, rest, pins = [], [], []
    node_idx = []
    pts.append(nodes[0][0])
    node_idx.append(0)
    for k in range(len(nodes) - 1):
        a, b = nodes[k][0], nodes[k + 1][0]
        kind = spec["spans"][k]
        if kind == "drape":
            da = (a - centre).normalized()
            db = (b - centre).normalized()
            ang = math.acos(max(-1.0, min(1.0, da.dot(db))))
            m = max(4, int(ang * 7.0 / ds))
            seg = [a]
            for j in range(1, m):
                t = j / m
                dd = (da * math.sin((1 - t) * ang) + db * math.sin(t * ang)) / max(1e-6, math.sin(ang))
                el = math.degrees(math.asin(max(-1.0, min(1.0, dd.z))))
                az = math.degrees(math.atan2(dd.y, dd.x))
                p, _n = surf_dir(col, centre, az, el, kinds=("canopy", "ribbon"))
                seg.append(p)
            seg.append(b)
            D = np.array([tuple(p) for p in seg])
            Dr, si = arc_resample(D, ds)
            slack = 1.0
        else:
            slack = float(kind.split(":")[1])
            c = (b - a).length
            ln = c * slack
            h = math.sqrt(max(0.0, 3 * c * (ln - c) / 8.0))
            m = 40
            D = np.array([tuple(a.lerp(b, j / m) - Vector((0, 0, h * 4 * (j / m) * (1 - j / m)))) for j in range(m + 1)])
            Dr, si = arc_resample(cr_dense(D, 4), ds)
        step = si[1] - si[0]
        for j in range(1, len(Dr)):
            pts.append(Vector(Dr[j].tolist()))
            rest.append(step * slack if kind == "drape" else step)
        node_idx.append(len(pts) - 1)
    # tails
    t0, t1 = spec.get("tail0", 0.0), spec.get("tail1", 0.0)
    side_hint = nodes[0][2] if nodes[0][2] is not None else Vector((1, 0, 0))
    pre = []
    if t0 > 0:
        d0 = Vector(spec["dir0"]) if "dir0" in spec else ((pts[0] - pts[1]) if len(pts) > 1 else -side_hint)
        pre = init_tail(pts[0], d0, t0, col, ds)
    post = []
    if t1 > 0:
        d1 = Vector(spec["dir1"]) if "dir1" in spec else ((pts[-1] - pts[-2]) if len(pts) > 1 else side_hint)
        post = init_tail(pts[-1], d1, t1, col, ds)
    allp = list(reversed(pre)) + pts + post
    rest_all = [ds] * len(pre) + rest + [ds] * len(post)
    off = len(pre)
    for k, nd in enumerate(spec["nodes"]):
        if spec["pins"][k]:
            pins.append(node_idx[k] + off)
    X = np.array([tuple(p) for p in allp], np.float64)
    if spec.get("start_pin"):
        pins += [0, 1]
    return X, np.array(rest_all), sorted(set(pins)), off, node_idx


def laplace(X, pinned, it=2, k=0.35):
    m = np.ones(len(X), bool)
    m[list(pinned)] = False
    for _ in range(it):
        Y = X.copy()
        Y[1:-1] = X[1:-1] + k * (0.5 * (X[:-2] + X[2:]) - X[1:-1])
        X = np.where(m[:, None], Y, X)
    return X


def rotate_about(v, axis, ang):
    """Rodrigues, rows."""
    c, s = np.cos(ang), np.sin(ang)
    return v * c + np.cross(axis, v) * s + axis * np.sum(axis * v, -1, keepdims=True) * (1 - c)


def ribbon_frames(X, col, spec, ds):
    n = len(X)
    T = nrm(np.gradient(X, axis=0))
    clear = np.empty(n)
    Nc = np.zeros((n, 3))
    for i in range(n):
        d, nr, kind = col.nearest(Vector(X[i].tolist()))
        clear[i] = d
        if nr is not None:
            Nc[i] = (nr.x, nr.y, nr.z)
    contact = clear < 0.09
    sn = spec.get("start_normal")
    if sn is not None:
        Nc[0] = tuple(sn)
        contact[0] = True
    Nc = nrm(Nc - T * np.sum(Nc * T, 1)[:, None])
    N = np.zeros((n, 3))
    tw = spec.get("twist", 0.16) * 2 * math.pi
    idx = np.nonzero(contact)[0]

    def walk(i_from, i_to, n0, sgn, rate):
        cur = n0.copy()
        out = {}
        rng_ = range(i_from, i_to + 1) if i_to >= i_from else range(i_from, i_to - 1, -1)
        dist = 0.0
        for i in rng_:
            cur = cur - T[i] * np.dot(cur, T[i])
            cur = cur / max(1e-12, np.linalg.norm(cur))
            if i != i_from:
                dist += ds
                ang = sgn * rate * ds * (1.0 + 0.25 * dist)
                cur = rotate_about(cur[None, :], T[i][None, :], ang)[0]
            out[i] = cur
        return out
    if len(idx) == 0:
        h = np.cross(T[0], [0, 0, 1.0])
        if np.linalg.norm(h) < 1e-3:
            h = np.array([1.0, 0, 0])
        N = np.array([v for k, v in sorted(walk(0, n - 1, nrm(h), 1, tw).items())])
    else:
        prev = None
        for i in idx:                          # contact points: the surface normal, sign kept continuous
            v = Nc[i]
            if prev is not None and np.dot(v, prev) < 0 and contact[i - 1]:
                v = -v
            N[i] = v
            prev = v
        if idx[0] > 0:                          # free start: walk backward from the first contact
            for i, v in walk(idx[0], 0, N[idx[0]], -1, tw).items():
                N[i] = v
        if idx[-1] < n - 1:                     # free end: walk forward from the last contact
            for i, v in walk(idx[-1], n - 1, N[idx[-1]], 1, tw).items():
                N[i] = v
        for a, b in zip(idx[:-1], idx[1:]):     # free runs between contacts: transport + spread the mismatch
            if b - a <= 1:
                continue
            fw = walk(a, b, N[a], 1, tw * 0.35)
            end = fw[b]
            tgt = N[b] if np.dot(N[b], end) >= 0 else -N[b]
            ang = math.atan2(np.dot(np.cross(end, tgt), T[b]), np.dot(end, tgt))
            for i in range(a + 1, b):
                N[i] = rotate_about(fw[i][None, :], T[i][None, :], ang * (i - a) / (b - a))[0]
    N = nrm(N - T * np.sum(N * T, 1)[:, None])
    for i in range(1, n):                       # the strip is two-sided: keep N's sign continuous
        if np.dot(N[i], N[i - 1]) < 0:
            N[i] = -N[i]
    return T, N, contact


def sway_tails(X, contact, pinned, seed, amp=0.1, grow=0.05, lam=3.2):
    """A gentle corkscrew sway on the free-hanging tail ends (grows with the distance from the last support)."""
    rng = random.Random(seed)
    n = len(X)
    anchor = contact.copy()
    anchor[list(pinned)] = True
    Y = X.copy()
    idx = np.nonzero(anchor)[0]
    if len(idx) == 0:
        return Y
    for direction, start in ((1, idx[-1]), (-1, idx[0])):
        ph = rng.uniform(0, 6.28)
        dist = 0.0
        i = start + direction
        while 0 <= i < n:
            dist += 0.1
            a = (amp + grow * dist) * float(sstep(0.0, 1.2, dist))
            Y[i] += np.array([math.cos(ph + dist * 6.283 / lam), math.sin(ph + dist * 6.283 / lam), 0.0]) * a
            i += direction
    return Y


# ------------------------------------------------------------------ ribbon section geometry
def edge_wave(s, side, ph):
    if side < 0:
        return 0.017 * np.sin(2 * np.pi * s / 0.86 + ph[0])
    return 0.017 * np.sin(2 * np.pi * s / 0.71 + ph[1])


def crumple(s, x, off):
    """Mid-surface offset (along N) for the HI ribbon: crumple folds, mostly running across the strip."""
    out = np.empty(len(s))
    o = Vector(off)
    for i in range(len(s)):
        q = Vector((float(s[i]) * 3.4, float(x[i]) * 1.6, 0.0)) + o
        r = 1.0 - abs(noise.noise(q))
        r2 = 1.0 - abs(noise.noise(q * 2.1 + Vector((3.1, 7.7, 1.3))))
        f = noise.noise(Vector((float(s[i]) * 7.0, float(x[i]) * 7.0, 5.0)) + o)
        out[i] = 0.009 * (r ** 4 - 0.25) + 0.005 * (r2 ** 4 - 0.25) + 0.003 * f
    return out


def smooth_normals(T, N, sigma=2.0):
    n = len(N)
    r = int(3 * sigma)
    ker = np.exp(-0.5 * (np.arange(-r, r + 1) / sigma) ** 2)
    Np = np.pad(N, ((r, r), (0, 0)), mode="edge")
    S = np.stack([np.convolve(Np[:, c], ker, mode="valid") for c in range(3)], 1)
    S = S - T * np.sum(S * T, 1)[:, None]
    bad = np.linalg.norm(S, axis=1) < 1e-6
    S[bad] = N[bad]
    return nrm(S)


def dense_curve(X, N, step=0.02):
    D = np.hstack([X, N])
    Dd = cr_dense(D, 6)
    s = arc_param(Dd)
    m = max(2, int(round(s[-1] / step)) + 1)
    si = np.linspace(0, s[-1], m)
    R = resample_at(Dd, s, si)
    P = R[:, :3]
    T = nrm(np.gradient(P, axis=0))
    Nn = nrm(R[:, 3:] - T * np.sum(R[:, 3:] * T, 1)[:, None])
    return P, T, Nn, si


def pick_low(P, T, Nn, si, max_len=0.26, max_turn=12.0):
    keep = [0]
    for i in range(1, len(P)):
        j = keep[-1]
        da = math.degrees(math.acos(max(-1.0, min(1.0, float(np.dot(T[i], T[j]))))))
        dn = math.degrees(math.acos(max(-1.0, min(1.0, abs(float(np.dot(Nn[i], Nn[j])))))))
        dist = si[i] - si[j]
        if dist >= max_len or ((da > max_turn or dn > max_turn) and dist > 0.03):
            keep.append(i)
    if keep[-1] != len(P) - 1:
        if si[-1] - si[keep[-1]] < 0.04 and len(keep) > 1:
            keep[-1] = len(P) - 1
        else:
            keep.append(len(P) - 1)
    return np.array(keep)


class Atlas:
    def __init__(self, size, k, margin=4):
        self.size, self.k, self.m = size, k, margin
        self.rowh = PERIM * k + margin
        self.row, self.x = 0, float(margin)

    def strip(self, s):
        """Per segment (xa, xb, row) for the section arc lengths s (studs)."""
        out = []
        x0, s0 = self.x, s[0]
        for a in range(len(s) - 1):
            xb = x0 + (s[a + 1] - s0) * self.k
            if xb > self.size - self.m:
                self.row += 1
                x0, s0 = float(self.m), s[a]
                xb = x0 + (s[a + 1] - s0) * self.k
            out.append((x0 + (s[a] - s0) * self.k, xb, self.row))
        self.x = out[-1][1] + 2 * self.m
        return out

    def row_y(self, row):
        return self.m * 0.5 + row * self.rowh

    def used_rows(self):
        return self.row + 1


def ribbon_low(P, T, Nn, si, keep, ph, atlas):
    """Box section per kept sample, vertices split per side so the box edges stay sharp: top (TL, TR), right edge
    (TR, BR), bottom (BR, BL), left edge (BL, TL), + 4 cap verts per end. Returns V, F (tris), UV per loop."""
    s = si[keep]
    C, Tk, Nk = P[keep], T[keep], Nn[keep]
    W = nrm(np.cross(Tk, Nk))
    wl = edge_wave(s, -1, ph)
    wr = edge_wave(s, 1, ph)
    TL = C - W * HW + Nk * (TP_T / 2 + wl)[:, None]
    TR = C + W * HW + Nk * (TP_T / 2 + wr)[:, None]
    BR = C + W * HW + Nk * (-TP_T / 2 + wr)[:, None]
    BL = C - W * HW + Nk * (-TP_T / 2 + wl)[:, None]
    n = len(s)
    sides = [(TL, TR), (TR, BR), (BR, BL), (BL, TL)]
    V = np.concatenate([np.stack([a_, b_], 1) for a_, b_ in sides], 1).reshape(-1, 3)   # (n, 8)
    segs = atlas.strip(s) if atlas is not None else [(0.0, 0.0, 0)] * (n - 1)
    F, UV = [], []
    pcoord = [0.0, TP_W, TP_W + TP_T, 2 * TP_W + TP_T, PERIM]
    S = atlas.size if atlas is not None else 1.0
    kk = atlas.k if atlas is not None else 1.0
    for a, (xa, xb, row) in enumerate(segs):
        y0 = atlas.row_y(row) if atlas is not None else 0.0
        for q in range(4):
            i00, i01 = a * 8 + 2 * q, a * 8 + 2 * q + 1
            i11, i10 = (a + 1) * 8 + 2 * q + 1, (a + 1) * 8 + 2 * q
            y_a = y0 + (PERIM - pcoord[q]) * kk
            y_b = y0 + (PERIM - pcoord[q + 1]) * kk
            uv00, uv01 = (xa / S, y_a / S), (xa / S, y_b / S)
            uv11, uv10 = (xb / S, y_b / S), (xb / S, y_a / S)
            F += [(i00, i01, i11), (i00, i11, i10)]
            UV += [uv00, uv01, uv11, uv00, uv11, uv10]
    base = len(V)
    caps = np.vstack([np.stack([TL[0], TR[0], BR[0], BL[0]]), np.stack([TL[-1], TR[-1], BR[-1], BL[-1]])])
    V = np.vstack([V, caps])
    for (xa, xb, row), e, first in ((segs[0], base, True), (segs[-1], base + 4, False)):
        y0 = atlas.row_y(row) if atlas is not None else 0.0
        x = xa if first else xb
        cu = [(x / S, (y0 + 0.2 * kk) / S), (x / S, (y0 + 0.25 * kk) / S), (x / S, (y0 + 0.3 * kk) / S)]
        if first:
            F += [(e, e + 3, e + 2), (e, e + 2, e + 1)]
        else:
            F += [(e, e + 1, e + 2), (e, e + 2, e + 3)]
        UV += cu + cu
    F = np.array(F, np.int32)
    UV = np.array(UV, np.float32)
    p0, p1, p2 = V[F[0, 0]], V[F[0, 1]], V[F[0, 2]]
    if np.dot(np.cross(p1 - p0, p2 - p0), Nk[0]) < 0:
        F = F[:, [0, 2, 1]]
        UV = UV.reshape(-1, 3, 2)[:, [0, 2, 1], :].reshape(-1, 2)
    return V, F, UV


def ribbon_hi(P, T, Nn, si, keep, ph, off, perf_phase):
    """HI bake source = the LO strip itself (its box section interpolated between the LO sections) + bounded detail
    only: a soft cup across the strip, crumple folds (mostly across) and perforation creases every 0.5 stud. The HI
    therefore never drifts more than ~0.025 from the LO surface, so every bake ray (cage 0.045) lands on the right
    face of the right strip. 9 verts across the top, 9 across the bottom."""
    s_low = si[keep]
    C, Tk, Nk = P[keep], T[keep], Nn[keep]
    Wk = nrm(np.cross(Tk, Nk))
    wl = edge_wave(s_low, -1, ph)
    wr = edge_wave(s_low, 1, ph)
    TL = C - Wk * HW + Nk * (TP_T / 2 + wl)[:, None]
    TR = C + Wk * HW + Nk * (TP_T / 2 + wr)[:, None]
    BR = C + Wk * HW + Nk * (-TP_T / 2 + wr)[:, None]
    BL = C - Wk * HW + Nk * (-TP_T / 2 + wl)[:, None]
    sp = np.arange(perf_phase, s_low[-1], 0.5)
    extra = np.concatenate([sp - 0.012, sp, sp + 0.012])
    extra = extra[(extra > s_low[0] + 0.01) & (extra < s_low[-1] - 0.01)]
    base_s = si[(si >= s_low[0]) & (si <= s_low[-1])]
    ok = np.ones(len(base_s), bool)
    for e_ in sp:
        ok &= np.abs(base_s - e_) > 0.008
    s_new = np.unique(np.concatenate([base_s[ok], extra, s_low[[0, -1]]]))
    m = len(s_new)
    k = np.clip(np.searchsorted(s_low, s_new, side="right") - 1, 0, len(s_low) - 2)
    t = ((s_new - s_low[k]) / np.maximum(1e-9, s_low[k + 1] - s_low[k]))[:, None]
    lerp = lambda A: A[k] * (1 - t) + A[k + 1] * t
    Ns = nrm(lerp(Nk))
    xs = np.linspace(-HW, HW, 9)
    u = ((xs + HW) / (2 * HW))[None, :, None]
    cr = crumple(np.repeat(s_new, 9), np.tile(xs, m), off).reshape(m, 9)
    cup = 0.010 * (1 - (xs / HW) ** 2)
    dperf = np.zeros(m)
    for e_ in sp:
        dperf -= 0.006 * np.clip(1 - np.abs(s_new - e_) / 0.013, 0, 1)
    det = cr + cup[None, :] + dperf[:, None]
    # smooth (bilinear) between the LO sections: with the strip normal smoothed and the twist per section limited,
    # it stays within ~0.012 of the LO triangles, and no LO facet gets baked into the normal map
    TLs, TRs, BRs, BLs = lerp(TL), lerp(TR), lerp(BR), lerp(BL)
    top = TLs[:, None, :] * (1 - u) + TRs[:, None, :] * u + Ns[:, None, :] * det[:, :, None]
    bot = BLs[:, None, :] * (1 - u) + BRs[:, None, :] * u + Ns[:, None, :] * det[:, :, None]
    V = np.concatenate([top, bot[:, ::-1, :]], 1)      # ring of 18: top L->R, bottom R->L
    kk = 18
    i = np.arange(m - 1)[:, None]
    j = np.arange(kk)[None, :]
    jn = (j + 1) % kk
    a0, b0 = i * kk + j, i * kk + jn
    c0, d0 = (i + 1) * kk + jn, (i + 1) * kk + j
    F = np.concatenate([np.stack([a0, b0, c0], -1).reshape(-1, 3), np.stack([a0, c0, d0], -1).reshape(-1, 3)])
    Vf = V.reshape(-1, 3)
    p0, p1, p2 = Vf[F[0, 0]], Vf[F[0, 1]], Vf[F[0, 2]]
    if np.dot(np.cross(p1 - p0, p2 - p0), Ns[0]) < 0:
        F = F[:, [0, 2, 1]]
    T2 = nrm(lerp(Tk))
    e0 = np.array([[0, j2, j2 + 1] for j2 in range(1, kk - 1)])
    e1 = np.array([[(m - 1) * kk, (m - 1) * kk + j2 + 1, (m - 1) * kk + j2] for j2 in range(1, kk - 1)])
    c_ = np.cross(Vf[e0[0, 1]] - Vf[e0[0, 0]], Vf[e0[0, 2]] - Vf[e0[0, 0]])
    if np.dot(c_, T2[0]) > 0:
        e0 = e0[:, [0, 2, 1]]
        e1 = e1[:, [0, 2, 1]]
    F = np.vstack([F, e0, e1])
    base = L(TP_RGB)
    drift = np.array([noise.noise(Vector((float(sv) * 0.6, 1.7, 3.3)) + Vector(off)) for sv in s_new])
    perf = np.zeros(m)
    for e_ in sp:
        perf += np.clip(1 - np.abs(s_new - e_) / 0.01, 0, 1)
    col_s = base[None, :] * (1 + 0.035 * drift)[:, None] * (1 - 0.08 * perf)[:, None]
    col = np.repeat(col_s, kk, 0)
    crv = np.concatenate([cr, cr[:, ::-1]], 1).reshape(-1)
    col = col * (1 - 0.05 * np.clip(-crv * 60, 0, 1))[:, None]
    rough = np.full(m * kk, 0.86)
    return Vf, F, np.clip(col, 0, 1), rough


# ------------------------------------------------------------------ rolls
def roll_frame(axis):
    a = Vector(axis).normalized()
    e1 = a.cross(Vector((0, 0, 1)))
    e1 = e1.normalized() if e1.length > 1e-4 else Vector((1, 0, 0))
    e2 = a.cross(e1).normalized()
    return a, e1, e2


ROLL = dict(Ro=0.34, Rc=0.15, Ri=0.125, hl=HW)


def orient_roll_faces(V, F, c, a, hl, Ri, UV=None):
    """Flip faces so ends face out along the axis, the wrap faces out radially, the inner tube faces the axis."""
    A_ = np.array(tuple(a))
    cen = np.array(tuple(c))
    p0, p1, p2 = V[F[:, 0]], V[F[:, 1]], V[F[:, 2]]
    fn = np.cross(p1 - p0, p2 - p0)
    m = (p0 + p1 + p2) / 3 - cen
    ax = np.sum(m * A_, 1)
    radial = m - A_[None, :] * ax[:, None]
    rr = np.linalg.norm(radial, axis=1)
    fa = np.abs(np.sum(nrm(fn) * A_[None, :], 1))
    is_end = fa > 0.7
    want = np.where(is_end[:, None], A_[None, :] * np.sign(ax)[:, None], radial / np.maximum(rr, 1e-9)[:, None])
    inner = (~is_end) & (rr < Ri + 0.02)
    want[inner] *= -1
    flip = np.sum(fn * want, 1) < 0
    F = F.copy()
    F[flip] = F[flip][:, [0, 2, 1]]
    if UV is not None:
        UV = UV.reshape(-1, 3, 2).copy()
        UV[flip] = UV[flip][:, [0, 2, 1], :]
        return F, UV.reshape(-1, 2)
    return F


def roll_low(c, axis, rects, nseg=20):
    """Paper wrap + paper end annuli + cardboard core rings + inner tube (a real hole). UVs in the TP atlas."""
    a, e1, e2 = roll_frame(axis)
    c = Vector(c)
    Ro, Rc, Ri, hl = ROLL["Ro"], ROLL["Rc"], ROLL["Ri"], ROLL["hl"]
    ang = [2 * math.pi * j / nseg for j in range(nseg + 1)]
    rad = lambda t: e1 * math.cos(t) + e2 * math.sin(t)
    V, F, UV = [], [], []
    S = rects["size"]

    def strip(r, x0, x1, rect):
        base = len(V)
        for t in ang:
            V.append(c + a * x0 + rad(t) * r)
            V.append(c + a * x1 + rad(t) * r)
        X0, Y0, w, h = rect
        for j in range(nseg):
            q = [base + 2 * j, base + 2 * j + 1, base + 2 * j + 3, base + 2 * j + 2]
            u0, u1 = X0 + w * j / nseg, X0 + w * (j + 1) / nseg
            uv = [(u0, Y0), (u0, Y0 + h), (u1, Y0 + h), (u1, Y0)]
            for t3 in ((0, 1, 2), (0, 2, 3)):
                F.append(tuple(q[z] for z in t3))
                UV.extend([(uv[z][0] / S, uv[z][1] / S) for z in t3])

    def annulus(x, r_out, r_in, rect):
        base = len(V)
        X0, Y0, w, h = rect
        cx, cy = X0 + w / 2, Y0 + h / 2
        sc_ = (w / 2 - 1) / Ro
        for t in ang:
            V.append(c + a * x + rad(t) * r_out)
            V.append(c + a * x + rad(t) * r_in)
        for j in range(nseg):
            q = [base + 2 * j, base + 2 * j + 1, base + 2 * j + 3, base + 2 * j + 2]
            rr_ = [r_out, r_in, r_in, r_out]
            tt = [ang[j], ang[j], ang[j + 1], ang[j + 1]]
            uv = [((cx + math.cos(tt[z]) * rr_[z] * sc_) / S, (cy + math.sin(tt[z]) * rr_[z] * sc_) / S) for z in range(4)]
            for t3 in ((0, 1, 2), (0, 2, 3)):
                F.append(tuple(q[z] for z in t3))
                UV.extend([uv[z] for z in t3])
    strip(Ro, -hl, hl, rects["outer"])
    annulus(hl, Ro, Rc, rects["endA"])
    annulus(hl, Rc, Ri, rects["endA"])
    annulus(-hl, Ro, Rc, rects["endB"])
    annulus(-hl, Rc, Ri, rects["endB"])
    strip(Ri, -hl, hl, rects["inner"])
    V = np.array([tuple(v) for v in V])
    F = np.array(F, np.int32)
    F, UVo = orient_roll_faces(V, F, c, a, hl, Ri, np.array(UV, np.float32))
    return V, F, UVo


def roll_hi(c, axis, seed, nseg=128):
    """Dense roll: paper layers as fine rings on the ends, a soft crinkle on the wrap, cardboard core with a seam."""
    a, e1, e2 = roll_frame(axis)
    c = Vector(c)
    Ro, Rc, Ri, hl = ROLL["Ro"], ROLL["Rc"], ROLL["Ri"], ROLL["hl"]
    rng = random.Random(seed)
    V, F, C = [], [], []
    paper = L(TP_RGB)
    endc = L((224, 218, 204))
    card = L((176, 132, 88))
    cardin = L((132, 96, 62))

    def P(x, r, t):
        return c + a * x + (e1 * math.cos(t) + e2 * math.sin(t)) * r

    def grid(rows, fn):
        base = len(V)
        nr = len(rows)
        for (x, r, colr) in rows:
            for j in range(nseg):
                t = 2 * math.pi * j / nseg
                p, cc = fn(x, r, t, colr)
                V.append(p)
                C.append(cc)
        for i in range(nr - 1):
            for j in range(nseg):
                jn = (j + 1) % nseg
                a0, b0 = base + i * nseg + j, base + i * nseg + jn
                c0, d0 = base + (i + 1) * nseg + jn, base + (i + 1) * nseg + j
                F.append((a0, b0, c0))
                F.append((a0, c0, d0))
    rows = [(-hl + 2 * hl * i / 24, Ro, paper) for i in range(25)]
    grid(rows, lambda x, r, t, cc: (P(x, r * (1 + 0.012 * noise.noise(Vector((x * 9, math.cos(t) * 3,
                                                                                 math.sin(t) * 3)))), t), cc))
    for sgn in (1, -1):
        rows = []
        nring = 30
        for i in range(nring + 1):
            r = Ro - (Ro - Rc) * i / nring
            wv = math.cos(2 * math.pi * i / 2.0)
            rows.append((sgn * (hl - 0.004 * (0.5 + 0.5 * wv)), r,
                         endc * (0.95 + 0.05 * wv + 0.02 * rng.uniform(-1, 1))))
        for i in range(1, 5):
            rows.append((sgn * (hl + 0.004), Rc - (Rc - Ri) * i / 4, card))
        grid(rows, lambda x, r, t, cc: (P(x, r, t), cc))
    rows = [(-hl + 2 * hl * i / 8, Ri, cardin) for i in range(9)]
    grid(rows, lambda x, r, t, cc: (P(x, r, t), cc * (0.8 if abs(((t + x * 9) % 1.2) - 0.6) < 0.03 else 1.0)))
    V = np.array([tuple(v) for v in V])
    F = orient_roll_faces(V, np.array(F, np.int32), c, a, hl, Ri)
    C = np.array([tuple(cc) for cc in C])
    return V, F, C


def roll_rects(atlas, count):
    """Allocate the roll UV rectangles below the ribbon rows (px)."""
    k, m = atlas.k, atlas.m
    ro = ROLL["Ro"]
    y = atlas.row_y(atlas.used_rows()) + m
    x = m
    rows_h = 2 * ro * k + m + 2

    def take(w, h):
        nonlocal x, y
        if x + w > atlas.size - m:
            x = m
            y += rows_h
        r = (x, y, w, h)
        x += w + m + 2
        return r
    out = []
    for _ in range(count):
        d = {"outer": take(2 * math.pi * ro * k, 2 * HW * k), "endA": take(2 * ro * k, 2 * ro * k),
             "endB": take(2 * ro * k, 2 * ro * k), "inner": take(2 * math.pi * ROLL["Ri"] * k, 2 * HW * k),
             "size": atlas.size}
        out.append(d)
    return out, y + rows_h


# ================================================================== TP assembly
def build_tp(specs, rolls, ctx, size, seed, ds=0.1):
    """Simulate every ribbon in order (each one collides with the ones before), build the LO TP (one atlas) and
    the HI bake source. rolls: [(centre, axis)]."""
    col = ctx["col"]
    rng = random.Random(seed)
    done = []
    prev = []
    for k, spec in enumerate(specs):
        X0, rest, pins, off, node_idx = init_ribbon(spec, ctx, ds)
        X = simulate(X0, rest, pins, col, steps=spec.get("steps", 300))
        X = laplace(X, pins, 2)
        T, N, contact = ribbon_frames(X, col, spec, ds)
        if spec.get("sway", 1.0) > 0:
            X = sway_tails(X, contact, pins, seed + k, amp=0.08 * spec.get("sway", 1.0),
                           grow=0.045 * spec.get("sway", 1.0))
            for i in range(len(X)):
                q, c = col.push(Vector(X[i].tolist()))
                X[i] = (q.x, q.y, q.z)
            X = laplace(X, pins, 1)
            T, N, contact = ribbon_frames(X, col, spec, ds)
        N = smooth_normals(T, N, 2.0)
        P, Tt, Nn, si = dense_curve(X, N)
        lifted = 0.0
        if prev:
            P, lifted = lift_off(P, Tt, Nn, prev)
        keep = pick_low(P, Tt, Nn, si)
        ph = (rng.uniform(0, 6.28), rng.uniform(0, 6.28))
        V, F, _ = ribbon_low(P, Tt, Nn, si, keep, ph, None)
        b = bvh_np(V, F)
        col.add(b, 0.08, "ribbon")
        prev.append(b)
        done.append(dict(name=spec["name"], P=P, T=Tt, N=Nn, si=si, keep=keep, ph=ph,
                         off=(rng.uniform(-90, 90), rng.uniform(-90, 90), rng.uniform(-90, 90)),
                         perf=rng.uniform(0.05, 0.5), contact=float(contact.mean()), X=X))
        log("  ribbon %-10s len %5.2f  low sections %4d  contact %.2f  zmin %.2f  lift %.3f" %
            (spec["name"], si[-1], len(keep), contact.mean(), P[:, 2].min(), lifted))
    total = sum(d["si"][-1] for d in done)
    # texel density: the largest k (px per stud) that fits every strip + the roll rectangles
    k = 96
    while k > 24:
        at = Atlas(size, k)
        for d in done:
            at.strip(d["si"][d["keep"]])
        _r, ybot = roll_rects(at, len(rolls))
        if ybot <= size - 2:
            break
        k -= 2
    atlas = Atlas(size, k)
    hmat = mat_vc("TPHiMat")
    los, his = [], []

    def lo_obj(name, V, F, UV):
        o = mesh_np(name, V, F)
        uvl = o.data.uv_layers.new(name="UVMap")
        uvl.data.foreach_set("uv", UV.astype(np.float32).ravel())
        return o

    def hi_obj(name, V, F, Cc, Rr):
        o = mesh_np(name, V, F)
        set_colors(o.data, "Col", Cc)
        set_colors(o.data, "Rough", np.stack([Rr, Rr, Rr], 1))
        o.data.materials.append(hmat)
        return o
    for j, d in enumerate(done):
        V, F, UV = ribbon_low(d["P"], d["T"], d["N"], d["si"], d["keep"], d["ph"], atlas)
        los.append(lo_obj("TPlo_%02d" % j, V, F, UV))
        V, F, Cc, Rr = ribbon_hi(d["P"], d["T"], d["N"], d["si"], d["keep"], d["ph"], d["off"], d["perf"])
        his.append(hi_obj("TPHi_%02d" % j, V, F, Cc, Rr))
    rects, ybot = roll_rects(atlas, len(rolls))
    for j, ((c, axis), rc) in enumerate(zip(rolls, rects)):
        V, F, UV = roll_low(c, axis, rc)
        los.append(lo_obj("TPlo_r%d" % j, V, F, UV))
        V, F, Cc = roll_hi(c, axis, seed + 100 + j)
        his.append(hi_obj("TPHi_r%d" % j, V, F, Cc, np.full(len(V), 0.84)))
    rep = dict(ribbons=len(done), length=round(total, 1), px_per_stud=k, tris=sum(tri_count(o) for o in los),
               hi_tris=sum(tri_count(o) for o in his), atlas_rows=atlas.used_rows(), atlas_bottom_px=int(ybot))
    return los, his, done, rep


def lift_off(P, T, Nn, prev, gap=0.035, iters=4):
    """Push a new strip off the strips already placed: probe its centre and both edges against their LO meshes and
    move it along their surface normal where it is closer than half-thickness + gap; the push is a smooth bump
    along the strip (running max, then a gaussian)."""
    W = nrm(np.cross(T, Nn))
    P = P.copy()
    m = len(P)
    total = 0.0
    ker = np.exp(-0.5 * (np.arange(-21, 22) / 7.0) ** 2)
    ker /= ker.sum()
    for _ in range(iters):
        push = np.zeros((m, 3))
        mag = np.zeros(m)
        for i in range(0, m, 2):
            for off in (-HW * 0.97, -HW * 0.5, 0.0, HW * 0.5, HW * 0.97):
                q = Vector((P[i] + W[i] * off).tolist())
                for b in prev:
                    loc, nr, idx, dist = b.find_nearest(q, 0.3)
                    if loc is None:
                        continue
                    need = TP_T / 2 + gap - (q - loc).dot(nr)
                    if need > mag[i]:
                        mag[i] = need
                        push[i] = (nr.x, nr.y, nr.z)
        if mag.max() <= 1e-4:
            break
        pad = np.pad(mag, 12)
        mx = np.lib.stride_tricks.sliding_window_view(pad, 25).max(1)
        mx = np.convolve(mx, ker, mode="same")
        dv = np.stack([np.convolve(push[:, c] * mag, ker, mode="same") for c in range(3)], 1)
        dv = nrm(dv + 1e-12)
        P = P + dv * mx[:, None] * 1.05
        total += float(mag.max())
    return P, total


def wedge_roll(la, lb, ro):
    """A roll wedged in the fork between two limbs: centre where the gap between the limb surfaces = 2 Ro."""
    for f in np.linspace(0.04, 0.8, 120):
        pa, ra, ia = point_on(la, f)
        pb, rb, ib = point_on(lb, f)
        if (pa - pb).length - ra - rb >= 2 * ro * 0.9:
            break
    ta = Vector((la["P"][min(ia + 1, len(la["P"]) - 1)] - la["P"][max(ia - 1, 0)]).tolist()).normalized()
    tb = Vector((lb["P"][min(ib + 1, len(lb["P"]) - 1)] - lb["P"][max(ib - 1, 0)]).tolist()).normalized()
    axis = ta.cross(tb).normalized()
    axis = Vector((axis.x, axis.y, axis.z * 0.45)).normalized()
    c = (pa + pb) * 0.5 - Vector((0, 0, 0.05))
    return c, axis


def roll_departure(c, axis, out_hint):
    """Where the paper leaves the roll and hangs straight down: the side point whose tangent is vertical."""
    e = Vector(out_hint)
    e.z = 0.0
    e = e - Vector(axis) * e.dot(Vector(axis))
    e.normalize()
    return c + e * (ROLL["Ro"] + 0.03), e


# ================================================================== the TREE
TREE_BLEND_WIP = os.path.join(WIP, "tree_wip.blend")
TREE_BLEND = os.path.join(OUT, "tptree.blend")
TREE_CENTRE = (0.0, 0.0, 10.0)


def tree_specs(rollA, rollB):
    (pa, ea), (pb, eb) = rollA, rollB
    D = lambda az, el: ("dir", az, el)
    return [
        dict(name="OverA", nodes=[D(-15, -4), D(-15, 40), D(-15, 84), D(165, 40), D(165, -6)],
             spans=["drape"] * 4, pins=[False, True, True, True, False], tail0=4.4, tail1=5.0, twist=0.14),
        dict(name="OverB", nodes=[D(72, -2), D(72, 45), D(72, 80), D(252, 45), D(252, -8)],
             spans=["drape"] * 4, pins=[False, True, True, True, False], tail0=3.4, tail1=5.6, twist=0.17),
        dict(name="OverC", nodes=[D(205, 2), D(215, 52), D(320, 58), D(318, 4)],
             spans=["drape"] * 3, pins=[False, True, True, False], tail0=3.0, tail1=3.6, twist=0.15),
        dict(name="FestFront", nodes=[D(262, -13), D(296, -12)], spans=["sag:1.2"], pins=[True, True],
             tail0=0.5, tail1=1.6, twist=0.12),
        dict(name="FestRight", nodes=[D(22, -16), D(56, -12)], spans=["sag:1.18"], pins=[True, True],
             tail0=0.9, tail1=2.4, twist=0.12),
        dict(name="FestBack", nodes=[D(136, -10), D(190, -15)], spans=["sag:1.18"], pins=[True, True],
             tail0=2.2, tail1=0.8, twist=0.12),
        dict(name="LimbLoopA", nodes=[("limb", 2, 0.5), ("limb", 3, 0.48)], spans=["sag:1.22"], pins=[True, True],
             tail0=2.0, tail1=2.8, twist=0.1),
        dict(name="LimbLoopB", nodes=[("limb", 0, 0.55), ("limb", 1, 0.5)], spans=["sag:1.2"], pins=[True, True],
             tail0=2.4, tail1=1.5, twist=0.1),
        dict(name="TwigA", nodes=[("twig", 0, 0.9)], spans=[], pins=[True], tail0=0.55, tail1=3.1, twist=0.2),
        dict(name="TwigB", nodes=[("twig", 1, 0.9)], spans=[], pins=[True], tail0=3.0, tail1=0.6, twist=0.18),
        dict(name="TwigC", nodes=[("twig", 2, 0.9)], spans=[], pins=[True], tail0=0.5, tail1=3.4, twist=0.2),
        dict(name="RollA", nodes=[("pt", tuple(pa), tuple(ea))], spans=[], pins=[True], tail1=4.6, dir1=(0, 0, -1),
             start_pin=True, start_normal=tuple(ea), twist=0.2),
        dict(name="RollB", nodes=[("pt", tuple(pb), tuple(eb))], spans=[], pins=[True], tail1=4.2, dir1=(0, 0, -1),
             start_pin=True, start_normal=tuple(eb), twist=0.18),
    ]


def canopy_parts(name, blobs, voxel, smooth_iter, namp, nfreq, seed, lo_tris, lo_push, zfloor=None):
    base = blob_mesh(name + "Base", blobs, voxel, smooth_iter, namp, nfreq, seed, zfloor)
    src = link(bpy.data.objects.new("LoSrc", base.data.copy()))
    V, T, N = obj_arrays(src)
    V = V + N * lo_push
    if zfloor is not None:
        V[:, 2] = np.maximum(V[:, 2], zfloor)
    set_co(src, V)
    lo = decimate_to(src, name, lo_tris)
    bpy.data.objects.remove(src)
    return base, lo


def mesh_area(ob):
    V, T, N = obj_arrays(ob)
    A, B, C = V[T[:, 0]], V[T[:, 1]], V[T[:, 2]]
    return float(0.5 * np.linalg.norm(np.cross(B - A, C - A), axis=1).sum())


def setup_scene():
    sc = fresh(samples=16)
    sc.render.threads_mode = "FIXED"
    sc.render.threads = 6
    return sc


def build_tree():
    setup_scene()
    q = CFG["quick"]
    rep = {}
    clumps, blobs = tree_clumps(21)
    base, canopy = canopy_parts("Canopy", blobs, 0.09 if q else 0.06, 8, 0.14, 0.7, 5, 14600, 0.07)
    area = mesh_area(base)
    nleaf = int(area * (6 if q else 25))
    log("canopy base", len(base.data.polygons), "area", round(area, 1), "leaves", nleaf)
    leaves, _p, _n = scatter_leaves("LeavesHi", base, nleaf,
                                    dict(L=(0.42, 0.62), wk=(0.48, 0.6), tilt=(0.16, 0.48), sink=0.03,
                                         fold=(0.15, 0.35), curl=(-0.05, 0.12), centre=TREE_CENTRE),
                                    tree_leaf_colours(clumps), 77)
    leaves.data.materials.append(mat_vc("LeafHi"))
    nv = len(base.data.vertices)
    set_colors(base.data, "Col", np.tile(L((62, 22, 12)), (nv, 1)))
    set_colors(base.data, "Rough", np.full((nv, 3), 0.9))
    base.data.materials.append(mat_vc("CanopyGapHi"))
    base.name = "CanopyHi"
    log("leaves", tri_count(leaves))
    br, limbs, twigs, lead = tree_skeleton(clumps, 3)
    trunk_hi, trunk, sk = build_trunk(br, base, 0.045 if q else 0.032, 7200, 9)
    log("trunk hi", tri_count(trunk_hi), "lo", tri_count(trunk))
    col = Colliders(0.035)
    col.add(bvh_ob(canopy), 0.085, "canopy")
    col.add(bvh_ob(trunk), 0.07, "trunk")
    ctx = dict(col=col, centre=TREE_CENTRE, limbs=limbs, twigs=twigs)
    cA, axA = wedge_roll(limbs[3], limbs[4], ROLL["Ro"])
    pA, eA = roll_departure(cA, axA, Vector((cA.x, cA.y, 0)) + Vector((0, -0.3, 0)))
    pS, nS = surf_dir(col, TREE_CENTRE, 118, 6)
    cB = pS - nS * 0.105 + nS * (ROLL["Ro"] * 0.5)
    axB = nS.cross(Vector((0, 0, 1))).normalized()
    axB = (Matrix.Rotation(math.radians(22), 3, nS) @ axB).normalized()
    pB, eB = roll_departure(cB, axB, nS)
    # roll clearance vs the skeleton (other branches)
    skd = []
    for b in br:
        d = np.linalg.norm(b["P"] - np.array(tuple(cA)), axis=1) - b["R"]
        skd.append(float(d.min()))
    rep["rollA"] = dict(centre=[round(v, 3) for v in cA], axis=[round(v, 3) for v in axA],
                        min_branch_clear=round(sorted(skd)[2], 3))
    rep["rollB"] = dict(centre=[round(v, 3) for v in cB], axis=[round(v, 3) for v in axB])
    specs = tree_specs((pA, eA), (pB, eB))
    tp_los, tp_his, done, trep = build_tp(specs, [(cA, axA), (cB, axB)], ctx, 1024, 4242)
    rep["tp"] = trep
    log("TP", trep)
    # two canopy MeshParts (x >= 0 / x < 0), one 1024 map each -> ~2x the leaf texel density
    Vw, _Tw, Nw = obj_arrays(canopy)
    halves = split_faces(canopy, {"CanopyA": lambda f: f.calc_center_median().x >= 0.0, "CanopyB": lambda f: True})
    canA, canB = halves["CanopyA"], halves["CanopyB"]
    from mathutils.kdtree import KDTree
    kd = KDTree(len(Vw))
    for i, v in enumerate(Vw):
        kd.insert(Vector(v.tolist()), i)
    kd.balance()
    for o in (canA, canB):
        o.data.shade_smooth()
        Vh, _t, _n = obj_arrays(o)
        # the normals of the unsplit canopy on both halves: no shading crease along the split
        o.data.normals_split_custom_set_from_vertices([tuple(Nw[kd.find(Vector(v.tolist()))[1]]) for v in Vh])
        smart_uv(o)
    smart_uv(trunk)
    rep["tris"] = {o.name: tri_count(o) for o in (trunk, canA, canB)}
    rep["tris"]["TP"] = trep["tris"]
    rep["hi_tris"] = {o.name: tri_count(o) for o in (trunk_hi, base, leaves)}
    rep["hi_tris"]["TPHi"] = trep["hi_tris"]
    rep["bbox"] = bbox_of([trunk, canA, canB] + tp_los)
    save_json(rep, os.path.join(WIP, "tree_build.json"))
    for o in [trunk_hi, base, leaves] + tp_his:
        o.hide_render = True
    bpy.ops.wm.save_as_mainfile(filepath=TREE_BLEND_WIP)
    return rep


def bbox_of(objs):
    V = np.vstack([obj_arrays(o)[0] for o in objs])
    mn, mx = V.min(0), V.max(0)
    return dict(min=[round(float(v), 3) for v in mn], max=[round(float(v), 3) for v in mx],
                size_blender=[round(float(v), 3) for v in (mx - mn)],
                size_roblox_XYZ=[round(float(mx[0] - mn[0]), 2), round(float(mx[2] - mn[2]), 2),
                                 round(float(mx[1] - mn[1]), 2)])


def save_json(d, path):
    with open(path, "w") as f:
        json.dump(d, f, indent=1)


# ================================================================== the BUSH
BUSH_BLEND_WIP = os.path.join(WIP, "bush_wip.blend")
BUSH_BLEND = os.path.join(OUT, "tpbush.blend")
BUSH_CENTRE = (0.0, 0.0, 1.8)


def bush_specs(roll_top):
    D = lambda az, el: ("dir", az, el)
    return [
        dict(name="BOverA", nodes=[D(20, 0), D(20, 62), D(200, 62), D(200, 0)], spans=["drape"] * 3,
             pins=[False, True, True, False], tail0=1.6, tail1=2.8, twist=0.16),
        dict(name="BRoll", nodes=[("pt", tuple(roll_top), (0, 0, 1)), D(-86, 26), D(-80, 74), D(100, 38)],
             spans=["sag:1.03", "drape", "drape"], pins=[True, False, True, False], tail1=2.0, twist=0.16),
        dict(name="BOverB", nodes=[D(150, 4), D(196, 52), D(322, 46), D(8, 2)], spans=["drape"] * 3,
             pins=[False, True, True, False], tail0=1.5, tail1=2.1, twist=0.15),
    ]


def build_bush():
    setup_scene()
    q = CFG["quick"]
    rep = {}
    clumps, blobs = bush_clumps(31)
    base, canopy = canopy_parts("Canopy", blobs, 0.06 if q else 0.04, 8, 0.07, 1.3, 8, 7600, 0.05, zfloor=-0.05)
    area = mesh_area(base)
    nleaf = int(area * (10 if q else 42))
    log("bush base", len(base.data.polygons), "area", round(area, 1), "leaves", nleaf)
    leaves, _p, _n = scatter_leaves("LeavesHi", base, nleaf,
                                    dict(L=(0.3, 0.42), wk=(0.5, 0.62), tilt=(0.16, 0.48), sink=0.02,
                                         fold=(0.15, 0.35), curl=(-0.04, 0.1), centre=BUSH_CENTRE),
                                    bush_leaf_colours(clumps, (0, 0, 1.6), 3.0, 4.8), 91)
    leaves.data.materials.append(mat_vc("LeafHi"))
    nv = len(base.data.vertices)
    set_colors(base.data, "Col", np.tile(L((22, 34, 14)), (nv, 1)))
    set_colors(base.data, "Rough", np.full((nv, 3), 0.9))
    base.data.materials.append(mat_vc("CanopyGapHi"))
    base.name = "CanopyHi"
    col = Colliders(0.035)
    col.add(bvh_ob(canopy), 0.075, "canopy")
    # the roll on the ground at the front, tucked under the bulge, axis along the bush outline
    cb = bvh_ob(canopy)
    ang = math.radians(-82)
    rdir = Vector((math.cos(ang), math.sin(ang), 0))
    rad = 1.6
    while rad < 3.5:
        c = rdir * rad + Vector((0, 0, ROLL["Ro"] + 0.005))
        loc, nr, idx, dist = cb.find_nearest(c, 5.0)
        inside = (c - loc).dot(nr) < 0
        if not inside and dist > ROLL["Ro"] + 0.04:
            break
        rad += 0.02
    axis = Vector((-rdir.y, rdir.x, 0)).normalized()
    axis = (Matrix.Rotation(math.radians(-14), 3, "Z") @ axis).normalized()
    roll_top = c + Vector((0, 0, ROLL["Ro"] + 0.04))
    rep["roll"] = dict(centre=[round(v, 3) for v in c], axis=[round(v, 3) for v in axis], radius_from_axis=round(rad, 3))
    ctx = dict(col=col, centre=BUSH_CENTRE, limbs=[], twigs=[])
    tp_los, tp_his, done, trep = build_tp(bush_specs(roll_top), [(c, axis)], ctx, 512, 5151)
    rep["tp"] = trep
    log("TP", trep)
    smart_uv(canopy)
    rep["tris"] = {"Canopy": tri_count(canopy), "TP": trep["tris"]}
    rep["hi_tris"] = {o.name: tri_count(o) for o in (base, leaves)}
    rep["hi_tris"]["TPHi"] = trep["hi_tris"]
    rep["bbox"] = bbox_of([canopy] + tp_los)
    save_json(rep, os.path.join(WIP, "bush_build.json"))
    for o in [base, leaves] + tp_his:
        o.hide_render = True
    bpy.ops.wm.save_as_mainfile(filepath=BUSH_BLEND_WIP)
    return rep


# ================================================================== bakes
def downsample(img, name, size, kind, outdir):
    big = img.size[0]
    f = big // size
    a = np.empty(big * big * 4, np.float32)
    img.pixels.foreach_get(a)
    b = a.reshape(size, f, size, f, 4).mean((1, 3))
    if kind == "normal":
        v = b[..., :3] * 2 - 1
        v /= np.maximum(1e-6, np.linalg.norm(v, axis=-1, keepdims=True))
        b[..., :3] = v * 0.5 + 0.5
    b[..., 3] = 1.0
    out = bpy.data.images.new(name, size, size, alpha=False)
    out.colorspace_settings.name = img.colorspace_settings.name
    out.pixels.foreach_set(b.ravel())
    save_png(out, os.path.join(outdir, name + ".png"))
    return out


def bake_part(lo, his, occluders, size, prefix, cage, maxray, ao_strength, ao_dist, ss=2):
    """bake_set at ss x the size (only the hi parts + the named LO occluders render; this LO is invisible to rays),
    then box-filtered down to `size`: anti-aliased leaf / fold edges."""
    sc = bpy.context.scene
    keep = {}
    for o in sc.objects:
        if o.type != "MESH":
            continue
        keep[o.name] = (o.hide_render, o.visible_diffuse, o.visible_shadow, o.visible_glossy, o.visible_transmission)
        if o in his or o in occluders:
            o.hide_render = False
            vis = True
        elif o == lo:
            o.hide_render = False
            vis = False
        else:
            o.hide_render = True
            vis = True
        o.visible_diffuse = o.visible_shadow = o.visible_glossy = o.visible_transmission = vis
    t = time.time()
    big = bake_set(lo, his, size * ss, prefix + "_ss", cage, maxray, ao_strength, ao_dist, outdir=WIP)
    for o in sc.objects:
        if o.name in keep:
            (o.hide_render, o.visible_diffuse, o.visible_shadow, o.visible_glossy, o.visible_transmission) = keep[o.name]
    imgs = {k: downsample(big[k], prefix + "_" + k, size, k, MAPS) for k in ("albedo", "normal", "rough", "ao")}
    for k in ("albedo", "normal", "rough", "ao"):
        bpy.data.images.remove(big[k])
    imgs["miss_fraction"] = big["miss_fraction"]
    log("  baked %s %dpx (x%d) in %.0fs, ray miss %.4f" % (prefix, size, ss, time.time() - t, imgs["miss_fraction"]))
    return imgs


def bake_groups_ss(groups, occluders, size, prefix, ao_strength, ao_dist, ss=2):
    """(Adapted from the PumpkinEggs builder's bake_groups.) groups: [(lo, [his], cage, maxray)], the lo parts share
    one UV atlas. Each lo only matches rays against ITS OWN hi parts (a strip can never pick up a neighbouring strip
    that crosses it). Coverage of each lo + its hit mask (EMIT) are baked with margin 0; covered texels that missed
    are grown from that group's hits; the empty space is dilated at the end. AO sees every hi part plus the
    `occluders` (LO meshes); the lo parts are invisible to rays. Baked at ss x size, box-filtered down."""
    sc = bpy.context.scene
    sc.world.light_settings.distance = ao_dist
    big = size * ss
    shp = (big, big, 4)
    acc = {k: np.zeros(shp, np.float32) for k in ("albedo", "normal", "rough", "ao")}
    owned = np.zeros((big, big), bool)
    zero = np.zeros(big * big * 4, np.float32)
    t_lin = bpy.data.images.new(prefix + "_tmpL", big, big, alpha=False)
    t_lin.colorspace_settings.name = "Non-Color"
    t_rgb = bpy.data.images.new(prefix + "_tmpC", big, big, alpha=False)
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
    nt.links.new(em.outputs["Emission"], nt.nodes["Material Output"].inputs["Surface"])
    ctex = nt.nodes.new("ShaderNodeTexImage")
    ctex.image = t_lin
    nt.nodes.active = ctex
    los = [g[0] for g in groups]
    his_all = [h for g in groups for h in g[1]]
    keep = {}
    for o in sc.objects:
        if o.type != "MESH":
            continue
        keep[o.name] = (o.hide_render, o.visible_diffuse, o.visible_shadow, o.visible_glossy, o.visible_transmission)
        if o in los:
            o.hide_render, vis = False, False
        elif o in his_all or o in occluders:
            o.hide_render, vis = False, True
        else:
            o.hide_render, vis = True, True
        o.visible_diffuse = o.visible_shadow = o.visible_glossy = o.visible_transmission = vis

    def bake(node, img, kind, s2a, cage=0.0, maxray=0.0, **kw):
        node.image = img
        img.pixels.foreach_set(zero)
        bpy.ops.object.bake(type=kind, use_selected_to_active=s2a, cage_extrusion=cage, max_ray_distance=maxray,
                            margin=0, use_clear=False, **kw)
        a = np.empty(big * big * 4, np.float32)
        img.pixels.foreach_get(a)
        return a.reshape(shp)

    def emit_white(hs, saved):
        for h in hs:
            for m in h.data.materials:
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

    def restore(saved):
        for m, n, colr, st, ls in saved:
            n.inputs["Emission Color"].default_value = colr
            n.inputs["Emission Strength"].default_value = st
            for a, b in ls:
                m.node_tree.links.new(a, b)
    t0 = time.time()
    miss_tot, cov_tot = 0, 0
    for lo, hs, cage, maxray in groups:
        for o in sc.objects:
            o.select_set(False)
        lo.select_set(True)
        bpy.context.view_layer.objects.active = lo
        lo.data.materials.clear()
        lo.data.materials.append(cmat)
        cov = bake(ctex, t_lin, "EMIT", False)[..., 0] > 0.5
        lo.data.materials.clear()
        lo.data.materials.append(bmat)
        for h in hs:
            h.select_set(True)
        out = {"normal": bake(tex, t_lin, "NORMAL", True, cage, maxray, normal_space="TANGENT"),
               "ao": bake(tex, t_lin, "AO", True, cage, maxray),
               "albedo": bake(tex, t_rgb, "DIFFUSE", True, cage, maxray, pass_filter={"COLOR"}),
               "rough": bake(tex, t_lin, "ROUGHNESS", True, cage, maxray)}
        saved = []
        emit_white(hs, saved)
        hit = bake(tex, t_lin, "EMIT", True, cage, maxray)[..., 0] > 0.5
        restore(saved)
        hit &= cov
        # a strip folded tight round a twig / a crossing can still send a ray to a wrong face: a baked tangent normal
        # tilted > ~70 deg is never paper detail -> treat as a miss (refilled from the good neighbours)
        hit &= out["normal"][..., 2] > 0.67
        for k2, arr in out.items():
            if k2 == "normal":
                arr = arr.copy()
                arr[~hit] = (0.5, 0.5, 1.0, 1.0)
            filled = fill_misses(arr, hit, iters=6) if k2 != "normal" else arr
            acc[k2][cov] = filled[cov]
        owned |= cov
        miss_tot += int((cov & ~hit).sum())
        cov_tot += int(cov.sum())
    for o in sc.objects:
        if o.name in keep:
            (o.hide_render, o.visible_diffuse, o.visible_shadow, o.visible_glossy, o.visible_transmission) = keep[o.name]
    for k2 in acc:
        if k2 == "normal":
            acc[k2][~owned] = (0.5, 0.5, 1.0, 1.0)
            acc[k2] = fill_misses(acc[k2], owned, iters=16)
        else:
            acc[k2] = fill_misses(acc[k2], owned, iters=16)
    acc["albedo"][..., :3] *= (1 - ao_strength) + ao_strength * acc["ao"][..., :1]
    imgs = {}
    for k2, cs in (("albedo", "sRGB"), ("normal", "Non-Color"), ("rough", "Non-Color"), ("ao", "Non-Color")):
        acc[k2][..., 3] = 1.0
        img = bpy.data.images.new(prefix + "_" + k2 + "_ss", big, big, alpha=False)
        img.colorspace_settings.name = cs
        img.pixels.foreach_set(acc[k2].ravel())
        imgs[k2] = downsample(img, prefix + "_" + k2, size, k2, MAPS)
        bpy.data.images.remove(img)
    for i in (t_lin, t_rgb):
        bpy.data.images.remove(i)
    imgs["miss_fraction"] = miss_tot / max(1, cov_tot)
    log("  baked %s %dpx (x%d, %d groups) in %.0fs, covered-texel miss %.4f" %
        (prefix, size, ss, len(groups), time.time() - t0, imgs["miss_fraction"]))
    return imgs


def join_parts(names, into):
    objs = [bpy.data.objects[n] for n in names]
    for o in bpy.context.scene.objects:
        o.select_set(o in objs)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.join()
    ob = bpy.context.view_layer.objects.active
    ob.name = into
    ob.data.name = into
    return ob


TREE_BAKES = [  # lo, his, occluder los, size, prefix, cage, maxray, ao strength, ao distance
    ("Trunk", ["TrunkHi"], ["CanopyA", "CanopyB"], 1024, "TPTree_Trunk", 0.12, 0.32, 0.6, 1.2),
    ("CanopyA", ["CanopyHi", "LeavesHi"], ["Trunk", "CanopyB"], 1024, "TPTree_CanopyA", 0.3, 0.62, 0.7, 0.9),
    ("CanopyB", ["CanopyHi", "LeavesHi"], ["Trunk", "CanopyA"], 1024, "TPTree_CanopyB", 0.3, 0.62, 0.7, 0.9),
    ("TP", None, ["CanopyA", "CanopyB", "Trunk"], 1024, "TPTree_TP", 0.045, 0.07, 0.5, 0.45),
]
BUSH_BAKES = [
    ("Canopy", ["CanopyHi", "LeavesHi"], [], 1024, "TPBush_Canopy", 0.2, 0.5, 0.7, 0.7),
    ("TP", None, ["Canopy"], 512, "TPBush_TP", 0.045, 0.07, 0.5, 0.45),
]


def bake_asset(which):
    wip, final, plan = (TREE_BLEND_WIP, TREE_BLEND, TREE_BAKES) if which == "tree" else \
        (BUSH_BLEND_WIP, BUSH_BLEND, BUSH_BAKES)
    bpy.ops.wm.open_mainfile(filepath=wip)
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = 16
    sc.render.threads_mode = "FIXED"
    sc.render.threads = 6
    ob = bpy.data.objects
    rep = {}
    for lo, his, occ, size, prefix, cage, maxray, aos, aod in plan:
        if lo == "TP":
            los = sorted(o.name for o in ob if o.name.startswith("TPlo_"))
            groups = [(ob[n], [ob[n.replace("TPlo_", "TPHi_")]], cage, maxray) for n in los]
            imgs = bake_groups_ss(groups, [ob[o] for o in occ], size, prefix, aos, aod)
            tp = join_parts(los, "TP")
            pbr_material(tp, "TP_PBR", imgs)
        else:
            imgs = bake_part(ob[lo], [ob[h] for h in his], [ob[o] for o in occ], size, prefix, cage, maxray, aos,
                             aod)
            pbr_material(ob[lo], lo + "_PBR", imgs)
        rep[lo] = dict(size=size, miss=round(imgs["miss_fraction"], 4))
    for o in ob:
        if o.name.endswith("Hi") or o.name.startswith("TPHi_"):
            o.hide_render = True
            o.hide_viewport = True
    bpy.ops.wm.save_as_mainfile(filepath=final)
    return rep


# ================================================================== review renders + export
def review_ground(soil_r):
    bpy.ops.mesh.primitive_plane_add(size=600, location=(0, 0, 0))
    g = bpy.context.active_object
    g.data.materials.append(mat_noise("Grass", lin((62, 132, 44)), lin((92, 162, 60)), nscale=0.08, detail=4,
                                      rough=0.95))
    bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=soil_r, depth=0.2, location=(0, 0, -0.08))
    s = bpy.context.active_object
    s.data.materials.append(mat_noise("Soil", lin((78, 54, 36)), lin((112, 80, 52)), nscale=1.2, detail=6,
                                      rough=0.95))


def render_asset(which, hi=False):
    final = TREE_BLEND if which == "tree" else BUSH_BLEND
    if hi:
        final = TREE_BLEND_WIP if which == "tree" else BUSH_BLEND_WIP
    bpy.ops.wm.open_mainfile(filepath=final)
    sc = review_setup()
    sc.eevee.taa_render_samples = 48
    for o in bpy.data.objects:
        if o.type == "MESH":
            ishi = o.name.endswith("Hi") or o.name.startswith("TPHi_")
            o.hide_render = (not ishi) if hi else ishi
    review_ground(7.5 if which == "tree" else 3.6)
    tag = "hi_" if hi else ""
    out = []
    if which == "tree":
        tgt = (0, 0, 7.8)
        out.append(shoot(os.path.join(OUT, "review_%stree_25studs.png" % tag), tgt, (0.55, -1, -0.02), 25, 30))
        out.append(shoot(os.path.join(OUT, "review_%stree_50studs.png" % tag), tgt, (0.55, -1, 0.02), 50, 35))
        out.append(shoot(os.path.join(OUT, "review_%stree_back_40studs.png" % tag), tgt, (-0.7, 1, 0.12), 40, 35))
        out.append(shoot(os.path.join(OUT, "review_%stree_high_40studs.png" % tag), (0, 0, 9), (0.3, -1, 0.75), 40, 35))
        rb = json.load(open(os.path.join(WIP, "tree_build.json")))["rollA"]["centre"]
        out.append(shoot(os.path.join(OUT, "review_%stree_close_fork.png" % tag), (rb[0], rb[1], rb[2] - 0.6),
                         (0.45, -1, 0.05), 7.5, 35))
        out.append(shoot(os.path.join(OUT, "review_%stree_close_canopy.png" % tag), (2.6, -5.0, 9.4),
                         (0.5, -1, 0.15), 7.0, 35))
    else:
        tgt = (0, 0, 2.2)
        out.append(shoot(os.path.join(OUT, "review_%sbush_25studs.png" % tag), tgt, (0.45, -1, 0.12), 25, 50))
        out.append(shoot(os.path.join(OUT, "review_%sbush_50studs.png" % tag), tgt, (0.45, -1, 0.1), 50, 50))
        out.append(shoot(os.path.join(OUT, "review_%sbush_back_25studs.png" % tag), tgt, (-0.6, 1, 0.3), 25, 50))
        rb = json.load(open(os.path.join(WIP, "bush_build.json")))["roll"]["centre"]
        out.append(shoot(os.path.join(OUT, "review_%sbush_close.png" % tag), (rb[0] * 0.6, rb[1] * 0.6, 1.2),
                         (0.35, -1, 0.35), 7.0, 35))
    return out


def export_asset(which):
    final = TREE_BLEND if which == "tree" else BUSH_BLEND
    bpy.ops.wm.open_mainfile(filepath=final)
    names = ("Trunk", "CanopyA", "CanopyB", "TP") if which == "tree" else ("Canopy", "TP")
    objs = [bpy.data.objects[n] for n in names]
    path = os.path.join(CDIMP, "Halloween_TPTree.fbx" if which == "tree" else "Halloween_TPBush.fbx")
    rep = export_fbx(objs, path)
    rep["tris"] = {o.name: tri_count(o) for o in objs}
    rep["bbox"] = bbox_of(objs)
    return rep


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    if argv and argv[0] == "quick":
        CFG["quick"] = True
        argv = argv[1:]
    step, which = argv[0], argv[1]
    if step == "build":
        rep = build_tree() if which == "tree" else build_bush()
    elif step == "bake":
        rep = bake_asset(which)
    elif step == "render":
        rep = render_asset(which)
    elif step == "preview":
        rep = render_asset(which, hi=True)
    elif step == "export":
        rep = export_asset(which)
    log("HW_REPORT " + json.dumps(rep))
