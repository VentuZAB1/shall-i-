# Cerberus (Magma egg #3) - FIERCE style (2026-10-09, FIERCE_PLAN "the hellgate hound"): a three-headed mastiff-wolf
# built from tapered blocks under a Roblox stud skin. Deep broad chest (tapering underneath, sloped tuck, narrow waist),
# a shoulder yoke carrying 3 thick necks fanned +-28 deg, each with a spiked collar and a fierce broad-muzzled head
# (narrow hellfire-red eyes under heavy brows with rust brow dots, bared fangs, red mouths). Personality is in the
# ears: LEFT pinned back (the hothead), CENTRE upright and 10 % bigger (the alpha), RIGHT one torn ear + a scar (the
# veteran). Rottweiler rust points (muzzles, brow dots, chest V, socks), a hackle ridge, thick legs with black claws,
# and a tail that ends in a SERPENT head (red eyes, 2 fangs). No glow (hellfire = VFX).
# Old chibi version: _tools/chibi_specs/Cerberus.py
import math
from mathutils import Vector, Euler, Matrix

DISPLAY = "Cerberus"
MOTION = "Walk"
RIG = "quad"
HEIGHT = 8.5

CHAR = (96, 92, 108)          # charcoal body (Roblox renders ~0.6x darker -> near-black hound in game)
BACK = (56, 54, 68)           # back saddle, hackles, crowns, brows, ear backs
RUST = (166, 94, 62)          # Rottweiler points: muzzles, brow dots, chest V, socks, paws
COLLAR = (60, 52, 58)
STEEL = (200, 200, 212)
RED = (255, 50, 40)           # the ONE accent: eyes, mouths, the serpent's eyes
RED_HOT = (255, 176, 166)
BLACK = (14, 14, 22)
TEETH = (238, 234, 220)
SCAR = (176, 170, 182)
SNAKE = (84, 92, 84)          # serpent tail scales (dark olive-grey) + belly
SNAKE_B = (150, 140, 112)

PITCH = 0.042                 # stud pitch = 0.042 x (U / U_raiju), U = model height / HEIGHT (1.58 / 8.5 vs 1.498 / 8)

# leg joints (left side): hip/shoulder, knee/elbow, ankle/wrist, paw centre
LEGS = {"F": ((0.19, -0.36, 0.76), (0.19, -0.28, 0.47), (0.19, -0.36, 0.115), (0.19, -0.41, 0.048)),
        "B": ((0.16, 0.38, 0.78), (0.16, 0.25, 0.48), (0.16, 0.47, 0.21), (0.16, 0.41, 0.048))}
# head tag -> (neck base, throat joint, yaw, scale)
HEADS = {"C": ((0, -0.44, 0.93), (0, -0.70, 1.15), 0.0, 1.10),
         "L": ((0.205, -0.44, 0.90), (0.37, -0.63, 1.05), 32.0, 1.0),
         "R": ((-0.205, -0.44, 0.90), (-0.37, -0.63, 1.05), -32.0, 1.0)}
TAILP = [(0, 0.58, 0.90), (0.04, 0.80, 0.94), (0.26, 0.93, 1.02), (0.58, 0.95, 1.20)]


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


def _rz(deg):
    return Matrix.Rotation(math.radians(deg), 3, "Z")


