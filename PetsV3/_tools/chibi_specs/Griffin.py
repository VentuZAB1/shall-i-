# Griffin (Celestial egg #2): a noble sky griffin rebuilt to STYLE_BIBLE.md (2026-10-08 pro pass): a big white eagle
# head with a hooked golden beak, a heavy white brow ridge over fierce amber eyes and feather ear-tufts, a shade
# "shingle" chest ruff, a white eagle front with yellow scaly shanks and dark talons, golden lion hindquarters with
# white socks, a feather-fan tail tip, and big 3-row feather wings: white coverts -> sky secondaries -> royal
# primaries with gold tips (wing3 rules: root-axis flap, hinge fold, small sweeps).
# Own moves: idle = snappy bird head-turns with holds, preens under one raised wing; walk = pigeon-style head-bob walk;
# roar = SCREECH (wings flung wide and up, beak gaping); fly / takeoff / land = powered strokes, talons tucked, hind
# legs trailing; signature = TALON STRIKE (springs up on big beats, hovers, dives talons-first into the ground).
import math
from mathutils import Vector, Euler, Matrix
import wing3

DISPLAY = "Griffin"
MOTION = "Fly"
RIG = "wingquad"
HEIGHT = 9.0

WHITE = (246, 246, 250)
SHADE = (210, 214, 230)
TALON = (40, 40, 50)
GOLD_F = (226, 160, 70)       # lion gold
BEAK = (255, 196, 50)
SKY = (120, 170, 255)
ROYAL = (60, 90, 220)
GOLD = (255, 206, 70)         # primary tips
IRIS = (255, 170, 30)
BROW = (52, 58, 92)           # dark slate brow bars on the white ridge (contrast rule)
MOUTH = (150, 60, 50)
DARK = (24, 20, 34)

# hip, knee, ankle (left side); legs 0.70 TH
LEGS = {"FL": ((0.21, -0.36, 0.76), (0.21, -0.47, 0.40), (0.21, -0.36, 0.13)),
        "BL": ((0.17, 0.38, 0.74), (0.17, 0.49, 0.38), (0.17, 0.38, 0.12))}
HC = Vector((0, -0.90, 1.55))                     # cranium centre (HW 0.68 = 0.90 TW, HH 0.60 = 0.86 TH)
# wing designed at 27 deg elevation, bind pose raised a further ELEV deg about the root line (heroic V like ref_20);
# the authored wing keys were tuned on the old 33 deg wing, so wings() subtracts KEY_OFS (= 27 + ELEV - 33).
# The WingTip hinge runs along the wing-plane NORMAL at the wrist, so "tip" sweeps the primaries back IN the wing
# plane (a bird's fold, primaries sliding under the secondaries) instead of flapping them down.
ELEV = 23.0
KEY_OFS = 27.0 + ELEV - 33.0
_S0, _BB0 = Vector((0.38, -0.24, 1.22)), Vector((0.37, 0.34, 1.14))
_ROT = Matrix.Rotation(math.radians(-ELEV), 3, (_BB0 - _S0).normalized())


def _raise(p):
    return _S0 + _ROT @ (Vector(p) - _S0)


_W, _H2, _T = _raise((1.04, -0.12, 1.52)), _raise((0.88, 0.60, 1.24)), _raise((1.98, 0.26, 1.84))
_N = (_T - _W).cross(_H2 - _W).normalized()
if _N.z < 0:
    _N = -_N
WING = wing3.Wing(S=tuple(_S0), W=tuple(_W), H=tuple(_W + _N * 0.30), BB=tuple(_BB0))
H2 = tuple(_H2)                                   # trailing point of the secondaries (geometry only)
TIP = tuple(_T)
TAILP = [(0, 0.60, 1.00), (0, 0.86, 0.95), (0, 1.04, 0.74), (0, 1.12, 0.50)]


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


def frame(z, n):
    """rotation: local z along z, local x = the plane normal n (orthogonalised)"""
    z = Vector(z).normalized()
    x = Vector(n)
    x = (x - z * x.dot(z)).normalized()
    return Matrix((x, z.cross(x), z)).transposed()


def feather(B, root, tip, nrm, width, thick, color, bone, tip_c=None, tip_frac=0.28, **kw):
    """a tapered feather block lying in the wing plane (thin along nrm), pointed at the tip; optional coloured tip"""
    root, tip = Vector(root), Vector(tip)
    R = frame(tip - root, nrm)
    L = (tip - root).length
    B.add((root + tip) / 2, (thick / 2, width / 2, L / 2), color, bone, R=R, top=(1.0, 0.25), studs=[],
          role="limb", **kw)
    if tip_c:
        c0 = tip - (tip - root) * tip_frac
        B.add((c0 + tip) / 2 + R @ Vector((0.004, 0, 0)), (thick / 2 + 0.004, width / 2 * (1 - 0.75 * (1 - tip_frac)),
              L * tip_frac / 2), tip_c, bone, R=R, top=(1.0, 0.25 / (1 - 0.75 * (1 - tip_frac))), studs=[],
              role="limb", **kw)


