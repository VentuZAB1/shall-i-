# Kraken (Tide egg) - FIERCE style (2026-10-09, FIERCE_PLAN.md "the deep terror"): a giant-squid mantle on octopus
# arms, built from tapered blocks and covered in Roblox studs: a tall maroon bullet mantle leaning back 15 deg with 2
# arrowhead fins at the top and a barnacle crust, an eye band at the mantle base with big sunken sockets, electric-blue
# eyes with horizontal slit pupils under heavy brow ridges, 6 big blue warning rings on the mantle (blue-ringed
# octopus), a hooked beak, and EIGHT arms (4 segments, tapering 0.18 -> 0.04 M, pale sucker discs underneath, tips
# curled). The 4 front arms (T1..T4) get a 4th tip bone so they can coil. Hovers (Motion = Swim). No glow.
# Old chibi version: _tools/chibi_specs/Kraken.py
import math
from mathutils import Vector, Matrix, Quaternion

DISPLAY = "Kraken"
MOTION = "Swim"
RIG = "kraken"
HEIGHT = 7.5                 # mantle ~5 studs at x1 (coordinator HEIGHT rule 2026-10-09)

# FIERCE_PLAN palette = in-game look; Roblox renders ~0.55-0.6x darker -> Blender colours ~1.8x brighter
BODY = (172, 42, 64)        # mantle maroon (plan 92,24,40)
BACK = (96, 22, 40)         # back, spots, brows (plan 50,12,24)
BODY_D = (136, 32, 52)      # darker mantle tip
UNDER = (236, 150, 140)     # underside + suckers (plan 168,98,96)
SUCK = (250, 196, 184)
BARN = (122, 114, 104)      # barnacle crust (plan 60,56,52)
BARN_L = (176, 168, 152)
RING = (40, 150, 255)       # accent: warning rings + eyes
EYE = (40, 150, 255)
EYE_HOT = (176, 216, 255)
BLACK = (14, 14, 22)
BEAK = (40, 22, 30)

H_MODEL = 1.66
PITCH = round(0.042 * (H_MODEL / HEIGHT) / (1.498 / 8.0), 4)

# arms: T1/T2 front pair, T3/T4 front-side pair (4 bones each, can coil), T5..T8 back (3 bones)
ANG = {1: 22.5, 2: -22.5, 3: 67.5, 4: -67.5, 5: 112.5, 6: -112.5, 7: 157.5, 8: -157.5}
FRONT = (1, 2, 3, 4)
Z0 = 0.0
RZ = [(0.22, 0.0, 0.44), (0.48, 0.02, 0.39), (0.76, 0.05, 0.27), (1.00, 0.06, 0.16), (1.20, 0.05, 0.11),
      (1.36, 0.02, 0.15), (1.43, -0.02, 0.27), (1.37, -0.05, 0.38), (1.26, -0.06, 0.37)]   # (radius, side, z): tip loop
HWS = [0.105, 0.090, 0.074, 0.058, 0.046, 0.036, 0.027, 0.020, 0.013]


def t_dirs(i):
    a = math.radians(ANG[i])
    d = Vector((math.sin(a), -math.cos(a), 0))       # radial (0 deg = front, -Y)
    t = Vector((math.cos(a), math.sin(a), 0))        # tangent: + rotation about it swings the arm DOWN
    return d, t


def t_path(i):
    d, t = t_dirs(i)
    cs = 1 if ANG[i] > 0 else -1                     # tips curl toward the back on both sides (mirror pairs)
    return [d * r + t * (w * cs) + Vector((0, 0, z + Z0)) for r, w, z in RZ]


def t_bones(i):
    return ["T%d%s" % (i, c) for c in ("abcd" if i in FRONT else "abc")]


MAN_C, MAN_H, MAN_ROT = Vector((0, 0.06, 0.92)), Vector((0.38, 0.34, 0.36)), -15.0


def man_R():
    return Matrix.Rotation(math.radians(MAN_ROT), 3, "X")


def man_pt(p):
    return MAN_C + man_R() @ Vector(p)


