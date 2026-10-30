# Raiju (Thunder egg): a proud thunder wolf, rebuilt to STYLE_BIBLE.md (2026-10-08 pro pass): big head, short thick
# legs, fierce layered eyes, white muzzle / bib / cheek ruffs, navy socks + brows, yellow bolt inlays + bolt tail.
import math
from mathutils import Vector

DISPLAY = "Raijū"
MOTION = "Walk"
RIG = "quad"
HEIGHT = 8.0

BLUE = (52, 104, 236)
BLUE_D = (40, 82, 200)
WHITE = (236, 242, 255)
NAVY = (30, 36, 86)
YELLOW = (255, 206, 46)
DARK = (22, 22, 38)
MOUTH = (110, 26, 44)
TONGUE = (236, 110, 140)
IRIS = (255, 214, 60)
BOLT = "ffd23a"
EYE = "ffe65c"


def slab(B, p0, p1, width, thick, color, bone, **kw):
    """flat bar from p0 to p1 in a y-z plane (its thin side along x)"""
    p0, p1 = Vector(p0), Vector(p1)
    d = p1 - p0
    th = math.degrees(math.atan2(-d.y, d.z))
    return B.add((p0 + p1) / 2, (thick, width / 2, d.length / 2), color, bone, rot=(th, 0, 0), **kw)