def wing(B, s, side):
    """STYLE_BIBLE 2d feather wing, all feathers in ONE plane (projected) and stacked in layers along its normal:
    sky secondaries (-), white coverts (+) on the arm bone; royal primaries with gold tips fanned from the wrist and
    white hand coverts ON TOP on the tip bone, so the primaries sweep back over the inner wing when folding."""
    S0, W, H, bb = X(WING.S, s), X(WING.W, s), X(H2, s), X(WING.BB, s)
    T = X(TIP, s)
    wb, tb = "Wing_" + side, "WingTip_" + side
    nrm = (T - W).cross(H - W).normalized()
    if nrm.z < 0:
        nrm = -nrm

    def pl(p):                                     # project onto the wing plane through the wrist
        p = Vector(p)
        return p - nrm * (p - W).dot(nrm)

    S, H, bb = pl(S0), pl(H), pl(bb)
    # arm bar (white, chunky) from the shoulder joint + wrist knuckle + hand bar
    B.seg(S0, W, 0.055, 0.08, WHITE, wb, side=nrm, ext=0.06, role="limb", studs=[])
    B.add(W, (0.06, 0.08, 0.08), WHITE, wb, R=frame(W - S, nrm), studs=[], role="limb")
    B.seg(W + nrm * 0.085, W.lerp(T, 0.30) + nrm * 0.085, 0.03, 0.06, WHITE, tb, side=nrm, studs=[], role="limb")
    # secondaries (sky): 7 broad feathers rooted along the arm, reaching back past the trailing edge (saw edge)
    n_sec = 7
    for i in range(n_sec):
        t = (i + 0.5) / n_sec
        a = S.lerp(W, 0.05 + 0.92 * t)
        end = bb.lerp(H, t)
        d = end - a
        end = end + d.normalized() * (0.09 + 0.05 * ((i % 2) * 2 - 1))
        feather(B, a - nrm * 0.02, end - nrm * 0.02, nrm, 0.21, 0.045, SKY, wb)
    # coverts (white): 6 broad short feathers over the secondaries' roots
    for i in range(6):
        t = (i + 0.5) / 6
        a = S.lerp(W, 0.03 + 0.94 * t)
        end = a.lerp(bb.lerp(H, t), 0.52)
        feather(B, a + nrm * 0.026, end + nrm * 0.026, nrm, 0.22, 0.045, WHITE, wb)
    # inner primaries (royal, gold tips) on the ARM bone at the secondaries' layer: they fill the spread wing
    # between the secondaries and the hand and stay with the inner wing when it folds
    for i, (t, f) in enumerate(((0.12, 0.70), (0.32, 0.78), (0.50, 0.84))):
        dv = (H - W).normalized().lerp((T - W).normalized(), t).normalized()
        ln = (T - W).length * f
        feather(B, W + dv * 0.05 - nrm * 0.02, W + dv * ln - nrm * 0.02, nrm, 0.22, 0.045, ROYAL, wb, tip_c=GOLD)
    # outer primaries (royal, gold tips): 5 broad feathers in a tight fan from the wrist, one layer above the
    # coverts on the tip bone: they sweep back over the inner wing into a closed bundle when folding
    n_pri = 5
    for i in range(n_pri):
        t = i / (n_pri - 1)
        dv = (H - W).normalized().lerp((T - W).normalized(), 0.64 + 0.36 * t).normalized()
        ln = (T - W).length * (0.90 + 0.10 * t) * (1.0 + 0.04 * ((i % 2) * 2 - 1))
        o = nrm * (0.085 + 0.005 * (n_pri - 1 - i))
        feather(B, W + dv * 0.05 + o, W + dv * ln + o, nrm, 0.22, 0.045, ROYAL, tb, tip_c=GOLD)
    # hand coverts (white) on top of the primaries' roots
    for i in range(4):
        t = (i + 0.5) / 4
        dv = (H - W).normalized().lerp((T - W).normalized(), 0.62 + 0.38 * t).normalized()
        o = nrm * 0.15
        feather(B, W + dv * 0.03 + o, W + dv * 0.40 + o, nrm, 0.21, 0.045, WHITE, tb)