def model(k):
    import blockkit as bk
    B = bk.Blocks(k, seed=97, tier=3, plates=False, th=0.95)
    R = man_R()
    # ---------------- mantle: ONE continuous bullet leaning back 15 deg (walls taper into the darker cone tip),
    #                  eye band at its base
    man = B.add(MAN_C, MAN_H, BODY, "Head", R=R, bot=(0.95, 0.95), top=(0.58, 0.58), rnd=0.48)
    B.add(man_pt((0, 0.0, 0.58)), (0.22, 0.20, 0.24), BODY_D, "Head", R=R, top=(0.20, 0.24), rnd=0.45)   # tip
    band = B.add((0, 0.01, 0.545), (0.29, 0.31, 0.135), BODY, "Head", bot=(0.86, 0.86), top=(1.0, 1.0), rnd=0.40)
    B.add((0, 0.02, 0.42), (0.29, 0.27, 0.06), UNDER, "Spine", rnd=0.4)                          # underside skirt

    def mface(blk, ax, sg, u, z, out=0.006):
        """point + normal on a mantle block's +-x (ax 0: u = local y) or +-y (ax 1: u = local x) face"""
        t = (z / blk.h.z + 1) / 2
        sc = [blk.bot[i] + (blk.top[i] - blk.bot[i]) * t for i in (0, 1)]
        slope = blk.h[ax] * (blk.top[ax] - blk.bot[ax]) / (2 * blk.h.z)
        ln = Vector((0, 0, -sg * slope))
        ln[ax] = sg
        lp = Vector((0, 0, z))
        lp[ax] = sg * blk.h[ax] * sc[ax]
        lp[1 - ax] = u
        n = (blk.R @ ln).normalized()
        return blk.world(lp) + n * out, n

    def disc(c, n, r, thick, col, bone="Head", seg=12):
        u = (R @ Vector((0, 0, 1)) - n * (R @ Vector((0, 0, 1))).dot(n)).normalized()
        v = n.cross(u)
        pts = [c + (u * math.cos(a) + v * math.sin(a)) * r for a in [2 * math.pi * j / seg for j in range(seg)]]
        B.poly([c] + pts + [pts[0]], thick, col, bone)
    # ---------------- 6 big blue warning rings (blue-ringed octopus): dark outline, blue ring, dark-red centre
    for ax, sg, u, z, r in ((0, 1, -0.04, -0.14, 0.10), (0, 1, 0.03, 0.12, 0.10), (0, -1, -0.04, -0.14, 0.10),
                            (0, -1, 0.03, 0.12, 0.10), (1, 1, 0.11, -0.12, 0.09), (1, 1, -0.11, -0.12, 0.09)):
        c, n = mface(man, ax, sg, u, z, 0.0)
        disc(c + n * 0.006, n, r * 1.18, 0.008, BACK)
        disc(c + n * 0.010, n, r, 0.008, RING)
        disc(c + n * 0.014, n, r * 0.58, 0.008, BODY_D)
    # barnacle cones on the upper back
    for du, dz in ((0.0, 0.22), (0.07, 0.17), (-0.06, 0.26)):
        cc, nn = mface(man, 1, 1, du, dz, -0.01)
        B.spike(cc, nn, 0.07, 0.025, BARN_L, "Head", top=(0.45, 0.45))
    # ---------------- arrowhead fins swept back from the cone (flat blades; an arrowhead from the front)
    for s_, side in ((1, "L"), (-1, "R")):
        pts = [(0.32, 0.16, 0.36), (0.05, 0.08, 0.80), (0.64, 0.30, 0.34), (0.42, 0.24, 0.32), (0.24, 0.12, 0.16),
               (0.20, 0.08, 0.36), (0.11, 0.08, 0.56)]
        P = [man_pt((s_ * x, y, z)) for x, y, z in pts]
        B.poly(P, 0.045, BODY, "Fin_" + side)
    # ---------------- eye band: sunken slanted slit eyes (black socket, blue iris, horizontal slit pupil, hot outer
    #                  glint), a dark lower-lid ridge and a heavy brow ridge
    for s in (1, -1):
        Re = Matrix.Rotation(math.radians(-s * 18), 3, "Y")                       # slanted, flat on the band front
        c = Vector((s * 0.135, -0.272, 0.60))
        B.add(c + Re @ Vector((0, 0.01, 0)), (0.118, 0.035, 0.058), BLACK, "Head", R=Re, role="detail",
              bevel=0.01)                                                                            # socket
        B.add(c + Re @ Vector((0, -0.026, -0.004)), (0.098, 0.006, 0.033), EYE, "Head", R=Re, role="detail",
              bevel=0.005)                                                                           # iris
        B.add(c + Re @ Vector((-s * 0.018, -0.032, -0.004)), (0.056, 0.004, 0.010), BLACK, "Head", R=Re,
              role="detail", bevel=0.002)                                                            # slit pupil
        B.add(c + Re @ Vector((s * 0.072, -0.032, -0.004)), (0.022, 0.004, 0.011), EYE_HOT, "Head", R=Re,
              role="detail", bevel=0.002)                                                            # hot outer end
        B.add(c + Re @ Vector((0.0, -0.005, -0.073)), (0.11, 0.03, 0.02), BACK, "Head", R=Re, role="detail",
              bevel=0.01)                                                                            # lower lid
        Rb = Re @ Matrix.Rotation(math.radians(-s * 5), 3, "Y")
        B.add(c + Re @ Vector((0.0, -0.01, 0.074)), (0.13, 0.05, 0.03), BACK, "Head", R=Rb, role="detail",
              bevel=0.012)                                                                           # brow ridge
    # parrot-beak maw low in the arm crown: 2 hooked mandibles between T1 / T2
    B.add((0, -0.26, 0.38), (0.07, 0.05, 0.05), BEAK, "Head", bot=(0.6, 0.8), role="limb")
    B.spike((0, -0.29, 0.37), (0, -0.5, -1), 0.07, 0.04, BEAK, "Head", top=(0.15, 0.3), nostud=True)
    B.spike((0, -0.29, 0.33), (0, -0.5, 0.6), 0.07, 0.035, BEAK, "Head", top=(0.15, 0.3), nostud=True)
    # ---------------- eight arms: 6 tapered segments, pale underside strip + sucker discs, tips curl inward
    for i in range(1, 9):
        d, t = t_dirs(i)
        P = t_path(i)
        bn = t_bones(i)
        bones = [bn[0], bn[1], bn[2]] + [bn[-1]] * (len(P) - 4)
        for j in range(len(P) - 1):
            bone = bones[j]
            hw0, hw1 = HWS[j], HWS[j + 1]
            dirv = (P[j + 1] - P[j]).normalized()
            up = dirv.cross(t).normalized()
            last = j == len(P) - 2
            B.seg(P[j], P[j + 1], hw0, hw0 * 0.88, BODY, bone, side=t, ext=0.10 if j == 0 else 0.02,
                  top=((0.25 if last else hw1 / hw0), (0.30 if last else hw1 / hw0)), rnd=0.42)
            if j < 7:                                   # pale underside strip + suckers
                B.seg(P[j] - up * hw0 * 0.62, P[j + 1] - up * hw1 * 0.62, hw0 * 0.78, hw0 * 0.30, UNDER, bone,
                      side=t, ext=0.02, top=(hw1 / hw0, hw1 / hw0))
                L = (P[j + 1] - P[j]).length
                ns = 3 if L > 0.24 else 2
                for q in range(ns if j < 4 else (1 if j < 6 else 0)):
                    u = (q + 0.5) / ns
                    w = hw0 + (hw1 - hw0) * u
                    c = P[j].lerp(P[j + 1], u) - up * (w * 0.62 + w * 0.30 + 0.006)
                    B.add(c, (w * 0.42, w * 0.42, 0.012), SUCK, bone, R=bk.frame_from(c, c - up, dirv), studs=[],
                          rnd=0.45, role="detail")
    B.build()
    bk.stud_skin(k, PITCH)
    return {"TH": round(B.th, 3), "PITCH": PITCH}


