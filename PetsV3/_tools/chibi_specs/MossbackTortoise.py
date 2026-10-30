# Mossback Tortoise (Wood egg #1, T1 Grass, quad lovely): a friendly old tortoise carrying a little garden, rebuilt to
# STYLE_BIBLE.md (2026-10-08 pro pass): a wide 3-tier stepped shell (tan rim band of 1x2 tiles, brown 2x2 scutes with
# dark gaps), a moss carpet with one chunky bonsai, 2 flower clusters and a red mushroom; a big round-faced head on a
# short thick neck with lovely eyes, blush and a little smile; stump legs with light toenails.
# Own moves: idle = stretches its neck out to look around, grazes (bite + chew), the bonsai sways in the wind, settles
# a front foot; walk = slow heavy lateral walk with the tortoise head-bob; roar = SNAP-HISS (pulls back, shoots the neck
# out gaping, double snap); signature = SHELL SPIN (pulls everything into the shell, spins twice like a top while the
# bonsai whips out, pops back out with a snap).
import math
from mathutils import Vector, Matrix

DISPLAY = "Mossback Tortoise"
MOTION = "Walk"
RIG = "quad"
HEIGHT = 7.0

SKIN = (104, 176, 76)
JAW = (214, 226, 150)
PLASTRON = (226, 204, 140)
RIM = (214, 168, 104)          # tan rim band (a warmer step of the plastron)
DARK = (60, 42, 30)
SHELL = (132, 88, 52)
GAP = (88, 58, 36)
MOSS = (92, 190, 72)
MOSS_L = (150, 220, 96)
PINK = (255, 156, 196)
YELLOW = (255, 228, 110)
RED = (226, 62, 56)
STEM = (246, 240, 226)
IRIS = (150, 96, 52)            # V 59 %: the dark pupil reads at game distance
MOUTH = (150, 56, 60)
TONGUE = (236, 110, 140)
BLUSH = (236, 132, 138)

TH = 0.62                       # plate-grid torso height (shell tiers carry hand-laid scutes instead)
# shell tiers (centre, half) - rim 1.0 S, mid 0.82 S, cap 0.60 S (S = 1.60)
PLAS = ((0, 0.0, 0.34), (0.62, 0.78, 0.06))
TIERS = {"rim": ((0, 0.0, 0.51), (0.80, 0.92, 0.13)),
         "mid": ((0, 0.02, 0.77), (0.656, 0.76, 0.15)),
         "cap": ((0, 0.04, 1.01), (0.48, 0.56, 0.11))}
# legs: hip (in the shell), knee (hidden in the shell), ankle; the stump block hangs straight under the rim
LEGS = {"F": ((0.50, -0.50, 0.80), (0.56, -0.62, 0.46), (0.62, -0.50, 0.10)),
        "B": ((0.50, 0.50, 0.80), (0.56, 0.62, 0.46), (0.62, 0.50, 0.10))}
HEAD_C = Vector((0, -1.38, 1.00))
HEAD_H = Vector((0.44, 0.34, 0.335))          # HW 0.88 = 0.55 S, HH 0.67 = 0.42 S


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


def frame(u, n):
    """rotation: local x = u (along the face), local z = n (face normal), local y = z x x"""
    z = Vector(n).normalized()
    x = Vector(u).normalized()
    y = z.cross(x)
    return Matrix((x, y, z)).transposed()