def head(B, tag):
    """one head in head-local space (throat joint at the origin, facing -Y), scaled and yawed"""
    import blockkit as bk
    base, J, yaw, sc = HEADS[tag]
    J = Vector(J)
    Rz = _rz(yaw)
    hb, jb, nb = "Head_" + tag, "Jaw_" + tag, "Neck_" + tag

    def P(p):
        return J + Rz @ (Vector(p) * sc)

    def add(p, h, color, bone, rot=(0, 0, 0), **kw):
        R = Rz @ Euler([math.radians(a) for a in rot], "XYZ").to_matrix()
        return B.add(P(p), tuple(v * sc for v in h), color, bone, R=R, **kw)

    def seg(p0, p1, hw, hd_, color, bone, **kw):
        return B.seg(P(p0), P(p1), hw * sc, hd_ * sc, color, bone, side=Rz @ Vector((1, 0, 0)), **kw)

    def spike(p, d, ln, w, color, bone, **kw):
        return B.spike(P(p), Rz @ Vector(d), ln * sc, w * sc, color, bone, side=Rz @ Vector((1, 0, 0)), **kw)

    # skull, dark crown, broad snout, rust upper lip, nose
    add((0, -0.13, 0.085), (0.125, 0.115, 0.105), CHAR, hb, top=(0.82, 0.85), rnd=0.30)
    add((0, -0.11, 0.195), (0.095, 0.09, 0.025), BACK, hb, top=(0.8, 0.8))
    seg((0, -0.22, 0.055), (0, -0.44, 0.035), 0.088, 0.066, CHAR, hb, top=(0.86, 0.84), ext=0.02)
    seg((0, -0.23, 0.002), (0, -0.43, -0.002), 0.084, 0.026, RUST, hb, top=(0.86, 0.9))
    add((0, -0.445, 0.082), (0.044, 0.026, 0.030), BLACK, hb, role="detail", bevel=0.01)
    # fangs + lip teeth
    for s in (1, -1):
        spike((s * 0.052, -0.39, -0.01), (0, 0, -1), 0.075, 0.016, TEETH, hb)
        for y in (-0.33, -0.28):
            spike((s * 0.066, y, -0.01), (0, 0, -1), 0.035, 0.012, TEETH, hb)
    # lower jaw (opens in the snaps) + red mouth + lower fangs
    seg((0, -0.20, -0.052), (0, -0.42, -0.056), 0.074, 0.026, RUST, jb, top=(0.82, 1), ext=0.02)
    add((0, -0.31, -0.024), (0.058, 0.10, 0.008), RED, jb, studs=[], role="detail", bevel=0.004)
    for s in (1, -1):
        spike((s * 0.044, -0.40, -0.03), (0, 0, 1), 0.05, 0.013, TEETH, jb)
    # narrow red eyes under heavy dark brows, rust brow dots, rust cheeks
    for s in (1, -1):
        rot = (0, -s * 18, s * 20)
        add((s * 0.074, -0.235, 0.130), (0.052, 0.008, 0.025), BLACK, hb, rot=rot, studs=[], role="detail",
            bevel=0.004)
        add((s * 0.076, -0.242, 0.130), (0.043, 0.006, 0.013), RED, hb, rot=rot, studs=[], role="detail",
            bevel=0.003)
        add((s * 0.083, -0.246, 0.132), (0.018, 0.004, 0.006), RED_HOT, hb, rot=rot, studs=[], role="detail",
            bevel=0.002)
        add((s * 0.068, -0.212, 0.172), (0.066, 0.03, 0.026), BACK, hb, rot=(0, -s * 22, s * 20), role="detail",
            bevel=0.01)                                                                   # heavy brow
        add((s * 0.06, -0.205, 0.205), (0.022, 0.012, 0.016), RUST, hb, role="detail", bevel=0.005)  # brow dot
    # ears: the personality
    def ear(s, rot, h=(0.048, 0.022, 0.09), top=(0.10, 0.5), torn=False):
        side = "L" if s > 0 else "R"
        e = add((s * 0.075, -0.07, 0.205 + h[2] * 0.85), h, BACK, hb, rot=rot, top=top)
        B.add(e.world((0, -h[1] * sc - 0.002, -0.012)), (h[0] * 0.6 * sc, 0.006, h[2] * 0.7 * sc), RUST, hb, R=e.R,
              top=(0.15 if not torn else 0.7, 1), studs=[], role="detail", bevel=0.004)
        return e
    for s in (1, -1):
        if tag == "C":                                   # alpha: tall upright ears
            ear(s, (-14, s * 8, -s * 12), h=(0.05, 0.022, 0.10))
        elif tag == "L":                                 # hothead: ears pinned flat back
            ear(s, (-72, s * 6, -s * 16))
        else:                                            # veteran: one upright, one torn short + blunt
            if s > 0:
                ear(s, (-12, s * 6, -s * 16))
            else:
                ear(s, (-20, s * 10, -s * 22), h=(0.05, 0.022, 0.06), top=(0.65, 0.6), torn=True)
    if tag == "R":                                       # veteran scar across its right eye
        B.bar(P((-0.13, -0.225, 0.19)), P((-0.04, -0.250, 0.04)), Rz @ Vector((0, -1, 0.2)), 0.016, 0.008, SCAR,
              hb, studs=[], bevel=0.003)
    # cheek ruff: swept-back dark spikes
    for s in (1, -1):
        for z, dz, L, w in ((0.03, -0.30, 0.10, 0.034), (0.10, 0.05, 0.11, 0.036)):
            spike((s * 0.105, -0.12, z), (s * 0.40, 0.92, dz), L, w, BACK, hb, top=(0.12, 0.4))
    # thick neck + spiked collar
    base = Vector(base)
    top = J + Rz @ (Vector((0, -0.02, 0.08)) * sc)
    side = Rz @ Vector((1, 0, 0))
    B.seg(base, top, 0.095 * sc, 0.108 * sc, CHAR, nb, side=side, ext=0.10, ext1=0.02, top=(0.92, 0.92))
    d = (top - base).normalized()
    c = base.lerp(top, 0.62)
    B.seg(c - d * 0.04, c + d * 0.04, 0.115 * sc, 0.130 * sc, COLLAR, nb, side=side, role="limb", rnd=0.2)
    fwd = d.cross(side).normalized()
    if fwd.z < 0:
        fwd = -fwd
    for a in (-50, 0, 50):                                  # top half only (clear of the neighbouring necks)
        r = (fwd * math.cos(math.radians(a)) + side * math.sin(math.radians(a))).normalized()
        B.spike(c + r * 0.11 * sc, r, 0.075, 0.024, STEEL, nb, top=(0.12, 0.12), role="limb")