def model(k):
    """STYLE_BIBLE Raiju (gate round 2): a proud thunder wolf, chest forward, big head (HW = TW), short thick legs
    with navy socks and white claw nubs, fierce yellow wedge eyes (iris ring, pupil, 2 highlights), open grin, white
    cheek patches + swept ruff blades, a navy hackle crest, flat bolt inlays on the flanks and a broad flat 3-zig bolt
    tail. No glow (sparks = particle VFX in Studio)."""
    import blockkit as bk
    B = bk.Blocks(k, seed=11, tier=3)
    D = 0.62                                                     # plate density on the big masses (gate fix 5)
    # ---- one torso: chest >= 15 % bigger than the hips (a deliberate shoulder step), 43 % overlap
    chest = B.add((0, -0.28, 0.84), (0.40, 0.42, 0.35), BLUE, "Chest", bot=(0.90, 0.95), density=0.75)
    B.add((0, 0.18, 0.79), (0.335, 0.40, 0.28), BLUE, "Spine", bot=(0.90, 0.95), density=D)
    # raised white V bib with 3 fur points + white belly band
    B.add((0, -0.69, 0.90), (0.25, 0.06, 0.21), WHITE, "Chest", bot=(0.65, 1), studs=[], role="limb")
    for x, l in ((-0.11, 0.15), (0.0, 0.19), (0.11, 0.15)):
        B.spike((x, -0.74, 0.71), (0, -0.25, -1), l, 0.07, WHITE, "Chest", top=(0.15, 0.35))
    B.add((0, -0.10, 0.50), (0.24, 0.45, 0.04), WHITE, "Chest", studs=[], role="limb")
    # navy hackle crest along the back line (top view gets a 2nd zone, hides the neck slot + shoulder step)
    for y, z, sz, bone, rx in ((-0.47, 1.45, 1.0, "Neck", -75), (-0.39, 1.30, 0.9, "Neck", -75),
                               (-0.20, 1.20, 0.8, "Chest", -60), (-0.02, 1.19, 0.7, "Chest", -60),
                               (0.17, 1.10, 0.6, "Spine", -60)):
        B.add((0, y, z), (0.13 * sz, 0.10 * sz, 0.14 * sz), NAVY, bone, rot=(rx, 0, 0), top=(0.25, 0.3), studs=[])
    # neck block (mostly hidden, joins chest and head)
    B.add((0, -0.64, 1.20), (0.36, 0.24, 0.26), BLUE, "Neck", rot=(28, 0, 0), studs=[])
    # ---- head: HW 0.80 (= TW), HH 0.60, soft top taper
    head = B.add((0, -0.80, 1.36), (0.40, 0.33, 0.30), BLUE, "Head", top=(0.94, 0.94), density=D)
    # muzzle: white, 0.60 HW wide, protrudes 0.32, buried 36 %
    muz = B.add((0, -1.20, 1.17), (0.24, 0.25, 0.135), WHITE, "Head", top=(0.88, 0.85), role="limb")
    B.on_face(muz, "+z", 0, 0.06, 0.10, 0.16, 0.02, BLUE)                                   # blue blaze up the nose
    B.add((0, -1.452, 1.255), (0.096, 0.048, 0.057), NAVY, "Head", studs=[], role="limb")    # big nose
    B.add((-0.045, -1.50, 1.285), (0.014, 0.004, 0.014), (246, 244, 250), "Head", studs=[], bevel=0.004)  # sheen
    # open grin: dark mouth plate across the muzzle front, tongue, 2 fangs
    B.add((0, -1.452, 1.075), (0.17, 0.006, 0.038), MOUTH, "Head", studs=[], bevel=0.008)
    B.add((0, -1.456, 1.058), (0.07, 0.006, 0.02), TONGUE, "Head", studs=[], bevel=0.006)
    for s in (1, -1):
        B.spike((s * 0.115, -1.462, 1.11), (0, 0, -1), 0.075, 0.022, (246, 244, 250), "Head")
    # lower jaw (opens in the roar): white
    B.add((0, -1.14, 1.005), (0.20, 0.24, 0.055), WHITE, "Jaw", bot=(0.85, 0.9), role="limb")
    B.add((0, -1.14, 1.062), (0.17, 0.20, 0.006), MOUTH, "Jaw", studs=[], bevel=0.004)
    # fierce eyes: iris ring all round the pupil, 2 highlights; 18 deg navy brows
    B.face_eyes(head, "fierce", IRIS, base=BLUE, brow=NAVY, look=(0, 0.6), pupil_size=(0.09, 0.095),
                hl_size=(0.07, 0.0), brow_spec=(0.30, 0.06, 18))
    # flush white cheek inlay + a fan of 3 ruff blades growing from the BACK edge of the head (ref_08)
    for s in (1, -1):
        B.add((s * 0.402, -0.83, 1.21), (0.008, 0.23, 0.08), WHITE, "Head", studs=[], bevel=0.006, top=(1, 0.6))
        for z, dz, L in ((1.16, -0.22, 0.26), (1.26, 0.02, 0.32), (1.36, 0.30, 0.26)):
            root = Vector((s * 0.36, -0.58, z))
            d = Vector((s * 0.55, 0.70, dz)).normalized()
            B.seg(root, root + d * L, 0.08, 0.05, WHITE, "Head", side=(0, 0, 1), ext=0.04, top=(0.15, 0.4),
                  studs=[], role="limb")
    # ears: wolf ears splayed out, lined with yellow
    for s, side in ((1, "L"), (-1, "R")):
        ear = B.add((s * 0.24, -0.66, 1.86), (0.14, 0.065, 0.22), BLUE, "Ear_" + side, rot=(-8, s * 10, -s * 12),
                    top=(0.25, 0.5), studs=[], role="limb")
        B.add(ear.world((0, -0.068, -0.03)), (0.10, 0.01, 0.15), YELLOW, "Ear_" + side, R=ear.R, top=(0.15, 1),
              studs=[], bevel=0.008)
    # ---- legs: 1 block + flush navy sock + paw with 3 white claw nubs (back legs with a thigh taper)
    for s, side in ((1, "L"), (-1, "R")):
        for fb, x, y, bot in (("F", 0.25, -0.42, (1, 1)), ("B", 0.215, 0.38, (0.88, 0.90))):
            bone = "Leg_" + fb + side
            X0 = s * x
            B.add((X0, y, 0.40), (0.145, 0.155, 0.31), BLUE, bone, bot=bot, density=D)
            B.add((X0, y, 0.165), (0.145 * bot[0] * 1.02, 0.155 * bot[1] * 1.02, 0.075), NAVY, bone, role="limb",
                  studs=[])
            B.add((X0, y - 0.03, 0.05), (0.162, 0.186, 0.05), NAVY, bone, role="limb", studs=[])
            for gx in (-0.095, 0.0, 0.095):
                B.add((X0 + gx, y - 0.228, 0.03), (0.024, 0.03, 0.022), WHITE, bone, studs=[])
    # ---- flat lightning bolts laid on the tapered chest flanks, ending in a point
    for s in (1, -1):
        n = Vector((s, 0, -0.057)).normalized()
        P = [Vector((s * (0.366 + 0.057 * (z - 0.49)), y, z)) for y, z in ((-0.47, 1.05), (-0.33, 0.87),
                                                                         (-0.20, 0.93), (-0.09, 0.77))]
        for a, b in zip(P, P[1:]):
            B.bar(a, b, n, 0.10, 0.014, YELLOW, "Chest", studs=[], bevel=0.006)
        dl = (P[3] - P[2]).normalized()
        B.bar(P[3], P[3] + dl * 0.09, n, 0.10, 0.014, YELLOW, "Chest", studs=[], bevel=0.006, top=(1, 0.1))
    # ---- tail: blue root + a broad FLAT 3-zig bolt in the y-z plane
    B.add((0, 0.62, 0.99), (0.12, 0.12, 0.15), BLUE, "Tail1", rot=(-50, 0, 0), studs=[], role="limb")
    slab(B, (0, 0.66, 1.03), (0, 0.88, 1.37), 0.24, 0.05, YELLOW, "Tail1", studs=[], role="limb")
    slab(B, (0, 0.93, 1.33), (0, 0.72, 1.47), 0.22, 0.05, YELLOW, "Tail2", studs=[], role="limb")
    B.add((0, 0.92, 1.58), (0.05, 0.13, 0.22), YELLOW, "Tail3", rot=(-56, 0, 0), top=(0.6, 0.08), studs=[],
          role="limb")
    B.build()
    return {"plates": B.stud_count, "TH": round(B.th, 3), "cell": round(B.pcell, 3)}


