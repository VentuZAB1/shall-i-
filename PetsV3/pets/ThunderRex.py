# Thunder Rex (Storm egg SECRET 1%, 2026-10-14) - v2 "THE STORM KING" (review 1: _review/ThunderRex_review1.md).
# A storm-black armoured tyrannosaur in the FIERCE studded style of our approved pets: dark armour shells split by
# glowing cyan seams over a storm-blue hide and a silver scute belly, a ridge of white-hot lightning crystal shards
# down the back (W fan from behind), a gold lightning crown + back-swept crystal horns, a cyan storm core on the chest,
# a thunder-blade tail tip. Techniques: MoltenBoar shell()/side_pt()/crack(), Ivonrath fierce_eye()/horns/crown band,
# LavaGolem molten heart + band(), CelestialDragon surf_hit() + scute keel + horn crown. No glow (Studio VFX on the
# anchor bones Crown / Core / Breath / Bolt / Ridge1-3). v1 (plain slate T-rex): _tools/rex_versions/ThunderRex_v1.py
import math
from mathutils import Vector, Matrix

DISPLAY = "Thunder Rex"
MOTION = "Walk"
RIG = "biped"
HEIGHT = 10.0                # total height (crown tips) in studs at x1 - the 1% secret stands taller than its egg

# Blender colours (Roblox renders ~0.6x darker)
ARMOR = (44, 50, 112)        # shells, skull cap, brows, thigh plates, shins, feet, horn bases
HIDE = (76, 88, 200)         # storm-blue hide under the shells
BELLY = (176, 196, 240)      # silver scute underside
BELLY_D = (140, 160, 214)    # scute gaps
DEEP = (34, 110, 230)        # crystal roots
CYAN = (60, 214, 255)        # crystal middles, seams, eyes, core
HOT = (215, 250, 255)        # crystal tips, seam centres, eye hot spots
GOLD = (255, 196, 50)        # crown band + core rim only
MOUTH = (40, 26, 80)
BLACK = (14, 14, 22)
TEETH = (238, 234, 220)
CLAW = (24, 22, 40)

H_MODEL = 2.02
PITCH = round(0.042 * (H_MODEL / HEIGHT) / (1.498 / 8.0), 4)

HIP, KNEE, ANKLE, TOE = (0.24, 0.30, 0.95), (0.30, 0.04, 0.58), (0.335, 0.30, 0.24), (0.355, 0.12, 0.04)
SHOULDER, ELBOW, HAND = (0.24, -0.42, 1.02), (0.30, -0.50, 0.88), (0.27, -0.62, 0.90)
TAILP = [(0, 0.50, 1.08), (0, 0.84, 1.05), (0, 1.18, 1.00), (0, 1.50, 0.99), (0, 1.78, 1.06)]
NECK0, NECK1 = Vector((0, -0.40, 1.27)), Vector((0, -0.64, 1.47))
CORE = (0, -0.50, 1.08)      # filled in by model(): chest core centre (VFX anchor)
RIDGE_TIPS = [(0, -0.30, 1.75), (0, -0.05, 1.70), (0, 0.10, 1.60)]   # filled in by model(): big shard tips
BOLT_C = (0, 1.97, 1.12)


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


# ------------------------------------------------------------------ helpers (MoltenBoar / LavaGolem / Ivonrath)
def prof(b, lz):
    t = (lz / b.h.z + 1) / 2
    fx = b.bot[0] + (b.top[0] - b.bot[0]) * t
    fy = b.bot[1] + (b.top[1] - b.bot[1]) * t
    return b.h.x * fx, b.h.y * fy, b.ts[1] * t


def shell(B, b, y0, y1, za, color, pad=0.024, bone=None, rnd=0.30, lift=0.0, **kw):
    """armour shell over body block b: local y range [y0, y1], local z from za up to the top (MoltenBoar)"""
    xa, ya, oa = prof(b, za)
    xb, yb, ob = prof(b, b.h.z)
    zb = b.h.z + pad + lift
    lo_a, hi_a = max(y0 + oa, oa - ya - pad), min(y1 + oa, oa + ya + pad)
    lo_b, hi_b = max(y0 + ob, ob - yb - pad), min(y1 + ob, ob + yb + pad)
    cy, hy = (lo_a + hi_a) / 2, (hi_a - lo_a) / 2
    hx = xa + pad
    c = b.world(Vector((0, cy, (za + zb) / 2)))
    return B.add(c, (hx, hy, (zb - za) / 2), color, bone or b.bone, R=b.R,
                 top=((xb + pad) / hx, (hi_b - lo_b) / 2 / hy), top_shift=(0, (lo_b + hi_b) / 2 - cy), rnd=rnd, **kw)


def side_pt(b, s, ly, lz, off=0.006):
    hx, _, oy = prof(b, lz)
    p = b.world(Vector((s * (hx + off), ly + oy, lz)))
    dx = b.h.x * (b.top[0] - b.bot[0]) / (2 * b.h.z)
    n = (b.R @ Vector((s, 0, -dx))).normalized()
    return p, n


def fpt(b, lx, lz, off=0.006):
    """point on the FRONT (-y) face of tapered block b at local (lx, lz) + its normal (LavaGolem)"""
    t = (lz / b.h.z + 1) / 2
    fy = b.bot[1] + (b.top[1] - b.bot[1]) * t
    p = b.world(Vector((lx + b.ts[0] * t, b.ts[1] * t - (b.h.y * fy + off), lz)))
    g = (b.ts[1] - b.h.y * (b.top[1] - b.bot[1])) / (2 * b.h.z)
    return p, (b.R @ Vector((0, -1, g))).normalized()


def crack(B, b, s, pts, w=0.034, off=0.03):
    """branching cyan crack running down the flank from a seam (MoltenBoar crack)"""
    Q = [side_pt(b, s, y, z, off) for y, z in pts]
    for i, ((a, n), (c, _)) in enumerate(zip(Q, Q[1:])):
        B.bar(a, c, n, w, 0.012, CYAN, b.bone, studs=[], bevel=0.004, nostud=True,
              top=(1, 0.2) if i == len(Q) - 2 else (1, 1))