def model(k):
    import blockkit as bk
    B = bk.Blocks(k, seed=127, tier=3, plates=False)
    # ---------------- torso: deep broad ribcage tapering underneath, sloped tuck, narrow waist, smaller hips
    rib = B.add((0, -0.22, 0.735), (0.25, 0.34, 0.265), CHAR, "Chest", bot=(0.66, 0.56), top=(0.90, 0.92), rnd=0.30)
    B.seg((0, -0.12, 0.50), (0, 0.26, 0.625), 0.13, 0.08, CHAR, "Spine", top=(0.82, 0.75), side=(1, 0, 0))   # tuck
    B.add((0, 0.12, 0.80), (0.17, 0.21, 0.15), CHAR, "Spine", bot=(0.72, 0.70), top=(0.95, 1), rnd=0.30)       # waist
    B.add((0, 0.38, 0.79), (0.20, 0.20, 0.17), CHAR, "Spine", rot=(-8, 0, 0), top=(0.84, 0.90), bot=(0.85, 0.9),
          rnd=0.30)                                                                                         # hips
    B.add((0, 0.02, 0.968), (0.12, 0.30, 0.025), BACK, "Spine")                                             # saddle
    # shoulder yoke that carries the three necks
    B.add((0, -0.40, 0.93), (0.29, 0.17, 0.11), CHAR, "Chest", top=(0.80, 0.75), rnd=0.38)
    # rust underside line + chest V
    B.add((0, -0.25, 0.476), (0.115, 0.16, 0.022), RUST, "Chest", bot=(0.8, 0.9), studs=[])
    B.seg((0, -0.12, 0.488), (0, 0.22, 0.596), 0.085, 0.02, RUST, "Spine", side=(1, 0, 0), top=(0.8, 1), ext=0.03)
    for s in (1, -1):
        p0 = Vector((s * 0.10, -0.497, 0.82))         # seated on the tapered ribcage front (LESSONS 2)
        p1 = Vector((s * 0.03, -0.446, 0.60))
        B.bar(p0, p1, (0, -1, -0.23), 0.07, 0.012, RUST, "Chest", studs=[], bevel=0.004, top=(1, 0.3))
    for tag in ("L", "R", "C"):
        head(B, tag)
    # hackle ridge along the back (dark, laid back, shrinking toward the tail)
    for y, z, L, ang, bone in ((-0.36, 1.03, 0.16, -55, "Chest"), (-0.22, 1.00, 0.17, -60, "Chest"),
                               (-0.08, 0.99, 0.15, -64, "Chest"), (0.06, 0.975, 0.13, -68, "Spine"),
                               (0.20, 0.965, 0.11, -70, "Spine"), (0.34, 0.95, 0.09, -72, "Spine")):
        d = Vector((0, math.sin(math.radians(-ang)), math.cos(math.radians(-ang))))
        B.spike((0, y, z - 0.04), d, L, 0.06, BACK, bone, top=(0.15, 0.25))
    # ---------------- legs: thick, rust socks, rust paws with 4 black claws
    for s, side in ((1, "L"), (-1, "R")):
        for fb in ("F", "B"):
            H, K, A, Pw = (X(p, s) for p in LEGS[fb])
            leg, shin, foot = "Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side
            if fb == "F":
                B.seg(H + Vector((0, 0, 0.08)), K, 0.092, 0.11, CHAR, leg, ext=0.0, ext1=0.03, top=(0.85, 0.72))
                B.seg(K, A, 0.080, 0.080, CHAR, shin, top=(0.85, 0.85), ext=0.03, ext1=0.02)
                B.seg(K + (A - K) * 0.62, A, 0.074, 0.074, RUST, shin, top=(0.95, 0.95), ext=0.0, ext1=0.035)
            else:
                B.seg(H + Vector((0, 0.03, 0.08)), K, 0.09, 0.15, CHAR, leg, bot=(0.85, 1), top=(0.75, 0.62),
                      ext=0.0, ext1=0.03)
                B.seg(K, A, 0.080, 0.084, CHAR, shin, top=(0.80, 0.80), ext=0.03, ext1=0.02)
                B.seg(A, Pw + Vector((0, 0.03, 0.03)), 0.064, 0.066, RUST, foot, ext=0.03)
            B.add(Pw, (0.086, 0.10, 0.048), RUST, foot, top=(0.85, 0.80))
            for gx in (-0.052, -0.0175, 0.0175, 0.052):
                B.spike((Pw.x + gx, Pw.y - 0.09, 0.036), (0, -1, -0.55), 0.06, 0.014, BLACK, foot)
    # ---------------- serpent tail: tapering scaled tail curving up, ending in a snake head (red eyes, 2 fangs)
    T = [Vector(p) for p in TAILP]
    for (a, b), (w, d), bn in zip(zip(T, T[1:]), ((0.062, 0.062), (0.056, 0.056), (0.05, 0.05)),
                                  ("Tail1", "Tail2", "Tail3")):
        B.seg(a, b, w, d, CHAR if bn == "Tail1" else SNAKE, bn, ext=0.04, top=(0.85, 0.85))
    for a, b, bn in ((T[1], T[2], "Tail2"), (T[2], T[3], "Tail3")):          # pale belly scales (front side)
        n = (b - a).cross(Vector((1, 0, 0))).normalized()
        if n.y > 0:
            n = -n
        B.bar(a + n * 0.042, b + n * 0.034, n, 0.05, 0.01, SNAKE_B, bn, studs=[], bevel=0.004)
    # snake head: wedge looking forward-up over the back
    hb = "Tail3"
    sp = T[3] + Vector((0, -0.02, 0.02))
    Ry = Euler((0, 0, math.radians(72)), "XYZ").to_matrix()          # yawed 72 deg out (beside the head fan)
    d = (Ry @ Vector((0, -0.6, 0.8))).normalized()
    sh = B.seg(sp, sp + d * 0.20, 0.078, 0.05, SNAKE, hb, top=(0.55, 0.6), ext=0.03)
    B.seg(sp + d * 0.04 - Vector((0, 0, 0)), sp + d * 0.18, 0.06, 0.016, RED, hb, top=(0.6, 1), studs=[],
          role="detail")                                                                   # open red mouth line
    side = Ry @ Vector((1, 0, 0))
    up = d.cross(side).normalized()
    if up.z < 0:
        up = -up
    for s in (1, -1):
        e = sp + d * 0.09 + side * (s * 0.058) + up * 0.035
        B.add(e, (0.010, 0.030, 0.014), RED, hb, R=bk.frame_from(e, e + d, side * s), studs=[], role="detail",
              bevel=0.003)
        B.spike(sp + d * 0.17 + side * (s * 0.028) - up * 0.02, -up + d * 0.25, 0.065, 0.013, TEETH, hb)
    B.build()
    bk.stud_skin(k, PITCH)
    return {"TH": round(B.th, 3)}


