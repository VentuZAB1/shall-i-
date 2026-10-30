# Cvetibara clips v2 (2026-10-08): same model + rig as v1 (Cvetibara_rigged.blend, already in Studio), new clips:
#   idle  - zen celestial capybara: slow breath, humming head-tilt, a cute double wing-flutter, halo bob, ear twitch
#   walk  - kept from v1 (planted-foot trot)
#   fly   - REAL flight: body level + nose a little down, legs tucked back, head up looking ahead, big strokes that
#           sweep the wings forward + inward on the downstroke and fold the tips on the upstroke, ears swept back
#   takeoff / land - crouch + launch (event launch) / flare + touch-down (event touch), like PetAnimator expects
#   roar  - 'celestial blessing': rears up on the hind legs, wings wide, halo rises
#   act_happy - kept from v1
# Run in Blender (MCP):  runpy.run_path(r"...\cvetibara_v2.py")["run"]()
import bpy, math, os, json, importlib.util
from mathutils import Vector

HERE = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\FriendPets\Cvetibara"


def _mod(name):
    sp = importlib.util.spec_from_file_location(name, os.path.join(HERE, name + ".py"))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


A = _mod("cvetibara_rig_anim")
X = _mod("cvetibara_export")
key, finish, wave = A.key, A.finish, A.wave
LEGS = ["Leg_FL", "Leg_FR", "Leg_BL", "Leg_BR"]
FLY_N = 20
EVENTS = {}


def joints(arm):
    J = {b.name: b.head_local.copy() for b in arm.data.bones}
    return J


def new(arm, name):
    return A.new_action(arm, name)


def plant(arm, J, n, legs=LEGS, frames=None):
    for fc in A.fcurves(arm):
        for kp in fc.keyframe_points:
            kp.interpolation = "BEZIER"
            kp.handle_left_type = kp.handle_right_type = "AUTO_CLAMPED"
        if not any(m.type == "CYCLES" for m in fc.modifiers):
            fc.modifiers.new("CYCLES")
        fc.update()
    sc = bpy.context.scene
    for f in (frames if frames is not None else range(0, n + 1)):
        sc.frame_set(f)
        for leg in legs:
            A.solve_leg(arm, leg, f, Vector((J[leg].x, J[leg].y, 0.0)), J)


def wings(arm, f, up, fwd=0.0, tip_up=0.0, tip_fwd=0.0, twist=0.0):
    for side, sx in (("L", 1), ("R", -1)):
        key(arm, "Wing_" + side, f, rot=(twist, -sx * fwd, -sx * up))
        key(arm, "WingTip_" + side, f, rot=(0, -sx * tip_fwd, -sx * tip_up))


FOLD = dict(up=6, fwd=0.0, tip_up=0.0, tip_fwd=0.0)


def idle(arm, J):
    n = 72
    new(arm, "idle")
    for f in range(0, n + 1, 3):
        s = wave(f, n)
        key(arm, "Spine", f, rot=(1.0 * s, 0, 1.8 * wave(f, n, 0.1)), loc=(0, 0, 0.016 * (1 + s) / 2))
        hum = wave(f, n, 0.0, 2)          # humming head tilt, twice per cycle
        key(arm, "Head", f, rot=(-2.5 * wave(f, n, 0.25), 4 * wave(f, n, 0.1), 7 * hum))
        key(arm, "Halo", f, rot=(5 * wave(f, n, 0.3), 0, 5 * wave(f, n, 0.55)),
            loc=(0, 0, 0.06 * (1 + wave(f, n, 0.15, 2)) / 2))
        key(arm, "Flower", f, rot=(0, 0, 9 * wave(f, n, 0.4, 2)))
    # wings: resting, with a cute double flutter around f 30..44
    for f, up, tu in ((0, 6, 0), (27, 6, 0), (31, 30, 16), (34, 2, -6), (37, 32, 18), (40, 2, -6), (45, 6, 0), (72, 6, 0)):
        wings(arm, f, up, 0, tu, 0)
    for side, sx in (("L", 1), ("R", -1)):
        for f, a in ((0, 0), (54, 0), (57, -20), (60, 5), (64, 0), (n, 0)):
            key(arm, "Ear_" + side, f, rot=(0, 0, sx * a if side == "R" else 0))
    plant(arm, J, n)
    finish(arm, True, n)