def tiles(B, c, h, key, cols, rows, color, bone, gap=0.045, relief=0.05, margin=0.05, vr=None, ur=None,
          skip=None, taper=0.74):
    """a grid of raised chamfered tiles on face `key` of an axis-aligned untapered box (c, h): scutes / rim plates.
    ur / vr: (lo, hi) face-coordinate range (default = the face minus `margin`); skip(p) -> True drops a tile."""
    c, h = Vector(c), Vector(h)
    ax = {"x": 0, "y": 1, "z": 2}[key[1]]
    sg = 1 if key[0] == "+" else -1
    n = Vector((0, 0, 0))
    n[ax] = sg
    ua, va = [(1, 2), (0, 2), (0, 1)][ax]
    u = Vector((0, 0, 0))
    u[ua] = 1
    lo_u, hi_u = ur or (c[ua] - h[ua] + margin, c[ua] + h[ua] - margin)
    lo_v, hi_v = vr or (c[va] - h[va] + margin, c[va] + h[va] - margin)
    tw = (hi_u - lo_u - gap * (cols - 1)) / cols
    tv = (hi_v - lo_v - gap * (rows - 1)) / rows
    R = frame(u, n)
    out = []
    for i in range(cols):
        for j in range(rows):
            p = Vector((0, 0, 0))
            p[ua] = lo_u + tw / 2 + i * (tw + gap)
            p[va] = lo_v + tv / 2 + j * (tv + gap)
            p[ax] = c[ax] + sg * (h[ax] + relief / 2 - 0.012)
            if skip and skip(p):
                continue
            out.append(B.add(p, (tw / 2, tv / 2, relief / 2), color, bone, R=R, top=(taper, taper), studs=[],
                             role="detail", bevel=0.006))
    return out


