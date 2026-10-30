# wing3: wings for PetsV3 flyers (built from the Storm Wyvern fix, 2026-10-08).
# Rules that keep wings from cutting through each other / the body (checked by blockkit.overlap_report):
#   * the FLAP turns about the wing ROOT line (shoulder -> body attachment): the membrane's body edge stays on the body
#   * the OUTER wing folds about a HINGE line (wrist -> trailing point): it closes like a fan, never through the inner wing
#   * small sweeps only (big back-sweeps swing the root edge across the spine -> left/right wings collide)
# Geometry per side is mirrored on x. Bones: Wing_<side> (arm + inner wing), WingTip_<side> (outer wing).
import math
from mathutils import Vector, Quaternion
import _common as cm


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


class Wing:
    """S shoulder, W wrist, H hinge end (trailing point; outer wing folds about W->H), BB body attachment."""

    def __init__(self, S, W, H, BB):
        self.S, self.W, self.H, self.BB = Vector(S), Vector(W), Vector(H), Vector(BB)

    def root_axis(self, side):
        s = 1 if side == "L" else -1
        return (X(self.BB, s) - X(self.S, s)).normalized()

    def arm_axis(self, side):
        s = 1 if side == "L" else -1
        return (X(self.W, s) - X(self.S, s)).normalized()

    def hinge_axis(self, side):
        s = 1 if side == "L" else -1
        return (X(self.H, s) - X(self.W, s)).normalized()

    def key(self, k, f, up, fwd=0.0, twist=0.0, tip=0.0, side=None):
        """up + raises the wing (about the root line), fwd + sweeps forward (about the vertical), twist + = leading
        edge down (about the arm), tip + folds the outer wing DOWN about the hinge."""
        for sd, sx in (("L", 1), ("R", -1)):
            if side and sd != side:
                continue
            extra = Quaternion((0, 0, 1), math.radians(-sx * fwd)) @ Quaternion(self.arm_axis(sd), math.radians(sx * twist))
            cm.key_axis(k, "Wing_" + sd, f, self.root_axis(sd), -sx * up, extra=extra)
            cm.key_axis(k, "WingTip_" + sd, f, self.hinge_axis(sd), sx * tip)

    def joints(self):
        out = []
        for s, sd in ((1, "L"), (-1, "R")):
            W, H = X(self.W, s), X(self.H, s)
            out += [(W, H, 0.12, "Wing_" + sd), (W, W, 0.22, "Wing_" + sd)]
        return out


def _ease(u):
    return 0.5 - 0.5 * math.cos(math.pi * u)


def stroke(ph, top=28.0, bot=-48.0, down=0.45, sweep=10.0, twist=12.0, fold=34.0):
    """one wing beat. Power downstroke ph 0 -> down (outer wing lags up, then follows through), recovery upstroke
    (outer wing folds down on the hinge to slip through the air). Returns dict(up, fwd, twist, tip)."""
    ph %= 1.0
    if ph < down:
        u = ph / down
        return dict(up=top + (bot - top) * _ease(u), fwd=sweep * math.sin(math.pi * u) - 2,
                    twist=twist * math.sin(math.pi * u), tip=-5 - 10 * math.sin(math.pi * u) + 13 * u)
    u = (ph - down) / (1 - down)
    return dict(up=bot + (top - bot) * _ease(u), fwd=-2 - 0.8 * sweep * math.sin(math.pi * u),
                twist=-0.7 * twist * math.sin(math.pi * u), tip=8 + fold * math.sin(math.pi * u) - 13 * u)


