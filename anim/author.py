"""Author procedural animation clips for one rigged creature, inside Blender.

blender -b -P ../rig/rigger.py -P author.py -- <Name> <type> [rig opts] [--preview]

rigger.py builds the armature (same bones as the Roblox model). This script then:
  * builds every clip for the creature (walk / idle / roar / acts / flight / swim ...) with
    real 2-bone IK so planted feet stay locked on the ground (no sliding, no sinking),
  * writes them as Blender actions and saves anim/blend/<Name>.blend (open it to look / tweak),
  * exports anim/out/<RobloxName>.json: per-frame bone rotations in ROOT space, already converted
    to Roblox axes (Blender (x,y,z) -> Roblox (-x, z, y)), read by CreatureAnimator,
  * with --preview: renders frames of every clip to anim/preview/_frames/ (run_anim.py builds sheets).

Conventions (Blender armature space): +Z up, creature faces -Y, +X is the creature's left.
D[bone] = rotation delta in root space applied at the bone head (Roblox: Transform = R0^-1 * D * R0).
"""
import bpy, sys, os, math, json, re
from mathutils import Vector, Quaternion, Matrix

HERE = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\anim"
sys.path.insert(0, HERE)
from profiles import profile_for, roblox_name

argv = sys.argv[sys.argv.index("--") + 1:]
NAME, TYPE = argv[0], argv[1]
PREVIEW = "--preview" in argv
ONLY = os.environ.get("ANIM_ONLY", "").split(",") if os.environ.get("ANIM_ONLY") else None
P = profile_for(NAME)
STYLE = P["style"]
FPS_AUTHOR = 30
FPS_EXPORT = 20

arm = bpy.data.objects[NAME + "_Rig"]
TAU = math.pi * 2
X, Y, Z = Vector((1, 0, 0)), Vector((0, 1, 0)), Vector((0, 0, 1))
QI = Quaternion()
sin, cos = math.sin, math.cos


def clamp(x, a, b):
    return a if x < a else b if x > b else x


def sm(x):
    x = clamp(x, 0.0, 1.0)
    return x * x * (3 - 2 * x)


def keys(t, ks):
    """smooth piecewise interpolation through (time, value) keys"""
    if t <= ks[0][0]:
        return ks[0][1]
    for (t0, v0), (t1, v1) in zip(ks, ks[1:]):
        if t <= t1:
            return v0 + (v1 - v0) * sm((t - t0) / max(t1 - t0, 1e-6))
    return ks[-1][1]


def q(axis, ang):
    return Quaternion(axis, ang)


def pitch(a):  # nose up (forward-pointing bone) / swing forward (hanging limb)
    return q(X, -a)


def yaw(a):  # turn left
    return q(Z, a)


def roll(a):  # left side down
    return q(Y, a)


def wup(s, a):  # wing up (s = +1 left wing, -1 right wing)
    return q(Y, -s * a)


def wback(s, a):  # wing tip sweeps back
    return q(Z, s * a)


# ------------------------------------------------------------------ rig description
class Rig:
    def __init__(self, arm):
        bs = arm.data.bones
        self.names = [b.name for b in bs]
        self.parent = {b.name: (b.parent.name if b.parent else None) for b in bs}
        self.head0 = {b.name: b.head_local.copy() for b in bs}
        self.tail0 = {b.name: b.tail_local.copy() for b in bs}
        self.R0 = {b.name: b.matrix_local.to_3x3().normalized().to_quaternion() for b in bs}

        def depth(n):
            d = 0
            while self.parent[n]:
                n = self.parent[n]
                d += 1
            return d
        self.order = sorted(self.names, key=depth)

    def has(self, n):
        return n in self.parent


R = Rig(arm)


class Leg:
    pass


def frame(d, n):
    d = d.normalized()
    n = n - d * n.dot(d)
    if n.length < 1e-8:
        n = d.orthogonal()
    n.normalize()
    b = d.cross(n)
    return Matrix((d, n, b)).transposed()


LEGS = []
for n in R.names:
    m = re.match(r"^Leg(\d+)_U$", n)
    if not m or not R.has(f"Leg{m.group(1)}_L"):
        continue
    lg = Leg()
    lg.i = int(m.group(1))
    lg.U, lg.L = n, f"Leg{lg.i}_L"
    lg.H0, lg.K0, lg.F0 = R.head0[lg.U], R.head0[lg.L], R.tail0[lg.L].copy()
    lg.F0.z = 0.0
    lg.a = (lg.K0 - lg.H0).length
    lg.b = (R.tail0[lg.L] - lg.K0).length
    lg.side = 1 if lg.F0.x > 0 else -1
    hf = R.tail0[lg.L] - lg.H0
    perp = (lg.K0 - lg.H0) - hf.normalized() * (lg.K0 - lg.H0).dot(hf.normalized())
    lg.parentBone = R.parent[lg.U]
    if perp.length < 0.01 * (lg.a + lg.b):  # straight leg: pick a natural bend
        perp = Vector((lg.side * 0.5, 0, 0.5)) if TYPE == "multileg" else Vector((0, 1 if lg.parentBone == "Chest" else -1, 0))
    lg.hint0 = perp.normalized()
    LEGS.append(lg)
LEGS.sort(key=lambda l: l.i)
if LEGS:
    ys = sorted(set(round(l.F0.y, 2) for l in LEGS))
    midy = sum(l.F0.y for l in LEGS) / len(LEGS)
    rows = sorted(LEGS, key=lambda l: l.F0.y)
    for k, l in enumerate(rows):
        l.row = k // 2
        l.front = l.F0.y < midy
LEG_LEN = (sum(l.H0.z for l in LEGS) / len(LEGS)) if LEGS else 0.5

TAILS = sorted([n for n in R.names if re.match(r"^Tail\d+$", n)], key=lambda n: int(n[4:]))
WINGS = {s: sorted([n for n in R.names if n.startswith("Wing" + c)], key=lambda n: int(n[5:]))
         for s, c in ((1, "L"), (-1, "R"))}
HAS_WINGS = bool(WINGS[1] or WINGS[-1])
ARMS = {s: (f"Arm{c}_U", f"Arm{c}_L") for s, c in ((1, "L"), (-1, "R")) if R.has(f"Arm{c}_U")}
TENTS = [n for n in R.names if n.startswith("Tent")]

