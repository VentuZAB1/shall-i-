# Venom Basilisk (Wood/Grass egg, NEW 5% pet, 2026-10-14) - FIERCE style "the serpent king's herald": a sprawled
# jungle lizard built from tapered blocks under a Roblox stud skin, in the family of our quadrupeds (Ivonrath's legs,
# torso tuck + belly recipe, fierce_eye). Hero feature: a ROYAL CROWN FRILL - 7 thorn spines fanned round the back of
# a wedge VIPER head with venom-purple membranes (flares in the hiss). Basilisk-lizard back SAIL with purple webbing,
# horned-viper brows, long ivory fangs with venom tips, forked venom tongue (Tongue bone, hidden in the jaw), dark
# stripes over jungle green, pale belly, banded whip tail ending in a small purple tail-frill. No glow.
import math
from mathutils import Vector, Matrix

DISPLAY = "Venom Basilisk"
MOTION = "Walk"
RIG = "quad"
HEIGHT = 8.0        # total height (frill tips) in studs at x1 - between Mossback (7) and Treant (10)

# Blender colours (Roblox renders ~0.6x darker)
GREEN = (72, 182, 78)        # jungle green hide
GREEN_D = (26, 90, 50)       # back, stripes, socks, brows, spines, tail bands
PALE = (218, 232, 146)       # belly, throat, chin
PALE_D = (176, 196, 104)     # belly scute gaps
VENOM = (198, 78, 255)       # ACCENT: frill / sail / tail-frill membranes, eyes, fang tips
VENOM_D = (118, 36, 178)     # tongue
VENOM_HOT = (246, 214, 255)
IVORY = (240, 234, 210)      # spine tips, teeth, fangs
BLACK = (14, 14, 22)
MOUTH = (96, 20, 62)

LEGS = {"F": ((0.20, -0.40, 0.50), (0.36, -0.32, 0.28), (0.31, -0.44, 0.09), (0.31, -0.50, 0.04)),
        "B": ((0.20, 0.34, 0.50), (0.36, 0.22, 0.30), (0.33, 0.45, 0.12), (0.33, 0.39, 0.04))}
NECKP = [(0, -0.50, 0.60), (0, -0.68, 0.70), (0, -0.80, 0.74)]          # Neck, Neck2, Head (throat pivot)
TAILP = [(0, 0.52, 0.54), (0, 0.85, 0.46), (0, 1.16, 0.38), (0, 1.44, 0.33), (0, 1.68, 0.30)]
FRILL0 = Vector((0, -0.80, 0.86))       # frill root (back of the skull top)
FRILL_TILT = 12.0                       # modelled lean-back of the fan (deg): faces the high-behind game camera
FRILL_A = (-84, -58, -30, 0, 30, 58, 84)
FRILL_L = (0.27, 0.37, 0.45, 0.51, 0.45, 0.37, 0.27)


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


def surf_hit(B, blks, origin, direction):
    """exact hit point + normal on the bevelled meshes of `blks` (seats inlays ON tapered / rounded faces)"""
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


def surf_strip(B, blks, origins, direction, width, thick, color, bone, proud=0.009, tip0=False, tip1=False, **kw):
    """flush strip of bars along a surface: ray-cast every origin along direction, bars between the hits"""
    hits = [surf_hit(B, blks, o, direction) for o in origins]
    kw.setdefault("studs", [])
    kw.setdefault("bevel", 0.004)
    out = []
    for i in range(len(hits) - 1):
        (a, na), (b, nb) = hits[i], hits[i + 1]
        n = (na + nb).normalized()
        a2, b2 = a + n * (proud - thick), b + n * (proud - thick)
        if tip0 and i == 0:
            out.append(B.bar(b2, a2, n, width, thick, color, bone, top=(1, 0.15), **kw))
        elif tip1 and i == len(hits) - 2:
            out.append(B.bar(a2, b2, n, width, thick, color, bone, top=(1, 0.15), **kw))
        else:
            out.append(B.bar(a2, b2, n, width, thick, color, bone, **kw))
    return out