def membrane(B, wing, s, side, F1, F2, arm_c, finger_c, mem1, mem2, trim, claw_c, arm_w=0.095):
    """bat/dragon wing: arm bar, wrist knuckle + claw, finger 3 = the hinge (inner), fingers 1-2 + 2 scalloped outer
    membranes (outer), inner membrane arm -> finger 3 -> body, trailing-edge trim."""
    S, W, f3, bb = X(wing.S, s), X(wing.W, s), X(wing.H, s), X(wing.BB, s)
    f1, f2 = X(F1, s), X(F2, s)
    wb, tb = "Wing_" + side, "WingTip_" + side
    B.seg(S, W, arm_w, arm_w + 0.005, arm_c, wb, side=(0, 0, 1), ext=0.1)
    B.add(W, (arm_w + 0.015,) * 3, finger_c, wb, studs=[])
    B.spike(W + Vector((0, 0, 0.08)), (s * 0.2, -0.5, 0.8), 0.22, 0.045, claw_c, wb)
    B.seg(W, f3, 0.05, 0.055, finger_c, wb, side=(0, 0, 1), top=(0.55, 0.55), studs=[])
    for f, w in ((f1, 0.06), (f2, 0.052)):
        B.seg(W, f, w, w + 0.005, finger_c, tb, side=(0, 0, 1), top=(0.55, 0.55), studs=[])
    e12 = f1.lerp(f2, 0.5).lerp(W, 0.2)
    e23 = f2.lerp(f3, 0.5).lerp(W, 0.2)
    q = f3.lerp(bb, 0.5).lerp(S, 0.15)
    B.poly([S, W, f3, q, bb], 0.03, mem1, wb)
    B.poly([W, f1, e12, f2], 0.03, mem1, tb)
    B.poly([W, f2, e23, f3], 0.03, mem2, tb)
    nrm = (f1 - W).cross(f3 - W).normalized()
    for a, b, bone in ((f1, e12, tb), (e12, f2, tb), (f2, e23, tb), (e23, f3, tb), (f3, q, wb), (q, bb, wb)):
        B.bar(a, b, nrm, 0.05, 0.04, trim, bone, studs=[], bevel=0.008)


def feathered(B, wing, s, side, tip, arm_c, cov_c, sec_c, pri_c, tip_c=None, n_sec=4, n_pri=5, arm_w=0.10):
    """bird/griffin wing: arm (Wing) with a covert block and secondary feathers hanging back to the hinge line,
    hand (WingTip) with primaries fanning from the wrist; feathers are tapered blocks with a coloured tip."""
    S, W, H, bb = X(wing.S, s), X(wing.W, s), X(wing.H, s), X(wing.BB, s)
    T = X(tip, s)
    wb, tb = "Wing_" + side, "WingTip_" + side
    nrm = (T - W).cross(H - W).normalized()
    if nrm.z < 0:
        nrm = -nrm
    B.seg(S, W, arm_w, arm_w, arm_c, wb, side=(0, 0, 1), ext=0.1)
    B.seg(W, W.lerp(T, 0.35), arm_w * 0.85, arm_w * 0.85, arm_c, tb, side=(0, 0, 1), studs=[])
    # coverts: a plate along the arm's trailing side
    for i in range(3):
        a = S.lerp(W, 0.15 + 0.3 * i)
        back = (H.lerp(bb, 0.5) - a).normalized()
        B.bar(a, a + back * 0.32, nrm, 0.30, 0.05, cov_c, wb, studs=[], bevel=0.012)
    # secondaries: from the arm back to the hinge line / body
    for i in range(n_sec):
        t = (i + 0.5) / n_sec
        a = S.lerp(W, 0.12 + 0.86 * t)
        end = bb.lerp(H, t)
        d = end - a
        B.bar(a, end + d.normalized() * 0.08, nrm, 0.26, 0.04, sec_c, wb, studs=[], bevel=0.01, top=(1, 0.55))
    # primaries: fan from the wrist between the hinge direction and the tip
    for i in range(n_pri):
        t = i / (n_pri - 1)
        dirv = (H - W).normalized().lerp((T - W).normalized(), 0.15 + 0.85 * t).normalized()
        ln = (T - W).length * (0.62 + 0.38 * t)
        a = W + dirv * 0.05
        e = W + dirv * ln
        B.bar(a, e, nrm, 0.22, 0.045, pri_c, tb, studs=[], bevel=0.01, top=(1, 0.4))
        if tip_c:
            B.bar(W + dirv * ln * 0.78, e + dirv * 0.02, nrm, 0.20, 0.05, tip_c, tb, studs=[], bevel=0.008, top=(1, 0.3))
