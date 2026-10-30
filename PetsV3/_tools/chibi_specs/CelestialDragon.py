# Celestial Dragon (Celestial egg #3, tier 6, winged quad): the V2 moon dragon rebuilt in the Steal-an-Egg block
# style (STYLE_BIBLE 3 "CelestialDragon"): a majestic pearl dragon with a royal-blue back, a deep chest with gold-cream
# belly bands, an S-neck with gold trim bands + rivets, a crown of 4 gold horns, fierce-majestic blue eyes under gold
# brow plates, broad royal-blue membrane wings with gold constellation plates, navy socks with gold claws, a long
# tail ending in a gold crescent-moon blade and 5 small gold stars floating above the back on an Orbit bone.
# No glow (sparkles / star breath = particle VFX; Breath and Flame bones are the anchors).
# Clips ported from PetsV2: dreamy idle (gazes up at the sky, half wing-stretch, tail S-sway), lateral walk, real
# flight (legs pump), takeoff (launch) / land (touch), roar = STAR BREATH (rears back, jaw wide), signature
# act_twirl = a happy twirl on the spot with little hops and half-open wings.
import math
from mathutils import Vector, Matrix
import wing3

DISPLAY = "Celestial Dragon"
MOTION = "Fly"
RIG = "wingquad"
HEIGHT = 7.5

PEARL = (232, 236, 255)
SHADE = (190, 200, 240)
BELLY = (255, 226, 150)
NAVY = (40, 48, 110)
ROYAL = (60, 90, 220)
MEM = (120, 160, 255)
MEM_IN = (96, 128, 224)
GOLD = (255, 200, 60)
GOLD_D = (226, 162, 36)
IRIS = (60, 120, 230)
MOUTH = (90, 30, 70)
FANG = (250, 248, 255)

HIPS_C, HIPS_H = (0, 0.30, 0.80), (0.36, 0.42, 0.28)
CHEST_C, CHEST_H = (0, -0.18, 0.88), (0.42, 0.36, 0.34)          # chest 17 % wider / 21 % taller than the hips
HEAD_C, HEAD_H = (0, -0.84, 1.88), (0.40, 0.31, 0.29)            # HW 0.80 (0.95 TW), HH 0.58 (0.85 TH)
LEGS = {"F": (0.27, -0.26), "B": (0.24, 0.50)}
LEG_TOP = 0.58
WING = wing3.Wing(S=(0.42, -0.14, 1.20), W=(1.10, 0.04, 1.72), H=(1.10, 1.04, 1.04), BB=(0.34, 0.46, 1.06))
F1, F2 = (1.88, 0.30, 1.94), (1.76, 0.92, 1.38)
TAILP = [(0, 0.70, 0.92), (0, 1.14, 0.78), (0, 1.56, 0.70), (0, 1.94, 0.74)]
ORBIT_C = (0, 0.36, 1.62)


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


def star(B, c, n, r, thick, color, bone, rot=0.0):
    """5-point star of tapered rays around a small core, lying in the plane with normal n"""
    c, n = Vector(c), Vector(n).normalized()
    u = Vector((1, 0, 0)) if abs(n.x) < 0.9 else Vector((0, 1, 0))
    u = (u - n * u.dot(n)).normalized()
    v = n.cross(u)
    B.add(c, (r * 0.36, r * 0.36, thick), color, bone, R=Matrix((u, v, n)).transposed(), studs=[], bevel=thick * 0.5)
    for i in range(5):
        a = math.radians(rot + 90 + 72 * i)
        d = u * math.cos(a) + v * math.sin(a)
        B.bar(c, c + d * r, n, r * 0.62, thick, color, bone, studs=[], top=(1, 0.12), bevel=thick * 0.5)


