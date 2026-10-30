# Nightmare Stallion (Void egg #2): a proud midnight horse rebuilt to STYLE_BIBLE.md (2026-10-08 pro pass): indigo
# coat, a thick arched neck, a long horse head with a broad lilac muzzle and a blaze ending in a forehead star, fierce
# light-rimmed magenta eyes, a crest of swept-back violet flame blades, a flat 4-blade tail cascade and lilac
# feathering over dark hooves.
# Own moves: idle = rests a hind hoof (cocked hip), tail swishes, ears turn, lowers its head, then ONE proud mane toss
# and a snort; walk = high-stepping prance; roar = NEIGH (head high, jaw open, a fore-hoof raised, mane flaring);
# signature = REAR & KICK (rears up on its hind legs, paws the air with both front hooves, crashes down).
import math
from mathutils import Vector, Euler, Matrix

DISPLAY = "Nightmare Stallion"
MOTION = "Walk"
RIG = "quad"
HEIGHT = 9.0

COAT = (52, 42, 88)           # indigo base
LILAC = (152, 132, 222)       # blaze, muzzle, jaw, ear inners, hoof feathering
HOOF = (24, 18, 40)           # hooves, nostrils, brows
MANE_D = (124, 62, 222)       # mane / tail gradient: dark -> mid -> light
MANE = (170, 90, 255)
MANE_L = (232, 176, 255)
IRIS = (236, 96, 206)
MOUTH = (44, 26, 60)
SHEEN = (246, 244, 250)

# hip, knee, ankle (left side); knees bent forward (front) / hocks back (hind) so the 2-bone IK has slack
LEGS = {"FL": ((0.22, -0.38, 0.92), (0.22, -0.54, 0.42), (0.22, -0.40, 0.13)),
        "BL": ((0.175, 0.42, 0.90), (0.175, 0.58, 0.42), (0.175, 0.42, 0.13))}
NECK0, NECK1 = Vector((0, -0.42, 1.14)), Vector((0, -0.83, 1.72))
HC = Vector((0, -0.98, 1.81))                       # cranium centre
HR = Euler((math.radians(10), 0, 0), "XYZ").to_matrix()   # head carried 10 deg nose-down


def hp(p):
    """point in the cranium's local frame -> rest space"""
    return HC + HR @ Vector(p)


MANE_J = NECK0 + (NECK1 - NECK0) * 0.50 + Vector((0, 0.817, 0.577)) * 0.17   # mane pivot low on the crest
TAILP = [(0, 0.67, 1.12), (0, 0.93, 1.25), (0, 1.08, 0.94), (0, 1.12, 0.52)]


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


def slab(B, p0, p1, width, thick, color, bone, **kw):
    """flat bar from p0 to p1 in a y-z plane (its thin side along x)"""
    p0, p1 = Vector(p0), Vector(p1)
    d = p1 - p0
    th = math.degrees(math.atan2(-d.y, d.z))
    return B.add((p0 + p1) / 2, (thick, width / 2, d.length / 2), color, bone, rot=(th, 0, 0), **kw)


def inlay(B, blk, u, v, hu, hv, thick, color, ang=0.0, key="-y", **kw):
    """flush plate on the front (-y) or top (+z) face of a block whose face is flat there, rotated `ang` deg"""
    if key == "-y":
        loc = Vector((u, -(blk.h.y + thick / 2 + 0.002), v))
        half, rot = (hu, thick / 2, hv), Euler((0, math.radians(ang), 0), "XYZ")
    else:
        loc = Vector((u, v, blk.h.z + thick / 2 + 0.002))
        half, rot = (hu, hv, thick / 2), Euler((0, 0, math.radians(ang)), "XYZ")
    kw.setdefault("studs", [])
    kw.setdefault("bevel", min(0.012, thick * 0.6))
    return B.add(blk.world(loc), half, color, blk.bone, R=blk.R @ rot.to_matrix(), **kw)