def rig(k):
    k.joint("Spine", (0, 0.0, 0.48), "Root", tail=(0, 0, 0.3))
    k.joint("Head", (0, 0.02, 0.52), "Spine", tail=(0, 0.1, 0.6))           # mantle pivot at its base
    for s, side in ((1, "L"), (-1, "R")):
        k.joint("Fin_" + side, tuple(man_pt((s * 0.20, 0.10, 0.40))), "Head", tail=(s * 0.3, 0.05, 0.1))
    for i in range(1, 9):
        P = t_path(i)
        bn = t_bones(i)
        par = "Spine"
        for j, b in enumerate(bn):
            k.joint(b, tuple(P[j]), par, tail=P[j + 1] - P[j])
            par = b


def check_pairs():
    order = [1, 3, 5, 7, 8, 6, 4, 2]              # neighbours around the ring
    P = []
    for a, b in zip(order, order[1:] + order[:1]):
        for x in t_bones(a)[1:]:
            for y in t_bones(b)[1:]:
                P.append((x, y))
    for i in range(1, 9):
        for x in t_bones(i)[1:]:
            P.append((x, "Head"))
            P.append((x, "Spine"))
    return P


def joints():
    out = []
    for i in range(1, 9):
        P = t_path(i)
        for j, b in enumerate(t_bones(i)):
            if j:
                out.append((P[j], P[j], 0.11 if j == 1 else 0.09, b))
    return out