# ------------------------------------------------------------------ rig
def rig(k):
    k.joint("Spine", (0, 0.20, 0.82), "Root", tail=(0, -0.4, 0))
    k.joint("Chest", (0, -0.10, 0.84), "Spine", tail=(0, -0.4, 0))
    k.joint("Neck", (0, -0.46, 1.00), "Chest")
    k.joint("Head", (0, -0.60, 1.10), "Neck", tail=(0, -0.35, 0.05))          # throat pivot
    k.joint("Jaw", (0, -0.92, 1.05), "Head", tail=(0, -0.3, 0))
    for s, side in ((1, "L"), (-1, "R")):
        k.joint("Ear_" + side, (s * 0.22, -0.66, 1.64), "Head", tail=(0, 0, 0.3))
        k.joint("Leg_F" + side, (s * 0.25, -0.42, 0.70), "Chest", tail=(0, 0, -0.45))
        k.joint("Leg_B" + side, (s * 0.215, 0.38, 0.70), "Spine", tail=(0, 0, -0.45))
    k.joint("Tail1", (0, 0.58, 0.95), "Spine")
    k.joint("Tail2", (0, 0.88, 1.35), "Tail1")
    k.joint("Tail3", (0, 0.76, 1.46), "Tail2", tail=(0, 0.3, 0.4))


def check_pairs():
    return [("Leg_FL", "Leg_BL"), ("Leg_FR", "Leg_BR"), ("Leg_FL", "Leg_FR"), ("Leg_BL", "Leg_BR"),
            ("Head", "Leg_FL"), ("Head", "Leg_FR"), ("Jaw", "Leg_FL"), ("Jaw", "Leg_FR"), ("Head", "Chest"),
            ("Jaw", "Chest"), ("Ear_L", "Ear_R"), ("Tail1", "Leg_BL"), ("Tail1", "Leg_BR"), ("Tail3", "Spine")]


