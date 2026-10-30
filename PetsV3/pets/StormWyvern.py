# Storm Wyvern (Thunder egg, flyer) - FIERCE style (2026-10-09, FIERCE_PLAN.md "the sky raptor"): a lean heraldic
# wyvern built from tapered blocks and covered in Roblox studs: upright 30 deg forward, a long crested pterosaur skull
# (back crest blade + 2 swept horns), narrow slanted crimson eyes under heavy brows, a jaw with 4 fangs, an S-curved
# neck, a deep keel chest with pale belly bands, digitigrade raptor legs (3 talons forward + 1 back), bat membrane
# wings (arm + 3 dark fingers, wrist thumb claw, darker inner panel, crimson red-sprite zigzags near the fingers) and a
# long tail ending in a flat crimson arrow blade. No glow (sprite flashes = Studio VFX).
# Old chibi version: _tools/chibi_specs/StormWyvern.py
import math
from mathutils import Vector

DISPLAY = "Storm Wyvern"
MOTION = "Fly"
RIG = "wingbiped"
HEIGHT = 8.5                 # chest top ~6 studs at x1 (coordinator HEIGHT rule 2026-10-09)

# FIERCE_PLAN palette = in-game look; Roblox renders ~0.55-0.6x darker -> Blender colours ~1.8-2.2x brighter
BODY = (96, 90, 166)         # dusky storm violet (plan 42,40,70)
BODY_D = (58, 54, 104)       # back spines, brows, saddle
MEM = (110, 102, 178)        # outer membranes (plan 60,56,96)
MEM_IN = (78, 72, 136)       # darker inner panel (plan 44,40,74)
BELLY = (170, 166, 212)      # belly bands (plan 120,118,150)
BELLY_D = (136, 132, 188)    # band grooves
BONE = (30, 26, 48)          # wing bones + claws (plan 18,16,30)
CREST = (226, 220, 238)      # crest + horns (plan 190,184,200)
RED = (255, 50, 90)          # accent: red-sprite crimson (eyes, blade, crest tip, membrane zigzags)
RED_HOT = (255, 170, 190)
BLACK = (14, 14, 22)
MOUTH = (86, 18, 30)
TEETH = (238, 234, 220)

H_MODEL = 1.77
PITCH = round(0.042 * (H_MODEL / HEIGHT) / (1.498 / 8.0), 4)

# joints (left side; right = mirrored x)
HIP, KNEE, ANKLE, TOE = (0.15, 0.12, 0.64), (0.18, -0.14, 0.44), (0.16, 0.07, 0.20), (0.16, -0.03, 0.03)
SHOULDER, WRIST = (0.21, -0.07, 1.17), (0.78, 0.02, 1.48)
F1, F2, F3, BODY_B = (1.62, 0.22, 1.50), (1.40, 0.68, 1.12), (0.94, 0.84, 0.80), (0.17, 0.30, 1.00)
TAILP = [(0, 0.26, 0.64), (0, 0.62, 0.44), (0, 1.02, 0.29), (0, 1.42, 0.21), (0, 1.80, 0.20)]


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


def zigzag(B, a, b, n, width, bone, amp=0.075, segs=4, lift=0.019):
    """crimson zigzag bolt from a to b lying on a membrane with normal n (both faces), ending in a point"""
    a, b = Vector(a), Vector(b)
    d = (b - a)
    side = d.cross(n).normalized()
    pts = [a + d * (i / segs) + side * (amp * (1 if i % 2 else -1) if 0 < i < segs else 0) for i in range(segs + 1)]
    for sg in (1, -1):
        for i in range(segs):
            p0, p1 = pts[i] + n * sg * lift, pts[i + 1] + n * sg * lift
            dd = (p1 - p0).normalized()
            B.bar(p0 - dd * (width * 0.4 if i else 0), p1, n, width, 0.008, RED, bone, studs=[], bevel=0.003,
                  top=(1, 0.15) if i == segs - 1 else (1, 1))


