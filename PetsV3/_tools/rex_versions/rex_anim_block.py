
# ------------------------------------------------------------------ animation
# Reference (owner rule 2026-10-10): animationreference.org "Tyrant Dragon Animation - MAYA 2023" (alessandro tommasi,
# tags #creature #3d-animation; no dinosaur clips exist on the site): ~0:08-0:12 the landing sinks into a deep crouch
# with the head dropped almost to the floor; ~0:16-0:20 it rises CHEST FIRST, the neck S-curves and the head arrives
# last (~5 frame lag) with the jaw half open. Used for the roar (anticipation crouch + chest-led rise) and the heavy
# body dip on every walk contact.
import petkit as pk
import _common as cm

LEGS = ["Leg_L", "Leg_R"]
TAIL = ["Tail1", "Tail2", "Tail3", "Tail4"]


def tail(k, f, pitch=0.0, yaw=0.0, each=(0.25, 0.5, 0.8, 1.0)):
    for b, g in zip(TAIL, each):
        k.key(b, f, rot=(pitch * g, yaw * g, 0))


def arms(k, f, up=0.0, spread=0.0, curl=0.0):
    for side, sx in (("L", 1), ("R", -1)):
        k.key("Arm_" + side, f, rot=(-up, 0, -sx * spread))
        k.key("Hand_" + side, f, rot=(-curl, 0, 0))


def plant_frames(k, frames, z=0.0):
    import bpy
    k.bake_bezier_now()
    for f in frames:
        bpy.context.scene.frame_set(f)
        for leg in LEGS:
            k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, z)))


def idle(k):
    """STORM KING WATCH: deep slow breaths (chest swells), a slow look left and right, a low sniff with two short
    nose lifts, a double jaw clack, the tiny claws flex, the tail sways low and heavy."""
    n = 120
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 2):
        b = pk.wave(f, n, 0, 3)
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, 0.010 * b))
        k.key("Chest", f, rot=(-1.5 * b, 0, 0))
        tail(k, f, -1 + 1.5 * pk.wave(f, n, 0.2, 2), 6 * pk.wave(f, n, 0.1, 1))
    for f, nk, ny, hd, hy, ht in ((0, 0, 0, 0, 0, 0), (26, 0, 0, 0, 0, 0), (34, -2, 10, -3, 14, 4), (50, -2, 10, -3, 14, 4),
                                  (58, -1, -9, -2, -12, -3), (72, -1, -9, -2, -12, -3), (80, 6, 0, 6, 0, 0),
                                  (86, 7, 0, 3, 0, 0), (89, 7, 0, 7, 0, 0), (92, 7, 0, 3, 0, 0), (95, 7, 0, 7, 0, 0),
                                  (106, 0, 0, 0, 0, 0), (120, 0, 0, 0, 0, 0)):
        k.key("Neck", f, rot=(nk, ny * 0.4, 0))
        k.key("Head", f, rot=(hd, hy * 0.6, ht))
    for f, j in ((0, 3), (60, 3), (64, 16), (67, 3), (70, 16), (73, 3), (120, 3)):
        k.key("Jaw", f, rot=(j, 0, 0))
    for f, c in ((0, 0), (36, 0), (40, 28), (44, 0), (47, 26), (51, 0), (120, 0)):
        arms(k, f, up=0, curl=c)
    plant_frames(k, range(0, n + 1))
    k.finish()
    k.meta["planted"] = LEGS


def walk(k):
    """heavy stomp: the body dips on every contact, the head counter-bobs a few frames late, the tail swings against
    the hips, toes peel off the ground"""
    n = 32

    def body(f):
        c = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)          # 0 at the contacts, 1 at passing
        k.key("Spine", f, rot=(1.2 * pk.wave(f, n, 0.12, 2), 4 * pk.wave(f, n, 0.0), 3 * pk.wave(f, n, 0.0)),
              loc=(0, 0, -0.035 * (1 - c)))
        k.key("Chest", f, rot=(0, -3 * pk.wave(f, n, 0.05), -2 * pk.wave(f, n, 0.0)))
        k.key("Neck", f, rot=(2 + 2.5 * pk.wave(f, n, 0.18, 2), -2 * pk.wave(f, n, 0.1), 0))
        k.key("Head", f, rot=(-2 - 3 * pk.wave(f, n, 0.28, 2), 3 * pk.wave(f, n, 0.15), 0))
        k.key("Jaw", f, rot=(4 + 2 * pk.wave(f, n, 0.3, 2), 0, 0))
        arms(k, f, up=4 * pk.wave(f, n, 0.25), curl=6)
        cm.chain(k, f, n, TAIL, sway=-5, pitch=1, cycles=1, lag=0.14, grow=0.5)
    orig = k.solve_leg
    k.solve_leg = lambda leg, f, T, foot_z=0.0, toe=None: orig(leg, f, T, foot_z,
                                                               toe=16.0 * min(1.0, max(0.0, T.z) / 0.1))
    try:
        return cm.biped_walk(k, n, 0.20, 0.13, body, legs=(("Leg_L", 0.0), ("Leg_R", 0.5)), duty=0.6)
    finally:
        del k.solve_leg


