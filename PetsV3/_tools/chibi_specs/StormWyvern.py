# Storm Wyvern (Thunder egg, flyer): an upright storm wyvern, rebuilt to STYLE_BIBLE.md (2026-10-08 pro pass): a big
# horned head (fierce yellow eyes, 20 deg dark brows, a snout over a jaw with 4 fangs, 2 swept-back horns, 2 cheek
# frills) on a short thick neck, a deep chest with light 2x1 belly armour bands and a yellow chest gem, thick hind legs
# with light ankle bands and dark claws, a long tapering tail ending in a flat yellow bolt blade, and 2-tone membrane
# wings built to bible 2d (dark finger bones, scalloped trailing edges, darker inner panel, wrist claw).
# Flight = the whole body flies: power downstroke / folded-tip upstroke, body rises on each beat, head stays steady,
# legs pulled back like an eagle's and PUMPING with every stroke, tail waving.  Signature move: THUNDERCLAP.
import math
from mathutils import Vector

DISPLAY = "Storm Wyvern"
MOTION = "Fly"
RIG = "wingbiped"
HEIGHT = 9.0

STORM = (78, 84, 200)
BELLY = (196, 206, 255)
BONE = (36, 30, 90)
MEM = (200, 204, 255)          # outer panels (3-step gradient away from the body)
MEM_IN = (150, 150, 250)       # inner panel + trailing trims
HORN = (242, 236, 220)
GOLD = (255, 214, 60)
IRIS = (255, 214, 60)
MOUTH = (110, 26, 44)
TOOTH = (246, 244, 250)

# joints (left side; right = mirrored x)
HIP, KNEE, ANKLE = (0.25, 0.16, 0.74), (0.29, -0.10, 0.44), (0.29, 0.08, 0.14)
SHOULDER, WRIST = (0.42, -0.02, 1.52), (1.44, 0.16, 2.10)
F1, F2, F3, BODY_B = (2.64, 0.42, 2.24), (2.36, 1.10, 1.62), (1.70, 1.48, 1.06), (0.34, 0.36, 1.42)
TAILP = [(0, 0.40, 0.74), (0, 0.92, 0.50), (0, 1.42, 0.36), (0, 1.84, 0.32)]
TH = 0.80


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


def slab(B, p0, p1, width, thick, color, bone, **kw):
    """flat bar from p0 to p1 in a y-z plane (its thin side along x)"""
    p0, p1 = Vector(p0), Vector(p1)
    d = p1 - p0
    th = math.degrees(math.atan2(-d.y, d.z))
    return B.add((p0 + p1) / 2, (thick, width / 2, d.length / 2), color, bone, rot=(th, 0, 0), **kw)


def membrane_wing(B, s, side):
    """STYLE_BIBLE 2d membrane wing: storm arm bar, dark wrist knuckle + claw, 3 dark finger bones tapering to 0.4
    (finger 3 = the fold hinge, inner), scalloped panels 0.035 TH thick (outer light, inner x0.80 V), darker trailing
    trims so the edges read solid (no cyan)."""
    S, W, f3, bb = X(SHOULDER, s), X(WRIST, s), X(F3, s), X(BODY_B, s)
    f1, f2 = X(F1, s), X(F2, s)
    wb, tb = "Wing_" + side, "WingTip_" + side
    B.seg(S, W, 0.075, 0.08, STORM, wb, side=(0, 0, 1), ext=0.06, top=(0.85, 0.85), studs=["+y", "-y"], density=0.7)
    B.add(W, (0.10, 0.10, 0.10), BONE, wb, studs=[], role="limb")
    B.spike(W + Vector((0, -0.02, 0.08)), (s * 0.15, -0.55, 0.8), 0.24, 0.05, BONE, wb, top=(0.12, 0.12))
    B.seg(W, f3, 0.055, 0.06, BONE, wb, side=(0, 0, 1), top=(0.4, 0.4), studs=[], role="limb")
    for f, w in ((f1, 0.06), (f2, 0.055)):
        B.seg(W, f, w, w + 0.005, BONE, tb, side=(0, 0, 1), top=(0.4, 0.4), studs=[], role="limb")
    e12 = f1.lerp(f2, 0.5).lerp(W, 0.16)
    e23 = f2.lerp(f3, 0.5).lerp(W, 0.16)
    q = f3.lerp(bb, 0.5).lerp(S, 0.14)
    th = 0.05 * TH
    B.poly([S, W, f3, q, bb], th, MEM_IN, wb)
    B.poly([W, f1, e12, f2], th, MEM, tb)
    B.poly([W, f2, e23, f3], th, MEM, tb)
    nrm = (f1 - W).cross(f3 - W).normalized()
    for a, b, bone in ((f1, e12, tb), (e12, f2, tb), (f2, e23, tb), (e23, f3, tb), (f3, q, wb), (q, bb, wb)):
        B.bar(a, b, nrm, 0.05, 0.04, MEM_IN, bone, studs=[], bevel=0.01)


