# SLINGSHOT Halloween hub GARDEN - row 4 "Graveyard" (2026-10-12).
#   Grave_A      rounded-top headstone: carved border groove, big serif "RIP", small cross, worn epitaph lines
#   Grave_B      stone cross on a stepped plinth: carved inset border line + a diamond at the crossing, cracked shaft
#   Grave_C      old cracked slab leaning back ~10 deg: broken top corner, a through-crack with a shifted piece,
#                worn carved skull & crossbones + epitaph
#   DeadGrass_A / _B   dry straw / olive grass tufts: real keeled blades (closed, no alpha), a few bent / broken
# Headless:  blender.exe -b --factory-startup --python graveyard.py -- grave A | grave B | grave C | grass A |
#            grass B | review | verify          (add "fast" first for a quick low-density test)
#
# Gravestone pipeline (no booleans at all): the stone = 2D outline(s) extruded along Y -> Bevel (chunky rounded rims)
# -> voxel Remesh (uniform dense quads; also unions the parts of the cross) -> per-vertex displacement in REST space:
# low-freq undulation, Voronoi edge chips, carving (a 2D signed-distance HEIGHTFIELD of the letters / border / cross /
# skull pushed into the front face: real geometry with chamfered walls, nothing can be dropped like an EXACT boolean),
# cracks (V grooves through the slab), pits, moss cushions -> taper / bend / lean. The game mesh is the SAME
# procedural stone at a coarse voxel size with only the low-freq displacement + chips (no carving), decimated.
# Soil mound = a polar heightfield (dense for the bake, coarse for the game). Bakes run per group (stone lo <- stone hi,
# mound lo <- mound hi; the other lo hidden) and are composited by their own hit masks, so a mound texel can never pick
# up the stone and vice versa. The dead-grass blades use a procedural strip atlas painted into a reserved column of the
# same 512 texture (blades are too thin to bake reliably).
import sys, os, json, time
sys.path.insert(0, r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween")
from hkit import *  # noqa: F401,F403
from mathutils import Matrix

OUT = os.path.join(HERE, "Graveyard")
MAPS = os.path.join(OUT, "maps")
WIP = os.path.join(OUT, "wip")
T0 = time.time()
CFG = {"fast": False}
RESERVE_PX = 464          # grave atlas: columns >= 464 px (of 512) hold the grass-blade strips


def log(*a):
    print("[grave %6.1fs]" % (time.time() - T0), *a, flush=True)


def s255(c):
    return np.array(c, dtype=np.float64) / 255.0


def sm(a, b, x):
    """numpy smoothstep (a > b allowed = falling edge)."""
    t = np.clip((x - a) / (b - a), 0.0, 1.0)
    return t * t * (3 - 2 * t)


# ------------------------------------------------------------------ 2D signed distance helpers (x, z face coords)
def sd_seg(px, pz, a, b):
    ax, az = a
    bx, bz = b
    dx, dz = bx - ax, bz - az
    L2 = dx * dx + dz * dz + 1e-12
    t = np.clip(((px - ax) * dx + (pz - az) * dz) / L2, 0.0, 1.0)
    qx = px - (ax + t * dx)
    qz = pz - (az + t * dz)
    return np.sqrt(qx * qx + qz * qz)


def sd_arc(px, pz, c, r, a0, a1):
    """distance to a circular arc from angle a0 to a1 (radians, a0 < a1)."""
    dx, dz = px - c[0], pz - c[1]
    ang = np.arctan2(dz, dx)
    mid = 0.5 * (a0 + a1)
    rel = (ang - mid + math.pi) % (2 * math.pi) - math.pi
    inside = np.abs(rel) <= 0.5 * (a1 - a0)
    d_circ = np.abs(np.sqrt(dx * dx + dz * dz) - r)
    e0 = (c[0] + r * math.cos(a0), c[1] + r * math.sin(a0))
    e1 = (c[0] + r * math.cos(a1), c[1] + r * math.sin(a1))
    d_end = np.minimum(np.hypot(px - e0[0], pz - e0[1]), np.hypot(px - e1[0], pz - e1[1]))
    return np.where(inside, d_circ, d_end)


def sd_poly(px, pz, poly):
    """signed distance to a closed polygon (negative inside)."""
    d = np.full(px.shape, 1e9)
    inside = np.zeros(px.shape, bool)
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        d = np.minimum(d, sd_seg(px, pz, a, b))
        if (a[1] > b[1]) or (a[1] < b[1]):
            cond = ((a[1] > pz) != (b[1] > pz)) & (px < (b[0] - a[0]) * (pz - a[1]) / (b[1] - a[1]) + a[0])
            inside ^= cond
    return np.where(inside, -d, d)


def d_polyline(px, pz, pts):
    d = np.full(px.shape, 1e9)
    for a, b in zip(pts[:-1], pts[1:]):
        d = np.minimum(d, sd_seg(px, pz, a, b))
    return d


def sd_strokes(px, pz, strokes):
    d = np.full(px.shape, 1e9)
    for s in strokes:
        k = s[0]
        if k == "seg":
            d = np.minimum(d, sd_seg(px, pz, s[1], s[2]) - s[3] / 2)
        elif k == "arc":      # right half circle (bowl of R / P)
            d = np.minimum(d, sd_arc(px, pz, s[1], s[2], -math.pi / 2, math.pi / 2) - s[3] / 2)
        elif k == "arcr":
            d = np.minimum(d, sd_arc(px, pz, s[1], s[2], s[3], s[4]) - s[5] / 2)
        elif k == "disc":
            d = np.minimum(d, np.hypot(px - s[1][0], pz - s[1][1]) - s[2])
        elif k == "poly":
            d = np.minimum(d, sd_poly(px, pz, s[1]))
    return d


# ------------------------------------------------------------------ outlines + carvings (face coords: x right, z up)
def outline_round(hw, zs, rz, zb, n_arc=96, n_side=10):
    """rounded-top headstone, CCW seen from the front (-Y)."""
    pts = [(-hw, zb), (hw, zb)]
    for i in range(1, n_side + 1):
        pts.append((hw, zb + (zs - zb) * i / n_side))
    for i in range(1, n_arc):
        a = math.pi * i / n_arc
        pts.append((hw * math.cos(a), zs + rz * math.sin(a)))
    for i in range(n_side, 0, -1):
        pts.append((-hw, zb + (zs - zb) * i / n_side))
    return pts


def box(x0, x1, z0, z1):
    return [(x0, z0), (x1, z0), (x1, z1), (x0, z1)]


def jag(pts, rng, step=0.06, amp=0.025):
    """subdivide a polyline into jagged steps (a crack / fracture line)."""
    out = [pts[0]]
    for a, b in zip(pts[:-1], pts[1:]):
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        n = max(1, int(L / step))
        nx, nz = -(b[1] - a[1]) / L, (b[0] - a[0]) / L
        for i in range(1, n + 1):
            t = i / n
            j = rng.uniform(-amp, amp) if i < n else 0.0
            out.append((a[0] + (b[0] - a[0]) * t + nx * j, a[1] + (b[1] - a[1]) * t + nz * j))
    return out


def letter_R(x0, z0, h):
    S = lambda x, z: (x0 + x * h, z0 + z * h)
    return [("seg", S(0.15, 0.06), S(0.15, 0.94), 0.19 * h),
            ("seg", S(0.0, 0.955), S(0.22, 0.955), 0.09 * h),
            ("seg", S(0.0, 0.045), S(0.32, 0.045), 0.09 * h),
            ("seg", S(0.15, 0.925), S(0.38, 0.925), 0.15 * h),
            ("arc", S(0.38, 0.71), 0.215 * h, 0.17 * h),
            ("seg", S(0.15, 0.495), S(0.38, 0.495), 0.15 * h),
            ("seg", S(0.34, 0.50), S(0.62, 0.07), 0.18 * h),
            ("seg", S(0.50, 0.045), S(0.72, 0.045), 0.09 * h)]


def letter_I(x0, z0, h):
    S = lambda x, z: (x0 + x * h, z0 + z * h)
    return [("seg", S(0.18, 0.06), S(0.18, 0.94), 0.19 * h),
            ("seg", S(0.0, 0.955), S(0.36, 0.955), 0.09 * h),
            ("seg", S(0.0, 0.045), S(0.36, 0.045), 0.09 * h)]


def letter_P(x0, z0, h):
    S = lambda x, z: (x0 + x * h, z0 + z * h)
    return [("seg", S(0.15, 0.06), S(0.15, 0.94), 0.19 * h),
            ("seg", S(0.0, 0.955), S(0.22, 0.955), 0.09 * h),
            ("seg", S(0.0, 0.045), S(0.32, 0.045), 0.09 * h),
            ("seg", S(0.15, 0.925), S(0.36, 0.925), 0.15 * h),
            ("arc", S(0.36, 0.685), 0.24 * h, 0.17 * h),
            ("seg", S(0.15, 0.445), S(0.36, 0.445), 0.15 * h)]


def rip_strokes(cx, zb, h, gap=0.15):
    wR, wI, wP = 0.72, 0.36, 0.685
    total = (wR + wI + wP + 2 * gap) * h
    x = cx - total / 2
    st = letter_R(x, zb, h)
    x += (wR + gap) * h
    st += letter_I(x, zb, h)
    x += (wI + gap) * h
    st += letter_P(x, zb, h)
    return st


def epitaph(rng, lines, w):
    """worn, illegible epitaph lines: (z, half length) -> dash strokes like eroded words."""
    st = []
    for z, hl in lines:
        x = -hl
        while x < hl:
            L = rng.uniform(0.07, 0.24)
            x1 = min(hl, x + L)
            if rng.random() > 0.12:
                st.append(("seg", (x, z + rng.uniform(-0.008, 0.008)), (x1, z + rng.uniform(-0.008, 0.008)), w))
            x = x1 + rng.uniform(0.05, 0.09) * (2.2 if rng.random() < 0.25 else 1.0)
    return st


def skull_carve(cx, zc):
    """skull & crossbones: (shallow recess strokes, deep strokes)."""
    shallow = [("disc", (cx, zc + 0.08), 0.30),
               ("poly", [(cx - 0.17, zc - 0.31), (cx + 0.17, zc - 0.31), (cx + 0.19, zc - 0.08), (cx - 0.19, zc - 0.08)])]
    deep = [("disc", (cx - 0.125, zc + 0.04), 0.088), ("disc", (cx + 0.125, zc + 0.04), 0.088),
            ("poly", [(cx - 0.05, zc - 0.05), (cx + 0.05, zc - 0.05), (cx, zc - 0.14)])]
    for x in (-0.105, -0.035, 0.035, 0.105):
        deep.append(("seg", (cx + x, zc - 0.29), (cx + x, zc - 0.2), 0.026))
    bones = []
    for (x0, z0, x1, z1) in ((-0.52, zc - 0.66, 0.52, zc - 0.30), (-0.52, zc - 0.30, 0.52, zc - 0.66)):
        bones.append(("seg", (cx + x0, z0), (cx + x1, z1), 0.085))
        dx, dz = x1 - x0, z1 - z0
        L = math.hypot(dx, dz)
        nx, nz = -dz / L * 0.045, dx / L * 0.045
        for (ex, ez) in ((x0, z0), (x1, z1)):
            bones.append(("disc", (cx + ex + nx, ez + nz), 0.055))
            bones.append(("disc", (cx + ex - nx, ez - nz), 0.055))
    return shallow, deep, bones


# ------------------------------------------------------------------ the three stones
def spec(key):
    rng = random.Random({"A": 11, "B": 23, "C": 37}[key])
    if key == "A":
        poly = outline_round(1.5, 2.65, 1.35, -0.28)
        border = outline_round(1.5 - 0.27, 2.65, 1.35 - 0.27, 0.64)
        S = dict(name="Grave_A", seed=11, H=4.0, parts=[dict(poly=poly, y0=-0.5, y1=0.5)], bevel=0.14,
                 taper_x=0.05, taper_y=0.12, bend_x=0.03, lean_back=2.5, lean_side=-1.8, yaw=0.0,
                 carve=[dict(sd=("groove", border, 0.05), depth=0.05, wall=0.028, erode=0.010, wear=0.25),
                        dict(sd=("strokes", rip_strokes(0.0, 1.72, 1.0)), depth=0.085, wall=0.032, erode=0.010,
                             wear=0.2),
                        dict(sd=("strokes", [("seg", (0, 2.94), (0, 3.48), 0.12),
                                             ("seg", (-0.18, 3.30), (0.18, 3.30), 0.12)]),
                             depth=0.065, wall=0.03, erode=0.010, wear=0.2),
                        dict(sd=("strokes", epitaph(rng, [(1.40, 0.84), (1.15, 0.62)], 0.065)), depth=0.035,
                             wall=0.02, erode=0.012, wear=0.55)],
                 cracks=[dict(pts=jag([(1.22, 3.62), (0.98, 3.25), (1.02, 2.98), (0.84, 2.72)], rng), w=0.032,
                              depth=0.075),
                         dict(pts=jag([(-1.6, 1.05), (-1.25, 0.92), (-1.12, 0.7)], rng), w=0.026, depth=0.06)],
                 chip=dict(freq=2.3, prob=0.62, cmin=0.09, cmax=0.25, rmin=0.16, rmax=0.38, slope=1.25),
                 moss=0.85, lichen=0.6, tone=(0, 0, 0), voxel=0.012,
                 mound=dict(cx=0.0, cy=-0.32, ax=2.0, ay=1.38, H=0.42, bumps=[(0.9, -0.75, 0.35, 0.06)]),
                 blades=[(-1.45, -0.62, 6), (1.35, -0.6, 5), (-0.3, -0.72, 4), (1.62, 0.2, 4), (-1.62, 0.25, 4),
                         (0.55, 0.62, 3)],
                 lo_target=2550)
    elif key == "B":
        cross = [(-0.31, 0.6), (0.31, 0.6), (0.31, 2.72), (1.3, 2.66), (1.3, 3.18), (1.16, 3.42), (0.31, 3.36),
                 (0.36, 4.2), (-0.36, 4.2), (-0.31, 3.36), (-1.3, 3.42), (-1.3, 2.66), (-0.31, 2.72)]
        inset = [(-0.20, 0.98), (0.20, 0.98), (0.20, 2.83), (1.18, 2.78), (1.18, 3.12), (1.08, 3.30), (0.20, 3.25),
                 (0.245, 4.09), (-0.245, 4.09), (-0.20, 3.25), (-1.18, 3.30), (-1.18, 2.78), (-0.20, 2.83)]
        diamond = [(0, 2.88), (0.15, 3.04), (0, 3.20), (-0.15, 3.04)]
        S = dict(name="Grave_B", seed=23, H=4.2,
                 parts=[dict(poly=box(-0.95, 0.95, -0.25, 0.40), y0=-0.47, y1=0.47),
                        dict(poly=box(-0.74, 0.74, 0.30, 0.78), y0=-0.38, y1=0.38),
                        dict(poly=cross, y0=-0.28, y1=0.28)],
                 bevel=0.10, taper_x=0.0, taper_y=0.0, bend_x=0.0, lean_back=1.2, lean_side=3.5, yaw=0.0,
                 carve=[dict(sd=("groove", inset, 0.036), depth=0.045, wall=0.022, erode=0.008, wear=0.2, zmin=0.9),
                        dict(sd=("strokes", [("poly", diamond)]), depth=0.06, wall=0.025, erode=0.008, wear=0.15),
                        dict(sd=("groove", box(-0.6, 0.6, 0.44, 0.66), 0.03), depth=0.035, wall=0.02, erode=0.01,
                             wear=0.3)],
                 cracks=[dict(pts=jag([(-0.45, 1.52), (-0.1, 1.62), (0.12, 1.58), (0.45, 1.78)], rng), w=0.035,
                              depth=0.085),
                         dict(pts=jag([(0.9, 3.5), (0.98, 3.2), (0.86, 3.05)], rng), w=0.026, depth=0.05)],
                 chip=dict(freq=2.6, prob=0.58, cmin=0.07, cmax=0.19, rmin=0.13, rmax=0.3, slope=1.25),
                 moss=0.75, lichen=0.75, tone=(6, 2, -4), voxel=0.011,
                 mound=dict(cx=0.0, cy=-0.25, ax=1.75, ay=1.3, H=0.22, bumps=[(-0.7, -0.75, 0.3, 0.05)]),
                 blades=[(-1.1, -0.62, 5), (1.12, -0.55, 5), (0.15, -0.68, 3), (1.15, 0.45, 4), (-1.12, 0.42, 4)],
                 lo_target=2500)
    else:
        top = lambda x: 3.38 + 0.30 * (1 - (x / 1.6) ** 2)
        # review round 1: the 0.07-step jittered outline, extruded through the slab, made parallel ripples + "teeth".
        # The fracture is now 6 chunky straight facets (0.2-0.26 long) + isotropic Voronoi cut planes (see "facets").
        # The old jag() call is kept (result unused) so every later rng draw (cracks, epitaph) is unchanged.
        jag([(1.56, 2.52), (1.40, 2.70), (1.34, 2.90), (1.14, 3.02), (1.08, 3.24), (0.90, 3.33), (0.86, top(0.86))],
            rng, step=0.07, amp=0.03)
        frac = [(1.56, 2.52), (1.40, 2.70), (1.34, 2.90), (1.14, 3.02), (1.08, 3.24), (0.90, 3.33), (0.86, top(0.86))]
        poly = [(-1.58, -0.2), (1.56, -0.2)] + [(1.56, -0.2 + 2.72 * i / 10) for i in range(1, 10)] + frac[:-1]
        poly += [(x, top(x)) for x in np.linspace(0.86, -1.52, 34)]
        poly += [(-1.58, 3.30), (-1.58, 2.15), (-1.50, 2.06), (-1.53, 1.94), (-1.58, 1.90)]
        poly += [(-1.58, z) for z in np.linspace(1.6, 0.0, 6)]
        crack = jag([(-0.40, 3.85), (-0.52, 3.30), (-0.78, 3.02), (-0.92, 2.55), (-1.26, 2.18), (-1.40, 1.70),
                     (-1.80, 1.36)], rng, step=0.055, amp=0.03)
        shallow, deep, bones = skull_carve(0.05, 2.78)
        S = dict(name="Grave_C", seed=37, H=3.68, parts=[dict(poly=poly, y0=-0.45, y1=0.45)], bevel=0.12,
                 taper_x=0.0, taper_y=0.06, bend_x=-0.03, lean_back=9.5, lean_side=-3.0, yaw=4.0,
                 carve=[dict(sd=("strokes", shallow), depth=0.032, wall=0.02, erode=0.010, wear=0.3),
                        dict(sd=("strokes", deep), depth=0.075, wall=0.025, erode=0.008, wear=0.15),
                        dict(sd=("strokes", bones), depth=0.055, wall=0.025, erode=0.010, wear=0.3),
                        dict(sd=("strokes", epitaph(rng, [(1.78, 0.98), (1.52, 1.06), (1.26, 0.8), (1.0, 0.5)],
                                                    0.065)), depth=0.032, wall=0.02, erode=0.014, wear=0.75)],
                 cracks=[dict(pts=crack, w=0.045, depth=0.12),
                         dict(pts=jag([(0.42, 0.35), (0.62, 0.88), (0.88, 1.22), (1.04, 1.62)], rng), w=0.03,
                              depth=0.07),
                         dict(pts=jag([(0.62, 0.88), (0.30, 1.10), (0.22, 1.32)], rng), w=0.022, depth=0.05)],
                 piece=dict(poly=crack + [(-1.95, 4.1)], vec=(-0.018, -0.04, -0.03)),
                 fracture=frac,
                 facets=dict(freq=4.6, hmin=0.02, hmax=0.1, slope=0.38, band=0.022, zone=0.14),
                 # round 2: broader, shallower chips (a deep narrow one read as a dark slot on the right side)
                 chip=dict(freq=2.4, prob=0.7, cmin=0.08, cmax=0.2, rmin=0.2, rmax=0.42, slope=0.8),
                 moss=1.0, lichen=1.0, tone=(-8, -4, 0), voxel=0.012,
                 mound=dict(cx=0.05, cy=-0.38, ax=2.2, ay=1.42, H=0.33, bumps=[(0.3, -0.62, 0.42, 0.07),
                                                                                (-1.0, 0.45, 0.35, 0.05)]),
                 blades=[(-1.55, -0.55, 6), (1.4, -0.66, 5), (0.35, -0.75, 4), (1.6, 0.35, 4), (-1.66, 0.6, 3),
                         (-0.5, 0.95, 3)],
                 lo_target=2550)
    return S


# ------------------------------------------------------------------ mesh helpers
def extrude_parts(name, parts, bevel):
    bm = bmesh.new()
    for part in parts:
        b = bmesh.new()
        vs = [b.verts.new((x, part["y0"], z)) for x, z in part["poly"]]
        f = b.faces.new(vs)
        ext = bmesh.ops.extrude_face_region(b, geom=[f])
        moved = [e for e in ext["geom"] if isinstance(e, bmesh.types.BMVert)]
        bmesh.ops.translate(b, vec=(0, part["y1"] - part["y0"], 0), verts=moved)
        bmesh.ops.recalc_face_normals(b, faces=b.faces)
        tmp = bpy.data.meshes.new("_p")
        b.to_mesh(tmp)
        b.free()
        bm.from_mesh(tmp)
        bpy.data.meshes.remove(tmp)
    ob = obj_from_bm(bm, name, smooth=False)
    bv = ob.modifiers.new("Bevel", "BEVEL")
    bv.width = bevel
    bv.segments = 5
    bv.limit_method = "ANGLE"
    bv.angle_limit = math.radians(35)
    bv.use_clamp_overlap = False
    apply_mods(ob)
    return ob


def remesh(ob, voxel):
    r = ob.modifiers.new("Remesh", "REMESH")
    r.mode = "VOXEL"
    r.voxel_size = voxel
    r.adaptivity = 0.0
    r.use_smooth_shade = True
    apply_mods(ob)


def arrays(ob):
    me = ob.data
    n = len(me.vertices)
    P = np.empty(n * 3, np.float32)
    me.vertices.foreach_get("co", P)
    N = np.empty(n * 3, np.float32)
    me.vertex_normals.foreach_get("vector", N)
    return P.reshape(-1, 3).astype(np.float64), N.reshape(-1, 3).astype(np.float64)


def set_positions(ob, P):
    ob.data.vertices.foreach_set("co", P.astype(np.float32).ravel())
    ob.data.update()


def deform(P, S):
    P = P.copy()
    t = np.clip(P[:, 2] / S["H"], 0.0, 1.0)
    P[:, 0] = P[:, 0] * (1 - S.get("taper_x", 0) * t) + S.get("bend_x", 0) * t * t
    P[:, 1] = P[:, 1] * (1 - S.get("taper_y", 0) * t) + S.get("bend_y", 0) * t * t
    R = (Matrix.Rotation(math.radians(S.get("yaw", 0)), 3, "Z")
         @ Matrix.Rotation(math.radians(S.get("lean_side", 0)), 3, "Y")
         @ Matrix.Rotation(-math.radians(S.get("lean_back", 0)), 3, "X"))
    return P @ np.array(R).T


def offsets(seed, n=20):
    rng = random.Random(seed * 7919 + 13)
    return [Vector((rng.uniform(-60, 60), rng.uniform(-60, 60), rng.uniform(-60, 60))) for _ in range(n)]


# ------------------------------------------------------------------ stone fields (displacement + colour + roughness)
def noise_fields(P, S, hi):
    o = offsets(S["seed"])
    cf = S["chip"]["freq"]
    n = len(P)
    keys = ["low"]
    if hi:
        keys += ["mid", "pit", "micro", "ero", "tone", "mott", "speck", "streak", "lich", "lich2", "moss", "mossh",
                 "brk", "wear"]
    A = {k: np.empty(n) for k in keys}
    A["d"], A["c1"], A["c2"] = np.empty((n, 4)), np.empty((n, 4)), np.empty((n, 4))
    if hi:
        A["lF1"], A["lc"], A["lc2"] = np.empty(n), np.empty(n), np.empty(n)
    nz, vor, cell = noise.noise, noise.voronoi, noise.cell
    for i in range(n):
        p = Vector(P[i])
        A["low"][i] = fbm(p * 1.3 + o[0], 3)
        d, pts = vor(p * cf + o[1])
        for k in range(4):
            A["d"][i, k] = d[k]
            A["c1"][i, k] = 0.5 + 0.5 * cell(pts[k])
            A["c2"][i, k] = 0.5 + 0.5 * cell(pts[k] * 1.731 + o[2])
        if hi:
            A["mid"][i] = fbm(p * 6.0 + o[3], 3)
            A["pit"][i] = nz(p * 15.0 + o[4])
            A["micro"][i] = nz(p * 46.0 + o[5])
            A["ero"][i] = nz(p * 24.0 + o[6])
            A["tone"][i] = fbm(p * 0.8 + o[7], 2)
            A["mott"][i] = fbm(p * 3.2 + o[8], 3)
            A["speck"][i] = nz(p * 42.0 + o[9])
            A["streak"][i] = nz(Vector((p.x * 5.5, p.y * 5.5, p.z * 0.6)) + o[10]) + 0.3 * nz(p * 9.0 + o[19])
            A["lich"][i] = fbm(p * 3.6 + o[11], 2)
            A["lich2"][i] = nz(p * 2.0 + o[12])
            A["moss"][i] = fbm(p * 2.6 + o[13], 3)
            A["mossh"][i] = fbm(p * 28.0 + o[14], 2)
            A["brk"][i] = fbm(p * 10.0 + o[15], 2)
            A["wear"][i] = nz(p * 1.6 + o[16])
            d, pts = vor(p * 7.0 + o[17])
            A["lF1"][i] = d[0]
            A["lc"][i] = 0.5 + 0.5 * cell(pts[0])
            A["lc2"][i] = 0.5 + 0.5 * cell(pts[0] * 2.3 + o[18])
    if "facets" in S and hi:     # isotropic Voronoi cut planes for the fresh break (bake source only)
        Fc = S["facets"]
        fo = offsets(S["seed"] + 911, 4)
        ff = Fc["freq"]
        A["fL1"], A["fL2"], A["fF"], A["fgrain"] = np.empty(n), np.empty(n), np.empty(n), np.zeros(n)
        cv = noise.cell_vector
        for i in range(n):
            p = Vector(P[i])
            d, pts = vor(p * ff + fo[0])
            for k, key in ((0, "fL1"), (1, "fL2")):
                q = pts[k]
                qw = (q - fo[0]) / ff
                h = Fc["hmin"] + (Fc["hmax"] - Fc["hmin"]) * (0.5 + 0.5 * cell(q + fo[1]))
                A[key][i] = h + Fc["slope"] * cv(q + fo[2]).dot(p - qw)
            A["fF"][i] = (d[1] - d[0]) / ff
            if hi:
                A["fgrain"][i] = fbm(p * 22.0 + fo[3], 2)
    return A


def part_metrics(P, parts):
    """per vertex: e = distance to the nearest rim edge (along the surface), s2 / face distance, junction flag."""
    x, y, z = P[:, 0], P[:, 1], P[:, 2]
    best = None
    near = np.zeros(len(P), int)
    for part in parts:
        s2 = sd_poly(x, z, part["poly"])
        side = np.minimum(y - part["y0"], part["y1"] - y)
        sd3 = np.maximum(s2, -side)
        e = np.maximum(np.maximum(-s2, 0.0), np.maximum(side, 0.0))
        near += (np.abs(sd3) < 0.06)
        if best is None:
            best = [np.abs(sd3), e, -s2]
        else:
            pick = np.abs(sd3) < best[0]
            best[0] = np.where(pick, np.abs(sd3), best[0])
            best[1] = np.where(pick, e, best[1])
            best[2] = np.where(pick, -s2, best[2])
    return best[1], best[2], near > 1


def carve_depth(x, z, A, layer):
    k = layer["sd"]
    if k[0] == "groove":
        sd = np.abs(sd_poly(x, z, k[1])) - k[2]
    else:
        sd = sd_strokes(x, z, k[1])
    sd = sd + layer["erode"] * A["ero"]
    d = layer["depth"] * sm(0.0, layer["wall"], -sd)
    d *= 1.0 - layer["wear"] * sm(-0.15, 0.45, A["mid"])
    if "zmin" in layer:
        d *= sm(layer["zmin"] - 0.05, layer["zmin"] + 0.05, z)
    return d


def stone_fields(P, N, S, hi):
    A = noise_fields(P, S, hi)
    x, y, z = P[:, 0], P[:, 1], P[:, 2]
    e, eface, junction = part_metrics(P, S["parts"])
    above = sm(0.05, 0.45, z)
    # chips: Voronoi cells along the rims, each a chamfer of its own depth
    c = S["chip"]
    prob = c["prob"] * (0.55 + 0.9 * sm(0.8, S["H"], z)) * above * (~junction)
    chip = np.zeros(len(P))
    for k in range(4):
        # a chip = a chamfer cut across the rim whose depth tapers smoothly to 0 away from a Voronoi point (no cell
        # walls -> no rectangular slots): lens-shaped outline on both faces, flat fracture surface
        ck = c["cmin"] + (c["cmax"] - c["cmin"]) * A["c2"][:, k]
        Rk = c["rmin"] + (c["rmax"] - c["rmin"]) * ((A["c2"][:, k] * 13.7) % 1.0)
        dk = A["d"][:, k] / c["freq"]
        ce = ck * np.maximum(0.0, 1 - (dk / Rk) ** 2)
        chip = np.maximum(chip, (A["c1"][:, k] < prob) * np.maximum(0.0, ce - c["slope"] * e))
    fz = np.zeros(len(P))
    if "facets" in S:     # stepped planar facets: each cell its own tilted cut plane, crisp 0.02 steps between cells
        Fc = S["facets"]
        fmask = sm(Fc["zone"], 0.02, d_polyline(x, z, S["fracture"])) * above
        if hi:
            w = sm(0.0, Fc["band"], A["fF"])
            rem = A["fL1"] * w + 0.5 * (A["fL1"] + A["fL2"]) * (1 - w)
            fz = np.clip(rem, 0.0, Fc["hmax"] + 0.06) * fmask
        else:             # game mesh: a smooth mean-depth offset; the facets come from the bake (decimating the
            fz = 0.5 * (Fc["hmin"] + Fc["hmax"]) * fmask      # sharp steps left triangular shards)
    disp = 0.032 * A["low"] - chip - fz
    off = np.zeros_like(P)
    if "piece" in S:   # the broken-off top-left piece of the cracked slab sits a little proud and lower
        f = sm(0.03, -0.03, sd_poly(x, z, S["piece"]["poly"]))
        off += f[:, None] * np.array(S["piece"]["vec"])[None, :]
    if not hi:
        return disp, off, None
    front = sm(0.55, 0.85, -N[:, 1]) * sm(0.06, 0.14, eface)
    carve = np.zeros(len(P))
    for layer in S["carve"]:
        carve = carve + carve_depth(x, z, A, layer)
    carve = np.minimum(carve, 0.12) * front
    crack = np.zeros(len(P))
    for cr in S["cracks"]:
        d = d_polyline(x, z, cr["pts"]) + 0.008 * A["ero"]
        crack = np.maximum(crack, cr["depth"] * np.clip(1 - d / cr["w"], 0, 1) ** 1.4)
    crack *= above
    brk = np.zeros(len(P))
    if "fracture" in S:
        brk = sm(0.13, 0.03, d_polyline(x, z, S["fracture"]))
    pits = sm(0.5, 0.8, A["pit"]) * 0.016
    cav = np.clip(carve / 0.05 + crack / 0.05, 0, 1)
    # moss: base band, tops, cavities
    mz = sm(0.95, 0.12, z) * sm(-0.25, 0.25, A["moss"] + 0.1)
    mt = sm(0.5, 0.9, N[:, 2]) * sm(0.02, 0.32, A["moss"]) * 0.9
    mc = sm(0.25, 0.9, cav) * sm(0.0, 0.3, A["moss"]) * 0.75
    moss = np.clip((mz + mt + 0.8 * mc) * S["moss"], 0, 1) * sm(0.4, 0.7, sm(-0.2, 0.2, A["mossh"]) + 0.55)
    moss = np.clip(moss, 0, 1) * (1 - 0.9 * brk)        # the fresh break is (almost) moss-free
    grain = A["fgrain"] * 0.005 if "facets" in S else A["brk"] * 0.016
    disp = (disp + 0.007 * A["mid"] - pits * (1 - moss) + 0.0028 * A["micro"] - carve - crack
            + brk * grain + 0.016 * moss * (0.5 + 0.5 * sm(-0.3, 0.4, A["mossh"])))
    # chipped surfaces get a rough fracture texture
    chipz = sm(0.004, 0.03, chip)
    disp += chipz * 0.012 * A["brk"]
    # ------------------------------------------------ colour (linear) + roughness
    tone = np.array(S["tone"], dtype=np.float64)
    L = lambda c: np.array(lin(tuple(np.clip(np.array(c) + tone, 0, 255))))
    warm, cool, dark, light = L((146, 132, 113)), L((116, 120, 126)), L((84, 83, 84)), L((180, 172, 158))
    grime, chipc, streak = L((58, 55, 50)), L((180, 173, 158)), L((88, 90, 90))
    Ln = lambda c: np.array(lin(c))
    lp, ly, lo_ = Ln((160, 166, 132)), Ln((184, 160, 80)), Ln((180, 116, 52))
    md, mm, ml = Ln((50, 82, 24)), Ln((86, 122, 32)), Ln((146, 168, 50))
    soil = Ln((104, 82, 58))
    T = lambda a: a[:, None]
    col = warm + (cool - warm) * T(sm(-0.35, 0.35, A["tone"]))
    col = col + (dark - col) * T(0.34 * sm(-0.1, 0.6, A["mott"]))
    col = col + (light - col) * T(0.16 * sm(0.15, 0.6, -A["mott"]))
    col = col * T(1.0 + 0.06 * A["speck"])
    face = sm(0.4, 0.8, np.abs(N[:, 1]))
    st = sm(0.15, 0.6, A["streak"]) * face * (0.35 + 0.65 * sm(1.0, S["H"], z))
    col = col + (streak - col) * T(0.45 * st)
    edge = sm(0.16, 0.02, e) * above
    col = col + (light - col) * T(0.3 * edge * sm(-0.3, 0.3, A["mott"] + 0.2))
    col = col + (chipc - col) * T(0.7 * chipz)
    fresh = L((190, 182, 166))
    col = col + (fresh - col) * T(0.62 * brk)          # fresh break: lighter, cleaner stone
    col = col + (grime - col) * T(np.clip(0.85 * cav + 0.3 * sm(0.55, 0.85, A["pit"]), 0, 1))
    # lichen blotches: pale grey-green rosettes + a few yellow / orange ones
    clus = sm(0.05, 0.35, A["lich"]) * (0.4 + 0.6 * sm(1.2, S["H"], z))
    lrad = 0.2 + 0.22 * A["lc2"] + 0.12 * A["ero"]          # lobed rosettes
    lich = (A["lc"] > 1 - 0.38 * S["lichen"]) * sm(lrad, lrad - 0.1, A["lF1"]) * clus * above * (1 - cav) * (1 - brk)
    lcol = np.where(T(A["lc2"] > 0.78), np.array(ly), np.array(lp))
    col = col + (lcol - col) * T(0.42 * lich)
    col = col + (soil - col) * T(0.55 * sm(0.45, -0.05, z))
    mcol = md + (mm - md) * T(sm(-0.3, 0.2, A["mossh"]))
    mcol = mcol + (ml - mcol) * T(0.6 * sm(0.15, 0.5, A["mossh"]))
    col = col + (mcol - col) * T(moss)
    rough = 0.84 + 0.06 * A["mott"] + 0.06 * cav - 0.08 * chipz + 0.1 * moss + 0.04 * lich
    return disp, off, dict(col=np.clip(col, 0, 1), rough=np.clip(rough, 0.3, 1.0), moss=moss)


def build_stone(S, voxel, hi, name):
    ob = extrude_parts(name, S["parts"], S["bevel"])
    remesh(ob, voxel)
    P, N = arrays(ob)
    log(name, "remeshed verts", len(P))
    disp, off, cr = stone_fields(P, N, S, hi)
    P2 = deform(P + N * disp[:, None] + off, S)
    P2[:, 2] = np.maximum(P2[:, 2], -0.28)
    set_positions(ob, P2)
    if hi:
        set_colors(ob.data, "Col", [tuple(c) for c in cr["col"]])
        set_colors(ob.data, "Rough", [(r, r, r) for r in cr["rough"]])
    for p in ob.data.polygons:
        p.use_smooth = True
    return ob


# ------------------------------------------------------------------ soil mound (polar heightfield)
SOIL = dict(dark=(92, 64, 42), mid=(128, 92, 60), dry=(166, 134, 96), pebble=(124, 118, 108),
            leaf1=(150, 88, 40), leaf2=(112, 64, 32), moss=(92, 120, 36))


def mound_height(x, y, M, o, hi, extra=None):
    dx, dy = (x - M["cx"]) / M["ax"], (y - M["cy"]) / M["ay"]
    r2 = dx * dx + dy * dy
    r = math.sqrt(r2)
    h = M["H"] * max(0.0, 1 - r2) ** 1.4 - 0.08 * smoothstep(0.78, 1.08, r)
    p = Vector((x, y, 0.0))
    h += 0.09 * fbm(p * 1.4 + o[0], 2) * max(0.0, 1 - r2) ** 0.5
    for bx, by, br, bh in M["bumps"]:
        h += bh * math.exp(-((x - bx) ** 2 + (y - by) ** 2) / (br * br))
    if not hi:
        return h
    inner = max(0.0, 1 - r2) ** 0.3
    clod = max(0.0, noise.noise(p * 4.6 + o[1])) ** 1.5
    h += (0.06 * clod + 0.014 * noise.noise(p * 15.0 + o[2]) + 0.004 * noise.noise(p * 42.0 + o[3])) * inner
    d, pts = noise.voronoi(p * 5.5 + o[4])
    peb = 0.5 + 0.5 * noise.cell(pts[0])
    pb = 0.0
    if peb > 0.8:
        pb = max(0.0, 1 - d[0] / 0.38) ** 0.6
        h += 0.03 * pb * inner
    if extra is not None:
        extra.update(clod=clod, peb=pb, r=r)
    return h


def mound_mesh(name, M, seed, hi, rings, segs):
    o = offsets(seed + 101)
    bm = bmesh.new()
    cols, rough = [], []
    rows = []

    def add(x, y):
        ex = {}
        z = mound_height(x, y, M, o, hi, ex if hi else None)
        v = bm.verts.new((x, y, z))
        if hi:
            p = Vector((x, y, 0))
            t = noise.noise(p * 2.2 + o[5])
            c = mix(lin(SOIL["dark"]), lin(SOIL["mid"]), smoothstep(-0.4, 0.4, t))
            c = mix(c, lin(SOIL["dry"]), 0.55 * ex["clod"] * smoothstep(-0.2, 0.4, noise.noise(p * 9.0 + o[6])))
            c = mix(c, lin(SOIL["dark"]), 0.35 * smoothstep(0.0, 0.6, noise.noise(p * 24.0 + o[7])))
            c = mix(c, lin(SOIL["pebble"]), 0.6 * smoothstep(0.1, 0.4, ex["peb"]))
            lf = noise.noise(p * 7.5 + o[8])
            if lf > 0.5:
                c = mix(c, lin(SOIL["leaf1"] if noise.noise(p * 7 + o[9]) > 0 else SOIL["leaf2"]),
                        0.5 * smoothstep(0.5, 0.56, lf))
            ms = smoothstep(0.35, 0.6, fbm(p * 2.0 + o[10], 2)) * smoothstep(1.0, 0.55, ex["r"])
            c = mix(c, lin(SOIL["moss"]), 0.55 * ms)
            cols.append(c)
            rr = 0.93 - 0.08 * smoothstep(0.1, 0.4, ex["peb"]) - 0.1 * ms * 0
            rough.append((rr, rr, rr))
        return v

    centre = add(M["cx"], M["cy"])
    for i in range(1, rings + 1):
        rho = 1.08 * (i / rings) ** 0.85
        row = []
        for j in range(segs):
            th = 2 * math.pi * j / segs
            row.append(add(M["cx"] + M["ax"] * rho * math.cos(th), M["cy"] + M["ay"] * rho * math.sin(th)))
        rows.append(row)
    for j in range(segs):
        bm.faces.new((centre, rows[0][j], rows[0][(j + 1) % segs]))
    for i in range(rings - 1):
        for j in range(segs):
            a, b = rows[i][j], rows[i][(j + 1) % segs]
            c2, d2 = rows[i + 1][(j + 1) % segs], rows[i + 1][j]
            bm.faces.new((a, d2, c2, b))   # radial x tangential = +Z (no recalc: it flipped the open dome)
    ob = obj_from_bm(bm, name)
    if hi:
        set_colors(ob.data, "Col", cols)
        set_colors(ob.data, "Rough", rough)
    return ob


# ------------------------------------------------------------------ dead-grass blades (shared with the tufts)
# strip atlas: 8 colour variants; front strip k, back strip 8 + k
VARIANTS = [
    dict(base=(206, 180, 112), tip=(230, 216, 170), root=(116, 98, 56), spots=False),   # 0 straw
    dict(base=(218, 198, 140), tip=(232, 220, 182), root=(126, 108, 64), spots=False),  # 1 pale straw
    dict(base=(198, 158, 76), tip=(224, 196, 124), root=(110, 86, 40), spots=True),     # 2 golden
    dict(base=(140, 136, 62), tip=(198, 180, 108), root=(82, 86, 36), spots=False),     # 3 olive
    dict(base=(148, 118, 66), tip=(190, 158, 102), root=(88, 70, 40), spots=True),      # 4 olive-brown
    dict(base=(180, 140, 90), tip=(206, 178, 130), root=(102, 78, 48), spots=True),     # 5 tan
    dict(base=(176, 158, 120), tip=(208, 194, 160), root=(102, 90, 64), spots=False),   # 6 grey dead
    dict(base=(118, 126, 54), tip=(178, 170, 92), root=(70, 80, 34), spots=False),      # 7 green-olive
]


# review round 1: tuft colours without the pink cast (tan -> straw-tan, faded -> ash grey), spots on ~1 blade in 3-4
VARIANTS_T = [
    dict(base=(206, 180, 112), tip=(230, 216, 170), root=(116, 98, 56), spots=0),      # 0 straw
    dict(base=(218, 198, 140), tip=(232, 220, 182), root=(126, 108, 64), spots=0),     # 1 pale straw
    dict(base=(198, 160, 78), tip=(224, 198, 126), root=(110, 86, 40), spots=2),       # 2 golden
    dict(base=(140, 136, 62), tip=(198, 180, 108), root=(82, 86, 36), spots=0),        # 3 olive
    dict(base=(148, 122, 66), tip=(190, 162, 102), root=(88, 72, 40), spots=3),        # 4 olive-brown
    dict(base=(184, 156, 98), tip=(212, 192, 142), root=(104, 84, 50), spots=0),       # 5 straw-tan
    dict(base=(166, 162, 146), tip=(204, 200, 186), root=(98, 94, 80), spots=0),       # 6 ash grey
    dict(base=(118, 126, 54), tip=(178, 170, 92), root=(70, 80, 34), spots=0),         # 7 green-olive
]


def arc_nseg(bend):
    """long arching blades: enough segments for <= ~7 deg per joint (review round 1)."""
    return int(max(8, min(10, math.ceil(math.degrees(bend) * 1.25 / 6.5) + 1)))


def paint_strip(Hpx, Wpx, var, back, seed, style=1):
    """one blade strip: (H, W, 3) sRGB albedo, (H, W, 3) encoded tangent normal, (H, W) roughness."""
    rng = np.random.default_rng(seed)
    u = (np.arange(Wpx) + 0.5) / Wpx
    v = (np.arange(Hpx) + 0.5) / Hpx
    U, V = np.meshgrid(u, v)
    base, tip, root = s255(var["base"]), s255(var["tip"]), s255(var["root"])
    T = lambda a: a[..., None]
    col = root + (base - root) * T(sm(0.0, 0.32, V))
    col = col + (tip - col) * T(0.8 * sm(0.6, 1.0, V))
    s = np.zeros_like(U)
    for f in ((4.0, 7.0, 11.0, 16.0) if style == 1 else (6.0, 11.0, 17.0, 23.0)):
        drift = rng.uniform(1, 4) if style == 1 else rng.uniform(-0.25, 0.25)    # style 2: straight veins
        s += np.sin(2 * math.pi * (f * U + rng.uniform(0, 1)) + drift * V * 2 * math.pi) / f * 3
    col = col * T(1.0 + 0.09 * s)
    edge = sm(0.3, 0.5, np.abs(U - 0.5))
    col = col + (s255((118, 90, 54)) - col) * T(0.35 * edge)
    mid = np.exp(-((U - 0.5) / 0.05) ** 2)
    col = col + (s255((236, 224, 182)) - col) * T((0.15 if back else 0.25) * mid)
    if var["spots"]:
        for _ in range(4 if style == 1 else int(var["spots"])):
            cu, cv = rng.uniform(0.25, 0.75), rng.uniform(0.3, 0.95)
            ru, rv = rng.uniform(0.1, 0.22), rng.uniform(0.006, 0.016)
            d = ((U - cu) / ru) ** 2 + ((V - cv) / rv) ** 2
            col = col + (s255((92, 66, 38)) - col) * T(0.75 * sm(1.0, 0.4, d))
    if back:
        col = col * 0.93 + 0.07 * s255((200, 190, 150))
    col = col * T(0.5 + 0.5 * sm(0.0, 0.3, V))
    g = np.exp(-((U - 0.5) / 0.07) ** 2) * np.sign(U - 0.5)
    nx = 0.2 * np.sin(2 * math.pi * U * 5.0) * (1 - mid) + (0.38 if back else -0.42) * g
    ny = 0.035 * np.sin(2 * math.pi * V * rng.uniform(9, 14) + rng.uniform(0, 6)) * sm(0.4, 0.9, V)
    nrm = np.stack([nx, ny, np.ones_like(nx)], -1)
    nrm /= np.linalg.norm(nrm, axis=-1, keepdims=True)
    rough = 0.84 + 0.05 * s / 3 + 0.06 * sm(0.6, 1.0, V)
    return np.clip(col, 0, 1), nrm * 0.5 + 0.5, np.clip(rough, 0, 1)


def add_blade(acc, root, az, tilt, length, w0, droop, nseg, rng, kink=None, twist=0.0, blunt=0.0, wob=0.07, prof=(0.25, 1.5),
              sf=(0.0, 1.0), sb=(0.0, 1.0), vr=(0.01, 0.99)):
    """one closed keeled blade: flat front strip (L, R) + V back (L, K, R); front / back own vertices (hard edge)."""
    V, F, UV = acc["V"], acc["F"], acc["UV"]
    o = Vector((math.cos(az), math.sin(az), 0.0))
    a = Vector((-math.sin(az), math.cos(az), 0.0))
    d = Matrix.Rotation(tilt, 3, a) @ Vector((0, 0, 1))
    Sv = Matrix.Rotation(rng.uniform(-0.6, 0.6), 3, d) @ a
    seg = length / nseg
    C, Ds, Ss = [Vector(root)], [d.copy()], [Sv.copy()]
    for i in range(nseg):
        t = (i + 0.5) / nseg
        ang = droop * seg * (prof[0] + prof[1] * t)
        if kink and i == kink[0]:
            ang += kink[1]
        d = Matrix.Rotation(ang, 3, a) @ d
        wa = Vector((rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(-1, 1))).cross(d)
        if wa.length > 1e-6:
            d = Matrix.Rotation(rng.uniform(-1, 1) * wob, 3, wa.normalized()) @ d
        d.normalize()
        C.append(C[-1] + d * seg)
        Sv = (Sv - d * Sv.dot(d)).normalized()
        Sv = Matrix.Rotation(twist / nseg, 3, d) @ Sv
        Ds.append(d.copy())
        Ss.append(Sv.copy())
    pointed = blunt <= 0.0
    nring = nseg if pointed else nseg + 1
    rings = []
    for i in range(nring):
        t = i / nseg
        if i == 0:
            dr = Ds[1]
        elif i == nseg:
            dr = Ds[nseg]
        else:
            dr = (Ds[i] + Ds[i + 1]).normalized()
        s_ = (Ss[i] - dr * Ss[i].dot(dr)).normalized()
        w = w0 * max(max(0.0, 1 - t ** 1.8) ** 0.75, blunt if not pointed else 0.0)
        if kink and i == kink[0] + 1:
            w *= 0.62
        f = dr.cross(s_).normalized()
        k = 0.004                                # back strip just behind the front one (Roblox culls back faces)
        c = C[i]
        base = len(V)
        V += [tuple(c - s_ * w / 2), tuple(c + s_ * w / 2), tuple(c - s_ * w / 2 - f * k), tuple(c + s_ * w / 2 - f * k)]
        rings.append((base, base + 1, base + 2, base + 3, t, f))
    vv = lambda t: vr[0] + (vr[1] - vr[0]) * t
    for i in range(len(rings) - 1):
        Lf0, Rf0, Lb0, Rb0, t0, _ = rings[i]
        Lf1, Rf1, Lb1, Rb1, t1, _ = rings[i + 1]
        F.append((Lf0, Lf1, Rf1, Rf0))                       # front, normal +F
        UV.append([(sf[0], vv(t0)), (sf[0], vv(t1)), (sf[1], vv(t1)), (sf[1], vv(t0))])
        F.append((Rb0, Rb1, Lb1, Lb0))                       # back, normal -F
        UV.append([(sb[1], vv(t0)), (sb[1], vv(t1)), (sb[0], vv(t1)), (sb[0], vv(t0))])
    Lf0, Rf0, Lb0, Rb0, t0, f = rings[-1]
    if pointed:
        tipc = C[nseg]
        tf = len(V)
        V += [tuple(tipc), tuple(tipc - f * 0.004)]
        F.append((Lf0, tf, Rf0))
        UV.append([(sf[0], vv(t0)), (0.5 * (sf[0] + sf[1]), vv(1.0)), (sf[1], vv(t0))])
        F.append((Rb0, tf + 1, Lb0))
        UV.append([(sb[1], vv(t0)), (0.5 * (sb[0] + sb[1]), vv(1.0)), (sb[0], vv(t0))])
    else:                                                    # broken-off end: a small cap
        F.append((Lf0, Rf0, Rb0, Lb0))
        UV.append([(sf[0], vv(t0)), (sf[1], vv(t0)), (sf[1], vv(t0 - 0.01)), (sf[0], vv(t0 - 0.01))])


def nseg_for(L, bend):
    return int(max(3, min(8, round(1.6 + 0.8 * L + 2.4 * bend))))


def acc_to_object(acc, name):
    me = bpy.data.meshes.new(name)
    acc["V"] = [(x, y, max(z, -0.15)) for x, y, z in acc["V"]]
    me.from_pydata(acc["V"], [], acc["F"])
    me.update()
    uvl = me.uv_layers.new(name="UVMap")
    for poly, uvs in zip(me.polygons, acc["UV"]):
        for li, uv in zip(poly.loop_indices, uvs):
            uvl.data[li].uv = uv
    for p in me.polygons:
        p.use_smooth = True
    return link(bpy.data.objects.new(name, me))


def tri_count(ob):
    return sum(len(p.vertices) - 2 for p in ob.data.polygons)


# ------------------------------------------------------------------ UV + bake (per group, composited by hit masks)
def uv_islands(bm, uvl):
    parent = list(range(len(bm.faces)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i
    for e in bm.edges:
        lf = e.link_faces
        if len(lf) != 2:
            continue
        f1, f2 = lf
        ok = True
        for v in e.verts:
            u1 = next(l[uvl].uv for l in f1.loops if l.vert == v)
            u2 = next(l[uvl].uv for l in f2.loops if l.vert == v)
            if (u1 - u2).length > 1e-5:
                ok = False
                break
        if ok:
            parent[find(f1.index)] = find(f2.index)
    groups = {}
    for f in bm.faces:
        groups.setdefault(find(f.index), []).append(f)
    return list(groups.values())


def scale_islands(ob, fn):
    """fn(island faces) -> scale factor; scales each UV island about its centre."""
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    bm.faces.ensure_lookup_table()
    uvl = bm.loops.layers.uv.active
    for isl in uv_islands(bm, uvl):
        s = fn(isl)
        if abs(s - 1.0) < 1e-6:
            continue
        uvs = [l[uvl].uv for f in isl for l in f.loops]
        c = sum((Vector(u) for u in uvs), Vector((0, 0))) / len(uvs)
        for f in isl:
            for l in f.loops:
                l[uvl].uv = c + (l[uvl].uv - c) * s
    bm.to_mesh(ob.data)
    bm.free()


def multi_edit(objs, fn):
    for o in bpy.context.scene.objects:
        o.select_set(False)
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.select_all(action="SELECT")
    fn()
    bpy.ops.object.mode_set(mode="OBJECT")


def grave_uvs(stone, mound, front_boost=1.55, mound_scale=0.75):
    # smart-project segmentation, then every island re-unwrapped with ABF (a planar projection stretched the texels
    # on tilted faces up to 2x: streaky fracture sides)
    smart_uv(stone, angle=60, margin=0.01)
    only(stone)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.select_all(action="SELECT")
    bpy.ops.uv.seams_from_islands()
    bpy.ops.uv.unwrap(method="ANGLE_BASED", margin=0.01)
    bpy.ops.object.mode_set(mode="OBJECT")
    me = mound.data
    uvl = me.uv_layers.new(name="UVMap")
    for li, lp in enumerate(me.loops):
        co = me.vertices[lp.vertex_index].co
        uvl.data[li].uv = (co.x * 0.2 + 0.5, co.y * 0.2 + 0.5)
    multi_edit([stone, mound], lambda: bpy.ops.uv.average_islands_scale())

    def front(isl):
        n = sum((f.normal * f.calc_area() for f in isl), Vector((0, 0, 0)))
        return front_boost if (n.length > 0 and n.normalized().y < -0.55) else 1.0
    scale_islands(stone, front)
    scale_islands(mound, lambda isl: mound_scale)
    multi_edit([stone, mound], lambda: bpy.ops.uv.pack_islands(rotate=True, scale=True, margin=0.012))
    lim = (RESERVE_PX - 6) / 512.0
    for ob in (stone, mound):
        uvd = ob.data.uv_layers["UVMap"].data
        arr = np.empty(len(uvd) * 2, np.float32)
        uvd.foreach_get("uv", arr)
        arr = arr.reshape(-1, 2)
        arr[:, 0] *= lim
        uvd.foreach_set("uv", arr.ravel())


def img_arr(img, size):
    return np.array(img.pixels[:], dtype=np.float32).reshape(size, size, 4)


def bake_group(lo, his, hide, size, cage, maxray, tag):
    sc = bpy.context.scene
    imgs = {}
    for key, cs in (("normal", "Non-Color"), ("ao", "Non-Color"), ("albedo", "sRGB"), ("rough", "Non-Color"),
                    ("mask", "Non-Color")):
        img = bpy.data.images.new(tag + "_" + key, size, size, alpha=False)
        img.colorspace_settings.name = cs
        imgs[key] = img
    mat = bpy.data.materials.new(tag + "_bake")
    mat.use_nodes = True
    nt = mat.node_tree
    tex = nt.nodes.new("ShaderNodeTexImage")
    lo.data.materials.clear()
    lo.data.materials.append(mat)
    for o in hide:
        o.hide_render = True
    lo.hide_render = False
    for o in sc.objects:
        o.select_set(False)
    for h in his:
        h.hide_render = False
        h.select_set(True)
    lo.select_set(True)
    bpy.context.view_layer.objects.active = lo

    def run(kind, img, **kw):
        tex.image = img
        nt.nodes.active = tex
        bpy.ops.object.bake(type=kind, use_selected_to_active=True, cage_extrusion=cage, max_ray_distance=maxray,
                            margin=0, use_clear=True, **kw)
    run("NORMAL", imgs["normal"], normal_space="TANGENT")
    run("AO", imgs["ao"])
    run("DIFFUSE", imgs["albedo"], pass_filter={"COLOR"})
    run("ROUGHNESS", imgs["rough"])
    saved = []
    for h in his:
        for m in h.data.materials:
            for n in m.node_tree.nodes:
                if n.type == "BSDF_PRINCIPLED":
                    links = [l for l in m.node_tree.links if l.to_socket == n.inputs["Emission Color"]]
                    saved.append((m, n, tuple(n.inputs["Emission Color"].default_value),
                                  n.inputs["Emission Strength"].default_value))
                    for l in links:
                        m.node_tree.links.remove(l)
                    n.inputs["Emission Color"].default_value = (1, 1, 1, 1)
                    n.inputs["Emission Strength"].default_value = 1.0
    run("EMIT", imgs["mask"])
    for m, n, c, s in saved:
        n.inputs["Emission Color"].default_value = c
        n.inputs["Emission Strength"].default_value = s
    for o in hide:
        o.hide_render = False
    out = {k: img_arr(imgs[k], size) for k in ("normal", "ao", "albedo", "rough")}
    out["hit"] = img_arr(imgs["mask"], size)[..., 0] > 0.5
    for img in imgs.values():
        bpy.data.images.remove(img)
    return out


def composite(groups, size, ao_strength):
    hit = np.zeros((size, size), bool)
    fin = {k: np.zeros((size, size, 4), np.float32) for k in ("normal", "ao", "albedo", "rough")}
    for g, aos in zip(groups, ao_strength):
        m = g["hit"] & ~hit
        for k in fin:
            fin[k][m] = g[k][m]
        a = fin["albedo"]
        a[m, :3] *= (1 - aos) + aos * g["ao"][m][:, :1]
        hit |= m
    for k in fin:
        fin[k] = fill_misses(fin[k], hit, iters=40)
        fin[k][..., 3] = 1.0
    n = fin["normal"][..., :3] * 2 - 1
    n /= np.maximum(np.linalg.norm(n, axis=-1, keepdims=True), 1e-6)
    fin["normal"][..., :3] = n * 0.5 + 0.5
    return fin, float(hit.mean())


def to_image(arr, name, cs, path):
    size = arr.shape[0]
    img = bpy.data.images.new(name, size, size, alpha=False)
    img.colorspace_settings.name = cs
    img.pixels[:] = arr.astype(np.float32).ravel()
    save_png(img, path)
    return img


def paint_atlas_region(fin, x0, x1, strips, seed):
    """paint blade strips into columns [x0, x1) of the final maps. strips: list of (variant, back)."""
    size = fin["albedo"].shape[0]
    w = (x1 - x0) // len(strips)
    cols = []
    for i, (vi, back) in enumerate(strips):
        c0 = x0 + i * w
        a, n, r = paint_strip(size, w, VARIANTS[vi], back, seed + i)
        fin["albedo"][:, c0:c0 + w, :3] = a
        fin["normal"][:, c0:c0 + w, :3] = n
        fin["rough"][:, c0:c0 + w, :3] = r[..., None]
        cols.append(((c0 + 1.5) / size, (c0 + w - 1.5) / size))
    return cols


# ------------------------------------------------------------------ graves
def grave_blades(S, M, mo, strips_uv, rng):
    """small dead-grass clumps around the stone base (roots buried in the mound)."""
    acc = dict(V=[], F=[], UV=[])
    for (cx, cy, n) in S["blades"]:
        for b in range(int(round(n * 1.7))):
            x = cx + rng.gauss(0, 0.08)
            y = cy + rng.gauss(0, 0.07)
            z = mound_height(x, y, M, mo, False) - 0.05
            az = math.atan2(cy + 0.15, cx) + rng.uniform(-1.0, 1.0)
            vi = rng.choice([0, 0, 1, 1])        # straw / olive pairs in the reserved strip region
            sfu = strips_uv[vi * 2]
            sbu = strips_uv[vi * 2 + 1]
            L = rng.uniform(0.45, 1.15)
            kink = (1, rng.uniform(1.3, 2.0)) if rng.random() < 0.18 else None
            dr = rng.uniform(0.4, 1.2)
            add_blade(acc, (x, y, z), az, rng.uniform(0.15, 0.85), L, rng.uniform(0.085, 0.12),
                      dr, max(3, min(5, nseg_for(L, dr * L))), rng, kink=kink, twist=rng.uniform(-1.2, 1.2),
                      sf=sfu, sb=sbu)
    return acc_to_object(acc, S["name"] + "_Blades")


def build_grave(key):
    S = spec(key)
    fast = CFG["fast"]
    sc = fresh(samples=32)
    name = S["name"]
    vhi = 0.03 if fast else S["voxel"]
    hi = build_stone(S, vhi, True, name + "_hi")
    hi.data.materials.append(mat_vc("StoneMat"))
    log("stone hi tris", tri_count(hi))
    lo = build_stone(S, 0.036, False, name + "_StoneLo")
    n0 = len(lo.data.polygons)
    dec = lo.modifiers.new("Dec", "DECIMATE")
    dec.ratio = min(1.0, S["lo_target"] / (2.0 * n0))
    lo.modifiers.new("Tri", "TRIANGULATE")
    apply_mods(lo)
    bm = bmesh.new()
    bm.from_mesh(lo.data)
    bmesh.ops.delete(bm, geom=[f for f in bm.faces if all(v.co.z < -0.06 for v in f.verts)], context="FACES")
    bm.to_mesh(lo.data)
    bm.free()
    for p in lo.data.polygons:
        p.use_smooth = True
    log("stone lo tris", tri_count(lo))
    M = S["mound"]
    mhi = mound_mesh(name + "_mound_hi", M, S["seed"], True, 70 if fast else 150, 180 if fast else 360)
    mhi.data.materials.append(mat_vc("SoilMat"))
    mlo = mound_mesh(name + "_MoundLo", M, S["seed"], False, 7, 40)
    # drop the coarse mound faces hidden inside the stone foot
    y0 = min(p["y0"] for p in S["parts"])
    y1 = max(p["y1"] for p in S["parts"])
    hw = max(max(abs(x) for x, z in p["poly"]) for p in S["parts"][:1])
    bm = bmesh.new()
    bm.from_mesh(mlo.data)
    bmesh.ops.delete(bm, geom=[f for f in bm.faces if all(abs(v.co.x) < hw - 0.18 and y0 + 0.16 < v.co.y < y1 - 0.16
                                                          for v in f.verts)], context="FACES")
    bm.to_mesh(mlo.data)
    bm.free()
    for p in mlo.data.polygons:
        p.use_smooth = True
    log("mound lo tris", tri_count(mlo), "mound hi faces", len(mhi.data.polygons))
    grave_uvs(lo, mlo)
    size = 512
    sc.cycles.samples = 32
    sc.world.light_settings.distance = 0.6
    g1 = bake_group(lo, [hi], [mlo], size, 0.12, 0.3, name + "_stone")
    g2 = bake_group(mlo, [mhi], [lo], size, 0.1, 0.25, name + "_mound")
    fin, cover = composite([g1, g2], size, [0.6, 0.5])
    strips = [(0, False), (0, True), (4, False), (4, True)]
    suv = paint_atlas_region(fin, RESERVE_PX, 512, strips, S["seed"])
    blades = grave_blades(S, M, offsets(S["seed"] + 101), suv, random.Random(S["seed"] + 5))
    imgs = {}
    for k, cs in (("albedo", "sRGB"), ("normal", "Non-Color"), ("rough", "Non-Color"), ("ao", "Non-Color")):
        imgs[k] = to_image(fin[k], name + "_" + k, cs, os.path.join(MAPS, name + "_" + k + ".png"))
    # join stone + mound + blades into the one game mesh
    for o in sc.objects:
        o.select_set(False)
    for o in (lo, mlo, blades):
        o.select_set(True)
    bpy.context.view_layer.objects.active = lo
    parts_tris = dict(stone=tri_count(lo), mound=tri_count(mlo), blades=tri_count(blades))
    bpy.ops.object.join()
    lo.name = name
    for p in lo.data.polygons:
        p.material_index = 0
    lo.data.name = name
    pbr_material(lo, name + "_PBR", imgs)
    lo.data.materials[0].use_backface_culling = True
    for o in (hi, mhi):
        o.hide_render = True
        o.hide_viewport = True
    co = np.array([v.co for v in lo.data.vertices])
    rep = dict(name=name, tris=tri_count(lo), parts_tris=parts_tris, texture=size, uv_cover=round(cover, 3),
               bbox_min=[round(float(v), 3) for v in co.min(0)], bbox_max=[round(float(v), 3) for v in co.max(0)],
               size_blender_xyz=[round(float(v), 3) for v in co.max(0) - co.min(0)])
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, name + ".blend"))
    if not fast:
        rep["export"] = export_fbx([lo], os.path.join(CDIMP, "Halloween_" + name + ".fbx"))
    with open(os.path.join(OUT, name + ".json"), "w") as f:
        json.dump(rep, f, indent=1)
    log("done", rep)
    return rep


# ------------------------------------------------------------------ dead-grass tufts
TUFT = {
    "A": dict(name="DeadGrass_A", seed=51, n=(48, 33, 14), flat=8, r0=0.4, Lmax=3.2, w=(0.11, 0.17), H=3.0, R=2.0,
              spread=0.9),
    "B": dict(name="DeadGrass_B", seed=67, n=(48, 35, 12), flat=6, r0=0.27, Lmax=2.6, w=(0.1, 0.15), H=2.5, R=1.25,
              spread=0.6),
}


def build_grass(key):
    """a chunky fountain tuft: upright core, arching middle, flopped outer blades, a few lying broken ones."""
    T = TUFT[key]
    sc = fresh(samples=16)
    rng = random.Random(T["seed"])
    acc = dict(V=[], F=[], UV=[])
    size = 512
    W = size // 16
    strip_uv = [((k * W + 1.5) / size, ((k + 1) * W - 1.5) / size) for k in range(16)]
    weights = [0.26, 0.06, 0.17, 0.16, 0.13, 0.11, 0.02, 0.09]
    Lm = T["Lmax"]
    jobs = [("core", i) for i in range(T["n"][0])] + [("mid", i) for i in range(T["n"][1])] +            [("out", i) for i in range(T["n"][2])] + [("flat", i) for i in range(T["flat"])]
    total = len(jobs)
    # review round 1: long arching / flopped blades get 8-10 segments (<= ~7 deg per joint, even droop profile, small
    # twist + wobble); short upright core blades 3-4 segments; snapped blades keep ONE sharp fold
    for kind, _ in jobs:
        az0 = rng.uniform(0, 2 * math.pi)
        if kind == "core":
            rr = abs(rng.gauss(0, T["r0"] * 0.35))
            tilt, L, bend = rng.uniform(0.05, 0.38), (0.35 + 0.65 * rng.random() ** 1.6) * Lm, rng.uniform(0.15, 0.42)
        elif kind == "mid":
            rr = rng.uniform(0.25, 0.75) * T["r0"]
            tilt, L, bend = rng.uniform(0.3, 0.6), rng.uniform(0.62, 0.9) * Lm, rng.uniform(0.6, 0.95)
        elif kind == "out":
            rr = rng.uniform(0.6, 1.0) * T["r0"]
            tilt, L, bend = rng.uniform(0.65, 0.9), rng.uniform(0.5, 0.72) * Lm * T["spread"] ** 0.5, rng.uniform(0.55, 0.95)
        else:
            rr = rng.uniform(0.5, 1.0) * T["r0"]
            tilt, L, bend = rng.uniform(1.2, 1.42), rng.uniform(0.3, 0.5) * Lm * T["spread"], rng.uniform(0.05, 0.25)
        if kind in ("mid", "out"):
            tilt *= T["spread"] ** 0.5
            bend *= 0.6 + 0.4 * T["spread"]
        x, y = rr * math.cos(az0), rr * math.sin(az0)
        az = az0 + rng.uniform(-0.45, 0.45)
        if kind == "flat":
            vi = rng.choice([0, 2, 4, 5])
        else:
            vi = rng.choices(range(8), weights=weights)[0]
            if kind == "core" and rng.random() < 0.35:
                vi = rng.choice([3, 7])
        longb = kind in ("mid", "out")
        nseg = arc_nseg(bend) if longb else (5 if kind == "flat" else (3 if L < 1.2 else 4))
        kink, blunt = None, 0.0
        q = rng.random()
        if kind in ("mid", "core") and q < 0.14:
            kink = (rng.randint(2, nseg - 3) if longb else rng.randint(1, nseg - 2), rng.uniform(1.5, 2.3))
        elif kind != "flat" and q < 0.22:
            blunt = rng.uniform(0.35, 0.55)
            L *= rng.uniform(0.45, 0.7)
            nseg = max(6, nseg - 2) if longb else max(3, nseg - 1)
        droop = bend / max(L, 0.3)
        w = rng.uniform(*T["w"]) * (0.8 if kind == "flat" else (0.9 if longb else 0.88))
        add_blade(acc, (x, y, -0.06), az, tilt, L, w, droop, nseg, rng, kink=kink,
                  twist=rng.uniform(-0.45, 0.45) if longb else rng.uniform(-0.35, 0.35), blunt=blunt,
                  wob=0.022 if longb else 0.03, prof=(0.75, 0.5), sf=strip_uv[vi], sb=strip_uv[8 + vi])
    ob = acc_to_object(acc, T["name"])
    co = np.array([v.co for v in ob.data.vertices])
    s = T["H"] / (co[:, 2].max())          # uniform: the generator is tuned to the footprint already
    reach = max(np.abs(co[:, 0]).max(), np.abs(co[:, 1]).max()) * s
    sxy = s * min(1.0, max(0.9, T["R"] / reach))
    for v in ob.data.vertices:
        v.co = Vector((v.co.x * sxy, v.co.y * sxy, v.co.z * s))
    alb = np.zeros((size, size, 4), np.float32)
    nrm = np.zeros((size, size, 4), np.float32)
    rgh = np.zeros((size, size, 4), np.float32)
    for k in range(16):
        a, n, r = paint_strip(size, W, VARIANTS_T[k % 8], k >= 8, T["seed"] * 10 + k, style=2)
        alb[:, k * W:(k + 1) * W, :3] = a
        nrm[:, k * W:(k + 1) * W, :3] = n
        rgh[:, k * W:(k + 1) * W, :3] = r[..., None]
    for arr in (alb, nrm, rgh):
        arr[..., 3] = 1.0
    imgs = {"albedo": to_image(alb, T["name"] + "_albedo", "sRGB", os.path.join(MAPS, T["name"] + "_albedo.png")),
            "normal": to_image(nrm, T["name"] + "_normal", "Non-Color", os.path.join(MAPS, T["name"] + "_normal.png")),
            "rough": to_image(rgh, T["name"] + "_rough", "Non-Color", os.path.join(MAPS, T["name"] + "_rough.png"))}
    pbr_material(ob, T["name"] + "_PBR", imgs)
    ob.data.materials[0].use_backface_culling = True   # = Roblox MeshPart (single-sided): front / back strips
    co = np.array([v.co for v in ob.data.vertices])
    rep = dict(name=T["name"], blades=total, tris=tri_count(ob), texture=size, scale=[round(float(sxy), 3), round(float(s), 3)],
               bbox_min=[round(float(v), 3) for v in co.min(0)], bbox_max=[round(float(v), 3) for v in co.max(0)],
               size_blender_xyz=[round(float(v), 3) for v in co.max(0) - co.min(0)])
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, T["name"] + ".blend"))
    if not CFG["fast"]:
        rep["export"] = export_fbx([ob], os.path.join(CDIMP, "Halloween_" + T["name"] + ".fbx"))
    with open(os.path.join(OUT, T["name"] + ".json"), "w") as f:
        json.dump(rep, f, indent=1)
    log("done", rep)
    return rep


