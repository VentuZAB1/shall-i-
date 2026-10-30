# Ivonrath (SECRET, Magma egg): the red fire dragon of the V2 friend pets, rebuilt in the Steal-an-Egg block style
# (STYLE_BIBLE 3 "Ivonrath"): chibi but proud - a big head with lovely-fierce amber slit eyes, a 10 deg brow and a smirk
# with 1 fang, a puffed chest with light belly bands, stubby legs, 2 big swept 3-segment horns with a gold crown band,
# dark-red back spikes with gold tips, 2-tone scalloped membrane wings (wing3 rules) and a curled tail ending in a flat
# spade. NO glow: breath fire and the tail flame are particle VFX later (Breath / Flame bones are their anchors).
# Clips ported from PetsV2: proud look-around idle, trot walk, real flight (legs pump), takeoff (launch) / land
# (touch), roar = rear back + lunge with the jaw wide (fire puff VFX), signature act_stretch = proud wing stretch.
import math
from mathutils import Vector, Quaternion
import wing3

DISPLAY = "Ivonrath"
MOTION = "Fly"
RIG = "wingquad"
HEIGHT = 7.5

RED = (222, 52, 42)
BELLY = (255, 192, 92)
BONE = (112, 22, 32)
HORN = (255, 224, 160)
MEM = (255, 124, 52)
MEM_IN = (204, 64, 40)
GOLD = (255, 204, 64)
IRIS = (255, 176, 30)
MOUTH = (110, 26, 44)
TONGUE = (236, 110, 140)
FANG = (250, 246, 236)
GEM = (236, 60, 52)

HIPS_C, HIPS_H = (0, 0.22, 0.58), (0.38, 0.44, 0.28)
CHEST_C, CHEST_H = (0, -0.20, 0.68), (0.46, 0.36, 0.36)          # chest 21 % wider / 29 % taller than the hips
HEAD_C, HEAD_H = (0, -0.84, 1.42), (0.46, 0.34, 0.36)            # HW 0.92, HH 0.72
LEGS = {"F": (0.28, -0.30), "B": (0.26, 0.48)}
LEG_TOP = 0.40
WING = wing3.Wing(S=(0.44, -0.06, 1.00), W=(1.06, 0.10, 1.46), H=(1.02, 0.98, 0.86), BB=(0.36, 0.44, 0.84))
F1, F2 = (1.70, 0.34, 1.66), (1.56, 0.86, 1.14)
TAILP = [(0, 0.62, 0.72), (0, 1.02, 0.58), (0, 1.38, 0.58), (0, 1.58, 0.84)]


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


def front_y(blk, z):
    t = ((z - blk.c.z) / blk.h.z + 1) / 2
    sy = blk.bot[1] + (blk.top[1] - blk.bot[1]) * t
    return blk.c.y + blk.ts[1] * t - blk.h.y * sy


def front_n(blk):
    dydz = -blk.h.y * (blk.top[1] - blk.bot[1]) / (2 * blk.h.z)
    return Vector((0, -1, dydz)).normalized()


def front_inlay(B, blk, x, z0, z1, width, thick, color, bone, **kw):
    n = front_n(blk)
    p0 = Vector((x, front_y(blk, z0), z0)) + n * (thick + 0.002)
    p1 = Vector((x, front_y(blk, z1), z1)) + n * (thick + 0.002)
    kw.setdefault("studs", [])
    kw.setdefault("bevel", min(0.012, thick * 0.6))
    return B.bar(p0, p1, n, width, thick, color, bone, **kw)