def joints():
    return [((0, -0.56, 1.06), (0, -0.62, 1.12), 0.30, "Head"), ((0.22, -0.66, 1.64), (-0.22, -0.66, 1.64), 0.10, "Head")]


# ------------------------------------------------------------------ animation
import petkit as pk
import _common as cm
TAIL = ["Tail1", "Tail2", "Tail3"]


def ears(k, f, l=0.0, r=None, splay=0.0):
    r = l if r is None else r
    k.key("Ear_L", f, rot=(l, 0, splay))
    k.key("Ear_R", f, rot=(r, 0, -splay))


def idle(k):
    """Proud sentinel: scans left and right with snappy turns and holds, ear flicks, light panting, tail bolt sways,
    then puffs its chest out with the chin raised high before settling again."""
    n = 120
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 2):
        b = pk.wave(f, n, 0, 3)
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, 0.012 * b))
        k.key("Chest", f, rot=(-1.5 - 1.2 * b, 0, 0))
        cm.chain(k, f, n, TAIL, sway=7, pitch=0, cycles=2, lag=0.12, grow=0.5)
        k.key("Jaw", f, rot=(3 + 3 * pk.wave(f, n, 0, 10), 0, 0))
    # head: look ahead -> left -> right -> ahead (snappy turns, holds)
    for f, nk, hd, yaw, tilt in ((0, -6, -6, 0, 0), (22, -6, -6, 0, 0), (28, -8, -4, 26, 4), (48, -8, -4, 26, 4),
                                 (54, -6, -8, -22, -3), (74, -6, -8, -22, -3), (80, -6, -6, 0, 0),
                                 (86, -6, -6, 0, 0), (92, -14, -10, 0, 0), (106, -14, -10, 0, 0), (114, -6, -6, 0, 0), (120, -6, -6, 0, 0)):
        k.key("Neck", f, rot=(nk, yaw * 0.4, 0))
        k.key("Head", f, rot=(hd, yaw * 0.6, tilt))
    # ears: perked, flick right at 40, flick left at 66, both perk forward when it looks around
    for f, l, r in ((0, 0, 0), (26, 6, 6), (38, 6, 6), (40, 6, -22), (43, 6, 6), (46, 6, -16), (50, 6, 6),
                    (64, 4, 4), (66, -22, 4), (70, 4, 4), (82, 0, 0), (120, 0, 0)):
        ears(k, f, l, r)
    # proud chest puff 86-112: chest lifts, chin high, then settles
    for f, ch in ((84, -1.5), (92, -7), (106, -7), (114, -1.5)):
        k.key("Chest", f, rot=(ch, 0, 0))
    cm.plant(k, n)
    k.finish()


def walk(k):
    n = 20

    def body(f):
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(1.0 * pk.wave(f, n, 0.1, 2), 0, 2.2 * pk.wave(f, n)), loc=(0, 0, 0.035 * b))
        k.key("Chest", f, rot=(-1.5, 3.0 * pk.wave(f, n, 0.25), -1.5 * pk.wave(f, n)))
        k.key("Neck", f, rot=(-4 + 2.5 * pk.wave(f, n, 0.15, 2), 0, 0))
        k.key("Head", f, rot=(-4 - 2.5 * pk.wave(f, n, 0.2, 2), -2 * pk.wave(f, n, 0.25), 0))
        k.key("Jaw", f, rot=(5 + 2 * pk.wave(f, n, 0, 2), 0, 0))
        ears(k, f, -8, -8)
        cm.chain(k, f, n, TAIL, sway=9, pitch=-4, cycles=1, lag=0.15)
    return cm.quad_walk(k, n, 0.20, 0.09, body, gait="trot")


