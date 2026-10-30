# Cerberus (Magma egg #3, tier 4): a three-headed hellhound rebuilt to STYLE_BIBLE.md (2026-10-08 pro pass): a broad
# charcoal Rottweiler body with tan points (chest V, socks, muzzles, brow dots), three big heads in a fan on thick
# necks, each with a red spiked collar and its OWN personality and ear pose: LEFT = the goof (round bold eyes looking
# off, tongue out, one ear flopped), CENTRE = the alpha (15 % bigger, higher, fierce eyes, 24 deg brows, snarl with
# fangs, upright ears), RIGHT = the grump (heavy half lids, a down-turned mouth, ears pinned back); a tail ending in a
# flat two-tone flame point (fire = particle VFX in Studio, no Neon).
# Own moves: idle = the left head yawns and nods off, the center head keeps guard (scans with holds), the right head pants
# and tilts at its brother; walk = heavy trot; roar = THREE-HEAD CHORUS (left, center, right howl in turn, then all
# three together); signature = TRIPLE SNAP (left snaps left, right snaps right, center lunges, then all three bite
# together in a pounce).
import math
from mathutils import Vector, Euler, Matrix

DISPLAY = "Cerberus"
MOTION = "Walk"
RIG = "quad"
HEIGHT = 8.5

CHAR = (60, 54, 74)            # V 29 % (bible floor 28 % for dark pets)
TAN = (214, 124, 54)
NOSE = (20, 18, 28)
COLLAR = (204, 44, 54)
SPIKE = (222, 222, 232)
TONGUE = (236, 110, 140)
IRIS = (255, 176, 44)
MOUTH = (110, 26, 44)
FANG = (246, 244, 250)
FLAME = (255, 128, 40)
FLAME_Y = (255, 204, 80)

# leg joints (left side): hip, knee (set back: IK slack, elbows/hocks fold back), ankle
LEGS = {"FL": ((0.26, -0.42, 0.66), (0.26, -0.32, 0.38), (0.26, -0.42, 0.11)),     # outer faces flush with the
        "BL": ((0.19, 0.40, 0.66), (0.19, 0.50, 0.38), (0.19, 0.40, 0.11))}     # tapered chest / hips flanks
# head tag -> (neck base, head joint at the throat, yaw, scale)
HEADS = {"C": ((0, -0.56, 1.14), (0, -0.84, 1.28), 0.0, 1.15),
         "L": ((0.34, -0.50, 1.06), (0.70, -0.72, 1.14), 20.0, 1.0),
         "R": ((-0.34, -0.50, 1.06), (-0.70, -0.72, 1.14), -20.0, 1.0)}
TH = 0.76
TAILP = [(0, 0.66, 1.04), (0, 0.88, 1.10), (0, 1.06, 1.19), (0, 1.20, 1.28)]     # low, swept back (no horn in front)


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


def _rz(deg):
    return Matrix.Rotation(math.radians(deg), 3, "Z")