def model(k):
    """STYLE_BIBLE Griffin (T6 Celestial, winged quad, fierce-noble): one torso (white eagle chest 20 % bigger than the
    gold lion hips), a big white eagle head (HW 0.90 TW, HH 0.86 TH) with a hooked golden beak, a heavy white brow
    ridge with dark slate brow bars over fierce amber eyes, 3 feather ear-tufts per side, a shade shingle chest ruff,
    eagle forelegs (white feathered thighs, yellow scaly shanks, 4 dark talons), lion hind legs with white socks and
    claw nubs, a lion tail ending in a flat feather fan, 3-row feather wings (span 2.8 x body length).
    No glow (sparkles = particle VFX in Studio)."""
    import blockkit as bk
    B = bk.Blocks(k, seed=157, tier=6)
    D = 0.62
    # ---- one torso: white eagle chest (20 % bigger) overlapping the gold lion hips by 43 %
    chest = B.add((0, -0.18, 0.83), (0.38, 0.42, 0.35), WHITE, "Chest", bot=(0.90, 0.95), density=0.7)
    B.add((0, 0.28, 0.80), (0.32, 0.35, 0.29), GOLD_F, "Spine", bot=(0.88, 0.92), density=0.7)
    # shingle chest ruff: 3 brick rows of down-pointing shade feathers, lower edges proud (ref_09)
    for r, (z, xs) in enumerate(((1.02, (-0.21, -0.07, 0.07, 0.21)), (0.88, (-0.14, 0.0, 0.14)),
                                 (0.74, (-0.07, 0.07)))):
        for x in xs:
            yf = -0.18 - 0.42 * (0.95 + 0.05 * (z - 0.48) / 0.70)
            B.add((x, yf - 0.012, z), (0.068, 0.022, 0.085), SHADE, "Chest", rot=(-20, 0, 0), bot=(0.15, 1.0),
                  studs=[], role="limb")
    # ---- neck: white, thick, with a ruff of shade feathers fanning down over the chest top
    B.seg((0, -0.46, 1.04), (0, -0.80, 1.45), 0.26, 0.21, WHITE, "Neck", side=(1, 0, 0), ext=0.06, studs=["+x", "-x"])
    for x, ln in ((-0.20, 0.20), (0.0, 0.24), (0.20, 0.20)):
        B.spike((x, -0.66, 1.25), (x * 0.8, -0.35, -1), ln, 0.075, SHADE, "Neck", top=(0.3, 0.6))
    # ---- head: big white eagle cranium (faces -y), ear tufts, beak below the eye band
    head = B.add(HC, (0.34, 0.23, 0.30), WHITE, "Head", top=(0.94, 0.94), density=0.8, studs=["+x", "-x", "+z", "+y"])
    # upper beak: tapered forward, golden, with a hooked tip; dark nostril slits on the cere
    beak = B.add(HC + Vector((0, -0.28, -0.12)), (0.15, 0.10, 0.17), BEAK, "Head", rot=(90, 0, 0), top=(0.55, 0.62),
                 studs=[], role="limb")
    B.spike(HC + Vector((0, -0.42, -0.07)), (0, -0.45, -1), 0.17, 0.055, BEAK, "Head", top=(0.25, 0.3))
    for s in (1, -1):
        B.add(HC + Vector((s * 0.06, -0.31, -0.040)), (0.026, 0.016, 0.008), DARK, "Head", rot=(0, 0, s * 20),
              studs=[], bevel=0.004)
    B.add(HC + Vector((0, -0.30, -0.226)), (0.11, 0.12, 0.006), MOUTH, "Head", studs=[], bevel=0.004)
    # lower beak (opens in the screech)
    B.add(HC + Vector((0, -0.30, -0.255)), (0.11, 0.12, 0.035), BEAK, "Jaw", bot=(0.8, 0.8), role="limb", studs=[])
    B.add(HC + Vector((0, -0.30, -0.218)), (0.09, 0.10, 0.004), MOUTH, "Jaw", studs=[], bevel=0.003)
    # fierce amber eyes (iris ring all round the pupil, 1 highlight); the brows are bars on the white ridge below
    B.face_eyes(head, "fierce", IRIS, base=WHITE, brow=None, look=(0, 0.6), pupil_size=(0.09, 0.095),
                hl_size=(0.07, 0.0), hl_on_pupil=True)
    # heavy white brow ridge (20 deg, inner end down) with a dark slate brow bar on its front face
    for s in (1, -1):
        ang = -s * 20
        R = Euler((0, math.radians(ang), 0), "XYZ").to_matrix()
        c = HC + Vector((s * 0.165, -0.245, 0.175))
        ridge = B.add(c, (0.13, 0.05, 0.045), WHITE, "Head", R=R, top=(1.0, 0.7), studs=[], role="limb")
        B.add(ridge.world((0, -0.052, -0.012)), (0.125, 0.006, 0.026), BROW, "Head", R=R, studs=[], bevel=0.006)
    # ear tufts: 3 feathers per side fanned from the top-back corner (white, shade, white)
    for s in (1, -1):
        root = HC + Vector((s * 0.25, 0.10, 0.24))
        for dv, ln, c in (((s * 0.25, 0.45, 1.0), 0.26, WHITE), ((s * 0.65, 0.55, 0.65), 0.22, SKY),
                          ((s * 0.05, 0.85, 0.60), 0.20, SHADE)):
            B.spike(root, dv, ln, 0.07, c, "Head", side=(0, 1, 0), top=(0.2, 0.55))
        # cheek ruff: 3 shade blades fanned back from the lower back edge of the head (extends the silhouette)
        for z, dz, L in ((-0.22, -0.55, 0.20), (-0.12, -0.20, 0.24), (-0.02, 0.15, 0.19)):
            root = HC + Vector((s * 0.31, 0.10, z))
            d = Vector((s * 0.55, 0.65, dz)).normalized()
            B.seg(root, root + d * L, 0.085, 0.04, SHADE, "Head", side=(0, 0, 1), ext=0.06, top=(0.15, 0.5),
                  studs=[], role="limb")
    # ---- feathered wings
    for s, side in ((1, "L"), (-1, "R")):
        wing(B, s, side)
    # ---- legs: eagle forelegs (white feathered thigh + fringe, yellow scaly shank, 4 talons), lion hind legs
    for s, side in ((1, "L"), (-1, "R")):
        for fb in ("F", "B"):
            H, K, A = (X(p, s) for p in LEGS[fb + "L"])
            leg, shin, foot = "Leg_" + fb + side, "Shin_" + fb + side, "Foot_" + fb + side
            if fb == "F":
                B.seg(H - Vector((0, 0, 0.02)), K, 0.13, 0.14, WHITE, leg, ext1=0.06, bot=(0.92, 0.92), density=D)
                for dx in (-0.08, 0.0, 0.08):          # feather fringe over the shank top
                    B.spike(K + Vector((s * dx, -0.03, 0.06)), (s * dx * 0.6, -0.25, -1), 0.13, 0.055, WHITE, leg,
                            top=(0.25, 0.5))
                B.seg(K, A, 0.095, 0.10, BEAK, shin, ext=0.04, ext1=0.03, studs=[], role="limb")
                for z in (0.20, 0.28):                 # scale bands
                    B.add(A + Vector((0, 0, z - 0.13)), (0.099, 0.104, 0.012), (232, 168, 40), shin, studs=[],
                          bevel=0.006)
                B.add(A + Vector((0, -0.02, -0.075)), (0.11, 0.11, 0.05), BEAK, foot, studs=[], role="limb")
                for dx in (-0.075, 0.0, 0.075):
                    tb = A + Vector((dx, -0.11, -0.085))
                    B.seg(A + Vector((dx * 0.6, -0.04, -0.085)), tb, 0.032, 0.035, BEAK, foot, studs=[], role="limb")
                    B.spike(tb + Vector((0, -0.02, 0)), (0, -1, -0.9), 0.09, 0.03, TALON, foot, top=(0.15, 0.15))
                B.spike(A + Vector((0, 0.08, -0.07)), (0, 1, -0.8), 0.09, 0.03, TALON, foot, top=(0.15, 0.15))
            else:
                B.seg(H - Vector((0, 0, 0.02)), K, 0.135, 0.16, GOLD_F, leg, ext1=0.06, bot=(0.92, 0.92), density=D)
                sw, sd = 0.135 * 0.92, 0.16 * 0.92
                B.seg(K, A, sw, sd, GOLD_F, shin, ext=0.05, ext1=0.02, density=D)
                dn = (A - K).normalized()
                B.seg(A - dn * 0.12, A + dn * 0.02, sw * 1.03, sd * 1.03, WHITE, shin, studs=[], role="limb")
                paw = B.add(A + Vector((0, -0.03, -0.066)), (0.15, 0.18, 0.056), WHITE, foot, studs=[], role="limb",
                            top=(0.95, 0.92))
                for gx in (-0.08, 0.0, 0.08):
                    B.add(A + Vector((gx, -0.03 - 0.18 - 0.01, -0.09)), (0.022, 0.026, 0.02), TALON, foot, studs=[])
    # ---- lion tail ending in a flat feather fan (royal, gold point) in the side-view plane
    P = [Vector(p) for p in TAILP]
    for i, (a, b) in enumerate(zip(P, P[1:])):
        w = (0.09, 0.075, 0.06)[i]
        B.seg(a, b, w, w, GOLD_F, "Tail%d" % (i + 1), ext=0.05, studs=[], role="limb")
    tip = P[3]
    for dv, ln, wd, c in (((0, 0.35, -1), 0.30, 0.17, ROYAL), ((0, 0.85, -0.55), 0.24, 0.13, SKY),
                          ((0, -0.30, -1), 0.22, 0.12, SKY)):
        dv = Vector(dv).normalized()
        R = frame(dv, (1, 0, 0))
        B.add(tip + dv * (ln / 2), (0.03, wd / 2, ln / 2), c, "Tail3", R=R, top=(1.0, 0.15), studs=[], role="limb")
    B.spike(tip + Vector((0, 0.35, -1)).normalized() * 0.20, (0, 0.35, -1), 0.13, 0.045, GOLD, "Tail3",
            side=(1, 0, 0), top=(0.8, 0.1))
    B.build()
    return {"plates": B.stud_count, "TH": round(B.th, 3), "cell": round(B.pcell, 3)}


