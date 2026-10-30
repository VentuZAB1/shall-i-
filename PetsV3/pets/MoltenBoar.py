# Molten Boar (Magma egg #1) - FIERCE style (2026-10-09, FIERCE_PLAN "the volcano hog"): a real wild boar built from
# tapered blocks under a Roblox stud skin. Wedge anatomy (massive head + shoulders, small hips, withers 1.0 / rump 0.85,
# BL 1.3), a molten orange core showing through the gaps between rock armour shells and across the belly, a conical
# snout ending in a disc, upturned ivory tusks, small narrow orange eyes in rock sockets, a bristle crest of two-tone
# spikes (Mane bone), short jointed legs on black cloven hooves with dewclaws, a short tail with a magma tuft.
# Old chibi version: _tools/chibi_specs/MoltenBoar.py
import math
from mathutils import Vector, Euler

DISPLAY = "Molten Boar"
MOTION = "Walk"
RIG = "quad"
HEIGHT = 6.6                 # withers (~1.03 of 1.21 model units) = ~5.6 studs at x1 (HEIGHT rule 2026-10-09)

ROCK = (112, 100, 98)        # rock armour (Roblox renders ~0.6x darker -> dark volcanic rock in game)
ROCK_T = (152, 138, 132)     # lighter rock: crest bases, brow shelves, forehead plate
DARK = (62, 54, 54)          # lower legs, ear backs
HOOF = (20, 18, 24)
MAGMA = (255, 110, 20)       # the ONE accent: core seams, belly, eyes, crest tips, ear lining
MAGMA_HOT = (255, 214, 120)
TUSK = (226, 214, 190)
SNOUT = (156, 104, 98)
BLACK = (14, 14, 22)
MOUTH = (86, 18, 30)

PITCH = 0.041                # stud pitch = 0.042 x (U / U_raiju), U = model height / HEIGHT (1.21 / 6.6 vs 1.498 / 8)

# leg joints (left side): hip/shoulder, knee/elbow, ankle/wrist, hoof centre
LEGS = {"F": ((0.19, -0.38, 0.68), (0.19, -0.31, 0.37), (0.19, -0.37, 0.115), (0.19, -0.405, 0.04)),
        "B": ((0.115, 0.42, 0.68), (0.115, 0.31, 0.40), (0.115, 0.47, 0.17), (0.115, 0.425, 0.04))}
TAILP = [(0, 0.62, 0.80), (0, 0.69, 0.68), (0, 0.72, 0.56)]


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


def prof(b, lz):
    """half extents (x, y) and the y centre offset of a tapered (top-shifted) block at local height lz"""
    t = (lz / b.h.z + 1) / 2
    fx = b.bot[0] + (b.top[0] - b.bot[0]) * t
    fy = b.bot[1] + (b.top[1] - b.bot[1]) * t
    return b.h.x * fx, b.h.y * fy, b.ts[1] * t


def shell(B, b, y0, y1, za, color, pad=0.024, bone=None, rnd=0.30, s0=0.0, s1=0.0, lift=0.0):
    """rock armour shell over body block b: local y range [y0, y1], local z from za to the top, following the tapers
    (the orange core shows below it and in the gaps between shells)"""
    xa, ya, oa = prof(b, za)
    xb, yb, ob = prof(b, b.h.z)
    zb = b.h.z + pad + lift
    lo_a, hi_a = max(y0 + oa, oa - ya - pad), min(y1 + oa, oa + ya + pad)
    lo_b, hi_b = max(y0 + ob + s0, ob - yb - pad), min(y1 + ob + s1, ob + yb + pad)
    cy, hy = (lo_a + hi_a) / 2, (hi_a - lo_a) / 2
    hx = xa + pad
    c = b.world(Vector((0, cy, (za + zb) / 2)))
    return B.add(c, (hx, hy, (zb - za) / 2), color, bone or b.bone, R=b.R, top=((xb + pad) / hx, (hi_b - lo_b) / 2 / hy),
                 top_shift=(0, (lo_b + hi_b) / 2 - cy), rnd=rnd)


def side_pt(b, s, ly, lz, off=0.006):
    """point on the +-x flank of tapered block b at local (ly, lz) + the flank normal"""
    hx, _, oy = prof(b, lz)
    p = b.world(Vector((s * (hx + off), ly + oy, lz)))
    dx = b.h.x * (b.top[0] - b.bot[0]) / (2 * b.h.z)
    n = (b.R @ Vector((s, 0, -dx))).normalized()
    return p, n