def model(k):
    """STYLE_BIBLE StormWyvern: HW 0.95 TW, HH 0.85 TH, head 29 % of H, legs 0.65 TH x 0.39 TW, tail 1.6 TL tapering
    1.0 -> 0.35 into a flat bolt blade, wings spanning ~5 BU."""
    import blockkit as bk
    B = bk.Blocks(k, seed=23, tier=3, th=TH)
    D = 0.62
    # ---- one torso: deep upright chest (leaning back), hips tucked under its back (chest 19 % wider)
    chest = B.add((0, -0.16, 1.10), (0.40, 0.34, 0.44), STORM, "Chest", rot=(-22, 0, 0), bot=(0.90, 1.0), density=D)
    B.add((0, 0.15, 0.78), (0.335, 0.30, 0.28), STORM, "Spine", rot=(-8, 0, 0), bot=(0.92, 0.95), density=D)
    # light belly armour bands (one per row, narrowing down) + yellow chest gem
    for v, hu in ((-0.385, 0.20), (-0.24, 0.24), (-0.095, 0.265)):
        B.on_face(chest, "-y", 0, v, hu, 0.062, 0.026, BELLY, bevel=0.016)
    gem_c = chest.world((0, -0.34 - 0.016, 0.05))
    B.add(gem_c, (0.062, 0.032, 0.062), GOLD, "Chest", R=chest.R @ bk.Euler((0, math.radians(45), 0), "XYZ").to_matrix(),
          studs=[], role="limb")
    # ---- short thick neck (0.9 HW) bridging the chest front-top and the head's back
    neck = B.add((0, -0.46, 1.62), (0.28, 0.22, 0.22), STORM, "Neck", rot=(35, 0, 0), studs=["+x", "-x"], density=D)
    for v in (-0.10, 0.08):
        B.on_face(neck, "-y", 0, v, 0.17, 0.06, 0.022, BELLY, bevel=0.014)
    # ---- head: HW 0.72, HH 0.68
    head = B.add((0, -0.66, 2.00), (0.38, 0.30, 0.34), STORM, "Head", top=(0.94, 0.94), density=D)
    B.add((0, -1.02, 1.84), (0.25, 0.20, 0.15), STORM, "Head", top=(0.86, 0.85), studs=["+x", "-x", "+z"],
          role="limb")                                                                             # snout
    for s in (1, -1):                                                                              # nostrils
        B.add((s * 0.085, -1.17, 1.975), (0.03, 0.03, 0.012), BONE, "Head", studs=[], bevel=0.006)
    B.add((0, -0.99, 1.692), (0.21, 0.19, 0.006), MOUTH, "Head", studs=[], bevel=0.004)            # mouth roof
    jaw = B.add((0, -0.99, 1.65), (0.22, 0.21, 0.05), BELLY, "Jaw", bot=(0.85, 0.9), studs=[], role="limb")
    B.add((0, -1.225, 1.695), (0.20, 0.008, 0.0125), MOUTH, "Head", studs=[], bevel=0.005)        # bite line
    for s in (1, -1):                                                        # 4 fangs, in front of the faces
        B.spike((s * 0.15, -1.235, 1.72), (0, 0, -1), 0.12, 0.032, TOOTH, "Head")
        B.spike((s * 0.08, -1.225, 1.66), (0, 0, 1), 0.08, 0.026, TOOTH, "Jaw")
    # fierce eyes (iris ring, pupil 69 % of the iris, 1 highlight), dark 20 deg brows
    B.face_eyes(head, "fierce", IRIS, base=STORM, brow=BONE, look=(0, 0.6), scale=1.1, pupil_size=(0.12, 0.09),
                hl_size=(0.055, 0.0), hl_on_pupil=True, brow_spec=(0.32, 0.07, 20))
    # 2 swept-back horns (2 segments + tip) and 2 cheek frills (fans of 3 flat blades from the head's back edge)
    for s in (1, -1):
        h0, h1 = Vector((s * 0.18, -0.52, 2.28)), Vector((s * 0.21, -0.26, 2.44))
        B.seg(h0, h1, 0.075, 0.075, HORN, "Head", side=(1, 0, 0), ext=0.06, top=(0.8, 0.8), studs=[], role="limb")
        B.spike(h1 - (h1 - h0).normalized() * 0.03, (s * 0.03, 0.95, 0.22), 0.34, 0.06, HORN, "Head")
        for dz, L in ((0.30, 0.30), (0.0, 0.36), (-0.30, 0.28)):
            root = Vector((s * 0.33, -0.50, 1.98 + dz * 0.25))
            d = Vector((s * 0.55, 0.75, dz)).normalized()
            B.seg(root, root + d * L, 0.07, 0.035, MEM, "Head", side=(0, 0, 1), ext=0.05, top=(0.2, 0.6), studs=[],
                  role="limb")
    # ---- dorsal spikes laid back along the back (wider than tall)
    for p, L, bone in (((0, 0.02, 1.58), 0.20, "Chest"), ((0, 0.18, 1.34), 0.18, "Chest"),
                       ((0, 0.30, 1.04), 0.16, "Spine")):
        B.spike(p, (0, 0.80, 0.42), L, 0.07, BONE, bone, side=(1, 0, 0), top=(0.15, 0.4))
    # ---- thick hind legs: drumstick thigh, shin with a light ankle band, foot with 3 dark claws + dew claw
    for s, side in ((1, "L"), (-1, "R")):
        H, K, A = X(HIP, s), X(KNEE, s), X(ANKLE, s)
        B.seg(H + Vector((0, 0.02, 0.10)), K, 0.17, 0.21, STORM, "Leg_" + side, ext=0.0, ext1=0.05, top=(0.80, 0.8),
              studs=["+x" if s > 0 else "-x", "-y"], density=D)
        B.seg(K, A, 0.13, 0.14, STORM, "Shin_" + side, ext=0.07, density=D)
        B.seg(A.lerp(K, 0.30), A.lerp(K, 0.0), 0.13 * 1.04, 0.14 * 1.04, BELLY, "Shin_" + side, studs=[],
              role="limb")
        foot = A + Vector((0, -0.06, -0.075))
        B.add(foot, (0.15, 0.20, 0.065), STORM, "Foot_" + side, studs=[], role="limb")
        for gx in (-0.09, 0.0, 0.09):
            B.spike(foot + Vector((gx, -0.16, -0.01)), (0, -1, -0.12), 0.12, 0.034, BONE, "Foot_" + side)
        B.spike(foot + Vector((0, 0.15, -0.01)), (0, 1, -0.3), 0.09, 0.028, BONE, "Foot_" + side)
    # ---- long tail tapering 1.0 -> 0.35, ending in a flat yellow bolt blade (y-z plane, ends in a point)
    T = [Vector(p) for p in TAILP]
    for i, (hw, hd, tp) in enumerate(((0.18, 0.17, 0.72), (0.13, 0.12, 0.70), (0.09, 0.085, 0.72))):
        B.seg(T[i], T[i + 1], hw, hd, STORM, "Tail%d" % (i + 1), ext=0.12 if i == 0 else 0.05, top=(tp, tp),
              studs=["+x", "-x"] if i == 0 else [], density=D, role="limb")
        dv = (T[i + 1] - T[i]).normalized()
        yl = dv.cross(Vector((1, 0, 0))).normalized()                       # the tail's underside direction
        yl = yl if yl.z < 0 else -yl
        B.seg(T[i] + yl * hd * 0.80, T[i + 1] + yl * hd * tp * 0.80, hw * 0.6, hd * 0.28, BELLY, "Tail%d" % (i + 1),
              ext=0.0 if i == 0 else 0.03, top=(tp, tp), studs=[], role="limb")             # light belly strip
    for i, (p, L) in enumerate((((0, 0.62, 0.78), 0.15), ((0, 1.12, 0.56), 0.12))):
        B.spike(p, (0, 0.85, 0.40), L, 0.055, BONE, "Tail%d" % (i + 1), side=(1, 0, 0), top=(0.15, 0.4))
    tip = T[3]
    slab(B, tip + Vector((0, -0.04, -0.02)), tip + Vector((0, 0.16, 0.26)), 0.20, 0.045, GOLD, "Tail3", studs=[],
         role="limb")
    slab(B, tip + Vector((0, 0.20, 0.22)), tip + Vector((0, 0.10, 0.36)), 0.18, 0.045, GOLD, "Tail3", studs=[],
         role="limb")
    B.add(tip + Vector((0, 0.20, 0.52)), (0.045, 0.10, 0.17), GOLD, "Tail3", rot=(-34, 0, 0), top=(0.6, 0.08),
          studs=[], role="limb")
    # ---- membrane wings (rest = spread); the outer wing hinges on finger 3 so it folds like a fan
    for s, side in ((1, "L"), (-1, "R")):
        membrane_wing(B, s, side)
    B.build()
    return {"plates": B.stud_count, "TH": round(B.th, 3), "cell": round(B.pcell, 3)}