# ------------------------------------------------------------------ rig
def rig(k):
    k.joint("Spine", (0, 0.20, 0.80), "Root", tail=(0, -0.4, 0))
    k.joint("Chest", (0, -0.10, 0.80), "Spine", tail=(0, -0.4, 0))
    for tag, (base, J, yaw, sc) in HEADS.items():
        d = (Vector(J) - Vector(base))
        k.joint("Neck_" + tag, base, "Chest", tail=tuple(d))
        fwd = _rz(yaw) @ Vector((0, -0.35, 0))
        k.joint("Head_" + tag, J, "Neck_" + tag, tail=tuple(fwd))
        k.joint("Jaw_" + tag, Vector(J) + _rz(yaw) @ (Vector((0, -0.20, -0.03)) * sc), "Head_" + tag,
                tail=tuple(fwd * 0.6))
    for s, side in ((1, "L"), (-1, "R")):
        for fb, parent, knee in (("F", "Chest", (0, 1, 0)), ("B", "Spine", (0, -1, 0))):
            H, K, A, Pw = (X(p, s) for p in LEGS[fb])
            k.joint("Leg_" + fb + side, H, parent)
            k.joint("Shin_" + fb + side, K, "Leg_" + fb + side)
            k.joint("Foot_" + fb + side, A, "Shin_" + fb + side, tail=(0, -0.15, 0))
            k.add_leg2("Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side, knee=knee)
    k.joint("Tail1", TAILP[0], "Spine")
    k.joint("Tail2", TAILP[1], "Tail1")
    k.joint("Tail3", TAILP[2], "Tail2", tail=(0, 0.07, 0.16))


# ------------------------------------------------------------------ animation (FIERCE_PLAN 2026-10-09)
import petkit as pk
import _common as cm

LEGS4 = ["Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR"]
TAIL = ["Tail1", "Tail2", "Tail3"]


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


def hd(k, f, tag, nk=0.0, ny=0.0, h=0.0, hy=0.0, roll=0.0, jaw=3.0, lunge=0.0):
    """one head: nk/ny = neck pitch/yaw (pitch - lifts; yaw + turns toward the pet's left, +X), h/hy = head
    pitch/yaw, roll = head tilt, jaw open (deg), lunge = the neck pushes out along the head's facing"""
    yaw = HEADS[tag][2]
    fwd = _rz(yaw) @ Vector((0, -1, 0))
    k.key("Neck_" + tag, f, rot=(nk, ny, 0), loc=tuple(fwd * lunge))
    k.key("Head_" + tag, f, rot=(h, hy, roll))
    k.key("Jaw_" + tag, f, rot=(jaw, 0, 0))


def tail(k, f, n, sway=8.0, lift=0.0, cycles=2, look=0.0):
    cm.chain(k, f, n, TAIL, sway=sway, pitch=lift, cycles=cycles, lag=0.15, grow=0.5)
    if look:
        k.key("Tail3", f, rot=(lift, look, 0))


def idle(k):
    """SIBLING SQUABBLE: the CENTRE alpha keeps guard with slow turns and long holds; the LEFT hothead pants, jaw
    pulsing; the RIGHT veteran eyes the centre and at 66-78 darts in and nips at the centre's ear (no contact) - the
    CENTRE flinches away, the LEFT whips round and snarls at them; all settle. (Plan variant: the right head cannot
    reach the left head's ear past the centre head, so it nips the centre's ear.)"""
    n = 120
    k.new_action("idle", n, True)
    # centre: (neck pitch, neck yaw, head pitch, head yaw, roll)
    C = [(0, (0, 0, 0, 0, 0)), (14, (0, 0, 0, 0, 0)), (22, (-2, 4, 0, 14, 0)), (38, (-2, 4, 0, 14, 0)),
         (46, (-2, -3, 0, -14, 0)), (56, (-2, -3, 0, -14, 0)), (63, (0, 0, 0, 0, 0)), (70, (-12, 4, -10, 4, 6)),
         (84, (-12, 4, -10, 4, 6)), (92, (-2, -4, 0, -8, 0)), (100, (-2, -4, 0, -8, 0)), (110, (0, 0, 0, 0, 0)),
         (120, (0, 0, 0, 0, 0))]
    # left (hothead): panting; whips toward the squabble and snarls at 76-88
    L = [(0, (2, 0, 2, 0, 0)), (72, (2, 0, 2, 0, 0)), (77, (-4, -4, -6, -6, 0)), (88, (-4, -4, -6, -6, 0)),
         (98, (2, 0, 2, 0, 0)), (120, (2, 0, 2, 0, 0))]
    # right (veteran): eyes the centre, darts in (66-72), nips (74), pulls back (80-92)
    R = [(0, (0, 0, 0, 0, 0)), (56, (0, 0, 0, 0, 0)), (61, (0, 3, 2, 12, 0)), (64, (0, 3, 2, 12, 0)),
         (69, (-10, 16, -6, 10, -6)), (76, (-10, 16, -6, 10, -6)), (84, (0, 6, 0, 6, 0)), (94, (0, 6, 0, 6, 0)),
         (106, (0, 0, 0, 0, 0)), (120, (0, 0, 0, 0, 0))]
    RJ = [(0, 3), (64, 3), (69, 22), (74, 0), (76, 14), (78, 0), (120, 3)]
    LJ = [(0, 0.0), (72, 0.0), (77, 1.0), (88, 1.0), (96, 0.0), (120, 0.0)]       # snarl weight
    for f in range(0, n + 1):
        if f % 2 and not (64 <= f <= 90):
            continue
        b = pk.wave(f, n, 0, 4)
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, 0.006 * b))
        k.key("Chest", f, rot=(-0.8 * b, 0, 0))
        nk, ny, h, hy, r = tab(C, f)
        hd(k, f, "C", nk, ny, h, hy, r, jaw=3)
        nk, ny, h, hy, r = tab(L, f)
        sn = tab(LJ, f)
        pant = 0.5 - 0.5 * math.cos(2 * math.pi * f / 8)
        hd(k, f, "L", nk + 1.5 * pant, ny, h + 1.5 * pant, hy, r, jaw=(1 - sn) * (3 + 15 * pant) + sn * 24)
        nk, ny, h, hy, r = tab(R, f)
        hd(k, f, "R", nk, ny, h, hy, r, jaw=tab(RJ, f), lunge=0.03 * tab([(0, 0.0), (66, 0.0), (70, 1.0),
                                                                            (76, 1.0), (82, 0.0), (120, 0.0)], f))
        tail(k, f, n, sway=7, lift=2, cycles=2, look=12 * pk.wave(f, n, 0.3, 2))
    cm.plant(k, n, legs=LEGS4)
    k.finish()
    k.meta["planted"] = LEGS4