def membrane_wing(B, s, side):
    """bat wing: arm, wrist knuckle + thumb claw, 3 dark tapering fingers (finger 3 = fold hinge), darker inner
    membrane (Wing bone), 2 outer membranes (WingTip bone) with scalloped trailing edge, crimson zigzags."""
    S, W, f3, bb = X(SHOULDER, s), X(WRIST, s), X(F3, s), X(BODY_B, s)
    f1, f2 = X(F1, s), X(F2, s)
    wb, tb = "Wing_" + side, "WingTip_" + side
    B.seg(S + (W - S).normalized() * 0.07, W, 0.062, 0.07, BODY, wb, side=(0, 0, 1), ext=0.0,
          top=(0.75, 0.75))                                  # arm (root starts in the flight muscle, clear of the neck)
    B.add(W, (0.07, 0.07, 0.07), BONE, wb, rnd=0.3)                                                # wrist knuckle
    B.spike(W + Vector((0, -0.03, 0.05)), (s * 0.1, -0.7, 0.7), 0.13, 0.034, BONE, wb, top=(0.12, 0.3),
            nostud=True)                                                                           # thumb
    B.seg(W, f3, 0.040, 0.045, BONE, wb, side=(0, 0, 1), top=(0.35, 0.35), nostud=True)
    for f, w in ((f1, 0.048), (f2, 0.042)):
        B.seg(W, f, w, w + 0.004, BONE, tb, side=(0, 0, 1), top=(0.3, 0.3), nostud=True)
    B.spike(f1 - (f1 - W).normalized() * 0.02, f1 - W, 0.10, 0.02, BONE, tb)                     # finger-1 claw
    e12 = f1.lerp(f2, 0.5).lerp(W, 0.20)
    e23 = f2.lerp(f3, 0.5).lerp(W, 0.20)
    q = f3.lerp(bb, 0.5).lerp(S, 0.16)
    th = 0.03
    B.poly([S, W, f3, q, bb], th, MEM_IN, wb)
    B.poly([W, f1, e12, f2], th, MEM, tb)
    B.poly([W, f2, e23, f3], th, MEM, tb)
    nrm = (f1 - W).cross(f3 - W).normalized()
    if nrm.z < 0:
        nrm = -nrm
    for a, b, bone in ((f1, e12, tb), (e12, f2, tb), (f2, e23, tb), (e23, f3, tb), (f3, q, wb), (q, bb, wb)):
        B.bar(a, b, nrm, 0.04, 0.022, MEM_IN, bone, nostud=True, bevel=0.006)                      # trailing trims
    # 3 red-sprite zigzags next to the fingers (each on its own panel plane)
    def up(n):
        n = n.normalized()
        return n if n.z > 0 else -n
    n1, n2, n3 = up((f1 - W).cross(f2 - W)), up((f2 - W).cross(f3 - W)), up((W - S).cross(f3 - S))
    zigzag(B, W.lerp(f1, 0.30).lerp(e12, 0.28), W.lerp(f1, 0.82).lerp(e12, 0.30), n1, 0.065, tb)
    zigzag(B, W.lerp(f2, 0.30).lerp(e23, 0.24), W.lerp(f2, 0.80).lerp(e23, 0.28), n2, 0.065, tb)
    zigzag(B, W.lerp(f3, 0.28).lerp(S, 0.20), W.lerp(f3, 0.70).lerp(q, 0.25), n3, 0.065, wb)