def surf_hit(B, blks, origin, direction):
    """exact hit point + normal on the bevelled meshes of blks (CelestialDragon)"""
    import blockkit as bk
    from mathutils.bvhtree import BVHTree
    B._resolve()
    best = None
    d = Vector(direction).normalized()
    for blk in blks:
        bm = bk._box_bm(blk)
        t = BVHTree.FromBMesh(bm)
        bm.free()
        loc, nrm, _, dist = t.ray_cast(Vector(origin), d)
        if loc is not None and (best is None or dist < best[2]):
            best = (loc, nrm.normalized(), dist)
    if best is None:
        raise RuntimeError("surf_hit: no surface from %s" % (tuple(origin),))
    return best[0], best[1]


def fierce_eye(B, c, s, bone="Head", yaw=14.0, tilt=18.0, sc=1.3):
    """Ivonrath's eye: black socket (inner corner down) -> cyan slit -> hot highlight, reptile pupil, heavy V brow"""
    from mathutils import Euler
    R = Euler((0, math.radians(-s * tilt), math.radians(s * yaw)), "XYZ").to_matrix()
    n = R @ Vector((0, -1, 0))
    c = Vector(c)
    B.add(c, (0.052 * sc, 0.008, 0.025 * sc), BLACK, bone, R=R, studs=[], role="detail", bevel=0.004)
    B.add(c + n * 0.006, (0.044 * sc, 0.006, 0.0135 * sc), CYAN, bone, R=R, studs=[], role="detail", bevel=0.003)
    B.add(c + n * 0.011 + R @ Vector((s * 0.022 * sc, 0, 0.002)), (0.014 * sc, 0.004, 0.006 * sc), HOT, bone,
          R=R, studs=[], role="detail", bevel=0.002)
    B.add(c + n * 0.011 + R @ Vector((-s * 0.004, 0, 0)), (0.006 * sc, 0.004, 0.0135 * sc), BLACK, bone, R=R,
          studs=[], role="detail", bevel=0.002)
    Rb = Euler((0, math.radians(-s * 22), math.radians(s * yaw)), "XYZ").to_matrix()
    B.add(c + Vector((0, 0, 0.044 * sc)) + n * 0.024, (0.074 * sc, 0.034, 0.028 * sc), ARMOR, bone, R=Rb,
          role="detail", bevel=0.012)


def shard(B, base, d, L, w, bone, kink=False, socket=True):
    """lightning crystal shard: armour socket -> DEEP root -> CYAN middle -> HOT tip; flat blade (thin across x);
    kink=True bends the middle back like a bolt"""
    import blockkit as bk
    d = Vector(d).normalized()
    base = Vector(base)
    side = Vector((1, 0, 0))
    if abs(d.x) > 0.2:                                   # splayed side shard: blade plane follows the splay
        side = Vector((d.z, 0, -d.x)).normalized() if d.x > 0 else Vector((-d.z, 0, d.x)).normalized()
    back = side.cross(d).normalized()
    if back.y < 0:
        back = -back
    if socket:
        B.add(base - d * 0.01, (w * 0.62, w * 1.25, 0.035), ARMOR, bone, R=bk.frame_from(base - d, base, side),
              top=(0.85, 0.85), role="limb")
    p0 = base - d * 0.05
    p1 = base + d * L * 0.40
    B.add((p0 + p1) / 2, (w * 0.42, w, (p1 - p0).length / 2), DEEP, bone, R=bk.frame_from(p0, p1, side),
          top=(0.85, 0.82), studs=[], nostud=True, role="limb")
    dk = (d + back * 0.55).normalized() if kink else d
    p2 = p1 - d * 0.03 + (back * w * 0.25 if kink else Vector())
    p3 = p2 + dk * L * 0.36
    B.add((p2 + p3) / 2, (w * 0.36, w * 0.80, (p3 - p2).length / 2), CYAN, bone, R=bk.frame_from(p2, p3, side),
          top=(0.85, 0.80), studs=[], nostud=True, role="limb")
    p4 = p3 - dk * 0.02 - (back * w * 0.35 if kink else Vector())
    tipL = L * 0.36
    B.add(p4 + d * tipL / 2, (w * 0.30, w * 0.66, tipL / 2), HOT, bone, R=bk.frame_from(p4, p4 + d, side),
          top=(0.12, 0.10), studs=[], nostud=True, role="limb")
    return p4 + d * tipL


