# Shade Panther (Void egg #1) - FIERCE style (2026-10-09, FIERCE_PLAN "the ghost leopard"): a black (melanistic)
# leopard built from tapered blocks under a Roblox stud skin. Long low body (BL 1.45 SH), deep chest with a strong
# tuck, prominent shoulder blades each carrying a violet crystal cluster, a SMALL round head with a short muzzle,
# narrow violet slit eyes with vertical pupils under heavy brows, long upper fangs, small rounded ears, swept cheek
# fur, big clawed paws, ghost rosettes (broken rings of darker inlays), and a long thick tail that hangs low and
# curls up to a crystal tip. No glow (void wisps = VFX). Old chibi version: _tools/chibi_specs/ShadePanther.py
import math
from mathutils import Vector, Euler

DISPLAY = "Shade Panther"
MOTION = "Walk"
RIG = "quad"
HEIGHT = 7.0                  # withers 0.80 of 0.99 model units = ~5.7 studs at x1 (HEIGHT rule 2026-10-09)

FUR = (92, 80, 148)           # indigo-black fur (Roblox renders ~0.6x darker -> deep void indigo in game)
FUR_D = (50, 42, 86)          # back stripe, brows, ear backs, cheek fur
GHOST = (48, 40, 86)          # ghost rosettes (only a little darker than the fur, like the real thing)
PALE = (140, 126, 186)        # underside, muzzle, throat
VIOLET = (170, 80, 255)       # the ONE accent: eyes, crystal clusters
VIOLET_L = (206, 160, 255)
BLACK = (14, 14, 22)
TEETH = (238, 234, 220)
MOUTH = (86, 18, 30)

PITCH = 0.032                 # stud pitch = 0.042 x (U / U_raiju), U = model height / HEIGHT (0.99 / 7.0 vs 1.498 / 8)

# leg joints (left side): hip/shoulder, knee/elbow, ankle/wrist, paw centre   (SH = 0.80: withers top at 0.80)
LEGS = {"F": ((0.12, -0.34, 0.60), (0.12, -0.27, 0.345), (0.12, -0.33, 0.095), (0.12, -0.375, 0.040)),
        "B": ((0.115, 0.37, 0.62), (0.115, 0.25, 0.38), (0.115, 0.45, 0.17), (0.115, 0.39, 0.040))}
TAILP = [(0, 0.52, 0.745), (0, 0.77, 0.58), (0.02, 1.02, 0.50), (0.07, 1.23, 0.54), (0.14, 1.33, 0.68)]
HJ = Vector((0, -0.64, 0.75))   # head group scale pivot (the throat)
HEAD_S = 1.12


def hs(p):
    """rest-space point of the head group after its scale about the throat"""
    return HJ + (Vector(p) - HJ) * HEAD_S


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


def prof(b, lz):
    t = (lz / b.h.z + 1) / 2
    fx = b.bot[0] + (b.top[0] - b.bot[0]) * t
    fy = b.bot[1] + (b.top[1] - b.bot[1]) * t
    return b.h.x * fx, b.h.y * fy, b.ts[1] * t


def side_pt(b, s, ly, lz, off=0.006):
    """point on the +-x flank of tapered block b at local (ly, lz) + the flank normal"""
    hx, _, oy = prof(b, lz)
    p = b.world(Vector((s * (hx + off), ly + oy, lz)))
    dx = b.h.x * (b.top[0] - b.bot[0]) / (2 * b.h.z)
    return p, (b.R @ Vector((s, 0, -dx))).normalized()


def rosette(B, b, s, ly, lz, r=0.052, n=5, rot=0.0):
    """ghost rosette: a broken ring of n short dark bars on a flank (ring diameter ~2r + bar width)"""
    import blockkit as bk
    p, nrm = side_pt(b, s, ly, lz, off=0.004)
    up = Vector((0, 0, 1))
    u = (up - nrm * up.dot(nrm)).normalized()
    v = nrm.cross(u).normalized()
    for i in range(n):
        a = math.radians(rot + 360 * i / n)
        c = p + (u * math.cos(a) + v * math.sin(a)) * r
        t = (-u * math.sin(a) + v * math.cos(a))
        L = r * (0.86 if i % 2 else 0.72)
        B.bar(c - t * L / 2, c + t * L / 2, nrm, 0.034, 0.008, GHOST, b.bone, studs=[], bevel=0.003)