def model(k):
    import blockkit as bk
    B = bk.Blocks(k, seed=23, tier=3, plates=False)
    # ---------------- torso: deep keel chest leaning 30 deg forward, a narrower pelvis tucked under its back
    chest = B.add((0, -0.04, 1.00), (0.25, 0.21, 0.25), BODY, "Chest", rot=(30, 0, 0), bot=(0.66, 0.60),
                  top=(0.92, 0.92), rnd=0.38)
    B.add((0, 0.13, 0.70), (0.185, 0.17, 0.15), BODY, "Spine", rot=(30, 0, 0), top=(0.92, 0.9), bot=(0.78, 0.72),
          rnd=0.35)
    for s_ in (1, -1):                                                                           # flight muscles
        B.add((s_ * 0.20, -0.08, 1.13), (0.10, 0.13, 0.12), BODY, "Chest", rot=(30, 0, 0), top=(0.8, 0.85), rnd=0.40)
    B.seg((0, -0.27, 1.10), (0, -0.07, 0.70), 0.13, 0.065, BELLY, "Chest", top=(0.40, 0.8), ext=0.03)      # keel
    for t, w in ((0.22, 0.115), (0.50, 0.085), (0.78, 0.06)):                                    # belly bands
        p = Vector((0, -0.27, 1.10)).lerp(Vector((0, -0.07, 0.70)), t)
        n = Vector((0, -0.894, -0.447))
        B.bar(p + n * 0.066 + Vector((-w, 0, 0)), p + n * 0.066 + Vector((w, 0, 0)), n, 0.022, 0.008, BELLY_D,
              "Chest", studs=[], bevel=0.003)
    # ---------------- S-curved neck + pale throat
    B.seg((0, -0.12, 1.12), (0, -0.20, 1.38), 0.125, 0.12, BODY, "Neck", ext=0.05, top=(0.88, 0.9))
    B.seg((0, -0.20, 1.36), (0, -0.31, 1.50), 0.11, 0.105, BODY, "Neck", ext=0.03)
    B.seg((0, -0.26, 1.16), (0, -0.32, 1.40), 0.085, 0.03, BELLY, "Neck", ext=0.02)            # throat
    # ---------------- head (throat pivot): long crested pterosaur skull, tapered snout, 4 fangs, slit eyes
    B.add((0, -0.37, 1.575), (0.105, 0.125, 0.085), BODY, "Head", top=(0.78, 0.85), rnd=0.35)      # skull
    B.seg((0, -0.45, 1.565), (0, -0.66, 1.50), 0.075, 0.058, BODY, "Head", top=(0.62, 0.70), ext=0.03)   # snout
    B.seg((0, -0.46, 1.495), (0, -0.64, 1.475), 0.07, 0.018, BELLY, "Head", top=(0.7, 0.9))       # pale upper lip
    for s_ in (1, -1):
        B.add((s_ * 0.026, -0.625, 1.545), (0.010, 0.022, 0.006), BLACK, "Head", rot=(-14, 0, -s_ * 30), studs=[],
              role="detail", bevel=0.003)                                                          # nostril slits
    for s in (1, -1):
        B.spike((s * 0.042, -0.605, 1.485), (0, -0.15, -1), 0.075, 0.016, TEETH, "Head")          # upper fangs
        B.spike((s * 0.055, -0.53, 1.485), (0, 0, -1), 0.035, 0.011, TEETH, "Head")
    B.seg((0, -0.38, 1.455), (0, -0.62, 1.455), 0.062, 0.022, BELLY, "Jaw", top=(0.7, 1), ext=0.02)   # lower jaw
    B.add((0, -0.51, 1.478), (0.05, 0.10, 0.006), MOUTH, "Jaw", studs=[], role="detail", bevel=0.003)
    for s in (1, -1):
        B.spike((s * 0.036, -0.585, 1.47), (0, 0, 1), 0.05, 0.012, TEETH, "Jaw")                  # lower fangs
    # heavy brows + narrow slanted crimson eyes on the skull front corners
    for s in (1, -1):
        B.add((s * 0.072, -0.488, 1.628), (0.062, 0.03, 0.024), BODY_D, "Head", rot=(0, -s * 22, s * 16),
              role="detail", bevel=0.01)                                                           # brow
        B.add((s * 0.078, -0.478, 1.592), (0.05, 0.012, 0.022), BLACK, "Head", rot=(0, -s * 18, s * 20), studs=[],
              role="detail", bevel=0.004)                                                          # socket
        B.add((s * 0.080, -0.486, 1.592), (0.042, 0.006, 0.012), RED, "Head", rot=(0, -s * 18, s * 20), studs=[],
              role="detail", bevel=0.003)                                                          # slit
        B.add((s * 0.090, -0.489, 1.596), (0.018, 0.004, 0.006), RED_HOT, "Head", rot=(0, -s * 18, s * 20),
              studs=[], role="detail", bevel=0.002)                                                # hot centre
    # back crest blade (flat in the side plane, ending in a crimson point) + 2 swept-back horns + jaw frills
    B.seg((0, -0.34, 1.64), (0, -0.10, 1.73), 0.028, 0.065, CREST, "Head", side=(1, 0, 0), top=(0.6, 0.35),
          ext=0.04, nostud=True)
    B.spike((0, -0.12, 1.725), (0, 0.94, 0.34), 0.13, 0.024, RED, "Head", side=(1, 0, 0), top=(0.4, 0.15),
            nostud=True)
    for s in (1, -1):
        B.spike((s * 0.075, -0.40, 1.645), (s * 0.65, 0.75, 0.25), 0.19, 0.026, CREST, "Head", top=(0.15, 0.15),
                nostud=True)
        for dz, L in ((0.0, 0.11), (-0.05, 0.09)):
            B.spike((s * 0.08, -0.34, 1.52 + dz), (s * 0.45, 0.9, -0.15 + dz * 4), L, 0.03, BODY_D, "Head",
                    top=(0.15, 0.35))
    # ---------------- dorsal spines laid back: neck -> back -> tail root
    for p, L, ang, bone in (((0, -0.22, 1.50), 0.17, 60, "Neck"), ((0, -0.14, 1.36), 0.19, 62, "Neck"),
                            ((0, -0.04, 1.22), 0.21, 66, "Chest"), ((0, 0.06, 1.08), 0.20, 68, "Chest"),
                            ((0, 0.16, 0.92), 0.17, 70, "Spine"), ((0, 0.25, 0.80), 0.13, 72, "Spine")):
        d = Vector((0, math.sin(math.radians(ang)), math.cos(math.radians(ang))))
        B.spike(p, d, L, 0.075, BODY_D, bone, side=(1, 0, 0), top=(0.15, 0.3))
    # ---------------- digitigrade raptor legs: drumstick thigh, shin, metatarsus, 3 talons forward + 1 back
    for s, side in ((1, "L"), (-1, "R")):
        H, K, A, T = X(HIP, s), X(KNEE, s), X(ANKLE, s), X(TOE, s)
        B.seg(H + Vector((0, 0.03, 0.08)), K, 0.118, 0.16, BODY, "Leg_" + side, ext=0.0, ext1=0.04,
              top=(0.70, 0.55), rnd=0.4)                                                           # drumstick thigh
        B.seg(K, A, 0.072, 0.08, BODY, "Shin_" + side, ext=0.03, ext1=0.02, top=(0.76, 0.76))
        B.seg(A, T + Vector((0, 0, 0.03)), 0.056, 0.058, BODY_D, "Foot_" + side, ext=0.03, top=(0.9, 0.9))
        B.add(T + Vector((0, -0.01, 0.0)), (0.07, 0.068, 0.03), BODY_D, "Foot_" + side)
        for gx, L in ((-0.045, 0.11), (0.0, 0.13), (0.045, 0.11)):
            B.spike(T + Vector((gx, -0.055, 0.016)), (gx * 3, -1, -0.33), L, 0.02, BONE, "Foot_" + side)
        B.spike(T + Vector((0, 0.05, 0.018)), (0, 1, -0.4), 0.075, 0.017, BONE, "Foot_" + side)
    # ---------------- long tail (4 bones) tapering into a flat crimson arrow blade
    T = [Vector(p) for p in TAILP]
    for i, (hw, tp) in enumerate(((0.12, 0.80), (0.095, 0.78), (0.072, 0.75), (0.052, 0.75))):
        B.seg(T[i], T[i + 1], hw, hw * 0.95, BODY, "Tail%d" % (i + 1), ext=0.10 if i == 0 else 0.04, top=(tp, tp))
        dv = (T[i + 1] - T[i]).normalized()
        dn = dv.cross(Vector((1, 0, 0))).normalized()
        dn = dn if dn.z < 0 else -dn
        B.seg(T[i] + dn * hw * 0.80, T[i + 1] + dn * hw * tp * 0.80, hw * 0.62, hw * 0.25, BELLY,
              "Tail%d" % (i + 1), ext=0.0 if i == 0 else 0.03, top=(tp, tp))                     # pale underside
        if i < 3:
            mid = T[i].lerp(T[i + 1], 0.5) + Vector((0, 0, hw * 0.8))
            B.spike(mid, (0, 0.85, 0.5), (0.15, 0.12, 0.09)[i], (0.0675, 0.0555, 0.0435)[i], BODY_D, "Tail%d" % (i + 1),
                    side=(1, 0, 0), top=(0.15, 0.3))
    tip = T[4]
    blade = [tip + Vector(v) for v in ((0, -0.02, 0.0), (0, 0.06, 0.14), (0, 0.13, 0.05), (0, 0.36, 0.0),
                                       (0, 0.13, -0.05), (0, 0.06, -0.12))]
    B.poly([tip + Vector((0, 0.10, 0.0))] + blade, 0.05, RED, "Tail4")
    # ---------------- membrane wings (rest = spread); the outer wing hinges on finger 3 to fold like a fan
    for s, side in ((1, "L"), (-1, "R")):
        membrane_wing(B, s, side)
    B.build()
    bk.stud_skin(k, PITCH)
    return {"TH": round(B.th, 3), "PITCH": PITCH}


