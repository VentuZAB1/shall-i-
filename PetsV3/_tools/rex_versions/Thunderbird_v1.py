# Thunderbird (Storm egg, NEW 5% pet, 2026-10-14) - FIERCE style "the storm herald": a giant thunder eagle built from
# tapered blocks under a Roblox stud skin, in the family of our approved pets (Griffin's 3-row feather wing + eagle head,
# Storm Wyvern's raptor biped stance and flight clips): a deep storm-TEAL body leaning 35 deg forward, a white bald-eagle
# head + neck ruff with a swept-back war-bonnet crest, a big gold hooked beak, narrow yellow eyes under heavy dark brows,
# huge 3-row feather wings whose primaries end in electric-yellow lightning tips, a fanned tail with yellow tips,
# feathered trousers, scaly gold shanks and black talons. No glow (lightning = Studio VFX).
import math
from mathutils import Vector, Euler, Matrix
import wing3

DISPLAY = "Thunderbird"
MOTION = "Fly"
RIG = "wingbiped"
HEIGHT = 8.5

# Blender colours (Roblox renders ~0.6x darker)
BODY = (46, 112, 172)        # storm teal
BODY_D = (28, 64, 110)       # back, wing secondaries, tail base
COVERT = (70, 140, 196)      # light wing row
PRIMARY = (24, 44, 84)       # dark primaries
WHITE = (236, 240, 248)      # head, neck ruff, chest shingles
WHITE_D = (196, 206, 224)    # shingle shading rows
GOLD = (255, 184, 40)        # beak, cere, shanks, feet
GOLD_D = (214, 134, 24)      # scale bands, beak shade
BOLT = (255, 226, 40)        # accent: lightning feather tips, crest tips, eyes
BOLT_HOT = (255, 250, 200)
BROW = (30, 50, 84)
BLACK = (14, 14, 22)
MOUTH = (96, 26, 30)

H_MODEL = 1.80
PITCH = round(0.042 * (H_MODEL / HEIGHT) / (1.498 / 8.0), 4)

HIP, KNEE, ANKLE, TOE = (0.15, 0.16, 0.62), (0.17, -0.10, 0.42), (0.16, 0.05, 0.17), (0.16, -0.04, 0.035)
HC = Vector((0, -0.40, 1.56))                      # cranium centre
TAILP = [(0, 0.24, 0.70), (0, 0.50, 0.56), (0, 0.80, 0.44)]

# wing: designed flat, raised ELEV deg about the root line for the bind pose (Griffin recipe)
ELEV = 16.0
_S0, _BB0 = Vector((0.20, -0.10, 1.16)), Vector((0.17, 0.22, 0.98))
_ROT = Matrix.Rotation(math.radians(-ELEV), 3, (_BB0 - _S0).normalized())


def _raise(p):
    return _S0 + _ROT @ (Vector(p) - _S0)


_W, _H2, _T = _raise((0.86, -0.04, 1.32)), _raise((0.72, 0.62, 1.12)), _raise((1.72, 0.30, 1.42))
_N = (_T - _W).cross(_H2 - _W).normalized()
if _N.z < 0:
    _N = -_N
WING = wing3.Wing(S=tuple(_S0), W=tuple(_W), H=tuple(_W + _N * 0.30), BB=tuple(_BB0))
H2 = tuple(_H2)
TIP = tuple(_T)


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


def frame(z, n):
    z = Vector(z).normalized()
    x = Vector(n)
    x = (x - z * x.dot(z)).normalized()
    return Matrix((x, z.cross(x), z)).transposed()


def feather(B, root, tip, nrm, width, thick, color, bone, taper=0.22, tipc=None, tipf=0.30):
    """flat tapered feather in the wing plane; tipc = a lightning-coloured tip (last tipf of the length)"""
    root, tip = Vector(root), Vector(tip)
    R = frame(tip - root, nrm)
    L = (tip - root).length
    if tipc is None:
        return B.add((root + tip) / 2, (thick / 2, width / 2, L / 2), color, bone, R=R, top=(1.0, taper),
                     role="limb", bevel=0.008)
    m = root.lerp(tip, 1 - tipf)
    B.add((root + m) / 2 + (tip - root).normalized() * 0.01, (thick / 2, width / 2, (m - root).length / 2 + 0.01), color,
          bone, R=R, top=(1.0, 0.82), role="limb", bevel=0.008)
    w2 = width * 0.82
    B.add((m + tip) / 2, (thick / 2 + 0.002, w2 / 2, (tip - m).length / 2), tipc, bone, R=R, top=(1.0, taper / 0.82),
          role="limb", bevel=0.006, studs=[], nostud=True)