def membrane_wing(B, s, side):
    """STYLE_BIBLE 2d membrane wing: royal-blue arm + fingers (tapering to 0.4), wrist knuckle + gold claw, 2-tone
    periwinkle panels with scalloped trailing edges, gold constellation plates on the outer panels (both faces)."""
    S, W, f3, bb = (X(p, s) for p in (WING.S, WING.W, WING.H, WING.BB))
    f1, f2 = X(F1, s), X(F2, s)
    wb, tb = "Wing_" + side, "WingTip_" + side
    B.seg(S, W, 0.05, 0.06, ROYAL, wb, side=(0, 0, 1), ext=0.10, role="limb", studs=[])
    B.add(W, (0.075, 0.075, 0.075), ROYAL, wb, studs=[], role="limb")
    B.add(W + Vector((0, 0, 0.0)), (0.08, 0.04, 0.04), GOLD, wb, studs=[], role="limb")
    B.spike(W + Vector((s * 0.02, -0.02, 0.05)), (s * 0.6, -0.3, 0.75), 0.17, 0.035, GOLD, wb, top=(0.15, 0.15))
    B.seg(W, f3, 0.034, 0.038, ROYAL, wb, side=(0, 0, 1), top=(0.45, 0.45), studs=[], role="limb")
    for f, w in ((f1, 0.042), (f2, 0.038)):
        B.seg(W, f, w, w + 0.004, ROYAL, tb, side=(0, 0, 1), top=(0.4, 0.4), studs=[], role="limb")
    e12 = f1.lerp(f2, 0.5).lerp(W, 0.16)
    e23 = f2.lerp(f3, 0.5).lerp(W, 0.16)
    q = f3.lerp(bb, 0.5).lerp(S, 0.14)
    B.poly([S, W, f3, q, bb], 0.03, MEM_IN, wb)
    B.poly([W, f1, e12, f2], 0.03, MEM, tb)
    B.poly([W, f2, e23, f3], 0.03, MEM, tb)
    # constellations: small gold squares on both faces of the outer panels (+ one on the inner panel)
    for pts, bone, (a, b, c) in (((W, f1, f2), tb, (0.55, 0.30, 0.15)), ((W, f1, f2), tb, (0.40, 0.42, 0.18)),
                                 ((W, f1, f2), tb, (0.32, 0.30, 0.38)), ((W, f2, f3), tb, (0.42, 0.30, 0.28)),
                                 ((W, f2, f3), tb, (0.30, 0.42, 0.28)), ((S, W, f3), wb, (0.20, 0.38, 0.42))):
        P0, P1, P2 = pts
        p = P0 * a + P1 * b + P2 * c
        nrm = (P1 - P0).cross(P2 - P0).normalized()
        for sg in (1, -1):
            B.add(p + nrm * sg * 0.022, (0.032, 0.032, 0.008), GOLD, bone, R=plane_R(nrm, 45), studs=[], bevel=0.004)


def plane_R(n, deg=0.0):
    """rotation whose local z is n (local x/y in the plane, turned by deg)"""
    n = Vector(n).normalized()
    u = Vector((1, 0, 0)) if abs(n.x) < 0.9 else Vector((0, 1, 0))
    u = (u - n * u.dot(n)).normalized()
    v = n.cross(u)
    return Matrix((u, v, n)).transposed() @ Matrix.Rotation(math.radians(deg), 3, "Z")