def fly_pose(arm, f, n=FLY_N, legs=True):
    ph = f / n
    flap = math.cos(2 * math.pi * ph)            # +1 = wings up (f0), -1 = down (f n/2)
    down = math.sin(2 * math.pi * ph)            # > 0 on the downstroke
    lag = math.cos(2 * math.pi * (ph - 0.13))
    rise = -math.sin(2 * math.pi * (ph - 0.05))
    key(arm, "Spine", f, rot=(9 + 2.5 * flap, 0, 0), loc=(0, 0, -0.08 * rise))
    key(arm, "Head", f, rot=(-12 - 2 * lag, 0, 0))
    wings(arm, f, up=12 + 50 * flap, fwd=16 * down - 4, tip_up=-4 + 26 * lag + 10 * max(0.0, -down),
          tip_fwd=-14 * max(0.0, -down) + 6 * down, twist=8 * down)
    for side, sx in (("L", 1), ("R", -1)):
        key(arm, "Ear_" + side, f, rot=(-24 - 4 * lag, 0, -sx * 6 * lag))      # ears swept back by the wind
    if legs:
        for leg, base in (("Leg_FL", 58), ("Leg_FR", 58), ("Leg_BL", 76), ("Leg_BR", 76)):
            key(arm, leg, f, rot=(base + 5 * lag, 0, 0), loc=(0, 0, 0.05))    # tucked back
    key(arm, "Halo", f, loc=(0, 0.04, -0.04 * rise), rot=(-8 + 4 * lag, 0, 0))
    key(arm, "Flower", f, rot=(12 + 8 * lag, 0, 0))


def fly(arm):
    new(arm, "fly")
    for f in range(0, FLY_N + 1):
        fly_pose(arm, f)
    finish(arm, True, FLY_N)