def crack(B, b, s, pts, w=0.05, color=MAGMA, off=0.006, bone=None):
    """zig-zag magma crack inlay on the flank of a tapered block; pts = [(ly, lz)] local"""
    Q = [side_pt(b, s, y, z, off) for y, z in pts]
    for i, ((a, n), (c, _)) in enumerate(zip(Q, Q[1:])):
        B.bar(a, c, n, w, 0.012, color, bone or b.bone, studs=[], bevel=0.004,
              top=(1, 0.2) if i == len(Q) - 2 else (1, 1))


def spike2(B, base, d, L, w, bone, col=DARK, tip=MAGMA, root=0.0):
    """two-tone crest spike laid back along the spine: long base along the back, thin across, last 40 % magma.
    root = extra length buried in the body (so a crest flare never opens a gap at the base)"""
    import blockkit as bk
    d = Vector(d).normalized()
    base = Vector(base) - d * root
    L = L + root
    for b0, ln, hx, hy, c, tp in ((base, 0.66 * L, w * 0.42, w, col, (0.62, 0.50)),
                                  (base + d * (0.58 * L), 0.42 * L, w * 0.30, w * 0.52, tip, (0.30, 0.10))):
        B.add(b0 + d * (ln / 2), (hx, hy, ln / 2), c, bone, R=bk.frame_from(b0, b0 + d, (1, 0, 0)), top=tp,
              studs=[], role="limb")