def wing(B, s, side):
    """Griffin's 3-row wing: coverts (light) over secondaries (dark) on the arm; primaries with lightning tips fanned
    from the wrist (outer ones on the tip bone)."""
    S0, W, H, bb = X(WING.S, s), X(WING.W, s), X(H2, s), X(WING.BB, s)
    T = X(TIP, s)
    wb, tb = "Wing_" + side, "WingTip_" + side
    nrm = (T - W).cross(H - W).normalized()
    if nrm.z < 0:
        nrm = -nrm

    def pl(p):
        p = Vector(p)
        return p - nrm * (p - W).dot(nrm)

    S, H, bb = pl(S0), pl(H), pl(bb)
    B.seg(S0, W, 0.055, 0.09, COVERT, wb, side=nrm, ext=0.05, role="limb")
    B.add(W, (0.055, 0.07, 0.07), COVERT, wb, R=frame(W - S, nrm), role="limb")
    B.seg(W + nrm * 0.078, W.lerp(T, 0.28) + nrm * 0.078, 0.028, 0.052, COVERT, tb, side=nrm, role="limb")
    n_sec = 7
    for i in range(n_sec):
        t = (i + 0.5) / n_sec
        a = S.lerp(W, 0.04 + 0.92 * t)
        end = bb.lerp(H, t)
        d = end - a
        end = end + d.normalized() * (0.07 + 0.04 * ((i % 2) * 2 - 1))
        feather(B, a - nrm * 0.016, end - nrm * 0.016, nrm, 0.27, 0.034, BODY_D, wb, taper=0.35, tipc=WHITE, tipf=0.18)
    for i in range(6):
        t = (i + 0.5) / 6
        a = S.lerp(W, 0.03 + 0.94 * t)
        end = a.lerp(bb.lerp(H, t), 0.50)
        feather(B, a + nrm * 0.02, end + nrm * 0.02, nrm, 0.22, 0.034, COVERT, wb, taper=0.5)
    for i, (t, f) in enumerate(((0.12, 0.68), (0.32, 0.78), (0.50, 0.86))):
        dv = (H - W).normalized().lerp((T - W).normalized(), t).normalized()
        ln = (T - W).length * f
        feather(B, W + dv * 0.04 - nrm * 0.016, W + dv * ln - nrm * 0.016, nrm, 0.25, 0.034, PRIMARY, wb, taper=0.3,
                tipc=BOLT, tipf=0.26)
    n_pri = 5
    for i in range(n_pri):
        t = i / (n_pri - 1)
        dv = (H - W).normalized().lerp((T - W).normalized(), 0.66 + 0.34 * t).normalized()
        ln = (T - W).length * (0.92 + 0.10 * t) * (1.0 + 0.04 * ((i % 2) * 2 - 1))
        o = nrm * (0.065 + 0.004 * (n_pri - 1 - i))
        feather(B, W + dv * 0.04 + o, W + dv * ln + o, nrm, 0.23, 0.034, PRIMARY, tb, taper=0.28, tipc=BOLT,
                tipf=0.28)
    for i in range(4):
        t = (i + 0.5) / 4
        dv = (H - W).normalized().lerp((T - W).normalized(), 0.60 + 0.40 * t).normalized()
        o = nrm * 0.11
        feather(B, W + dv * 0.03 + o, W + dv * 0.36 + o, nrm, 0.20, 0.034, COVERT, tb, taper=0.5)


def eye(B, c, s, yaw=26, bone="Head", sc=1.0):
    R = Euler((0, math.radians(-s * 18), math.radians(s * yaw)), "XYZ").to_matrix()
    c = Vector(c)
    B.add(c, (0.05 * sc, 0.008, 0.026 * sc), BLACK, bone, R=R, studs=[], role="detail", bevel=0.004)
    B.add(c + R @ Vector((0.002 * s, -0.006, -0.002)), (0.042 * sc, 0.006, 0.014 * sc), BOLT, bone, R=R, studs=[],
          role="detail", bevel=0.003)
    B.add(c + R @ Vector((s * 0.016 * sc, -0.010, 0.0)), (0.017 * sc, 0.004, 0.006 * sc), BOLT_HOT, bone, R=R,
          studs=[], role="detail", bevel=0.002)


