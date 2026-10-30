# Kraken (Tide egg #3): a crisp block sea monster, rebuilt to STYLE_BIBLE.md (2026-10-08 pro pass): ONE tall rounded
# crimson mantle leaning back a little (= the head), hovering over a light underside skirt, bold amber eyes with
# horizontal bar pupils under a 15 deg dark brow ridge, a small dark hooked beak, dark 2x2 spots, two side fins with dark
# rims (a barnacle cluster on the left one) and EIGHT thick tapered tentacles (4 segments, the last two curling up) with
# a light underside strip and sucker rows. Floats (Motion = Swim): clips idle / swim / roar / act.
# Own moves: idle = hovers and scans, a travelling wave rolls around the tentacle ring, fins ripple; swim = jet
# propulsion (tentacles snap together under the body, then spread like an umbrella); roar = KRAKEN RISE (rears up with
# all eight tentacles flared up like a spiked crown, tips writhing); signature = SHIP CRUSHER (the front pair rises
# high and SLAMS down, then the next pairs drum down left and right).
import math
from mathutils import Vector, Quaternion

DISPLAY = "Kraken"
MOTION = "Swim"
RIG = "kraken"
HEIGHT = 8.0

BODY = (220, 64, 92)
UNDER = (255, 200, 176)
SUCK = (255, 222, 204)
SPOT = (128, 26, 56)
BARN = (226, 222, 206)
IRIS = (255, 196, 48)
BEAK = (70, 22, 42)
N_T = 8
MW = 1.0                         # mantle width


def t_angle(i):
    return math.radians(22.5 + 45 * i)


def t_dirs(i):
    a = t_angle(i)
    d = Vector((math.sin(a), -math.cos(a), 0))       # radial (0 deg = front, -Y)
    t = Vector((math.cos(a), math.sin(a), 0))        # tangent: +rotation about it swings the tentacle DOWN
    return d, t


# tentacle centre line: (radius, z) per point; joints at P0 (a), P1 (b), P2 (c); segments 3 + 4 (+ tip) ride on c
Z0 = 0.08                        # the whole kraken hovers 0.08 higher (tentacles stay off the floor in every clip)
RZ = [(0.31, 0.47 + Z0), (0.62, 0.25 + Z0), (0.88, 0.11 + Z0), (1.15, 0.14 + Z0), (1.32, 0.31 + Z0),
      (1.34, 0.43 + Z0)]
HWS = [0.115, 0.098, 0.082, 0.066, 0.050, 0.036]   # half widths at each point (base 0.23 MW -> tip 0.35x)


def t_path(i):
    d, _ = t_dirs(i)
    return [d * r + Vector((0, 0, z)) for r, z in RZ]


def face_pt(blk, key, s, t):
    """point + outward normal + 'up the face' vector on a (tapered / shifted / rotated) block face, s, t in 0..1"""
    P = blk.face_corners(key)
    n = (P[1] - P[0]).cross(P[3] - P[0]).normalized()
    if (sum(P, Vector()) / 4 - blk.c).dot(n) < 0:
        n = -n
    p = (P[0].lerp(P[1], s)).lerp(P[3].lerp(P[2], s), t)
    v = (P[3].lerp(P[2], s) - P[0].lerp(P[1], s)).normalized()
    return p, n, v


def spot_cluster(B, blk, key, s, t, ds, dt, color):
    """dark spot cluster: one 2x2 square + two 1x1 squares touching its corners (diagonal), flush on the face"""
    for (si, ti, h) in ((s, t, 0.10), (s + ds, t + dt, 0.05), (s - ds, t - dt, 0.05)):
        p, n, v = face_pt(blk, key, si, ti)
        B.bar(p - v * h, p + v * h, n, 2 * h, 0.016, color, blk.bone, studs=[], bevel=0.012)