def head(B, tag):
    """one head in head-local space (throat joint at the origin, facing -Y, scaled), turned by the head's yaw"""
    base, J, yaw, sc = HEADS[tag]
    J = Vector(J)
    Rz = _rz(yaw)
    hb, jb, nb = "Head_" + tag, "Jaw_" + tag, "Neck_" + tag

    def P(p):
        return J + Rz @ (Vector(p) * sc)

    def add(p, h, color, bone, rot=(0, 0, 0), **kw):
        R = Rz @ Euler([math.radians(a) for a in rot], "XYZ").to_matrix()
        kw.setdefault("studs", [])
        return B.add(P(p), tuple(v * sc for v in h), color, bone, R=R, **kw)

    def spike(p, d, ln, w, color, bone, **kw):
        return B.spike(P(p), Rz @ Vector(d), ln * sc, w * sc, color, bone, **kw)

    hd = add((0, -0.22, 0.20), (0.275, 0.24, 0.21), CHAR, hb, top=(0.94, 0.94), density=0.62,
             studs=["+x", "-x", "+z", "+y"])
    add((0, -0.51, 0.085), (0.165, 0.17, 0.095), TAN, hb, top=(0.88, 1.0), role="limb")            # tan muzzle
    add((0, -0.665, 0.178), (0.068, 0.036, 0.042), NOSE, hb, role="limb")                          # big nose
    add((-0.026, -0.703, 0.198), (0.012, 0.004, 0.012), (246, 244, 250), hb, bevel=0.003)          # sheen
    add((0, -0.47, -0.035), (0.145, 0.16, 0.045), TAN, jb, bot=(0.85, 0.9), role="limb")            # lower jaw
    add((0, -0.48, 0.012), (0.12, 0.13, 0.004), MOUTH, jb, bevel=0.003)
    for s in (1, -1):                                                    # tan Rottweiler cheek marks (flush)
        add((s * 0.215, -0.466, 0.075), (0.05, 0.006, 0.045), TAN, hb, bevel=0.005)
    if tag == "C":            # the alpha: fierce eyes, 24 deg tan brows, snarl with fangs, upright ears
        B.face_eyes(hd, "fierce", IRIS, base=CHAR, brow=TAN, look=(0, 0.6), z=0.66, pupil_size=(0.085, 0.088),
                    hl_size=(0.06, 0.0), brow_spec=(0.22, 0.075, 24), hl_on_pupil=True)
        add((0, -0.682, 0.038), (0.13, 0.006, 0.032), MOUTH, hb, bevel=0.006)
        for s in (1, -1):
            spike((s * 0.085, -0.688, 0.07), (0, 0, -1), 0.075, 0.022, FANG, hb, role="limb")
            ear = add((s * 0.17, -0.14, 0.47), (0.08, 0.04, 0.12), CHAR, hb, rot=(-6, s * 6, -s * 10), top=(0.25, 0.5),
                      role="limb")
            B.add(ear.world((0, -0.042, -0.02)), (0.05 * sc, 0.006, 0.08 * sc), TAN, hb, R=ear.R, top=(0.2, 1),
                  studs=[], bevel=0.006)
    elif tag == "L":          # the goof: round bold eyes looking off, tongue out, one ear up one flopped
        B.face_eyes(hd, "bold", IRIS, base=CHAR, brow=TAN, look=(0.6, 0.5), z=0.64, pupil_size=(0.11, 0.13),
                    hl_size=(0.07, 0.0), brow_spec=(0.12, 0.075, -8), hl_on_pupil=True)
        add((0, -0.682, 0.04), (0.10, 0.006, 0.025), MOUTH, hb, bevel=0.006)
        add((0.05, -0.66, -0.10), (0.06, 0.016, 0.10), TONGUE, jb, rot=(12, 0, -8), role="limb")      # tongue out
        ear = add((-0.18, -0.14, 0.46), (0.08, 0.04, 0.12), CHAR, hb, rot=(-6, 0, 18), top=(0.3, 0.5), role="limb")
        B.add(ear.world((0, -0.042, -0.02)), (0.05 * sc, 0.006, 0.08 * sc), TAN, hb, R=ear.R, top=(0.2, 1), studs=[],
              bevel=0.006)
        add((0.30, -0.14, 0.30), (0.035, 0.085, 0.13), CHAR, hb, rot=(0, -18, 0), top=(0.8, 0.6), role="limb")  # flop
    else:                     # the grump: heavy half lids, flat brows, down-turned mouth, ears pinned back
        B.face_eyes(hd, "bold", IRIS, base=CHAR, brow=TAN, look=(0, 0.2), z=0.64, lids=0.38, pupil_size=(0.10, 0.11),
                    hl_size=(0.065, 0.0), brow_spec=(0.16, 0.07, 4), hl_on_pupil=True)
        for s in (1, -1):
            add((s * 0.05, -0.682, 0.05), (0.055, 0.006, 0.013), MOUTH, hb, rot=(0, s * 20, 0), bevel=0.004)
            add((s * 0.19, -0.03, 0.40), (0.07, 0.11, 0.035), CHAR, hb, rot=(28, 0, -s * 16), top=(0.5, 0.3),
                role="limb")
    # neck + red spiked collar
    base = Vector(base)
    top = J + Rz @ Vector((0, 0.03, 0.10 * sc))
    B.seg(base, top, 0.16 if tag == "C" else 0.17, 0.16 * sc, CHAR, nb, side=Rz @ Vector((1, 0, 0)), ext=0.10, studs=[])
    d = (top - base).normalized()
    c = base.lerp(top, 0.60)
    B.seg(c - d * 0.055, c + d * 0.055, 0.215 * sc, 0.205 * sc, COLLAR, nb, side=Rz @ Vector((1, 0, 0)), studs=[],
          role="limb")
    side = (Rz @ Vector((1, 0, 0)))
    fwd = d.cross(side).normalized()
    if fwd.y > 0:
        fwd = -fwd
    for a in (-60, 0, 60):
        r = (fwd * math.cos(math.radians(a)) + side * math.sin(math.radians(a))).normalized()
        B.spike(c + r * 0.19 * sc, r, 0.12, 0.04, SPIKE, nb, top=(0.15, 0.15), role="limb")
    for s in (1, -1):
        r = side * s
        B.spike(c + r * 0.20 * sc, r, 0.11, 0.037, SPIKE, nb, top=(0.15, 0.15), role="limb")