def model(k):
    import blockkit as bk
    B = bk.Blocks(k, seed=211, tier=3, plates=False)
    # ---------------- torso: deep keeled breast leaning forward, tucked belly, narrower rump over the legs
    B.add((0, -0.06, 1.02), (0.25, 0.22, 0.26), BODY, "Chest", rot=(32, 0, 0), bot=(0.62, 0.58), top=(0.92, 0.92),
          rnd=0.38)
    B.add((0, 0.14, 0.74), (0.19, 0.18, 0.16), BODY, "Spine", rot=(32, 0, 0), top=(0.92, 0.9), bot=(0.78, 0.72),
          rnd=0.36)
    B.add((0, 0.10, 1.10), (0.16, 0.22, 0.04), BODY_D, "Chest", rot=(32, 0, 0), top=(0.7, 0.85))          # dark back
    # white shingle breast: 3 brick rows of down-pointing feathers (Griffin chest ruff)
    for r, (z, xs) in enumerate(((1.14, (-0.15, -0.05, 0.05, 0.15)), (1.00, (-0.10, 0.0, 0.10)),
                                 (0.87, (-0.05, 0.05)))):
        for x in xs:
            B.add((x, -0.255 + 0.075 * r, z), (0.06, 0.02, 0.075), WHITE if r < 2 else WHITE_D, "Chest",
                  rot=(14, 0, 0), bot=(0.2, 1.0), role="detail", bevel=0.008)
    # feather skirt over the thighs (sides)
    for s in (1, -1):
        for z, L in ((0.86, 0.16), (0.74, 0.18), (0.62, 0.15)):
            B.spike((s * 0.16, 0.06, z), (s * 0.3, 0.7, -0.5), L, 0.06, BODY, "Spine", side=(s, 0, 0), top=(0.2, 0.3))
    # ---------------- neck: white ruff of swept feathers (bald-eagle head)
    B.seg((0, -0.16, 1.18), (0, -0.30, 1.46), 0.15, 0.15, WHITE, "Neck", ext=0.05, ext1=0.03, top=(0.88, 0.9))
    for s in (1, -1):
        for y, z, L in ((-0.30, 1.42, 0.16), (-0.24, 1.32, 0.18), (-0.18, 1.22, 0.16)):
            B.spike((s * 0.12, y, z), (s * 0.45, 0.8, -0.35), L, 0.055, WHITE, "Neck", top=(0.12, 0.35))
    for y, z, L in ((-0.20, 1.44, 0.16), (-0.12, 1.32, 0.17)):                                    # nape hackles
        B.spike((0, y, z), (0, 0.85, -0.2), L, 0.07, WHITE_D, "Neck", top=(0.15, 0.4))
    # ---------------- eagle head (throat pivot): white cranium, gold cere + big hooked beak, dark brow ridges
    B.add(HC, (0.135, 0.13, 0.115), WHITE, "Head", top=(0.85, 0.85))
    B.add(HC + Vector((0, -0.10, -0.045)), (0.10, 0.06, 0.075), WHITE, "Head", top=(0.9, 1))
    B.add(HC + Vector((0, -0.165, -0.015)), (0.072, 0.035, 0.036), GOLD, "Head", top=(0.85, 1))          # cere
    for s in (1, -1):
        B.add(HC + Vector((s * 0.073, -0.17, -0.005)), (0.004, 0.010, 0.007), BLACK, "Head", studs=[],
              role="detail", bevel=0.003)
    B.seg(HC + Vector((0, -0.16, -0.012)), HC + Vector((0, -0.30, -0.035)), 0.066, 0.058, GOLD, "Head",
          top=(0.6, 0.6), ext=0.0)
    B.seg(HC + Vector((0, -0.26, -0.005)), HC + Vector((0, -0.325, -0.05)), 0.038, 0.044, GOLD_D, "Head",
          top=(0.8, 0.8), ext=0.01)
    B.spike(HC + Vector((0, -0.315, -0.04)), (0, -0.25, -1), 0.11, 0.034, GOLD_D, "Head", top=(0.15, 0.2))
    B.add(HC + Vector((0, -0.22, -0.068)), (0.052, 0.07, 0.005), MOUTH, "Head", studs=[], role="detail", bevel=0.003)
    for s in (1, -1):
        B.add(HC + Vector((s * 0.062, -0.20, -0.06)), (0.004, 0.06, 0.007), MOUTH, "Head", rot=(-8, 0, 0), studs=[],
              role="detail", bevel=0.002)
    B.seg(HC + Vector((0, -0.14, -0.088)), HC + Vector((0, -0.28, -0.09)), 0.052, 0.02, GOLD, "Jaw", top=(0.7, 1),
          ext=0.02)
    for s in (1, -1):
        eye(B, HC + Vector((s * 0.10, -0.128, 0.022)), s, sc=1.1)
        B.add(HC + Vector((s * 0.080, -0.118, 0.072)), (0.088, 0.047, 0.032), BROW, "Head",
              rot=(0, -s * 20, s * 22), role="detail", bevel=0.012)
    # war-bonnet crest: 5 long feathers swept back from the crown, white with lightning-yellow tips
    for x, L, up in ((0.0, 0.34, 0.55), (0.05, 0.30, 0.42), (-0.05, 0.30, 0.42), (0.095, 0.24, 0.28),
                     (-0.095, 0.24, 0.28)):
        root = HC + Vector((x, 0.02, 0.10))
        d = Vector((x * 1.6, 1.0, up)).normalized()
        m = root + d * L * 0.68
        B.seg(root, m, 0.03, 0.022, WHITE, "Head", side=(1, 0, 0), ext=0.02, top=(0.9, 0.9), role="limb")
        B.spike(m - d * 0.01, d, L * 0.34, 0.028, BOLT, "Head", side=(1, 0, 0), top=(0.15, 0.3), nostud=True)
    # ---------------- feathered wings
    for s, side in ((1, "L"), (-1, "R")):
        wing(B, s, side)
    # ---------------- raptor legs: feathered trousers, scaly gold shanks, 3 talons forward + 1 back
    for s, side in ((1, "L"), (-1, "R")):
        H, K, A, T = X(HIP, s), X(KNEE, s), X(ANKLE, s), X(TOE, s)
        B.seg(H + Vector((0, 0.03, 0.08)), K, 0.11, 0.14, BODY, "Leg_" + side, ext=0.0, ext1=0.04, top=(0.75, 0.65),
              rnd=0.4)                                                                                  # trousers
        for dx in (-0.06, 0.0, 0.06):
            B.spike(K + Vector((s * dx, -0.02, 0.06)), (s * dx * 0.8, -0.1, -1), 0.12, 0.045, BODY, "Leg_" + side,
                    top=(0.2, 0.4))
        B.seg(K, A, 0.05, 0.055, GOLD, "Shin_" + side, ext=0.03, ext1=0.02, role="limb")
        for t in (0.30, 0.55, 0.80):
            B.add(K.lerp(A, t), (0.053, 0.058, 0.008), GOLD_D, "Shin_" + side, rot=(-12, 0, 0), studs=[],
                  role="detail", bevel=0.004)
        B.seg(A, T + Vector((0, 0, 0.03)), 0.045, 0.048, GOLD, "Foot_" + side, ext=0.03, role="limb")
        B.add(T + Vector((0, 0.005, 0.0)), (0.06, 0.06, 0.035), GOLD, "Foot_" + side, role="limb")
        for dx, dy in ((-0.05, -0.075), (0.0, -0.09), (0.05, -0.075)):
            tb = T + Vector((dx, dy, -0.005))
            B.seg(T + Vector((dx * 0.5, -0.02, 0.0)), tb, 0.023, 0.024, GOLD, "Foot_" + side, role="limb")
            B.spike(tb + Vector((0, -0.01, 0.008)), (0, -1, -0.62), 0.085, 0.02, BLACK, "Foot_" + side)
        B.spike(T + Vector((0, 0.05, 0.0)), (0, 1, -0.6), 0.075, 0.019, BLACK, "Foot_" + side)
    # ---------------- fanned tail: dark base + 7 long feathers spread in a fan, lightning tips
    T = [Vector(p) for p in TAILP]
    B.seg(T[0], T[1], 0.12, 0.08, BODY_D, "Tail1", ext=0.08, top=(0.9, 0.8))
    fan_n = Vector((0, 0.42, 0.91)).normalized()        # fan plane normal (tail held slightly raised)
    for i in range(7):
        a = (i - 3) / 3.0
        d = Vector((a * 0.55, 1.0, -0.38 + 0.05 * abs(a))).normalized()
        root = T[1] + Vector((a * 0.05, -0.04, 0.0))
        L = 0.56 - 0.06 * abs(a)
        feather(B, root, root + d * L, fan_n, 0.15, 0.03, BODY_D if i % 2 else PRIMARY, "Tail2", taper=0.4,
                tipc=BOLT, tipf=0.22)
    B.build()
    bk.stud_skin(k, PITCH)
    return {"TH": round(B.th, 3), "PITCH": PITCH}