def rig(k):
    k.joint("Spine", (0, 0.36, 0.80), "Root", tail=(0, -0.4, 0))
    k.joint("Chest", (0, -0.02, 0.83), "Spine", tail=(0, -0.4, 0))
    k.joint("Neck", (0, -0.46, 1.06), "Chest", tail=(0, -0.28, 0.30))
    k.joint("Head", (0, -0.76, 1.31), "Neck", tail=(0, -0.35, 0))           # throat pivot
    k.joint("Jaw", tuple(HC + Vector((0, -0.19, -0.24))), "Head", tail=(0, -0.2, 0))
    for s, side in ((1, "L"), (-1, "R")):
        k.joint("Wing_" + side, X(WING.S, s), "Chest")
        k.joint("WingTip_" + side, X(WING.W, s), "Wing_" + side, tail=(s * 0.6, 0.2, 0.1))
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
FOLD = dict(up=42, fwd=-5, twist=0, tip=82)         # fold-searched: wings raised heraldic-style (75 deg), primaries
                                                    # swept back over the inner wing (bind-relative up = 42 - KEY_OFS)


def wings(k, f, up, fwd=0.0, twist=0.0, tip=0.0, side=None):
    WING.key(k, f, up - KEY_OFS, fwd, twist, tip, side=side)      # keys are in the old wing's elevation frame