# ------------------------------------------------------------------ review (imports the exported FBX files)
ALL = ["Grave_A", "Grave_B", "Grave_C", "DeadGrass_A", "DeadGrass_B"]


def import_asset(name, src):
    before = set(bpy.data.objects)
    if src == "fbx":
        bpy.ops.import_scene.fbx(filepath=os.path.join(CDIMP, "Halloween_" + name + ".fbx"))
        obs = [o for o in bpy.data.objects if o not in before and o.type == "MESH"]
        for o in obs:                 # the FBX is written in Roblox units (global_scale 0.01): back to studs
            o.scale = o.scale * 100.0
            o.location = o.location * 100.0
            for m in o.data.materials:
                m.use_backface_culling = True     # Roblox MeshParts are single-sided
    else:
        with bpy.data.libraries.load(os.path.join(OUT, name + ".blend")) as (src_d, dst):
            dst.objects = [name]
        obs = [o for o in dst.objects]
        for o in obs:
            link(o)
    for o in bpy.data.objects:
        if o not in before and o.type != "MESH":
            bpy.data.objects.remove(o)
    ob = obs[0]
    bpy.context.view_layer.update()
    return ob


def review(src="fbx", tag=""):
    sc = fresh(samples=16)
    review_setup(res=(1600, 1000))
    g = mat_noise("Grass", lin((96, 168, 62)), lin((74, 140, 48)), nscale=0.35, detail=6, rough=0.9, lo=0.3, hi=0.7)
    bpy.ops.mesh.primitive_plane_add(size=160)
    bpy.context.active_object.data.materials.append(g)
    bm = bmesh.new()
    bmesh.ops.create_circle(bm, cap_ends=True, segments=96, radius=11.0)
    bed = obj_from_bm(bm, "Bed")
    bed.location.z = 0.004
    bed.data.materials.append(mat_noise("BedSoil", lin((112, 82, 56)), lin((88, 64, 44)), nscale=1.2, detail=6,
                                        rough=0.95, lo=0.3, hi=0.7))
    lay = {"Grave_A": ((0.0, 0.0), 0), "Grave_B": ((-5.2, 1.4), 12), "Grave_C": ((5.0, 1.0), -10),
           "DeadGrass_A": ((-2.9, -2.4), 0), "DeadGrass_B": ((2.7, -2.7), 40)}
    obs = {}
    info = {}
    for nm in ALL:
        ob = import_asset(nm, src)
        info[nm] = dict(dims=[round(v, 3) for v in ob.dimensions], scale=[round(v, 4) for v in ob.scale],
                        loc=[round(v, 3) for v in ob.location], rot=[round(v, 3) for v in ob.rotation_euler])
        (x, y), rz = lay[nm]
        ob.location = (x, y, 0)
        ob.rotation_euler.z += math.radians(rz)
        obs[nm] = ob
    extra = import_asset("DeadGrass_B", src)
    extra.location = (-7.6, -1.2, 0)
    extra.rotation_euler.z += 1.3
    extra2 = import_asset("DeadGrass_A", src)
    extra2.location = (7.8, -1.8, 0)
    extra2.rotation_euler.z += 2.1
    bpy.context.view_layer.update()
    out = WIP if (CFG["fast"] or tag) else OUT
    shots = []
    tgt = Vector((0, 0, 1.7))
    shots.append(shoot(os.path.join(out, "review_25studs%s.png" % tag), tgt, (0.0, -1.0, 0.32), 25.0, lens=50))
    shots.append(shoot(os.path.join(out, "review_50studs%s.png" % tag), tgt, (0.25, -1.0, 0.42), 50.0, lens=50))
    shots.append(shoot(os.path.join(WIP, "review_back%s.png" % tag), tgt, (-0.3, 1.0, 0.35), 25.0, lens=50))
    shots.append(shoot(os.path.join(WIP, "review_34%s.png" % tag), tgt, (0.9, -0.8, 0.45), 22.0, lens=50))
    for nm, d in (("Grave_A", (0.15, -1.0, 0.18)), ("Grave_B", (-0.25, -1.0, 0.22)), ("Grave_C", (0.2, -1.0, 0.3))):
        c = obs[nm].location + Vector((0, 0, 2.0))
        shots.append(shoot(os.path.join(out if nm == "Grave_A" else WIP, "review_close_%s%s.png" % (nm, tag)), c,
                           Matrix.Rotation(obs[nm].rotation_euler.z, 3, "Z") @ Vector(d), 9.0, lens=50))
    gc = obs["DeadGrass_A"].location + Vector((0, 0, 1.2))
    shots.append(shoot(os.path.join(out, "review_close_grass%s.png" % tag), gc + Vector((1.3, 0, 0)),
                       (0.2, -1.0, 0.35), 8.5, lens=50))
    return dict(shots=shots, info=info)