# ------------------------------------------------------------------ rig
def rig(k):
    k.joint("Spine", (0, 0.12, 0.72), "Root", tail=(0, -0.2, 0.35))
    k.joint("Chest", (0, 0.00, 0.88), "Spine", tail=(0, -0.2, 0.35))
    k.joint("Neck", (0, -0.14, 1.16), "Chest", tail=(0, -0.12, 0.3))
    k.joint("Head", tuple(HC + Vector((0, 0.08, -0.12))), "Neck", tail=(0, -0.35, 0))       # throat pivot
    k.joint("Jaw", tuple(HC + Vector((0, -0.12, -0.08))), "Head", tail=(0, -0.2, 0))
    for s, side in ((1, "L"), (-1, "R")):
        k.joint("Wing_" + side, X(WING.S, s), "Chest")
        k.joint("WingTip_" + side, X(WING.W, s), "Wing_" + side, tail=(s * 0.6, 0.2, 0.1))
        k.joint("Leg_" + side, X(HIP, s), "Spine")
        k.joint("Shin_" + side, X(KNEE, s), "Leg_" + side)
        k.joint("Foot_" + side, X(ANKLE, s), "Shin_" + side, tail=(0, -0.15, -0.1))
        k.add_leg2("Leg_" + side, "Shin_" + side, "Foot_" + side, knee=(0, -1, 0))
    k.joint("Tail1", TAILP[0], "Spine")
    k.joint("Tail2", TAILP[1], "Tail1", tail=tuple(Vector(TAILP[2]) - Vector(TAILP[1])))