# ------------------------------------------------------------------ rig
def rig(k):
    k.joint("Spine", (0, 0.12, 0.80), "Root", tail=(0, -0.4, 0.1))
    k.joint("Chest", (0, -0.06, 0.96), "Spine", tail=(0, -0.3, 0.15))
    k.joint("Neck", (0, -0.34, 1.44), "Chest")
    k.joint("Head", (0, -0.50, 1.74), "Neck", tail=(0, -0.4, 0))              # throat pivot
    k.joint("Jaw", (0, -0.82, 1.68), "Head", tail=(0, -0.3, 0))
    for s, side in ((1, "L"), (-1, "R")):
        k.joint("Wing_" + side, X(SHOULDER, s), "Chest")
        k.joint("WingTip_" + side, X(WRIST, s), "Wing_" + side, tail=(s * 0.6, 0.2, 0.1))
        k.joint("Leg_" + side, X(HIP, s), "Spine")
        k.joint("Shin_" + side, X(KNEE, s), "Leg_" + side)
        k.joint("Foot_" + side, X(ANKLE, s), "Shin_" + side, tail=(0, -0.3, 0))
        k.add_leg2("Leg_" + side, "Shin_" + side, "Foot_" + side, knee=(0, -1, 0))
    k.joint("Tail1", TAILP[0], "Spine")
    k.joint("Tail2", TAILP[1], "Tail1")
    k.joint("Tail3", TAILP[2], "Tail2", tail=(0, 0.45, -0.04))