def crystals(B, base, d, L, w, bone, n=3, splay=26, seed=0.0):
    """violet crystal cluster: a main shard (45 deg twist) + n smaller splayed shards, light tips, dark socket"""
    import blockkit as bk
    d = Vector(d).normalized()
    base = Vector(base)
    side = d.orthogonal().normalized()
    B.add(base + d * 0.006, (w * 1.5, w * 1.5, w * 0.6), FUR_D, bone, R=bk.frame_from(base, base + d, side),
          role="limb")
    shards = [(d, L, w)]
    for i in range(n):
        ang = math.radians(splay)
        r = (d.cross(side).normalized() * math.cos(2 * math.pi * i / n + seed) +
             side * math.sin(2 * math.pi * i / n + seed))
        shards.append(((d * math.cos(ang) + r * math.sin(ang)).normalized(), L * (0.55 + 0.12 * (i % 2)), w * 0.72))
    for dd, ln, ww in shards:
        sd = (dd.orthogonal().normalized() + dd.cross(dd.orthogonal()).normalized()).normalized()
        R = bk.frame_from(base, base + dd, sd)
        B.add(base + dd * (0.75 * ln / 2), (ww, ww, 0.75 * ln / 2), VIOLET, bone, R=R, top=(0.85, 0.85), studs=[],
              role="limb")
        B.add(base + dd * (0.75 * ln + 0.25 * ln / 2 - 0.004), (ww * 0.85, ww * 0.85, 0.25 * ln / 2), VIOLET_L, bone,
              R=R, top=(0.10, 0.10), studs=[], role="limb")