def model(k):
    """STYLE_BIBLE Kraken: a back-leaning rounded bulb mantle (W 1.08 / H 1.1, widest high up) hovering 0.41 up over a
    light lip band that carries the beak, eyes at 43 % of its height, swept-back blade fins, tentacles 0.23 MW at the
    base tapering to 0.35x, ~1.25 mantle H long, last 2 segments curled up."""
    import blockkit as bk
    B = bk.Blocks(k, seed=97, tier=2, th=0.95)          # floater: cell 0.18 mantle W
    D = 0.62
    # ---- mantle (= head): a back-leaning octopus bulb = body (narrow base, widest at ~75 % of the height) + a dome
    #      crown whose base matches the body top (buried 0.15, so the side line runs on without a step)
    man = B.add((0, 0.02, 0.73 + Z0), (0.54, 0.46, 0.40), BODY, "Head", bot=(0.82, 0.82), top=(1.0, 1.0),
                top_shift=(0, 0.10), rot=(-5, 0, 0), density=D, role="mass", rnd=0.30, studs=["+x", "-x", "+y"],
                prelief=1.4)
    top_c = man.world(Vector((0, 0.10, 0.40)))
    dome = B.add(top_c + man.R @ Vector((0, 0.04, 0.10)), (0.54, 0.46, 0.25), BODY, "Head", R=man.R,
                 top=(0.50, 0.50), top_shift=(0, 0.04), studs=["+z", "+y"], density=D, role="mass", rnd=0.45)
    # light lip band wrapping the lower front and sides (the muzzle zone) + the hidden underside skirt
    B.add((0, -0.06, 0.47 + Z0), (0.47, 0.38, 0.12), UNDER, "Head", studs=[], role="mass", rnd=0.48)
    B.add((0, 0.02, 0.37 + Z0), (0.40, 0.38, 0.075), UNDER, "Spine", studs=[], role="limb")
    # dark spot clusters on the top-back and both upper flanks
    spot_cluster(B, dome, "+y", 0.42, 0.55, 0.15, 0.25, SPOT)
    spot_cluster(B, man, "+x", 0.26, 0.66, 0.15, 0.18, SPOT)
    spot_cluster(B, man, "-x", 0.74, 0.66, -0.15, 0.18, SPOT)
    # ---- face on the leaning front: a proxy block lying in the front plane carries the eyes (tilted correctly)
    P = man.face_corners("-y")
    pb, pt = (P[0] + P[1]) / 2, (P[2] + P[3]) / 2
    zd = (pt - pb).normalized()
    xd = Vector((1, 0, 0))
    yd = zd.cross(xd).normalized()
    R = bk.Matrix((xd, yd, zd)).transposed()
    proxy = bk.Block((pb + pt) / 2 + yd * 0.30, (0.46, 0.30, (pt - pb).length / 2), BODY, "Head", R=R)
    B.face_eyes(proxy, "bold", IRIS, base=BODY, brow=SPOT, z=0.55, x=0.22, scale=1.0, look=(0, 0.6),
                pupil_size=(0.12, 0.09),
                hl_on_pupil=True, hl_size=(0.05, 0.0), brow_spec=(0.29, 0.065, 15))
    # small dark hooked beak on the lip band, 2 cream teeth
    yl = -0.06 - 0.38
    B.add((0, yl - 0.01, 0.50 + Z0), (0.12, 0.05, 0.05), BEAK, "Head", bot=(0.55, 0.8), studs=[], role="limb")
    B.spike((0, yl - 0.04, 0.47 + Z0), (0, -0.35, -1), 0.08, 0.05, BEAK, "Head", top=(0.12, 0.3))
    for s in (1, -1):
        B.spike((s * 0.075, yl - 0.02, 0.465 + Z0), (0, -0.1, -1), 0.055, 0.016, BARN, "Head")
    # ---- fins: flat blades in the side-view plane, sweeping back to a point; dark rim on the trailing edge only;
    #      a barnacle cluster on the left fin
    for s, side in ((1, "L"), (-1, "R")):
        r0, r1 = Vector((s * 0.46, 0.12, 0.94 + Z0)), Vector((s * 0.60, 0.68, 1.14 + Z0))
        B.seg(r0, r1, 0.18, 0.05, BODY, "Fin_" + side, side=(0, 0, 1), ext=0.05, top=(0.25, 1.0), studs=[],
              role="limb")
        d = (r1 - r0).normalized()
        u = (Vector((0, 0, 1)) - d * d.z).normalized()
        B.seg(r0 - u * 0.165, r1 - u * 0.035, 0.028, 0.056, SPOT, "Fin_" + side, side=u, ext=0.0, ext1=0.03,
              top=(0.6, 1.0), studs=[], role="limb")
        if s > 0:
            out = d.cross(u).normalized()
            out = out if out.x > 0 else -out
            for q, dv, h in ((0.30, 0.05, 0.05), (0.46, -0.04, 0.042), (0.24, -0.08, 0.036), (0.58, 0.04, 0.032)):
                c = r0.lerp(r1, q) + u * dv + out * 0.045
                B.spike(c, out, h * 1.3, h, BARN, "Fin_" + side, top=(0.55, 0.55))
    # ---- eight tentacles: tapered segments, light underside strip, sucker rows, curled tips
    for i in range(N_T):
        d, t = t_dirs(i)
        P = t_path(i)
        bones = ["T%da" % (i + 1), "T%db" % (i + 1)] + ["T%dc" % (i + 1)] * 4
        for j in range(len(P) - 1):
            bone = bones[j]
            hw0, hw1 = HWS[j], HWS[j + 1]
            dirv = (P[j + 1] - P[j]).normalized()
            up = dirv.cross(t).normalized()
            last = j == len(P) - 2
            B.seg(P[j], P[j + 1], hw0, hw0 * 0.86, BODY, bone, side=t, ext=0.10 if j == 0 else 0.03,
                  top=((0.15 if last else hw1 / hw0), (0.25 if last else hw1 / hw0)), studs=[], role="limb")
            if j < 4:                                  # light underside strip + suckers
                B.seg(P[j] - up * hw0 * 0.60, P[j + 1] - up * hw1 * 0.60, hw0 * 1.04, hw0 * 0.34, UNDER, bone,
                      side=t, ext=0.02, top=(hw1 / hw0, hw1 / hw0), studs=[], role="limb")
                L = (P[j + 1] - P[j]).length
                ns = 3 if L > 0.24 else 2
                for q in range(ns):
                    u = (q + 0.5) / ns
                    w = hw0 + (hw1 - hw0) * u
                    c = P[j].lerp(P[j + 1], u) - up * (w * 0.60 + w * 0.34 + 0.008)
                    B.add(c, (w * 0.40, w * 0.40, 0.014), SUCK, bone, R=bk.frame_from(c, c - up, dirv), studs=[],
                          rnd=0.4, role="detail")
    B.build()
    return {"plates": B.stud_count, "TH": round(B.th, 3), "cell": round(B.pcell, 3)}