def model(k):
    import blockkit as bk
    global CORE, RIDGE_TIPS
    B = bk.Blocks(k, seed=31, tier=4, plates=False)
    up = Vector((0, 0, 1))
    # ================= torso: deep ribcage raised at the front, hips; storm-blue hide
    rib = B.add((0, -0.16, 1.10), (0.29, 0.31, 0.28), HIDE, "Chest", rot=(-12, 0, 0), bot=(0.62, 0.58),
                top=(0.86, 0.90), rnd=0.32)
    hips = B.add((0, 0.26, 1.04), (0.25, 0.25, 0.245), HIDE, "Spine", rot=(-2, 0, 0), bot=(0.72, 0.70),
                 top=(0.86, 0.90), rnd=0.32)
    # silver scute belly strip following the rising belly line
    B.seg((0, -0.36, 0.85), (0, 0.32, 0.785), 0.17, 0.05, BELLY, "Chest", side=(1, 0, 0), top=(0.75, 0.9),
          ext=0.03)
    for t, w in ((0.12, 0.15), (0.36, 0.15), (0.60, 0.13), (0.84, 0.11)):
        p = Vector((0, -0.36, 0.797)).lerp(Vector((0, 0.32, 0.737)), t)
        B.bar(p + Vector((-w, 0, 0)), p + Vector((w, 0, 0)), Vector((0, 0, -1)), 0.024, 0.008, BELLY_D, "Chest",
              studs=[], bevel=0.003, nostud=True)
    # keel plate on the chest front + storm core (dark socket, gold rim, cyan diamond, hot centre)
    kp, kn = fpt(rib, 0, -0.19, off=0.0)
    keel = B.add(kp + kn * 0.01, (0.013, 0.13, 0.09), BELLY, "Chest", R=bk.frame_from(kp - up, kp, kn),
                 top=(1, 0.75), rnd=0.25)
    for v in (-0.045, 0.025):
        B.add(keel.world((0.014, 0, v)), (0.004, 0.12 * (0.8 + 0.2 * (v + 0.09) / 0.18), 0.008), BELLY_D, "Chest",
              R=keel.R, studs=[], role="detail", bevel=0.003)
    cp, cn = fpt(rib, 0, -0.07, off=0.03)
    CORE = tuple(cp)
    dia = Vector((0.7071, 0, 0.7071))
    for ang, sz in ((45, (0.135, 0.135)), (18, (0.10, 0.105)), (72, (0.095, 0.11))):
        B.add(cp + cn * 0.004, (0.012, sz[0], sz[1]), ARMOR, "Chest", R=bk.frame_from(cp, cp + Vector(
            (math.cos(math.radians(ang)), 0, math.sin(math.radians(ang)))), cn), studs=[], role="detail", bevel=0.008)
    B.add(cp + cn * 0.012, (0.012, 0.097, 0.097), GOLD, "Chest", R=bk.frame_from(cp, cp + dia, cn), studs=[],
          role="detail", bevel=0.006)
    B.add(cp + cn * 0.020, (0.012, 0.077, 0.077), CYAN, "Chest", R=bk.frame_from(cp, cp + dia, cn), studs=[],
          role="detail", bevel=0.006)
    B.add(cp + cn * 0.029, (0.008, 0.034, 0.034), HOT, "Chest", R=bk.frame_from(cp, cp + dia, cn), studs=[],
          role="detail", bevel=0.004)
    # ================= armour shells (dark) with recessed cyan seams in the gaps; jagged lower edges; flank cracks
    shells = []
    for b, y0, y1, za, lift in ((rib, -0.31, -0.085, -0.07, 0.02), (rib, -0.035, 0.31, -0.09, 0.0),
                                (hips, -0.10, 0.25, -0.06, 0.0)):
        sh = shell(B, b, y0, y1, za, ARMOR, rnd=0.42, lift=lift)
        shells.append(sh)
        for s in (1, -1):
            for t, L in ((0.2, 0.10), (0.5, 0.07), (0.8, 0.09)):
                ly = y0 + (y1 - y0) * t
                p0, nrm = side_pt(b, s, ly, za + 0.03, off=0.030)
                p1 = p0 + Vector((0, 0.015, -L))
                B.add((p0 + p1) / 2, (0.014, 0.05, (p1 - p0).length / 2), ARMOR, b.bone,
                      R=bk.frame_from(p0, p1, nrm), top=(1, 0.10), role="detail", bevel=0.006)
    for b, y0, y1, za in ((rib, -0.085, -0.035, -0.09), (hips, -0.15, -0.10, -0.06)):
        shell(B, b, y0, y1, za - 0.02, CYAN, pad=0.012, rnd=0.30, studs=[], nostud=True)       # seam bands
    for s in (1, -1):
        crack(B, rib, s, ((-0.06, -0.10), (-0.02, -0.16), (-0.08, -0.20), (-0.03, -0.25)))
        crack(B, rib, s, ((-0.29, -0.08), (-0.24, -0.14), (-0.27, -0.19)), w=0.03)
        crack(B, hips, s, ((-0.125, -0.07), (-0.08, -0.12), (-0.12, -0.17), (-0.07, -0.21)))
    # ================= neck: hide, armour top, silver throat
    nd = (NECK1 - NECK0).normalized()
    nn = Vector((0, -nd.z, nd.y)) if nd.y < 0 else Vector((0, nd.z, -nd.y))
    if nn.z < 0:
        nn = -nn
    B.seg(NECK0, NECK1, 0.17, 0.18, HIDE, "Neck", ext=0.07, ext1=0.03, top=(0.92, 0.9))
    neck_arm = B.seg(NECK0 + nn * 0.12, NECK1 + nn * 0.12, 0.15, 0.075, ARMOR, "Neck", ext=0.05, top=(0.9, 0.85),
                     rnd=0.4)
    B.seg(NECK0.lerp(NECK1, 0.45) - nn * 0.13, NECK1 - nn * 0.13, 0.12, 0.05, BELLY, "Neck", ext=0.03)
    # ================= head (throat pivot): massive skull, sloped narrowing snout BELOW the eye line
    B.add((0, -0.80, 1.56), (0.19, 0.18, 0.165), HIDE, "Head", top=(0.80, 0.84), rnd=0.25)               # skull
    B.add((0, -0.78, 1.715), (0.165, 0.165, 0.05), ARMOR, "Head", top=(0.75, 0.8))                      # skull cap
    for s in (1, -1):                                                                                 # jaw muscles
        B.add((s * 0.18, -0.72, 1.50), (0.055, 0.11, 0.12), HIDE, "Head", top=(0.7, 0.8), rnd=0.4)
    B.seg((0, -0.92, 1.48), (0, -1.33, 1.40), 0.135, 0.105, HIDE, "Head", top=(0.65, 0.78), ext=0.03)     # snout
    B.seg((0, -0.95, 1.585), (0, -1.29, 1.50), 0.045, 0.02, ARMOR, "Head", top=(0.6, 1), ext=0.0)         # nasal plate
    for s in (1, -1):                                                                                 # nostrils
        B.add((s * 0.05, -1.326, 1.47), (0.022, 0.012, 0.007), ARMOR, "Head", rot=(0, -s * 25, -s * 20),
              studs=[], role="detail", bevel=0.003)                                            # slanted slits
    # upper teeth: 2 big fangs + 4 graded teeth per side at varied angles (snarl)
    for s in (1, -1):
        for y, L, w, dy, dx in ((-1.29, 0.055, 0.014, -0.15, 0.0), (-1.235, 0.125, 0.022, -0.12, 0.08),
                                (-1.165, 0.07, 0.016, 0.0, 0.1), (-1.10, 0.06, 0.015, 0.1, 0.05),
                                (-1.035, 0.105, 0.02, 0.05, 0.12), (-0.965, 0.05, 0.013, 0.15, 0.0)):
            z = 1.395 - (1.395 - 1.333) * (-0.92 - y) / 0.41 + 0.012
            B.spike((s * 0.13, y, z), (s * dx, dy, -1), L, w, TEETH, "Head")
    # lower jaw (rest ~6 deg open), silver underside, dark mouth, teeth pointing up
    B.seg((0, -0.78, 1.33), (0, -1.28, 1.225), 0.125, 0.055, HIDE, "Jaw", top=(0.80, 1), ext=0.03)
    B.seg((0, -0.80, 1.27), (0, -1.24, 1.172), 0.10, 0.022, BELLY, "Jaw", top=(0.8, 1), ext=0.02)
    B.seg((0, -0.86, 1.39), (0, -1.24, 1.293), 0.10, 0.02, MOUTH, "Jaw", studs=[], role="detail", bevel=0.004)
    B.seg((0, -0.94, 1.385), (0, -1.24, 1.31), 0.10, 0.012, MOUTH, "Head", studs=[], role="detail", bevel=0.004)
    B.add((0, -0.86, 1.36), (0.06, 0.02, 0.04), CYAN, "Head", studs=[], nostud=True, role="detail", bevel=0.006)
    for s in (1, -1):
        for y, L, dx in ((-1.255, 0.07, 0.05), (-1.18, 0.055, 0.0), (-1.11, 0.06, 0.08), (-1.03, 0.05, 0.0),
                         (-0.95, 0.045, 0.06)):
            z = 1.385 - (1.385 - 1.28) * (-0.80 - y) / 0.48 - 0.012
            B.spike((s * (0.085 if y < -1.24 else 0.098), y, z), (s * dx, -0.08, 1), L, 0.014, TEETH, "Jaw")
    # eyes (forward, above the snout) under heavy V brows
    for s in (1, -1):
        fierce_eye(B, (s * 0.118, -0.968, 1.655), s, yaw=14, tilt=18, sc=1.3)
    # swept cheek spikes from the jaw hinge (Raiju ruff, bigger)
    for s in (1, -1):
        for z, dz, L, w in ((1.45, -0.30, 0.16, 0.045), (1.53, -0.05, 0.19, 0.05), (1.61, 0.18, 0.15, 0.042)):
            B.spike((s * 0.20, -0.74, z), (s * 0.38, 0.92, dz), L, w, ARMOR, "Head", top=(0.12, 0.4))
    # ================= STORM CROWN: 2 big back-swept 3-segment horns with crystal tips, 2 jaw-hinge horns,
    # gold band with 5 lightning prongs (Ivonrath crown band + CelestialDragon horn crown)
    for s in (1, -1):
        P = [Vector((s * 0.10, -0.86, 1.71)), Vector((s * 0.16, -0.73, 1.85)), Vector((s * 0.21, -0.57, 1.95)),
             Vector((s * 0.25, -0.38, 2.00))]
        B.seg(P[0], P[1], 0.048, 0.05, ARMOR, "Head", side=(1, 0, 0), ext=0.06, top=(0.85, 0.85), role="limb")
        B.seg(P[1], P[2], 0.041, 0.043, ARMOR, "Head", side=(1, 0, 0), ext=0.02, top=(0.8, 0.8), role="limb")
        d3 = (P[3] - P[2]).normalized()
        B.seg(P[2] - d3 * 0.02, P[2] + d3 * 0.10, 0.034, 0.036, CYAN, "Head", side=(1, 0, 0), top=(0.85, 0.85),
              studs=[], nostud=True, role="limb")
        B.spike(P[2] + d3 * 0.09, d3, (P[3] - P[2]).length - 0.02, 0.029, HOT, "Head", top=(0.12, 0.12),
                nostud=True)
        Q = [Vector((s * 0.18, -0.76, 1.52)), Vector((s * 0.28, -0.64, 1.56)), Vector((s * 0.37, -0.56, 1.55))]
        B.seg(Q[0], Q[1], 0.036, 0.038, ARMOR, "Head", side=(0, 0, 1), ext=0.05, top=(0.8, 0.8), role="limb")
        dq = (Q[2] - Q[1]).normalized()
        B.spike(Q[1] - dq * 0.02, dq, (Q[2] - Q[1]).length + 0.04, 0.03, CYAN, "Head", top=(0.12, 0.12),
                nostud=True)
    B.add((0, -0.935, 1.735), (0.165, 0.055, 0.045), GOLD, "Head", top=(0.9, 0.9), role="limb", bevel=0.01,
          studs=[], nostud=True)
    for s in (1, -1):                                                                     # circlet side bars
        B.seg((s * 0.165, -0.93, 1.735), (s * 0.155, -0.665, 1.745), 0.022, 0.03, GOLD, "Head", studs=[],
              nostud=True, role="limb")
    B.add((0, -0.655, 1.74), (0.10, 0.02, 0.035), GOLD, "Head", studs=[], nostud=True, role="limb", bevel=0.008)
    B.add((0, -0.633, 1.74), (0.022, 0.006, 0.022), CYAN, "Head", rot=(0, 45, 0), studs=[], role="detail",
          bevel=0.004)                                                                   # back gem
    for x, h, kink in ((-0.11, 0.12, False), (-0.055, 0.18, True), (0.0, 0.24, True), (0.055, 0.18, True),
                       (0.11, 0.12, False)):
        base = Vector((x, -0.945, 1.75))
        d = Vector((x * 0.6, -0.15, 1)).normalized()
        if kink:
            m1 = base + d * h * 0.45
            m2 = m1 + Vector((0.025 if x >= 0 else -0.025, 0.02, 0.02))
            B.seg(base, m1, 0.028, 0.02, GOLD, "Head", side=(0, 1, 0), ext=0.02, studs=[], nostud=True, role="limb")
            B.seg(m1 - d * 0.01, m2, 0.026, 0.018, GOLD, "Head", side=(0, 1, 0), studs=[], nostud=True, role="limb")
            B.spike(m2 - d * 0.01, d, h * 0.55, 0.02, HOT, "Head", top=(0.12, 0.12), nostud=True)
        else:
            B.seg(base, base + d * h * 0.55, 0.028, 0.02, GOLD, "Head", side=(0, 1, 0), ext=0.02, studs=[],
                  nostud=True, role="limb")
            B.spike(base + d * h * 0.5, d, h * 0.5, 0.019, HOT, "Head", top=(0.12, 0.12), nostud=True)
    B.add((0, -0.988, 1.735), (0.024, 0.006, 0.024), CYAN, "Head", rot=(0, 45, 0), studs=[], role="detail",
          bevel=0.004)                                                                       # crown gem
    # ================= tiny (thicker) two-claw arms
    for s, side in ((1, "L"), (-1, "R")):
        Sh, El, Ha = X(SHOULDER, s), X(ELBOW, s), X(HAND, s)
        B.seg(Sh, El, 0.055, 0.06, HIDE, "Arm_" + side, ext=0.04, ext1=0.02, top=(0.85, 0.85))
        B.seg(El, Ha, 0.045, 0.05, ARMOR, "Hand_" + side, ext=0.02, ext1=0.01, top=(0.9, 0.9))
        for gx in (-0.018, 0.018):
            B.spike(Ha + Vector((gx, -0.015, -0.01)), (gx, -0.6, -0.8), 0.075, 0.014, CLAW, "Hand_" + side)
    # ================= huge legs: hide thigh + armour plate, armour shin sock, cyan knee band, big clawed foot
    for s, side in ((1, "L"), (-1, "R")):
        H, K, A, T = X(HIP, s), X(KNEE, s), X(ANKLE, s), X(TOE, s)
        lb, sb, fb = "Leg_" + side, "Shin_" + side, "Foot_" + side
        B.seg(H + Vector((0, 0.02, 0.12)), K, 0.175, 0.25, HIDE, lb, ext=0.0, ext1=0.05, top=(0.55, 0.45),
              rnd=0.50)                                                                          # thigh
        B.seg(H + Vector((s * 0.15, 0.03, 0.08)), K + Vector((s * 0.075, -0.01, 0.08)), 0.05, 0.21, ARMOR, lb,
              ext=0.0, top=(0.7, 0.55), rnd=0.45)                                                 # thigh plate
        B.seg(K + (A - K).normalized() * 0.01, K + (A - K).normalized() * 0.06, 0.125, 0.13, CYAN, sb, studs=[],
              nostud=True, role="limb", rnd=0.25)                                                 # knee band
        B.seg(K, A, 0.115, 0.12, ARMOR, sb, ext=0.0, ext1=0.03, top=(0.82, 0.82))                   # shin sock
        B.seg(A, T + Vector((0, 0, 0.045)), 0.095, 0.095, ARMOR, fb, ext=0.04, top=(0.9, 0.9))
        B.add(T + Vector((0, 0.0, 0.002)), (0.12, 0.11, 0.042), ARMOR, fb)
        for gx in (-0.07, 0.0, 0.07):
            a = T + Vector((gx, -0.05, 0.035))
            b2 = T + Vector((gx * 1.35, -0.19, 0.03))
            B.seg(a, b2, 0.032, 0.03, ARMOR, fb, ext=0.0, top=(0.8, 0.8))                          # toe
            B.spike(b2 + Vector((0, 0.01, -0.005)), (gx * 2, -1, -0.5), 0.10 if gx else 0.115, 0.024, CLAW, fb)
        B.spike(T + Vector((0, 0.09, 0.035)), (0, 1, -0.4), 0.085, 0.02, CLAW, fb)                 # dewclaw
        B.spike(A + Vector((0, 0.07, 0.02)), (0, 1, -0.2), 0.10, 0.03, ARMOR, fb, top=(0.12, 0.3))  # ankle spur
    # ================= tail: hide core, armour top shells, silver underside, cyan joint bands, thunder blade
    T = [Vector(p) for p in TAILP]
    tail_tops = []
    for i, hw in enumerate((0.22, 0.17, 0.125, 0.085)):
        bone = "Tail%d" % (i + 1)
        a, b = T[i], T[i + 1]
        dv = (b - a).normalized()
        dn = dv.cross(Vector((1, 0, 0))).normalized()
        dn = dn if dn.z < 0 else -dn
        tp = 0.76
        B.seg(a, b, hw, hw * 0.95, HIDE, bone, ext=0.0 if i == 0 else 0.05, top=(tp, tp))
        B.seg((a.lerp(b, 0.15) if i == 0 else a) + dn * hw * 0.80, b + dn * hw * tp * 0.80, hw * 1.0, hw * 0.26, BELLY, bone,
              ext=0.0 if i == 0 else 0.03, top=(tp, tp))
        tt = B.seg(a.lerp(b, 0.08) - dn * hw * 0.42, a.lerp(b, 0.92) - dn * hw * tp * 0.42, hw * 1.06, hw * 0.62,
                   ARMOR, bone, top=(0.8, 0.8), rnd=0.42)
        tail_tops.append(tt)
        if i > 0:
            B.seg(a - dv * 0.025, a + dv * 0.025, hw * 1.16, hw * 1.10, CYAN, bone, studs=[], nostud=True,
                  role="limb", rnd=0.3)                                                         # joint band
    # thunder blade: a flat lightning bolt (3 flat segments) growing from the tail tip, upturned
    tip = T[4]
    b1 = tip + Vector((0, 0.13, 0.11))
    b2 = b1 + Vector((0, 0.07, -0.06))
    b3 = b2 + Vector((0, 0.16, 0.15))
    B.seg(tip - Vector((0, 0.04, 0)), b1, 0.040, 0.07, DEEP, "Tail4", side=(1, 0, 0), studs=[], nostud=True,
          role="limb")
    B.seg(b1 - Vector((0, 0.03, -0.03)), b2, 0.040, 0.06, CYAN, "Tail4", side=(1, 0, 0), studs=[], nostud=True,
          role="limb")
    B.seg(b2 - Vector((0, 0.03, 0.03)), b3, 0.040, 0.065, CYAN, "Tail4", side=(1, 0, 0), top=(0.6, 0.12),
          studs=[], nostud=True, role="limb")
    B.spike(b3 - (b3 - b2).normalized() * 0.06, b3 - b2, 0.10, 0.03, HOT, "Tail4", top=(0.12, 0.12), nostud=True)
    for s in (1, -1):
        shard(B, b1, (s * 0.55, 0.45, 0.70), 0.15, 0.05, "Tail4", socket=False)
    # ================= CRYSTAL BACK RIDGE: centre row (bolt-kinked every second shard) + splayed side rows (W fan)
    body_tops = shells + [neck_arm] + tail_tops
    centre = [(-0.47, 0.27, 27, "Chest", True), (-0.335, 0.36, 28, "Chest", False),
              (-0.20, 0.42, 29, "Chest", True), (-0.065, 0.40, 30, "Chest", False), (0.07, 0.34, 31, "Chest", True),
              (0.21, 0.28, 32, "Spine", False), (0.35, 0.22, 33, "Spine", True), (0.58, 0.18, 35, "Tail1", False),
              (0.92, 0.15, 35, "Tail2", True), (1.24, 0.12, 35, "Tail3", False)]
    tips = {}
    for y, L, ang, bone, kink in centre:
        p, _ = surf_hit(B, body_tops, (0, y, 3.0), (0, 0, -1))
        d = Vector((0, math.sin(math.radians(ang)), math.cos(math.radians(ang))))
        tips[y] = shard(B, p, d, L, 0.045 + 0.075 * L, bone, kink=kink)
    RIDGE_TIPS = [tuple(round(v, 4) for v in tips[y]) for y in (-0.335, -0.20, -0.065)]
    for s in (1, -1):
        for (y, L, ang, bone, _), sx, f in [(c, 0.13, 0.55) for c in centre[1:7]] + [(centre[7], 0.12, 0.6),
                                                                                     (centre[8], 0.09, 0.6)]:
            p, _ = surf_hit(B, body_tops, (s * sx, y, 3.0), (0, 0, -1))
            sp = math.radians(28)
            d = Vector((s * math.sin(sp), math.sin(math.radians(ang)) * math.cos(sp),
                        math.cos(math.radians(ang)) * math.cos(sp)))
            shard(B, p, d, L * f, 0.035 + 0.06 * L, bone, kink=False)
    B.build()
    bk.stud_skin(k, PITCH)
    return {"TH": round(B.th, 3), "PITCH": PITCH, "CORE": [round(v, 3) for v in CORE], "RIDGE": RIDGE_TIPS}