# ------------------------------------------------------------------ rig
def rig(k):
    k.joint("Spine", (0, 0.14, 0.70), "Root", tail=(0, -0.2, 0.35))
    k.joint("Chest", (0, 0.02, 0.86), "Spine", tail=(0, -0.2, 0.35))
    k.joint("Neck", (0, -0.13, 1.14), "Chest", tail=(0, -0.12, 0.3))
    k.joint("Head", (0, -0.30, 1.47), "Neck", tail=(0, -0.4, 0))              # throat pivot
    k.joint("Jaw", (0, -0.40, 1.465), "Head", tail=(0, -0.25, 0))
    for s, side in ((1, "L"), (-1, "R")):
        k.joint("Wing_" + side, X(SHOULDER, s), "Chest")
        k.joint("WingTip_" + side, X(WRIST, s), "Wing_" + side, tail=(s * 0.6, 0.2, 0.0))
        k.joint("Leg_" + side, X(HIP, s), "Spine")
        k.joint("Shin_" + side, X(KNEE, s), "Leg_" + side)
        k.joint("Foot_" + side, X(ANKLE, s), "Shin_" + side, tail=(0, -0.15, -0.1))
        k.add_leg2("Leg_" + side, "Shin_" + side, "Foot_" + side, knee=(0, -1, 0))
    for i in range(4):
        k.joint("Tail%d" % (i + 1), TAILP[i], "Spine" if i == 0 else "Tail%d" % i,
                tail=(Vector(TAILP[i + 1]) - Vector(TAILP[i])) if i == 3 else None)