def model(k):
    import blockkit as bk
    B = bk.Blocks(k, seed=101, tier=3, plates=False)
    # ---------------- torso: molten core (ribcage tapering underneath, sloped tuck, narrow waist, smaller hips)
    # (wedge: the ribcage tips forward so the withers are the high point and the belly line rises backwards)
    rib = B.add((0, -0.24, 0.72), (0.25, 0.36, 0.29), MAGMA, "Chest", rot=(-6, 0, 0), bot=(0.66, 0.56),
                top=(0.86, 0.80), top_shift=(0, 0.07), rnd=0.30)
    B.seg((0, -0.10, 0.475), (0, 0.28, 0.62), 0.13, 0.08, ROCK, "Spine", top=(0.85, 0.8), side=(1, 0, 0))   # tuck
    B.add((0, -0.26, 0.425), (0.11, 0.17, 0.022), MAGMA, "Chest", bot=(0.8, 0.9), studs=[])          # magma belly
    B.seg((0, -0.10, 0.403), (0, 0.27, 0.547), 0.085, 0.024, MAGMA, "Spine", side=(1, 0, 0), top=(0.8, 1), ext=0.03)
    waist = B.add((0, 0.12, 0.74), (0.185, 0.21, 0.15), MAGMA, "Spine", rot=(-6, 0, 0), bot=(0.72, 0.70),
                  top=(0.92, 1), rnd=0.30)
    hips = B.add((0, 0.42, 0.70), (0.18, 0.21, 0.16), MAGMA, "Spine", rot=(-10, 0, 0), bot=(0.78, 0.80),
                 top=(0.74, 0.72), top_shift=(0, -0.04), rnd=0.30)
    # rock armour shells (magma shows in the gaps, the waist band and along the underside)
    # (seams lean back like overlapping plates; the withers shell stands highest)
    # 4 shells: shoulder | rib | waist band | rump, with 0.055 magma gaps; shells reach ~0.03 above the underside
    for b, y0, y1, za, r, s0, s1, lift, teeth in (
            (rib, -0.40, -0.088, -0.26, 0.42, 0.0, 0.07, 0.025, (-0.27, -0.16)),
            (rib, -0.058, 0.36, -0.25, 0.42, 0.07, 0.04, 0.0, (-0.02, 0.10)),
            (waist, -0.065, 0.13, -0.135, 0.42, 0.085, 0.03, 0.0, (0.06,)),
            (hips, -0.135, 0.30, -0.13, 0.50, 0.03, 0.0, -0.02, (-0.06, 0.08))):
        shell(B, b, y0, y1, za, ROCK, rnd=r, s0=s0, s1=s1, lift=lift)           # shoulder / rib / rump shells
        # jagged rock teeth along the shell's lower edge, hanging over the magma
        for s in (1, -1):
            for i, ly in enumerate(teeth):
                p0, nrm = side_pt(b, s, ly, za + 0.035, off=0.030)
                p1 = p0 + Vector((0, 0.015, -0.11 if i % 2 == 0 else -0.085))
                B.add((p0 + p1) / 2, (0.014, 0.042, (p1 - p0).length / 2), ROCK, b.bone,
                      R=bk.frame_from(p0, p1, nrm), top=(1, 0.10), role="detail", bevel=0.006)
    # magma flank cracks running out of the gaps
    for s in (1, -1):
        crack(B, rib, s, ((-0.20, 0.10), (-0.15, -0.01), (-0.22, -0.07), (-0.16, -0.17)), w=0.036, off=0.03)
        crack(B, hips, s, ((0.0, 0.06), (0.06, 0.0), (0.02, -0.05), (0.08, -0.11)), w=0.034, off=0.03)
    # ---------------- neck: thick, short (boars barely have one)
    B.seg((0, -0.50, 0.71), (0, -0.74, 0.70), 0.185, 0.17, ROCK, "Neck", ext=0.04, top=(0.92, 0.95))
    # nape hump: the boar's straight top line rising from the crown to the withers (the wedge)
    B.seg((0, -0.70, 0.80), (0, -0.48, 0.915), 0.165, 0.10, ROCK, "Neck", top=(1.08, 1.0), ext=0.03, ext1=0.02,
          rnd=0.40)
    # ---------------- head: wedge skull (pivot at the throat), conical snout ending in a disc, tusks
    head = B.add((0, -0.83, 0.70), (0.16, 0.15, 0.165), ROCK, "Head", top=(0.76, 0.70), bot=(0.88, 0.92),
                 top_shift=(0, 0.04))
    B.seg((0, -0.78, 0.835), (0, -1.02, 0.72), 0.075, 0.03, ROCK_T, "Head", top=(0.75, 1), ext=0.02)  # forehead ridge
    snout = B.seg((0, -0.92, 0.655), (0, -1.15, 0.565), 0.10, 0.082, ROCK, "Head", top=(0.76, 0.80), ext=0.04)
    tip = snout.world(Vector((0, 0, snout.h.z)))
    B.add(tip, (0.080, 0.068, 0.022), SNOUT, "Head", R=snout.R, rnd=0.45, studs=[])                    # snout disc
    for s in (1, -1):
        B.add(snout.world(Vector((s * 0.032, 0.004, snout.h.z + 0.018))), (0.010, 0.015, 0.006), BLACK, "Head",
              R=snout.R @ Euler((0, 0, math.radians(s * 20)), "XYZ").to_matrix(), studs=[], role="detail",
              bevel=0.003)                                                                      # nostrils
    # lower jaw (champs in the roar) + mouth + lower teeth
    B.seg((0, -0.84, 0.535), (0, -1.10, 0.505), 0.085, 0.032, ROCK, "Jaw", top=(0.80, 0.9), ext=0.02)
    B.seg((0, -0.88, 0.566), (0, -1.08, 0.540), 0.062, 0.006, MOUTH, "Jaw", studs=[], role="detail", bevel=0.003)
    for s in (1, -1):
        B.spike((s * 0.055, -1.07, 0.55), (0, -0.2, 1), 0.045, 0.012, TUSK, "Jaw")
    # upturned tusks: out of the lip, out + up, then curling back
    for s in (1, -1):
        b0, b1 = Vector((s * 0.075, -1.065, 0.535)), Vector((s * 0.165, -1.100, 0.625))
        B.seg(b0, b1, 0.030, 0.030, TUSK, "Head", ext=0.02, studs=[], role="limb")
        b2 = b1 + Vector((s * 0.035, 0.03, 0.10))
        B.seg(b1, b2, 0.028, 0.028, TUSK, "Head", ext=0.02, top=(0.85, 0.85), studs=[], role="limb")
        B.spike(b2, (s * 0.05, 0.45, 0.9), 0.07, 0.024, TUSK, "Head", top=(0.15, 0.15), role="limb")
    # narrow fierce eyes in rock sockets (black socket + orange slit + hot spot on the outer half) + heavy brows
    for s in (1, -1):
        rot = (0, -s * 18, s * 22)
        B.add((s * 0.088, -0.988, 0.775), (0.050, 0.010, 0.024), BLACK, "Head", rot=rot, studs=[], role="detail",
              bevel=0.004)
        B.add((s * 0.090, -0.995, 0.775), (0.040, 0.007, 0.013), MAGMA, "Head", rot=rot, studs=[], role="detail",
              bevel=0.003)
        B.add((s * 0.097, -0.999, 0.777), (0.017, 0.004, 0.006), MAGMA_HOT, "Head", rot=rot, studs=[],
              role="detail", bevel=0.002)
        B.add((s * 0.080, -0.968, 0.818), (0.066, 0.032, 0.026), ROCK_T, "Head", rot=(0, -s * 20, s * 22),
              role="detail", bevel=0.01)
    # cheek bristles: swept-back rock spikes from the jowls
    for s in (1, -1):
        for z, dz, L, w in ((0.585, -0.40, 0.12, 0.032), (0.645, -0.05, 0.15, 0.036), (0.71, 0.30, 0.11, 0.03)):
            B.spike((s * 0.135, -0.80, z), (s * 0.40, 0.92, dz), L, w, ROCK, "Head", top=(0.12, 0.35))
    # ears: pointed, up and out, magma lining
    for s, side in ((1, "L"), (-1, "R")):
        R = Euler((math.radians(-22), math.radians(s * 10), math.radians(-s * 28)), "XYZ").to_matrix()
        root = Vector((s * 0.105, -0.74, 0.82))
        ear = B.add(root + R @ Vector((0, 0, 0.085)), (0.052, 0.022, 0.09), DARK, "Ear_" + side, R=R, top=(0.12, 0.5))
        B.add(ear.world((0, -0.024, -0.01)), (0.032, 0.006, 0.062), MAGMA, "Ear_" + side, R=R, top=(0.12, 1),
              studs=[], role="detail", bevel=0.004)
    # ---------------- bristle crest: head -> mid back, laid back, shrinking toward the tail
    # (2 on the Neck end short of the Mane spikes so a head lift never drives them into the crest behind)
    for y, z, L, w, ang, bone in ((-0.665, 0.90, 0.15, 0.062, 60, "Neck"), (-0.585, 0.945, 0.16, 0.072, 36, "Neck"),
                                  (-0.37, 1.03, 0.31, 0.095, 50, "Mane"), (-0.24, 1.02, 0.29, 0.09, 53, "Mane"),
                                  (-0.11, 1.005, 0.24, 0.08, 57, "Mane"), (0.04, 0.95, 0.18, 0.07, 62, "Spine"),
                                  (0.18, 0.925, 0.13, 0.06, 66, "Spine")):
        d = (0, math.sin(math.radians(ang)), math.cos(math.radians(ang)))
        spike2(B, (0, y, z - 0.02), d, L, w, bone, col=ROCK if bone == "Neck" else DARK,
               root=0.06 if bone == "Mane" else 0.0)
    # ---------------- legs: rock shoulder / thigh, slim lower legs, black cloven hooves with dewclaws
    for s, side in ((1, "L"), (-1, "R")):
        for fb in ("F", "B"):
            H, K, A, P = (X(p, s) for p in LEGS[fb])
            leg, shin, foot = "Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side
            if fb == "F":
                up = B.seg(H + Vector((0, 0, 0.10)), K, 0.085, 0.12, ROCK, leg, ext=0.0, ext1=0.03, top=(0.75, 0.62))
                B.seg(K, A, 0.054, 0.060, ROCK, shin, top=(0.80, 0.82), ext=0.03, ext1=0.0)
                B.seg(K + (A - K) * 0.55, A, 0.050, 0.054, DARK, shin, top=(0.92, 0.92), ext=0.0, ext1=0.035)  # sock
            else:
                up = B.seg(H + Vector((0, 0.02, 0.10)), K, 0.085, 0.14, ROCK, leg, bot=(0.85, 1), top=(0.72, 0.62),
                           ext=0.0, ext1=0.03)                                                     # ham
                B.seg(K, A, 0.052, 0.062, ROCK, shin, top=(0.80, 0.80), ext=0.03, ext1=0.02)
                B.seg(A, P + Vector((0, 0.01, 0.05)), 0.042, 0.044, DARK, foot, ext=0.03)          # hock -> hoof
            # cloven hoof: two pointed black toes + two dewclaws behind
            for gx in (-0.026, 0.026):
                B.add((P.x + gx, P.y - 0.01, P.z), (0.024, 0.048, 0.04), HOOF, foot, top=(0.8, 0.62),
                      top_shift=(0, 0.012), role="limb", studs=[])
                B.spike((P.x + gx * 1.3, P.y + 0.045, P.z + 0.07), (0, 0.5, -1), 0.05, 0.012, HOOF, foot)
    # magma cracks on the shoulder and ham armour
    for s in (1, -1):
        for fb, bone in (("F", "Leg_F"), ("B", "Leg_B")):
            H, K, _, _ = (X(p, s) for p in LEGS[fb])
            n = Vector((s, 0, 0))
            hw = 0.085
            pts = [H + (K - H) * t + Vector((s * (hw + 0.004), dy, 0.10 * (1 - t))) for t, dy in
                   ((0.0, -0.02), (0.30, 0.03), (0.52, -0.025), (0.78, 0.02))]
            for i, (a, b) in enumerate(zip(pts, pts[1:])):
                B.bar(a, b, n, 0.034, 0.010, MAGMA, bone + ("L" if s > 0 else "R"), studs=[], bevel=0.004,
                      top=(1, 0.2) if i == 2 else (1, 1))
    # ---------------- short tail hanging down with a flat magma tuft
    T = [Vector(p) for p in TAILP]
    B.seg(T[0], T[1], 0.028, 0.03, ROCK, "Tail1", ext=0.04)
    B.seg(T[1], T[2], 0.022, 0.024, DARK, "Tail2", ext=0.01)
    B.seg(T[2] + Vector((0, -0.01, 0.03)), T[2] + Vector((0, 0.03, -0.12)), 0.012, 0.045, MAGMA, "Tail2",
          top=(0.6, 0.12), side=(1, 0, 0))
    B.build()
    bk.stud_skin(k, PITCH)
    return {"TH": round(B.th, 3)}