def model(k):
    import blockkit as bk
    B = bk.Blocks(k, seed=131, tier=3, plates=False)
    # ---------------- torso: deep narrow ribcage, strong sloped tuck, narrow waist, hips (long and low)
    rib = B.add((0, -0.24, 0.59), (0.165, 0.30, 0.215), FUR, "Chest", bot=(0.62, 0.52), top=(0.88, 0.92), rnd=0.30)
    B.seg((0, -0.10, 0.395), (0, 0.24, 0.525), 0.10, 0.06, FUR, "Spine", top=(0.82, 0.75), side=(1, 0, 0))  # tuck
    waist = B.add((0, 0.10, 0.655), (0.125, 0.20, 0.12), FUR, "Spine", bot=(0.72, 0.70), top=(0.95, 1), rnd=0.30)
    hips = B.add((0, 0.37, 0.645), (0.145, 0.19, 0.145), FUR, "Spine", rot=(-8, 0, 0), top=(0.84, 0.90),
                 bot=(0.85, 0.9), rnd=0.30)
    # dark topline saddle lying ON the top surfaces: withers -> waist -> rump
    for a, b, bone in (((0, -0.36, 0.817), (0, -0.10, 0.804), "Chest"), ((0, -0.10, 0.804), (0, 0.10, 0.787), "Spine"),
                       ((0, 0.10, 0.787), (0, 0.40, 0.80), "Spine")):
        B.seg(a, b, 0.065, 0.014, FUR_D, bone, side=(1, 0, 0), ext=0.012, ext1=0.012, top=(0.95, 1), rnd=0.3)
    # pale underside following the tuck + pale chest front / throat
    B.add((0, -0.25, 0.383), (0.08, 0.13, 0.02), PALE, "Chest", bot=(0.8, 0.9), studs=[])
    B.seg((0, -0.10, 0.385), (0, 0.22, 0.508), 0.065, 0.018, PALE, "Spine", side=(1, 0, 0), top=(0.8, 1), ext=0.03)
    B.add((0, -0.53, 0.60), (0.10, 0.025, 0.12), PALE, "Chest", bot=(0.5, 1), top=(0.9, 1), rot=(-12, 0, 0))
    # prominent shoulder blades (stand above the back line) carrying the violet crystal clusters
    for s in (1, -1):
        sb = B.add((s * 0.095, -0.36, 0.79), (0.055, 0.11, 0.05), FUR, "Chest", rot=(-10, 0, s * 8), top=(0.6, 0.7),
                   rnd=0.35)
        crystals(B, (s * 0.12, -0.31, 0.81), (s * 0.55, 0.85, 0.40), 0.19, 0.042, "Chest", seed=0.6 * s)
    # ---------------- neck (carried low and forward) + small round head with a short muzzle
    B.seg((0, -0.40, 0.66), (0, -0.62, 0.76), 0.10, 0.115, FUR, "Neck", ext=0.05)
    B.seg((0, -0.46, 0.60), (0, -0.66, 0.70), 0.075, 0.06, PALE, "Neck", side=(1, 0, 0), ext=0.02)   # pale throat
    B.add((0, -0.72, 0.825), (0.10, 0.085, 0.085), FUR, "Head", top=(0.82, 0.85), bot=(0.9, 0.95), rnd=0.42)
    B.add((0, -0.70, 0.905), (0.07, 0.06, 0.012), FUR_D, "Head", top=(0.8, 0.8))                    # dark crown
    B.seg((0, -0.78, 0.800), (0, -0.865, 0.790), 0.070, 0.042, FUR, "Head", top=(0.85, 0.85), ext=0.02)   # muzzle
    for sx in (1, -1):                                                                     # whisker pads
        B.add((sx * 0.030, -0.850, 0.768), (0.034, 0.022, 0.016), FUR, "Head", rnd=0.2)
    B.add((0, -0.871, 0.812), (0.020, 0.010, 0.013), BLACK, "Head", bot=(0.45, 0.8), role="detail", bevel=0.004)
    for s in (1, -1):                                                        # long upper fangs + small teeth
        B.spike((s * 0.036, -0.858, 0.752), (0, -0.1, -1), 0.062, 0.012, TEETH, "Head")
        B.spike((s * 0.050, -0.830, 0.750), (0, 0, -1), 0.025, 0.009, TEETH, "Head")
    # lower jaw (snarls) + mouth + lower fangs
    B.seg((0, -0.70, 0.725), (0, -0.85, 0.722), 0.058, 0.02, PALE, "Jaw", top=(0.8, 1), ext=0.02)
    B.add((0, -0.79, 0.744), (0.04, 0.07, 0.005), MOUTH, "Jaw", studs=[], role="detail", bevel=0.003)
    for s in (1, -1):
        B.spike((s * 0.028, -0.84, 0.738), (0, 0, 1), 0.035, 0.009, TEETH, "Jaw")
    # narrow violet slit eyes with a vertical pupil, heavy dark brows
    for s in (1, -1):
        rot = (0, -s * 18, s * 22)
        B.add((s * 0.052, -0.800, 0.845), (0.036, 0.008, 0.017), BLACK, "Head", rot=rot, studs=[], role="detail",
              bevel=0.003)
        B.add((s * 0.053, -0.806, 0.845), (0.030, 0.006, 0.0095), VIOLET, "Head", rot=rot, studs=[],
              role="detail", bevel=0.002)
        B.add((s * 0.050, -0.8125, 0.845), (0.0060, 0.0035, 0.0110), BLACK, "Head", rot=(0, 0, s * 22), studs=[],
              role="detail", bevel=0.0012)                                                 # vertical cat pupil
        B.add((s * 0.067, -0.8115, 0.8465), (0.010, 0.003, 0.004), VIOLET_L, "Head", rot=rot, studs=[],
              role="detail", bevel=0.0012)
        B.add((s * 0.048, -0.785, 0.876), (0.048, 0.022, 0.017), FUR_D, "Head", rot=(0, -s * 20, s * 22),
              role="detail", bevel=0.007)                                                  # heavy brow
    # cheek fur: swept-back dark blades from the jaw line
    for s in (1, -1):
        for z, dz, L, w in ((0.77, -0.35, 0.09, 0.028), (0.82, 0.0, 0.10, 0.03)):
            B.spike((s * 0.085, -0.73, z), (s * 0.45, 0.88, dz), L, w, FUR_D, "Head", top=(0.12, 0.4))
    # small rounded ears, pale inside
    for s, side in ((1, "L"), (-1, "R")):
        R = Euler((math.radians(-14), math.radians(s * 6), math.radians(-s * 16)), "XYZ").to_matrix()
        root = Vector((s * 0.062, -0.69, 0.895))
        ear = B.add(root + R @ Vector((0, 0, 0.032)), (0.034, 0.014, 0.034), FUR_D, "Ear_" + side, R=R,
                    top=(0.55, 0.7), rnd=0.35)
        B.add(ear.world((0, -0.014, -0.004)), (0.020, 0.004, 0.022), FUR, "Ear_" + side, R=R, top=(0.5, 1),
              studs=[], role="detail", bevel=0.003)
    for blk in B.items:
        if blk.bone in ("Head", "Jaw", "Ear_L", "Ear_R") and hasattr(blk, "h"):
            blk.c = hs(blk.c)
            blk.h = blk.h * HEAD_S
    # ---------------- legs: muscled upper, slim lower, BIG paws with 4 black claws
    for s, side in ((1, "L"), (-1, "R")):
        for fb in ("F", "B"):
            H, K, A, Pw = (X(p, s) for p in LEGS[fb])
            leg, shin, foot = "Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side
            if fb == "F":
                B.seg(H + Vector((0, 0, 0.07)), K, 0.058, 0.085, FUR, leg, ext=0.0, ext1=0.03, top=(0.85, 0.72))
                B.seg(K, A, 0.048, 0.052, FUR, shin, top=(0.88, 0.88), ext=0.03, ext1=0.02)
            else:
                B.seg(H + Vector((0, 0.03, 0.07)), K, 0.072, 0.12, FUR, leg, bot=(0.85, 1), top=(0.75, 0.62),
                      ext=0.0, ext1=0.03)
                B.seg(K, A, 0.05, 0.058, FUR, shin, top=(0.80, 0.80), ext=0.03, ext1=0.02)
                B.seg(A, Pw + Vector((0, 0.03, 0.025)), 0.04, 0.042, FUR, foot, ext=0.03)
            B.add(Pw, (0.062, 0.075, 0.038), FUR_D, foot, top=(0.85, 0.80))
            for gx in (-0.036, -0.012, 0.012, 0.036):
                B.spike((Pw.x + gx, Pw.y - 0.066, 0.030), (0, -1, -0.55), 0.05, 0.011, BLACK, foot)
    # ---------------- ghost rosettes on the flanks, shoulders and thighs
    for s in (1, -1):
        for ly, lz, r, rt in ((-0.15, 0.05, 0.054, 10), (0.10, 0.01, 0.052, 46)):
            rosette(B, rib, s, ly, lz, r=r, rot=rt)
        rosette(B, waist, s, 0.0, 0.0, r=0.050, rot=28)
        for ly, lz, r, rt in ((-0.075, 0.035, 0.050, 15), (0.085, -0.025, 0.050, 52)):
            rosette(B, hips, s, ly, lz, r=r, rot=rt)
    # ---------------- long thick tail: hangs low, curls up at the tip, violet crystal tip
    P = [Vector(p) for p in TAILP]
    # (thick in depth = side view; slimmer across at the root so it clears the thighs)
    for i, ((a, b), (w, d)) in enumerate(zip(zip(P, P[1:]), ((0.044, 0.064), (0.048, 0.056), (0.048, 0.050),
                                                             (0.042, 0.042)))):
        B.seg(a, b, w, d, FUR if i < 2 else FUR_D, "Tail%d" % (i + 1), ext=0.035, top=(0.92, 0.92))
    crystals(B, P[4] - Vector((0, 0.0, 0.015)), (0, 0.75, 0.65), 0.19, 0.036, "Tail4", seed=0.4)
    B.build()
    bk.stud_skin(k, PITCH)
    return {"TH": round(B.th, 3)}