def model(k):
    """STYLE_BIBLE MossbackTortoise: wide 3-tier stepped shell + garden, big friendly head forward on a short thick
    neck (face at ~85 % of the shell height), lovely eyes, blush, 3-bar smile, stump legs with 3 light toenails."""
    import blockkit as bk
    B = bk.Blocks(k, seed=41, tier=1, th=TH)
    D = 0.62
    # ---- shell: cream plastron, tan rim band of 1x2 tiles, 2 tiers of brown 2x2 scutes over dark gaps
    B.add(PLAS[0], PLAS[1], PLASTRON, "Spine", studs=[], role="mass")
    RND = {"rim": None, "mid": 0.34, "cap": 0.40}                 # rounder upper tiers = a dome, not a ziggurat
    for nm, (c, h) in TIERS.items():
        B.add(c, h, GAP, "Spine", studs=[], role="mass", rnd=RND[nm])

    def neck_skip(p):
        return (abs(p.x) < 0.50 and p.y < -0.5 and p.z < 0.98) or (abs(p.x) < 0.16 and p.y > 0.9 and p.z < 0.56)

    c, h = TIERS["rim"]
    for key, cols in (("+x", 7), ("-x", 7), ("-y", 6), ("+y", 6)):
        tiles(B, c, h, key, cols, 1, RIM, "Spine", gap=0.05, relief=0.05, margin=0.06, skip=neck_skip)
    c, h = TIERS["mid"]
    for key, cols in (("+x", 5), ("-x", 5), ("-y", 4), ("+y", 4)):
        tiles(B, c, h, key, cols, 1, SHELL, "Spine", gap=0.055, relief=0.06, skip=neck_skip,
              vr=(c[2] - h[2] + 0.06, c[2] + h[2] - 0.065),
              ur=None if key[1] == "y" else (c[1] - h[1] + 0.08, c[1] + h[1] - 0.08))
    c, h = TIERS["cap"]
    for key, cols in (("+x", 4), ("-x", 4), ("-y", 3), ("+y", 3)):
        tiles(B, c, h, key, cols, 1, SHELL, "Spine", gap=0.055, relief=0.055,
              vr=(c[2] - h[2] + 0.05, c[2] + h[2] - 0.055),
              ur=(c[0] - h[0] + 0.08, c[0] + h[0] - 0.08) if key[1] == "y" else (c[1] - h[1] + 0.08, c[1] + h[1] - 0.08))
    # ledge tiles: the rim's top ring (tan) and the mid tier's top ring (brown scutes) read from above
    (rc, rh), (mc, mh), (cc, chh) = TIERS["rim"], TIERS["mid"], TIERS["cap"]
    for (ic, ih), (oc, oh), col, nlong, nshort in (((mc, mh), (rc, rh), RIM, 7, 6), ((cc, chh), (mc, mh), SHELL, 5, 4)):
        z = oc[2] + oh[2]
        for s in (1, -1):
            x0, x1 = ic[0] + ih[0], oc[0] + oh[0]
            xm = s * (x0 + x1) / 2
            hw = (x1 - x0) / 2
            tiles(B, (xm, oc[1], z - 0.01), (hw, oh[1], 0.01), "+z", 1, nlong, col, "Spine", gap=0.04,
                  relief=0.04, ur=(xm - hw + 0.03, xm + hw - 0.03),
                  vr=(oc[1] - oh[1] + 0.05, oc[1] + oh[1] - 0.05), skip=neck_skip)
            y0, y1 = ic[1] + s * ih[1], oc[1] + s * oh[1]
            ym = (y0 + y1) / 2
            hd = abs(y1 - y0) / 2
            tiles(B, (0, ym, z - 0.01), (ih[0], hd, 0.01), "+z", nshort, 1, col, "Spine", gap=0.04,
                  relief=0.04, ur=(-ih[0] + 0.02, ih[0] - 0.02), vr=(ym - hd + 0.03, ym + hd - 0.03), skip=neck_skip)
    # ---- garden: moss carpet + edge drips, a chunky bonsai (Tree bone), 2 flower clusters, a red mushroom
    ctop = cc[2] + chh[2]
    B.add((0, cc[1], ctop + 0.03), (0.43, 0.51, 0.045), MOSS, "Spine", studs=["+z"], density=0.55, role="mass")
    for x, y, hw, hd in ((0.47, -0.22, 0.03, 0.11), (-0.47, 0.20, 0.03, 0.13), (0.18, 0.59, 0.12, 0.03),
                         (-0.26, -0.58, 0.10, 0.03)):
        B.add((x, y + cc[1], ctop - 0.035), (hw, hd, 0.075), MOSS, "Spine", studs=[], role="limb")
    tz = ctop + 0.07
    B.add((0.02, 0.18, tz + 0.02), (0.10, 0.10, 0.04), SHELL, "Tree", studs=[], role="limb")            # root flare
    B.seg((0.02, 0.18, tz), (0.06, 0.20, tz + 0.24), 0.072, 0.072, SHELL, "Tree", studs=[], role="limb")
    B.seg((0.06, 0.20, tz + 0.22), (-0.02, 0.18, tz + 0.42), 0.066, 0.066, SHELL, "Tree", studs=[], role="limb",
          ext=0.04)
    B.seg((0.04, 0.20, tz + 0.26), (0.20, 0.16, tz + 0.40), 0.045, 0.045, SHELL, "Tree", studs=[], role="limb")
    for p, hh, col in (((-0.02, 0.18, tz + 0.58), (0.25, 0.23, 0.17), MOSS_L),
                       ((0.22, 0.12, tz + 0.46), (0.16, 0.15, 0.12), MOSS),
                       ((-0.22, 0.26, tz + 0.44), (0.15, 0.15, 0.11), MOSS)):
        B.add(p, hh, col, "Tree", studs=["+z", "-y", "+x", "-x", "+y"], density=0.8, rnd=0.30, role="mass")
    for pts, col, mid in ((((-0.29, -0.18), (-0.13, -0.30), (-0.31, -0.38)), PINK, YELLOW),
                          (((0.30, 0.34), (0.15, 0.46), (0.31, 0.52)), YELLOW, PINK)):
        for i, (x, y) in enumerate(pts):
            z = tz + 0.01 + 0.03 * (i == 1)
            B.add((x, y, z), (0.05, 0.05, 0.03), MOSS, "Spine", studs=[], role="detail")
            B.add((x, y, z + 0.05), (0.085, 0.085, 0.032), col, "Spine", studs=[], role="limb", rnd=0.3)
            B.add((x, y, z + 0.088), (0.034, 0.034, 0.012), mid, "Spine", studs=[], role="detail")
    mx, my = 0.27, -0.30
    B.add((mx, my, tz + 0.05), (0.035, 0.035, 0.07), STEM, "Spine", studs=[], role="detail")
    B.add((mx, my, tz + 0.15), (0.10, 0.10, 0.05), RED, "Spine", top=(0.62, 0.62), studs=[], role="limb")
    for dx, dy in ((-0.04, -0.03), (0.04, 0.02)):
        B.add((mx + dx, my + dy, tz + 0.196), (0.018, 0.018, 0.008), STEM, "Spine", studs=[], role="detail")
    # ---- short thick neck + big head (front face -y): lovely eyes, blush, light snout + jaw with a 3-bar smile
    B.add((0, -0.92, 0.80), (0.40, 0.24, 0.23), SKIN, "Neck", studs=[], role="limb")
    head = B.add(HEAD_C, HEAD_H, SKIN, "Head", top=(0.94, 0.94), density=D)
    hb = HEAD_C.z - HEAD_H.z                                  # head bottom
    fy = HEAD_C.y - HEAD_H.y                                  # face plane
    B.add((0, fy - 0.06, hb + 0.11), (0.27, 0.13, 0.09), JAW, "Head", top=(0.88, 0.85), studs=[], role="limb")
    for s in (1, -1):
        B.add((s * 0.075, fy - 0.19, hb + 0.165), (0.022, 0.006, 0.016), DARK, "Head", studs=[], bevel=0.004)
    # smile: 3 bars (centre flat, ends tipped up) on the snout front
    B.add((0, fy - 0.193, hb + 0.075), (0.045, 0.006, 0.014), DARK, "Head", studs=[], bevel=0.004)
    for s in (1, -1):
        B.add((s * 0.075, fy - 0.193, hb + 0.088), (0.04, 0.006, 0.014), DARK, "Head", rot=(0, -s * 28, 0), studs=[],
              bevel=0.004)
    B.add((0, fy + 0.02, hb + 0.012), (0.24, 0.12, 0.008), MOUTH, "Head", studs=[], bevel=0.004)       # mouth roof
    B.add((0, fy + 0.04, hb - 0.035), (0.30, 0.20, 0.06), JAW, "Jaw", bot=(0.9, 0.9), studs=[], role="limb")
    B.add((0, fy + 0.02, hb + 0.027), (0.22, 0.12, 0.006), MOUTH, "Jaw", studs=[], bevel=0.004)
    B.add((0, fy - 0.02, hb + 0.034), (0.10, 0.06, 0.006), TONGUE, "Jaw", studs=[], bevel=0.004)
    B.face_eyes(head, "lovely", IRIS, base=SKIN, z=0.58, pupil_size=(0.10, 0.12), hl_size=(0.08, 0.0), look=(0, -0.6))
    for s in (1, -1):
        B.add((s * 0.335, fy - 0.004, hb + 0.22), (0.06, 0.006, 0.024), BLUSH, "Head", studs=[], bevel=0.006)
    # ---- stump legs splayed 8 deg, light toenails
    for s, side in ((1, "L"), (-1, "R")):
        for fb in ("F", "B"):
            H, K, A = (X(p, s) for p in LEGS[fb])
            leg, shin, foot = "Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side
            B.seg(H, K, 0.15, 0.15, SKIN, leg, ext=0.04, studs=[], role="limb")
            top = Vector((A.x - s * 0.05, A.y, 0.52))
            bot = Vector((A.x, A.y, 0.10))
            B.seg(bot, top, 0.19, 0.19, SKIN, shin, side=(1, 0, 0), density=0.95, studs=["+x", "-x", "-y", "+y"])
            B.add((A.x, A.y - 0.02, 0.06), (0.205, 0.22, 0.06), SKIN, foot, studs=[], role="limb")
            for gx in (-0.11, 0.0, 0.11):
                B.add((A.x + gx, A.y - 0.235, 0.045), (0.036, 0.03, 0.035), PLASTRON, foot, studs=[], role="detail",
                      bevel=0.012)
    # ---- short pointed tail
    B.seg((0, 0.86, 0.46), (0, 1.20, 0.40), 0.12, 0.05, SKIN, "Tail1", side=(1, 0, 0), top=(0.15, 0.6), studs=[],
          role="limb")
    B.build()
    return {"plates": B.stud_count, "TH": round(B.th, 3), "cell": round(B.pcell, 3)}