def check_pairs():
    W = ["Wing_L", "WingTip_L", "Wing_R", "WingTip_R"]
    pairs = [("Wing_L", "WingTip_L"), ("Wing_R", "WingTip_R"), ("WingTip_L", "WingTip_R"), ("Wing_L", "Wing_R"),
             ("WingTip_L", "Wing_R"), ("Wing_L", "WingTip_R"), ("Leg_L", "Leg_R"), ("Shin_L", "Shin_R"),
             ("Foot_L", "Foot_R"), ("Head", "Chest"), ("Jaw", "Chest"), ("Head", "Wing_L"), ("Head", "Wing_R")]
    for w in W:
        for b in ("Head", "Neck", "Tail1", "Tail2", "Leg_L", "Leg_R", "Shin_L", "Shin_R", "Foot_L", "Foot_R"):
            if (w, b) not in pairs:
                pairs.append((w, b))
    for t in ("Tail2", "Tail3", "Tail4"):
        for b in ("Shin_L", "Shin_R", "Foot_L", "Foot_R"):
            pairs.append((t, b))
    return pairs


def joints():
    out = []
    for s, side in ((1, "L"), (-1, "R")):
        W, f3 = X(WRIST, s), X(F3, s)
        out += [(W, f3, 0.10, "Wing_" + side), (W, W, 0.16, "Wing_" + side)]
    return out


# ------------------------------------------------------------------ animation (FIERCE_PLAN: gargoyle perch / hood
# shriek / thunder claps; bat flight with leg pump, takeoff "launch", land "touch"). Wyvern-only motifs: the cloak
# perch, the swan-busk hood, the triple wing clap above the back.
import petkit as pk
import _common as cm
import wing3

LEGS = ["Leg_L", "Leg_R"]
TAIL = ["Tail1", "Tail2", "Tail3", "Tail4"]
WING = wing3.Wing(SHOULDER, WRIST, F3, BODY_B)
FOLD = dict(up=42, fwd=-6, twist=0, tip=105)          # ground pose: wings folded high on the shoulders like a cloak


def wings(k, f, up, fwd=0.0, twist=0.0, tip=0.0, side=None):
    WING.key(k, f, up, fwd, twist, tip, side)


def folded(k, f, du=0.0, dfwd=0.0, dtip=0.0, side=None):
    wings(k, f, FOLD["up"] + du, FOLD["fwd"] + dfwd, FOLD["twist"], FOLD["tip"] + dtip, side)


def tail(k, f, pitch=0.0, yaw=0.0, each=(1.0, 1.0, 1.0, 1.0)):
    for b, g in zip(TAIL, each):
        k.key(b, f, rot=(pitch * g, yaw * g, 0))


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
    """FLOOR RULE for airborne frames: raise the Spine just enough that no vertex goes below `target`"""
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