# The auto-skinning sometimes gives a leg vertices that belong to the tail/body far from the foot
# (low tail parts near the hind feet). Rotating such a leg a lot drags that geometry into a sheet,
# so FK leg poses (tuck/reach/paddle) are scaled down by l.calm for those legs.
_mesh = [o for o in bpy.data.objects if o.type == "MESH"][0]
_gi = {g.name: g.index for g in _mesh.vertex_groups}
for l in LEGS:
    bad = 0
    ids = {_gi.get(l.U), _gi.get(l.L)}
    for v in _mesh.data.vertices:
        for g in v.groups:
            if g.group in ids and g.weight > 0.3:
                if Vector((v.co.x - l.F0.x, v.co.y - l.F0.y)).length > 0.9 * LEG_LEN + 0.15:
                    bad += 1
                break
    l.calm = 0.3 if bad > 15 else 1.0
    if bad > 15:
        print("CALM", l.U, bad)
HIND_TUCK = 1.0

# Upright flyers (birds, upright dragons, sitting griffins) must tip the whole body forward to fly,
# otherwise they look like they're standing in mid-air. LEAN = how far the spine is above a
# comfortable flight angle; applied at Hips (legs/tail follow), head kept level.
LEAN = 0.0
if STYLE in ("bird", "dragon", "moth", "skydragon") and R.has("Hips") and (R.has("Head") or R.has("Chest")):
    _v = R.head0["Head" if R.has("Head") else "Chest"] - R.head0["Hips"]
    _elev = math.atan2(_v.z, max(-_v.y, 1e-3))
    LEAN = clamp(_elev - 0.3, 0.0, 1.15)
LEAN = P.get("lean", LEAN)
print("LEAN %.2f" % LEAN)

# walking stride + how much the body must drop so the legs can reach (knees always a bit bent)
STRIDE, DROP = 0.0, 0.0
if LEGS and "stride" in P:
    STRIDE = P["stride"] * LEG_LEN
    for _ in range(20):
        need = 0.0
        ok = True
        for l in LEGS:
            hz = l.H0.z
            hd = Vector((l.H0.x - l.F0.x, l.H0.y - l.F0.y)).length
            reach = (l.a + l.b) * 0.95
            r2 = reach ** 2 - (hd + STRIDE / 2) ** 2
            if r2 <= (hz * 0.6) ** 2:
                ok = False
                break
            need = max(need, hz - math.sqrt(r2))
        if ok:
            break
        STRIDE *= 0.85
    DROP = max(need, 0.025 * LEG_LEN)
else:
    DROP = 0.02 * LEG_LEN


# ------------------------------------------------------------------ pose + evaluation
class Pose:
    def __init__(self):
        self.D = {}
        self.off = Vector()
        self.tg = {}      # leg index -> (target, ik weight)
        self.stab = 0.0   # head stabilisation 0..1
        self.headW = QI   # wanted head world rotation when stabilised

    def rot(self, n, quat):
        if R.has(n):
            self.D[n] = self.D.get(n, QI) @ quat

    def plant(self, w=1.0, lift=None):
        for l in LEGS:
            self.tg[l.i] = (l.F0.copy(), w)


def evaluate(D, off):
    W, Pp = {}, {}
    for n in R.order:
        p = R.parent[n]
        d = D.get(n, QI)
        if p is None:
            W[n], Pp[n] = d, R.head0[n].copy()
        else:
            W[n] = W[p] @ d
            Pp[n] = Pp[p] + W[p] @ (R.head0[n] - R.head0[p])
        if n == "Hips":
            Pp[n] = Pp[n] + off
    return W, Pp


def solve(pose):
    """finalise a pose: head stabilisation + leg IK. Returns D (root-space deltas) and hips offset."""
    D = dict(pose.D)
    W, Pp = evaluate(D, pose.off)
    if pose.stab > 0 and R.has("Head") and R.parent["Head"]:
        par = R.parent["Head"]
        want = W[par].inverted() @ pose.headW
        D["Head"] = D.get("Head", QI).slerp(want @ D.get("Head", QI), pose.stab)
    for l in LEGS:
        if l.i not in pose.tg:
            continue
        target, w = pose.tg[l.i]
        if w <= 0:
            continue
        Hp = Pp[l.U]
        Wp = W[l.parentBone]
        hint = Wp @ l.hint0
        dv = target - Hp
        d = clamp(dv.length, abs(l.a - l.b) + 1e-4, (l.a + l.b) * 0.999)
        u = dv.normalized()
        x = (l.a * l.a - l.b * l.b + d * d) / (2 * d)
        h = math.sqrt(max(0.0, l.a * l.a - x * x))
        hp = hint - u * hint.dot(u)
        if hp.length < 1e-8:
            hp = u.orthogonal()
        hp.normalize()
        K = Hp + u * x + hp * h
        F = Hp + u * d
        WU = (frame(K - Hp, hp) @ frame(l.K0 - l.H0, l.hint0).transposed()).to_quaternion()
        WL = (frame(F - K, hp) @ frame(R.tail0[l.L] - l.K0, l.hint0).transposed()).to_quaternion()
        dU = Wp.inverted() @ WU
        dL = WU.inverted() @ WL
        D[l.U] = D.get(l.U, QI).slerp(dU, w) if w < 1 else dU
        D[l.L] = D.get(l.L, QI).slerp(dL, w) if w < 1 else dL
    return D, pose.off


# ------------------------------------------------------------------ shared building blocks
def walk_target(l, u, duty, S, lift):
    u %= 1.0
    if u < duty:
        y, z = -S / 2 + S * (u / duty), 0.0
    else:
        v = (u - duty) / (1 - duty)
        y = S / 2 - S * sm(v)
        z = lift * math.sin(math.pi * clamp(v, 0, 1) ** 0.75)
    return l.F0 + Vector((0, y, z))


def gait_offset(l, gait):
    if TYPE == "multileg":
        side = 0 if l.side > 0 else 1
        return ((l.row + side) % 2) * 0.5 + l.row * 0.06
    if len(LEGS) == 2:
        return 0.0 if l.side > 0 else 0.5
    if gait == "trot":
        diag = (l.front and l.side > 0) or (not l.front and l.side < 0)
        return 0.0 if diag else 0.5
    # lateral-sequence walk: LH, LF, RH, RF
    if not l.front:
        return 0.0 if l.side > 0 else 0.5
    return 0.25 if l.side > 0 else 0.75


def tail_wave(s, t, amp, cycles=1.0, lag=0.7, droop=0.0):
    n = len(TAILS)
    for k, tn in enumerate(TAILS):
        s.rot(tn, yaw(amp * sin(TAU * cycles * t - lag * k) * (0.7 + 0.3 * k / max(n, 1))) @ pitch(-droop))