def fierce_eye(B, c, s, bone="Head", yaw=20.0, tilt=18.0, sc=1.0):
    """black socket (tilted, inner corner down) -> venom slit -> hot highlight on the outer half, vertical reptile
    pupil, heavy dark brow above (Ivonrath recipe, venom colours)"""
    from mathutils import Euler
    R = Euler((0, math.radians(-s * tilt), math.radians(s * yaw)), "XYZ").to_matrix()
    n = R @ Vector((0, -1, 0))
    c = Vector(c)
    B.add(c, (0.052 * sc, 0.008, 0.025 * sc), BLACK, bone, R=R, studs=[], role="detail", bevel=0.004)
    B.add(c + n * 0.006, (0.044 * sc, 0.006, 0.0135 * sc), VENOM, bone, R=R, studs=[], role="detail", bevel=0.003)
    B.add(c + n * 0.011 + R @ Vector((s * 0.022 * sc, 0, 0.002)), (0.014 * sc, 0.004, 0.006 * sc), VENOM_HOT, bone,
          R=R, studs=[], role="detail", bevel=0.002)
    B.add(c + n * 0.011 + R @ Vector((-s * 0.004, 0, 0)), (0.006 * sc, 0.004, 0.0135 * sc), BLACK, bone, R=R,
          studs=[], role="detail", bevel=0.002)
    Rb = Euler((0, math.radians(-s * 20), math.radians(s * yaw)), "XYZ").to_matrix()
    B.add(c + Vector((0, 0, 0.042 * sc)) + n * 0.022, (0.068 * sc, 0.03, 0.026 * sc), GREEN_D, bone, R=Rb,
          role="detail", bevel=0.01)


def thorn(B, root, d, L, w, bone):
    """one thorn spine: dark shaft (0 -> 0.68 L) + ivory point (0.62 L -> L), flat-sided like Ivonrath's crests"""
    import blockkit as bk
    d = Vector(d).normalized()
    root = Vector(root)
    R = bk.frame_from(root, root + d, (1, 0, 0) if abs(d.x) < 0.7 else (0, 1, 0))
    B.add(root + d * L * 0.34, (w * 0.55, w, L * 0.34), GREEN_D, bone, R=R, top=(0.7, 0.62), role="limb")
    B.add(root + d * L * 0.81, (w * 0.55 * 0.7, w * 0.62, L * 0.19), IVORY, bone, R=R, top=(0.12, 0.1), role="limb")
    return root + d * L


def web(B, roots, tips, thick, color, bone, scallop=0.30):
    """membrane between neighbouring spines: root_i, tip_i, scalloped notch, tip_j, root_j (fan from the root mid)"""
    for (r0, t0), (r1, t1) in zip(zip(roots, tips), zip(roots[1:], tips[1:])):
        a, b = r0.lerp(t0, 0.90), r1.lerp(t1, 0.90)
        rm, tm = r0.lerp(r1, 0.5), a.lerp(b, 0.5)
        notch = tm.lerp(rm, scallop)
        B.poly([rm, r0, a, notch, b, r1], thick, color, bone)


def frill_dirs():
    """fan directions of the crown frill: in-plane angle a (0 = straight up), plane leaned back FRILL_TILT deg,
    every spine also swept back a little"""
    T = math.radians(FRILL_TILT)
    out = []
    for a in FRILL_A:
        ar = math.radians(a)
        u = Vector((math.sin(ar), 0, math.cos(ar)))
        d = Vector((u.x, u.z * math.sin(T) + 0.16 + 0.42 * abs(u.x), u.z * math.cos(T))).normalized()   # cupped ruff
        out.append((u, d))
    return out