def roar(k):
    """STORM ROAR (ref: Tyrant Dragon crouch -> chest-led rise): sinks into a deep crouch with the head dropped low,
    rises chest first, the head arrives last and throws the jaw wide open; arms flare, the tail lifts stiff and its
    tip shivers; the jaw buzzes through the hold; settles."""
    n = 84
    k.new_action("roar", n, False)
    K = [  # f, spine z, spine pitch, chest, neck, head, jaw, tail pitch, arm up, spread, curl
        (0, 0.0, 0, 0, 0, 0, 3, 0, 0, 0, 0),
        (14, -0.10, 9, 4, 16, 10, 5, 10, -10, 0, 10),
        (20, -0.10, 10, 5, 18, 12, 6, 12, -12, 0, 12),
        (27, 0.02, -6, -4, -6, 4, 18, 8, 10, 14, 20),
        (32, 0.03, -8, -5, -10, -14, 40, 12, 16, 24, 32),
        (60, 0.02, -7, -5, -9, -12, 38, 12, 16, 24, 32),
        (70, -0.02, 2, 0, 2, 2, 8, 4, 4, 6, 8),
        (84, 0.0, 0, 0, 0, 0, 3, 0, 0, 0, 0)]
    for f, z, p, ch, nk, hd, jw, tp, au, sp, cu in K:
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(ch, 0, 0))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        tail(k, f, tp, 0)
        arms(k, f, up=au, spread=sp, curl=cu)
    for f in range(34, 60, 3):
        w = 1 if (f // 3) % 2 else -1
        k.key("Jaw", f, rot=(38 + 3 * w, 0, 0))
        k.key("Tail4", f, rot=(12, 6 * w, 0))
    plant_frames(k, range(0, n + 1))
    k.finish(loop=False)
    k.events["roar"] = {"peak": round(32 / n, 3), "end": round(60 / n, 3)}


def tailspin(k):
    """SIGNATURE (Thunder Rex only) - STORM TAILSPIN: crouches with the tail cocked, hops up and spins a full 360 in the
    air with the tail whipping round behind it (legs tucked), lands in a deep STOMP crouch (bolt VFX on the impact),
    rises into a power pose (chest up, chin high, jaw open, claws spread), settles."""
    import bpy
    n = 76
    k.new_action("act_tailspin", n, False)
    Z = (0, 0, 1)
    K = [  # f, z, yaw, chest pitch, neck, head, jaw, tail pitch, tail yaw, arm up, spread
        (0, 0.0, 0, 0, 0, 0, 3, 0, 0, 0, 0),
        (10, -0.09, 0, 6, 6, 4, 4, 10, 18, -8, 0),
        (14, -0.07, 0, 4, 4, 2, 6, 8, 22, -6, 0),
        (18, 0.16, 70, -2, 0, 0, 10, 4, -20, 6, 10),
        (21, 0.20, 160, -2, 0, 0, 10, 2, -40, 6, 10),
        (24, 0.20, 250, -2, 0, 0, 10, 2, -46, 6, 10),
        (27, 0.14, 330, -2, 0, -2, 10, 4, -36, 6, 10),
        (30, 0.02, 360, 4, 2, 2, 8, 6, 20, 0, 0),
        (33, -0.11, 360, 10, 10, 8, 22, 10, 30, -10, 0),
        (37, -0.09, 360, 8, 8, 6, 6, 6, -8, -6, 0),
        (44, 0.02, 360, -6, -8, -12, 26, 10, 0, 16, 26),
        (60, 0.02, 360, -6, -8, -12, 26, 10, 0, 16, 26),
        (76, 0.0, 360, 0, 0, 0, 3, 0, 0, 0, 0)]
    for f, z, yaw, p, nk, hd, jw, tp, ty, au, sp in K:
        cm.key_axis(k, "Spine", f, Z, yaw, loc=(0, 0, z))
        k.key("Chest", f, rot=(p, 0, 0))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        tail(k, f, tp, ty, each=(0.15, 0.45, 0.8, 1.0))
        arms(k, f, up=au, spread=sp, curl=sp)
    k.bake_bezier_now()
    sc = bpy.context.scene
    ground = list(range(0, 15)) + list(range(30, n + 1))
    for f in ground:
        sc.frame_set(f)
        for leg in LEGS:
            k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, 0.0)))
    for f, th, sh in ((18, -28, 46), (21, -34, 56), (24, -34, 56), (27, -26, 44)):
        for leg in LEGS:
            k.key(leg, f, rot=(th, 0, 0), loc=(0, 0, 0))
            k.key(leg.replace("Leg_", "Shin_"), f, rot=(sh, 0, 0))
            k.key(leg.replace("Leg_", "Foot_"), f, rot=(-10, 0, 0))
    k.finish(loop=False)
    k.events["act_tailspin"] = {"spin": round(18 / n, 3), "stomp": round(33 / n, 3)}


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    tailspin(k)
    return stride


def joints():
    return [((0, -0.62, 1.36), (0, -0.70, 1.45), 0.26, "Head"), ((0, -0.78, 1.38), (0, -0.78, 1.38), 0.10, "Head")]

