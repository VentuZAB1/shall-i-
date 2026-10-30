# ------------------------------------------------------------------ animation (plan section 7 + ANIM_REFS.md)
import petkit as pk
import _common as cm
import bpy

LEGS2 = ["Leg_L", "Leg_R"]


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


def wrist(k, side, f, P, toe=0.0):
    """2-bone arm IK: put the wrist at world point P (fist kept level unless toe tilts it)"""
    s = 1 if side == "L" else -1
    Sv, Wv = X(S, s), X(W, s)
    P = Vector(P)
    k.solve_leg("Arm_" + side, f, Vector((Sv.x + P.x - Wv.x, Sv.y + P.y - Wv.y, P.z - Wv.z)), toe=toe)


def rest_wrist(side):
    return X(W, 1 if side == "L" else -1)


def plant_feet(k, f):
    for leg in LEGS2:
        k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, 0.0)))


def plates(k, f, a):
    """lift the outer rim of both shoulder crusts by a deg"""
    k.key("Plate_L", f, rot=(0, 0, -a))
    k.key("Plate_R", f, rot=(0, 0, a))


def idle(k):
    """PLATE SETTLE: slow hip sway (yaw +-4), three breaths; the shoulder crusts lift 4 deg and settle twice (f30-50);
    the head lowers 6 deg at f55-75 and is back by f100. Feet planted, arms hang."""
    n = 120
    k.new_action("idle", n, True)
    HD = [(0, 0.0), (55, 0.0), (65, 6.0), (75, 6.0), (100, 0.0), (120, 0.0)]
    PL = [(0, 0.0), (30, 0.0), (35, 4.0), (40, 0.5), (45, 4.0), (50, 0.0), (120, 0.0)]
    for f in range(0, n + 1, 2):
        br = 0.5 + 0.5 * pk.wave(f, n, 0.25, 3)
        k.key("Spine", f, rot=(0, 4.0 * pk.wave(f, n, 0.0, 1), 0), loc=(0, 0, -0.006 * br))
        k.key("Chest", f, rot=(-1.2 * br, -1.5 * pk.wave(f, n, 0.05, 1), 0))
        k.key("Head", f, rot=(tab(HD, f) + 0.6 * br, -1.5 * pk.wave(f, n, 0.1, 1), 0))
        k.key("Jaw", f, rot=(2.0 + 1.0 * br, 0, 0))
        plates(k, f, tab(PL, f))
    cm.plant(k, n, legs=LEGS2)
    k.finish()
    k.meta["planted"] = LEGS2
    k.events["idle"] = {"settle1": round(40 / n, 3), "settle2": round(50 / n, 3)}


def walk(k):
    """KNUCKLE WALK (Muybridge plate 747): diagonal sequence LH, RF, RH, LF; hunched (torso -0.07, chest +9 deg) so the
    fists plant on the snow; the swinging fist lifts with the elbow out; the chest yaws with the arm in stance; the head
    stays level."""
    n = 48
    S_, LIFT, DUTY = 0.12, 0.07, 0.62
    legs = [("Leg_L", 0.0), ("Arm_L", 0.25), ("Leg_R", 0.5), ("Arm_R", 0.75)]
    k.new_action("walk", n, True)
    for f in range(0, n + 1, 2):
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(3.0 + 1.0 * pk.wave(f, n, 0.1, 2), 3 * pk.wave(f, n, 0.0), 2.0 * pk.wave(f, n, 0.05)),
              loc=(0, 0, -0.075 - 0.033 * b))
        k.key("Chest", f, rot=(6.0 + 1.0 * pk.wave(f, n, 0.15, 2), -5 * pk.wave(f, n, 0.0), -2 * pk.wave(f, n, 0.05)))
        k.key("Head", f, rot=(-9.0 - 1.0 * pk.wave(f, n, 0.2, 2), 3 * pk.wave(f, n, 0.0), 0))
        k.key("Jaw", f, rot=(3, 0, 0))
        plates(k, f, 1.0 + 1.0 * pk.wave(f, n, 0.3, 2))
    k.bake_bezier_now()
    sc = bpy.context.scene
    for f in range(0, n + 1):
        sc.frame_set(f)
        for leg, off in legs:
            T = pk.gait_target(k, leg, f, n, off, S_, LIFT, DUTY)
            if leg.startswith("Arm"):
                T = Vector((T.x, T.y, T.z - 0.10))               # knuckles on the snow, 0.10 below the hang height
                k.solve_leg(leg, f, T, toe=-10.0 * max(0.0, T.z + 0.10) / LIFT)
            else:
                k.solve_leg(leg, f, T)
    k.finish()
    k.meta["walk_cycle"] = n
    k.meta["legs"] = legs
    k.meta["duty"] = DUTY
    k.events["walk"] = {"stomp": 0.0}
    return (2 * S_) / DUTY