def model(k):
    """STYLE_BIBLE NightmareStallion (T5 Void, quad fierce): one torso (chest 20 % bigger than the hips), a thick
    arched neck (0.6 TW) flaring into the chest, a long horse head (HW 0.62 TW, cranium + muzzle, 0.95 TH long), a
    lilac blaze running from a forehead star down the muzzle to a lilac nose, flared nostrils, fierce lilac-rimmed
    magenta eyes with dark brows, a fan of 6 swept-back 2-tone flame blades along the crest, a flat 4-blade tail
    cascade ending in a point, chunky legs (0.85 TH x 0.32 TW) with lilac feathering over dark hooves.
    No glow (wisps = particle VFX in Studio)."""
    import blockkit as bk
    B = bk.Blocks(k, seed=139, tier=5)
    D = 0.62
    # ---- one torso: chest 20 % bigger than the hips in W and H, 43 % overlap
    B.add((0, -0.18, 0.95), (0.37, 0.46, 0.35), COAT, "Chest", bot=(0.90, 0.95), density=0.75)
    B.add((0, 0.33, 0.93), (0.31, 0.36, 0.29), COAT, "Spine", bot=(0.88, 0.92), density=0.75)
    # lilac chest shield: a flush pointed inlay following the chest's tapered front face (front view: 2nd zone)
    def chest_front(z):
        return Vector((0, -0.18 - 0.46 * (0.95 + 0.05 * (z - 0.60) / 0.70) - 0.008, z))
    nf = Vector((0, -0.44, -0.0145)).normalized()
    B.bar(chest_front(0.72), chest_front(1.17), nf, 0.40, 0.012, LILAC, "Chest", bot=(1, 0.25), studs=[], rnd=0.3)
    # ---- thick arched neck (W 0.44 = 0.96 HW) flaring at the base, bottom buried in the chest, top in the head
    B.seg(NECK0, NECK1, 0.23, 0.21, COAT, "Neck", side=(1, 0, 0), ext=0.04, bot=(1.0, 0.95), top_shift=(0, 0.03),
          density=D)
    # ---- head: cranium HW 0.46, HH 0.46 (faces -y), carried 10 deg nose-down like a horse; coat-colour muzzle
    head = B.add(HC, (0.23, 0.20, 0.23), COAT, "Head", R=HR, top=(0.94, 1.0), density=D,
                 studs=["+x", "-x", "+z", "+y"])
    muz = B.add(hp((0, -0.235, -0.155)), (0.175, 0.19, 0.115), COAT, "Head", R=HR, top=(0.86, 1.0), role="limb",
                studs=[])
    # blaze: diamond star on the forehead, a stripe over the muzzle top into a lilac nose pad
    inlay(B, head, 0, 0.135, 0.044, 0.044, 0.012, LILAC, ang=45)
    inlay(B, muz, 0, -0.04, 0.045, 0.15, 0.012, LILAC, key="+z", rnd=0.2)
    inlay(B, muz, 0, -0.005, 0.135, 0.085, 0.012, LILAC, rnd=0.25)               # nose pad on the muzzle front
    # flared nostrils (slanted dark ovals, outer end up) + sheen
    for s in (1, -1):
        inlay(B, muz, s * 0.075, 0.02, 0.034, 0.024, 0.02, HOOF, ang=s * 22, rnd=0.3)
    inlay(B, muz, -0.12, 0.07, 0.015, 0.015, 0.014, SHEEN)
    # mouth: a dark line under the nose pad + dark roof (shows when the jaw opens)
    inlay(B, muz, 0, -0.098, 0.115, 0.009, 0.008, MOUTH)
    B.add(hp((0, -0.225, -0.272)), (0.14, 0.16, 0.006), MOUTH, "Head", R=HR, studs=[], bevel=0.004)
    # lower jaw (opens in the neigh)
    B.add(hp((0, -0.225, -0.31)), (0.145, 0.16, 0.045), LILAC, "Jaw", R=HR, bot=(0.85, 0.9), role="limb")
    B.add(hp((0, -0.225, -0.263)), (0.125, 0.14, 0.004), MOUTH, "Jaw", R=HR, studs=[], bevel=0.003)
    # fierce glare: thin lilac rim, magenta iris, pupil 68 % of the iris height with the glint on it, dark brows
    sp = bk.STYLE["eyes"]["fierce"]
    saved = dict(sp)
    sp.update(outline=(0.285, 0.185), iris=(0.235, 0.14))
    B.face_eyes(head, "fierce", IRIS, base=COAT, brow=HOOF, outline=(206, 186, 255), z=0.55, x=0.235, look=(0, 0.6),
                pupil_size=(0.09, 0.095), hl_size=(0.07, 0.0), brow_spec=(0.30, 0.065, 20), scale=1.1, hl_on_pupil=True)
    bk.STYLE["eyes"]["fierce"] = saved
    # ears: tall pointed horse ears, lilac lined, splayed
    for s, side in ((1, "L"), (-1, "R")):
        ear = B.add(hp((s * 0.15, 0.07, 0.30)), (0.075, 0.05, 0.13), COAT, "Ear_" + side,
                    R=HR @ Euler((math.radians(-14), math.radians(s * 12), math.radians(-s * 10)), "XYZ").to_matrix(),
                    top=(0.25, 0.5), studs=[], role="limb")
        B.add(ear.world((0, -0.052, -0.02)), (0.048, 0.008, 0.088), LILAC, "Ear_" + side, R=ear.R, top=(0.2, 1),
              studs=[], bevel=0.006)
    # ---- mane: 5 broad shark-fin flame blades standing on the crest (base along the crest line, tips swept back
    #      ~70 deg), lighter tips; kept between the poll and the withers so head tosses and nods never cut them
    d = (NECK1 - NECK0).normalized()
    nb = Vector((0, d.z, -d.y))                      # back normal of the neck (points back-up)
    L = (NECK1 - NECK0).length
    x = Vector((1, 0, 0))
    # continuous violet crest band from the withers to the poll (on the Neck: the blades stand on a surface)
    B.seg(NECK0 + d * L * 0.30 + nb * 0.205, NECK0 + d * L * 1.0 + nb * 0.235, 0.115, 0.045, MANE, "Neck",
          side=(1, 0, 0), studs=[], role="limb")
    for i, (t, h, w) in enumerate(((0.76, 0.50, 0.13), (0.65, 0.42, 0.13), (0.55, 0.46, 0.125), (0.455, 0.34, 0.10))):
        base = NECK0 + d * L * t + nb * 0.17
        y = -d                                       # along the crest, toward the withers
        z = nb
        R = Matrix((x, y, z)).transposed()
        B.add(base + z * (h / 2), (0.09, w, h / 2), MANE, "Mane", R=R, top=(0.45, 0.25), top_shift=(0, w * 0.85),
              studs=[], role="limb")
        B.add(base + z * (h * 0.78) + y * (w * 0.97), (0.095, w * 0.55, h * 0.23), MANE_L, "Mane", R=R,
              top=(0.55, 0.25), top_shift=(0, w * 0.35), studs=[], role="limb", bot=(0.95, 0.95))
    # side locks: 3 per side falling outward-back from the crest edge (the mane reads from the front and back)
    for s in (1, -1):
        for i, (t, ln) in enumerate(((0.72, 0.30), (0.60, 0.27))):
            root = NECK0 + d * L * t + nb * 0.13 + Vector((s * 0.15, 0, 0))
            dv = (nb * 0.35 + Vector((s * 0.75, 0.25, -0.55))).normalized()
            B.spike(root, dv, ln, 0.085, MANE_D, "Mane", side=(0, 1, 0), top=(0.25, 0.5))
            B.spike(root + dv * ln * 0.55, dv, ln * 0.45, 0.06, MANE, "Mane", side=(0, 1, 0), top=(0.25, 0.5))
    # ---- legs: upper block + flush shin, lilac feather ring + 3 soft tufts over a dark hoof
    for s, side in ((1, "L"), (-1, "R")):
        for fb in ("F", "B"):
            H, K, A = (X(p, s) for p in LEGS[fb + "L"])
            leg, shin, foot = "Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side
            hw, hd = (0.12, 0.13) if fb == "F" else (0.115, 0.13)
            B.seg(H - Vector((0, 0, 0.04)), K, hw, hd, COAT, leg, ext1=0.07, bot=(0.92, 0.92), density=D)
            sw, sd = hw * 0.92, hd * 0.92
            B.seg(K, A, sw, sd, COAT, shin, ext=0.05, ext1=0.02, density=D)
            dn = (A - K).normalized()
            B.seg(A - dn * 0.15, A + dn * 0.02, sw * 1.03, sd * 1.03, LILAC, shin, studs=[], role="limb")
            for dv, ln in (((s * 0.45, -0.75, -0.55), 0.095), ((s * 0.9, 0.05, -0.45), 0.10), ((0, 0.85, -0.5), 0.10)):
                dv = Vector(dv).normalized()
                root = A + Vector((dv.x * sw * 0.7, dv.y * sd * 0.7, 0.06))
                B.spike(root, dv, ln, 0.05, LILAC, shin, top=(0.45, 0.55))
            B.add(A + Vector((0, -0.012, -0.073)), (hw * 1.08, hd * 1.12, 0.057), HOOF, foot, studs=[], role="limb")
    # ---- tail cascade: 4 flat broad blades (dark -> light), the last one ending in a point
    P = [Vector(p) for p in TAILP]
    B.add((0, 0.65, 1.13), (0.09, 0.10, 0.10), COAT, "Tail1", rot=(-40, 0, 0), studs=[], role="limb")
    slab(B, P[0], P[1] + Vector((0, 0.04, 0.02)), 0.24, 0.06, MANE_D, "Tail1", studs=[], role="limb",
         top=(1, 0.75))
    slab(B, P[1] + Vector((0, -0.03, 0.05)), P[2], 0.28, 0.06, MANE, "Tail2", studs=[], role="limb", bot=(1, 0.8))
    slab(B, Vector((0, 0.98, 1.17)), Vector((0, 1.19, 0.90)), 0.17, 0.05, MANE_L, "Tail2", studs=[], role="limb",
         top=(1, 0.35))
    slab(B, P[2] + Vector((0, -0.01, 0.06)), P[3], 0.26, 0.06, MANE_L, "Tail3", studs=[], role="limb",
         top=(1, 0.08))
    B.build()
    return {"plates": B.stud_count, "TH": round(B.th, 3), "cell": round(B.pcell, 3)}