def membrane_wing(B, s, side):
    """STYLE_BIBLE 2d membrane wing: dark-red arm bar + wrist knuckle + ivory claw, finger 3 = hinge (inner wing),
    fingers 1-2 (outer wing, WingTip bone) tapering to 0.4, 2-tone panels (outer orange, inner x0.8 V) with the
    trailing edges pulled in 18 % between the fingers (scallops)."""
    S, W, f3, bb = (X(p, s) for p in (WING.S, WING.W, WING.H, WING.BB))
    f1, f2 = X(F1, s), X(F2, s)
    wb, tb = "Wing_" + side, "WingTip_" + side
    B.seg(S, W, 0.05, 0.055, BONE, wb, side=(0, 0, 1), ext=0.10, role="limb", studs=[])
    B.add(W, (0.07, 0.07, 0.07), BONE, wb, studs=[], role="limb")
    B.spike(W + Vector((s * 0.02, -0.02, 0.05)), (s * 0.6, -0.3, 0.75), 0.17, 0.035, HORN, wb, top=(0.15, 0.15))
    B.seg(W, f3, 0.034, 0.038, BONE, wb, side=(0, 0, 1), top=(0.45, 0.45), studs=[], role="limb")
    for f, w in ((f1, 0.04), (f2, 0.036)):
        B.seg(W, f, w, w + 0.004, BONE, tb, side=(0, 0, 1), top=(0.4, 0.4), studs=[], role="limb")
    e12 = f1.lerp(f2, 0.5).lerp(W, 0.18)
    e23 = f2.lerp(f3, 0.5).lerp(W, 0.18)
    q = f3.lerp(bb, 0.5).lerp(S, 0.14)
    B.poly([S, W, f3, q, bb], 0.03, MEM_IN, wb)
    B.poly([W, f1, e12, f2], 0.03, MEM, tb)
    B.poly([W, f2, e23, f3], 0.03, MEM, tb)