# ------------------------------------------------------------------ rig
def rig(k):
    k.joint("Spine", (0, 0.26, 1.04), "Root", tail=(0, -0.4, 0.02))
    k.joint("Chest", (0, -0.06, 1.08), "Spine", tail=(0, -0.4, 0.08))
    k.joint("Neck", (0, -0.40, 1.27), "Chest", tail=(0, -0.2, 0.17))
    k.joint("Head", (0, -0.64, 1.40), "Neck", tail=(0, -0.4, 0.0))           # throat pivot
    k.joint("Jaw", (0, -0.78, 1.38), "Head", tail=(0, -0.4, -0.05))
    for s, side in ((1, "L"), (-1, "R")):
        k.joint("Arm_" + side, X(SHOULDER, s), "Chest")
        k.joint("Hand_" + side, X(ELBOW, s), "Arm_" + side, tail=(0, -0.1, 0.02))
        k.joint("Leg_" + side, X(HIP, s), "Spine")
        k.joint("Shin_" + side, X(KNEE, s), "Leg_" + side)
        k.joint("Foot_" + side, X(ANKLE, s), "Shin_" + side, tail=(0, -0.15, -0.1))
        k.add_leg2("Leg_" + side, "Shin_" + side, "Foot_" + side, knee=(0, -1, 0))
    for i in range(4):
        k.joint("Tail%d" % (i + 1), TAILP[i], "Spine" if i == 0 else "Tail%d" % i,
                tail=(Vector(TAILP[i + 1]) - Vector(TAILP[i])) if i == 3 else None)
    # empty VFX anchor bones (Studio particles / lights attach here)
    k.joint("Crown", (0, -0.93, 1.90), "Head", tail=(0, 0, 0.2))
    k.joint("Core", CORE, "Chest", tail=(0, -0.2, 0))
    k.joint("Breath", (0, -1.26, 1.31), "Head", tail=(0, -0.2, 0))
    k.joint("Bolt", BOLT_C, "Tail4", tail=(0, 0.2, 0.1))
    for i, tp in enumerate(RIDGE_TIPS):
        k.joint("Ridge%d" % (i + 1), tp, "Chest", tail=(0, 0, 0.2))