# ------------------------------------------------------------------ animation
import petkit as pk
import _common as cm

LEGS = ["Leg_L", "Leg_R"]
TAIL = ["Tail1", "Tail2", "Tail3"]
# ground pose of the wings: (arm up, arm forward-sweep, arm twist, outer-wing fold about finger 3; + = folds down)
FOLD = dict(up=25, fwd=-15, twist=0, tip=95)


def hinge_axis(side):
    s = 1 if side == "L" else -1
    return (X(F3, s) - X(WRIST, s)).normalized()


def root_axis(side):
    s = 1 if side == "L" else -1
    return (X(BODY_B, s) - X(SHOULDER, s)).normalized()


def arm_axis(side):
    s = 1 if side == "L" else -1
    return (X(WRIST, s) - X(SHOULDER, s)).normalized()


def wings(k, f, up, fwd, twist=0.0, tip=0.0, side=None):
    """arm pose + outer-wing hinge fold. The flap turns about the wing ROOT line (shoulder -> body attachment), so the
    membrane's body edge stays on the body; fwd = small sweep about the vertical, twist = about the arm.
    side=None keys both wings mirrored."""
    from mathutils import Quaternion
    for sd, sx in (("L", 1), ("R", -1)):
        if side and sd != side:
            continue
        extra = Quaternion((0, 0, 1), math.radians(-sx * fwd)) @ Quaternion(arm_axis(sd), math.radians(sx * twist))
        cm.key_axis(k, "Wing_" + sd, f, root_axis(sd), -sx * up, extra=extra)
        cm.key_axis(k, "WingTip_" + sd, f, hinge_axis(sd), sx * tip)