# ------------------------------------------------------------------ animation (FIERCE_PLAN: hover wave / kraken rise /
# jet swim / ship-crusher coil). Kraken-only motifs: the travelling arm-ring wave, the deimatic arm crown, the coil.
import petkit as pk
import _common as cm

ARM_RING = [1, 3, 5, 7, 8, 6, 4, 2]                # arms in order round the ring (front-left -> back -> front-right)


def ground_lift(k, n, target=0.03):
    """FLOOR RULE: raise the whole body (Spine z, keyed every frame) just enough that no arm vertex goes below target"""
    import bpy
    sc = bpy.context.scene
    body = k.main
    if not hasattr(k, "_tent_idx"):
        names = {g.index: g.name for g in body.vertex_groups}
        k._tent_idx = [v.index for v in body.data.vertices if v.groups and
                       names[max(v.groups, key=lambda g: g.weight).group][:1] == "T"]
    pb = k.arm.pose.bones["Spine"]
    R0 = k.arm.data.bones["Spine"].matrix_local.to_quaternion()
    k.bake_bezier_now()
    zs, base = [], []
    for f in range(0, n + 1):
        sc.frame_set(f)
        dg = bpy.context.evaluated_depsgraph_get()
        ev = body.evaluated_get(dg)
        me = ev.to_mesh()
        mw = ev.matrix_world
        zs.append(min((mw @ me.vertices[i].co).z for i in k._tent_idx))
        ev.to_mesh_clear()
        base.append((R0 @ pb.location).z)
    lift = [max(0.0, target - z) for z in zs]
    if max(lift) <= 0:
        return
    for f in range(0, n + 1):
        k.key("Spine", f, loc=(0, 0, base[f] + lift[f]))


def tent(k, f, i, a=0.0, b=0.0, c=0.0, d=0.0, twist=0.0, yb=0.0, yc=0.0, yd=0.0):
    """a/b/c/d + = that segment swings DOWN / curls under, - = lifts / curls back; twist sways the whole arm
    sideways; yb/yc/yd = sideways coil of b/c/d about the vertical (back arms: d folds into c)"""
    from mathutils import Quaternion
    _, t = t_dirs(i)
    bn = t_bones(i)
    Z = Vector((0, 0, 1))
    cm.key_axis(k, bn[0], f, t, a, extra=Quaternion(Z, math.radians(twist)))
    cm.key_axis(k, bn[1], f, t, b, extra=Quaternion(Z, math.radians(yb)))
    if len(bn) > 3:
        cm.key_axis(k, bn[2], f, t, c, extra=Quaternion(Z, math.radians(yc)))
        cm.key_axis(k, bn[3], f, t, d, extra=Quaternion(Z, math.radians(yd)))
    else:
        cm.key_axis(k, bn[2], f, t, c + 0.5 * d, extra=Quaternion(Z, math.radians(yc + 0.5 * yd)))