def model(k):
    """Ivonrath, bible SECRET Magma: chibi-proud red dragon. Plate fill .45 (SECRET) on soft masses, no glow."""
    import blockkit as bk
    B = bk.Blocks(k, seed=61, tier="S")
    D = 0.80
    hips = B.add(HIPS_C, HIPS_H, RED, "Spine", bot=(0.90, 0.94), rnd=0.28, density=1.0, studs=["+x", "-x", "+y", "-y"])
    chest = B.add(CHEST_C, CHEST_H, RED, "Spine", bot=(0.86, 0.92), rnd=0.34, density=D)
    # light belly bands across the chest front (follow the taper) + belly plate underneath
    for z0, z1, w in ((0.40, 0.50, 0.50), (0.56, 0.66, 0.58), (0.72, 0.82, 0.62), (0.88, 0.96, 0.56)):
        front_inlay(B, chest, 0, z0, z1, w, 0.008, BELLY, "Spine")
    B.add((0, 0.10, 0.306), (0.28, 0.38, 0.012), BELLY, "Spine", studs=[], bevel=0.008)
    # chunky neck (>= 0.9 HW wide), mostly hidden between the chest and the head
    B.add((0, -0.56, 1.10), (0.40, 0.22, 0.24), RED, "Neck", rot=(24, 0, 0), studs=[], rnd=0.35)
    # ---- head (final size) + muzzle, jaw, smirk with 1 fang, nostrils
    head = B.add(HEAD_C, HEAD_H, RED, "Head", top=(0.94, 0.94), rnd=0.32, density=D, studs=["+x", "-x", "+y", "+z"])
    snout = B.add((0, -1.24, 1.24), (0.27, 0.22, 0.14), RED, "Head", top=(0.90, 0.88), rnd=0.34, studs=[])
    for sx in (1, -1):
        B.add((sx * 0.085, front_y(snout, 1.33) - 0.004, 1.335), (0.035, 0.012, 0.02), BONE, "Head",
              rot=(0, sx * 18, 0), studs=[], bevel=0.006)
    jaw = B.add((0, -1.18, 1.06), (0.24, 0.21, 0.055), BELLY, "Jaw", bot=(0.9, 0.9), studs=[], role="limb", rnd=0.3)
    B.add((0, -1.18, 1.112), (0.21, 0.18, 0.006), MOUTH, "Jaw", studs=[], bevel=0.004)
    B.add((0, -1.16, 1.12), (0.12, 0.12, 0.008), TONGUE, "Jaw", studs=[], bevel=0.004)
    # smirk: dark mouth line on the muzzle front, flat on the right, curling up on the left; 1 fang on the left
    fy = front_y(snout, 1.12) - 0.006
    B.add((-0.05, fy, 1.118), (0.15, 0.006, 0.013), MOUTH, "Head", studs=[], bevel=0.004)
    B.add((0.135, fy, 1.142), (0.055, 0.006, 0.013), MOUTH, "Head", rot=(0, -32, 0), studs=[], bevel=0.004)
    B.spike((0.13, fy - 0.004, 1.13), (0, -0.15, -1), 0.085, 0.026, FANG, "Head")
    # lovely-fierce eyes: bold sizes, slit pupils, 2 highlights, 10 deg dark-red brows
    B.face_eyes(head, "bold", IRIS, base=RED, brow=BONE, z=0.63, x=0.25, scale=1.06, pupil_size=(0.05, 0.12),
                hl_size=(0.075, 0.03), brow_spec=(0.26, 0.05, 10), look=(0, 0.4))
    # cheek frills: 2 swept blades per side growing from the back edge of the jaw line
    for s in (1, -1):
        for z, dz, L in ((1.22, -0.30, 0.20), (1.32, 0.05, 0.24)):
            root = Vector((s * 0.42, -0.62, z))
            d = Vector((s * 0.55, 0.75, dz)).normalized()
            B.seg(root, root + d * L, 0.07, 0.04, BONE, "Head", side=(0, 0, 1), ext=0.05, top=(0.15, 0.5), studs=[],
                  role="limb")
    # ---- horns: 3 curved segments swept back, ivory; gold crown band with 3 points + a gem between them
    for s in (1, -1):
        P = [Vector((s * 0.29, -0.80, 1.74)), Vector((s * 0.40, -0.66, 1.96)), Vector((s * 0.50, -0.42, 2.10)),
             Vector((s * 0.56, -0.12, 2.13))]
        B.seg(P[0], P[1], 0.085, 0.085, HORN, "Head", side=(1, 0, 0), ext=0.10, top=(0.85, 0.85), studs=[], role="limb")
        B.seg(P[1], P[2], 0.072, 0.072, HORN, "Head", side=(1, 0, 0), ext=0.03, top=(0.8, 0.8), studs=[], role="limb")
        B.spike(P[2] - (P[3] - P[2]).normalized() * 0.03, P[3] - P[2], (P[3] - P[2]).length + 0.05, 0.058, HORN,
                "Head", top=(0.12, 0.12))
    B.add((0, -0.80, 1.775), (0.26, 0.10, 0.04), GOLD, "Head", studs=[], role="limb")
    for x, h in ((-0.15, 0.10), (0.0, 0.14), (0.15, 0.10)):
        B.spike((x, -0.86, 1.80), (0, -0.25, 1), h, 0.035, GOLD, "Head", top=(0.12, 0.12))
    B.add((0, -0.905, 1.775), (0.04, 0.006, 0.03), GEM, "Head", rot=(0, 45, 0), studs=[], bevel=0.006)
    # ---- back spikes: broad dark-red blades laid back 62 deg (wider than tall) with gold tips, steps 100/80/60 %
    for y, z, sz, bone in ((-0.60, 1.30, 0.85, "Neck"), (-0.34, 1.05, 1.0, "Spine"), (-0.08, 1.05, 1.0, "Spine"),
                           (0.18, 0.88, 0.85, "Spine"), (0.42, 0.87, 0.75, "Spine"), (0.74, 0.86, 0.6, "Tail1"),
                           (0.98, 0.74, 0.5, "Tail1")):
        base = Vector((0, y, z - 0.04))
        d = Vector((0, 0.88, 0.47)).normalized() if bone != "Neck" else Vector((0, 0.80, 0.60)).normalized()
        L = 0.28 * sz
        R = bk.frame_from(base, base + d, (1, 0, 0))
        B.add(base + d * L / 2, (0.05 * sz, 0.12 * sz, L / 2), BONE, bone, R=R, top=(0.45, 0.10), studs=[],
              role="limb")
        B.add(base + d * L * 0.80, (0.05 * sz * 0.62, 0.12 * sz * 0.42, L * 0.20), GOLD, bone, R=R, top=(0.3, 0.12),
              studs=[], role="limb")
    # ---- stubby legs: one chunky block + dark-red paw with 3 ivory claw nubs
    for s, side in ((1, "L"), (-1, "R")):
        for fb in ("F", "B"):
            x, y = LEGS[fb]
            X0 = s * x
            bone = "Leg_" + fb + side
            hx = 0.15 if fb == "F" else 0.13
            B.add((X0, y, 0.25), (hx, 0.16, 0.20), RED, bone, bot=(0.94, 0.94), rnd=0.3, density=D)
            B.add((X0, y - 0.015, 0.05), (hx * 1.12, 0.185, 0.05), BONE, bone, studs=[], role="limb", rnd=0.35)
            for gx in (-0.07, 0.0, 0.07):
                B.spike((X0 + gx, y - 0.19, 0.04), (0, -1, -0.25), 0.07, 0.024, HORN, bone, top=(0.25, 0.25))
    # ---- curled tail: 3 tapering segments + a flat spade (side-view plane) on Tail3
    T = [Vector(p) for p in TAILP]
    for i, (hw, hd) in enumerate(((0.12, 0.14), (0.10, 0.105), (0.08, 0.08))):
        B.seg(T[i], T[i + 1], hw, hd, RED, "Tail%d" % (i + 1), side=(1, 0, 0), ext=0.14 if i == 0 else 0.06,
              top=(0.85, 0.85), studs=[], role="limb")
    d = (T[3] - T[2]).normalized()
    up = Vector((0, -d.z, d.y))
    C = T[3] + d * 0.04
    R = bk.frame_from(C, C + d, (1, 0, 0))
    B.add(C + d * 0.03, (0.04, 0.19, 0.08), MEM, "Tail3", R=R, top=(1, 1), bot=(1, 0.40), studs=[], role="limb")
    B.add(C + d * 0.25, (0.04, 0.19, 0.14), MEM, "Tail3", R=R, top=(1, 0.06), bot=(1, 1), studs=[], role="limb")
    # ---- wings
    for s, side in ((1, "L"), (-1, "R")):
        membrane_wing(B, s, side)
    B.build()
    return {"plates": B.stud_count, "TH": round(B.th, 3), "cell": round(B.pcell, 3)}