def ground_scene():
    sc = fresh(samples=16)
    review_setup(res=(1600, 1000))
    g = mat_noise("Grass", lin((96, 168, 62)), lin((74, 140, 48)), nscale=0.35, detail=6, rough=0.9, lo=0.3, hi=0.7)
    bpy.ops.mesh.primitive_plane_add(size=160)
    bpy.context.active_object.data.materials.append(g)
    bm = bmesh.new()
    bmesh.ops.create_circle(bm, cap_ends=True, segments=96, radius=11.0)
    bed = obj_from_bm(bm, "Bed")
    bed.location.z = 0.004
    bed.data.materials.append(mat_noise("BedSoil", lin((112, 82, 56)), lin((88, 64, 44)), nscale=1.2, detail=6,
                                        rough=0.95, lo=0.3, hi=0.7))
    return sc


def preview(name, src="blend"):
    ground_scene()
    ob = import_asset(name, src)
    bpy.context.view_layer.update()
    h = ob.dimensions.z
    c = Vector((0, 0, h * 0.5))
    out = []
    for tag, d, dist in (("front25", (0.0, -1.0, 0.3), 25.0), ("close", (0.12, -1.0, 0.15), max(h * 2.1, 5.0)),
                         ("34", (0.9, -0.7, 0.4), max(h * 2.2, 5.0)), ("back", (-0.4, 1.0, 0.35), max(h * 2.2, 5.0)),
                         ("side", (1.0, 0.05, 0.2), max(h * 2.2, 5.0))):
        out.append(shoot(os.path.join(WIP, "pv_%s_%s.png" % (name, tag)), c, d, dist, lens=50))
    return out