def rig(k):
    k.joint("Spine", (0, 0.02, 0.50 + Z0), "Root", tail=(0, 0, 0.4))
    k.joint("Head", (0, 0.02, 0.46 + Z0), "Spine", tail=(0, 0.05, 0.5))          # mantle pivot at its base
    for s, side in ((1, "L"), (-1, "R")):
        k.joint("Fin_" + side, (s * 0.44, 0.12, 0.94 + Z0), "Head", tail=(s * 0.1, 0.4, 0.15))
    for i in range(N_T):
        P = t_path(i)
        k.joint("T%da" % (i + 1), tuple(P[0]), "Spine", tail=P[1] - P[0])
        k.joint("T%db" % (i + 1), tuple(P[1]), "T%da" % (i + 1), tail=P[2] - P[1])
        k.joint("T%dc" % (i + 1), tuple(P[2]), "T%db" % (i + 1), tail=P[3] - P[2])


# ------------------------------------------------------------------ animation
import petkit as pk
import _common as cm


def ground_lift(k, n, target=0.03):
    """FLOOR RULE: after a clip is keyed, measure the lowest tentacle vertex per frame and raise the whole body
    (Spine z, keyed every frame) just enough that nothing ever goes below `target` - the tentacles push the body up
    instead of sinking into the floor."""
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