# ------------------------------------------------------------------ rig
def rig(k):
    k.joint("Spine", (0, 0.20, 0.72), "Root", tail=(0, -0.4, 0))
    k.joint("Chest", (0, -0.10, 0.72), "Spine", tail=(0, -0.4, 0))
    k.joint("Mane", (0, -0.30, 0.98), "Chest", tail=(0, 0, 0.2))
    k.joint("Neck", (0, -0.52, 0.74), "Chest", tail=(0, -0.2, -0.02))
    k.joint("Head", (0, -0.70, 0.58), "Neck", tail=(0, -0.35, 0.0))           # throat pivot (low back of the head)
    k.joint("Jaw", (0, -0.86, 0.54), "Head", tail=(0, -0.25, 0))
    for s, side in ((1, "L"), (-1, "R")):
        k.joint("Ear_" + side, (s * 0.105, -0.74, 0.82), "Head", tail=(s * 0.08, 0.04, 0.16))
        for fb, parent, knee in (("F", "Chest", (0, 1, 0)), ("B", "Spine", (0, -1, 0))):
            H, K, A, P = (X(p, s) for p in LEGS[fb])
            k.joint("Leg_" + fb + side, H, parent)
            k.joint("Shin_" + fb + side, K, "Leg_" + fb + side)
            k.joint("Foot_" + fb + side, A, "Shin_" + fb + side, tail=(0, -0.15, 0))
            k.add_leg2("Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side, knee=knee)
    k.joint("Tail1", TAILP[0], "Spine")
    k.joint("Tail2", TAILP[1], "Tail1", tail=(0, 0.03, -0.12))


def joints():
    return [((0, -0.66, 0.60), (0, -0.74, 0.66), 0.20, "Head")]


# ------------------------------------------------------------------ animation (FIERCE_PLAN 2026-10-09)
import petkit as pk
import _common as cm

LEGS4 = ["Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR"]


def tab(T, f):
    """eased (smoothstep) interpolation through [(frame, value | tuple)]"""
    if f <= T[0][0]:
        return T[0][1]
    for (f0, v0), (f1, v1) in zip(T, T[1:]):
        if f0 <= f <= f1:
            u = (f - f0) / (f1 - f0) if f1 > f0 else 1.0
            u = u * u * (3 - 2 * u)
            if isinstance(v0, tuple):
                return tuple(a + (b - a) * u for a, b in zip(v0, v1))
            return v0 + (v1 - v0) * u
    return T[-1][1]


def lowest(k, f):
    """lowest z of the posed mesh at frame f"""
    import bpy
    bpy.context.scene.frame_set(f)
    dg = bpy.context.evaluated_depsgraph_get()
    ev = k.main.evaluated_get(dg)
    me = ev.to_mesh()
    mw = ev.matrix_world
    z = min((mw @ v.co).z for v in me.vertices)
    ev.to_mesh_clear()
    return z


def ears(k, f, l=0.0, r=None, splay=0.0):
    r = l if r is None else r
    k.key("Ear_L", f, rot=(l, 0, -splay))
    k.key("Ear_R", f, rot=(r, 0, splay))


def tail(k, f, n, amp=14.0, lift=0.0, cycles=3, ph=0.0):
    k.key("Tail1", f, rot=(lift, amp * pk.wave(f, n, ph, cycles), 0))
    k.key("Tail2", f, rot=(lift * 0.5, amp * 1.4 * pk.wave(f, n, ph - 0.12, cycles), 0))


def idle(k):
    """ROOT & SNORT: head low, quick sniffs, roots the ground twice with the snout (dig + scoop), lifts the head and
    SNORTS (the body jolts, the crest flares); an ear flick each side, the tail twirls."""
    n = 120
    k.new_action("idle", n, True)
    NK = [(0, 4), (8, 8), (38, 8), (44, 13), (49, 6), (54, 9), (58, 13), (63, 6), (68, 8), (76, 8), (84, -1),
          (89, -2), (92, -1), (100, -1), (110, 2), (120, 4)]
    HD = [(0, 6), (8, 14), (38, 14), (44, 28), (49, 4), (54, 14), (58, 28), (63, 4), (68, 14), (76, 14), (84, -10),
          (89, -18), (92, -10), (100, -12), (110, 3), (120, 6)]
    JW = [(0, 0), (44, 0), (49, 5), (52, 0), (58, 0), (63, 5), (66, 0), (88, 0), (90, 12), (94, 2), (120, 0)]
    JOLT = [(0, (0.0, 0.0)), (86, (0.0, 0.0)), (89, (-0.02, 2.0)), (92, (0.012, -2.0)), (96, (0.0, 0.0)),
            (120, (0.0, 0.0))]
    MN = [(0, (0.0, 0.0)), (86, (0.0, 0.0)), (90, (6.0, 1.0)), (100, (5.0, 0.8)), (112, (0.0, 0.0)),
          (120, (0.0, 0.0))]
    EAR = [(0, (0, 0)), (28, (0, 0)), (30, (-30, 0)), (33, (0, 0)), (70, (0, 0)), (72, (0, -28)), (75, (0, 0)),
           (88, (0, 0)), (90, (-20, -20)), (100, (-12, -12)), (112, (0, 0)), (120, (0, 0))]
    for f in range(0, n + 1):
        if f % 2 and not (40 <= f <= 66 or 84 <= f <= 96 or 26 <= f <= 36 or 68 <= f <= 76):
            continue
        b = pk.wave(f, n, 0, 4)
        jz, jc = tab(JOLT, f)
        sniff = (2.5 * math.sin(2 * math.pi * f / 5) if 10 <= f <= 38 else 0.0)
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, 0.006 * b + jz))
        k.key("Chest", f, rot=(-0.6 * b + jc, 0, 0))
        k.key("Neck", f, rot=(tab(NK, f), 0, 0))
        k.key("Head", f, rot=(tab(HD, f) + sniff, 0, 0))
        k.key("Jaw", f, rot=(tab(JW, f), 0, 0))
        mp, mz = tab(MN, f)
        k.key("Mane", f, rot=(mp, 0, 0), loc=(0, 0.02 * mz, 0.045 * mz))
        el, er = tab(EAR, f)
        ears(k, f, el, er)
        tail(k, f, n, amp=18, lift=4, cycles=6)
    cm.plant(k, n, legs=LEGS4)
    k.finish()
    k.meta["planted"] = LEGS4