def folded(k, f, du=0.0, dfwd=0.0, dtip=0.0, side=None):
    wings(k, f, FOLD["up"] + du, FOLD["fwd"] + dfwd, FOLD["twist"], FOLD["tip"] + dtip, side)


def rest_keys(k, f, z=0.0, pitch=0.0):
    k.key("Spine", f, rot=(pitch, 0, 0), loc=(0, 0, z))
    k.key("Chest", f, rot=(0, 0, 0))
    k.key("Neck", f, rot=(0, 0, 0))
    k.key("Head", f, rot=(0, 0, 0))
    k.key("Jaw", f, rot=(2, 0, 0))
    folded(k, f)
    for b in TAIL:
        k.key(b, f, rot=(0, 0, 0))


# ---- flight
PITCH, NECK, HEAD = 30.0, 26.0, -44.0
TOP, BOT = 28.0, -48.0
THI, SHI, FOO = 64.0, -30.0, 95.0


def _ease(u):
    return 0.5 - 0.5 * math.cos(math.pi * u)


def stroke(ph):
    """one beat: power downstroke ph 0 -> 0.45 (outer wing lags up, then follows through),
    recovery upstroke 0.45 -> 1 (outer wing folds down on the hinge to slip through the air)"""
    ph %= 1.0
    if ph < 0.45:
        u = ph / 0.45
        return dict(up=TOP + (BOT - TOP) * _ease(u), fwd=10 * math.sin(math.pi * u) - 2,
                    twist=12 * math.sin(math.pi * u), tip=-5 - 10 * math.sin(math.pi * u) + 13 * u)
    u = (ph - 0.45) / 0.55
    return dict(up=BOT + (TOP - BOT) * _ease(u), fwd=-2 - 8 * math.sin(math.pi * u),
                twist=-8 * math.sin(math.pi * u), tip=8 + 34 * math.sin(math.pi * u) - 13 * u)


def fly_legs(k, f, ph):
    for s, side in ((1, "L"), (-1, "R")):
        p = ph + 0.03 * s
        k.key("Leg_" + side, f, rot=(THI + 9 * math.sin(2 * math.pi * (p - 0.15)), 0, -s * 2), loc=(0, 0, 0))
        k.key("Shin_" + side, f, rot=(SHI + 12 * math.sin(2 * math.pi * (p - 0.30)), 0, 0))
        k.key("Foot_" + side, f, rot=(FOO + 16 * math.sin(2 * math.pi * (p - 0.42)), 0, 0))


def fly_pose(k, f, ph, legs=True):
    w = stroke(ph)
    wings(k, f, w["up"], w["fwd"], w["twist"], w["tip"])
    k.key("Spine", f, rot=(PITCH - 4 * math.sin(2 * math.pi * (ph - 0.1)), 0, 0),
          loc=(0, 0, 0.10 * math.cos(2 * math.pi * (ph - 0.45))))
    k.key("Chest", f, rot=(-3 * math.sin(2 * math.pi * (ph - 0.2)), 0, 0))
    k.key("Neck", f, rot=(NECK + 4 * math.sin(2 * math.pi * (ph - 0.25)), 0, 0))
    k.key("Head", f, rot=(HEAD - 6 * math.sin(2 * math.pi * (ph - 0.32)), 0, 0))
    k.key("Jaw", f, rot=(3, 0, 0))
    for i, b in enumerate(TAIL):
        k.key(b, f, rot=(-6 + 6 * math.sin(2 * math.pi * (ph - 0.3 - 0.12 * i)),
                         3 * math.sin(2 * math.pi * (ph - 0.2 * i)), 0))
    if legs:
        fly_legs(k, f, ph)