def rig(k):
    k.joint("Spine", (0, 0.04, 0.70), "Root", tail=(0, -0.4, 0))
    k.joint("Tree", (0.02, 0.18, 1.19), "Spine", tail=(0, 0, 0.4))
    k.joint("Neck", (0, -0.70, 0.80), "Spine", tail=(0, -0.4, 0.1))
    k.joint("Head", (0, -1.08, 0.72), "Neck", tail=(0, -0.4, 0.05))          # throat pivot
    k.joint("Jaw", (0, -1.30, 0.66), "Head", tail=(0, -0.3, 0))
    for s, side in ((1, "L"), (-1, "R")):
        for fb, knee in (("F", (0, -1, 0)), ("B", (0, 1, 0))):
            H, K, A = (X(p, s) for p in LEGS[fb])
            k.joint("Leg_" + fb + side, H, "Spine")
            k.joint("Shin_" + fb + side, K, "Leg_" + fb + side)
            k.joint("Foot_" + fb + side, A, "Shin_" + fb + side, tail=(0, -0.25, 0))
            k.add_leg2("Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side, knee=knee)
    k.joint("Tail1", (0, 0.86, 0.46), "Spine", tail=(0, 0.3, -0.1))


# ------------------------------------------------------------------ animation
import petkit as pk
import _common as cm

LEGS4 = ["Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR"]


def tree(k, f, n, amp=1.0, pitch=0.0, roll=0.0):
    """wind in the tree: slow two-axis sway (+ extra pitch / roll for reactions)"""
    k.key("Tree", f, rot=(amp * 1.6 * pk.wave(f, n, 0, 2) + pitch, 0, amp * 2.4 * pk.wave(f, n, 0.3, 2) + roll))


def neck(k, f, pitch=0.0, yaw=0.0, ly=0.0, head=0.0, hyaw=0.0, jaw=3.0):
    k.key("Neck", f, rot=(pitch, yaw, 0), loc=(0, ly, 0))
    k.key("Head", f, rot=(head, hyaw, 0))
    k.key("Jaw", f, rot=(jaw, 0, 0))


def idle(k):
    """old guardian: slow breaths, stretches its neck out and looks around (holds), grazes (bite, tear, chew), the
    tree sways in the wind, settles its right fore-foot."""
    import bpy
    n = 160
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 2):
        b = pk.wave(f, n, 0, 4)
        sp = 3.0 * max(0.0, math.sin(math.pi * (f - 104) / 40)) if 104 <= f <= 144 else 0.0
        k.key("Spine", f, rot=(0.5 * b + sp, 0, 0), loc=(0, 0, 0.01 * b))
        tree(k, f, n)
        k.key("Tail1", f, rot=(0, 4 * pk.wave(f, n, 0.1, 2), 0))
    for row in ((0, 0, 0, 0, 0, 0, 3), (24, 0, 0, 0, 0, 0, 3),
                (40, -6, 14, -0.12, -4, 18, 3), (70, -6, 14, -0.12, -4, 18, 3),
                (82, -2, -10, -0.06, 0, -16, 3), (98, -2, -10, -0.06, 0, -16, 3),
                (114, 12, 0, -0.10, 8, 0, 3), (118, 13, 0, -0.10, 9, 0, 18), (121, 11, 0, -0.10, 7, 0, 1),
                (127, 6, 0, -0.02, 4, 0, 12), (131, 6, 0, -0.02, 4, 0, 2), (135, 4, 0, 0, 2, 0, 12),
                (139, 4, 0, 0, 2, 0, 2), (148, 0, 0, 0, 0, 0, 3), (160, 0, 0, 0, 0, 0, 3)):
        f, p, y, ly, h, hy, j = row
        neck(k, f, p, y, ly, h, hy, j)
    k.bake_bezier_now()
    sc = bpy.context.scene
    for f in range(0, n + 1):
        sc.frame_set(f)
        for leg in LEGS4:
            T = Vector((k.J[leg].x, k.J[leg].y, 0.0))
            if leg == "Leg_FR" and 50 <= f <= 62:
                T.z = 0.09 * math.sin(math.pi * (f - 50) / 12)
            k.solve_leg(leg, f, T)
    k.finish()
    k.meta["planted"] = ["Leg_FL", "Leg_BL", "Leg_BR"]      # FR lifts + re-plants on purpose (weight shift)