# ---- flight (bat-like: deep full-arm downstroke, outer wing folds on the upstroke, legs pump, tail S-waves)
PITCH, NECK, HEAD = 42.0, -10.0, -30.0
THI, SHI, FOO = 62.0, -46.0, 70.0


def fly_legs(k, f, ph):
    for s, side in ((1, "L"), (-1, "R")):
        p = ph + 0.03 * s
        k.key("Leg_" + side, f, rot=(THI + 10 * math.sin(2 * math.pi * (p - 0.15)), 0, -s * 3), loc=(0, 0, 0))
        k.key("Shin_" + side, f, rot=(SHI - 14 * math.sin(2 * math.pi * (p - 0.30)), 0, 0))
        k.key("Foot_" + side, f, rot=(FOO + 16 * math.sin(2 * math.pi * (p - 0.42)), 0, 0))


def fly_pose(k, f, ph, legs=True):
    w = wing3.stroke(ph, top=34, bot=-38, down=0.45, sweep=10, twist=10, fold=40)
    wings(k, f, w["up"], w["fwd"], w["twist"], w["tip"])
    k.key("Spine", f, rot=(PITCH - 4 * math.sin(2 * math.pi * (ph - 0.1)), 0, 0),
          loc=(0, 0, 0.10 + 0.08 * math.cos(2 * math.pi * (ph - 0.45))))
    k.key("Chest", f, rot=(-3 * math.sin(2 * math.pi * (ph - 0.2)), 0, 0))
    k.key("Neck", f, rot=(NECK + 4 * math.sin(2 * math.pi * (ph - 0.25)), 0, 0))
    k.key("Head", f, rot=(HEAD - 5 * math.sin(2 * math.pi * (ph - 0.32)), 0, 0))
    k.key("Jaw", f, rot=(3, 0, 0))
    for i, b in enumerate(TAIL):
        k.key(b, f, rot=(-10 + 7 * math.sin(2 * math.pi * (ph - 0.3 - 0.12 * i)),
                         4 * math.sin(2 * math.pi * (ph - 0.2 * i)), 0))
    if legs:
        fly_legs(k, f, ph)


def fly(k):
    n = 28
    k.new_action("fly", n, True)
    for f in range(0, n + 1):
        fly_pose(k, f, f / n)
    k.finish()


def takeoff(k):
    """crouch, wings unfold high, LAUNCH (event) on a huge downstroke, legs push then pull back into flight"""
    n = 30
    k.new_action("takeoff", n, False)
    rest_keys(k, 0)
    for f, z, p, ch, hd, w in ((5, -0.10, 6, 4, -6, (60, -6, 0, 40)), (10, -0.20, 10, 6, -12, (70, 0, -8, -4)),
                               (13, 0.06, 18, 0, -20, (-10, 10, 12, -10)), (17, 0.12, 30, -2, -26, (-38, 8, 6, 4))):
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
    for s, side in ((1, "L"), (-1, "R")):               # legs leave the ground: push long, then pull back
        k.key("Leg_" + side, 14, rot=(24, 0, 0), loc=(0, 0, 0))
        k.key("Shin_" + side, 14, rot=(-10, 0, 0))
        k.key("Foot_" + side, 14, rot=(40, 0, 0))
        k.key("Leg_" + side, 18, rot=(44, 0, 0), loc=(0, 0, 0))
        k.key("Shin_" + side, 18, rot=(-34, 0, 0))
        k.key("Foot_" + side, 18, rot=(62, 0, 0))
    lift_air_frames(k, range(13, n + 1))
    k.finish(loop=False)
    k.events["takeoff"] = {"launch": round(11 / n, 3)}