def roar(k):
    """HOWL: leans back, chin to the sky, jaw wide open, ears pinned back, tail bolt snaps up and buzzes."""
    n = 66
    k.new_action("roar", n, False)
    P = [(0, 0, -6, -6, 3, 0), (10, -6, -14, -12, 6, 0.4), (20, -10, -26, -30, 28, 1), (48, -10, -28, -32, 30, 1),
         (56, -3, -12, -10, 8, 0.3), (66, 0, -6, -6, 3, 0)]
    for f, ch, nk, hd, jw, t in P:
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, -0.03 * t))
        k.key("Chest", f, rot=(ch, 0, 0))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        ears(k, f, -30 * t, -30 * t)
        for i, b in enumerate(TAIL):
            k.key(b, f, rot=(14 * t, 0, 0))
    for f in range(22, 48, 2):          # the howl wavers
        w = 1 if (f // 2) % 2 else -1
        k.key("Head", f, rot=(-31, 0, 2.5 * w))
        k.key("Tail3", f, rot=(14, 7 * w, 0))
    cm.plant(k, n)
    k.finish(loop=False)


def thunderflip(k):
    """SIGNATURE (Raiju only): crouches low with ears pinned, EXPLODES upward into a full barrel roll with all four
    legs tucked, lands on all fours and holds a proud power pose (chest high, chin up, tail bolt raised)."""
    import bpy
    n = 64
    k.new_action("act_thunderflip", n, False)
    Y = (0, 1, 0)
    # body path: (frame, spine z, roll degrees about the body axis, chest pitch, neck, head, ears, tail pitch)
    P = [(0, 0.0, 0, 0, -6, -6, 0, 0), (8, -0.07, 0, 4, -2, -4, -20, 4), (14, -0.11, 0, 6, 0, -2, -30, 4),
         (18, 0.30, 0, -4, -10, -8, -30, 8), (21, 0.70, 90, -2, -8, -8, -30, 10), (24, 0.95, 180, 0, -6, -8, -30, 10),
         (27, 0.95, 270, 0, -6, -8, -30, 10), (30, 0.70, 360, -2, -8, -8, -26, 6), (34, 0.18, 360, -4, -16, -14, -10, 0),
         (38, -0.08, 360, 2, -10, -8, 0, 0), (44, 0.0, 360, -6, -14, -10, 10, 14), (56, 0.0, 360, -6, -14, -10, 10, 14),
         (64, 0.0, 360, 0, -6, -6, 0, 0)]
    for f, z, roll, ch, nk, hd, ear, tp in P:
        cm.key_axis(k, "Spine", f, Y, roll, loc=(0, 0, z))
        k.key("Chest", f, rot=(ch, 0, 0))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(14 if 44 <= f <= 56 else 3, 0, 0))
        ears(k, f, ear, ear)
        for i, b in enumerate(TAIL):
            k.key(b, f, rot=(tp, 0, 0))
    k.bake_bezier_now()
    sc = bpy.context.scene
    for f in list(range(0, 17)) + list(range(36, n + 1)):          # paws planted before take-off and after landing
        sc.frame_set(f)
        for leg in cm.LEGS4:
            k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, 0.0)))
    for f, front, back, spl in ((18, 30, 34, 0), (22, 16, -16, 12), (30, 16, -16, 12), (34, 0, 4, 2)):  # push, tuck, reach
        for leg in cm.LEGS4:
            sx = 1 if leg.endswith("L") else -1
            k.key(leg, f, rot=(front if "_F" in leg else back, 0, -sx * spl), loc=(0, 0, 0))
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    thunderflip(k)
    return stride


# head group moved 0.12 forward / 0.18 up (scale 1 = translation only): clears the shoulders in the howl and walk
HEAD_XF = [((0, -0.60, 1.10), 1.0, ("Head", "Jaw", "Ear_L", "Ear_R"), (0, -0.12, 0.18))]