def fold_wings(s, amt=1.0, breathe=0.0):
    """resting wing pose: raised a little and swept back along the body"""
    for sd, chain in WINGS.items():
        for k, wn in enumerate(chain):
            if k == 0:
                s.rot(wn, wback(sd, 0.75 * amt) @ wup(sd, (0.3 + breathe) * amt))
            elif k == 1:
                s.rot(wn, wback(sd, 0.55 * amt) @ wup(sd, -0.35 * amt))
            else:
                s.rot(wn, wback(sd, 0.35 * amt) @ wup(sd, -0.2 * amt))


def flap_angle(t):
    """wing-1 stroke angle over a flap cycle: fast downstroke (0..0.45), slower upstroke"""
    t %= 1.0
    if t < 0.45:
        return 0.95 - 1.55 * sm(t / 0.45)
    return -0.6 + 1.55 * sm((t - 0.45) / 0.55)


def wings_flap(s, t, amp=1.0, extra_up=0.0):
    for sd, chain in WINGS.items():
        prev = 0.0
        for k, wn in enumerate(chain):
            a = flap_angle(t - 0.06 * k) * amp * (1.0 if k == 0 else 0.55) + extra_up
            up_stroke = sm(((t - 0.45) % 1.0) / 0.55) if (t % 1.0) >= 0.45 else 0.0
            fold = math.sin(math.pi * up_stroke) if (t % 1.0) >= 0.45 else 0.0
            sweep = (-0.18 if (t % 1.0) < 0.45 else 0.12) * amp if k == 0 else 0.35 * fold * amp
            if k == 0:
                s.rot(wn, wback(sd, sweep) @ wup(sd, a))
            else:
                s.rot(wn, wback(sd, sweep) @ wup(sd, a - prev * 0.0 - 0.25 * fold * amp))
            prev = a


def wings_glide(s, t, wobble=1.0):
    for sd, chain in WINGS.items():
        for k, wn in enumerate(chain):
            w = 0.04 * wobble * sin(TAU * 2 * t + k * 0.6)
            s.rot(wn, wup(sd, (0.12 if k == 0 else 0.06) + w) @ wback(sd, 0.05))


def tuck_legs(s, amt=1.0, t=None):
    """flight legs: hind legs stream back like a bird of prey, front claws fold up under the chest.
    With t (flap phase) the legs pump a little with every wingbeat so they never look parked."""
    base = amt
    pump = 0.0 if t is None else sin(TAU * (t - 0.1))
    for l in LEGS:
        amt = base * l.calm
        side_lag = 0.0 if l.side > 0 else 0.25
        pp = 0.0 if t is None else sin(TAU * (t - 0.1 - side_lag * 0.2))
        if TYPE in ("bird", "biped") or not l.front:
            # thigh swings far back, shin stretched behind (talons trailing under the tail)
            back = max(0.5, 1.4 - LEAN)
            s.rot(l.U, pitch(-(back + 0.12 * pp) * amt) @ roll(l.side * 0.08 * amt))
            s.rot(l.L, pitch(-(0.3 + 0.15 * pp) * amt))
        else:
            # front legs: elbow back, forearm folded hard forward-up -> claws tucked under the chest
            s.rot(l.U, pitch(-(0.9 + 0.1 * pp) * amt) @ roll(-l.side * 0.1 * amt))
            s.rot(l.L, pitch((2.0 - 0.15 * pp) * amt))


def reach_legs(s, amt=1.0):
    """legs stretched down/forward to catch the ground (landing)"""
    for l in LEGS:
        s.rot(l.U, pitch(0.35 * amt * l.calm))
        s.rot(l.L, pitch(-0.15 * amt * l.calm))


def arms_hang(s, t, swing, breathe=0.0):
    for sd, (u, lo) in ARMS.items():
        s.rot(u, pitch(swing * sd) @ roll(sd * (0.05 + breathe)))
        s.rot(lo, pitch(0.25))


def breath_count(T, per=1.6):
    return max(1, round(T / per))


# ------------------------------------------------------------------ ground clips
def c_idle(t, T):
    s = Pose()
    nb = breath_count(T, 2.0 if P.get("walkT", 1) > 1.2 else 1.5)
    br = sin(TAU * nb * t)
    sh = sin(TAU * t)
    L = LEG_LEN
    s.off = Vector((0.015 * L * sh, 0, -DROP * 0.5 + 0.008 * L * br))
    s.rot("Hips", roll(0.02 * sh))
    s.rot("Chest", pitch(0.025 * br) @ roll(-0.015 * sh))
    s.rot("Neck", pitch(0.04 * sin(TAU * t + 1.0)))
    s.rot("Head", pitch(0.03 * sin(TAU * 2 * t + 0.4)))
    tail_wave(s, t, 0.12 + P.get("tail", 0.1) * 0.4, cycles=2, droop=0.05)
    if ARMS:
        arms_hang(s, t, 0.04 * sin(TAU * t), breathe=0.03 * br)
    if HAS_WINGS:
        fold_wings(s, 1.0, breathe=0.04 * br)
    s.plant()
    return s


def c_walk(t, T):
    s = Pose()
    p = P
    L = LEG_LEN
    gait = p.get("gait", "walk")
    duty = 0.6 if len(LEGS) == 2 else 0.55 if (TYPE == "multileg" or gait == "trot") else 0.66
    lift = p["lift"] * L
    for l in LEGS:
        s.tg[l.i] = (walk_target(l, t + gait_offset(l, gait), duty, STRIDE, lift), 1.0)
    bob = p["bob"] * L
    if len(LEGS) == 2:
        s.off = Vector((p["sway"] * L * cos(TAU * (t - 0.3)), 0, -DROP - bob * (0.5 + 0.5 * cos(2 * TAU * t))))
        s.rot("Hips", yaw(0.06 * sin(TAU * t)) @ roll(-p["roll"] * cos(TAU * (t - 0.3))))
        s.rot("Chest", yaw(-0.1 * sin(TAU * t)) @ roll(p["roll"] * 0.6 * cos(TAU * (t - 0.3))))
        if ARMS:
            for sd, (u, lo) in ARMS.items():
                sw = p.get("arms", 0.4) * cos(TAU * t) * sd
                s.rot(u, pitch(sw) @ roll(sd * 0.08))
                s.rot(lo, pitch(0.3 + 0.15 * max(0, sw)))
    else:
        s.off = Vector((p["sway"] * L * sin(TAU * t), 0, -DROP - bob * (0.5 + 0.5 * cos(2 * TAU * (t - 0.12)))))
        s.rot("Hips", roll(p["roll"] * sin(TAU * t)) @ pitch(0.02 * sin(2 * TAU * t)))
        s.rot("Chest", roll(-p["roll"] * 0.6 * sin(TAU * t + 0.4)))
        sp = p.get("spine", 0.0)
        if sp:
            s.rot("Hips", yaw(sp * sin(TAU * t)))
            s.rot("Chest", yaw(-2 * sp * sin(TAU * t)))
            s.rot("Neck", yaw(sp * sin(TAU * t)))
    if p.get("nod"):
        s.rot("Neck", pitch(-p["nod"] * sin(2 * TAU * t + 0.6)))
        s.rot("Head", pitch(p["nod"] * 0.4 * sin(2 * TAU * t + 0.2)))
    if p.get("headbob"):  # pigeon-style head thrust
        hb = p["headbob"]
        s.rot("Neck", pitch(-hb * (sm((2 * t) % 1.0 * 2) - 0.5)))
    s.stab = p.get("stab", 0.0)
    tail_wave(s, t, p.get("tail", 0.12), cycles=1, droop=0.03)
    if HAS_WINGS:
        fold_wings(s, 1.0)
    return s