def land(k):
    """flare upright, braking beats with the wings swept forward, legs swing forward and reach, TOUCH (event),
    absorb in a crouch, fold the wings into the cloak"""
    n = 30
    k.new_action("land", n, False)
    fly_pose(k, 0, 0.0)
    for f, p, z, nk, hd, w, lg in (
            (6, 16, 0.10, -4, -18, (24, 16, -10, -4), (-4, -16, 10)),
            (10, -4, 0.10, 0, -8, (-24, 20, -10, 8), (-20, 4, -8)),
            (13, -6, 0.08, 0, -6, (22, 16, -8, -6), (-18, 8, -12)),
            (15, -4, 0.04, 0, -4, (0, 8, -6, 12), (-10, 4, -6))):
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(-3, 0, 0))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(3, 0, 0))
        wings(k, f, *w)
        tail(k, f, 6, 0)
        for s, side in ((1, "L"), (-1, "R")):
            k.key("Leg_" + side, f, rot=(lg[0], 0, 0), loc=(0, 0, 0))
            k.key("Shin_" + side, f, rot=(lg[1], 0, 0))
            k.key("Foot_" + side, f, rot=(lg[2], 0, 0))
    for f, z, p, w in ((17, -0.14, 6, (16, 0, 0, 40)), (21, -0.08, 3, (34, -6, 0, 90)), (26, 0.0, 0, None)):
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(2, 0, 0))
        k.key("Neck", f, rot=(p * 0.5, 0, 0))
        k.key("Head", f, rot=(-p * 0.4, 0, 0))
        k.key("Jaw", f, rot=(2, 0, 0))
        if w:
            wings(k, f, *w)
        else:
            folded(k, f)
        tail(k, f, 8 if f < 26 else 0, 0)
    rest_keys(k, n)
    lift_air_frames(k, range(0, 17))
    plant_frames(k, range(17, n + 1))
    k.finish(loop=False)
    k.events["land"] = {"touch": round(17 / n, 3)}


# ---- ground
def idle(k):
    """GARGOYLE PERCH: crouched low with the wings folded high on the shoulders like a hunched cloak (wrists above the
    head), head low; slow breaths; f40 the tail tip whip-cracks once; 70-80 the jaw clacks twice; 90-110 a slow head
    turn and back."""
    n = 120
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 2):
        b = pk.wave(f, n, 0, 3)
        k.key("Spine", f, rot=(6, 0, 0), loc=(0, 0, -0.07 + 0.01 * b))
        k.key("Chest", f, rot=(-1.5 * b, 0, 0))
        folded(k, f, du=4 + 2 * b, dfwd=4)
    for f, nk, ny, hd, hy in ((0, 8, 0, 6, 0), (88, 8, 0, 6, 0), (98, 6, 12, 4, 20), (104, 6, 12, 4, 20),
                              (114, 8, 0, 6, 0), (120, 8, 0, 6, 0)):
        k.key("Neck", f, rot=(nk, ny, 0))
        k.key("Head", f, rot=(hd, hy, 0))
    for f, j in ((0, 2), (68, 2), (71, 16), (73, 2), (76, 16), (78, 2), (120, 2)):
        k.key("Jaw", f, rot=(j, 0, 0))
    for f, p, y4 in ((0, -2, 0), (34, -2, 0), (37, -6, -14), (40, 8, 34), (42, -4, -16), (46, -2, 0), (120, -2, 0)):
        tail(k, f, p, y4 * 0.2, each=(0.3, 0.5, 0.8, 1.0))
        k.key("Tail4", f, rot=(p, y4, 0))
    plant_frames(k, range(0, n + 1))
    k.finish()
    k.meta["planted"] = LEGS


def walk(k):
    n = 28

    def body(f):
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(1.5 * pk.wave(f, n, 0.1, 2), 4 * pk.wave(f, n, 0.0), 3.5 * pk.wave(f, n, 0.0)),
              loc=(0, 0, -0.03 * b))
        k.key("Chest", f, rot=(0, -3 * pk.wave(f, n, 0.05), -2 * pk.wave(f, n, 0.0)))
        k.key("Neck", f, rot=(3 + 2 * pk.wave(f, n, 0.15, 2), -2 * pk.wave(f, n, 0.1), 0))
        k.key("Head", f, rot=(-3 - 2 * pk.wave(f, n, 0.25, 2), 2 * pk.wave(f, n, 0.1), 0))
        k.key("Jaw", f, rot=(2, 0, 0))
        folded(k, f, du=3 * pk.wave(f, n, 0.3, 2))
        cm.chain(k, f, n, TAIL, sway=-7, pitch=0, cycles=1, lag=0.15, grow=0.4)
    orig = k.solve_leg
    k.solve_leg = lambda leg, f, T, foot_z=0.0, toe=None: orig(leg, f, T, foot_z, toe=14.0 * min(1.0, max(0.0, T.z) / 0.1))
    try:
        return cm.biped_walk(k, n, 0.18, 0.12, body, legs=(("Leg_L", 0.0), ("Leg_R", 0.5)), duty=0.6)
    finally:
        del k.solve_leg