def model(k):
    """Celestial Dragon, bible T6: majestic pearl + royal blue + gold, 4-horn crown, crescent tail, orbiting stars."""
    import blockkit as bk
    B = bk.Blocks(k, seed=83, tier=6)
    D = 0.62
    hips = B.add(HIPS_C, HIPS_H, ROYAL, "Spine", bot=(0.90, 0.94), rnd=0.28, density=D, studs=["+x", "-x", "+y", "-y"])
    chest = B.add(CHEST_C, CHEST_H, PEARL, "Spine", bot=(0.86, 0.92), rnd=0.28, density=D)
    # royal-blue hindquarters + a royal mantle on the chest top (continuous blue back), gold constellation on top
    B.add((0, -0.08, 1.228), (0.30, 0.22, 0.008), ROYAL, "Spine", studs=[], bevel=0.006)
    for (x, y) in ((-0.10, 0.22), (0.0, 0.32), (0.11, 0.30), (0.08, 0.48), (-0.06, 0.58)):
        B.add((x, y, 1.097), (0.026, 0.026, 0.006), GOLD, "Spine", rot=(0, 0, 45), studs=[], bevel=0.003)
    # gold-cream belly bands across the chest front (follow the taper) + belly plate underneath
    for z0, z1, w in ((0.62, 0.70, 0.46), (0.76, 0.84, 0.54), (0.90, 0.98, 0.56), (1.04, 1.10, 0.48)):
        front_inlay(B, chest, 0, z0, z1, w, 0.008, BELLY, "Spine")
    B.add((0, 0.16, 0.522), (0.24, 0.40, 0.010), BELLY, "Spine", studs=[], bevel=0.006)
    # dorsal blades: royal blue, laid back 62 deg, wider than tall (chest top -> hips -> tail)
    for y, z, sz, bone in ((-0.30, 1.22, 0.9, "Spine"), (-0.06, 1.22, 1.0, "Spine"), (0.62, 1.08, 0.8, "Spine"),
                           (0.86, 1.00, 0.65, "Tail1"), (1.08, 0.92, 0.55, "Tail1")):
        base = Vector((0, y, z - 0.04))
        d = Vector((0, 0.88, 0.47)).normalized()
        L = 0.24 * sz
        R = bk.frame_from(base, base + d, (1, 0, 0))
        B.add(base + d * L / 2, (0.045 * sz, 0.11 * sz, L / 2), ROYAL if y < 0.2 else PEARL, bone, R=R,
              top=(0.45, 0.10), studs=[], role="limb")
    # ---- S-neck: lower block leaning forward, upper block leaning back; gold trim bands with rivets; belly plates
    n1 = B.add((0, -0.48, 1.26), (0.26, 0.21, 0.26), PEARL, "Neck", rot=(28, 0, 0), studs=[], rnd=0.3)
    n2 = B.add((0, -0.62, 1.56), (0.235, 0.19, 0.22), PEARL, "Neck", rot=(-10, 0, 0), studs=[], rnd=0.3)
    for blk, v in ((n1, -0.06), (n2, 0.02)):
        B.add(blk.world((0, 0, v)), (blk.h.x + 0.018, blk.h.y + 0.018, 0.035), GOLD, "Neck", R=blk.R, studs=[],
              role="limb", rnd=0.3)
        for sx in (1, -1):
            B.add(blk.world((sx * (blk.h.x + 0.026), -0.08, v)), (0.012, 0.022, 0.022), GOLD_D, "Neck", R=blk.R,
                  studs=[], bevel=0.006)
            B.add(blk.world((sx * (blk.h.x + 0.026), 0.08, v)), (0.012, 0.022, 0.022), GOLD_D, "Neck", R=blk.R,
                  studs=[], bevel=0.006)
    for blk, vs in ((n1, (0.14, -0.16)), (n2, (-0.12,))):
        for v in vs:
            B.add(blk.world((0, -blk.h.y - 0.008, v)), (blk.h.x * 0.7, 0.008, 0.045), BELLY, "Neck", R=blk.R,
                  studs=[], bevel=0.006)
    # ---- head (final size): muzzle, jaw, nostrils, 2 small fangs, fierce-majestic eyes under gold brow plates
    head = B.add(HEAD_C, HEAD_H, PEARL, "Head", top=(0.94, 0.94), rnd=0.28, density=D, studs=["+x", "-x", "+y", "+z"])
    snout = B.add((0, -1.25, 1.73), (0.24, 0.20, 0.12), PEARL, "Head", top=(0.90, 0.86), rnd=0.32, studs=[])
    for sx in (1, -1):
        B.add((sx * 0.08, front_y(snout, 1.80) - 0.004, 1.805), (0.032, 0.012, 0.018), NAVY, "Head",
              rot=(0, sx * 18, 0), studs=[], bevel=0.006)
    B.add((0, -1.19, 1.565), (0.21, 0.19, 0.05), BELLY, "Jaw", bot=(0.9, 0.9), studs=[], role="limb", rnd=0.3)
    B.add((0, -1.19, 1.617), (0.18, 0.16, 0.006), MOUTH, "Jaw", studs=[], bevel=0.004)
    fy = front_y(snout, 1.62) - 0.006
    B.add((0, fy, 1.622), (0.16, 0.006, 0.012), NAVY, "Head", studs=[], bevel=0.004)
    for sx in (1, -1):
        B.spike((sx * 0.115, fy - 0.004, 1.63), (0, -0.1, -1), 0.07, 0.022, FANG, "Head")
    B.face_eyes(head, "fierce", IRIS, base=PEARL, brow=GOLD, z=0.63, x=0.25, scale=1.22, pupil_size=(0.09, 0.09),
                hl_size=(0.07, 0.0), look=(0, 0.6), brow_spec=(0.30, 0.07, 16), hl_on_pupil=True)
    # cheek fins: 2 royal-blue blades per side from the back edge of the head
    for s in (1, -1):
        for z, dz, L in ((1.72, -0.25, 0.20), (1.84, 0.10, 0.24)):
            root = Vector((s * 0.36, -0.62, z))
            d = Vector((s * 0.55, 0.75, dz)).normalized()
            B.seg(root, root + d * L, 0.07, 0.035, ROYAL, "Head", side=(0, 0, 1), ext=0.05, top=(0.15, 0.5), studs=[],
                  role="limb")
    # ---- crown of 4 gold horns: 2 big swept-back 3-segment horns + 2 small forward horns, gold-dark tips
    for s in (1, -1):
        P = [Vector((s * 0.24, -0.76, 2.14)), Vector((s * 0.33, -0.60, 2.36)), Vector((s * 0.42, -0.36, 2.48)),
             Vector((s * 0.47, -0.08, 2.50))]
        B.seg(P[0], P[1], 0.07, 0.07, GOLD, "Head", side=(1, 0, 0), ext=0.10, top=(0.85, 0.85), studs=[], role="limb")
        B.seg(P[1], P[2], 0.06, 0.06, GOLD, "Head", side=(1, 0, 0), ext=0.03, top=(0.8, 0.8), studs=[], role="limb")
        B.spike(P[2] - (P[3] - P[2]).normalized() * 0.03, P[3] - P[2], (P[3] - P[2]).length + 0.05, 0.048, GOLD_D,
                "Head", top=(0.12, 0.12))
        B.spike(Vector((s * 0.34, -0.96, 2.10)), (s * 0.45, -0.25, 0.85), 0.20, 0.045, GOLD, "Head", top=(0.15, 0.15))
    # ---- legs: pearl, flush navy sock + navy paw with 3 gold claw nubs
    for s, side in ((1, "L"), (-1, "R")):
        for fb in ("F", "B"):
            x, y = LEGS[fb]
            X0 = s * x
            bone = "Leg_" + fb + side
            hx = 0.14 if fb == "F" else 0.13
            B.add((X0, y, 0.32), (hx, 0.15, 0.28), PEARL if fb == "F" else ROYAL, bone, bot=(0.9, 0.9), rnd=0.3,
                  density=D)
            B.add((X0, y, 0.115), (hx * 0.9 * 1.03, 0.15 * 0.9 * 1.03, 0.06), NAVY, bone, studs=[], role="limb")
            B.add((X0, y - 0.015, 0.045), (hx * 1.12, 0.17, 0.045), NAVY, bone, studs=[], role="limb", rnd=0.35)
            for gx in (-0.07, 0.0, 0.07):
                B.spike((X0 + gx, y - 0.175, 0.04), (0, -1, -0.25), 0.07, 0.022, GOLD, bone, top=(0.25, 0.25))
    # ---- long tail tapering 1.0 -> 0.35 + a flat gold crescent-moon blade (side-view plane)
    T = [Vector(p) for p in TAILP]
    for i, (hw, hd) in enumerate(((0.12, 0.13), (0.09, 0.095), (0.065, 0.07))):
        B.seg(T[i], T[i + 1], hw, hd, ROYAL if i < 2 else SHADE, "Tail%d" % (i + 1), side=(1, 0, 0),
              ext=0.12 if i == 0 else 0.05, top=(0.85, 0.85), studs=[], role="limb")
    C = T[3] + Vector((0, 0.10, 0.08))
    pts = []
    for j in range(7):
        a = math.radians(-120 + 240 * j / 6)
        pts.append(C + Vector((0, 0.20 * math.cos(a) - 0.02, 0.24 * math.sin(a))))
    for j in range(6):
        a, b = pts[j], pts[j + 1]
        t = abs(j + 0.5 - 3) / 3
        w = 0.12 * (1 - 0.7 * t)
        B.seg(a, b, 0.032, w / 2 + 0.01, GOLD, "Tail3", side=(1, 0, 0), ext=0.02, ext1=0.02, studs=[], role="limb",
              top=(1, 0.8 if j >= 3 else 1), bot=(1, 0.8 if j < 3 else 1))
    # ---- 5 floating gold stars on the Orbit bone (a small ring above the back)
    oc = Vector(ORBIT_C)
    for i in range(5):
        a = math.radians(90 + 72 * i)
        p = oc + Vector((0.24 * math.cos(a), 0.24 * math.sin(a), 0.03 * math.sin(2 * a)))
        star(B, p, (math.cos(a), math.sin(a), 0.0), 0.10, 0.018, GOLD, "Orbit", rot=0)
    # ---- wings
    for s, side in ((1, "L"), (-1, "R")):
        membrane_wing(B, s, side)
    B.build()
    return {"plates": B.stud_count, "TH": round(B.th, 3), "cell": round(B.pcell, 3)}