def c_roar(t, T):
    s = Pose()
    L = LEG_LEN
    k = [(0, 0), (0.16, 1), (0.3, 1.1), (0.4, 0), (1, 0)]
    ant = keys(t, [(0, 0), (0.18, 1), (0.3, 1), (0.42, 0)])            # anticipation (wind-up)
    hit = keys(t, [(0, 0), (0.3, 0), (0.42, 1), (0.78, 0.9), (1, 0)])   # the roar itself
    trem = keys(t, [(0, 0), (0.4, 0), (0.45, 1), (0.75, 1), (0.85, 0)]) * sin(TAU * 22 * t * T)
    s.off = Vector((0, 0.06 * L * ant - 0.06 * L * hit, -DROP * 0.5 - 0.08 * L * ant + 0.02 * L * hit))
    s.rot("Chest", pitch(-0.14 * ant + 0.18 * hit))
    s.rot("Neck", pitch(-0.3 * ant + 0.38 * hit + 0.02 * trem) @ yaw(0.03 * trem))
    s.rot("Head", pitch(0.12 * ant + 0.32 * hit + 0.03 * trem))
    for k_, tn in enumerate(TAILS):
        s.rot(tn, pitch(0.25 * hit - 0.1 * ant) @ yaw(0.06 * trem))
    if ARMS:
        for sd, (u, lo) in ARMS.items():
            s.rot(u, pitch(-0.3 * ant + 0.5 * hit) @ roll(-sd * (0.2 * ant + 1.0 * hit)))
            s.rot(lo, pitch(0.5 * ant + 0.6 * hit))
    if HAS_WINGS:  # intimidation: wings flare up and wide
        fold_wings(s, 1.0 - hit)
        for sd, chain in WINGS.items():
            for kk, wn in enumerate(chain):
                s.rot(wn, wup(sd, (0.7 if kk == 0 else 0.15) * hit + 0.02 * trem))
    if TYPE == "multileg":  # rear up, front legs raised
        s.rot("Hips", pitch(0.25 * hit))
        for l in LEGS:
            if l.row == 0:
                s.tg[l.i] = (l.F0 + Vector((0, -0.25 * L * hit, 0.7 * L * hit)), 1.0)
            else:
                s.tg[l.i] = (l.F0.copy(), 1.0)
        return s
    s.plant()
    return s


def c_sniff(t, T):
    s = c_idle(t, T)
    env = keys(t, [(0, 0), (0.22, 1), (0.8, 1), (1, 0)])
    sn = sin(TAU * 3.5 * t * T) * 0.04 * env
    s.off += Vector((0, 0, -0.04 * LEG_LEN * env))
    s.rot("Chest", pitch(-0.12 * env))
    s.rot("Neck", pitch(-0.55 * env + sn) @ yaw(0.25 * sin(TAU * t) * env))
    s.rot("Head", pitch(-0.2 * env + sn * 1.5))
    return s


def c_shake(t, T):
    s = c_idle(t, T)
    env = keys(t, [(0, 0), (0.12, 1), (0.65, 0.7), (1, 0)])
    w = lambda lag: sin(TAU * 6 * t * T - lag) * env
    s.rot("Head", roll(0.45 * w(0)))
    s.rot("Neck", roll(0.3 * w(0.5)))
    s.rot("Chest", roll(0.22 * w(1.0)))
    s.rot("Hips", roll(0.14 * w(1.5)))
    for k, tn in enumerate(TAILS):
        s.rot(tn, yaw(0.35 * w(2.0 + 0.4 * k)))
    if HAS_WINGS:
        for sd, chain in WINGS.items():
            if chain:
                s.rot(chain[0], wup(sd, 0.25 * w(1.2)))
    return s


def c_stomp(t, T):
    """paw / scrape the ground with a front foot, head lowered (charge threat)"""
    s = c_idle(t, T)
    L = LEG_LEN
    env = keys(t, [(0, 0), (0.15, 1), (0.85, 1), (1, 0)])
    s.off += Vector((0, 0.03 * L * env, -0.05 * L * env))
    s.rot("Neck", pitch(-0.35 * env))
    s.rot("Head", pitch(0.12 * env))
    front = [l for l in LEGS if l.front and l.side > 0] or LEGS[:1]
    if front:
        l = front[0]
        z = keys(t, [(0, 0), (0.14, 0.22), (0.26, 0), (0.42, 0.24), (0.54, 0), (1, 0)]) * L
        y = keys(t, [(0, 0), (0.14, -0.1), (0.26, 0.0), (0.32, 0.18), (0.42, -0.1), (0.54, 0.0), (0.6, 0.18), (0.75, 0), (1, 0)]) * L
        s.tg[l.i] = (l.F0 + Vector((0, y, z)), 1.0)
        thud = keys(t, [(0.24, 0), (0.27, 1), (0.33, 0), (0.52, 0), (0.55, 1), (0.62, 0)])
        s.rot("Chest", pitch(-0.04 * thud))
    return s


def c_stretch(t, T):
    """play-bow stretch + yawn"""
    s = c_idle(t, T)
    L = LEG_LEN
    env = keys(t, [(0, 0), (0.25, 1), (0.7, 1), (0.95, 0)])
    yawn = keys(t, [(0, 0), (0.35, 0), (0.48, 1), (0.62, 1), (0.75, 0)])
    s.rot("Hips", pitch(-0.22 * env))
    s.off += Vector((0, 0.05 * L * env, -0.05 * L * env))
    s.rot("Neck", pitch(0.25 * env + 0.15 * yawn))
    s.rot("Head", pitch(0.15 * yawn))
    for tn in TAILS:
        s.rot(tn, pitch(0.15 * env))
    for l in LEGS:
        if l.front:
            s.tg[l.i] = (l.F0 + Vector((0, -0.35 * L * env, 0)), 1.0)
    return s