def walk(k):
    n = 22

    def body(f):
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(0.8 * pk.wave(f, n, 0.1, 2), 1.2 * pk.wave(f, n), 2.0 * pk.wave(f, n)),
              loc=(0, 0, -0.02 * b))
        k.key("Chest", f, rot=(0, -2 * pk.wave(f, n, 0.25), -1.5 * pk.wave(f, n, 0.25)))
        k.key("Neck", f, rot=(4 + 2 * pk.wave(f, n, 0.1, 2), 0, 0))
        k.key("Head", f, rot=(4 - 2.5 * pk.wave(f, n, 0.2, 2), 2 * pk.wave(f, n, 0.25), 0))
        k.key("Jaw", f, rot=(0, 0, 0))
        k.key("Mane", f, rot=(2 * pk.wave(f, n, 0.3, 2), 0, 0), loc=(0, 0, 0))
        ears(k, f, 6 * pk.wave(f, n, 0.2, 2))
        tail(k, f, n, amp=10, lift=8, cycles=2)
    return cm.quad_walk(k, n, 0.12, 0.07, body, gait="trot")


def roar(k):
    """CREST & CHAMP: drops its head, the crest bristles up, the jaw champs 4 fast clacks (embers), then a squeal
    with the head thrown 20 deg up, jaw wide and trembling, ears pinned, tail up; settles."""
    n = 60
    k.new_action("roar", n, False)
    NK = [(0, 0), (8, 8), (34, 8), (40, -2), (50, -2), (60, 0)]
    HD = [(0, 0), (8, 12), (34, 12), (40, -22), (50, -22), (60, 0)]
    MN = [(0, (0.0, 0.0)), (8, (6.0, 1.0)), (50, (6.0, 1.0)), (60, (0.0, 0.0))]
    EAR = [(0, 0), (8, -28), (34, -28), (38, -34), (50, -34), (60, 0)]
    TL = [(0, 0), (8, 18), (50, 30), (60, 0)]
    SP = [(0, (0.0, 0.0)), (8, (2.0, -0.02)), (34, (2.0, -0.02)), (40, (-3.0, 0.0)), (50, (-3.0, 0.0)),
          (60, (0.0, 0.0))]
    for f in range(0, n + 1, 2):
        cp, z = tab(SP, f)
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(cp, 0, 0))
        k.key("Neck", f, rot=(tab(NK, f), 0, 0))
        k.key("Head", f, rot=(tab(HD, f), 0, 0))
        mp, mz = tab(MN, f)
        k.key("Mane", f, rot=(mp, 0, 0), loc=(0, 0.02 * mz, 0.045 * mz))
        ears(k, f, tab(EAR, f))
        t = tab(TL, f)
        k.key("Tail1", f, rot=(t, 4 * pk.wave(f, n, 0, 6), 0))
        k.key("Tail2", f, rot=(t * 0.5, 6 * pk.wave(f, n, -0.1, 6), 0))
    for f, jw in ((0, 0), (10, 0), (13, 25), (16, 0), (19, 25), (22, 0), (25, 25), (28, 0), (31, 25), (34, 0),
                  (38, 30), (40, 27), (42, 32), (44, 27), (46, 32), (48, 28), (50, 30), (56, 4), (60, 0)):
        k.key("Jaw", f, rot=(jw, 0, 0))
    cm.plant(k, n, legs=LEGS4)
    k.finish(loop=False)