# ------------------------------------------------------------------ rig
def rig(k):
    k.joint("Spine", (0, 0.18, 0.64), "Root", tail=(0, -0.4, 0))
    k.joint("Chest", (0, -0.10, 0.64), "Spine", tail=(0, -0.4, 0))
    k.joint("Neck", (0, -0.42, 0.68), "Chest", tail=(0, -0.2, 0.08))
    k.joint("Head", (0, -0.64, 0.75), "Neck", tail=(0, -0.25, 0.0))           # throat pivot
    k.joint("Jaw", tuple(hs((0, -0.70, 0.735))), "Head", tail=(0, -0.17, 0))
    for s, side in ((1, "L"), (-1, "R")):
        k.joint("Ear_" + side, tuple(hs((s * 0.062, -0.69, 0.895))), "Head", tail=(s * 0.03, 0, 0.08))
        for fb, parent, knee in (("F", "Chest", (0, 1, 0)), ("B", "Spine", (0, -1, 0))):
            H, K, A, Pw = (X(p, s) for p in LEGS[fb])
            k.joint("Leg_" + fb + side, H, parent)
            k.joint("Shin_" + fb + side, K, "Leg_" + fb + side)
            k.joint("Foot_" + fb + side, A, "Shin_" + fb + side, tail=(0, -0.12, 0))
            k.add_leg2("Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side, knee=knee)
    for i in range(4):
        k.joint("Tail%d" % (i + 1), TAILP[i], "Spine" if i == 0 else "Tail%d" % i,
                tail=tuple(Vector(TAILP[i + 1]) - Vector(TAILP[i])))


# ------------------------------------------------------------------ animation (FIERCE_PLAN 2026-10-09)
import petkit as pk
import _common as cm

LEGS4 = ["Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR"]
TAIL = ["Tail1", "Tail2", "Tail3", "Tail4"]


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


def tail(k, f, n, sway=8.0, lift=0.0, cycles=2, twitch=0.0, curl=0.0):
    """long cat tail: slow sway down the chain, optional tip twitch (fast) and curl (last two bones lift)"""
    for i, b in enumerate(TAIL):
        ph = -0.12 * i
        p = lift + (curl if i >= 2 else 0.0)
        y = sway * (1 + 0.5 * i) * pk.wave(f, n, ph, cycles)
        if i == 3 and twitch:
            y += twitch * math.sin(2 * math.pi * f / 5)
        k.key(b, f, rot=(p, y, 0))


def feet(k, f, T):
    """solve all four legs at frame f; T = {leg: (dx, dy, lift)} offsets from the rest ground spot"""
    import bpy
    bpy.context.scene.frame_set(f)
    for leg in LEGS4:
        dx, dy, lift = T.get(leg, (0.0, 0.0, 0.0))
        k.solve_leg(leg, f, Vector((k.J[leg].x + dx, k.J[leg].y + dy, lift)))


def step(f, f0, f1, d0, d1, h=0.05):
    """foot offset (dy, lift) for a step from d0 to d1 between f0 and f1"""
    if f <= f0:
        return d0, 0.0
    if f >= f1:
        return d1, 0.0
    u = (f - f0) / (f1 - f0)
    return d0 + (d1 - d0) * (0.5 - 0.5 * math.cos(math.pi * u)), h * math.sin(math.pi * u)


def idle(k):
    """BIG-CAT STRETCH: the play-bow - both front paws slide far forward, the chest sinks to the ground and the
    rump stays high, a long hold with the claws spread, back up; then it watches something off to the left, ears
    forward, the tail tip twitching."""
    n = 120
    k.new_action("idle", n, True)
    BOW = [(0, 0.0), (10, 0.0), (28, 1.0), (44, 1.0), (60, 0.0), (120, 0.0)]
    LOOK = [(0, 0.0), (64, 0.0), (72, 1.0), (104, 1.0), (112, 0.0), (120, 0.0)]
    for f in range(0, n + 1, 2):
        w, lk = tab(BOW, f), tab(LOOK, f)
        b = pk.wave(f, n, 0, 4) * (1 - w)
        k.key("Spine", f, rot=(15 * w, 0, 0), loc=(0, 0.02 * w, 0.004 * b - 0.07 * w))
        k.key("Chest", f, rot=(8 * w - 0.6 * b, 0, 0))
        k.key("Neck", f, rot=(-14 * w - 2 * lk, 10 * lk, 0))
        k.key("Head", f, rot=(-8 * w - 2 * lk, 16 * lk, 4 * lk))
        k.key("Jaw", f, rot=(2 + 4 * w, 0, 0))
        ears(k, f, -20 * w + 12 * lk + (8 * math.sin(2 * math.pi * f / 16) if 72 <= f <= 104 else 0.0),
             -20 * w + 12 * lk)
        tail(k, f, n, sway=6 * (1 - lk), lift=-4 + 8 * w, cycles=2, twitch=14 * lk, curl=6 * lk)
    k.bake_bezier_now()
    for f in range(0, n + 1):
        w = tab(BOW, f)
        reach = -0.22 * w
        feet(k, f, {"Leg_FL": (0.0, reach, 0.0), "Leg_FR": (0.0, reach, 0.0)})
    k.finish()
    k.meta["planted"] = ["Leg_BL", "Leg_BR"]


def walk(k):
    n = 28

    def body(f):
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(0.6 * pk.wave(f, n, 0.1, 2), 2.0 * pk.wave(f, n), 1.5 * pk.wave(f, n)),
              loc=(0, 0, -0.012 * b))
        k.key("Chest", f, rot=(0, -3 * pk.wave(f, n, 0.25), -1.5 * pk.wave(f, n, 0.25)))
        k.key("Neck", f, rot=(4 + 1.5 * pk.wave(f, n, 0.1, 2), 0, 0))
        k.key("Head", f, rot=(-3 - 1.5 * pk.wave(f, n, 0.2, 2), -2 * pk.wave(f, n, 0.25), 0))
        k.key("Jaw", f, rot=(2, 0, 0))
        ears(k, f, 4)
        tail(k, f, n, sway=7, lift=-2, cycles=1, curl=6)
    return cm.quad_walk(k, n, 0.14, 0.07, body, gait="walk")