def roar(k):
    """SHOULDER-HEAVE BELLOW: the shoulders pull back (chest lifts back), two heaves (chest yaw +10 / -10, the arm on
    the forward shoulder swinging with it), the head up 15 deg, the jaw opens late (f20-45) showing the fangs; settles.
    No chest beat, no arms raised. Feet planted."""
    n = 60
    k.new_action("roar", n, False)
    # f, spine z, chest pitch, chest yaw, head pitch, jaw, plates
    P = [(0, 0.0, 0, 0, 0, 2, 0), (12, 0.02, -6, 0, -4, 3, 3), (17, 0.0, 2, 10, -12, 6, 2), (22, 0.0, 2, -10, -15, 16, 3),
         (28, 0.0, 0, 0, -15, 24, 4), (45, 0.0, 0, 0, -15, 22, 4), (52, 0.0, 0, 0, -6, 6, 1), (60, 0.0, 0, 0, 0, 2, 0)]
    for f, sz, cp, cy, hp, jw, pl in P:
        k.key("Spine", f, rot=(0, cy * 0.3, 0), loc=(0, 0, sz))
        k.key("Chest", f, rot=(cp, cy, 0))
        k.key("Head", f, rot=(hp - cp, -cy * 0.5, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        plates(k, f, pl)
        for side, sx in (("L", 1), ("R", -1)):                     # the arm on the heaving shoulder swings forward
            sw = max(0.0, sx * cy) / 10.0
            k.key("Arm_" + side, f, rot=(-8 * sw + 3 * (cp < 0), 0, 0))
            k.key("Fore_" + side, f, rot=(-6 * sw, 0, 0))
    for f in (32, 38):                                            # a slight tremble in the held bellow
        k.key("Jaw", f, rot=(26 if f == 32 else 22, 0, 0))
    k.bake_bezier_now()
    sc = bpy.context.scene
    for f in range(0, n + 1):
        sc.frame_set(f)
        plant_feet(k, f)
    k.finish(loop=False)
    k.events["roar"] = {"roar": round(24 / n, 3)}


def skid(k):
    """SIGNATURE - SNOW SKID AND BRAKE: drops onto wide-planted fists (chest -0.06H), sweeps both arms forward and back
    like a sled (skid1), slides the chest low with the feet planted (skid2), digs the fists in for a hard brake (brake,
    ice shards), pushes up with a shoulder heave and settles to rest. Root net 0."""
    n = 100
    k.new_action("act_skid", n, False)
    # f, spine z, spine pitch, chest pitch, chest yaw, head pitch, jaw, plates
    BODY = [(0, (0.0, 0, 0, 0, 0, 2, 0)), (10, (-0.08, 4, 12, 0, -10, 4, 2)), (16, (-0.10, 5, 15, 0, -13, 6, 3)),
            (22, (-0.11, 5, 16, 0, -14, 8, 4)), (34, (-0.12, 6, 17, 0, -14, 8, 4)), (42, (-0.14, 7, 18, 0, -15, 10, 5)),
            (52, (-0.13, 6, 17, 0, -14, 8, 4)), (56, (-0.11, 5, 14, 0, -12, 6, 3)), (58, (-0.14, 7, 19, 0, -16, 18, 6)),
            (62, (-0.14, 7, 19, 0, -16, 16, 6)), (66, (-0.12, 6, 16, 0, -14, 8, 4)), (74, (-0.02, 2, 2, 9, -4, 6, 3)),
            (80, (0.01, 0, -2, -7, -2, 4, 4)), (86, (0.0, 0, 0, 0, 0, 3, 1)), (92, (0.0, 0, 0, 0, 0, 2, 3)),
            (100, (0.0, 0, 0, 0, 0, 2, 0))]
    for f in range(0, n + 1, 2):
        sz, sp, cp, cy, hp, jw, pl = tab(BODY, f)
        k.key("Spine", f, rot=(sp, cy * 0.3, 0), loc=(0, 0, sz))
        k.key("Chest", f, rot=(cp, cy, 0))
        k.key("Head", f, rot=(hp, -cy * 0.4, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        plates(k, f, pl)
    k.bake_bezier_now()
    sc = bpy.context.scene
    # wrist targets (left side; the right is mirrored): rest -> planted wide -> sled sweeps -> slide -> dig -> rest
    R0 = tuple(rest_wrist("L"))
    WT = [(0, R0), (8, (0.66, -0.52, 0.44)), (16, (0.76, -0.62, 0.33)),       # plant wide on the snow
          (22, (0.74, -0.80, 0.36)), (28, (0.74, -0.42, 0.33)), (34, (0.74, -0.76, 0.35)),   # sled sweeps
          (42, (0.76, -0.70, 0.33)), (52, (0.76, -0.72, 0.33)),                           # slide low
          (55, (0.75, -0.74, 0.40)), (58, (0.76, -0.75, 0.31)), (64, (0.76, -0.75, 0.31)),   # cocked, DIG IN (brake)
          (74, (0.66, -0.56, 0.48)), (86, R0), (100, R0)]
    for f in range(0, n + 1):
        sc.frame_set(f)
        plant_feet(k, f)
        p = Vector(tab(WT, f))
        sweep = 1.0 if 16 < f < 36 else 0.0
        lift = 0.05 * sweep * max(0.0, math.sin(math.pi * (f - 16) / 6.0)) if sweep else 0.0
        for side, sx in (("L", 1), ("R", -1)):
            wrist(k, side, f, Vector((sx * p.x, p.y, p.z + (lift if side == "L" else lift))))
    k.finish(loop=False)
    k.events["act_skid"] = {"skid1": round(22 / n, 3), "skid2": round(42 / n, 3), "brake": round(58 / n, 3)}


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    skid(k)
    return stride


HEAD_XF = []