def walk(k):
    n = 22

    def body(f):
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(0.8 * pk.wave(f, n, 0.1, 2), 1.5 * pk.wave(f, n), 2.0 * pk.wave(f, n)),
              loc=(0, 0, -0.02 * b))
        k.key("Chest", f, rot=(0, -2 * pk.wave(f, n, 0.25), -1.5 * pk.wave(f, n, 0.25)))
        for tag, ph, jw in (("L", 0.1, 10), ("C", 0.0, 3), ("R", 0.2, 4)):
            hd(k, f, tag, nk=2 + 2 * pk.wave(f, n, ph, 2), h=-2 * pk.wave(f, n, ph + 0.1, 2),
               jaw=jw + (4 * pk.wave(f, n, ph, 4) if tag == "L" else 0))
        tail(k, f, n, sway=10, lift=4, cycles=1)
    return cm.quad_walk(k, n, 0.16, 0.09, body, gait="trot")


def roar(k):
    """THREE-HEAD FAN SNARL: the body braces back, all three heads drop low, then FAN OUT wide (left head out-left,
    right head out-right, centre up), jaws open trembling in a snarl, front paws step out wide, the serpent tail
    rears; holds; returns."""
    import bpy
    n = 60
    k.new_action("roar", n, False)
    W = [(0, 0.0), (10, -1.0), (16, 1.0), (46, 1.0), (56, 0.0), (60, 0.0)]       # -1 = heads low, +1 = fan
    SP = [(0, (0.0, 0.0)), (10, (2.0, 0.025)), (16, (-3.0, 0.03)), (46, (-3.0, 0.03)), (56, (0.0, 0.0)),
          (60, (0.0, 0.0))]
    for f in range(0, n + 1):
        if f % 2 and not (14 <= f <= 46):
            continue
        w = tab(W, f)
        lo, fan = max(0.0, -w), max(0.0, w)
        ch, by = tab(SP, f)
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, by, -0.02 * fan))
        k.key("Chest", f, rot=(ch, 0, 0))
        tr = 3 * math.sin(2 * math.pi * f / 4) if 18 <= f <= 46 else 0.0
        jw = 3 + 25 * fan + tr
        hd(k, f, "C", nk=10 * lo - 10 * fan, h=8 * lo - 6 * fan, jaw=jw)
        hd(k, f, "L", nk=10 * lo + 2 * fan, ny=20 * fan, h=8 * lo, hy=10 * fan, roll=-6 * fan, jaw=jw)
        hd(k, f, "R", nk=10 * lo + 2 * fan, ny=-20 * fan, h=8 * lo, hy=-10 * fan, roll=6 * fan, jaw=jw)
        k.key("Tail1", f, rot=(-6 * fan, 0, 0))
        k.key("Tail2", f, rot=(-10 * fan, 0, 0))
        k.key("Tail3", f, rot=(-14 * fan, 6 * math.sin(2 * math.pi * f / 6) * fan, 0))
    k.bake_bezier_now()
    sc = bpy.context.scene
    SPRD = [(0, (0.0, 0.0)), (11, (0.0, 0.0)), (16, (0.05, 0.06)), (19, (0.05, 0.0)), (48, (0.05, 0.0)),
            (52, (0.0, 0.05)), (56, (0.0, 0.0)), (60, (0.0, 0.0))]
    for f in range(0, n + 1):
        sc.frame_set(f)
        dx, lift = tab(SPRD, f)
        for leg in LEGS4:
            s = 1 if leg.endswith("L") else -1
            fr = "_F" in leg
            k.solve_leg(leg, f, Vector((k.J[leg].x + (s * dx if fr else 0), k.J[leg].y, lift if fr else 0.0)))
    k.finish(loop=False)