def c_look(t, T):
    """turn the upper body to look around, left then right"""
    s = c_idle(t, T)
    a = keys(t, [(0, 0), (0.2, 1), (0.42, 1), (0.6, -1), (0.85, -1), (1, 0)])
    s.rot("Chest", yaw(0.15 * a))
    s.rot("Neck", yaw(0.3 * a))
    s.rot("Head", yaw(0.25 * a) @ pitch(0.05 * abs(a)))
    return s


def c_crouch(t, T):
    s = c_idle(t, T)
    env = keys(t, [(0, 0), (0.25, 1), (0.75, 1), (1, 0)])
    s.off += Vector((0, 0, -0.2 * LEG_LEN * env))
    s.rot("Chest", pitch(-0.25 * env))
    s.rot("Neck", pitch(0.15 * env) @ yaw(0.3 * sin(TAU * t) * env))
    s.rot("Head", pitch(0.1 * env))
    return s


def c_pound(t, T):
    """heavy biped: pound the chest twice, then a short roar"""
    s = c_idle(t, T)
    env = keys(t, [(0, 0), (0.15, 1), (0.8, 1), (1, 0)])
    beat = abs(sin(TAU * 2.5 * t)) * env
    s.rot("Chest", pitch(0.1 * env) @ roll(0.05 * sin(TAU * 2.5 * t) * env))
    s.rot("Head", pitch(0.2 * env))
    for sd, (u, lo) in ARMS.items():
        ph = 0 if sd > 0 else math.pi
        b = abs(sin(TAU * 2.5 * t + ph / 2)) * env
        s.rot(u, pitch(0.9 * env + 0.3 * b) @ roll(sd * 0.4 * env))
        s.rot(lo, pitch(1.3 * env))
    return s


def c_twitch(t, T):
    s = c_idle(t, T)
    for l in LEGS:
        ph = l.row * 0.12 + (0 if l.side > 0 else 0.06)
        z = keys(t, [(0, 0), (0.2 + ph, 0), (0.26 + ph, 0.12), (0.32 + ph, 0), (1, 0)]) * LEG_LEN
        s.tg[l.i] = (l.F0 + Vector((0, 0, z)), 1.0)
    s.rot("Chest", yaw(0.15 * sin(TAU * 2 * t) * keys(t, [(0, 0), (0.2, 1), (0.8, 1), (1, 0)])))
    return s


def c_wingstretch(t, T):
    s = c_idle(t, T)
    a = keys(t, [(0, 0), (0.15, 1), (0.42, 1), (0.52, 0), (1, 0)])
    b = keys(t, [(0, 0), (0.48, 0), (0.62, 1), (0.88, 1), (1, 0)])
    s.D = {k: v for k, v in s.D.items() if not k.startswith("Wing")}
    for sd, chain in WINGS.items():
        e = a if sd > 0 else b
        for k, wn in enumerate(chain):
            fold = 1 - e
            if k == 0:
                s.rot(wn, wback(sd, 0.75 * fold) @ wup(sd, 0.3 * fold + 0.5 * e))
            elif k == 1:
                s.rot(wn, wback(sd, 0.55 * fold) @ wup(sd, -0.35 * fold - 0.1 * e))
            else:
                s.rot(wn, wback(sd, 0.35 * fold) @ wup(sd, -0.2 * fold))
    s.rot("Neck", yaw(0.35 * (a - b)))
    return s


# ------------------------------------------------------------------ flight clips
def lean_body(s, amt):
    """tip an upright body forward into flight attitude, keep the neck/head looking ahead"""
    if LEAN > 0 and amt > 0:
        s.rot("Hips", pitch(-LEAN * amt))
        s.rot("Chest", pitch(0.25 * LEAN * amt))
        s.rot("Neck", pitch(0.75 * LEAN * amt))
        s.headW = QI


def c_fly(t, T):
    s = Pose()
    lean_body(s, 1.0)
    L = LEG_LEN
    if HAS_WINGS:
        wings_flap(s, t, P.get("flapA", 1.0))
        # body is thrown up by each downstroke and sinks on the upstroke; chest heaves, hips counter
        s.off = Vector((0, 0, 0.08 * L * sin(TAU * (t - 0.15))))
        s.rot("Chest", pitch(0.09 * sin(TAU * (t - 0.05))) @ roll(0.03 * sin(TAU * t * 0.5)))
        s.rot("Hips", pitch(-0.06 * sin(TAU * (t - 0.15))))
        s.rot("Neck", pitch(-0.1 * sin(TAU * (t - 0.12))))
    else:  # wingless sky dragon: swims through the air
        for k, tn in enumerate(TAILS):
            s.rot(tn, yaw(0.22 * sin(TAU * t - 0.9 * k)) @ pitch(0.08 * sin(TAU * t - 0.9 * k + 1.2)))
        s.rot("Hips", yaw(0.12 * sin(TAU * t + 0.9)) @ pitch(0.05 * sin(TAU * t)))
        s.rot("Chest", yaw(-0.16 * sin(TAU * t + 1.6)) @ pitch(0.06 * sin(TAU * t + 0.8)))
        s.rot("Neck", yaw(0.1 * sin(TAU * t + 2.2)))
        s.off = Vector((0, 0, 0.06 * L * sin(TAU * t)))
    tuck_legs(s, 1.0, t)
    for k, tn in enumerate(TAILS):
        # tail whips with the wingbeat (vertical) and steers (sideways)
        s.rot(tn, pitch(0.14 * sin(TAU * t - 0.8 * (k + 1))) @ yaw(0.07 * sin(TAU * 0.5 * t - 0.6 * k)))
    s.stab = 0.95 if LEAN > 0.3 else 0.6
    return s


def c_glide(t, T):
    s = Pose()
    lean_body(s, 1.0)
    if HAS_WINGS:
        wings_glide(s, t, wobble=2.0)
    else:
        for k, tn in enumerate(TAILS):
            s.rot(tn, yaw(0.14 * sin(TAU * t - 0.8 * k)))
    tuck_legs(s, 1.0, (t * 2) % 1.0)
    for k, tn in enumerate(TAILS):
        s.rot(tn, yaw(0.12 * sin(TAU * t - 0.6 * k)) @ pitch(0.06 * sin(TAU * 2 * t - 0.7 * k)))
    s.rot("Chest", roll(0.05 * sin(TAU * t)) @ pitch(0.03 * sin(TAU * 2 * t)))
    s.rot("Hips", roll(-0.03 * sin(TAU * t + 0.5)))
    # looks around while gliding: left ... ahead ... right ... ahead
    look = keys(t, [(0, 0), (0.15, 0.5), (0.35, 0.5), (0.5, 0), (0.65, -0.45), (0.85, -0.45), (1, 0)])
    s.rot("Neck", yaw(0.6 * look) @ pitch(-0.1 * abs(look)))
    s.rot("Head", yaw(0.4 * look))
    s.stab = 0.85 if LEAN > 0.3 else 0.0
    return s