def wallow(k):
    """SIGNATURE - LAVA WALLOW: kneels on its front legs, flops onto its left side, rolls onto its BACK and bicycles
    all four legs in the air while wriggling its back in the lava mud, rolls back onto its side, springs up onto its
    legs and gives one big snort with the crest flaring."""
    import bpy
    n = 100
    k.new_action("act_wallow", n, False)
    # body: (pitch, yaw, roll) + z  (roll + = the left/+X side goes down)
    BODY = [(0, (0, 0, 0, 0.0)), (10, (8, 0, 0, -0.10)), (16, (4, 0, 35, -0.20)), (22, (0, 0, 90, -0.40)),
            (30, (-13, 0, 158, -0.30)), (50, (-13, 0, 158, -0.30)), (56, (0, 0, 90, -0.40)), (64, (0, 0, 90, -0.40)),
            (70, (4, 0, 22, -0.08)), (75, (-3, 0, 0, 0.03)), (79, (0, 0, 0, 0.0)), (100, (0, 0, 0, 0.0))]

    def body(f):
        p, y, r, z = tab(BODY, f)
        if 30 <= f <= 50:                                  # wriggling the back in the mud
            w = math.sin(2 * math.pi * (f - 30) / 10)
            y += 8 * w
            r += 5 * math.sin(2 * math.pi * (f - 30) / 20)
        return p, y, r, z

    NK = [(0, 0), (10, -2), (22, -2), (56, -2), (68, -2), (78, 0), (82, -2), (86, -1), (92, 0), (100, 0)]
    HD = [(0, 0), (10, -8), (22, -14), (56, -14), (68, -6), (78, 0), (82, -18), (86, -12), (92, 0), (100, 0)]
    JW = [(0, 0), (22, 0), (30, 14), (50, 14), (56, 0), (80, 0), (82, 14), (86, 3), (100, 0)]
    MN = [(0, (0.0, 0.0)), (78, (0.0, 0.0)), (82, (6.0, 1.0)), (90, (5.0, 0.8)), (98, (0.0, 0.0)),
          (100, (0.0, 0.0))]
    for f in range(0, n + 1, 2):
        p, y, r, z = body(f)
        k.key("Spine", f, rot=(p, y, r), loc=(0, 0, z))
        k.key("Chest", f, rot=(0, 0, 0))
        k.key("Neck", f, rot=(tab(NK, f), 0, 0))
        k.key("Head", f, rot=(tab(HD, f), 0, 0))
        jw = tab(JW, f) + (5 * math.sin(2 * math.pi * f / 6) if 30 <= f <= 50 else 0)
        k.key("Jaw", f, rot=(jw, 0, 0))
        mp, mz = tab(MN, f)
        lay = tab([(0, 0.0), (16, 0.0), (24, 1.0), (56, 1.0), (64, 0.0), (100, 0.0)], f)   # crest laid flat in the mud
        k.key("Mane", f, rot=(mp - 36 * lay, 0, 0), loc=(0, 0.02 * mz, 0.045 * mz))
        ears(k, f, -24 if 16 <= f <= 66 else 0)
        tail(k, f, n, amp=24 if 28 <= f <= 52 else 8, cycles=10)
    k.bake_bezier_now()
    sc = bpy.context.scene

    def fk_legs(f, kick):
        for leg in LEGS4:
            fr = leg[4] == "F"
            s = 1 if leg.endswith("L") else -1
            ph = (0.0 if fr else 0.5) + (0.0 if s > 0 else 0.25)
            w = math.sin(2 * math.pi * (f / 10 + ph)) * kick
            k.key(leg, f, rot=((-24 if fr else 24) + 16 * w, 0, -s * 10))
            k.key("Shin_" + leg[4:], f, rot=((34 if fr else -34) + 18 * w, 0, 0))
            k.key("Foot_" + leg[4:], f, rot=(10 * w, 0, 0))

    FK = (16, 66)
    IKF = list(range(0, FK[0] - 1)) + list(range(FK[1] + 4, n + 1))
    for f in range(FK[0], FK[1] + 1, 2):
        sc.frame_set(f)
        fk_legs(f, 1.0 if 28 <= f <= 52 else 0.3)

    def plant_ik():
        for f in IKF:
            sc.frame_set(f)
            for leg in LEGS4:
                k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, 0.0)))

    plant_ik()
    # rest the body ON the ground while it lies there, never through it (every frame of the roll + get-up)
    fix = {}
    for f in range(FK[0] - 2, FK[1] + 15):
        low = lowest(k, f)
        fix[f] = (0.004 - low) if 22 <= f <= 56 else max(0.0, 0.004 - low)
    for f, dz in fix.items():
        p, y, r, z = body(f)
        k.key("Spine", f, rot=(p, y, r), loc=(0, 0, z + dz))
    k.bake_bezier_now()
    plant_ik()
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    wallow(k)
    return stride


def check_pairs():
    P = [("Leg_FL", "Leg_BL"), ("Leg_FR", "Leg_BR"), ("Leg_FL", "Leg_FR"), ("Leg_BL", "Leg_BR"),
         ("Shin_FL", "Shin_FR"), ("Shin_BL", "Shin_BR"), ("Shin_FL", "Shin_BL"), ("Shin_FR", "Shin_BR"),
         ("Foot_FL", "Foot_FR"), ("Foot_BL", "Foot_BR"), ("Foot_FL", "Foot_BL"), ("Foot_FR", "Foot_BR")]
    for a in ("Head", "Jaw"):
        for b in ("Leg_FL", "Leg_FR", "Shin_FL", "Shin_FR", "Foot_FL", "Foot_FR"):
            P.append((a, b))
    for b in ("Leg_BL", "Leg_BR", "Shin_BL", "Shin_BR", "Foot_BL", "Foot_BR"):
        P.append(("Tail2", b))
    P += [("Ear_L", "Mane"), ("Ear_R", "Mane"), ("Head", "Chest"), ("Jaw", "Chest"), ("Mane", "Neck"),
          ("Head", "Mane")]
    return P