def fly(k):
    n = 28
    k.new_action("fly", n, True)
    for f in range(0, n + 1):
        fly_pose(k, f, f / n)
    k.finish()


def plant_frames(k, frames, z=0.0):
    import bpy
    k.bake_bezier_now()
    for f in frames:
        bpy.context.scene.frame_set(f)
        for leg in LEGS:
            k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, z)))


def lift_air_frames(k, frames, target=0.02):
    """FLOOR RULE for airborne frames: raise the Spine just enough that no vertex goes below `target`
    (measured per frame after the keys are baked; keyed every frame of the range)."""
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


def takeoff(k):
    """crouch, wings unfold high, LAUNCH (event) on a huge downstroke, legs push then pull back into flight"""
    n = 30
    k.new_action("takeoff", n, False)
    rest_keys(k, 0)
    for f, z, p, ch, hd, w in ((5, -0.12, 8, 4, -10, (0, -20, 0, 60)), (10, -0.24, 12, 6, -16, (TOP + 8, 0, -8, -6)),
                               (13, 0.06, 18, 0, -26, (-10, 10, 12, -12)), (16, 0.10, 26, -2, -38, (BOT, 6, 4, 6))):
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(ch, 0, 0))
        k.key("Neck", f, rot=(p * 0.6, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(2, 0, 0))
        wings(k, f, *w)
        for b in TAIL:
            k.key(b, f, rot=(-4 - p * 0.3, 0, 0))
    fly_pose(k, 23, 0.0)
    fly_pose(k, n, 0.45)
    plant_frames(k, range(0, 14))
    for s, side in ((1, "L"), (-1, "R")):               # legs leave the ground: push long, then pull back
        k.key("Leg_" + side, 14, rot=(30, 0, 0), loc=(0, 0, 0))
        k.key("Shin_" + side, 14, rot=(-8, 0, 0))
        k.key("Foot_" + side, 14, rot=(55, 0, 0))
        k.key("Leg_" + side, 18, rot=(40, 0, 0), loc=(0, 0, 0))
        k.key("Shin_" + side, 18, rot=(-36, 0, 0))
        k.key("Foot_" + side, 18, rot=(85, 0, 0))
    lift_air_frames(k, range(14, n + 1))
    k.finish(loop=False)
    k.events["takeoff"] = {"launch": round(11 / n, 3)}


def land(k):
    """flare upright, braking beats with the wings swept forward, legs swing forward and reach, touch (event), absorb"""
    n = 30
    k.new_action("land", n, False)
    fly_pose(k, 0, 0.0)
    for f, p, z, nk, hd, w, legs in (
            (6, 12, 0.04, 14, -28, (20, 20, -14, -4), (-5, -18, 10)),
            (10, -6, 0.08, 6, -12, (-20, 24, -14, 6), (-24, 6, -15)),
            (13, -8, 0.08, 4, -8, (18, 18, -10, -6), (-22, 12, -20)),
            (15, -6, 0.04, 2, -6, (0, 8, -6, 10), (-14, 6, -8))):
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(-4, 0, 0))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(3, 0, 0))
        wings(k, f, *w)
        for b in TAIL:
            k.key(b, f, rot=(8, 0, 0))
        for s, side in ((1, "L"), (-1, "R")):
            k.key("Leg_" + side, f, rot=(legs[0], 0, 0), loc=(0, 0, 0))
            k.key("Shin_" + side, f, rot=(legs[1], 0, 0))
            k.key("Foot_" + side, f, rot=(legs[2], 0, 0))
    for f, z, p, w in ((17, -0.20, 8, (10, 0, 0, 30)), (21, -0.10, 4, (8, -12, 0, 95)), (26, 0.02, 0, None)):
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(2, 0, 0))
        k.key("Neck", f, rot=(p * 0.5, 0, 0))
        k.key("Head", f, rot=(-p * 0.4, 0, 0))
        k.key("Jaw", f, rot=(2, 0, 0))
        if w:
            wings(k, f, *w)
        else:
            folded(k, f)
        for b in TAIL:
            k.key(b, f, rot=(-2, 0, 0))
    rest_keys(k, n)
    lift_air_frames(k, range(0, 17))                     # still coming down: feet stay above the floor
    plant_frames(k, range(17, n + 1))
    k.finish(loop=False)
    k.events["land"] = {"touch": round(17 / n, 3)}