def check_pairs():
    P = [("Leg_L", "Leg_R"), ("Shin_L", "Shin_R"), ("Foot_L", "Foot_R"), ("Head", "Chest"), ("Jaw", "Chest"),
         ("Jaw", "Neck"), ("Head", "Arm_L"), ("Head", "Arm_R"), ("Jaw", "Arm_L"), ("Jaw", "Arm_R"),
         ("Jaw", "Hand_L"), ("Jaw", "Hand_R"), ("Arm_L", "Leg_L"), ("Arm_R", "Leg_R"), ("Hand_L", "Leg_L"),
         ("Hand_R", "Leg_R"), ("Hand_L", "Hand_R")]
    for t in ("Tail2", "Tail3", "Tail4"):
        for b in ("Shin_L", "Shin_R", "Foot_L", "Foot_R"):
            P.append((t, b))
    P += [("Tail1", "Leg_L"), ("Tail1", "Leg_R")]
    return P


# ------------------------------------------------------------------ animation
# Reference (owner rule 2026-10-10): animationreference.org "Tyrant Dragon Animation - MAYA 2023" (alessandro tommasi,
# tags #creature #3d-animation; no dinosaur clips exist on the site): ~0:08-0:12 the landing sinks into a deep crouch
# with the head dropped almost to the floor; ~0:16-0:20 it rises CHEST FIRST, the neck S-curves and the head arrives
# last (~5 frame lag) with the jaw half open. Used for the roar (anticipation crouch + chest-led rise) and the heavy
# body dip on every walk contact.
import petkit as pk
import _common as cm