def model(k):
    """STYLE_BIBLE Cerberus: see the header."""
    import blockkit as bk
    B = bk.Blocks(k, seed=127, tier=4, th=TH)
    D = 0.62
    # ---- torso: broad chest 21 % bigger than the hips, 39 % overlap
    chest = B.add((0, -0.22, 0.86), (0.46, 0.46, 0.38), CHAR, "Chest", bot=(0.90, 0.95), density=D)
    B.add((0, 0.31, 0.83), (0.38, 0.38, 0.31), CHAR, "Spine", bot=(0.90, 0.95), density=D)
    B.add((0, -0.684, 0.82), (0.24, 0.02, 0.22), TAN, "Chest", bot=(0.12, 1), studs=[], role="limb")      # tan chest V
    B.add((0, -0.20, 0.47), (0.26, 0.40, 0.012), TAN, "Chest", studs=[], role="limb")                    # tan belly
    B.add((0, 0.684, 0.72), (0.15, 0.006, 0.13), TAN, "Spine", top=(0.25, 1), studs=[], role="limb")     # under the tail
    for tag in ("C", "L", "R"):
        head(B, tag)
    # ---- legs: thigh + shin with a flush tan sock, tan paw with 3 dark claw nubs
    for s, side in ((1, "L"), (-1, "R")):
        for fb, (H, K, A) in (("F", LEGS["FL"]), ("B", LEGS["BL"])):
            leg, shin, foot = "Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side
            x, y = s * H[0], H[1]
            tw = 0.175 if fb == "F" else 0.165
            B.add((x, y, 0.54), (tw, 0.19, 0.26), CHAR, leg, bot=(0.92, 0.92), density=D)
            B.add((x, y - 0.01, 0.245), (0.14, 0.16, 0.155), CHAR, shin, density=D)   # ends just under the ankle
            B.add((x, y - 0.01, 0.15), (0.14 * 1.02, 0.16 * 1.02, 0.06), TAN, shin, studs=[], role="limb")
            if fb == "B":     # tan up the back of the hind shins, above the sock
                B.add((x, y + 0.156, 0.27), (0.05, 0.006, 0.06), TAN, shin, studs=[], role="limb")
            B.add((x, y - 0.04, 0.045), (0.157, 0.19, 0.045), TAN, foot, studs=[], role="limb")
            for gx in (-0.095, 0.0, 0.095):
                B.add((x + gx, y - 0.232, 0.03), (0.026, 0.03, 0.022), NOSE, foot, studs=[])
    # ---- tail: charcoal root curving up, ending in a flat two-tone flame point (y-z plane)
    T = [Vector(p) for p in TAILP]
    for (a, b), w, bn in zip(zip(T, T[1:]), (0.085, 0.072, 0.06), ("Tail1", "Tail2", "Tail3")):
        B.seg(a, b, w, w, CHAR, bn, ext=0.04, studs=[], role="limb")
    tip = T[3]
    B.seg(tip - Vector((0, 0.04, 0.03)), tip + Vector((0, 0.26, 0.20)), 0.035, 0.13, FLAME, "Tail3", top=(1, 0.08),
          studs=[], role="limb")
    B.seg(tip + Vector((0, 0.0, 0.01)), tip + Vector((0, 0.21, 0.16)), 0.041, 0.065, FLAME_Y, "Tail3", top=(1, 0.10),
          studs=[], role="limb")
    B.build()
    return {"plates": B.stud_count, "TH": round(B.th, 3), "cell": round(B.pcell, 3)}


