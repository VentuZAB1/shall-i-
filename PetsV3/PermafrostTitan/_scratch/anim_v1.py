

# ------------------------------------------------------------------ animation (clips 2026-10-27, refs: ANIM_REFS.md)
# Heavy, slow, upright: the Titan never pounds or presses (the Frostcrown Dragon owns the press). The walk is the
# Plate-27 load walk; the act is the Plate-356 kneel and rise. Feet are IK-planted in every frame of idle / roar / act.
import petkit as pk
import _common as cm

LEGS = ("Leg_L", "Leg_R")


def curve(keys, f):
    """smoothstep through (frame, value) keys"""
    for (f0, v0), (f1, v1) in zip(keys, keys[1:]):
        if f0 <= f <= f1:
            u = (f - f0) / float(f1 - f0) if f1 > f0 else 1.0
            return v0 + (v1 - v0) * u * u * (3 - 2 * u)
    return keys[-1][1] if f > keys[-1][0] else keys[0][1]


def vcurve(keys, f):
    """curve() for (frame, Vector) keys"""
    for (f0, v0), (f1, v1) in zip(keys, keys[1:]):
        if f0 <= f <= f1:
            u = (f - f0) / float(f1 - f0) if f1 > f0 else 1.0
            return Vector(v0).lerp(Vector(v1), u * u * (3 - 2 * u))
    return Vector(keys[-1][1] if f > keys[-1][0] else keys[0][1])


def sn(f, n, ph=0.0, cyc=1):
    return math.sin(2 * math.pi * (cyc * f / n + ph))


def ankle_to(k, leg, f, A, toe=0.0):
    """IK: put the ankle of `leg` at world point A; toe = foot pitch (deg, + = toes down)"""
    foot = k.legs2[leg]["foot"]
    hipR, ankR = k.J[leg], k.J[foot]
    k.solve_leg(leg, f, Vector((A.x - (ankR.x - hipR.x), A.y - (ankR.y - hipR.y), A.z - ankR.z)), toe=toe)


def arms_fk(k, f, out=0.0, fwd=0.0, bend=0.0):
    """FK arms: out + = the arm swings away from the body, fwd + = swings forward, bend + = the elbow flexes"""
    for s, side in ((1, "L"), (-1, "R")):
        k.key("Arm_" + side, f, rot=(-fwd, 0, -s * out))
        k.key("Fore_" + side, f, rot=(-bend, 0, 0))
        k.key("Hand_" + side, f, rot=(0, 0, 0))


def idle(k):
    """WEIGHT SHIFT (plan): hip yaw +/-3 deg over one cycle, two slow breaths, the shoulders (pauldrons) settle 2 deg at
    f30 and f70, core pulses f40 / f100. No head tilt (the head stays level and forward). Feet planted."""
    n = 120
    k.new_action("idle", n, True)
    settle = [(0, 0), (26, 0), (30, 2), (42, 0), (66, 0), (70, 2), (82, 0), (120, 0)]
    for f in range(0, n + 1, 2):
        yaw = 3 * sn(f, n)
        br = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(0, yaw, 0), loc=(0, 0, -0.005 * br))
        k.key("Chest", f, rot=(-1.0 * br, -0.4 * yaw, 0))
        k.key("Head", f, rot=(1.0 * br, -0.6 * yaw, 0))
        k.key("Jaw", f, rot=(0, 0, 0))
        arms_fk(k, f, out=curve(settle, f), bend=1.0 * br)
    cm.plant(k, n, legs=LEGS)
    k.finish()
    k.meta["planted"] = list(LEGS)
    k.events["idle"] = {"frost1": round(30 / n, 3), "core1": round(40 / n, 3), "frost2": round(70 / n, 3),
                        "core2": round(100 / n, 3)}


def walk(k):
    """HEAVY LOAD WALK (Plate 27, W1-W5): flat-foot contacts, the body sinks just after each contact and rises at
    passing, low swing foot, upright torso, the weight rolls over the stance foot, arms swing only 4 deg."""
    n = 48
    half = n // 2
    dip = [(0, -0.012), (5, -0.035), (14, 0.004), (24, -0.012)]

    def body(f):
        t = f % half
        k.key("Spine", f, rot=(0.6, 3 * sn(f, n, 0.0), 2 * sn(f, n, 0.0)),
              loc=(0.022 * sn(f, n, 0.15), 0, curve(dip, t)))
        k.key("Chest", f, rot=(0, -2 * sn(f, n, 0.0), -1.5 * sn(f, n, 0.0)))
        k.key("Head", f, rot=(-0.6 - 0.8 * sn(f, n, 0.3, 2), -1 * sn(f, n, 0.0), 0))
        k.key("Jaw", f, rot=(0, 0, 0))
        for s, side in ((1, "L"), (-1, "R")):
            k.key("Arm_" + side, f, rot=(4 * s * sn(f, n, 0.0), 0, 0))           # opposite the same-side leg
            k.key("Fore_" + side, f, rot=(-3 - 2 * s * sn(f, n, 0.05), 0, 0))
            k.key("Hand_" + side, f, rot=(0, 0, 0))
    orig = k.solve_leg
    k.solve_leg = lambda leg, f, T, foot_z=0.0, toe=None: orig(leg, f, T, foot_z,
                                                               toe=10.0 * min(1.0, max(0.0, T.z) / 0.07))
    try:
        stride = cm.biped_walk(k, n, 0.20, 0.07, body, legs=(("Leg_L", 0.0), ("Leg_R", 0.5)), duty=0.62)
    finally:
        del k.solve_leg
    return stride