def check_pairs():
    W = ["Wing_L", "WingTip_L", "Wing_R", "WingTip_R"]
    P = [("Wing_L", "WingTip_L"), ("Wing_R", "WingTip_R"), ("WingTip_L", "WingTip_R"), ("Wing_L", "Wing_R"),
         ("WingTip_L", "Wing_R"), ("Wing_L", "WingTip_R")]
    for w in W:
        for b in ("Head", "Neck", "Tail1", "Tail2", "Leg_L", "Leg_R", "Shin_L", "Shin_R", "Foot_L", "Foot_R"):
            P.append((w, b))
    P += [("Leg_L", "Leg_R"), ("Shin_L", "Shin_R"), ("Foot_L", "Foot_R"), ("Head", "Chest"), ("Jaw", "Chest")]
    for b in ("Shin_L", "Shin_R", "Foot_L", "Foot_R"):
        P.append(("Tail2", b))
    return P


def joints():
    out = WING.joints()
    for s, sd in ((1, "L"), (-1, "R")):
        out.append((X(WING.S, s), X(WING.BB, s), 0.12, "Wing_" + sd))
    return out



# ------------------------------------------------------------------ animation
# Reference (owner rule): animationreference.org "Tyrant Dragon Animation - MAYA 2023" (#creature #3d-animation; the
# site has no bird clips): glide with the wings high and the outer wing trailing; LANDING = wings swept forward and down
# to brake while the legs reach, a heavy touchdown crouch absorbing the weight with the wings still up, then the fold.
# Flight/ground clips adapted from the Storm Wyvern (biped legs) + Griffin (feather wing fold) recipes.
import petkit as pk
import _common as cm

LEGS = ["Leg_L", "Leg_R"]
TAIL = ["Tail1", "Tail2"]
FOLD = (40.0, -4.0, 0.0, 100.0)          # Griffin fold: raised V, primaries swept back over the inner wing


def ease(u):
    u = max(0.0, min(1.0, u))
    return 0.5 - 0.5 * math.cos(math.pi * u)


def wings(k, f, up, fwd=0.0, twist=0.0, tip=0.0, side=None):
    WING.key(k, f, up, fwd, twist, tip, side)


def folded(k, f, du=0.0, dfwd=0.0, dtip=0.0, side=None):
    wings(k, f, FOLD[0] + du, FOLD[1] + dfwd, FOLD[2], FOLD[3] + dtip, side)


def tail(k, f, pitch=0.0, yaw=0.0):
    k.key("Tail1", f, rot=(pitch * 0.6, yaw * 0.5, 0))
    k.key("Tail2", f, rot=(pitch * 0.4, yaw * 0.5, 0))


def rest_keys(k, f, z=0.0, pitch=0.0):
    k.key("Spine", f, rot=(pitch, 0, 0), loc=(0, 0, z))
    k.key("Chest", f, rot=(0, 0, 0))
    k.key("Neck", f, rot=(0, 0, 0))
    k.key("Head", f, rot=(0, 0, 0))
    k.key("Jaw", f, rot=(2, 0, 0))
    folded(k, f)
    tail(k, f, 0, 0)


def plant_frames(k, frames, z=0.0):
    import bpy
    k.bake_bezier_now()
    for f in frames:
        bpy.context.scene.frame_set(f)
        for leg in LEGS:
            k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, z)), toe=0.0)


def lift_air_frames(k, frames, target=0.02):
    """airborne frames: raise the Spine just enough that no vertex goes below `target` (Storm Wyvern)"""
    import bpy
    sc = bpy.context.scene
    body = k.main
    pb = k.arm.pose.bones["Spine"]
    R0 = k.arm.data.bones["Spine"].matrix_local.to_quaternion()
    k.bake_bezier_now()
    rows = []
    for f in frames:
        sc.frame_set(f)
        dg = bpy.context.evaluated_depsgraph_get()
        ev = body.evaluated_get(dg)
        me = ev.to_mesh()
        mw = ev.matrix_world
        mz = min((mw @ v.co).z for v in me.vertices)
        ev.to_mesh_clear()
        rows.append((f, mz, pb.rotation_quaternion.copy(), (R0 @ pb.location).copy()))
    for f, mz, q, loc in rows:
        if mz < target:
            pb.rotation_quaternion = q
            pb.keyframe_insert("rotation_quaternion", frame=f, group="Spine")
            k.key("Spine", f, loc=(loc.x, loc.y, loc.z + target - mz))