def fins(k, f, a):
    k.key("Fin_L", f, rot=(0, 0, -a))
    k.key("Fin_R", f, rot=(0, 0, a))


def idle(k):
    """HOVER WAVE: a slow bob while a travelling wave rolls round the arm ring (each arm lifts and curls in turn)
    and the fins ripple."""
    n = 120
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 2):
        k.key("Spine", f, rot=(1.5 * pk.wave(f, n, 0.1, 2), 0, 1.5 * pk.wave(f, n, 0.3)),
              loc=(0, 0, 0.03 + 0.03 * pk.wave(f, n, 0, 2)))
        k.key("Head", f, rot=(-2.5 * pk.wave(f, n, 0.2, 2), 0, 2 * pk.wave(f, n, 0.35)))
        fins(k, f, 10 * pk.wave(f, n, 0, 4))
        for j, i in enumerate(ARM_RING):
            ph = j / len(ARM_RING)
            w = lambda lag: math.sin(2 * math.pi * (2 * f / n - ph - lag))
            tent(k, f, i, a=-3 + 7 * w(0), b=2 + 7 * w(0.07), c=4 + 9 * w(0.14), d=4 + 10 * w(0.21),
                 twist=3 * math.sin(2 * math.pi * (f / n - ph)))
    ground_lift(k, n)
    k.finish()


def swim(k):
    """JET PROPULSION: the arms snap together under the body (thrust, the body surges up), then open like an umbrella
    while it glides; the mantle squeezes and the fins beat twice."""
    n = 30
    k.new_action("swim", n, True)
    for f in range(0, n + 1):
        u = f / n
        if u < 0.35:
            s = math.sin(math.pi * u / 0.35 * 0.5)                  # 0 -> 1 contraction
        else:
            s = 0.5 + 0.5 * math.cos(math.pi * (u - 0.35) / 0.65)   # 1 -> 0 spread
        k.key("Spine", f, rot=(10 - 3 * s, 0, 0), loc=(0, 0, 0.08 * math.sin(2 * math.pi * (u - 0.1))))
        k.key("Head", f, rot=(-4 + 6 * s, 0, 0))
        fins(k, f, 14 * math.sin(4 * math.pi * u))
        for i in range(1, 9):
            tent(k, f, i, a=-8 + 30 * s, b=-4 + 14 * s, c=2 + 8 * s, d=2 + 6 * s)
    ground_lift(k, n)
    k.finish()
    return 0.0


BACKF = {5: 0.6, 6: 0.6, 7: 0.45, 8: 0.45}       # back arms flare less (clear of the back-leaning mantle and fins)


def roar(k):
    """KRAKEN RISE: sinks, then rears up high with all eight arms flared UP like a spiked crown (deimatic display),
    tips writhing; holds; crashes back down."""
    n = 60
    k.new_action("roar", n, False)
    for f, z, sp, hd, fa, A, Bb, C, D in ((0, 0, 0, 0, 0, 0, 0, 0, 0), (10, -0.08, 5, 3, -10, 18, 10, 12, 8),
                                         (20, 0.24, -8, -12, 30, -46, -18, -12, -10),
                                         (42, 0.24, -8, -12, 30, -48, -20, -14, -12),
                                         (50, -0.05, 5, 3, 0, 20, 12, 14, 10), (60, 0, 0, 0, 0, 0, 0, 0, 0)):
        k.key("Spine", f, rot=(sp, 0, 0), loc=(0, 0, z))
        k.key("Head", f, rot=(hd, 0, 0))
        fins(k, f, fa)
        for i in range(1, 9):
            g = BACKF.get(i, 1.0) if A < 0 else 1.0
            tent(k, f, i, a=A * g, b=Bb * g, c=C * g, d=D * g)
    for f in range(22, 42, 3):                      # tips writhe in the crown
        for j, i in enumerate(ARM_RING):
            g = BACKF.get(i, 1.0)
            wr = 12 * math.sin(2 * math.pi * (f / 10 + j / 8))
            tent(k, f, i, a=-47 * g, b=-19 * g, c=(-13 + wr) * g, d=(-11 - wr) * g,
                 twist=5 * math.sin(2 * math.pi * (f / 15 + j / 3)))
    ground_lift(k, n)
    k.finish(loop=False)