def roar(k):
    """SNARL & SWIPE: crouches, ears flat, lips curl back (jaw 25), the right forepaw rears up and SWIPES the air
    across its face claws-out, a held snarl, then it plants the paw and settles."""
    import bpy
    n = 60
    k.new_action("roar", n, False)
    CR = [(0, 0.0), (8, 1.0), (36, 1.0), (48, 0.0), (60, 0.0)]
    UP = [(0, 0.0), (14, 0.0), (20, 1.0), (40, 1.0), (50, 0.0), (60, 0.0)]
    JW = [(0, 2), (6, 2), (12, 26), (44, 26), (54, 2), (60, 2)]
    for f in range(0, n + 1):
        c, u = tab(CR, f), tab(UP, f)
        tr = 2.5 * math.sin(2 * math.pi * f / 4) if 14 <= f <= 44 else 0.0
        k.key("Spine", f, rot=(-3 * u, 0, 3 * u), loc=(0, 0.03 * c, -0.045 * c))
        k.key("Chest", f, rot=(-4 * u, 0, 0))
        k.key("Neck", f, rot=(-8 * c - 6 * u, 0, 0))
        k.key("Head", f, rot=(-6 * c, 4 * u, -4 * u))
        k.key("Jaw", f, rot=(tab(JW, f) + tr, 0, 0))
        ears(k, f, -48 * c)
        tail(k, f, n, sway=10 * c, lift=-6, cycles=4, twitch=10 * c)
    k.bake_bezier_now()
    sc = bpy.context.scene
    # right forepaw: (leg pitch, leg yaw, leg roll, shin pitch, foot pitch) - pitch - raises it forward
    SW = [(14, (0, 0, 0, 0, 0)), (20, (-62, -18, -10, -40, -30)), (25, (-62, -18, -10, -40, -30)),
          (29, (-70, 26, 0, -30, -40)), (33, (-62, 30, 0, -40, -30)), (40, (-46, 10, 0, -44, -20)),
          (46, (-16, 0, 0, -10, -6)), (50, (0, 0, 0, 0, 0))]
    for f in range(0, n + 1):
        sc.frame_set(f)
        for leg in LEGS4:
            if leg == "Leg_FR" and 16 <= f <= 49:
                lp, ly, lr, sp, fp = tab(SW, f)
                k.key("Leg_FR", f, rot=(lp, ly, lr), loc=(0, 0, 0))
                k.key("Shin_FR", f, rot=(sp, 0, 0))
                k.key("Foot_FR", f, rot=(fp, 0, 0))
            else:
                k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, 0.0)))
    k.finish(loop=False)


