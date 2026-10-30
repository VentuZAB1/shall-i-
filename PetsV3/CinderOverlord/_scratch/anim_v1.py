

# ------------------------------------------------------------------ animation (clips 2026-10-27, refs: ANIM_REFS.md)
# No legs: the rear body lies on the ground (all its bends are yaw = in the ground plane, so it never sinks); the reared
# neck holds the head level (cobra, ref S2). The crown blades each hinge on their own bone (Crown_1..5).
import petkit as pk
import _common as cm

NECK3 = ["Neck1", "Neck2", "Neck3"]
CROWN = ["Crown_%d" % i for i in range(1, 6)]
CROWN_OUT = [-1, -1, 0, 1, 1]           # outward roll sign per blade (blade 1 is at -x)
SL_AMP = [3, 6, 9, 10, 10, 9, 8, 7, 6]  # slither curvature amplitude per chain bone (deg), U2


def curve(keys, f):
    """smoothstep through (frame, value) keys"""
    for (f0, v0), (f1, v1) in zip(keys, keys[1:]):
        if f0 <= f <= f1:
            u = (f - f0) / float(f1 - f0) if f1 > f0 else 1.0
            return v0 + (v1 - v0) * u * u * (3 - 2 * u)
    return keys[-1][1] if f > keys[-1][0] else keys[0][1]


def sn(f, n, ph=0.0, cyc=1):
    return math.sin(2 * math.pi * (cyc * f / n + ph))


def rest_chain(k, f, skip=()):
    for b in CHAIN:
        if b not in skip:
            k.key(b, f, rot=(0, 0, 0))


def neck(k, f, pitch=0.0, yaw=0.0, head_pitch=0.0, head_yaw=0.0):
    """pitch < 0 = the neck leans back / rises (each neck bone gets a third, <= 8 deg); the head pitch is separate"""
    for b in NECK3:
        k.key(b, f, rot=(pitch / 3.0, yaw / 3.0, 0))
    k.key("Head", f, rot=(head_pitch, head_yaw, 0))


def crown(k, f, vals):
    """vals: per blade (lift, out): lift + = the blade rises (the rest lean-back is 24 deg), out + = it fans outward"""
    for b, sgn, (lift, out) in zip(CROWN, CROWN_OUT, vals):
        k.key(b, f, rot=(lift, 0, sgn * out))              # + pitch = the blade rises toward vertical


def arms(k, f, paddle_l=0.0, paddle_r=0.0, spread=0.0, curl=0.0):
    for s, side, pdl in ((1, "L", paddle_l), (-1, "R", paddle_r)):
        k.key("Arm_" + side, f, rot=(pdl, 0, -s * spread))
        k.key("Claw_" + side, f, rot=(curl, 0, 0))


def idle(k):
    """EMBER BREATHING (plan; refs S2 C1/C2): two slow breaths - the neck rises and sinks back with the head held near
    level, a slow sway, the vents smoke on each breath; one quick tail flick at f80."""
    n = 120
    k.new_action("idle", n, True)
    flick = [(0, 0), (74, 0), (78, 8), (81, -3), (86, 0), (120, 0)]
    for f in range(0, n + 1, 2):
        br = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)                  # 0 -> 1 -> 0 twice
        sway = 2.0 * sn(f, n)
        neck(k, f, pitch=-6 * br, yaw=sway, head_pitch=4 * br, head_yaw=-0.6 * sway)
        k.key("Jaw", f, rot=(1.5 * br, 0, 0))
        rest_chain(k, f, skip=("Tail3", "Tail4"))
        k.key("Tail3", f, rot=(0, 0.4 * curve(flick, f), 0))
        k.key("Tail4", f, rot=(0, curve(flick, f), 0))
        crown(k, f, [(1.5 * br, 0)] * 5)
        arms(k, f, paddle_l=2 * br, paddle_r=2 * br)
    k.finish()
    k.events["idle"] = {"smoke1": round(30 / n, 3), "flick": round(80 / n, 3), "smoke2": round(90 / n, 3)}