def folded(k, f, du=0.0, dfwd=0.0, dtip=0.0, side=None):
    wings(k, f, FOLD["up"] + du, FOLD["fwd"] + dfwd, FOLD["twist"], FOLD["tip"] + dtip, side)


def tail(k, f, n, sway=8.0, lift=0.0, cycles=2):
    for i, bn in enumerate(TAIL):
        k.key(bn, f, rot=(lift + 3 * i, sway * (0.6 + 0.3 * i) * pk.wave(f, n, 0.15 * i, cycles), 0))


def rest_keys(k, f, z=0.0, pitch=0.0):
    k.key("Spine", f, rot=(pitch, 0, 0), loc=(0, 0, z))
    k.key("Chest", f, rot=(0, 0, 0))
    k.key("Neck", f, rot=(0, 0, 0), loc=(0, 0, 0))
    k.key("Head", f, rot=(0, 0, 0))
    k.key("Jaw", f, rot=(0, 0, 0))
    folded(k, f)
    for b in TAIL:
        k.key(b, f, rot=(0, 0, 0))


def plant_frames(k, frames, legs=LEGS4):
    import bpy
    k.bake_bezier_now()
    for f in frames:
        bpy.context.scene.frame_set(f)
        for leg in legs:
            k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, 0.0)))


# ---- flight
PITCH = 14.0


def fly_legs(k, f, ph, amt=1.0):
    for leg in LEGS4:
        fr = leg[4] == "F"
        side = leg[5:]
        s = 1 if side.endswith("L") else -1
        w = math.sin(2 * math.pi * (ph - (0.15 if fr else 0.3)))
        if fr:       # eagle talons pulled up under the chest
            k.key(leg, f, rot=(amt * (-50 + 6 * w), 0, 0))
            k.key("Shin_" + side, f, rot=(amt * (110 + 8 * w), 0, 0))
            k.key("Foot_" + side, f, rot=(amt * 40, 0, 0))
        else:        # lion hind legs trailing back
            k.key(leg, f, rot=(amt * (28 + 8 * w), 0, 0))
            k.key("Shin_" + side, f, rot=(amt * (-6 + 8 * w), 0, 0))
            k.key("Foot_" + side, f, rot=(amt * 50, 0, 0))