# ---- ground
def idle(k):
    """STORM WATCH: perched upright, quick bird head snaps with holds (left, right, down at the ground, sky), a slow
    one-wing stretch down and back, the tail fan flicks, a breath swell."""
    n = 132
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 2):
        b = pk.wave(f, n, 0, 3)
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, 0.008 * b))
        k.key("Chest", f, rot=(-1.5 * b, 0, 0))
        k.key("Jaw", f, rot=(2, 0, 0))
    snaps = ((0, 0, 0, 0, 0), (18, 0, 0, 0, 0), (20, -2, 30, 6, -4), (34, -2, 30, 6, -4), (36, -2, -28, -6, 4),
             (50, -2, -28, -6, 4), (52, 8, 0, 14, 0), (64, 8, 0, 14, 0), (66, -6, 0, -12, 0), (76, -6, 0, -12, 0),
             (78, 0, 0, 0, 0), (132, 0, 0, 0, 0))
    for f, nk, ny, hd, ht in snaps:
        k.key("Neck", f, rot=(nk, ny * 0.3, 0))
        k.key("Head", f, rot=(hd, ny * 0.7, ht))
    for f, d in ((0, 0), (84, 0), (94, 1), (110, 1), (120, 0), (132, 0)):     # left wing stretch down/back
        wings(k, f, FOLD[0] - 46 * d, FOLD[1] - 10 * d, 0, FOLD[3] - 60 * d, side="L")
        folded(k, f, side="R")
    for f, p, y in ((0, 0, 0), (40, 0, 0), (43, 10, 8), (46, -4, -6), (49, 0, 0), (132, 0, 0)):
        tail(k, f, p, y)
    plant_frames(k, range(0, n + 1))
    k.finish()
    k.meta["planted"] = LEGS


def walk(k):
    """raptor walk: the head bobs (thrust + hold) twice per cycle, the body rolls over the stance leg, tail fan sways"""
    n = 28

    def body(f):
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(1.5 * pk.wave(f, n, 0.1, 2), 3 * pk.wave(f, n, 0.0), 4 * pk.wave(f, n, 0.0)),
              loc=(0, 0, -0.025 * b))
        k.key("Chest", f, rot=(0, -2 * pk.wave(f, n, 0.05), -2 * pk.wave(f, n, 0.0)))
        k.key("Neck", f, rot=(4 * pk.wave(f, n, 0.0, 2), 0, 0))
        k.key("Head", f, rot=(-4 * pk.wave(f, n, 0.08, 2), 0, 0))
        k.key("Jaw", f, rot=(2, 0, 0))
        folded(k, f, du=2 * pk.wave(f, n, 0.3, 2))
        tail(k, f, 2 * pk.wave(f, n, 0.2, 2), 6 * pk.wave(f, n, 0.15))
    orig = k.solve_leg
    k.solve_leg = lambda leg, f, T, foot_z=0.0, toe=None: orig(leg, f, T, foot_z, toe=14.0 * min(1.0, max(0.0, T.z) / 0.1))
    try:
        return cm.biped_walk(k, n, 0.15, 0.11, body, legs=(("Leg_L", 0.0), ("Leg_R", 0.5)), duty=0.6)
    finally:
        del k.solve_leg


def roar(k):
    """SKY SCREECH: rears up tall, throws the wings wide open to the sides (full display), head up, beak wide, two
    thunder beats of the open wings (events beat1/beat2), folds."""
    n = 70
    k.new_action("roar", n, False)
    OPEN = (-6, 2, 0, -8)
    for f, p, z, nk, hd, jw, w in ((0, 0, 0, 0, 0, 2, None), (8, 4, -0.04, 4, 4, 4, (30, 0, 0, 40)),
                                   (16, -10, 0.03, -6, -12, 34, OPEN), (24, -10, 0.03, -6, -12, 34, (22, 6, 6, -4)),
                                   (28, -10, 0.03, -6, -12, 36, OPEN), (36, -10, 0.03, -6, -12, 34, (22, 6, 6, -4)),
                                   (40, -10, 0.03, -6, -12, 36, OPEN), (50, -8, 0.02, -5, -10, 30, OPEN),
                                   (60, 2, 0.0, 0, 0, 4, (30, 0, 0, 60)), (70, 0, 0, 0, 0, 2, None)):
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(p * 0.3, 0, 0))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        if w:
            wings(k, f, *w)
        else:
            folded(k, f)
        tail(k, f, 8 if 8 <= f <= 50 else 0, 0)
    plant_frames(k, range(0, n + 1))
    k.finish(loop=False)
    k.events["roar"] = {"beat1": round(28 / n, 3), "beat2": round(40 / n, 3)}