def walk(k):
    """SLITHER (refs U1-U4): a lateral curvature wave runs head -> tail (each chain bone lags the one in front by
    3 f), amplitude growing to mid-body; the reared neck counter-yaws so the head stays on its line; the forearms
    paddle 6 deg. Returns the body travel per cycle (the bends stay put on the ground: wave speed x cycle)."""
    n = 48
    lag = 3
    k.new_action("walk", n, True)
    for f in range(0, n + 1, 2):
        for i, b in enumerate(CHAIN):
            k.key(b, f, rot=(0, SL_AMP[i] * sn(f - lag * i, n), 0))
        nk = -SL_AMP[0] * sn(f, n)                                       # cancels the Spine yaw for the front
        neck(k, f, pitch=0.0, yaw=nk + 1.5 * sn(f, n, 0.25), head_yaw=-0.5 * sn(f, n, 0.25),
             head_pitch=0.6 * sn(f, n, 0.1, 2))
        k.key("Jaw", f, rot=(0, 0, 0))
        crown(k, f, [(0, 0)] * 5)
        arms(k, f, paddle_l=6 * sn(f, n, 0.0), paddle_r=6 * sn(f, n, 0.5))
    k.finish()
    k.meta["walk_cycle"] = n
    seg = sum((CP[i + 1] - CP[i]).length for i in range(len(CHAIN))) / len(CHAIN)
    return seg / lag * n


def roar(k):
    """CROWN FLARE (plan; refs #3 + #6): the neck gathers (12 deg up) with the head held level; the five blades flare
    out and up 15 deg with a 2-frame lag (`flare` f20); the jaw opens late, fangs show, the forearms spread (`roar`
    f30); the jaw closes and the blades settle back slower."""
    n = 66
    k.new_action("roar", n, False)
    gather = [(0, 0), (14, -12), (44, -12), (58, -2), (66, 0)]
    head = [(0, 0), (14, 10), (26, 8), (44, 8), (58, 1), (66, 0)]
    jaw = [(0, 0), (24, 0), (30, 26), (44, 24), (54, 2), (66, 0)]
    spread = [(0, 0), (26, 0), (32, 16), (44, 16), (56, 0), (66, 0)]
    for f in range(0, n + 1, 2):
        neck(k, f, pitch=curve(gather, f), head_pitch=curve(head, f))
        k.key("Jaw", f, rot=(curve(jaw, f), 0, 0))
        rest_chain(k, f)
        vals = []
        for i in range(5):
            d = 2 * abs(i - 2)                                           # centre first, the outer blades lag
            u = curve([(0, 0), (14 + d, 0), (22 + d, 1), (44, 1), (60 + d / 2, 0), (66, 0)], f)
            vals.append((15 * u, (10 if i != 2 else 0) * u))
        crown(k, f, vals)
        arms(k, f, spread=curve(spread, f), curl=-0.6 * curve(spread, f))
    k.finish(loop=False)
    k.events["roar"] = {"flare": round(20 / n, 3), "roar": round(30 / n, 3)}


def act_molt(k):
    """THE CROWN SHEDS (plan; refs #9 + U1): the neck arches 25 deg with the head level; the blades lift one by one
    35 deg (2-frame lag, `lift1` f22); the centre blade lifts furthest and holds while the outer blades drop back
    (`lift2` f48, `shed` f56); a ripple runs along the body (tail -> head, 6 deg per bone, 3-bone lag); the blades
    reseat in reverse order, slower; exact rest."""
    n = 110
    k.new_action("act_molt", n, False)
    arch = [(0, 0), (18, -24), (84, -24), (100, -4), (110, 0)]
    head = [(0, 0), (18, 22), (84, 22), (100, 3), (110, 0)]
    for f in range(0, n + 1, 2):
        neck(k, f, pitch=curve(arch, f), head_pitch=curve(head, f))
        k.key("Jaw", f, rot=(curve([(0, 0), (50, 0), (56, 8), (62, 0), (110, 0)], f), 0, 0))
        vals = []
        for i in range(5):
            up_f = 18 + 2 * i                                            # lift one by one (blade 1 -> 5)
            back_f = 96 - 2 * i                                          # reseat in reverse order
            if i == 2:
                keys = [(0, 0), (up_f, 0), (up_f + 10, 35), (44, 35), (52, 40), (84, 40), (back_f, 6), (104, 0), (110, 0)]
            else:
                keys = [(0, 0), (up_f, 0), (up_f + 10, 35), (44, 35), (54, 10), (84, 10), (back_f, 2), (104, 0), (110, 0)]
            vals.append((curve(keys, f), 0.0))
        crown(k, f, vals)
        for i, b in enumerate(CHAIN):                                    # the ripple: tail -> head
            j = len(CHAIN) - 1 - i
            env = curve([(0, 0), (62, 0), (68, 1), (78, 1), (86, 0), (110, 0)], f - 3 * j)
            k.key(b, f, rot=(0, 6 * env * sn(f - 3 * j, 16), 0))
        arms(k, f, curl=curve([(0, 0), (18, 10), (84, 10), (100, 0), (110, 0)], f))
    k.finish(loop=False)
    k.events["act_molt"] = {"lift1": round(22 / n, 3), "lift2": round(48 / n, 3), "shed": round(56 / n, 3)}


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    act_molt(k)
    return stride