# ---- ground (every move here is the Wyvern's own)
def idle(k):
    """sentinel on a cliff: rises tall on its neck to survey, lowers its head to stare you down with a low growl,
    stretches ONE wing wide (left, later right) and folds it back, tail sweeping slowly along the ground."""
    n = 150
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 2):
        b = pk.wave(f, n, 0, 3)
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, 0.012 * b))
        k.key("Chest", f, rot=(-1.2 * b, 0, 0))
        cm.chain(k, f, n, TAIL, sway=7, pitch=0, cycles=1, lag=0.16, grow=0.5)
    for f, nk, ny, hd, hy in ((0, 0, 0, 0, 0), (14, -12, 0, -6, 0), (34, -12, 12, -6, 8), (52, -12, -10, -6, -8),
                              (66, 0, 0, 0, 0), (96, 0, 0, 0, 0), (106, 14, 0, -16, 0), (124, 14, 0, -16, 0),
                              (136, 0, 0, 0, 0), (150, 0, 0, 0, 0)):
        k.key("Neck", f, rot=(nk, ny, 0))
        k.key("Head", f, rot=(hd, hy, 0))
    for f, j in ((0, 2), (106, 2), (110, 10), (124, 10), (130, 2), (150, 2)):
        k.key("Jaw", f, rot=(j, 0, 0))
    for side, a in (("L", 66), ("R", 136)):
        for f, du, df, dt in ((0, 0, 0, 0), (a - 10, 0, 0, 0), (a, 70, 50, -150), (a + 8, 74, 54, -152),
                              (a + 14, 0, 0, 0), (n, 0, 0, 0)):
            if 0 <= f <= n:
                folded(k, f, du, df, dt, side=side)
    cm.plant(k, n, legs=LEGS)
    k.finish()
    k.meta["planted"] = LEGS


def walk(k):
    n = 28

    def body(f):
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(1.5 * pk.wave(f, n, 0.1, 2), 4 * pk.wave(f, n, 0.0), 3.5 * pk.wave(f, n, 0.0)),
              loc=(0, 0, 0.04 * b))
        k.key("Chest", f, rot=(0, -3 * pk.wave(f, n, 0.05), -2 * pk.wave(f, n, 0.0)))
        k.key("Neck", f, rot=(3 + 2 * pk.wave(f, n, 0.15, 2), -2 * pk.wave(f, n, 0.1), 0))
        k.key("Head", f, rot=(-3 - 2 * pk.wave(f, n, 0.25, 2), 2 * pk.wave(f, n, 0.1), 0))
        k.key("Jaw", f, rot=(2, 0, 0))
        folded(k, f, du=3 * pk.wave(f, n, 0.3, 2))
        cm.chain(k, f, n, TAIL, sway=-8, pitch=0, cycles=1, lag=0.15, grow=0.5)
    return cm.biped_walk(k, n, 0.24, 0.16, body, legs=(("Leg_L", 0.0), ("Leg_R", 0.5)), duty=0.6)