def walk(k):
    n = 40

    def body(f):
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(0.6 * pk.wave(f, n, 0.1, 2), 1.2 * pk.wave(f, n, 0.0), 3.0 * pk.wave(f, n, 0.0)),
              loc=(0, 0, -0.02 * b))
        k.key("Neck", f, rot=(2 * pk.wave(f, n, 0.15, 2), 3 * pk.wave(f, n, 0.25), 0),
              loc=(0, -0.05 * pk.wave(f, n, 0.1, 2), 0))
        k.key("Head", f, rot=(-2 * pk.wave(f, n, 0.15, 2), -2 * pk.wave(f, n, 0.25), 0))
        k.key("Jaw", f, rot=(3, 0, 0))
        k.key("Tail1", f, rot=(0, 8 * pk.wave(f, n, 0.3), 0))
        k.key("Tree", f, rot=(1.5 * pk.wave(f, n, 0.2, 2), 0, -3.5 * pk.wave(f, n, 0.15)))
    return cm.quad_walk(k, n, 0.13, 0.08, body, gait="walk")


def roar(k):
    """SNAP-HISS: pulls the head back and rears, shoots the neck out with the beak gaping (hiss, jaw trembling),
    then two hard snaps; the tree jolts with each snap, tail lifts."""
    n = 64
    k.new_action("roar", n, False)
    P = [(0, 0, 0, 0, 3, 0, 0), (10, -8, 0.14, -6, 3, -2, -0.02), (15, -10, -0.26, -14, 42, 4, -0.04),
         (34, -10, -0.26, -14, 40, 4, -0.04), (38, -8, -0.32, -10, 0, 5, -0.04), (42, -9, -0.27, -12, 30, 4, -0.04),
         (45, -8, -0.32, -10, 0, 5, -0.04), (54, -2, -0.05, -2, 3, 1, -0.01), (64, 0, 0, 0, 3, 0, 0)]
    for f, p, ly, h, j, spp, z in P:
        k.key("Spine", f, rot=(spp, 0, 0), loc=(0, 0, z))
        neck(k, f, p, 0, ly, h, 0, j)
        k.key("Tail1", f, rot=(14 * (10 <= f <= 45), 0, 0))
    for f in range(17, 34, 2):
        k.key("Jaw", f, rot=(40 + (3 if (f // 2) % 2 else -3), 0, 0))
    for f, tp in ((0, 0), (36, 0), (39, 5), (43, -3), (46, 4), (50, -2), (56, 0), (64, 0)):
        k.key("Tree", f, rot=(tp, 0, 0))
    cm.plant(k, n, legs=LEGS4)
    k.finish(loop=False)


def shellspin(k):
    """SIGNATURE - SHELL SPIN: crouches, pulls head, tail and legs into the shell, drops onto its plastron and spins
    twice like a top (with a wobble; the tree leans out), rocks to a stop, pushes back up and pops its head out with
    a snap."""
    import bpy
    from mathutils import Quaternion
    n = 112
    DROP = -0.25                 # plastron bottom (z 0.28) comes to rest just above the ground
    k.new_action("act_shellspin", n, False)
    for f, z, p in ((0, 0, 0), (8, -0.06, 2), (14, -0.08, 0), (24, DROP, 0)):
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
    for f in range(25, 84):
        u = (f - 24) / 60
        deg = 720 * (0.5 - 0.5 * math.cos(math.pi * u))
        phi = math.radians(deg * 0.4 + 30)
        extra = Quaternion((math.cos(phi), math.sin(phi), 0), math.radians(3.5 * math.sin(math.pi * u)))
        cm.key_axis(k, "Spine", f, (0, 0, 1), deg, loc=(0, 0, DROP), extra=extra)
    for f, z, p in ((84, DROP, 0), (86, DROP, 3), (89, DROP, -2), (92, DROP, 0), (102, 0.02, 0), (106, 0, 0),
                    (112, 0, 0)):
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
    for f, p, ly, h, j in ((0, 0, 0, 0, 3), (10, -4, 0, -4, 3), (16, 0, 0.14, 0, 3), (96, 0, 0.14, 0, 3),
                           (101, -6, -0.06, -6, 3), (104, -4, 0, -4, 30), (107, -2, 0, -2, 0), (112, 0, 0, 0, 3)):
        neck(k, f, p, 0, ly, h, 0, j)
    for f, y, p in ((0, 0, 0), (10, 0, 0), (16, 0, 34), (94, 0, 34), (102, 0, 0), (112, 0, 0)):
        k.key("Tail1", f, rot=(p, y, 0))
    for f, tp in ((0, 0), (14, 0), (24, -2), (40, -10), (54, -13), (70, -10), (84, -2), (87, 10), (91, -5), (95, 2),
                  (100, 0), (112, 0)):
        k.key("Tree", f, rot=(tp, 0, 0))
    k.bake_bezier_now()

    def tuck(f):
        if f <= 12 or f >= 92:
            return 0.0
        if f < 24:
            u = (f - 12) / 12
        elif f <= 84:
            return 1.0
        else:
            u = 1 - (f - 84) / 8
        return 0.5 - 0.5 * math.cos(math.pi * u)

    sc = bpy.context.scene
    J = k.J
    sp = k.arm.pose.bones["Spine"]
    sp_rest_inv = k.arm.data.bones["Spine"].matrix_local.inverted()
    for f in range(0, n + 1):
        sc.frame_set(f)
        M = sp.matrix @ sp_rest_inv
        u = tuck(f)
        for leg in LEGS4:
            s = 1 if leg.endswith("L") else -1
            L = k.legs2[leg]
            T = Vector((J[leg].x, J[leg].y, 0.0))
            if u > 0:         # real tortoise tuck: forelegs fold forward (armour out), hind legs fold back, lifted in
                hipR, ankR = J[leg], J[L["foot"]]
                fy = 0.18 if leg[4] == "F" else -0.12
                At = M @ (hipR + Vector((s * 0.05, fy, -0.18)))
                Tt = Vector((At.x - (ankR.x - hipR.x), At.y - (ankR.y - hipR.y), At.z - ankR.z))
                T = T.lerp(Tt, u)
            k.solve_leg(leg, f, T)
            if u > 0:
                k.key(leg, f, loc=(0, 0, 0.22 * u))
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    shellspin(k)
    return stride


def check_pairs():
    P = [("Leg_FL", "Leg_FR"), ("Leg_BL", "Leg_BR"), ("Leg_FL", "Leg_BL"), ("Leg_FR", "Leg_BR"),
         ("Shin_FL", "Shin_FR"), ("Shin_BL", "Shin_BR"), ("Shin_FL", "Shin_BL"), ("Shin_FR", "Shin_BR"),
         ("Foot_FL", "Foot_FR"), ("Foot_BL", "Foot_BR")]
    for a in ("Head", "Jaw"):
        for b in ("Leg_FL", "Leg_FR", "Shin_FL", "Shin_FR", "Foot_FL", "Foot_FR"):
            P.append((a, b))
    for b in ("Leg_BL", "Leg_BR", "Shin_BL", "Shin_BR"):
        P.append(("Tail1", b))
    return P