# ------------------------------------------------------------------ rig
def rig(k):
    k.joint("Spine", (0, 0.20, 0.62), "Root", tail=(0, -0.45, 0.1))
    k.joint("Neck", (0, -0.46, 0.98), "Spine", tail=(0, -0.2, 0.3))
    k.joint("Head", (0, -0.62, 1.14), "Neck", tail=(0, -0.35, 0.05))          # throat pivot
    k.joint("Jaw", (0, -1.00, 1.08), "Head", tail=(0, -0.3, 0))
    k.joint("Breath", (0, -1.42, 1.12), "Head", tail=(0, -0.25, 0))          # fire-breath VFX anchor (no mesh)
    for s, side in ((1, "L"), (-1, "R")):
        for fb in ("F", "B"):
            x, y = LEGS[fb]
            k.joint("Leg_" + fb + side, (s * x, y, LEG_TOP), "Spine", tail=(0, 0, -0.35))
        k.joint("Wing_" + side, X(WING.S, s), "Spine")
        k.joint("WingTip_" + side, X(WING.W, s), "Wing_" + side, tail=(s * 0.6, 0.2, 0.1))
    k.joint("Tail1", TAILP[0], "Spine")
    k.joint("Tail2", TAILP[1], "Tail1")
    k.joint("Tail3", TAILP[2], "Tail2")
    k.joint("Flame", (0, 1.64, 1.04), "Tail3", tail=(0, 0, 0.2))             # tail-flame VFX anchor (no mesh)