def talonstrike(k):
    """SIGNATURE (Thunderbird only) - TALON STRIKE: crouches with the wings cocked high, hops up, swings BOTH feet
    forward and drives the talons down into the ground in front (event strike: lightning impact), wings flared up and
    back, head down over the kill; then lifts the head and screams with the talons still clenched; folds."""
    import bpy
    n = 80
    k.new_action("act_talonstrike", n, False)
    rest_keys(k, 0)
    K = [  # f, spine z, spine pitch, neck, head, jaw, wings (up, fwd, twist, tip) | None = folded, tail pitch
        (8, -0.07, 6, 4, 4, 2, (60, -6, 0, 40), 6),
        (12, -0.08, 6, 4, 4, 2, (66, -4, 0, 30), 6),
        (17, 0.16, -14, -4, -6, 6, (30, 4, 0, 10), 12),
        (21, 0.12, -6, 2, 4, 8, (50, -8, 0, 20), 10),
        (24, -0.02, 14, 8, 10, 10, (56, -12, 0, 24), 12),
        (32, -0.04, 16, 8, 12, 4, (54, -12, 0, 26), 10),
        (42, -0.03, 4, -6, -12, 32, (46, -8, 0, 40), 8),
        (54, -0.03, 4, -6, -12, 30, (46, -8, 0, 40), 8),
        (66, 0.0, 0, 0, 0, 2, None, 0)]
    for f, z, p, nk, hd, jw, w, tp in K:
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(p * 0.2, 0, 0))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        if w:
            wings(k, f, *w)
        else:
            folded(k, f)
        tail(k, f, tp, 0)
    rest_keys(k, n)
    k.bake_bezier_now()
    sc = bpy.context.scene
    reach = Vector((0, -0.16, 0))                       # talons strike the ground in front of the rest spot
    for f in list(range(0, 15)):
        sc.frame_set(f)
        for leg in LEGS:
            k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, 0.0)), toe=0.0)
    for f in range(24, 56):
        sc.frame_set(f)
        for leg in LEGS:
            k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, 0.0)) + reach, toe=0.0)
    for f in range(66, n + 1):
        sc.frame_set(f)
        for leg in LEGS:
            k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, 0.0)), toe=0.0)
    for f, th, sh, fo in ((17, -20, 30, 30), (21, -40, 50, 20)):      # airborne: feet swing forward
        for leg in LEGS:
            k.key(leg, f, rot=(th, 0, 0), loc=(0, 0, 0))
            k.key(leg.replace("Leg_", "Shin_"), f, rot=(sh, 0, 0))
            k.key(leg.replace("Leg_", "Foot_"), f, rot=(fo, 0, 0))
    for f, dy in ((58, -0.10), (62, -0.04)):              # step the feet back to the rest spots
        sc.frame_set(f)
        for leg in LEGS:
            k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y + dy + 0.16 * 0, 0.03 if f == 58 else 0.0)), toe=0.0)
    k.finish(loop=False)
    k.events["act_talonstrike"] = {"strike": round(24 / n, 3), "scream": round(42 / n, 3)}


# ---- flight (eagle: deep full-arm downstroke, outer wing tucks on the upstroke, legs tucked back, tail fan steers)
FPITCH, FNECK, FHEAD = 40.0, -10.0, -30.0
THI, SHI, FOO = 70.0, -40.0, 76.0


def fly_legs(k, f, ph):
    for s, side in ((1, "L"), (-1, "R")):
        p = ph + 0.03 * s
        k.key("Leg_" + side, f, rot=(THI + 4 * math.sin(2 * math.pi * (p - 0.15)), 0, -s * 3), loc=(0, 0, 0))
        k.key("Shin_" + side, f, rot=(SHI - 6 * math.sin(2 * math.pi * (p - 0.30)), 0, 0))
        k.key("Foot_" + side, f, rot=(FOO + 8 * math.sin(2 * math.pi * (p - 0.42)), 0, 0))