def roar(k):
    """STORM ROAR: pulls back, then lunges the head forward and low with the jaw wide, both wings flaring up and
    forward like a cape, tail lashing once."""
    n = 60
    k.new_action("roar", n, False)
    for f, p, nk, hd, jw, w in ((0, 0, 0, 0, 2, None), (10, -6, -14, -10, 8, (10, -12, 0, 95)),
                                (18, 10, 34, -16, 36, (30, 20, -10, 20)), (44, 10, 36, -18, 38, (34, 24, -10, 16)),
                                (52, 2, 6, -4, 6, (12, -12, 0, 95)), (60, 0, 0, 0, 2, None)):
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, -0.04 * (p > 0)))
        k.key("Chest", f, rot=(p * 0.3, 0, 0))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        if w:
            wings(k, f, *w)
        else:
            folded(k, f)
    for f in range(0, n + 1, 2):
        cm.chain(k, f, 30, TAIL, sway=16 if 16 <= f <= 46 else 0, pitch=0, cycles=1, lag=0.2, grow=0.6)
    cm.plant(k, n, legs=LEGS)
    k.finish(loop=False)


def thunderclap(k):
    """SIGNATURE: rears up with wings wide, crouches, slams both wings down so hard it LEAPS, roars mid-air with
    wings low, stomps back down with a tail slam and holds a wings-up power pose before folding."""
    n = 76
    k.new_action("act_thunderclap", n, False)
    K = [  # f, spine z, spine pitch, chest, neck, head, jaw, wings (up, fwd, twist, tip), tail pitch
        (0, 0.0, 0, 0, 0, 0, 2, None, 0),
        (12, 0.02, -10, -8, -8, -12, 10, (20, -10, -6, -5), 14),          # tail lifts as it rears back
        (20, -0.24, 10, 2, 6, -10, 4, (TOP + 6, 2, -10, -8), 4),
        (25, 0.42, 18, -4, 4, -28, 34, (BOT, 12, 12, 10), -14),
        (31, 0.46, 14, -6, 0, -30, 38, (BOT, 10, 10, 6), -18),
        (38, 0.10, 10, -4, 6, -22, 30, (26, -6, 0, 30), -6),
        (42, -0.13, 8, 4, 14, -10, 8, (28, -10, 0, 20), 14),
        (50, -0.04, -6, -6, -8, -8, 12, (24, 8, -6, -4), 4),
        (60, 0.0, -6, -6, -8, -8, 12, (24, 8, -6, -4), 0),
        (68, 0.0, 0, 0, 0, 0, 2, None, 0),
        (76, 0.0, 0, 0, 0, 0, 2, None, 0)]
    for f, z, p, ch, nk, hd, jw, w, tp in K:
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(ch, 0, 0))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        if w:
            wings(k, f, *w)
        else:
            folded(k, f)
        for i, b in enumerate(TAIL):
            k.key(b, f, rot=(tp * (1 + 0.3 * i), 0, 0))
    plant_frames(k, list(range(0, 23)) + list(range(41, n + 1)))
    for s, side in ((1, "L"), (-1, "R")):
        for f, a, b_, c in ((25, 18, -6, 40), (31, 34, -40, 70), (37, 2, -6, 12)):
            k.key("Leg_" + side, f, rot=(a, 0, 0), loc=(0, 0, 0))
            k.key("Shin_" + side, f, rot=(b_, 0, 0))
            k.key("Foot_" + side, f, rot=(c, 0, 0))
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    fly(k)
    takeoff(k)
    land(k)
    roar(k)
    thunderclap(k)
    return stride


def check_pairs():
    W = ["Wing_L", "WingTip_L", "Wing_R", "WingTip_R"]
    pairs = [("Wing_L", "WingTip_L"), ("Wing_R", "WingTip_R"), ("WingTip_L", "WingTip_R"), ("Wing_L", "Wing_R"),
             ("WingTip_L", "Wing_R"), ("Wing_L", "WingTip_R")]
    for w in W:
        for b in ("Head", "Neck", "Tail1", "Tail2", "Leg_L", "Leg_R", "Shin_L", "Shin_R"):
            pairs.append((w, b))
    return pairs


def joints():
    """rest-space hinge/knuckle segments for the overlap checker"""
    out = []
    for s in (1, -1):
        W, f3 = X(WRIST, s), X(F3, s)
        side = "L" if s > 0 else "R"
        out += [(W, f3, 0.12, "Wing_" + side), (W, W, 0.22, "Wing_" + side)]
    return out