def tent(k, f, i, a=0.0, b=0.0, c=0.0, twist=0.0):
    """a/b/c + = that segment swings DOWN / curls under, - = lifts up / curls back. twist sways sideways."""
    _, t = t_dirs(i)
    side = Quaternion(Vector((0, 0, 1)), math.radians(twist))
    cm.key_axis(k, "T%da" % (i + 1), f, t, a, extra=side)
    cm.key_axis(k, "T%db" % (i + 1), f, t, b)
    cm.key_axis(k, "T%dc" % (i + 1), f, t, c)


def fins(k, f, a):
    k.key("Fin_L", f, rot=(0, 0, -a))
    k.key("Fin_R", f, rot=(0, 0, a))


def idle(k):
    """hovers: slow bob, turns to scan left and right, the mantle sways after the body, fins ripple, and a travelling
    wave rolls around the tentacle ring (each tentacle lifts and curls in turn)."""
    n = 96
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 2):
        k.key("Spine", f, rot=(1.5 * pk.wave(f, n, 0.1, 2), 9 * pk.wave(f, n, 0.0), 2 * pk.wave(f, n, 0.3)),
              loc=(0, 0, 0.03 + 0.03 * pk.wave(f, n, 0, 2)))
        k.key("Head", f, rot=(-3 * pk.wave(f, n, 0.2, 2), -3 * pk.wave(f, n, 0.1), 2 * pk.wave(f, n, 0.35)))
        fins(k, f, 10 * pk.wave(f, n, 0, 4))
        for i in range(N_T):
            ph = i / N_T
            w = math.sin(2 * math.pi * (2 * f / n - ph))
            tent(k, f, i, a=-4 + 7 * w, b=2 + 7 * math.sin(2 * math.pi * (2 * f / n - ph - 0.08)),
                 c=6 + 12 * math.sin(2 * math.pi * (2 * f / n - ph - 0.16)),
                 twist=5 * math.sin(2 * math.pi * (f / n - ph)))
    ground_lift(k, n)
    k.finish()


def swim(k):
    """jet propulsion: tentacles snap together under the body (thrust, body surges up/forward), then spread out like an
    umbrella while gliding; mantle squeezes, fins beat twice."""
    n = 30
    k.new_action("swim", n, True)
    for f in range(0, n + 1):
        u = f / n
        if u < 0.35:
            s = math.sin(math.pi * u / 0.35 * 0.5)                  # 0 -> 1 contraction
        else:
            s = 0.5 + 0.5 * math.cos(math.pi * (u - 0.35) / 0.65)   # 1 -> 0 spread
        k.key("Spine", f, rot=(12 - 3 * s, 0, 0), loc=(0, 0, 0.08 * math.sin(2 * math.pi * (u - 0.1))))
        k.key("Head", f, rot=(-4 + 6 * s, 0, 0))
        fins(k, f, 14 * math.sin(4 * math.pi * u))
        for i in range(N_T):
            tent(k, f, i, a=-8 + 34 * s, b=-4 + 18 * s, c=4 + 10 * s, twist=0)
    ground_lift(k, n)
    k.finish()
    return 0.0


BACK = {3: 0.55, 4: 0.55, 2: 0.85, 5: 0.85}     # back tentacles flare less (clear of the leaning mantle)


