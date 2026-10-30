# ------------------------------------------------------------------ animation (clips 2026-10-27, refs: ANIM_REFS.md)
# BASE POSE (review 2 M2, lead ruling): every clip keys the Spine at the walk's 45 deg yaw with the six feet planted on
# the yawed rest spots, so the runtime idle <-> walk crossfade turns nothing (only the leg phase blends). The game moves
# pets along their facing (-Y); the walk carries the body at 45 deg (a diagonal scuttle, the crusher side leads) and
# steps the legs along the travel axis in alternating tripods.
import petkit as pk
import _common as cm

LEGS6 = ["Leg_%d" % j for j in range(1, 7)]
YAW_WALK = 45.0                 # r2 (M1, lead ruling): a 45 deg diagonal scuttle
BASE_YAW = YAW_WALK             # r3 (review 2 M2): idle / roar / act rest at the same yaw
WALK_OFF = [("Leg_1", 0.00), ("Leg_5", 0.04), ("Leg_3", 0.08), ("Leg_4", 0.50), ("Leg_2", 0.54), ("Leg_6", 0.58)]


def curve(keys, f):
    """smoothstep through (frame, value) keys"""
    for (f0, v0), (f1, v1) in zip(keys, keys[1:]):
        if f0 <= f <= f1:
            u = (f - f0) / float(f1 - f0) if f1 > f0 else 1.0
            return v0 + (v1 - v0) * u * u * (3 - 2 * u)
    return keys[-1][1] if f > keys[-1][0] else keys[0][1]


def about_spine(k, P, yaw):
    J = k.J["Spine"]
    return J + Quaternion((0, 0, 1), math.radians(yaw)) @ (Vector(P) - J)


def ankle_to(k, leg, f, P, yaw=0.0, toe=0.0):
    """put the ANKLE of `leg` at world point P; the dactyl keeps its rest direction turned by the body yaw"""
    foot = k.legs2[leg]["foot"]
    hipR, ankR = k.J[leg], k.J[foot]
    k.solve_leg(leg, f, Vector((P.x - (ankR.x - hipR.x), P.y - (ankR.y - hipR.y), P.z - ankR.z)), toe=toe)
    k._aim(foot, f, Quaternion((0, 0, 1), math.radians(yaw)) @ Quaternion((1, 0, 0), math.radians(toe)))


def plant6(k, frames, legs=None, yaw=BASE_YAW):
    import bpy
    k.bake_bezier_now()
    for f in frames:
        bpy.context.scene.frame_set(f)
        for leg in (legs or LEGS6):
            ankle_to(k, leg, f, about_spine(k, k.J[k.legs2[leg]["foot"]], yaw), yaw=yaw)


def claw(k, f, side, lift=0.0, spread=0.0, fore=0.0, wrist=0.0, pinch=0.0):
    """FK claw: lift + = the merus rises (about merus x up), spread + = swings outward (yaw), fore + = the carpus
    rises, wrist + = the palm tips up (about its out axis), pinch + = the dactyl opens"""
    s = 1 if side == "L" else -1
    S, E, W, F, a, o, out = claw_frame(side)
    dm = (E - S).normalized()
    ax_up = dm.cross(Vector((0, 0, 1))).normalized()
    cm.key_axis(k, "Arm_" + side, f, ax_up, lift, extra=Quaternion((0, 0, 1), math.radians(s * spread)))
    dfo = (W - E).normalized()
    cm.key_axis(k, "Fore_" + side, f, dfo.cross(Vector((0, 0, 1))).normalized(), fore)
    cm.key_axis(k, "Claw_" + side, f, out * s, wrist)
    cm.key_axis(k, "Pincer_" + side, f, out * s, -pinch)


def eyes(k, f, l=0.0, r=0.0, up=0.0):
    k.key("Eye_L", f, rot=(-up, l, 0))
    k.key("Eye_R", f, rot=(-up, r, 0))