# ------------------------------------------------------------------ rig
def rig(k):
    k.joint("Spine", (0, 0.30, 0.84), "Root", tail=(0, -0.45, 0.1))
    k.joint("Neck", (0, -0.40, 1.08), "Spine", tail=(0, -0.2, 0.4))
    k.joint("Head", (0, -0.66, 1.64), "Neck", tail=(0, -0.35, 0.05))          # throat pivot
    k.joint("Jaw", (0, -1.02, 1.62), "Head", tail=(0, -0.3, 0))
    k.joint("Breath", (0, -1.48, 1.68), "Head", tail=(0, -0.25, 0))          # star-breath VFX anchor (no mesh)
    for s, side in ((1, "L"), (-1, "R")):
        for fb in ("F", "B"):
            x, y = LEGS[fb]
            k.joint("Leg_" + fb + side, (s * x, y, LEG_TOP), "Spine", tail=(0, 0, -0.4))
        k.joint("Wing_" + side, X(WING.S, s), "Spine")
        k.joint("WingTip_" + side, X(WING.W, s), "Wing_" + side, tail=(s * 0.6, 0.2, 0.1))
    k.joint("Tail1", TAILP[0], "Spine")
    k.joint("Tail2", TAILP[1], "Tail1")
    k.joint("Tail3", TAILP[2], "Tail2")
    k.joint("Flame", (0, 2.04, 0.82), "Tail3", tail=(0, 0, 0.2))             # crescent sparkle VFX anchor (no mesh)
    k.joint("Orbit", ORBIT_C, "Spine", tail=(0, 0, 0.2))