def rig(k):
    k.joint("Spine", (0, 0.42, 0.90), "Root", tail=(0, -0.4, 0))        # at the hind hips: rearing pivots here
    k.joint("Chest", (0, -0.04, 0.95), "Spine", tail=(0, -0.4, 0))
    k.joint("Neck", (0, -0.40, 1.22), "Chest", tail=tuple(NECK1 - NECK0))     # pivot at the withers line
    k.joint("Head", tuple(hp((0, 0.12, -0.20))), "Neck", tail=(0, -0.3, -0.05))     # throat pivot
    k.joint("Jaw", tuple(hp((0, -0.09, -0.29))), "Head", tail=(0, -0.2, -0.03))
    k.joint("Mane", tuple(MANE_J), "Neck", tail=(0, 0.2, 0.2))
    for s, side in ((1, "L"), (-1, "R")):
        k.joint("Ear_" + side, tuple(hp((s * 0.14, 0.07, 0.21))), "Head", tail=(0, 0, 0.2))
        for fb, parent, knee in (("F", "Chest", (0, -1, 0)), ("B", "Spine", (0, 1, 0))):
            H, K, A = (X(p, s) for p in LEGS[fb + "L"])
            k.joint("Leg_" + fb + side, H, parent)
            k.joint("Shin_" + fb + side, K, "Leg_" + fb + side)
            k.joint("Foot_" + fb + side, A, "Shin_" + fb + side, tail=(0, -0.2, 0))
            k.add_leg2("Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side, knee=knee)
    for i in range(3):
        k.joint("Tail%d" % (i + 1), TAILP[i], "Spine" if i == 0 else "Tail%d" % i,
                tail=tuple(Vector(TAILP[i + 1]) - Vector(TAILP[i])))


# ------------------------------------------------------------------ animation
import petkit as pk
import _common as cm

LEGS4 = ["Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR"]
TAIL = ["Tail1", "Tail2", "Tail3"]


def ears(k, f, a=0.0, b=None):
    """yaw: + turns the ear opening outward/back"""
    b = a if b is None else b
    k.key("Ear_L", f, rot=(0, a, 0))
    k.key("Ear_R", f, rot=(0, -b, 0))


def idle(k):
    """rests its right hind hoof on the toe (hip dropped), swishes its tail at flies, turns its ears, lowers its head
    to look at the ground, then ONE proud mane toss and a snort."""
    import bpy
    n = 160
    k.new_action("idle", n, True)

    def rest(f):
        if 4 <= f <= 16:
            return 0.5 - 0.5 * math.cos(math.pi * (f - 4) / 12)
        if 16 < f < 64:
            return 1.0
        if 64 <= f <= 76:
            return 0.5 + 0.5 * math.cos(math.pi * (f - 64) / 12)
        return 0.0

    for f in range(0, n + 1, 2):
        b = pk.wave(f, n, 0, 4)
        r = rest(f)
        k.key("Spine", f, rot=(0, 0, -2.5 * r), loc=(0, 0, 0.01 * b - 0.02 * r))
        k.key("Chest", f, rot=(-0.8 * b, 0, 1.0 * r))
        sw = 0.0
        for c in (24, 96):
            if c <= f <= c + 14:
                sw = 34 * math.sin(2 * math.pi * (f - c) / 14)
        for i, bn in enumerate(TAIL):
            k.key(bn, f, rot=(-4 + 2 * i, sw * (0.6 + 0.3 * i), 0))
    for f, nk, h, jw, mp in ((0, 0, 0, 0, 0), (70, 0, 0, 0, 0), (84, 20, 14, 0, 0), (104, 20, 16, 0, 0), (110, 12, 8, 0, 0),
                             (116, -22, -20, 6, -24), (122, -6, -4, 0, 10), (128, 0, 0, 0, -4), (136, 0, 0, 0, 0),
                             (140, -4, -4, 10, 0), (143, 0, 0, 0, 0), (160, 0, 0, 0, 0)):
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(h, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        k.key("Mane", f, rot=(-mp * 0.15, 0, 0))          # mane bristles UP as the neck goes back
    for f, a, b in ((0, 0, 0), (30, 0, 0), (36, 40, 0), (52, 40, 0), (58, 0, 0), (84, -10, -10), (104, -10, -10),
                    (110, 0, 0), (146, 0, 0), (150, 0, 40), (156, 0, 0), (160, 0, 0)):
        ears(k, f, a, b)
    for f, z in ((138, 0), (140, 0.025), (144, 0)):
        k.key("Spine", f, loc=(0, 0, z))
    k.bake_bezier_now()
    sc = bpy.context.scene
    for f in range(0, n + 1):
        sc.frame_set(f)
        r = rest(f)
        for leg in LEGS4:
            T = Vector((k.J[leg].x, k.J[leg].y, 0.0))
            if leg == "Leg_BR" and r > 0:
                T = Vector((k.J[leg].x + 0.04 * r, k.J[leg].y - 0.06 * r, 0.05 * r))
                k.solve_leg(leg, f, T, toe=40 * r)
            else:
                k.solve_leg(leg, f, T)
    k.finish()
    k.meta["planted"] = ["Leg_FL", "Leg_FR", "Leg_BL"]


def walk(k):
    """high-stepping prance (trot with lifted knees), head carried high, mane and tail flowing."""
    n = 26

    def body(f):
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(0.8 * pk.wave(f, n, 0.1, 2), 1.0 * pk.wave(f, n, 0.0), 1.5 * pk.wave(f, n, 0.0)),
              loc=(0, 0, 0.03 * b))
        k.key("Chest", f, rot=(-1.5 * pk.wave(f, n, 0.15, 2), 0, -1.2 * pk.wave(f, n, 0.25)))
        k.key("Neck", f, rot=(-6 + 3 * pk.wave(f, n, 0.2, 2), 0, 0))
        k.key("Head", f, rot=(4 - 3 * pk.wave(f, n, 0.3, 2), 0, 0))
        k.key("Jaw", f, rot=(0, 0, 0))
        k.key("Mane", f, rot=(1 + 3 * pk.wave(f, n, 0.3, 2), 0, 3 * pk.wave(f, n, 0.2)))
        ears(k, f, -6)
        for i, bn in enumerate(TAIL):
            k.key(bn, f, rot=(10 - 3 * i + 4 * pk.wave(f, n, 0.2 + 0.1 * i, 2), 6 * pk.wave(f, n, 0.3 + 0.1 * i), 0))
    return cm.quad_walk(k, n, 0.16, 0.15, body, gait="trot")


def roar(k):
    """NEIGH: lifts the head high with the mane flaring back, jaw open in a long whinny (jaw quivers), the left fore-hoof
    raised and pawing once, tail lifted; settles."""
    import bpy
    n = 72
    k.new_action("roar", n, False)
    for f, ch, nk, h, jw, mp, tl in ((0, 0, 0, 0, 0, 0, 0), (10, 2, 6, 6, 0, 0, 0), (22, -6, -28, -24, 30, -30, 30),
                                     (50, -6, -30, -25, 32, -32, 30), (60, 0, -6, -6, 4, -6, 6), (72, 0, 0, 0, 0, 0, 0)):
        k.key("Chest", f, rot=(ch, 0, 0))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(h, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        k.key("Mane", f, rot=(-mp * 0.15, 0, 0))          # mane bristles UP as the neck goes back
        k.key("Spine", f, rot=(-3 * (22 <= f <= 50), 0, 0), loc=(0, 0, 0))
        for i, bn in enumerate(TAIL):
            k.key(bn, f, rot=(tl * (1 - 0.3 * i), 0, 0))
        ears(k, f, 30 if 22 <= f <= 50 else 0)
    for f in range(24, 50, 2):
        k.key("Jaw", f, rot=(31 + (3 if (f // 2) % 2 else -3), 0, 0))
    k.bake_bezier_now()
    sc = bpy.context.scene
    for f in range(0, n + 1):
        sc.frame_set(f)
        for leg in LEGS4:
            T = Vector((k.J[leg].x, k.J[leg].y, 0.0))
            if leg == "Leg_FL" and 18 <= f <= 54:
                u = (f - 18) / 36
                T = Vector((k.J[leg].x, k.J[leg].y - 0.10 * math.sin(math.pi * u),
                            0.40 * math.sin(math.pi * min(1.0, u * 1.6)) if u < 0.62 else 0.40 * (1 - (u - 0.62) / 0.38) ** 2))
            k.solve_leg(leg, f, T)
    k.finish(loop=False)


def rear(k):
    """SIGNATURE - REAR & KICK: gathers itself, REARS up onto its hind legs (body pivoting at the hips), paws and kicks
    the air with both front hooves while whinnying with the mane streaming, then crashes down onto its front hooves."""
    import bpy
    n = 112
    k.new_action("act_rear", n, False)
    for f, p, z, ch, nk, h, jw, mp, tl in ((0, 0, 0, 0, 0, 0, 0, 0, 0), (10, 4, -0.06, 2, 6, 4, 0, 0, -6),
                                           (24, -52, -0.12, -6, 14, 20, 20, -30, 34), (60, -54, -0.12, -6, 14, 22, 24, -30, 34),
                                           (72, 6, -0.04, 4, 0, -4, 6, 14, 10), (76, 2, -0.06, 2, -6, -8, 0, 6, 4),
                                           (88, 0, 0, 0, 0, 0, 0, 0, 0), (n, 0, 0, 0, 0, 0, 0, 0, 0)):
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(ch, 0, 0))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(h, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        k.key("Mane", f, rot=(-mp * 0.15, 0, 0))          # mane bristles UP as the neck goes back
        for i, bn in enumerate(TAIL):
            k.key(bn, f, rot=(tl * (1 - 0.3 * i), 0, 0))
        ears(k, f, 20 if 20 <= f <= 64 else 0)
    for f in range(28, 58, 2):
        k.key("Jaw", f, rot=(22 + (4 if (f // 2) % 2 else -4), 0, 0))
    for f in range(26, 60, 2):
        k.key("Mane", f, rot=(4 + 3 * math.sin(2 * math.pi * f / 8), 4 * math.sin(2 * math.pi * f / 11), 0))
    k.bake_bezier_now()
    sc = bpy.context.scene

    def paw(f, ph):
        w = math.sin(2 * math.pi * ((f - 24) / 14 + ph))
        return w

    for f in range(0, n + 1):
        sc.frame_set(f)
        for leg in LEGS4:
            fr = leg[4] == "F"
            side = leg[5:]
            if fr and 14 <= f <= 68:
                if f <= 22 or f >= 62:                                # tuck while rising / unfold to land
                    u = 1.0 if 22 < f < 62 else ((f - 14) / 8 if f <= 22 else (68 - f) / 6)
                    k.key(leg, f, rot=(-24 * u, 0, 0))
                    k.key("Shin_" + side, f, rot=(115 * u, 0, 0))
                    k.key("Foot_" + side, f, rot=(30 * u, 0, 0))
                else:                                                 # pawing / kicking the air
                    w = paw(f, 0.0 if side == "FL" else 0.5)
                    k.key(leg, f, rot=(-24 - 22 * w, 0, 0))
                    k.key("Shin_" + side, f, rot=(110 - 35 * w, 0, 0))
                    k.key("Foot_" + side, f, rot=(30 + 15 * w, 0, 0))
            else:
                k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, 0.0)))
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    rear(k)
    return stride


def check_pairs():
    P = [("Leg_FL", "Leg_BL"), ("Leg_FR", "Leg_BR"), ("Leg_FL", "Leg_FR"), ("Leg_BL", "Leg_BR"),
         ("Shin_FL", "Shin_FR"), ("Shin_BL", "Shin_BR"), ("Shin_FL", "Shin_BL"), ("Shin_FR", "Shin_BR"),
         ("Foot_FL", "Foot_FR"), ("Foot_FL", "Foot_BL"), ("Foot_FR", "Foot_BR")]
    for a in ("Head", "Jaw", "Neck"):
        for b in ("Leg_FL", "Leg_FR", "Shin_FL", "Shin_FR", "Foot_FL", "Foot_FR"):
            P.append((a, b))
    P += [("Head", "Chest"), ("Jaw", "Chest"), ("Mane", "Chest"), ("Mane", "Head"), ("Ear_L", "Mane"),
          ("Ear_R", "Mane")]
    for b in ("Leg_BL", "Leg_BR", "Shin_BL", "Shin_BR"):
        P.append(("Tail3", b))
        P.append(("Tail2", b))
    return P


def joints():
    """the deep neck's root overlaps the shoulders inside the chest (hidden)"""
    b = Vector(NECK0)
    return [(b, b, 0.30, "Neck")]