def body(k, f, up=0.0, pitch=0.0, roll=0.0):
    """the carapace at the base yaw; up = rise (BU), pitch + = nose down, roll"""
    k.key("Spine", f, rot=(pitch, BASE_YAW, roll), loc=(0, 0, up))


def idle(k):
    """CLAW GUARD (plan; ref #7): the crusher lifts 20 deg to guard and holds, the eyestalks swivel one at a time with
    freezes between, the cutter taps the shell once (f70). Starts and ends in the base pose (portrait = f0)."""
    n = 120
    k.new_action("idle", n, True)
    guard = [(0, 0), (12, 0), (28, 20), (98, 20), (114, 0), (120, 0)]
    gfore = [(0, 0), (12, 0), (28, 8), (98, 8), (114, 0), (120, 0)]
    gpin = [(0, 0), (14, 0), (26, 10), (34, 4), (98, 4), (112, 0), (120, 0)]
    tap = [(0, 0), (60, 0), (66, 12), (70, -1), (74, 0), (120, 0)]
    eyl = [(0, 0), (18, 0), (24, 10), (44, 10), (50, 0), (120, 0)]
    eyr = [(0, 0), (54, 0), (60, -10), (80, -10), (86, 0), (120, 0)]
    for f in range(0, n + 1, 2):
        body(k, f, up=0.004 * (0.5 - 0.5 * math.cos(4 * math.pi * f / n)))
        claw(k, f, "R", lift=curve(guard, f), fore=curve(gfore, f), pinch=curve(gpin, f))
        claw(k, f, "L", lift=curve(tap, f), pinch=0.6 * curve(tap, f))
        eyes(k, f, l=curve(eyl, f), r=curve(eyr, f), up=2 * pk.wave(f, n, 0.1, 1))
        k.key("Mouth", f, rot=(3 * max(0.0, pk.wave(f, n, 0.3, 2)), 0, 0))
    plant6(k, range(0, n + 1))
    k.finish()
    k.meta["planted"] = LEGS6
    k.events["idle"] = {"tap": round(70 / n, 3)}


def walk(k):
    """diagonal scuttle (refs R1-R4): tripods along the travel line, body at 45 deg, claws folded low (review 2 N5)"""
    import bpy
    n, S, LIFT, duty = 30, 0.085, 0.07, 0.55
    k.new_action("walk", n, True)
    for f in range(0, n + 1, 2):
        k.key("Spine", f, rot=(0, YAW_WALK, 1.2 * pk.wave(f, n, 0.1, 2)),
              loc=(0, 0, 0.010 * (0.5 - 0.5 * math.cos(4 * math.pi * f / n))))
        for sd in ("L", "R"):
            claw(k, f, sd, lift=-10 + 3 * pk.wave(f, n, 0.0 if sd == "L" else 0.5), fore=-4,
                 wrist=2 * pk.wave(f, n, 0.2))
        eyes(k, f, l=-6 * pk.wave(f, n, 0.22), r=-6 * pk.wave(f, n, 0.22))       # the eyes lag (plan)
        k.key("Mouth", f, rot=(0, 0, 0))
    k.bake_bezier_now()
    for f in range(0, n + 1):
        bpy.context.scene.frame_set(f)
        for leg, off in WALK_OFF:
            A0 = about_spine(k, k.J[k.legs2[leg]["foot"]], YAW_WALK)
            t = ((f / n) + off) % 1.0
            if t < duty:
                y, z = -S + 2 * S * (t / duty), 0.0
            else:
                u = (t - duty) / (1 - duty)
                y, z = S - 2 * S * (0.5 - 0.5 * math.cos(math.pi * u)), LIFT * math.sin(math.pi * u)
            ankle_to(k, leg, f, A0 + Vector((0, y, z)), yaw=YAW_WALK)
    k.finish()
    k.meta["walk_cycle"] = n
    k.meta["legs"] = list(WALK_OFF)
    k.meta["duty"] = duty
    k.events["walk"] = {"sand1": round(13.8 / n, 3), "sand2": round(28.8 / n, 3)}   # tripod B / A touch-downs
    return 2 * S / duty