def check_pairs():
    W = ["Wing_L", "WingTip_L", "Wing_R", "WingTip_R"]
    P = [("Wing_L", "WingTip_L"), ("Wing_R", "WingTip_R"), ("WingTip_L", "WingTip_R"), ("Wing_L", "Wing_R"),
         ("WingTip_L", "Wing_R"), ("Wing_L", "WingTip_R")]
    for w in W:
        for b in ("Head", "Neck", "Spine", "Tail1", "Tail2", "Tail3", "Orbit", "Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR"):
            P.append((w, b))
    P += [("Leg_FL", "Leg_BL"), ("Leg_FR", "Leg_BR"), ("Leg_FL", "Leg_FR"), ("Leg_BL", "Leg_BR"),
          ("Head", "Leg_FL"), ("Head", "Leg_FR"), ("Jaw", "Leg_FL"), ("Jaw", "Leg_FR"), ("Head", "Spine"),
          ("Jaw", "Spine"), ("Jaw", "Neck"), ("Tail1", "Leg_BL"), ("Tail1", "Leg_BR"), ("Tail2", "Leg_BL"),
          ("Tail2", "Leg_BR"), ("Orbit", "Head"), ("Orbit", "Neck"), ("Orbit", "Spine"), ("Orbit", "Tail1"),
          ("Head", "Tail3")]
    return P


def joints():
    out = WING.joints()
    for s, sd in ((1, "L"), (-1, "R")):
        out.append((X(WING.S, s), X(WING.BB, s), 0.13, "Wing_" + sd))
    out.append(((0, -0.60, 1.58), (0, -0.70, 1.68), 0.26, "Head"))          # neck / head junction
    out.append(((0, -0.42, 1.10), (0, -0.40, 1.14), 0.24, "Neck"))          # neck / chest junction
    return out


# ------------------------------------------------------------------ animation
import petkit as pk
import _common as cm

LEGS4 = ["Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR"]
TAIL = ["Tail1", "Tail2", "Tail3"]
FOLD = dict(up=22, fwd=-8, twist=0, tip=92)


def wings(k, f, up, fwd=0.0, twist=0.0, tip=0.0, side=None):
    WING.key(k, f, up, fwd, twist, tip, side=side)


def folded(k, f, du=0.0, dfwd=0.0, dtip=0.0, side=None):
    wings(k, f, FOLD["up"] + du, FOLD["fwd"] + dfwd, FOLD["twist"], FOLD["tip"] + dtip, side)


def anchors(k, f):
    k.key("Breath", f, rot=(0, 0, 0), loc=(0, 0, 0))
    k.key("Flame", f, rot=(0, 0, 0))