def model(k):
    import blockkit as bk
    B = bk.Blocks(k, seed=503, tier=3, plates=False)
    # ---------------- torso: low lizard ribcage tapering underneath, tucked waist, heavy hips (Ivonrath recipe)
    B.add((0, -0.24, 0.52), (0.22, 0.30, 0.19), GREEN, "Chest", bot=(0.70, 0.60), top=(0.88, 0.95), rnd=0.30)
    B.add((0, -0.34, 0.70), (0.17, 0.20, 0.05), GREEN_D, "Chest", top=(0.70, 0.80))                 # shoulders
    B.seg((0, -0.10, 0.36), (0, 0.26, 0.44), 0.15, 0.07, GREEN, "Spine", top=(0.82, 0.75), side=(1, 0, 0))   # tuck
    B.add((0, 0.10, 0.53), (0.17, 0.20, 0.14), GREEN, "Spine", bot=(0.74, 0.72), top=(0.95, 1), rnd=0.30)   # waist
    B.add((0, 0.34, 0.53), (0.19, 0.20, 0.15), GREEN, "Spine", rot=(-6, 0, 0), top=(0.84, 0.90), bot=(0.85, 0.9))
    B.add((0, 0.06, 0.675), (0.10, 0.36, 0.022), GREEN_D, "Spine")                                   # saddle
    # pale belly: brisket + scute strip along the tuck, flank band rising with the tuck; scute gaps
    B.add((0, -0.26, 0.345), (0.14, 0.18, 0.022), PALE, "Chest", bot=(0.8, 0.9), studs=[])
    belly = B.seg((0, -0.10, 0.293), (0, 0.24, 0.37), 0.11, 0.022, PALE, "Spine", side=(1, 0, 0), top=(0.8, 1),
                  ext=0.03)
    torso = [blk for blk in B.items if blk.bone in ("Chest", "Spine")][:5]
    for s in (1, -1):
        pts = [(-0.38 + 0.60 * t, 0.41 + 0.09 * t) for t in (0, 0.25, 0.5, 0.75, 1.0)]
        surf_strip(B, torso, [(s * 1.0, y, z) for y, z in pts[:3]], (-s, 0, 0), 0.065, 0.010, PALE, "Chest",
                   proud=0.009)
        surf_strip(B, torso, [(s * 1.0, y, z) for y, z in pts[2:]], (-s, 0, 0), 0.065, 0.010, PALE, "Spine",
                   proud=0.009)
        # dark tiger stripes over the flank (top -> down-back), 5 per side
        for y, zt, bone in ((-0.44, 0.67, "Chest"), (-0.25, 0.67, "Chest"), (-0.04, 0.62, "Spine"),
                            (0.16, 0.62, "Spine"), (0.36, 0.63, "Spine")):
            surf_strip(B, torso, [(s * 1.0, y, zt), (s * 1.0, y + 0.04, zt - 0.08), (s * 1.0, y + 0.09, zt - 0.16)],
                       (-s, 0, 0), 0.05, 0.010, GREEN_D, bone, proud=0.010, tip1=True)
    for y in (-0.38, -0.26, -0.14):
        B.add((0, y, 0.320), (0.12, 0.009, 0.004), PALE_D, "Chest", studs=[], role="detail", bevel=0.002)
    for t in (0.2, 0.45, 0.7, 0.92):
        B.add(belly.world((0, 0.024, (t - 0.5) * 2 * belly.h.z)), (0.09, 0.004, 0.009), PALE_D, "Spine",
              R=belly.R, studs=[], role="detail", bevel=0.002)
    # ---------------- serpent neck (Neck + Neck2), pale throat, dark bands
    N0, N1, N2 = (Vector(p) for p in NECKP)
    B.seg(N0 + Vector((0, 0.04, -0.04)), N1, 0.15, 0.13, GREEN, "Neck", ext=0.06, ext1=0.03)
    B.seg(N1, N2 + Vector((0, -0.02, 0.03)), 0.135, 0.115, GREEN, "Neck2", ext=0.04, ext1=0.03)
    B.seg((0, -0.52, 0.475), (0, -0.74, 0.615), 0.10, 0.045, PALE, "Neck", ext=0.02)
    B.seg((0, -0.73, 0.61), (0, -0.84, 0.655), 0.09, 0.04, PALE, "Neck2", ext=0.02)
    for y, z, bone in ((-0.56, 0.71, "Neck"), (-0.70, 0.79, "Neck2")):
        B.add((0, y, z), (0.10, 0.035, 0.02), GREEN_D, bone, rot=(-30, 0, 0), top=(0.8, 1))
    # ---------------- wedge VIPER head: wide jaw-muscle back, tapering skull + snout, horned brows
    B.seg((0, -0.80, 0.80), (0, -1.04, 0.79), 0.17, 0.095, GREEN, "Head", top=(0.72, 0.9), ext=0.02)  # skull
    B.add((0, -0.90, 0.897), (0.11, 0.10, 0.018), GREEN_D, "Head", top=(0.8, 0.8))                   # dark crown
    B.seg((0, -1.00, 0.785), (0, -1.30, 0.76), 0.118, 0.056, GREEN, "Head", top=(0.62, 0.8), ext=0.01)   # snout
    B.seg((0, -1.02, 0.835), (0, -1.26, 0.808), 0.045, 0.016, GREEN_D, "Head", top=(0.6, 0.7))       # snout ridge
    for s in (1, -1):
        B.add((s * 0.03, -1.285, 0.79), (0.011, 0.016, 0.007), BLACK, "Head", rot=(0, 0, s * 18), studs=[],
              role="detail", bevel=0.003)                                                       # nostril
    for i, y in enumerate((-1.06, -1.11, -1.16, -1.21)):                                       # upper teeth
        for s in (1, -1):
            B.spike((s * (0.085 - 0.012 * i), y, 0.72), (s * 0.1, 0, -1), 0.035, 0.011, IVORY, "Head")
    for s in (1, -1):                                                                           # VENOM FANGS
        f0 = Vector((s * 0.048, -1.255, 0.725))
        B.spike(f0, (0, -0.22, -1), 0.085, 0.018, IVORY, "Head", top=(0.45, 0.45))
        B.spike(f0 + Vector((0, -0.018, -0.082)), (0, -0.25, -1), 0.045, 0.0085, VENOM, "Head", top=(0.12, 0.12))
    B.seg((0, -0.86, 0.665), (0, -1.28, 0.675), 0.105, 0.034, GREEN, "Jaw", top=(0.68, 0.9), ext=0.02)  # lower jaw
    B.seg((0, -0.88, 0.635), (0, -1.24, 0.645), 0.075, 0.014, PALE, "Jaw", top=(0.7, 1), ext=0.0)     # pale chin
    B.add((0, -1.06, 0.706), (0.075, 0.19, 0.006), MOUTH, "Jaw", top=(0.7, 1), studs=[], role="detail", bevel=0.003)
    for i, y in enumerate((-1.08, -1.14, -1.20)):                                              # lower teeth
        for s in (1, -1):
            B.spike((s * (0.072 - 0.012 * i), y, 0.705), (s * 0.1, 0, 1), 0.032, 0.010, IVORY, "Jaw")
    B.add((0, -0.90, 0.69), (0.145, 0.07, 0.05), GREEN, "Jaw", top=(0.95, 0.9))                     # jaw muscle
    # forked venom tongue: lives inside the closed jaw, the idle / hiss slide it out along the jaw (loc keys)
    B.seg((0, -0.92, 0.688), (0, -1.16, 0.688), 0.016, 0.006, VENOM_D, "Tongue", studs=[], role="detail")
    for s in (1, -1):
        B.spike((0, -1.155, 0.688), (s * 0.35, -1, 0), 0.06, 0.008, VENOM_D, "Tongue", side=(0, 0, 1))
    for s in (1, -1):
        B.add((s * 0.105, -1.005, 0.855), (0.05, 0.03, 0.04), GREEN, "Head", rot=(0, 0, s * 26), role="detail",
              bevel=0.01)                                                                       # eye socket
        fierce_eye(B, (s * 0.09, -1.035, 0.862), s, yaw=26, sc=0.95)
        for dx, dy, L in ((0.0, 0.0, 0.085), (0.03, 0.035, 0.065)):                            # horned-viper brows
            B.spike((s * (0.10 + dx), -1.02 + dy, 0.90), (s * 0.35, 0.45, 1), L, 0.022, GREEN_D, "Head",
                    top=(0.12, 0.35))
        for z, dz, L in ((0.72, -0.25, 0.13), (0.79, 0.0, 0.11)):                              # cheek thorns
            B.spike((s * 0.16, -0.84, z), (s * 0.6, 0.8, dz), L, 0.034, GREEN_D, "Head", top=(0.12, 0.35))
    # ---------------- ROYAL CROWN FRILL (hero): 7 thorn spines fanned round the back of the skull, venom webbing
    roots, tips = [], []
    for (u, d), L in zip(frill_dirs(), FRILL_L):
        r = FRILL0 + Vector((u.x * 0.10, 0.02, u.z * 0.03 - 0.01))
        roots.append(r)
        tips.append(thorn(B, r - d * 0.02, d, L, 0.030, "Frill"))
    web(B, roots, tips, 0.02, VENOM, "Frill", scallop=0.28)
    B.seg(FRILL0 + Vector((0, 0.03, -0.03)), FRILL0 + Vector((0, -0.04, 0.03)), 0.12, 0.035, GREEN_D, "Frill",
          side=(1, 0, 0), top=(0.85, 1))                                                       # frill collar
    # ---------------- basilisk BACK SAIL: thorn spines withers -> hips with venom webbing
    sy = (-0.46, -0.30, -0.14, 0.02, 0.18, 0.34)
    sl = (0.24, 0.34, 0.42, 0.42, 0.34, 0.22)
    sb = ("Chest", "Chest", "Chest", "Spine", "Spine", "Spine")
    sd = Vector((0, 0.32, 1)).normalized()
    roots = [Vector((0, y, 0.70)) for y in sy]
    tips = [thorn(B, r - sd * 0.03, sd, L, 0.028, b) for r, L, b in zip(roots, sl, sb)]
    web(B, roots[:3], tips[:3], 0.018, VENOM, "Chest", scallop=0.32)
    web(B, roots[2:], tips[2:], 0.018, VENOM, "Spine", scallop=0.32)
    # ---------------- sprawled legs: elbows / knees out, dark socks, 4 splayed black claws, spur (Ivonrath)
    for s, side in ((1, "L"), (-1, "R")):
        for fb in ("F", "B"):
            H, K, A, P = (Vector(X(p, s)) for p in LEGS[fb])
            leg, shin, foot = "Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side
            if fb == "F":
                B.seg(H + Vector((0, 0, 0.05)), K, 0.085, 0.10, GREEN, leg, ext1=0.04, top=(0.8, 0.8))
                B.seg(K, A, 0.066, 0.07, GREEN_D, shin, top=(0.85, 0.85), ext=0.04, ext1=0.02)
            else:
                B.seg(H + Vector((0, 0.02, 0.05)), K, 0.10, 0.14, GREEN, leg, ext1=0.04, top=(0.75, 0.7))
                B.seg(K, A, 0.066, 0.07, GREEN_D, shin, top=(0.85, 0.85), ext=0.04, ext1=0.02)
                B.seg(A, P + Vector((0, 0.03, 0.03)), 0.056, 0.056, GREEN_D, foot, ext=0.03)
            B.spike(K + Vector((s * 0.05, 0.03, 0.0)), (s * 0.7, 0.7, 0.0), 0.10, 0.03, GREEN_D,
                    shin if fb == "F" else leg)                                              # elbow / knee spur
            B.add(P, (0.08, 0.095, 0.042), GREEN_D, foot, top=(0.85, 0.80))
            for gx in (-0.055, -0.018, 0.018, 0.055):
                B.spike((P.x + gx, P.y - 0.085, 0.033), (gx * 2.2, -1, -0.5), 0.085, 0.015, BLACK, foot)
    # ---------------- banded whip tail (4 bones): pale underside, dark bands, Tail1 sail, thorn pairs
    T = [Vector(p) for p in TAILP]
    dims = ((0.15, 0.13), (0.115, 0.10), (0.085, 0.075), (0.06, 0.052))
    for i, ((a, b), (w, d)) in enumerate(zip(zip(T, T[1:]), dims)):
        bone = "Tail%d" % (i + 1)
        B.seg(a, b, w, d, GREEN, bone, ext=0.08 if i == 0 else 0.03, ext1=0.02, top=(0.82, 0.82))
        B.seg(a + Vector((0, 0, -d + 0.012)), b + Vector((0, 0, -dims[min(i + 1, 3)][1] * 0.82 + 0.012)), w * 0.7,
              0.014, PALE, bone, ext=0.02)
        B.seg(a.lerp(b, 0.52), a.lerp(b, 0.72), w * 0.97, d * 1.04, GREEN_D, bone, top=(0.94, 0.94))   # band
        if i in (1, 2):
            for s in (1, -1):
                B.spike(a.lerp(b, 0.35) + Vector((s * w * 0.8, 0, d * 0.4)), (s * 0.55, 0.65, 0.5),
                        0.09 - 0.015 * i, 0.024, GREEN_D, bone, top=(0.12, 0.35))
    troots = [T[0] + Vector((0, 0.10, 0.12)), T[0] + Vector((0, 0.26, 0.09))]
    td = Vector((0, 0.5, 1)).normalized()
    ttips = [thorn(B, r - td * 0.03, td, L, 0.024, "Tail1") for r, L in zip(troots, (0.18, 0.12))]
    web(B, troots, ttips, 0.016, VENOM, "Tail1", scallop=0.35)
    # tail-frill: 3 thorns fanned up / back / down at the tip with venom webbing (echo of the crown)
    tip = T[4]
    fr = [tip + Vector((0, -0.02, 0.025)), tip + Vector((0, 0.0, 0.0)), tip + Vector((0, -0.02, -0.025))]
    fd = [Vector((0, 0.55, 0.85)), Vector((0, 1, 0.05)), Vector((0, 0.6, -0.6))]
    ft = [thorn(B, r, d, L, 0.024, "Tail4") for r, d, L in zip(fr, fd, (0.20, 0.22, 0.15))]
    web(B, fr, ft, 0.016, VENOM, "Tail4", scallop=0.25)
    B.build()
    mn, mx = k.bounds()
    pitch = 0.2243 * (mx.z - mn.z) / HEIGHT
    bk.stud_skin(k, pitch)
    return {"TH": round(B.th, 3), "pitch": round(pitch, 4), "H": round(mx.z - mn.z, 3)}