# act_wrap: the 4 front arms coil round an imaginary mast in front (left arms clockwise, right arms anticlockwise,
# each pair at its own height), squeeze it x3 and drag it down; the back arms brace on the ground.
WRAP = {1: (-54, -1, 1.0), 2: (-26, 1, 1.0), 3: (-14, -1, 0.7), 4: (-2, 1, 0.7)}    # reach lift (a), coil direction (- = clockwise)


def wrap(k):
    """SIGNATURE - SHIP CRUSHER COIL: the 4 front arms rise and reach forward as if grabbing a mast, COIL round it,
    squeeze three times (the mantle pulses, the fins flare), drag the mast down with the mantle leaning in, then
    release with the arms unfurling outward and settle back to the hover."""
    n = 100
    k.new_action("act_wrap", n, False)
    # f, spine (z, pitch), head pitch, fins, reach (0..1), coil (0..1), squeeze (deg), drag (deg), unfurl (deg)
    P = [(0, 0.0, 0, 0, 0, 0.0, 0.0, 0, 0, 0), (14, 0.06, -4, -4, 16, 1.0, 0.0, 0, 0, 0),
         (30, 0.06, 2, 0, 10, 1.0, 1.0, 0, 0, 0), (36, -0.01, 6, 4, 26, 1.0, 1.0, 25, 0, 0),
         (42, 0.06, 2, 0, 8, 1.0, 1.0, 0, 0, 0), (48, -0.01, 6, 4, 26, 1.0, 1.0, 25, 0, 0),
         (54, 0.06, 2, 0, 8, 1.0, 1.0, 0, 0, 0), (60, -0.01, 6, 4, 28, 1.0, 1.0, 25, 0, 0),
         (76, -0.02, 15, 6, 10, 1.0, 0.8, 0, 30, 0), (84, 0.04, -4, -4, 24, 0.3, 0.0, 0, 0, -22),
         (90, 0.03, -2, -2, 8, 0.0, 0.0, 0, 0, -8), (100, 0.0, 0, 0, 0, 0.0, 0.0, 0, 0, 0)]
    for f, z, sp, hd, fa, reach, coil, sq, drag, unf in P:
        k.key("Spine", f, rot=(sp, 0, 0), loc=(0, 0, z))
        k.key("Head", f, rot=(hd, 0, 0))
        fins(k, f, fa)
        for i in range(1, 9):
            if i in WRAP:
                lift, sd, cs = WRAP[i]
                cy = (24 + sq * 0.6) * coil * cs
                tent(k, f, i, a=lift * reach + drag + unf, b=(8 + 22 * coil) * reach + unf * 0.6,
                     c=(10 + 26 * coil) * reach, d=(12 + 28 * coil + sq) * reach,
                     yb=sd * cy * 0.6, yc=sd * cy, yd=sd * (cy + 8 * coil))
            else:                                  # back arms brace on the ground, splayed
                br = 1.0 if 6 <= f <= 80 else 0.0
                tent(k, f, i, a=12 * br + unf * 0.5, b=4 * br, c=-6 * br, d=-4 * br)
    ground_lift(k, n)
    k.finish(loop=False)


def anim(k):
    idle(k)
    swim(k)
    roar(k)
    wrap(k)
    return 0.0


HEAD_XF = []