def orbit(k, f, n, turns=1):
    """the 5 stars circle slowly (whole turns per clip so loops stay seamless) and bob"""
    cm.key_axis(k, "Orbit", f, (0, 0, 1), 360.0 * turns * f / n, loc=(0, 0, 0.03 * pk.wave(f, n, 0.0, 2)))


def keys_orbit(k, n, turns=1, step=None):
    step = step or max(1, n // 24)
    for f in range(0, n + 1, step):
        orbit(k, f, n, turns)
    if n % step:
        orbit(k, n, n, turns)


def idle(k):
    """dreamy: slow breathing, gazes up at the sky and slowly back, then looks aside; graceful tail S-sway; a lazy
    half wing-stretch; the stars circle above the back."""
    n = 108
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 3):
        s = pk.wave(f, n, 0, 2)
        k.key("Spine", f, rot=(-1.2 - 0.8 * s, 0, 0.6 * pk.wave(f, n, 0.3)), loc=(0, 0, 0.012 * (1 + s) / 2))
        cm.chain(k, f, n, TAIL, sway=9, pitch=2, cycles=2, lag=0.12, grow=0.45)
        k.key("Jaw", f, rot=(2, 0, 0))
        anchors(k, f)
    for f, nk, hd, yaw in ((0, 0, 0, 0), (20, 0, 0, 0), (36, -12, -14, 8), (56, -12, -16, 8), (70, 0, 0, -12),
                           (88, 0, 0, -12), (108, 0, 0, 0)):
        k.key("Neck", f, rot=(nk, yaw * 0.4, 0))
        k.key("Head", f, rot=(hd, yaw * 0.6, 0))
    for f, du, df in ((0, 0, 0), (60, 0, 0), (70, 16, 6), (82, 16, 6), (92, 0, 0), (108, 0, 0)):
        folded(k, f, du, df)
    keys_orbit(k, n, 1)
    cm.plant(k, n, legs=LEGS4)
    k.finish()
    k.meta["planted"] = LEGS4


def walk(k):
    n = 26

    def body(f):
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(1.0 * pk.wave(f, n, 0, 2), 2.0 * pk.wave(f, n, 0.1), 1.8 * pk.wave(f, n)),
              loc=(0, 0, 0.03 * b))
        k.key("Neck", f, rot=(-2 - 2 * pk.wave(f, n, 0.1, 2), -2 * pk.wave(f, n, 0.1), 0))
        k.key("Head", f, rot=(1 - 2 * pk.wave(f, n, 0.15, 2), -2 * pk.wave(f, n, 0.1), -2 * pk.wave(f, n, 0.05)))
        k.key("Jaw", f, rot=(2, 0, 0))
        folded(k, f, 3 * pk.wave(f, n, 0.1, 2))
        cm.chain(k, f, n, TAIL, sway=11, pitch=2, cycles=1, lag=0.15)
        anchors(k, f)
        orbit(k, f, n, 0)
    return cm.quad_walk(k, n, 0.15, 0.10, body, gait="walk")


# ---- flight
FLY_N = 24
PITCH = 16.0


def fly_legs(k, f, ph, amt=1.0):
    for leg in LEGS4:
        fr = leg[4] == "F"
        w = math.sin(2 * math.pi * (ph - (0.12 if fr else 0.25)))
        base = 58 if fr else 74
        k.key(leg, f, rot=(amt * (base + 12 * w), 0, 0), loc=(0, 0, 0))


def fly_pose(k, f, ph, legs=True):
    w = wing3.stroke(ph, top=28.0, bot=-46.0, sweep=12.0, twist=12.0, fold=32.0)
    wings(k, f, w["up"], w["fwd"], w["twist"], w["tip"])
    k.key("Spine", f, rot=(PITCH - 3 * math.sin(2 * math.pi * (ph - 0.1)), 0, 0),
          loc=(0, 0, 0.09 * math.cos(2 * math.pi * (ph - 0.45))))
    k.key("Neck", f, rot=(-12 - 2 * math.sin(2 * math.pi * (ph - 0.25)), 0, 0))
    k.key("Head", f, rot=(-10 + 2 * math.sin(2 * math.pi * (ph - 0.32)), 0, 0))
    k.key("Jaw", f, rot=(2, 0, 0))
    for i, b in enumerate(TAIL):
        k.key(b, f, rot=(4 + 8 * math.sin(2 * math.pi * (ph - 0.12 * (i + 1))),
                         3 * math.sin(2 * math.pi * (ph - 0.2 * i)), 0))
    anchors(k, f)
    if legs:
        fly_legs(k, f, ph)