def takeoff(arm, J):
    n = 27
    new(arm, "takeoff")
    # crouch with the wings lifted (0-10), launch at 11 with a big downstroke + leg push, reach fly phase 0.45
    P = [(0, 0.0, 0, 6, 0, 0, 0), (6, -0.09, 4, 34, -10, 12, -6), (10, -0.12, 6, 62, -6, 24, -4),
         (13, 0.20, -8, -26, 12, -8, 6), (17, 0.30, 4, 22, 0, 16, -6)]
    for f, z, p, up, fwd, tu, tf in P:
        key(arm, "Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
        key(arm, "Head", f, rot=(-6 - p * 0.5, 0, 0))
        wings(arm, f, up, fwd, tu, tf)
        for side in ("L", "R"):
            key(arm, "Ear_" + side, f, rot=(-10 if f >= 13 else 0, 0, 0))
        key(arm, "Halo", f, rot=(0, 0, 0), loc=(0, 0, 0.02))
        key(arm, "Flower", f, rot=(0, 0, 0))
    fly_pose(arm, n, legs=False)
    key(arm, "Spine", n, rot=None, loc=(0, 0, -0.08 * -math.sin(2 * math.pi * (0.45 - 0.05))))
    plant(arm, J, n, frames=range(0, 12))
    for f, a_f, a_b in ((14, 28, 40), (20, 50, 66), (n, 58 + 5 * math.cos(2 * math.pi * (0.45 - 0.13)), 76 + 5 * math.cos(2 * math.pi * (0.45 - 0.13)))):
        for leg in LEGS:
            key(arm, leg, f, rot=(a_f if "F" in leg[4] else a_b, 0, 0), loc=(0, 0, 0.05 if f == n else 0.0))
    finish(arm, False, n)
    EVENTS["takeoff"] = {"launch": round(11 / n, 3)}


def land(arm, J):
    n = 27
    new(arm, "land")
    fly_pose(arm, 0)
    P = [(7, 0.10, -14, 34, -24, 22, -16), (12, 0.06, -8, -10, -12, 4, -6), (16, -0.08, 4, 12, -6, -6, -8),
         (21, 0.02, -1, 0, 0, -4, -4), (27, 0.0, 0, 6, 0, 0, 0)]
    for f, z, p, up, fwd, tu, tf in P:
        key(arm, "Spine", f, rot=(p, 0, 0), loc=(0, 0, z))
        key(arm, "Head", f, rot=(-5 - p * 0.3, 0, 0))
        wings(arm, f, up, fwd, tu, tf)
        for side in ("L", "R"):
            key(arm, "Ear_" + side, f, rot=(-12 if f < 16 else 0, 0, 0))
        key(arm, "Halo", f, rot=(0, 0, 0), loc=(0, 0, 0.03 if f < 21 else 0.0))
        key(arm, "Flower", f, rot=(0, 0, 0))
    for leg in LEGS:
        key(arm, leg, 7, rot=(-20 if "F" in leg[4] else -8, 0, 0), loc=(0, 0, 0))
    plant(arm, J, n, frames=range(16, n + 1))
    finish(arm, False, n)
    EVENTS["land"] = {"touch": round(16 / n, 3)}


def roar(arm, J):
    """'celestial blessing': rears up on her hind legs, front paws up, wings spread wide, halo floats up + spins."""
    n = 54
    new(arm, "roar")
    P = [(0, 0, 0, 6, 0, 0.0, 0), (10, 6, 3, 2, -4, 0.0, 0), (20, -24, -8, 52, 30, 0.14, 1), (36, -24, -10, 56, 32, 0.16, 1),
         (46, 4, 2, 4, -4, 0.02, 0), (54, 0, 0, 6, 0, 0.0, 0)]
    for f, sp, hd, up, tu, halo, rear in P:
        key(arm, "Spine", f, rot=(sp, 0, 0), loc=(0, 0, 0.05 * rear))
        key(arm, "Head", f, rot=(hd, 0, 0))
        wings(arm, f, up, -6 * rear, tu, 0)
        key(arm, "Halo", f, rot=(0, 0, 40 * rear), loc=(0, 0, halo))
        key(arm, "Flower", f, rot=(0, 0, 10 * rear))
        for side, sx in (("L", 1), ("R", -1)):
            key(arm, "Ear_" + side, f, rot=(0, 0, sx * 8 * rear))
    for f in range(20, 37, 4):    # happy wing shimmer while up
        k = 1 if (f // 4) % 2 else -1
        wings(arm, f, 54 + 5 * k, -6, 31 + 4 * k, 0)
    # hind legs stay planted the whole time; front legs planted except while rearing
    plant(arm, J, n, legs=["Leg_BL", "Leg_BR"])
    plant(arm, J, n, legs=["Leg_FL", "Leg_FR"], frames=list(range(0, 11)) + list(range(47, n + 1)))
    for f in (16, 28, 40):
        for leg in ("Leg_FL", "Leg_FR"):
            key(arm, leg, f, rot=(-40 if f != 40 else -10, 0, 0), loc=(0, 0, 0))
    finish(arm, False, n)


def run():
    bpy.ops.wm.open_mainfile(filepath=os.path.join(HERE, "Cvetibara_rigged.blend"))
    arm = bpy.data.objects["Armature"]
    J = joints(arm)
    J["Root"] = arm.data.bones["Root"].head_local.copy()
    EVENTS.clear()
    idle(arm, J)
    fly(arm)
    takeoff(arm, J)
    land(arm, J)
    roar(arm, J)
    clips = {"idle": (72, True), "walk": (24, True), "fly": (FLY_N, True), "takeoff": (27, False), "land": (27, False),
             "roar": (54, False), "act_happy": (36, False)}
    rep = A.audit(arm, J, clips)
    stride = A.walk_stride(arm, J, 24)
    data = A.sample(arm, J, clips)
    data["walk"]["stride"] = round(stride, 4)
    d = json.load(open(os.path.join(HERE, "Cvetibara.json")))
    d["clips"] = data
    d["stride"] = round(stride, 4)
    d["events"] = EVENTS
    with open(os.path.join(HERE, "Cvetibara.json"), "w") as fh:
        json.dump(d, fh, separators=(",", ":"))
    info = X.luau()
    # luau() writes events = {} - put the takeoff/land events in
    p = os.path.join(HERE, "Cvetibara.lua")
    src = open(p, encoding="utf-8").read()
    ev = ", ".join(f'{c} = {{' + ", ".join(f"{e} = {v:.3f}" for e, v in dd.items()) + "}" for c, dd in EVENTS.items())
    src = src.replace("\tevents = {},", "\tevents = {" + ev + "},")
    open(p, "w", encoding="utf-8").write(src)
    A.set_action(arm, "idle")
    bpy.context.scene.frame_set(0)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, "Cvetibara_rigged_v2.blend"))
    return {"audit": rep, "stride": round(stride, 4), "lua_bytes": len(src), "events": EVENTS}