def fly_pose(k, f, ph, legs=True):
    w = wing3.stroke(ph, bot=-40)
    wings(k, f, w["up"], w["fwd"], w["twist"], w["tip"])
    k.key("Spine", f, rot=(PITCH - 3 * math.sin(2 * math.pi * (ph - 0.1)), 0, 0),
          loc=(0, 0, 0.09 * math.cos(2 * math.pi * (ph - 0.45))))
    k.key("Chest", f, rot=(-2 * math.sin(2 * math.pi * (ph - 0.2)), 0, 0))
    k.key("Neck", f, rot=(-6 + 3 * math.sin(2 * math.pi * (ph - 0.25)), 0, 0), loc=(0, 0, 0))
    k.key("Head", f, rot=(-8 - 4 * math.sin(2 * math.pi * (ph - 0.32)), 0, 0))
    k.key("Jaw", f, rot=(0, 0, 0))
    for i, b in enumerate(TAIL):
        k.key(b, f, rot=(-4 + 5 * math.sin(2 * math.pi * (ph - 0.3 - 0.12 * i)), 3 * math.sin(2 * math.pi * (ph - 0.2 * i)), 0))
    if legs:
        fly_legs(k, f, ph)


def fly(k):
    n = 26
    k.new_action("fly", n, True)
    for f in range(0, n + 1):
        fly_pose(k, f, f / n)
    k.finish()


def takeoff(k):
    """crouch with the wings opening high, LAUNCH (frame 11) on a huge downstroke, legs push then tuck"""
    n = 30
    k.new_action("takeoff", n, False)
    rest_keys(k, 0)
    for f, z, p, w in ((5, -0.10, 6, (8, -10, -8, 60)), (10, -0.20, 8, (wing3.TOP if hasattr(wing3, "TOP") else 36, -2, -8, -6)),
                       (13, 0.08, 10, (-12, 8, 12, -10)), (16, 0.12, 12, (-46, 6, 4, 6))):
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(2, 0, 0))
        k.key("Neck", f, rot=(-8, 0, 0), loc=(0, 0, 0))
        k.key("Head", f, rot=(-6, 0, 0))
        k.key("Jaw", f, rot=(0, 0, 0))
        wings(k, f, *w)
        for b in TAIL:
            k.key(b, f, rot=(-4, 0, 0))
    fly_pose(k, 23, 0.0)
    fly_pose(k, n, 0.45)
    plant_frames(k, range(0, 12))
    for f, a in ((15, 0.5), (19, 0.9)):
        fly_legs(k, f, 0.0, a)
    k.finish(loop=False)
    k.events["takeoff"] = {"launch": round(11 / n, 3)}


def land(k):
    """flares upright with braking beats, legs swing down and reach, touches (frame 17), absorbs, folds the wings"""
    n = 30
    k.new_action("land", n, False)
    fly_pose(k, 0, 0.0)
    for f, p, z, w in ((6, 4, 0.06, (20, 18, -14, -4)), (10, -8, 0.10, (-18, 22, -14, 6)), (13, -8, 0.08, (18, 16, -10, -6)),
                       (15, -4, 0.04, (0, 8, -6, 10))):
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(-2, 0, 0))
        k.key("Neck", f, rot=(-4, 0, 0), loc=(0, 0, 0))
        k.key("Head", f, rot=(-4, 0, 0))
        k.key("Jaw", f, rot=(0, 0, 0))
        wings(k, f, *w)
        for b in TAIL:
            k.key(b, f, rot=(8, 0, 0))
    for f, a in ((6, 0.6), (11, 0.2)):
        fly_legs(k, f, 0.0, a)
    for f, z, p, w in ((17, -0.16, 6, (10, -6, 0, 40)), (21, -0.08, 3, (28, -4, -4, 80)), (26, 0.0, 0, None)):
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(1, 0, 0))
        k.key("Neck", f, rot=(p * 0.5, 0, 0), loc=(0, 0, 0))
        k.key("Head", f, rot=(-p * 0.3, 0, 0))
        k.key("Jaw", f, rot=(0, 0, 0))
        if w:
            wings(k, f, *w)
        else:
            folded(k, f)
        for b in TAIL:
            k.key(b, f, rot=(-2, 0, 0))
    rest_keys(k, n)
    plant_frames(k, range(17, n + 1))
    k.finish(loop=False)
    k.events["land"] = {"touch": round(17 / n, 3)}