LEGS = ["Leg_L", "Leg_R"]
TAIL = ["Tail1", "Tail2", "Tail3", "Tail4"]


def tail(k, f, pitch=0.0, yaw=0.0, each=(0.25, 0.5, 0.8, 1.0)):
    for b, g in zip(TAIL, each):
        k.key(b, f, rot=(pitch * g, yaw * g, 0))


def arms(k, f, up=0.0, spread=0.0, curl=0.0):
    for side, sx in (("L", 1), ("R", -1)):
        k.key("Arm_" + side, f, rot=(-up, 0, -sx * spread))
        k.key("Hand_" + side, f, rot=(-curl, 0, 0))


def plant_frames(k, frames, z=0.0):
    import bpy
    k.bake_bezier_now()
    for f in frames:
        bpy.context.scene.frame_set(f)
        for leg in LEGS:
            k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, z)))


def idle(k):
    """STORM KING WATCH: deep slow breaths (chest swells), a slow look left and right, a low sniff with two short
    nose lifts, a double jaw clack, the tiny claws flex, the tail sways low and heavy."""
    n = 120
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 2):
        b = pk.wave(f, n, 0, 3)
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, 0.010 * b))
        k.key("Chest", f, rot=(-1.5 * b, 0, 0))
        tail(k, f, -1 + 1.5 * pk.wave(f, n, 0.2, 2), 6 * pk.wave(f, n, 0.1, 1))
    for f, nk, ny, hd, hy, ht in ((0, 0, 0, 0, 0, 0), (26, 0, 0, 0, 0, 0), (34, -2, 20, -3, 28, 4), (50, -2, 20, -3, 28, 4),
                                  (60, -1, -18, -2, -24, -3), (72, -1, -18, -2, -24, -3), (80, 6, 0, 6, 0, 0),
                                  (86, 7, 0, 3, 0, 0), (89, 7, 0, 7, 0, 0), (92, 7, 0, 3, 0, 0), (95, 7, 0, 7, 0, 0),
                                  (106, 0, 0, 0, 0, 0), (120, 0, 0, 0, 0, 0)):
        k.key("Neck", f, rot=(nk, ny * 0.4, 0))
        k.key("Head", f, rot=(hd, hy * 0.6, ht))
    for f, j in ((0, 3), (60, 3), (64, 16), (67, 3), (70, 16), (73, 3), (120, 3)):
        k.key("Jaw", f, rot=(j, 0, 0))
    for f, c in ((0, 0), (36, 0), (40, 28), (44, 0), (47, 26), (51, 0), (120, 0)):
        arms(k, f, up=0, curl=c)
    plant_frames(k, range(0, n + 1))
    k.finish()
    k.meta["planted"] = LEGS