TAKEOFF_LAUNCH = 0.4   # normalised time the feet leave the ground (PetAnimator lifts the root from here)
LAND_TOUCH = 0.42      # normalised time the feet touch the ground


def c_takeoff(t, T):
    s = Pose()
    L = LEG_LEN
    crouch = keys(t, [(0, 0), (0.32, 1), (0.42, 0)])
    air = sm((t - TAKEOFF_LAUNCH) / 0.35)
    s.off = Vector((0, 0.03 * L * crouch, -DROP * 0.5 - 0.16 * L * crouch + 0.05 * L * keys(t, [(0.38, 0), (0.46, 1), (0.6, 0)])))
    s.rot("Chest", pitch(-0.15 * crouch + 0.2 * keys(t, [(0.36, 0), (0.5, 1), (1, 0.2)])))
    s.rot("Neck", pitch(-0.15 * crouch + 0.15 * air))
    if HAS_WINGS:
        if t < 0.35:
            wa = keys(t, [(0, 0.3), (0.32, 1.15)])
        elif t < 0.55:
            wa = keys(t, [(0.35, 1.15), (0.55, -0.7)])
        elif t < 0.8:
            wa = keys(t, [(0.55, -0.7), (0.8, 1.0)])
        else:
            wa = keys(t, [(0.8, 1.0), (1.0, -0.6)])
        fold = 1 - sm(t / 0.25)
        for sd, chain in WINGS.items():
            for k, wn in enumerate(chain):
                lag = wa * (1.0 if k == 0 else 0.5)
                s.rot(wn, wback(sd, 0.6 * fold * (1 if k == 0 else 0.6)) @ wup(sd, lag))
    lean_body(s, air)
    tuck_legs(s, air)
    for l in LEGS:
        s.tg[l.i] = (l.F0.copy(), 1 - sm((t - TAKEOFF_LAUNCH + 0.02) / 0.08))
    for k, tn in enumerate(TAILS):
        s.rot(tn, pitch(-0.2 * crouch + 0.1 * air))
    return s


def c_land(t, T):
    s = Pose()
    L = LEG_LEN
    flare = keys(t, [(0, 0.3), (0.3, 1), (0.48, 0.9), (0.75, 0)])
    impact = keys(t, [(LAND_TOUCH - 0.02, 0), (0.52, 1), (0.75, 0.2), (1, 0)])
    settle = sm((t - 0.55) / 0.4)
    s.off = Vector((0, 0, -DROP * 0.5 - 0.14 * L * impact))
    s.rot("Hips", pitch(0.3 * flare * (1 - settle)))
    s.rot("Chest", pitch(-0.1 * impact))
    s.rot("Neck", pitch(-0.25 * flare + 0.1 * impact))
    if HAS_WINGS:
        back = sin(TAU * 4 * t) * 0.25 * keys(t, [(0, 0), (0.15, 1), (0.42, 1), (0.5, 0)])
        for sd, chain in WINGS.items():
            for k, wn in enumerate(chain):
                up = (0.75 if k == 0 else 0.2) * flare + (back if k == 0 else 0)
                s.rot(wn, wback(sd, -0.35 * flare if k == 0 else 0) @ wup(sd, up))
        tmp = Pose()
        fold_wings(tmp, settle)
        for k, v in tmp.D.items():
            s.D[k] = s.D.get(k, QI) @ v
    lean_body(s, 1 - sm(t / (LAND_TOUCH * 0.8)))
    reach_legs(s, 1 - sm((t - LAND_TOUCH + 0.1) / 0.1))
    ground = sm((t - LAND_TOUCH + 0.03) / 0.05)
    for l in LEGS:
        s.tg[l.i] = (l.F0.copy(), ground)
    for k, tn in enumerate(TAILS):
        s.rot(tn, pitch(-0.25 * flare + 0.15 * impact))
    return s


# ------------------------------------------------------------------ moth (always fluttering)
def c_moth_idle(t, T):
    s = Pose()
    nb = 2
    o = 0.5 + 0.5 * sin(TAU * nb * t)
    for sd, chain in WINGS.items():
        for k, wn in enumerate(chain):
            s.rot(wn, wup(sd, (0.9 * o + 0.1) if k == 0 else 0.1 * o))
    s.off = Vector((0, 0, 0.01 * sin(TAU * t)))
    return s


# ------------------------------------------------------------------ swim / water
def c_swim_idle(t, T):
    s = Pose()
    s.off = Vector((0, 0, 0.05 * sin(TAU * t)))
    for tn in TENTS:
        i = int(tn[4:].split("_")[0]); k = int(tn.split("_")[1])
        r = R.head0[tn]
        radial = Vector((r.x, r.y, 0))
        radial = radial.normalized() if radial.length > 1e-4 else X
        ax = radial.cross(Z)
        s.rot(tn, q(ax, 0.12 * sin(TAU * 2 * t - 0.8 * k + i * 1.1)))
    if TYPE == "seahorse":
        for k, tn in enumerate(TAILS):
            s.rot(tn, pitch(0.12 * sin(TAU * 2 * t - 0.7 * k)))
        for l in LEGS:
            s.rot(l.U, pitch(0.15 * sin(TAU * 2 * t + (0 if l.side > 0 else 1))))
        s.rot("Chest", pitch(0.03 * sin(TAU * t)))
    return s


def c_swim(t, T):
    s = Pose()
    pulse = keys(t, [(0, 0), (0.28, 1), (0.6, 0.15), (1, 0)])
    s.off = Vector((0, 0, 0.08 * pulse - 0.03))
    for tn in TENTS:
        i = int(tn[4:].split("_")[0]); k = int(tn.split("_")[1])
        r = R.head0[tn]
        radial = Vector((r.x, r.y, 0))
        radial = radial.normalized() if radial.length > 1e-4 else X
        ax = radial.cross(Z)
        # contract: tentacles snap inward, then trail out with a lagged wave
        a = -0.35 * keys((t - 0.05 * k) % 1.0, [(0, 0), (0.25, 1), (0.6, -0.3), (1, 0)]) + 0.08 * sin(TAU * t - 0.9 * k + i)
        s.rot(tn, q(ax, a))
    if TYPE == "seahorse":
        for k, tn in enumerate(TAILS):
            s.rot(tn, pitch(0.25 * sin(TAU * t - 0.8 * k)))
        for l in LEGS:
            s.rot(l.U, pitch(0.5 * sin(TAU * t + (0 if l.side > 0 else math.pi))))
            s.rot(l.L, pitch(0.4 * max(0, sin(TAU * t + 0.6 + (0 if l.side > 0 else math.pi)))))
        s.rot("Chest", pitch(0.06 * sin(TAU * t)))
        s.rot("Neck", pitch(-0.05 * sin(TAU * t)))
    return s