def rig(k):
    k.joint("Spine", (0, 0.30, 0.84), "Root", tail=(0, -0.4, 0))
    k.joint("Chest", (0, -0.06, 0.86), "Spine", tail=(0, -0.4, 0))
    for tag, (base, J, yaw, sc) in HEADS.items():
        d = (Vector(J) - Vector(base))
        k.joint("Neck_" + tag, base, "Chest", tail=tuple(d))
        fwd = _rz(yaw) @ Vector((0, -0.35, 0))
        k.joint("Head_" + tag, J, "Neck_" + tag, tail=tuple(fwd))
        k.joint("Jaw_" + tag, Vector(J) + _rz(yaw) @ (Vector((0, -0.34, 0.0)) * sc), "Head_" + tag, tail=tuple(fwd * 0.6))
    for s, side in ((1, "L"), (-1, "R")):
        for fb, parent, knee in (("F", "Chest", (0, 1, 0)), ("B", "Spine", (0, 1, 0))):
            H, K, A = (X(p, s) for p in LEGS[fb + "L"])
            k.joint("Leg_" + fb + side, H, parent)
            k.joint("Shin_" + fb + side, K, "Leg_" + fb + side)
            k.joint("Foot_" + fb + side, A, "Shin_" + fb + side, tail=(0, -0.2, 0))
            k.add_leg2("Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side, knee=knee)
    k.joint("Tail1", TAILP[0], "Spine")
    k.joint("Tail2", TAILP[1], "Tail1")
    k.joint("Tail3", TAILP[2], "Tail2", tail=(0, 0.2, 0.15))


# ------------------------------------------------------------------ animation
import petkit as pk
import _common as cm

LEGS4 = ["Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR"]
TAIL = ["Tail1", "Tail2", "Tail3"]


def hd(k, f, tag, nk=0.0, ny=0.0, h=0.0, hy=0.0, roll=0.0, jaw=4.0, lunge=0.0):
    """one head: nk/ny = neck pitch/yaw, h/hy = head pitch/yaw, roll = head tilt, jaw open, lunge = neck pushes forward"""
    yaw = HEADS[tag][2]
    fwd = _rz(yaw) @ Vector((0, -1, 0))
    k.key("Neck_" + tag, f, rot=(nk, ny, 0), loc=tuple(fwd * lunge))
    k.key("Head_" + tag, f, rot=(h, hy, roll))
    k.key("Jaw_" + tag, f, rot=(jaw, 0, 0))


def idle(k):
    """three personalities: LEFT yawns at 30, nods off (head sinking in jerks) and snaps awake at 128; CENTER keeps
    guard, scanning left / right with holds; RIGHT pants with its tongue out and tilts its head at its brothers."""
    n = 160
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 2):
        b = pk.wave(f, n, 0, 5)
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, 0.01 * b))
        k.key("Chest", f, rot=(-1.0 * b, 0, 0))
        cm.chain(k, f, n, TAIL, sway=6, pitch=8, cycles=2, lag=0.15, grow=0.5)
        # right head: pants the whole time
        pant = 0.5 + 0.5 * math.sin(2 * math.pi * f / 8)
        tilt = 0.0
        for c, w in ((70, 16), (104, 16)):
            if c - 8 <= f <= c + 16:
                tilt = -w * math.sin(math.pi * (f - (c - 8)) / 24)
        hd(k, f, "R", nk=-2, ny=0, h=4 + 2 * pant, hy=8 if 60 <= f <= 116 else 0, roll=tilt, jaw=10 + 10 * pant)
    # left head: yawn, then nodding off in jerks, snaps awake
    for f, nk, h, jaw in ((0, 0, 4, 3), (24, -6, -10, 4), (32, -10, -18, 40), (42, -10, -18, 42), (50, 0, 0, 3),
                          (70, 4, 8, 3), (80, 10, 16, 3), (84, 4, 6, 3), (96, 12, 18, 3), (102, 6, 8, 3), (118, 16, 24, 3),
                          (128, -6, -6, 8), (134, 0, 0, 3), (160, 0, 4, 3)):
        hd(k, f, "L", nk=nk, h=h, jaw=jaw)
    # center head: guard scan with holds
    for f, ny, hy, h in ((0, 0, 0, 0), (20, 0, 0, 0), (28, 3, 20, -2), (56, 3, 20, -2), (64, -3, -20, -2),
                         (92, -3, -20, -2), (100, 0, 0, 0), (126, 0, 0, 0), (130, 4, 10, -6), (140, 0, 0, 0), (160, 0, 0, 0)):
        hd(k, f, "C", nk=-2, ny=ny, h=h, hy=hy, jaw=4)
    cm.plant(k, n, legs=LEGS4)
    k.finish()
    k.meta["planted"] = LEGS4