def snap(k):
    """SIGNATURE - FLY SNAPPING: all three heads track a buzzing fly round a circle; the CENTRE snaps up at it
    overhead, the LEFT lunges far left and snaps, the RIGHT lunges far right and snaps; the fly lands in front and all
    three snap DOWN together in a fan (jaws clamp at f52), body braced, serpent tail up; the three jaws chew, smug;
    back to rest."""
    n = 95
    k.new_action("act_triplesnap", n, False)
    # per head: (neck pitch, neck yaw, head pitch, head yaw, roll, lunge)
    Z = (0, 0, 0, 0, 0, 0.0)
    C = [(0, Z), (10, Z), (15, (-22, 0, -14, 0, 0, 0.0)), (22, (-22, 0, -14, 0, 0, 0.0)), (28, (-4, 6, -4, 6, 0, 0.0)),
         (40, (-4, -6, -4, -6, 0, 0.0)), (46, (-2, 0, -2, 0, 0, 0.0)), (50, (18, 0, 14, 0, 0, 0.05)),
         (56, (18, 0, 14, 0, 0, 0.05)), (62, (-2, 0, -6, 0, 0, 0.0)), (75, (-2, 0, -6, 0, 0, 0.0)), (88, Z), (95, Z)]
    L = [(0, Z), (10, Z), (16, (-4, 4, -4, 4, 0, 0.0)), (22, (0, 4, 0, 4, 0, 0.0)), (27, (4, 24, 2, 10, -6, 0.07)),
         (34, (4, 24, 2, 10, -6, 0.07)), (40, (0, 4, 0, 4, 0, 0.0)), (46, (0, 0, 0, 0, 0, 0.0)),
         (50, (18, -4, 14, -4, 0, 0.05)), (56, (18, -4, 14, -4, 0, 0.05)), (62, (-2, 0, -6, 0, 6, 0.0)),
         (75, (-2, 0, -6, 0, 6, 0.0)), (88, Z), (95, Z)]
    R = [(0, Z), (10, Z), (16, (-4, -4, -4, -4, 0, 0.0)), (34, (0, -4, 0, -4, 0, 0.0)),
         (39, (4, -24, 2, -10, 6, 0.07)), (46, (4, -18, 2, -8, 6, 0.04)), (50, (18, 4, 14, 4, 0, 0.05)),
         (56, (18, 4, 14, 4, 0, 0.05)), (62, (-2, 0, -6, 0, -6, 0.0)), (75, (-2, 0, -6, 0, -6, 0.0)), (88, Z),
         (95, Z)]
    JC = [(0, 3), (12, 3), (16, 30), (19, 0), (46, 0), (49, 26), (52, 0), (95, 0)]
    JL = [(0, 3), (24, 3), (28, 30), (31, 0), (46, 0), (49, 26), (52, 0), (95, 0)]
    JR = [(0, 3), (36, 3), (40, 30), (43, 0), (46, 0), (49, 26), (52, 0), (95, 0)]
    SP = [(0, (0.0, 0.0)), (46, (0.0, 0.0)), (50, (-3.0, 0.03)), (58, (-3.0, 0.03)), (66, (0.0, 0.0)),
          (95, (0.0, 0.0))]
    for f in range(0, n + 1):
        ch, by = tab(SP, f)
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, by, 0))
        k.key("Chest", f, rot=(ch, 0, 0))
        track = 0.0 if f > 12 else math.sin(math.pi * f / 12)     # 0-10: all heads follow the fly's circle
        cp, cy = 5 * math.sin(2 * math.pi * f / 10) * track, 8 * math.cos(2 * math.pi * f / 10) * track
        chew = 6 * (0.5 - 0.5 * math.cos(2 * math.pi * (f - 56) / 8)) if 56 <= f <= 74 else 0.0
        for tag, T, J, ph in (("C", C, JC, 0.0), ("L", L, JL, 0.33), ("R", R, JR, 0.66)):
            nk, ny, h, hy, r, lg = tab(T, f)
            cw = 6 * (0.5 - 0.5 * math.cos(2 * math.pi * ((f - 56) / 8 + ph))) if 56 <= f <= 74 else 0.0
            hd(k, f, tag, nk + cp, ny + cy, h + cp * 0.5, hy, r, jaw=tab(J, f) + cw, lunge=lg)
        lift = tab([(0, 0.0), (46, 0.0), (52, -18.0), (66, -14.0), (80, 0.0), (95, 0.0)], f)
        tail(k, f, n, sway=6, lift=lift, cycles=3)
    cm.plant(k, n, legs=LEGS4)
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    snap(k)
    return stride