def c_swim_roar(t, T):
    s = Pose()
    hit = keys(t, [(0, 0), (0.3, 0), (0.42, 1), (0.78, 0.9), (1, 0)])
    ant = keys(t, [(0, 0), (0.2, 1), (0.32, 1), (0.42, 0)])
    trem = keys(t, [(0.4, 0), (0.45, 1), (0.75, 1), (0.85, 0)]) * sin(TAU * 20 * t * T)
    s.off = Vector((0, 0, 0.1 * hit - 0.06 * ant))
    for tn in TENTS:
        i = int(tn[4:].split("_")[0]); k = int(tn.split("_")[1])
        r = R.head0[tn]
        radial = Vector((r.x, r.y, 0))
        radial = radial.normalized() if radial.length > 1e-4 else X
        ax = radial.cross(Z)
        s.rot(tn, q(ax, (0.55 if k == 1 else 0.25) * hit - 0.3 * ant + 0.05 * trem * sin(i)))
    if TYPE == "seahorse":
        s.rot("Chest", pitch(0.2 * hit - 0.1 * ant))
        s.rot("Neck", pitch(0.3 * hit - 0.2 * ant))
        s.rot("Head", pitch(0.2 * hit + 0.03 * trem))
        for l in LEGS:  # rear up, hooves strike
            s.rot(l.U, pitch(0.9 * hit * (0.8 + 0.2 * sin(TAU * 4 * t * T))))
            s.rot(l.L, pitch(-0.8 * hit))
        for tn in TAILS:
            s.rot(tn, pitch(0.15 * hit))
    return s


# ------------------------------------------------------------------ snakes
def serpent_body(s, t, amp, cycles=1.0, raise_=0.0):
    if TYPE == "snake":
        # head end raised ready to strike; body chain undulates (travelling wave)
        s.rot("Chest", pitch(0.35 + raise_))
        s.rot("Neck", pitch(0.3 + raise_ * 0.5))
        s.rot("Head", pitch(-0.45 - raise_ * 0.8))
        n = len(TAILS)
        prev = 0.0
        for k, tn in enumerate(TAILS):
            ang = amp * sin(TAU * cycles * t - TAU * 0.9 * (k + 1) / max(n, 1))
            s.rot(tn, yaw(ang - prev))
            prev = ang
        s.rot("Hips", yaw(amp * 0.5 * sin(TAU * cycles * t)))
        s.rot("Neck", yaw(-amp * 0.4 * sin(TAU * cycles * t)))
    else:  # upright coiled serpent: S-curve sway up the body
        s.rot("Hips", yaw(amp * 0.5 * sin(TAU * cycles * t)) @ roll(amp * 0.3 * sin(TAU * cycles * t + 0.4)))
        s.rot("Chest", yaw(-amp * 0.8 * sin(TAU * cycles * t - 0.8)) @ pitch(raise_ * 0.4))
        s.rot("Neck", yaw(amp * 0.9 * sin(TAU * cycles * t - 1.6)) @ pitch(raise_ * 0.5))
        s.rot("Head", yaw(-amp * 0.5 * sin(TAU * cycles * t - 2.2)))


def c_snake_idle(t, T):
    s = Pose()
    serpent_body(s, t, 0.12, cycles=2, raise_=0.04 * sin(TAU * t))
    s.rot("Head", yaw(0.08 * sin(TAU * 3 * t)))
    return s


def c_slither(t, T):
    s = Pose()
    serpent_body(s, t, 0.35 if TYPE == "snake" else 0.2, cycles=1)
    return s


def c_snake_roar(t, T):
    """coil back, then strike forward"""
    s = Pose()
    ant = keys(t, [(0, 0), (0.25, 1), (0.36, 1), (0.42, 0)])
    hit = keys(t, [(0, 0), (0.36, 0), (0.44, 1), (0.7, 0.8), (1, 0)])
    trem = keys(t, [(0.44, 0), (0.48, 1), (0.7, 1), (0.8, 0)]) * sin(TAU * 18 * t * T)
    serpent_body(s, t, 0.08, cycles=1, raise_=0.35 * ant + 0.15 * hit)
    s.off = Vector((0, 0.1 * ant - 0.18 * hit, 0))
    s.rot("Neck", pitch(0.4 * ant - 0.3 * hit))
    s.rot("Head", pitch(-0.3 * ant + 0.45 * hit + 0.04 * trem))
    return s


# ------------------------------------------------------------------ clip set per creature
FLYER = STYLE in ("bird", "dragon", "moth", "skydragon")
CLIPS = {}  # name -> (fn, seconds, loop)
if STYLE == "moth":
    CLIPS = {"idle": (c_moth_idle, 4.0, True), "fly": (c_fly, P["flapT"], True),
             "glide": (c_fly, P["flapT"] * 1.8, True), "takeoff": (c_takeoff, 0.9, False),
             "land": (c_land, 1.0, False), "roar": (c_roar, P["roarT"], False)}
elif TYPE in ("snake", "serpent"):
    CLIPS = {"idle": (c_snake_idle, P["idleT"], True), "slither": (c_slither, P["slitherT"], True),
             "roar": (c_snake_roar, P["roarT"], False)}
elif TYPE in ("jelly", "kraken", "seahorse"):
    CLIPS = {"idle": (c_swim_idle, P["idleT"], True), "swim": (c_swim, P["swimT"], True),
             "roar": (c_swim_roar, P["roarT"], False)}