def walk(k):
    n = 24

    def body(f):
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(0.8 * pk.wave(f, n, 0.1, 2), 1.5 * pk.wave(f, n, 0.0), 2.0 * pk.wave(f, n, 0.0)),
              loc=(0, 0, -0.025 * b))
        k.key("Chest", f, rot=(0, -2 * pk.wave(f, n, 0.25), -1.5 * pk.wave(f, n, 0.25)))
        for tag, ph in (("L", 0.1), ("C", 0.0), ("R", 0.2)):
            hd(k, f, tag, nk=2 * pk.wave(f, n, ph, 2), h=-2 * pk.wave(f, n, ph + 0.1, 2), jaw=4 if tag != "R" else 14)
        cm.chain(k, f, n, TAIL, sway=10, pitch=6, cycles=1, lag=0.15, grow=0.5)
    return cm.quad_walk(k, n, 0.17, 0.10, body, gait="trot")


def roar(k):
    """THREE-HEAD CHORUS: the left head howls, then the center, then the right (each throws its head up with the jaw
    wide), then all three howl together with the chest rising."""
    n = 84
    k.new_action("roar", n, False)
    HOWL = dict(nk=-26, h=-30, jaw=32)
    REST = dict(nk=0, h=0, jaw=4)
    seq = {"L": (8, 14, 26, 32), "C": (22, 28, 40, 46), "R": (36, 42, 54, 60)}
    for tag, (a, b, c, d) in seq.items():
        for f, v in ((0, REST), (a, REST), (b, HOWL), (c, HOWL), (d, dict(nk=-4, h=-4, jaw=6)), (62, dict(nk=-4, h=-4, jaw=6)),
                     (68, dict(nk=-30, h=-32, jaw=36)), (78, dict(nk=-30, h=-32, jaw=36)), (84, REST)):
            hd(k, f, tag, **v)
    for f, ch, z in ((0, 0, 0), (62, 0, 0), (68, -6, 0.03), (78, -6, 0.03), (84, 0, 0)):
        k.key("Chest", f, rot=(ch, 0, 0))
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, z))
    for f in range(0, n + 1, 2):
        cm.chain(k, f, n, TAIL, sway=8, pitch=20, cycles=3, lag=0.15, grow=0.5)
    cm.plant(k, n, legs=LEGS4)
    k.finish(loop=False)