def fly_pose(k, f, ph, legs=True):
    w = wing3.stroke(ph, top=30, bot=-34, down=0.45, sweep=10, twist=10, fold=36)
    wings(k, f, w["up"], w["fwd"], w["twist"], w["tip"])
    k.key("Spine", f, rot=(FPITCH - 4 * math.sin(2 * math.pi * (ph - 0.1)), 0, 0),
          loc=(0, 0, 0.10 + 0.08 * math.cos(2 * math.pi * (ph - 0.45))))
    k.key("Chest", f, rot=(-3 * math.sin(2 * math.pi * (ph - 0.2)), 0, 0))
    k.key("Neck", f, rot=(FNECK + 3 * math.sin(2 * math.pi * (ph - 0.25)), 0, 0))
    k.key("Head", f, rot=(FHEAD - 4 * math.sin(2 * math.pi * (ph - 0.32)), 0, 0))
    k.key("Jaw", f, rot=(2, 0, 0))
    tail(k, f, -6 + 5 * math.sin(2 * math.pi * (ph - 0.3)), 3 * math.sin(2 * math.pi * ph))
    if legs:
        fly_legs(k, f, ph)


def fly(k):
    n = 28
    k.new_action("fly", n, True)
    for f in range(0, n + 1):
        fly_pose(k, f, f / n)
    k.finish()


def takeoff(k):
    """crouch, wings unfold high, LAUNCH (event) on a huge downstroke, legs push then tuck back"""
    n = 30
    k.new_action("takeoff", n, False)
    rest_keys(k, 0)
    for f, z, p, ch, hd, w in ((5, -0.08, 6, 4, -6, (60, -6, 0, 40)), (10, -0.16, 10, 6, -12, (66, 0, -8, -4)),
                               (13, 0.06, 18, 0, -20, (-10, 10, 12, -10)), (17, 0.12, 30, -2, -26, (-34, 8, 6, 4))):
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(ch, 0, 0))
        k.key("Neck", f, rot=(-p * 0.25, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(2, 0, 0))
        wings(k, f, *w)
        tail(k, f, 6 + p * 0.2, 0)
    fly_pose(k, 23, 0.0)
    fly_pose(k, n, 0.45)
    plant_frames(k, range(0, 13))
    for s, side in ((1, "L"), (-1, "R")):
        k.key("Leg_" + side, 14, rot=(24, 0, 0), loc=(0, 0, 0))
        k.key("Shin_" + side, 14, rot=(-10, 0, 0))
        k.key("Foot_" + side, 14, rot=(40, 0, 0))
        k.key("Leg_" + side, 18, rot=(50, 0, 0), loc=(0, 0, 0))
        k.key("Shin_" + side, 18, rot=(-30, 0, 0))
        k.key("Foot_" + side, 18, rot=(66, 0, 0))
    lift_air_frames(k, range(13, n + 1))
    k.finish(loop=False)
    k.events["takeoff"] = {"launch": round(11 / n, 3)}


def land(k):
    """(ref: Tyrant Dragon landing) flare upright, wings swept forward and down to brake, legs reach, TOUCH (event),
    a heavy crouch absorbing the weight with the wings still up, then the fold"""
    n = 32
    k.new_action("land", n, False)
    fly_pose(k, 0, 0.0)
    for f, p, z, nk, hd, w, lg in (
            (6, 16, 0.10, -4, -18, (24, 16, -10, -4), (-4, -16, 10)),
            (10, -4, 0.10, 0, -8, (-24, 22, -10, 8), (-24, 4, -8)),
            (13, -6, 0.08, 0, -6, (22, 18, -8, -6), (-20, 8, -12)),
            (15, -4, 0.04, 0, -4, (0, 8, -6, 12), (-10, 4, -6))):
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(-3, 0, 0))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(3, 0, 0))
        wings(k, f, *w)
        tail(k, f, 10, 0)
        for s, side in ((1, "L"), (-1, "R")):
            k.key("Leg_" + side, f, rot=(lg[0], 0, 0), loc=(0, 0, 0))
            k.key("Shin_" + side, f, rot=(lg[1], 0, 0))
            k.key("Foot_" + side, f, rot=(lg[2], 0, 0))
    for f, z, p, w in ((17, -0.12, 8, (40, 4, 0, 30)), (22, -0.07, 4, (46, -2, 0, 80)), (28, 0.0, 0, None)):
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(2, 0, 0))
        k.key("Neck", f, rot=(p * 0.5, 0, 0))
        k.key("Head", f, rot=(-p * 0.4, 0, 0))
        k.key("Jaw", f, rot=(2, 0, 0))
        if w:
            wings(k, f, *w)
        else:
            folded(k, f)
        tail(k, f, 6 if f < 28 else 0, 0)
    rest_keys(k, n)
    lift_air_frames(k, range(0, 17))
    plant_frames(k, range(17, n + 1))
    k.finish(loop=False)
    k.events["land"] = {"touch": round(17 / n, 3)}


def anim(k):
    idle(k)
    stride = walk(k)
    fly(k)
    takeoff(k)
    land(k)
    roar(k)
    talonstrike(k)
    return stride


HEAD_XF = []