# ---- ground
def idle(k):
    """noble sentinel: SNAPPY bird head-turns (quick turn, long hold), cocks its head, then preens: opens the raised
    left wing out to the side and reaches its beak under it, folds it back up."""
    n = 150
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 2):
        b = pk.wave(f, n, 0, 4)
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, 0.01 * b))
        k.key("Chest", f, rot=(-0.8 * b, 0, 0))
        tail(k, f, n, sway=8, lift=0, cycles=2)
        k.key("Jaw", f, rot=(0, 0, 0))
    turns = [(0, 0, 0, 0, 0), (14, 0, 0, 0, 0), (16, 0, 34, -2, 0), (34, 0, 34, -2, 0), (36, 0, -30, -2, 0), (52, 0, -30, -2, 0),
             (54, 0, -30, -2, 18), (62, 0, -30, -2, 18), (64, 0, 0, 0, 0), (76, 0, 0, 0, 0),
             (86, 8, 60, 10, 0), (94, 11, 66, 13, 0), (100, 8, 62, 11, 0), (106, 11, 66, 13, 0), (114, 0, 0, 0, 0), (n, 0, 0, 0, 0)]
    for f, nk, ny, h, roll in turns:
        k.key("Neck", f, rot=(nk, 0, 0), loc=(0, 0, 0))              # neck stays square (wing roots beside it)
        k.key("Head", f, rot=(h, ny, roll))
    for f, du, df, dt in ((0, 0, 0, 0), (78, 0, 0, 0), (86, -45, 10, -60), (108, -45, 10, -60), (116, 0, 0, 0), (n, 0, 0, 0)):
        folded(k, f, du, df, dt, side="L")
    for f in (0, n):
        folded(k, f, side="R")
    cm.plant(k, n, legs=LEGS4)
    k.finish()
    k.meta["planted"] = LEGS4


def walk(k):
    """lateral walk with a pigeon-style HEAD BOB: the head thrusts forward and holds still against the body each step."""
    n = 30

    def body(f):
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(0.6 * pk.wave(f, n, 0.1, 2), 1.2 * pk.wave(f, n, 0.0), 1.5 * pk.wave(f, n, 0.0)),
              loc=(0, 0, -0.02 * b))
        k.key("Chest", f, rot=(0, -1.5 * pk.wave(f, n, 0.25), -1.5 * pk.wave(f, n, 0.25)))
        u = (2 * f / n) % 1.0
        bob = (u / 0.3) if u < 0.3 else (1 - (u - 0.3) / 0.7)          # quick thrust forward, slow return
        k.key("Neck", f, rot=(4 * bob, 0, 0), loc=(0, -0.07 * bob, 0))
        k.key("Head", f, rot=(-4 * bob, 0, 0))
        k.key("Jaw", f, rot=(0, 0, 0))
        folded(k, f, du=2 * pk.wave(f, n, 0.3, 2))               # raised wings bob with the steps
        tail(k, f, n, sway=10, lift=0, cycles=1)
    return cm.quad_walk(k, n, 0.15, 0.11, body, gait="walk")