def roar(k):
    """HOOD SHRIEK: the wings arch up and forward over the head like a hood (wrists high, tips hanging down in
    front - swan busking), the head held low between them, jaw wide shrieking, the tail lashes once; folds."""
    n = 60
    k.new_action("roar", n, False)
    HOOD = (64, 34, -12, 70)
    for f, p, nk, hd, jw, w in ((0, 0, 0, 0, 2, None), (10, -4, -6, -6, 6, (54, 10, -6, 70)),
                                (18, 8, 14, 10, 36, HOOD), (44, 8, 14, 10, 38, HOOD),
                                (52, 2, 4, 2, 6, (50, 4, -4, 90)), (60, 0, 0, 0, 2, None)):
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, -0.03 * (p > 0)))
        k.key("Chest", f, rot=(p * 0.3, 0, 0))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        if w:
            wings(k, f, *w)
        else:
            folded(k, f)
    for f in range(20, 44, 3):
        k.key("Jaw", f, rot=(36 + (3 if (f // 3) % 2 else -3), 0, 0))
    for f, y in ((0, 0), (22, 0), (27, 30), (32, -24), (37, 0), (60, 0)):
        tail(k, f, 6 if 22 <= f <= 37 else 0, y, each=(0.2, 0.5, 0.8, 1.0))
    plant_frames(k, range(0, n + 1))
    k.finish(loop=False)


def thunderclap(k):
    """SIGNATURE - THUNDER CLAPS: crouches with the tail braced and wings half open, sweeps the wings up over the back
    and CLAPS them together above it three times (spark VFX), the head thrusting forward with a jaw snap on each;
    the third, biggest clap goes up on its toes with the tail lifted; holds the wings high and open roaring; folds."""
    n = 90
    k.new_action("act_thunderclap", n, False)
    CLAP = (CL, -12, 0, -12)
    OPEN = (40, 6, 0, -10)
    K = [  # f, spine z, spine pitch, neck, head, jaw, wings, tail pitch
        (0, 0.0, 0, 0, 0, 2, None, 0),
        (10, -0.08, 8, 4, 2, 4, (20, 4, 0, 20), 10),
        (20, -0.05, 4, -2, -2, 6, (CL - 10, -10, -4, -12), 8),
        (24, -0.04, 8, 10, 8, 30, CLAP, 6),
        (26, -0.04, 8, 8, 6, 8, CLAP, 6),
        (32, -0.05, 4, 0, 0, 6, OPEN, 6),
        (38, -0.04, 8, 10, 8, 30, CLAP, 6),
        (40, -0.04, 8, 8, 6, 8, CLAP, 6),
        (46, -0.07, 4, 0, 0, 6, (14, 8, 0, 0), 8),     # wings swung low: the biggest arc into clap 3
        (52, 0.06, 14, 12, 10, 34, CLAP, 14),
        (56, 0.06, 14, 10, 8, 10, CLAP, 14),
        (62, 0.0, -4, -6, -10, 34, (56, 10, -6, -6), 8),
        (70, 0.0, -4, -6, -10, 34, (56, 10, -6, -6), 6),
        (80, 0.0, 0, 0, 0, 4, (48, 0, 0, 80), 0),
        (90, 0.0, 0, 0, 0, 2, None, 0)]
    for f, z, p, nk, hd, jw, w, tp in K:
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(-p * 0.3, 0, 0))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        if w:
            wings(k, f, *w)
        else:
            folded(k, f)
        tail(k, f, tp, 0, each=(1.0, 0.6, 0.3, 0.2))
    import bpy
    k.bake_bezier_now()
    for f in range(0, n + 1):
        bpy.context.scene.frame_set(f)
        up = 0.08 * max(0.0, math.sin(math.pi * (f - 48) / 12)) if 48 <= f <= 60 else 0.0
        for leg in LEGS:                                        # up on its toes for the third clap
            k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, up)), toe=15.0 * up / 0.08)
    k.finish(loop=False)
    k.events["act_thunderclap"] = {"clap1": round(24 / n, 3), "clap2": round(38 / n, 3), "clap3": round(52 / n, 3)}


CL = 66.5                                                       # clap: wings raised to meet above the back


def anim(k):
    idle(k)
    stride = walk(k)
    fly(k)
    takeoff(k)
    land(k)
    roar(k)
    thunderclap(k)
    return stride


HEAD_XF = []