def roar(k):
    """CLACK THREAT (plan; refs #6 + #5): a short crouch, the body rises 0.05 H and both claws lift forward 25 deg;
    three clacks (cocked open 2 f -> snap shut 2 f -> hard stop); the mandibles open; lower and settle."""
    n = 60
    k.new_action("roar", n, False)
    rise = [(0, 0), (4, -0.012), (14, 0.052), (40, 0.052), (52, 0.0), (60, 0.0)]
    lift = [(0, 0), (4, -4), (14, 25), (40, 25), (52, 0), (60, 0)]
    spread = [(0, 0), (14, 14), (40, 14), (52, 0), (60, 0)]
    fore = [(0, 0), (14, 12), (40, 12), (52, 0), (60, 0)]
    pin = [(0, 0), (12, 14), (16, 14), (20, 30), (22, 0), (24, 8), (28, 30), (30, 0), (32, 8), (36, 30), (38, 0),
           (40, 4), (52, 0), (60, 0)]
    mouth = [(0, 0), (14, 0), (20, 14), (44, 14), (52, 0), (60, 0)]
    for f in range(0, n + 1, 2):
        u = curve(rise, f)
        body(k, f, up=u, pitch=-4 * u / 0.052 if u > 0 else 0.0)
        for sd in ("L", "R"):
            claw(k, f, sd, lift=curve(lift, f), spread=curve(spread, f), fore=curve(fore, f), pinch=curve(pin, f))
        eyes(k, f, up=8 * max(0.0, u) / 0.052)
        k.key("Mouth", f, rot=(curve(mouth, f), 0, 0))
    plant6(k, range(0, n + 1))
    k.finish(loop=False)
    k.events["roar"] = {"clack1": round(22 / n, 3), "clack2": round(30 / n, 3), "clack3": round(38 / n, 3),
                        "bubble": round(24 / n, 3)}


def act_semaphore(k):
    """THE FIDDLER WAVE (plan; refs F1-F3): stand tall, the crusher unfolds up 60 deg and waves three slow arcs
    (slow up-sweep, quicker return), points straight out and holds while the cutter taps twice, folds back down, rest.
    Legs planted every frame."""
    n = 100
    k.new_action("act_semaphore", n, False)
    up = [(0, 0), (18, 1), (88, 1), (100, 0)]
    lift_r = [(0, 0), (18, 45), (62, 45), (66, 32), (72, 32), (86, 0), (100, 0)]
    fore_r = [(0, 0), (18, 12), (26, 42), (31, 8), (40, 42), (45, 8), (54, 42), (59, 12), (64, 0), (72, 0), (86, 0),
              (100, 0)]
    spread_r = [(0, 0), (18, 30), (62, 30), (66, 44), (72, 44), (86, 0), (100, 0)]
    wrist_r = [(0, 0), (18, -10), (62, -10), (66, 0), (100, 0)]
    pin_r = [(0, 0), (18, 10), (62, 10), (66, 2), (86, 0), (100, 0)]
    tap_l = [(0, 0), (18, -6), (62, -6), (64, 6), (66, -6), (68, 6), (70, -6), (80, -6), (90, 0), (100, 0)]
    for f in range(0, n + 1, 2):
        u = curve(up, f)
        body(k, f, up=0.05 * u, pitch=-3 * u, roll=-2 * u)
        claw(k, f, "R", lift=curve(lift_r, f), spread=curve(spread_r, f), fore=curve(fore_r, f),
             wrist=curve(wrist_r, f), pinch=curve(pin_r, f))
        claw(k, f, "L", lift=curve(tap_l, f))
        eyes(k, f, up=6 * u, r=-8 * u)
        k.key("Mouth", f, rot=(0, 0, 0))
    plant6(k, range(0, n + 1))
    k.finish(loop=False)
    k.events["act_semaphore"] = {"wave1": round(26 / n, 3), "wave2": round(40 / n, 3), "wave3": round(54 / n, 3),
                                 "tap1": round(66 / n, 3), "tap2": round(70 / n, 3)}


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    act_semaphore(k)
    return stride