def check_pairs():
    P = [("Leg_FL", "Leg_BL"), ("Leg_FR", "Leg_BR"), ("Leg_FL", "Leg_FR"), ("Leg_BL", "Leg_BR"),
         ("Shin_FL", "Shin_FR"), ("Shin_BL", "Shin_BR"), ("Shin_FL", "Shin_BL"), ("Shin_FR", "Shin_BR"),
         ("Foot_FL", "Foot_FR"), ("Foot_BL", "Foot_BR"), ("Foot_FL", "Foot_BL"), ("Foot_FR", "Foot_BR")]
    for a, b in (("L", "C"), ("R", "C"), ("L", "R")):
        for x in ("Head_", "Jaw_", "Neck_"):
            for y in ("Head_", "Jaw_", "Neck_"):
                P.append((x + a, y + b))
    for tag in "LCR":
        for b in ("Leg_FL", "Leg_FR", "Shin_FL", "Shin_FR", "Foot_FL", "Foot_FR"):
            P.append(("Head_" + tag, b))
            P.append(("Jaw_" + tag, b))
        P.append(("Head_" + tag, "Chest"))
        P.append(("Jaw_" + tag, "Chest"))
    for t in ("Tail2", "Tail3"):
        for b in ("Leg_BL", "Leg_BR", "Shin_BL", "Shin_BR"):
            P.append((t, b))
    return P


def joints():
    out = []
    for tag, (base, J, yaw, sc) in HEADS.items():
        Jv = Vector(J)
        out.append((Jv, Jv, 0.12, "Head_" + tag))
        bv = Vector(base)                 # neck roots overlap inside the shoulder yoke (hidden)
        out.append((bv, bv, 0.24, "Neck_" + tag))
    return out