def verify():
    out = {}
    for nm in ALL:
        bpy.ops.wm.read_factory_settings(use_empty=True)
        bpy.ops.import_scene.fbx(filepath=os.path.join(CDIMP, "Halloween_" + nm + ".fbx"))
        r = []
        for o in [o for o in bpy.context.scene.objects if o.type == "MESH"]:
            me = o.data
            co = np.array([o.matrix_world @ v.co for v in me.vertices])
            texs = []
            for m in me.materials:
                texs += [f"{n.image.name} {n.image.size[0]}x{n.image.size[1]} packed={bool(n.image.packed_file)}"
                         for n in m.node_tree.nodes if n.type == "TEX_IMAGE" and n.image]
            r.append(dict(name=o.name, tris=sum(len(p.vertices) - 2 for p in me.polygons),
                          dims=[round(v, 3) for v in o.dimensions], world_min=[round(float(v), 3) for v in co.min(0)],
                          world_max=[round(float(v), 3) for v in co.max(0)], textures=texs))
        out[nm] = r
    return out


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    if "fast" in argv:
        CFG["fast"] = True
        argv.remove("fast")
    os.makedirs(MAPS, exist_ok=True)
    os.makedirs(WIP, exist_ok=True)
    rep = {}
    i = 0
    while i < len(argv):
        st = argv[i]
        if st == "grave":
            rep["grave_" + argv[i + 1]] = build_grave(argv[i + 1])
            i += 2
        elif st == "grass":
            rep["grass_" + argv[i + 1]] = build_grass(argv[i + 1])
            i += 2
        elif st == "review":
            rep["review"] = review()
            i += 1
        elif st == "review_blend":
            rep["review"] = review("blend", "_blend")
            i += 1
        elif st == "preview":
            rep["preview"] = preview(argv[i + 1], argv[i + 2] if i + 2 < len(argv) and argv[i + 2] in ("fbx", "blend") else "blend")
            i += 3 if (i + 2 < len(argv) and argv[i + 2] in ("fbx", "blend")) else 2
        elif st == "verify":
            rep["verify"] = verify()
            i += 1
        else:
            raise SystemExit("unknown step " + st)
    print("GRAVE_REPORT " + json.dumps(rep, default=str))