def pounce(k):
    """SIGNATURE - STALK & POUNCE: sinks into a low stalk, the front paws creeping forward in slow motion; the
    hind-end wiggle; LEAPS forward 0.5 SH through the air with the front paws reaching; lands, pins the prey and
    bites; springs back to its spot."""
    import bpy
    n = 100
    k.new_action("act_pounce", n, False)
    # body: (y travel, z, pitch, yaw, roll)
    BODY = [(0, (0.0, 0.0, 0, 0, 0)), (12, (-0.02, -0.11, 2, 0, 0)), (30, (-0.06, -0.12, 2, 0, 0)),
            (44, (-0.06, -0.13, 4, 0, 0)), (47, (-0.10, -0.04, -12, 0, 0)), (51, (-0.24, 0.12, -6, 0, 0)),
            (55, (-0.38, 0.06, 6, 0, 0)), (58, (-0.42, -0.06, 6, 0, 0)), (70, (-0.42, -0.06, 4, 0, 0)),
            (76, (-0.30, 0.05, -4, 0, 0)), (82, (-0.06, 0.04, -2, 0, 0)), (86, (0.0, -0.02, 0, 0, 0)),
            (92, (0.0, 0.0, 0, 0, 0)), (100, (0.0, 0.0, 0, 0, 0))]

    def body(f):
        y, z, p, yw, r = tab(BODY, f)
        if 30 <= f <= 44:                                  # hind-end wiggle
            w = math.sin(2 * math.pi * (f - 30) / 5)
            yw += 5 * w
            r += 3 * w
        return y, z, p, yw, r

    NK = [(0, 0), (12, 10), (44, 10), (48, -10), (56, 0), (60, 18), (68, 18), (76, 0), (100, 0)]
    HD = [(0, 0), (12, -8), (44, -8), (48, -6), (56, 4), (60, 16), (68, 16), (76, 0), (100, 0)]
    JW = [(0, 2), (40, 2), (48, 18), (56, 24), (60, 30), (63, 4), (66, 10), (69, 4), (76, 2), (100, 2)]
    EAR = [(0, 0), (12, 10), (44, 10), (48, -30), (60, -30), (70, -10), (84, 0), (100, 0)]
    TL = [(0, 0.0), (12, -6.0), (44, -6.0), (48, 10.0), (58, 4.0), (70, 0.0), (100, 0.0)]
    for f in range(0, n + 1):
        y, z, p, yw, r = body(f)
        k.key("Spine", f, rot=(p, yw, r), loc=(0, y, z))
        k.key("Chest", f, rot=(0, 0, 0))
        k.key("Neck", f, rot=(tab(NK, f), 0, 0))
        k.key("Head", f, rot=(tab(HD, f), 0, 0))
        k.key("Jaw", f, rot=(tab(JW, f), 0, 0))
        ears(k, f, tab(EAR, f))
        tail(k, f, n, sway=4 if f < 30 else 0, lift=tab(TL, f), cycles=3,
             twitch=16 if 26 <= f <= 44 else 0.0)
    k.bake_bezier_now()
    sc = bpy.context.scene
    AIR = (47, 57)

    def foot_targets(f):
        y = body(f)[0]
        T = {}
        for leg in LEGS4:
            fr = "_F" in leg
            left = leg.endswith("L")
            if f < AIR[0]:                                 # stalk: the front paws creep forward one at a time
                if fr:
                    f0 = 6 if left else 17
                    d, h = step(f, f0, f0 + 9, 0.0, -0.08, 0.04)
                else:
                    d, h = step(f, 22 if left else 26, (22 if left else 26) + 6, 0.0, -0.05, 0.03)
                    if 32 <= f <= 44:                      # hind feet tread during the wiggle
                        h = 0.012 * max(0.0, math.sin(2 * math.pi * (f - 32) / 5 + (0 if left else math.pi)))
                T[leg] = (0.0, d, h)
            elif f >= 58 and f <= 70:                      # landed: paws pin the prey
                T[leg] = (0.0, -0.42 + (-0.05 if fr else 0.0), 0.0)
            elif f > 70:                                   # hop back home
                d, h = step(f, 72, 84, -0.42 + (-0.05 if fr else 0.0), 0.0, 0.10)
                T[leg] = (0.0, d, h)
        return T

    # legs in the air: front reach forward, hind trail back
    LEAP = [(47, (0, 0, 0, 0)), (51, (-48, -20, 40, 20)), (54, (-40, -10, 30, 10)), (57, (-20, -6, 10, 4))]
    for f in range(0, n + 1):
        sc.frame_set(f)
        if AIR[0] <= f <= AIR[1]:
            fl, fs, bl, bs = tab(LEAP, f)
            for leg in LEGS4:
                fr = "_F" in leg
                k.key(leg, f, rot=(fl if fr else bl, 0, 0), loc=(0, 0, 0))
                k.key(leg.replace("Leg_", "Shin_"), f, rot=(fs if fr else bs, 0, 0))
                k.key(leg.replace("Leg_", "Foot_"), f, rot=(-20 if fr else 30, 0, 0))
        else:
            feet(k, f, foot_targets(f))
    # never through the floor during the take-off / flight / landing
    fix = {}
    for f in range(44, 62):
        fix[f] = max(0.0, 0.004 - lowest(k, f))
    for f, dz in fix.items():
        if dz > 0:
            y, z, p, yw, r = body(f)
            k.key("Spine", f, rot=(p, yw, r), loc=(0, y, z + dz))
    k.bake_bezier_now()
    for f in range(0, n + 1):
        if not (AIR[0] <= f <= AIR[1]):
            feet(k, f, foot_targets(f))
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    pounce(k)
    return stride


def check_pairs():
    P = [("Leg_FL", "Leg_BL"), ("Leg_FR", "Leg_BR"), ("Leg_FL", "Leg_FR"), ("Leg_BL", "Leg_BR"),
         ("Shin_FL", "Shin_FR"), ("Shin_BL", "Shin_BR"), ("Shin_FL", "Shin_BL"), ("Shin_FR", "Shin_BR"),
         ("Foot_FL", "Foot_BL"), ("Foot_FR", "Foot_BR"), ("Foot_FL", "Foot_FR"), ("Foot_BL", "Foot_BR")]
    for a in ("Head", "Jaw"):
        for b in ("Leg_FL", "Leg_FR", "Shin_FL", "Shin_FR", "Foot_FL", "Foot_FR"):
            P.append((a, b))
    P += [("Head", "Chest"), ("Jaw", "Chest"), ("Ear_L", "Ear_R")]
    for b in ("Leg_BL", "Leg_BR", "Shin_BL", "Shin_BR", "Foot_BL", "Foot_BR"):
        for t in ("Tail1", "Tail2"):
            P.append((t, b))
    return P


def joints():
    return [((0, -0.62, 0.72), (0, -0.68, 0.78), 0.12, "Head")]