def snap(k):
    """SIGNATURE - TRIPLE SNAP: the left head lunges out to the left and snaps, the right head to the right, the center
    lunges straight ahead, then all three bite together as the whole body pounces forward."""
    import bpy
    n = 100
    k.new_action("act_triplesnap", n, False)
    REST = dict(nk=0, h=0, jaw=4)
    seq = {"L": 10, "R": 24, "C": 38}
    for tag, t in seq.items():
        side = {"L": 1, "R": -1, "C": 0}[tag]
        out = dict(nk=8, ny=12 * side, h=6, hy=6 * side, jaw=4)
        for f, v in ((0, REST), (t - 6, dict(nk=-10, ny=-4 * side, h=-8, jaw=30)), (t, dict(out, jaw=34, lunge=0.14)),
                     (t + 2, dict(out, jaw=0, lunge=0.16)), (t + 8, dict(nk=-2, h=-2, jaw=4)), (52, dict(nk=-6, h=-6, jaw=8)),
                     (58, dict(nk=-14, h=-10, jaw=36)), (64, dict(nk=10, h=8, jaw=0, lunge=0.10)), (70, dict(nk=6, h=6, jaw=0)),
                     (84, REST), (n, REST)):
            hd(k, f, tag, **v)
    for f, y, z, p in ((0, 0, 0, 0), (36, 0, 0, 0), (40, -0.06, -0.02, 2), (46, 0, 0, 0), (54, 0.08, -0.10, -4),
                       (62, -0.30, 0.06, 4), (66, -0.30, -0.04, 6), (76, -0.18, -0.02, 2), (90, 0, 0, 0), (n, 0, 0, 0)):
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, y, z))
        k.key("Chest", f, rot=(0, 0, 0))
    for f in range(0, n + 1, 2):
        cm.chain(k, f, n, TAIL, sway=10, pitch=14, cycles=4, lag=0.15, grow=0.5)
    k.bake_bezier_now()
    sc = bpy.context.scene
    for f in range(0, n + 1):
        sc.frame_set(f)
        for leg in LEGS4:
            T = Vector((k.J[leg].x, k.J[leg].y, 0.0))
            if leg[4] == "F" and 56 <= f <= 66:              # front paws leave the ground in the pounce, land forward
                u = (f - 56) / 10
                T = Vector((k.J[leg].x, k.J[leg].y - 0.30 * (0.5 - 0.5 * math.cos(math.pi * u)), 0.22 * math.sin(math.pi * u)))
            elif leg[4] == "F" and 66 < f <= 84:
                u = (f - 66) / 18
                T = Vector((k.J[leg].x, k.J[leg].y - 0.30 * (1 - u) if f < 76 else k.J[leg].y - 0.30 * (1 - u),
                            0.10 * math.sin(math.pi * min(1, max(0, (f - 74) / 10))) if f >= 74 else 0.0))
            k.solve_leg(leg, f, T)
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    snap(k)
    return stride


def check_pairs():
    P = [("Leg_FL", "Leg_BL"), ("Leg_FR", "Leg_BR"), ("Leg_FL", "Leg_FR"), ("Leg_BL", "Leg_BR"),
         ("Shin_FL", "Shin_FR"), ("Shin_BL", "Shin_BR"), ("Shin_FL", "Shin_BL"), ("Shin_FR", "Shin_BR")]
    for a, b in (("L", "C"), ("R", "C"), ("L", "R")):
        for x in ("Head_", "Jaw_", "Neck_"):
            for y in ("Head_", "Jaw_", "Neck_"):
                P.append((x + a, y + b))
    for tag in "LCR":
        for b in ("Leg_FL", "Leg_FR", "Shin_FL", "Shin_FR"):
            P.append(("Head_" + tag, b))
            P.append(("Jaw_" + tag, b))
        P.append(("Head_" + tag, "Chest"))
    for b in ("Leg_BL", "Leg_BR"):
        P.append(("Tail1", b))
    return P


def joints():
    out = []
    for tag, (base, J, yaw, sc) in HEADS.items():
        Jv = Vector(J)
        out.append((Jv, Jv, 0.12, "Head_" + tag))
        bv = Vector(base)                 # neck roots overlap inside the chest (hidden)
        out.append((bv, bv, 0.24, "Neck_" + tag))
    return out