def check_pairs():
    W = ["Wing_L", "WingTip_L", "Wing_R", "WingTip_R"]
    P = [("Wing_L", "WingTip_L"), ("Wing_R", "WingTip_R"), ("WingTip_L", "WingTip_R"), ("Wing_L", "Wing_R"),
         ("WingTip_L", "Wing_R"), ("Wing_L", "WingTip_R")]
    for w in W:
        for b in ("Head", "Neck", "Spine", "Tail1", "Tail2", "Tail3", "Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR"):
            P.append((w, b))
    P += [("Leg_FL", "Leg_BL"), ("Leg_FR", "Leg_BR"), ("Leg_FL", "Leg_FR"), ("Leg_BL", "Leg_BR"),
          ("Head", "Leg_FL"), ("Head", "Leg_FR"), ("Jaw", "Leg_FL"), ("Jaw", "Leg_FR"), ("Head", "Spine"),
          ("Jaw", "Spine"), ("Tail1", "Leg_BL"), ("Tail1", "Leg_BR"), ("Tail2", "Leg_BL"), ("Tail2", "Leg_BR"),
          ("Tail3", "Spine"), ("Head", "Tail3")]
    return P


def joints():
    out = WING.joints()
    for s, sd in ((1, "L"), (-1, "R")):
        out.append((X(WING.S, s), X(WING.BB, s), 0.13, "Wing_" + sd))
    out.append(((0, -0.56, 1.10), (0, -0.64, 1.16), 0.30, "Head"))          # neck / head junction
    return out


# ------------------------------------------------------------------ animation
import petkit as pk
import _common as cm

LEGS4 = ["Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR"]
TAIL = ["Tail1", "Tail2", "Tail3"]
FOLD = dict(up=22, fwd=-14, twist=0, tip=92)         # ground pose: arm raised, outer wing folded down on the hinge


def wings(k, f, up, fwd=0.0, twist=0.0, tip=0.0, side=None):
    WING.key(k, f, up, fwd, twist, tip, side=side)


def folded(k, f, du=0.0, dfwd=0.0, dtip=0.0, side=None):
    wings(k, f, FOLD["up"] + du, FOLD["fwd"] + dfwd, FOLD["twist"], FOLD["tip"] + dtip, side)


def tail(k, f, n, yaw_amp, pitch=0.0, phase=0.0, cycles=1, pitch_amp=0.0):
    for i, b in enumerate(TAIL):
        lag = phase - 0.1 * i
        k.key(b, f, rot=(pitch + pitch_amp * pk.wave(f, n, lag, cycles),
                         yaw_amp * (1 + 0.45 * i) * pk.wave(f, n, lag, cycles), 0))


def anchors(k, f):
    k.key("Breath", f, rot=(0, 0, 0), loc=(0, 0, 0))
    k.key("Flame", f, rot=(0, 0, 0))


def idle(k):
    """proud and cheeky: chin up, looks right, back, left, back with a slow breath; tail swishes, wings settle."""
    n = 60
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 3):
        s = pk.wave(f, n)
        k.key("Spine", f, rot=(-1.5 - 1.0 * s, 0, 0.8 * pk.wave(f, n, 0.3)), loc=(0, 0, 0.014 * (1 + s) / 2))
        look = 18 * pk.wave(f, n, 0.0) * abs(pk.wave(f, n, 0.0)) ** 0.3
        k.key("Neck", f, rot=(-5 + 2 * pk.cwave(f, n), look * 0.45, 0))
        k.key("Head", f, rot=(-4 + 3 * pk.wave(f, n, 0.15, 2), look * 0.55, -4 * pk.wave(f, n, 0.1)))
        k.key("Jaw", f, rot=(2, 0, 0))
        folded(k, f, du=3 * pk.wave(f, n, 0.2), dfwd=2 * pk.cwave(f, n))
        tail(k, f, n, 9, pitch=3, phase=0.05, pitch_amp=3)
        anchors(k, f)
    cm.plant(k, n, legs=LEGS4)
    k.finish()
    k.meta["planted"] = LEGS4