def roar(k):
    """KRAKEN RISE: sinks, then rears up high with the mantle thrown back and all eight tentacles flared UP like a
    spiked crown, tips writhing; holds, then crashes them back down."""
    n = 72
    k.new_action("roar", n, False)
    for f, z, sp, hd, fa, A, Bb, C in ((0, 0, 0, 0, 0, 0, 6, 10), (12, -0.10, 6, 4, -10, 20, 14, 20),
                                       (22, 0.26, -10, -16, 30, -50, -22, -14), (48, 0.26, -10, -16, 30, -52, -24, -16),
                                       (58, -0.06, 6, 4, 0, 24, 16, 18), (72, 0, 0, 0, 0, 0, 6, 10)):
        k.key("Spine", f, rot=(sp, 0, 0), loc=(0, 0, z))
        k.key("Head", f, rot=(hd, 0, 0))
        fins(k, f, fa)
        for i in range(N_T):
            g = BACK.get(i, 1.0) if A < 0 else 1.0
            tent(k, f, i, a=A * g, b=Bb * g, c=C * g)
    for f in range(24, 48, 3):
        for i in range(N_T):
            g = BACK.get(i, 1.0)
            wr = 10 * math.sin(2 * math.pi * (f / 12 + i / N_T))
            tent(k, f, i, a=-51 * g, b=-23 * g, c=(-15 + wr) * g, twist=6 * math.sin(2 * math.pi * (f / 18 + i / 3)))
    ground_lift(k, n)
    k.finish(loop=False)


def crush(k):
    """SIGNATURE - SHIP CRUSHER: leans back raising the front pair of tentacles high (tips curled), holds, SLAMS them
    down in front (body lunges forward), then the next pair on the left and on the right rise and drum down in turn."""
    n = 112
    k.new_action("act_crush", n, False)
    REST = dict(a=0, b=6, c=10)
    UP = dict(a=-55, b=-32, c=-4)
    SLAM = dict(a=34, b=12, c=-8)
    plan = {0: (0, 7), 1: (1, 6), 2: (2, 5)}          # slam groups: front pair, front-side pair, side pair
    timing = {0: (0, 22, 34, 40, 46), 1: (40, 52, 58, 62, 68), 2: (56, 68, 74, 78, 84)}   # rest, up, hold, slam, recoil
    keys = {i: {0: REST, n: REST} for i in range(N_T)}
    for g, (i0, i1) in plan.items():
        t0, t1, t2, t3, t4 = timing[g]
        for i in (i0, i1):
            keys[i].update({t0: REST, t1: UP, t2: UP, t3: SLAM, t4: dict(a=22, b=10, c=4), 96: REST})
    for i in range(N_T):
        for f, v in sorted(keys[i].items()):
            tent(k, f, i, **v)
    for f, z, sp, hd, fa in ((0, 0, 0, 0, 0), (22, 0.18, -12, -8, 20), (34, 0.20, -12, -8, 20), (40, -0.08, 14, 6, -10),
                             (46, -0.02, 6, 2, 0), (52, 0.10, -6, -4, 14), (62, -0.06, 10, 4, -8), (68, 0.08, -4, -2, 10),
                             (78, -0.06, 10, 4, -8), (88, 0, 2, 0, 0), (96, 0, 0, 0, 0), (n, 0, 0, 0, 0)):
        k.key("Spine", f, rot=(sp, 4 if 52 <= f <= 62 else (-4 if 68 <= f <= 78 else 0), 0), loc=(0, 0, z))
        k.key("Head", f, rot=(hd, 0, 0))
        fins(k, f, fa)
    ground_lift(k, n)
    k.finish(loop=False)


def anim(k):
    idle(k)
    swim(k)
    roar(k)
    crush(k)
    return 0.0


def check_pairs():
    P = []
    for i in range(N_T):
        j = (i + 1) % N_T
        for x in "bc":
            for y in "bc":
                P.append(("T%d%s" % (i + 1, x), "T%d%s" % (j + 1, y)))
        for x in "bc":
            P.append(("T%d%s" % (i + 1, x), "Head"))
            P.append(("T%d%s" % (i + 1, x), "Spine"))
    return P


def joints():
    out = []
    for i in range(N_T):
        P = t_path(i)
        for j, bn in ((1, "b"), (2, "c")):
            out.append((P[j], P[j], 0.12 if j == 1 else 0.10, "T%d%s" % (i + 1, bn)))
    return out