def fly(k):
    n = FLY_N
    k.new_action("fly", n, True)
    for f in range(0, n + 1):
        fly_pose(k, f, f / n)
    keys_orbit(k, n, 1)
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
    for f, z, p, w in ((6, -0.10, -6, (26, -12, -4, 40)), (10, -0.13, -8, (34, -4, -8, -6)),
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
    keys_orbit(k, n, 0)
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
    for f, z, p, w in ((7, 0.10, -14, (24, 18, -12, -8)), (12, 0.06, -8, (-16, 12, -8, 4)),
                       (16, -0.08, 4, (14, -6, 0, 30)), (21, 0.02, -1, (20, -12, 0, 80))):
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
        k.key("Neck", f, rot=(-6 - p * 0.4, 0, 0))
        k.key("Head", f, rot=(-5, 0, 0))
        k.key("Jaw", f, rot=(2, 0, 0))
        wings(k, f, *w)
        for b in TAIL:
            k.key(b, f, rot=(4 - p * 0.3, 0, 0))
        anchors(k, f)
    rest_keys(k, n)
    keys_orbit(k, n, 0)
    for leg in LEGS4:
        k.key(leg, 7, rot=(-22 if leg[4] == "F" else -8, 0, 0), loc=(0, 0, 0))
    plant_frames(k, range(16, n + 1))
    k.finish(loop=False)
    k.events["land"] = {"touch": round(16 / n, 3)}


def roar(k):
    """STAR BREATH: rears back with the wings half raised, then stretches the S-neck forward and breathes out with
    the jaw wide (star-sparkle VFX from the Breath anchor), the stars spin faster, then settles."""
    n = 50
    k.new_action("roar", n, False)
    for f, sp, nk, hd, jw, du in ((0, 0, 0, 0, 2, 0), (11, -8, -16, -12, 6, 12), (18, 5, 14, 4, 30, 6),
                                  (32, 4, 12, 4, 32, 6), (40, 0, 0, 0, 4, 0), (50, 0, 0, 0, 2, 0)):
        k.key("Spine", f, rot=(sp, 0, 0), loc=(0, 0, 0.02 * (sp < 0)))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        folded(k, f, du=du, dfwd=-4 * (du > 0))
        for b in TAIL:
            k.key(b, f, rot=(4 - sp * 0.5, 0, 0))
        anchors(k, f)
    keys_orbit(k, n, 2)
    cm.plant(k, n, legs=LEGS4)
    k.finish(loop=False)


def twirl(k):
    """SIGNATURE (Celestial Dragon only) - CELESTIAL TWIRL: a happy full spin on the spot with little hops, wings
    half open, head up, the orbiting stars whirling twice as it turns, then a graceful pose."""
    import bpy
    n = 56
    k.new_action("act_twirl", n, False)
    for f, deg in ((0, 0), (8, 0), (16, 90), (24, 180), (32, 270), (40, 360), (48, 360), (56, 360)):
        cm.key_axis(k, "Spine", f, (0, 0, 1), deg, loc=(0, 0, 0.05 if 8 < f < 40 else 0))
        folded(k, f, 16 if 8 <= f <= 40 else 0, 4 if 8 <= f <= 40 else 0)
        k.key("Neck", f, rot=(-6 if 8 <= f <= 40 else 0, 0, 0))
        k.key("Head", f, rot=(-6 if 8 <= f <= 40 else 0, 0, 0))
        k.key("Jaw", f, rot=(2, 0, 0))
        for b in TAIL:
            k.key(b, f, rot=(4, -12 if 8 < f < 40 else 0, 0))
        anchors(k, f)
    keys_orbit(k, n, 2)
    k.bake_bezier_now()
    sc = bpy.context.scene
    for f in range(0, n + 1):
        sc.frame_set(f)
        for leg in LEGS4:
            if 9 <= f <= 39:
                hop = math.sin(math.pi * ((f - 9) % 6) / 6)
                k.key(leg, f, rot=(-10 * hop if leg[4] == "F" else 10 * hop, 0, 0), loc=(0, 0, 0))
            else:
                k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, 0.0)))
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    fly(k)
    takeoff(k)
    land(k)
    roar(k)
    twirl(k)
    return stride