def roar(k):
    """SCREECH: rears its chest up, flings both wings wide and high, thrusts the head forward with the beak gaping,
    holds the screech, folds back."""
    n = 66
    k.new_action("roar", n, False)
    for f, p, z, nk, h, jw, w in ((0, 0, 0, 0, 0, 0, None), (10, 4, -0.04, 6, 6, 2, (6, -10, -8, 70)),
                                  (20, -10, 0.02, -14, 14, 34, (40, 6, -6, -8)), (46, -10, 0.02, -14, 14, 36, (42, 8, -6, -10)),
                                  (56, -2, 0, -2, 2, 4, (16, -10, -8, 60)), (66, 0, 0, 0, 0, 0, None)):
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(0, 0, 0))
        k.key("Neck", f, rot=(nk, 0, 0), loc=(0, -0.06 * (20 <= f <= 46), 0))
        k.key("Head", f, rot=(h, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        if w:
            wings(k, f, *w)
        else:
            folded(k, f)
        for i, b in enumerate(TAIL):
            k.key(b, f, rot=(10 * (20 <= f <= 46), 0, 0))
    for f in range(22, 46, 2):
        k.key("Jaw", f, rot=(35 + (2 if (f // 2) % 2 else -2), 0, 0))
    cm.plant(k, n, legs=LEGS4)
    k.finish(loop=False)


def strike(k):
    """SIGNATURE - TALON STRIKE: crouches, springs straight up on two huge wingbeats, hovers (talons cocked, head down
    locked on the target), then DIVES and drives both talons into the ground, wings mantled; folds and stands."""
    import bpy
    n = 112
    k.new_action("act_strike", n, False)
    # body height/pitch
    for f, z, p in ((0, 0, 0), (8, -0.16, 6), (12, -0.20, 8), (20, 0.50, -6), (30, 0.85, -4), (44, 0.95, 10), (58, 0.95, 12),
                    (68, 0.20, 26), (72, -0.12, 20), (80, -0.14, 18), (92, -0.04, 4), (100, 0, 0), (n, 0, 0)):
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(0, 0, 0))
    for f, nk, h, jw in ((0, 0, 0, 0), (12, 4, 4, 0), (24, -6, -6, 0), (44, 14, 22, 6), (58, 14, 22, 6), (66, 8, 14, 30),
                         (72, 4, 6, 34), (78, 4, 6, 4), (92, 0, 0, 0), (n, 0, 0, 0)):
        k.key("Neck", f, rot=(nk, 0, 0), loc=(0, 0, 0))
        k.key("Head", f, rot=(h, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
    # wings: open, two big beats up, hover beats, swept back for the dive, mantled over the strike, fold
    folded(k, 0)
    wings(k, 10, 34, -2, -8, -6)
    for i, f0 in enumerate((14, 24, 34, 44, 54)):
        for j, ph in enumerate((0.0, 0.45)):
            w = wing3.stroke(ph, bot=-40)
            wings(k, f0 + j * 5, w["up"], w["fwd"], w["twist"], w["tip"])
    wings(k, 64, 12, -4, -8, 50)
    wings(k, 70, 30, 14, -8, 10)
    wings(k, 80, 26, 12, -6, 14)
    wings(k, 92, 30, -4, -6, 80)
    folded(k, 102)
    folded(k, n)
    for f in range(0, n + 1, 2):
        tail(k, f, n, sway=6, lift=-8 if 20 <= f <= 66 else 4, cycles=4)
    k.bake_bezier_now()
    sc = bpy.context.scene
    for f in range(0, n + 1):
        sc.frame_set(f)
        if 14 <= f <= 68:
            u = 1.0 if 20 <= f <= 62 else ((f - 14) / 6 if f < 20 else (68 - f) / 6)
            for leg in LEGS4:
                side = leg[5:]
                if leg[4] == "F":          # talons cocked forward-down for the strike
                    k.key(leg, f, rot=(-30 * u - (24 if f >= 58 else 0) * u, 0, 0))
                    k.key("Shin_" + side, f, rot=(60 * u, 0, 0))
                    k.key("Foot_" + side, f, rot=(-10 * u, 0, 0))
                else:
                    k.key(leg, f, rot=(40 * u, 0, 0))
                    k.key("Shin_" + side, f, rot=(-20 * u, 0, 0))
                    k.key("Foot_" + side, f, rot=(40 * u, 0, 0))
        else:
            for leg in LEGS4:
                k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, 0.0)))
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    fly(k)
    takeoff(k)
    land(k)
    roar(k)
    strike(k)
    return stride


def check_pairs():
    W = ["Wing_L", "WingTip_L", "Wing_R", "WingTip_R"]
    P = [("Wing_L", "WingTip_L"), ("Wing_R", "WingTip_R"), ("WingTip_L", "WingTip_R"), ("Wing_L", "Wing_R"),
         ("WingTip_L", "Wing_R"), ("Wing_L", "WingTip_R")]
    for w in W:
        for b in ("Head", "Neck", "Tail1", "Tail2", "Tail3", "Leg_BL", "Leg_BR", "Shin_BL", "Shin_BR", "Leg_FL", "Leg_FR"):
            P.append((w, b))
    P += [("Leg_FL", "Leg_BL"), ("Leg_FR", "Leg_BR"), ("Leg_FL", "Leg_FR"), ("Leg_BL", "Leg_BR"),
          ("Shin_FL", "Shin_FR"), ("Shin_BL", "Shin_BR"), ("Shin_FL", "Shin_BL"), ("Shin_FR", "Shin_BR")]
    for a in ("Head", "Jaw"):
        for b in ("Leg_FL", "Leg_FR", "Shin_FL", "Shin_FR", "Foot_FL", "Foot_FR"):
            P.append((a, b))
    P.append(("Head", "Chest"))
    for w in W:                                     # the raised fold and the strokes must stay clear of the torso
        P += [(w, "Chest"), (w, "Spine")]
    return P


def joints():
    """wrist knuckle + hinge (wing3) and the shoulder: the arm root turns about the root line inside the chest edge"""
    out = WING.joints()
    for s, sd in ((1, "L"), (-1, "R")):
        out.append((X(WING.S, s), X(WING.BB, s), 0.12, "Wing_" + sd))
    return out