def roar(k):
    """CORE BELLOW (plan; refs #3 + #9): lean in and tuck (anticipation), then the head lifts 10 deg and the arms go out
    8 deg; the jaw opens late; the core pulses f22 / f34; hold to f50; a slower settle."""
    n = 66
    k.new_action("roar", n, False)
    K = [  # f, spine z, spine pitch, chest pitch, head pitch, jaw, arms out
        (0, 0.0, 0, 0, 0, 0, 0),
        (10, -0.012, 1, 3, 4, 0, -2),
        (22, 0.010, -1, -3, -10, 8, 8),
        (27, 0.010, -1, -3, -10, 16, 8),
        (34, 0.014, -1.5, -3.5, -10, 15, 9),
        (50, 0.010, -1, -3, -9, 14, 8),
        (58, 0.0, 0, -0.5, -2, 4, 3),
        (66, 0.0, 0, 0, 0, 0, 0)]
    for f, z, sp, ch, hd, jw, ao in K:
        k.key("Spine", f, rot=(sp, 0, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(ch, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        arms_fk(k, f, out=ao, bend=max(0.0, ao) * 0.6)
    cm.plant(k, n, legs=LEGS)
    k.finish(loop=False)
    k.events["roar"] = {"core1": round(22 / n, 3), "glint": round(22 / n, 3), "icedust": round(24 / n, 3),
                        "core2": round(34 / n, 3)}


DROP = 0.30          # pelvis drop of the kneel (right knee cap on the snow)


def act_kneelrise(k):
    """KNEEL AND RISE (plan; Plate 356 K1-K4 + #9): the left foot steps forward, the body drops straight down and the
    right knee lands (ice crack), the right toes tuck, the head bows 12 deg, the fists come to rest over the thighs;
    the kneel holds while the core pulses twice; the rise starts with a forward lean, then the front leg drives up,
    the right foot comes through and the left foot steps back; exact rest."""
    import bpy
    n = 100
    k.new_action("act_kneelrise", n, False)
    SP = [  # f, x, y, z, spine pitch, chest pitch, head pitch
        (0, 0.0, 0.0, 0.0, 0, 0, 0), (6, -0.03, 0.0, -0.01, 0, 0, 0),
        (18, 0.0, -0.04, -DROP, 4, 2, 12), (34, 0.0, -0.04, -DROP + 0.006, 4, 2, 12),
        (50, 0.0, -0.04, -DROP, 4, 2, 12),
        (58, 0.0, -0.09, -DROP + 0.01, 10, 4, 6), (70, 0.0, -0.05, -0.12, 6, 2, 3), (80, 0.0, -0.01, -0.02, 1, 0, 0),
        (84, 0.0, 0.0, 0.0, 0, 0, 0), (100, 0.0, 0.0, 0.0, 0, 0, 0)]
    ARM = [(0, 0, 0, 0), (18, 4, 14, 22), (50, 4, 14, 22), (62, 2, 6, 8), (80, 0, 0, 0), (100, 0, 0, 0)]
    for f in range(0, n + 1, 2):
        x = curve([(a[0], a[1]) for a in SP], f)
        y = curve([(a[0], a[2]) for a in SP], f)
        z = curve([(a[0], a[3]) for a in SP], f)
        k.key("Spine", f, rot=(curve([(a[0], a[4]) for a in SP], f), 0, 0), loc=(x, y, z))
        k.key("Chest", f, rot=(curve([(a[0], a[5]) for a in SP], f), 0, 0))
        k.key("Head", f, rot=(curve([(a[0], a[6]) for a in SP], f), 0, 0))
        k.key("Jaw", f, rot=(0, 0, 0))
        arms_fk(k, f, out=curve([(a[0], a[1]) for a in ARM], f), fwd=curve([(a[0], a[2]) for a in ARM], f),
                bend=curve([(a[0], a[3]) for a in ARM], f))
    k.bake_bezier_now()
    aL, aR = k.J["Foot_L"].copy(), k.J["Foot_R"].copy()
    L = [(0, aL), (2, aL), (5, aL + Vector((0, -0.10, 0.06))), (9, aL + Vector((0, -0.22, 0.0))),
         (70, aL + Vector((0, -0.22, 0.0))), (74, aL + Vector((0, -0.11, 0.05))), (79, aL), (100, aL)]
    R = [(0, aR), (6, aR), (12, aR + Vector((0, 0.20, 0.08))), (18, aR + Vector((0, 0.34, 0.135))),
         (52, aR + Vector((0, 0.34, 0.135))), (62, aR + Vector((0, 0.24, 0.10))), (70, aR + Vector((0, 0.08, 0.07))),
         (76, aR), (100, aR)]
    TR = [(0, 0), (6, 0), (18, 38), (52, 38), (62, 26), (70, 8), (76, 0), (100, 0)]
    TL = [(0, 0), (2, 0), (5, 8), (9, 0), (70, 0), (74, 8), (79, 0), (100, 0)]
    for f in range(0, n + 1):
        bpy.context.scene.frame_set(f)
        ankle_to(k, "Leg_L", f, vcurve(L, f), toe=curve(TL, f))
        ankle_to(k, "Leg_R", f, vcurve(R, f), toe=curve(TR, f))
    k.finish(loop=False)
    k.events["act_kneelrise"] = {"icecrack": round(18 / n, 3), "core1": round(30 / n, 3), "core2": round(44 / n, 3)}


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    act_kneelrise(k)
    return stride