def walk(k):
    n = 24

    def body(f):
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(1.5 * pk.wave(f, n, 0, 2), 3 * pk.wave(f, n, 0.1), 2.5 * pk.wave(f, n)),
              loc=(0, 0, 0.035 * b))
        k.key("Neck", f, rot=(-4 - 2 * pk.wave(f, n, 0.1, 2), -2 * pk.wave(f, n, 0.1), 0))
        k.key("Head", f, rot=(-2 - 2.5 * pk.wave(f, n, 0.15, 2), -2.5 * pk.wave(f, n, 0.1), -2 * pk.wave(f, n, 0.05)))
        k.key("Jaw", f, rot=(2, 0, 0))
        folded(k, f, du=3 * pk.wave(f, n, 0.1, 2))
        tail(k, f, n, 11, pitch=2, phase=0.2)
        anchors(k, f)
    return cm.quad_walk(k, n, 0.12, 0.09, body, gait="trot")


# ---- flight
FLY_N = 22
PITCH = 16.0


def fly_legs(k, f, ph, amt=1.0):
    for leg in LEGS4:
        fr = leg[4] == "F"
        w = math.sin(2 * math.pi * (ph - (0.12 if fr else 0.25)))
        base = 60 if fr else 76
        k.key(leg, f, rot=(amt * (base + 12 * w), 0, 0), loc=(0, 0, 0))


def fly_pose(k, f, ph, legs=True):
    w = wing3.stroke(ph, top=30.0, bot=-46.0, sweep=12.0, twist=12.0, fold=32.0)
    wings(k, f, w["up"], w["fwd"], w["twist"], w["tip"])
    k.key("Spine", f, rot=(PITCH - 3 * math.sin(2 * math.pi * (ph - 0.1)), 0, 0),
          loc=(0, 0, 0.09 * math.cos(2 * math.pi * (ph - 0.45))))
    k.key("Neck", f, rot=(-14 - 2 * math.sin(2 * math.pi * (ph - 0.25)), 0, 0))
    k.key("Head", f, rot=(-10 + 2 * math.sin(2 * math.pi * (ph - 0.32)), 0, 0))
    k.key("Jaw", f, rot=(2, 0, 0))
    for i, b in enumerate(TAIL):
        k.key(b, f, rot=(6 + 7 * math.sin(2 * math.pi * (ph - 0.12 * (i + 1))),
                         3 * math.sin(2 * math.pi * (ph - 0.2 * i)), 0))
    anchors(k, f)
    if legs:
        fly_legs(k, f, ph)


def fly(k):
    n = FLY_N
    k.new_action("fly", n, True)
    for f in range(0, n + 1):
        fly_pose(k, f, f / n)
    k.finish()


def rest_keys(k, f, z=0.0, pitch=0.0):
    k.key("Spine", f, rot=(pitch, 0, 0), loc=(0, 0, z))
    k.key("Neck", f, rot=(0, 0, 0))
    k.key("Head", f, rot=(0, 0, 0))
    k.key("Jaw", f, rot=(2, 0, 0))
    folded(k, f)
    for b in TAIL:
        k.key(b, f, rot=(0, 0, 0))
    anchors(k, f)


def plant_frames(k, frames):
    import bpy
    k.bake_bezier_now()
    for f in frames:
        bpy.context.scene.frame_set(f)
        for leg in LEGS4:
            k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, 0.0)))


def takeoff(k):
    """crouch with the wings opening high (0-10), LAUNCH at 11 on a huge downstroke + leg push, into flight"""
    n = 27
    k.new_action("takeoff", n, False)
    rest_keys(k, 0)
    for f, z, p, w in ((6, -0.09, -6, (26, -12, -4, 40)), (10, -0.12, -8, (36, -4, -8, -6)),
                       (13, 0.22, 10, (-34, 12, 10, 4)), (17, 0.34, 14, (16, 0, 0, -8))):
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
        k.key("Neck", f, rot=(-8 - p * 0.5, 0, 0))
        k.key("Head", f, rot=(-6, 0, 0))
        k.key("Jaw", f, rot=(2, 0, 0))
        wings(k, f, *w)
        for b in TAIL:
            k.key(b, f, rot=(4 + p * 0.4, 0, 0))
        anchors(k, f)
    fly_pose(k, 22, 0.0, legs=False)
    fly_pose(k, n, 0.22, legs=False)
    plant_frames(k, range(0, 12))
    for f, a in ((14, 0.45), (19, 0.85)):
        fly_legs(k, f, 0.0, a)
    fly_legs(k, 22, 0.0)
    fly_legs(k, n, 0.22)
    k.finish(loop=False)
    k.events["takeoff"] = {"launch": round(11 / n, 3)}