# ------------------------------------------------------------------ rig
def rig(k):
    k.joint("Spine", (0, 0.18, 0.52), "Root", tail=(0, -0.4, 0))
    k.joint("Chest", (0, -0.12, 0.52), "Spine", tail=(0, -0.4, 0))
    k.joint("Neck", NECKP[0], "Chest", tail=(0, -0.2, 0.1))
    k.joint("Neck2", NECKP[1], "Neck", tail=(0, -0.13, 0.04))
    k.joint("Head", NECKP[2], "Neck2", tail=(0, -0.35, 0.03))          # throat pivot
    k.joint("Jaw", (0, -0.88, 0.70), "Head", tail=(0, -0.3, 0))
    k.joint("Tongue", (0, -0.92, 0.688), "Jaw", tail=(0, -0.2, 0))
    k.joint("Frill", tuple(FRILL0), "Head", tail=(0, 0.1, 0.2))
    k.joint("Venom", (0, -1.34, 0.72), "Head", tail=(0, -0.25, 0))     # venom-spit VFX anchor (no mesh)
    for s, side in ((1, "L"), (-1, "R")):
        for fb, parent, knee in (("F", "Chest", (s * 0.8, 1, 0)), ("B", "Spine", (s * 0.8, -1, 0))):
            H, K, A, P = (X(p, s) for p in LEGS[fb])
            k.joint("Leg_" + fb + side, H, parent)
            k.joint("Shin_" + fb + side, K, "Leg_" + fb + side)
            k.joint("Foot_" + fb + side, A, "Shin_" + fb + side, tail=(0, -0.15, 0))
            k.add_leg2("Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side, knee=knee)
    k.joint("Tail1", TAILP[0], "Spine")
    k.joint("Tail2", TAILP[1], "Tail1")
    k.joint("Tail3", TAILP[2], "Tail2")
    k.joint("Tail4", TAILP[3], "Tail3", tail=(0, 0.3, 0))


LEGS4 = ["Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR"]
TAIL = ["Tail1", "Tail2", "Tail3", "Tail4"]


def check_pairs():
    P = []
    for s in ("L", "R"):
        P += [("Leg_F" + s, "Leg_B" + s), ("Shin_F" + s, "Shin_B" + s), ("Foot_F" + s, "Foot_B" + s)]
    P += [("Shin_FL", "Shin_FR"), ("Shin_BL", "Shin_BR"), ("Foot_FL", "Foot_FR"), ("Foot_BL", "Foot_BR")]
    for a in ("Head", "Jaw", "Frill"):
        for b in ("Chest", "Shin_FL", "Shin_FR", "Foot_FL", "Foot_FR", "Leg_FL", "Leg_FR"):
            P.append((a, b))
    P += [("Jaw", "Neck"), ("Jaw", "Neck2"), ("Head", "Neck"), ("Frill", "Neck"), ("Frill", "Neck2")]
    for t in ("Tail2", "Tail3", "Tail4"):
        for b in ("Head", "Jaw", "Neck", "Neck2", "Chest", "Shin_BL", "Shin_BR", "Foot_BL", "Foot_BR", "Foot_FL",
                  "Foot_FR"):
            P.append((t, b))
    return P


def joints():
    return [(NECKP[2], (0, -0.98, 0.80), 0.20, "Head"), (NECKP[1], NECKP[1], 0.17, "Neck2"),
            (NECKP[0], NECKP[0], 0.20, "Neck")]


HEAD_XF = []