else:
    CLIPS = {"idle": (c_idle, P["idleT"], True), "roar": (c_roar, P["roarT"], False)}
    if LEGS and "walkT" in P:  # flyers walk too (wings folded) between their flights
        CLIPS["walk"] = (c_walk, P["walkT"], True)
    if FLYER:
        CLIPS.update({"fly": (c_fly, P.get("flapT", 1.0), True), "glide": (c_glide, 6.0, True),
                      "takeoff": (c_takeoff, 1.1 if STYLE != "dragon" else 1.3, False),
                      "land": (c_land, 1.3 if STYLE != "dragon" else 1.5, False)})
    ACTS = {"sniff": c_sniff, "shake": c_shake, "stomp": c_stomp, "stretch": c_stretch, "look": c_look,
            "crouch": c_crouch, "pound": c_pound, "twitch": c_twitch, "wingstretch": c_wingstretch}
    ACT_LEN = {"sniff": 4.0, "shake": 1.6, "stomp": 2.6, "stretch": 3.4, "look": 4.0, "crouch": 4.0,
               "pound": 3.0, "twitch": 1.6, "wingstretch": 4.0}
    for a in P.get("acts", ()):
        if a == "pound" and not ARMS:
            continue
        if a == "wingstretch" and not HAS_WINGS:
            continue
        CLIPS["act_" + a] = (ACTS[a], ACT_LEN[a], False)
if ONLY:
    CLIPS = {k: v for k, v in CLIPS.items() if k in ONLY}

EVENTS = {"takeoff": {"launch": TAKEOFF_LAUNCH}, "land": {"touch": LAND_TOUCH}}


# ------------------------------------------------------------------ bake
def sample(fn, T, loop, fps):
    n = max(2, round(T * fps))
    frames = []
    for i in range(n + (0 if loop else 1)):
        t = i / n
        frames.append(solve(fn(t, T)))
    return frames


def to_roblox_q(qt):
    # Blender (x, y, z) -> Roblox (-x, z, y)  (proper rotation, det +1)
    return (-qt.x, qt.z, qt.y, qt.w)


out = {"name": roblox_name(NAME), "blender": NAME, "rig": TYPE, "style": STYLE, "fps": FPS_EXPORT,
       "stride": 0, "clips": {}, "events": {}}
ref = "Head" if R.has("Head") else "Chest" if R.has("Chest") else "Hips"
out["ref"] = {"bone": ref, "dist": (R.head0[ref] - R.head0["Root"]).length}

for cname, (fn, T, loop) in CLIPS.items():
    frames = sample(fn, T, loop, FPS_EXPORT)
    rot = {}
    for b in R.names:
        if b == "Root":
            continue
        seq = []
        moving = False
        for D, off in frames:
            qt = D.get(b, QI).normalized()
            if qt.w < 0:
                qt = -qt
            if abs(qt.w) < 0.99999:
                moving = True
            seq.extend(round(v, 4) for v in to_roblox_q(qt))
        if moving:
            rot[b] = seq
    offs = []
    for D, off in frames:
        offs.extend(round(v, 4) for v in (-off.x, off.z, off.y))
    clip = {"n": len(frames), "loop": loop, "len": T, "rot": rot, "off": offs}
    if cname in ("walk", "slither", "swim"):
        # distance travelled per cycle (Blender units): stride for legs, ~0.7 wavelength for slithering
        clip["stride"] = STRIDE if cname == "walk" else 0.6 * (max(v.y for v in R.tail0.values()) - min(v.y for v in R.head0.values()))
    if cname in EVENTS:
        out["events"][cname] = EVENTS[cname]
    out["clips"][cname] = clip
    print("CLIP", cname, "frames", len(frames), "bones", len(rot))

os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
if not ONLY:
  with open(os.path.join(HERE, "out", roblox_name(NAME) + ".json"), "w") as f:
    json.dump(out, f, separators=(",", ":"))
print("LEGS", len(LEGS), "LEG_LEN %.3f STRIDE %.3f DROP %.3f" % (LEG_LEN, STRIDE, DROP))

# ------------------------------------------------------------------ Blender actions (+ .blend) and previews
pbs = arm.pose.bones
for pb in pbs:
    pb.rotation_mode = "QUATERNION"
sc = bpy.context.scene
sc.render.fps = FPS_AUTHOR


def apply(D, off):
    for pb in pbs:
        n = pb.name
        r0 = R.R0[n]
        pb.rotation_quaternion = r0.inverted() @ D.get(n, QI) @ r0
        pb.location = (r0.inverted() @ off) if n == "Hips" else Vector()


arm.animation_data_create()
for cname, (fn, T, loop) in CLIPS.items():
    act = bpy.data.actions.new(cname)
    act.use_fake_user = True
    arm.animation_data.action = act
    n = max(2, round(T * FPS_AUTHOR))
    for i in range(n + 1):
        D, off = solve(fn((i / n) % 1.0 if loop else i / n, T))
        apply(D, off)
        for pb in pbs:
            pb.keyframe_insert("rotation_quaternion", frame=i + 1)
            if pb.name == "Hips":
                pb.keyframe_insert("location", frame=i + 1)
os.makedirs(os.path.join(HERE, "blend"), exist_ok=True)
arm.animation_data.action = None
if not ONLY:
  bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, "blend", roblox_name(NAME) + ".blend"))

if PREVIEW:
    import math as m
    fdir = os.path.join(HERE, "preview", "_frames", roblox_name(NAME))
    os.makedirs(fdir, exist_ok=True)
    sc.render.engine = "BLENDER_WORKBENCH"
    sc.display.shading.light = "STUDIO"
    sc.display.shading.color_type = "TEXTURE"
    sc.render.resolution_x, sc.render.resolution_y = 300, 260
    cam = bpy.data.objects.new("pcam", bpy.data.cameras.new("pcam"))
    sc.collection.objects.link(cam)
    sc.camera = cam
    cam.data.type = "ORTHO"
    cam.data.ortho_scale = 3.8
    # ground plate (dark) so foot contact / sinking is visible
    bpy.ops.mesh.primitive_plane_add(size=8, location=(0, 0, -0.002))
    g = bpy.context.active_object
    mat = bpy.data.materials.new("g")
    mat.diffuse_color = (0.12, 0.12, 0.14, 1)
    g.data.materials.append(mat)
    views = {"side": ((5, 0, 1.75), (m.radians(80), 0, m.radians(90))),
             "q": ((3.6, -3.6, 2.6), (m.radians(66), 0, m.radians(45)))}
    for cname, (fn, T, loop) in CLIPS.items():
        nshots = 8
        for j in range(nshots):
            t = j / nshots if loop else j / (nshots - 1)
            D, off = solve(fn(t, T))
            apply(D, off)
            bpy.context.view_layer.update()
            for vn, (loc, rot_) in views.items():
                if vn == "q" and cname not in ("walk", "fly", "takeoff", "land", "roar"):
                    continue
                cam.location, cam.rotation_euler = loc, rot_
                sc.render.filepath = os.path.join(fdir, f"{cname}_{vn}_{j}.png")
                bpy.ops.render.render(write_still=True)
    print("PREVIEW", fdir)