def walk(k):
    """heavy stomp: the body dips on every contact, the head counter-bobs a few frames late, the tail swings against
    the hips, toes peel off the ground"""
    n = 32

    def dip(f):                                            # stomp: drops 0.05 within 3 f of a contact, rises slowly
        t = f % (n // 2)
        if t <= 3:
            u = t / 3.0
            return -0.05 * (u * u * (3 - 2 * u))
        u = (t - 3) / (n / 2 - 3)
        return -0.05 * (1 - u * u * (3 - 2 * u))

    def body(f):
        k.key("Spine", f, rot=(1.2 * pk.wave(f, n, 0.12, 2), 4 * pk.wave(f, n, 0.0), 3 * pk.wave(f, n, 0.0)),
              loc=(0, 0, dip(f)))
        k.key("Chest", f, rot=(0, -3 * pk.wave(f, n, 0.05), -2 * pk.wave(f, n, 0.0)))
        k.key("Neck", f, rot=(2 + 2.5 * pk.wave(f, n, 0.18, 2), -2 * pk.wave(f, n, 0.1), 0))
        k.key("Head", f, rot=(-2 - 3 * pk.wave(f, n, 0.28, 2), 3 * pk.wave(f, n, 0.15), 0))
        k.key("Jaw", f, rot=(4 + 2 * pk.wave(f, n, 0.3, 2), 0, 0))
        arms(k, f, up=4 * pk.wave(f, n, 0.25), curl=6)
        cm.chain(k, f, n, TAIL, sway=-5, pitch=1, cycles=1, lag=0.14, grow=0.5)
    orig = k.solve_leg
    k.solve_leg = lambda leg, f, T, foot_z=0.0, toe=None: orig(leg, f, T, foot_z,
                                                               toe=16.0 * min(1.0, max(0.0, T.z) / 0.1))
    try:
        return cm.biped_walk(k, n, 0.18, 0.13, body, legs=(("Leg_L", 0.0), ("Leg_R", 0.5)), duty=0.6)
    finally:
        del k.solve_leg


def roar(k):
    """STORM ROAR (ref: Tyrant Dragon crouch -> chest-led rise): sinks into a deep crouch with the head dropped low,
    rises chest first, the head arrives last and throws the jaw wide open; arms flare, the tail lifts stiff and its
    tip shivers; the jaw buzzes through the hold; settles."""
    n = 84
    k.new_action("roar", n, False)
    K = [  # f, spine z, spine pitch, chest, neck, head, jaw, tail pitch, arm up, spread, curl
        (0, 0.0, 0, 0, 0, 0, 3, 0, 0, 0, 0),
        (14, -0.10, 14, 4, 8, 12, 5, -4, -10, 0, 10),
        (20, -0.10, 16, 5, 8, 14, 6, -6, -12, 0, 12),
        (27, 0.02, -8, -4, -4, 4, 18, 8, 10, 14, 20),
        (32, 0.03, -11, -5, -8, -16, 40, 12, 16, 24, 32),
        (60, 0.02, -10, -5, -7, -14, 38, 12, 16, 24, 32),
        (70, -0.02, 2, 0, 2, 2, 8, 4, 4, 6, 8),
        (84, 0.0, 0, 0, 0, 0, 3, 0, 0, 0, 0)]
    for f, z, p, ch, nk, hd, jw, tp, au, sp, cu in K:
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(ch, 0, 0))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        tail(k, f, tp, 0)
        arms(k, f, up=au, spread=sp, curl=cu)
    for f in range(34, 60, 3):
        w = 1 if (f // 3) % 2 else -1
        k.key("Jaw", f, rot=(38 + 3 * w, 0, 0))
        k.key("Tail4", f, rot=(12, 6 * w, 0))
    plant_frames(k, range(0, n + 1))
    k.finish(loop=False)
    k.events["roar"] = {"peak": round(32 / n, 3), "end": round(60 / n, 3)}


def stormbreath(k):
    """SIGNATURE (Thunder Rex only, review 3) - STORM BREATH, the kaiju charge: plants low and glares, the tail drags
    then goes stiff; the body sinks and PUMPS three times while the crystal ridge lights up tail -> crown (VFX events
    charge1-3 on Bolt+Ridge3 / Ridge2+Core / Ridge1+Crown); rears and inhales, then fires a lightning beam from the mouth
    (Breath anchor) with a recoil absorbed by the planted legs, sweeping the head slowly across the beam; snaps the jaw
    shut (smoke puff), snorts and exhales; settles. Planted the whole time, no head shake (owner rule)."""
    n = 100
    k.new_action("act_stormbreath", n, False)
    EACH = (0.2, 0.45, 0.75, 1.0)
    K = [  # f, spine z, spine y, spine pitch, chest, neck pitch, neck yaw, head pitch, head yaw, jaw, tail, curl, spread
        (0, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0),
        (8, -0.06, 0.0, 6, 3, 6, 0, 8, 0, 3, -4, 20, 0),
        (14, -0.06, 0.0, 6, 3, 6, 0, 8, 0, 3, -4, 20, 0),
        (20, -0.085, 0.0, 6, -2, 6, 0, 10, 0, 4, 0, 22, 0),
        (25, -0.06, 0.0, 6, 3, 6, 0, 10, 0, 3, 2, 22, 0),
        (30, -0.085, 0.0, 6, -2, 6, 0, 12, 0, 4, 4, 24, 0),
        (35, -0.06, 0.0, 6, 3, 6, 0, 12, 0, 3, 6, 24, 0),
        (40, -0.085, 0.0, 6, -2, 6, 0, 14, 0, 4, 8, 26, 0),
        (44, -0.06, 0.0, 4, 2, 4, 0, 10, 0, 6, 8, 26, 0),
        (50, -0.02, 0.0, -6, -4, -8, 0, -14, 0, 26, 6, 30, 12),
        (52, -0.02, 0.0, -6, -4, -8, 0, -14, 0, 26, 6, 30, 12),
        (54, -0.05, 0.04, 4, 2, 4, -5, 6, -12, 40, 4, 34, 16),
        (80, -0.04, 0.01, 4, 2, 4, 5, 6, 12, 40, 4, 34, 16),
        (83, -0.03, 0.0, 2, 1, 2, 2, 2, 5, 3, 3, 20, 6),
        (86, -0.03, 0.0, 0, 0, 0, 0, -4, 0, 3, 2, 10, 0),
        (90, -0.01, 0.0, 0, 0, 0, 0, 0, 0, 3, 1, 4, 0),
        (100, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0)]
    for f, z, y, p, ch, nk, ny, hd, hy, jw, tp, cu, sp in K:
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, y, z))
        k.key("Chest", f, rot=(ch, 0, 0))
        k.key("Neck", f, rot=(nk, ny, 0))
        k.key("Head", f, rot=(hd, hy, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        tail(k, f, tp, 0, each=EACH)
        arms(k, f, up=0, spread=sp, curl=cu)
    for f in range(57, 80, 3):                       # beam: jaw buzz + tail-tip shiver, head sweeping slowly
        w = 1 if (f // 3) % 2 else -1
        t = (f - 54) / 26.0
        k.key("Jaw", f, rot=(40 + 2 * w, 0, 0))
        k.key("Head", f, rot=(6, -12 + 24 * t, 0))
        k.key("Neck", f, rot=(4, -5 + 10 * t, 0))
        k.key("Tail4", f, rot=(4, 5 * w, 0))
    plant_frames(k, range(0, n + 1))
    k.finish(loop=False)
    k.events["act_stormbreath"] = {"charge1": round(20 / n, 3), "charge2": round(30 / n, 3), "charge3": round(40 / n, 3),
                                   "breath": round(54 / n, 3), "breath_end": round(80 / n, 3), "smoke": round(83 / n, 3)}


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    stormbreath(k)
    return stride


def joints():
    out = [((0, -0.62, 1.36), (0, -0.70, 1.45), 0.26, "Head"), ((0, -0.78, 1.38), (0, -0.78, 1.38), 0.10, "Head")]
    for s, side in ((1, "L"), (-1, "R")):           # hidden hip / tail-root junction (inside the haunch)
        out.append(((s * 0.15, 0.40, 1.00), (s * 0.15, 0.56, 0.90), 0.13, "Leg_" + side))
    return out


HEAD_XF = []