def land(k):
    """flare upright with braking beats, legs reach, touch down at 16, absorb, fold the wings"""
    n = 27
    k.new_action("land", n, False)
    fly_pose(k, 0, 0.0)
    for f, z, p, w in ((7, 0.10, -14, (26, 18, -12, -8)), (12, 0.06, -8, (-16, 12, -8, 4)),
                       (16, -0.08, 4, (14, -6, 0, 30)), (21, 0.02, -1, (20, -16, 0, 80))):
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
        k.key("Neck", f, rot=(-6 - p * 0.4, 0, 0))
        k.key("Head", f, rot=(-5, 0, 0))
        k.key("Jaw", f, rot=(2, 0, 0))
        wings(k, f, *w)
        for b in TAIL:
            k.key(b, f, rot=(4 - p * 0.3, 0, 0))
        anchors(k, f)
    rest_keys(k, n)
    for leg in LEGS4:
        k.key(leg, 7, rot=(-22 if leg[4] == "F" else -8, 0, 0), loc=(0, 0, 0))
    plant_frames(k, range(16, n + 1))
    k.finish(loop=False)
    k.events["land"] = {"touch": round(16 / n, 3)}


def roar(k):
    """rears back with the wings half-raised, then LUNGES the head forward with the jaw wide (fire-puff VFX from the
    Breath anchor), holds the roar, settles."""
    n = 45
    k.new_action("roar", n, False)
    for f, sp, nk, hd, jw, du in ((0, 0, 0, 0, 2, 0), (11, -10, -14, -10, 6, 10), (18, 6, 14, 6, 30, 8),
                                  (30, 5, 12, 5, 32, 8), (37, 0, 0, 0, 4, 0), (45, 0, 0, 0, 2, 0)):
        k.key("Spine", f, rot=(sp, 0, 0), loc=(0, 0, 0.02 * (sp < 0)))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        folded(k, f, du=du, dfwd=-4 * (du > 0))
        for b in TAIL:
            k.key(b, f, rot=(4 - sp * 0.6, 0, 0))
        anchors(k, f)
    for f in range(20, 30, 2):           # the roar rumbles
        w = 1 if (f // 2) % 2 else -1
        k.key("Jaw", f, rot=(31 + 2 * w, 0, 0))
    cm.plant(k, n, legs=LEGS4)
    k.finish(loop=False)


def stretch(k):
    """SIGNATURE (Ivonrath only) - PROUD WING STRETCH: puffs the chest, lifts the chin and unfurls both wings wide and
    high, holds the pose with a slow proud head turn and the tail curled up, then folds back with a satisfied nod."""
    n = 54
    k.new_action("act_stretch", n, False)
    P = [(0, None, 0, 0, 0, 0), (12, (32, -6, -6, 0), -6, -8, -6, 12), (20, (38, -4, -8, -6), -8, -10, -8, 16),
         (34, (36, -4, -8, -4), -8, -10, -8, 16), (44, (26, -12, -2, 62), -2, -2, 2, 4), (54, None, 0, 0, 0, 0)]
    for f, w, sp, nk, hd, tl in P:
        k.key("Spine", f, rot=(sp, 0, 0), loc=(0, 0, 0))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(2, 0, 0))
        if w:
            wings(k, f, *w)
        else:
            folded(k, f)
        for i, b in enumerate(TAIL):
            k.key(b, f, rot=(tl * (0.6 + 0.4 * i), 0, 0))
        anchors(k, f)
    for f, yaw in ((22, 0), (26, 14), (30, 14), (33, 0)):        # slow proud head turn at the top
        k.key("Head", f, rot=(-8, yaw, 0))
    cm.plant(k, n, legs=LEGS4)
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    fly(k)
    takeoff(k)
    land(k)
    roar(k)
    stretch(k)
    return stride
