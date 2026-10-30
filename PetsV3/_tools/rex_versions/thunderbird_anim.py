
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

