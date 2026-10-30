# Sea Turtle Warrior (Tide egg) - FIERCE style (2026-10-09, FIERCE_PLAN.md "the tide soldier"): a broad-shouldered
# loggerhead-turtle soldier built from tapered blocks and covered in Roblox studs: a big head with a massive hooked
# beak, narrow coral slit eyes under a heavy beak brow, a tattered coral war-band with 2 tails, a short thick neck, a
# keeled carapace (5 keels, serrated rear rim) with keeled shoulder guards, a cream plastron of 3 armour segments,
# forearms flattened like flipper blades ending in 3-claw gripping hands, thick legs with wide paddle feet and 2 claws,
# darker scale patches on the skin, and a dark-bronze barbed TRIDENT (taller than the pet, coral wraps, pearl).
# Old chibi version: _tools/chibi_specs/SeaTurtleWarrior.py
import math
from mathutils import Vector, Quaternion

DISPLAY = "Sea Turtle Warrior"
MOTION = "Walk"
RIG = "biped"
HEIGHT = 9.0                 # chest top ~6 studs at x1 (coordinator HEIGHT rule 2026-10-09)

# FIERCE_PLAN palette = in-game look; Roblox renders ~0.55-0.6x darker -> Blender colours ~1.6-2x brighter
SKIN = (76, 170, 150)        # plan (40,90,80)
SCALE = (44, 108, 100)       # darker scale pattern (plan 24,58,54)
SHELL = (56, 108, 142)       # carapace (plan 26,50,66)
SHELL_L = (70, 128, 164)     # raised scutes
KEEL = (30, 60, 84)          # keels, rim teeth (plan 16,32,44)
PLAST = (224, 206, 150)      # plastron (plan 160,148,108)
PLAST_D = (176, 160, 112)
BEAK = (128, 122, 88)       # horn beak
BEAK_D = (82, 78, 58)
BRONZE = (178, 138, 78)      # trident (plan 112,86,48)
BRONZE_D = (120, 90, 50)
PEARL = (230, 240, 246)
CORAL = (255, 100, 70)       # accent: war-band, trident wraps, eyes
CORAL_D = (200, 64, 50)
EYE = (255, 100, 70)
EYE_HOT = (255, 200, 182)
BLACK = (14, 14, 22)
MOUTH = (86, 18, 30)

H_MODEL = 2.16
PITCH = round(0.042 * (H_MODEL / HEIGHT) / (1.498 / 8.0), 4)

S = (0.40, 0.0, 1.33)                          # shoulder
E = (0.50, 0.04, 1.06)                         # elbow
W = (0.55, -0.08, 0.84)                        # wrist
LEG = ((0.17, 0.02, 0.72), (0.20, -0.08, 0.40), (0.22, 0.02, 0.12))   # hip, knee, ankle (bent: IK reach)
GRIP = Vector((-0.57, -0.22, 0.76))            # right fist grip on the shaft
SHAFT = (0.03, 1.72)                           # shaft bottom / collar z (trident upright at rest)


def X(p, s):
    return Vector((s * p[0], p[1], p[2]))


def face_pt(blk, ax, sg, u, v, out=0.0):
    """point + outward normal on a (tapered, rotated) block's +-x (ax 0: u = local y) or +-y (ax 1: u = local x) face
    at local height v (local z)"""
    t = (v / blk.h.z + 1) / 2
    sc = [blk.bot[i] + (blk.top[i] - blk.bot[i]) * t for i in (0, 1)]
    slope = blk.h[ax] * (blk.top[ax] - blk.bot[ax]) / (2 * blk.h.z)
    ln = Vector((0, 0, -sg * slope))
    ln[ax] = sg
    lp = Vector((0, 0, v))
    lp[ax] = sg * blk.h[ax] * sc[ax]
    lp[1 - ax] = u
    n = (blk.R @ ln).normalized()
    return blk.world(lp) + n * out, n


def inlay(B, blk, ax, sg, pts, color, bone):
    """flush hexagon scale inlays (<= 0.012 proud) on a block face: pts = [(u, v, r)]"""
    for u, v, r in pts:
        r *= 1.2
        c, n = face_pt(blk, ax, sg, u, v, 0.003)
        up = (blk.R @ Vector((0, 0, 1)))
        up = (up - n * up.dot(n)).normalized()
        sd = n.cross(up)
        P = [c + (up * math.cos(a) + sd * math.sin(a)) * r for a in [math.radians(30 + 60 * j) for j in range(6)]]
        B.poly([c] + P + [P[0]], 0.012, color, bone)


def model(k):
    import blockkit as bk
    B = bk.Blocks(k, seed=83, tier=3, plates=False)
    # ---------------- torso: V-taper chest (broad shoulders, narrow waist), pelvis; plastron of 3 armour segments
    chest = B.add((0, 0.0, 1.12), (0.36, 0.24, 0.29), SKIN, "Chest", bot=(0.74, 0.86), top=(1.0, 0.95), rnd=0.38)
    B.add((0, 0.03, 0.80), (0.26, 0.20, 0.14), SKIN, "Spine", bot=(0.9, 0.9), rnd=0.35)
    for zc, hw, hz, bn in ((1.28, 0.25, 0.085, "Chest"), (1.105, 0.215, 0.075, "Chest"), (0.94, 0.165, 0.07, "Chest"),
                           (0.80, 0.15, 0.06, "Spine")):
        if bn == "Chest":
            t = (zc - 0.83) / 0.58
            yf, tilt = -0.24 * (0.86 + 0.09 * t), 2.1
        else:
            t = (zc - 0.66) / 0.28
            yf, tilt = 0.03 - 0.20 * (0.9 + 0.1 * t), 4.1
        B.add((0, yf - 0.012, zc), (hw, 0.022, hz), PLAST if bn == "Chest" else PLAST_D, bn, rot=(tilt, 0, 0),
              bot=(0.82, 1), rnd=0.35)
    # ---------------- carapace: a teardrop flange (only its serrated lower rim shows) + a deep dome carrying
    #                  the plan's 5 continuous keels (3 on the back, 1 down each flank) that end in points at the rim
    B.add((0, 0.19, 1.05), (0.44, 0.045, 0.44), KEEL, "Chest", bot=(0.62, 1), rnd=0.45)            # rim flange
    dome = B.add((0, 0.25, 1.06), (0.42, 0.40, 0.21), SHELL, "Chest", rot=(-90, 0, 0), top=(0.62, 0.66),
                 rnd=0.25)
    hz, R = dome.h.z, dome.R

    def ridge(pts, hw, hd):
        """keel along dome-local (x, y, z, nx, ny, nz) samples: half buried, last piece ends in a point"""
        W = [(dome.world((x, y, z)), (R @ Vector((nx, ny, nz))).normalized()) for x, y, z, nx, ny, nz in pts]
        for i in range(len(W) - 1):
            (a, na), (b, nb) = W[i], W[i + 1]
            n = (na + nb).normalized()
            last = i == len(W) - 2
            B.seg(a, b, hw, hd, KEEL, "Chest", side=n.cross(b - a).normalized(), ext=0.0 if last else 0.02,
                  top=(0.25, 0.4) if last else (1, 1), rnd=0.3)
    for u, hd in ((0.0, 0.05), (0.13, 0.035), (-0.13, 0.035)):                                  # back keels
        ridge([(u, -0.30, hz - 0.08, 0, -0.5, 1), (u * 1.05, -0.21, hz, 0, 0, 1), (u * 1.05, 0.21, hz, 0, 0, 1),
               (u * 0.75, 0.38, -0.17, 0, 0.9, 0.55)], 0.025, hd)
    for s_ in (1, -1):                                                                        # flank keels
        ridge([(s_ * 0.34, -0.29, 0.0, s_, 0, 0.38), (s_ * 0.34, 0.20, 0.0, s_, 0, 0.38),
               (s_ * 0.31, 0.38, -0.12, s_, 0.6, 0.38)], 0.025, 0.035)
    for x, L in ((-0.22, 0.09), (-0.11, 0.11), (0.0, 0.13), (0.11, 0.11), (0.22, 0.09)):     # serrated rear rim
        B.spike((x, 0.19, 0.64), (x * 0.4, 0.3, -1), L, 0.045, KEEL, "Chest", side=(1, 0, 0), top=(0.15, 0.4))
    # ---------------- thick neck jutting forward + a big domed loggerhead head with a massive hooked beak
    neck = B.seg((0, 0.0, 1.34), (0, -0.10, 1.52), 0.16, 0.15, SKIN, "Neck", ext=0.03)
    for s_ in (1, -1):
        inlay(B, neck, 0, s_, [(0.02, 0.02, 0.04), (-0.06, -0.05, 0.035)], SCALE, "Neck")
    head = B.add((0, -0.15, 1.65), (0.19, 0.20, 0.18), SKIN, "Head", top=(0.70, 0.72), rnd=0.45)
    for x, y, h in ((0.0, -0.19, 0.04), (0.05, -0.115, 0.03), (-0.05, -0.115, 0.03), (0.0, -0.07, 0.026)):
        B.add((x, y, 1.831), (h, h, 0.006), SCALE, "Head", role="detail", bevel=0.006)          # crown scutes
    B.seg((0, -0.28, 1.585), (0, -0.48, 1.50), 0.18, 0.07, BEAK, "Head", top=(0.50, 0.75), ext=0.02, rnd=0.3)
    B.spike((0, -0.49, 1.535), (0, -0.1, -1), 0.15, 0.068, BEAK, "Head", side=(1, 0, 0), top=(0.3, 0.3))  # hook
    for s_ in (1, -1):
        B.add((s_ * 0.035, -0.455, 1.555), (0.012, 0.006, 0.009), BLACK, "Head", rot=(40, 0, 0), role="detail",
              bevel=0.003)                                                                     # nostrils
        B.seg((s_ * 0.15, -0.31, 1.515), (s_ * 0.08, -0.46, 1.48), 0.01, 0.006, BEAK_D, "Head", role="detail",
              bevel=0.003)                                                                     # beak edge
    B.add((0, -0.32, 1.482), (0.12, 0.10, 0.006), MOUTH, "Jaw", role="detail", bevel=0.003)
    B.seg((0, -0.24, 1.455), (0, -0.45, 1.462), 0.155, 0.03, BEAK, "Jaw", top=(0.55, 0.9), ext=0.02, rnd=0.3)
    # heavy beak brow + narrow slanted coral eyes on the skull front, above the beak
    for s_ in (1, -1):
        B.add((s_ * 0.092, -0.335, 1.718), (0.078, 0.036, 0.03), SCALE, "Head", rot=(0, -s_ * 22, s_ * 18),
              role="detail", bevel=0.012)                                                      # brow
        B.add((s_ * 0.098, -0.318, 1.672), (0.058, 0.03, 0.024), BLACK, "Head", rot=(0, -s_ * 18, s_ * 24),
              role="detail", bevel=0.005)                                                      # socket
        B.add((s_ * 0.101, -0.344, 1.672), (0.048, 0.006, 0.013), EYE, "Head", rot=(0, -s_ * 18, s_ * 24),
              role="detail", bevel=0.003)                                                      # slit
        B.add((s_ * 0.115, -0.346, 1.676), (0.02, 0.004, 0.006), EYE_HOT, "Head", rot=(0, -s_ * 18, s_ * 24),
              role="detail", bevel=0.002)                                                      # hot centre
    # tattered coral war-band = a headband just above the brows (fitted to the domed skull), knot + 2 ragged tails
    B.add((0, -0.15, 1.768), (0.19 * 0.74 + 0.012, 0.20 * 0.76 + 0.012, 0.024), CORAL, "Head", role="limb",
          rnd=0.2, top=(0.965, 0.965), bot=(1.03, 1.03))
    B.add((0, 0.03, 1.76), (0.06, 0.04, 0.05), CORAL_D, "Head", role="limb")
    for s_ in (1, -1):
        a, b, c = Vector((s_ * 0.04, 0.05, 1.76)), Vector((s_ * 0.12, 0.24, 1.69)), Vector((s_ * 0.18, 0.42, 1.63))
        n2 = (s_ * 0.5, -0.25, 1)
        B.bar(a, b, (0, -0.25, 1), 0.085, 0.022, CORAL, "Band1", role="limb")
        B.bar(b - (b - a).normalized() * 0.03, c, n2, 0.08, 0.022, CORAL, "Band2", role="limb")
        d = (c - b).normalized()
        side = d.cross(Vector(n2).normalized()).normalized()
        for off, L in ((0.022, 0.10), (-0.022, 0.07)):                                       # ragged split end
            B.bar(c - d * 0.02 + side * off, c + d * L + side * off * 1.6, n2, 0.036, 0.02, CORAL, "Band2",
                  role="limb", top=(1, 0.15))
    # ---------------- arms: keeled + spiked shell pauldron, upper arm, flipper-blade forearm, 3-claw gripping hand
    for s_, side in ((1, "L"), (-1, "R")):
        Sv, Ev, Wv = X(S, s_), X(E, s_), X(W, s_)
        B.seg(Sv, Ev, 0.10, 0.10, SKIN, "Arm_" + side, ext=0.08)
        B.add(Sv + Vector((s_ * 0.05, 0.0, 0.07)), (0.15, 0.16, 0.06), SHELL, "Arm_" + side, rot=(0, -s_ * 26, 0),
              top=(0.70, 0.74), rnd=0.40)                                                      # pauldron
        for dy in (-0.07, 0.06):
            B.spike(Sv + Vector((s_ * 0.10, dy, 0.13)), (s_ * 0.5, 0.25, 1), 0.10, 0.03, KEEL, "Arm_" + side,
                    top=(0.15, 0.3))                                                           # pauldron spikes
        fa = B.seg(Ev, Wv, 0.13, 0.055, SKIN, "Fore_" + side, side=(0, 1, 0.35), ext=0.06, top=(0.75, 0.9),
                   rnd=0.35)                                                                   # flipper blade
        inlay(B, fa, 1, s_, [(-0.05, 0.07, 0.042), (0.045, 0.0, 0.04), (-0.03, -0.08, 0.036)], SCALE, "Fore_" + side)
        B.spike(Ev.lerp(Wv, 0.35) + Vector((0, 0.10, 0)), (0, 0.6, -1), 0.13, 0.04, SKIN, "Fore_" + side,
                side=(1, 0, 0), top=(0.2, 0.4))                                                # trailing flipper edge
        hand = "Hand_" + side
        B.add(Wv + Vector((0, -0.06, -0.08)), (0.09, 0.095, 0.08), SKIN, hand, rnd=0.3)        # fist
        for gx in (-0.055, 0.0, 0.055):
            B.spike(Wv + Vector((gx, -0.16, -0.06)), (0, -0.3, -1), 0.065, 0.017, KEEL, hand)  # 3 gripping claws
    # ---------------- trident (own bone, child of the right hand): smooth dark bronze shaft, 2 coral wraps,
    #                  barbed prongs, pearl
    x, y = GRIP.x, GRIP.y
    T = dict(nostud=True, role="limb")
    B.seg((x, y, SHAFT[0]), (x, y, SHAFT[1]), 0.032, 0.032, BRONZE, "Trident", **T)
    for zc in (0.56, 0.92):
        B.add((x, y, zc), (0.042, 0.042, 0.035), CORAL, "Trident", **T)
    B.add((x, y, SHAFT[0] + 0.03), (0.042, 0.042, 0.03), BRONZE_D, "Trident", **T)
    top = SHAFT[1]
    B.add((x, y, top), (0.05, 0.045, 0.045), BRONZE_D, "Trident", **T)                            # collar
    B.add((x, y, top + 0.065), (0.17, 0.035, 0.03), BRONZE, "Trident", **T)                       # crossbar
    for dx, ln in ((-0.15, 0.20), (0.0, 0.28), (0.15, 0.20)):
        p0 = Vector((x + dx, y, top + 0.06))
        B.seg(p0, p0 + Vector((0, 0, ln)), 0.026 if dx else 0.030, 0.026 if dx else 0.030, BRONZE, "Trident", **T)
        p1 = p0 + Vector((0, 0, ln))
        B.spike(p1 - Vector((0, 0, 0.02)), (0, 0, 1), 0.12, 0.045, BRONZE, "Trident", side=(0, 1, 0),
                top=(0.1, 0.5), nostud=True)                                                    # blade tip
        sd = -1 if dx < 0 else 1
        B.spike(p1 + Vector((sd * 0.02, 0, 0.0)), (sd * 0.55, 0, -1), 0.08, 0.02, BRONZE, "Trident",
                side=(0, 1, 0), top=(0.15, 0.6), nostud=True)                                   # barb
    B.add((x, y, top + 0.15), (0.05, 0.045, 0.05), PEARL, "Trident", rnd=0.45, **T)               # pearl
    # ---------------- thick legs: thigh + shin with flush scale inlays, shell knee guard with an upward keel,
    #                  wide paddle feet with 2 claws
    for s_, side in ((1, "L"), (-1, "R")):
        H, K, A = (X(p, s_) for p in LEG)
        th = B.seg(H, K, 0.16, 0.17, SKIN, "Leg_" + side, ext=0.0, ext1=0.04, top=(0.85, 0.85), rnd=0.35)
        inlay(B, th, 0, s_, [(-0.04, 0.07, 0.042), (0.05, 0.0, 0.04), (-0.03, -0.08, 0.036)], SCALE, "Leg_" + side)
        sh = B.seg(K, A, 0.125, 0.135, SKIN, "Shin_" + side, ext=0.06, top=(0.9, 0.9), rnd=0.35)
        inlay(B, sh, 0, s_, [(0.0, 0.04, 0.04), (0.05, -0.07, 0.034), (-0.05, -0.05, 0.034)], SCALE, "Shin_" + side)
        kg = K + Vector((0, -0.125, -0.02))
        B.add(kg, (0.11, 0.04, 0.10), SHELL, "Shin_" + side, rot=(-8, 0, 0), top=(0.7, 0.8), rnd=0.4)   # knee guard
        B.spike(kg + Vector((0, -0.035, -0.06)), (0, -0.35, 1), 0.12, 0.03, KEEL, "Shin_" + side,
                top=(0.2, 0.2))                                                                # guard keel
        B.add(A + Vector((s_ * 0.01, -0.07, -0.065)), (0.16, 0.22, 0.055), SKIN, "Foot_" + side, top=(0.9, 0.85),
              rnd=0.3)                                                                         # paddle foot
        for gx in (-0.065, 0.065):
            B.spike(A + Vector((s_ * 0.01 + gx, -0.26, -0.07)), (0, -1, -0.3), 0.08, 0.022, KEEL, "Foot_" + side)
    B.build()
    bk.stud_skin(k, PITCH)
    return {"TH": round(B.th, 3), "PITCH": PITCH}


def rig(k):
    k.joint("Spine", (0, 0.02, 0.66), "Root", tail=(0, 0, 0.3))
    k.joint("Chest", (0, 0.0, 0.92), "Spine", tail=(0, 0, 0.4))
    k.joint("Neck", (0, 0.0, 1.36), "Chest", tail=(0, 0, 0.12))
    k.joint("Head", (0, -0.06, 1.49), "Neck", tail=(0, -0.1, 0.3))           # throat pivot
    k.joint("Jaw", (0, -0.22, 1.485), "Head", tail=(0, -0.2, 0))
    k.joint("Band1", (0, 0.05, 1.76), "Head", tail=(0, 0.18, -0.07))
    k.joint("Band2", (0, 0.24, 1.69), "Band1", tail=(0, 0.18, -0.06))
    for s, side in ((1, "L"), (-1, "R")):
        Sv, Ev, Wv = X(S, s), X(E, s), X(W, s)
        k.joint("Arm_" + side, Sv, "Chest")
        k.joint("Fore_" + side, Ev, "Arm_" + side)
        k.joint("Hand_" + side, Wv, "Fore_" + side, tail=(0, -0.05, -0.2))
        H, K, A = (X(p, s) for p in LEG)
        k.joint("Leg_" + side, H, "Spine")
        k.joint("Shin_" + side, K, "Leg_" + side)
        k.joint("Foot_" + side, A, "Shin_" + side, tail=(0, -0.2, 0))
        k.add_leg2("Leg_" + side, "Shin_" + side, "Foot_" + side, knee=(0, -1, 0))
    k.joint("Trident", GRIP, "Hand_R", tail=(0, 0, 0.5))


def check_pairs():
    P = [("Leg_L", "Leg_R"), ("Shin_L", "Shin_R"), ("Foot_L", "Foot_R")]
    for b in ("Head", "Neck", "Chest", "Spine", "Leg_L", "Leg_R", "Shin_L", "Shin_R", "Foot_L", "Foot_R", "Arm_L",
              "Fore_L", "Hand_L", "Band1", "Band2", "Arm_R", "Jaw"):
        P.append(("Trident", b))
    for s in ("L", "R"):
        for a in ("Fore_" + s, "Hand_" + s):
            for b in ("Spine", "Leg_L", "Leg_R", "Shin_L", "Shin_R", "Head", "Jaw"):
                P.append((a, b))
    for b in ("Chest", "Arm_L", "Arm_R"):
        P.append(("Band2", b))
    P += [("Head", "Chest"), ("Jaw", "Chest"), ("Band1", "Chest"), ("Head", "Arm_L"), ("Head", "Arm_R")]
    P += [("Fore_L", "Chest"), ("Fore_R", "Chest"), ("Hand_L", "Chest"), ("Hand_R", "Chest")]
    return P


def joints():
    out = []
    for s, side in ((1, "L"), (-1, "R")):
        Wv = X(W, s)
        out.append((Wv, Wv, 0.09, "Hand_" + side))
    out.append((GRIP + Vector((0, 0, -0.1)), GRIP + Vector((0, 0, 0.1)), 0.09, "Trident"))
    return out


# ------------------------------------------------------------------ animation (FIERCE_PLAN: surface breath / trident
# thrust / tide-spring twirl). Turtle-only motifs: the gulp of air, the trident taps, thrust, helicopter twirl + strike.
import petkit as pk
import _common as cm

LEGS2 = ["Leg_L", "Leg_R"]
GUARD_R = dict(pitch=-8, roll=4, elbow=12, hand=0)           # right fist holds the upright trident
GUARD_L = dict(pitch=-4, roll=10, elbow=22, hand=30)


def arm(k, f, side, pitch=0.0, yaw=0.0, roll=0.0, elbow=0.0, hand=0.0):
    """pitch - swings the arm forward/up, roll + lifts it sideways, elbow + bends the forearm forward"""
    s = 1 if side == "L" else -1
    k.key("Arm_" + side, f, rot=(pitch, s * yaw, -s * roll))
    k.key("Fore_" + side, f, rot=(-elbow, 0, 0))
    k.key("Hand_" + side, f, rot=(-hand, 0, 0))


def hold(k, f, pitch, roll, elbow, hand=0.0):
    """keep the trident upright in the chest frame (cancels the right arm's pitch / roll)"""
    k.key("Trident", f, rot=(elbow + hand - pitch, 0, -roll), loc=(0, 0, 0))


def band(k, f, n, amp=8.0, lift=0.0, phase=0.0, cycles=2):
    cm.chain(k, f, n, ["Band1", "Band2"], sway=amp, pitch=lift, phase=phase, cycles=cycles, lag=0.18, grow=0.6)


def solve(k, leg, f, T):
    """IK with a gentle toe tilt (the kit's 35 deg toe-off sinks the 0.44-long paddle feet into the floor)"""
    k.solve_leg(leg, f, T, toe=10.0 * min(1.0, max(0.0, T.z) / 0.1))


def _key_q(k, bone, f, q):
    pb = k.arm.pose.bones[bone]
    R0 = k.arm.data.bones[bone].matrix_local.to_quaternion()
    pb.rotation_quaternion = R0.inverted() @ q @ R0
    pb.keyframe_insert("rotation_quaternion", frame=f, group=bone)


def _hand_q(k, f):
    import bpy
    bpy.context.scene.frame_set(f)
    hb = k.arm.pose.bones["Hand_R"]
    return hb.matrix.to_quaternion() @ k.arm.data.bones["Hand_R"].matrix_local.to_quaternion().inverted()


GRIP_Z = 0.002                    # trident butt height when it rests on the ground


def _butt(k, f):
    """(lowest Trident vertex z, world dz per unit slide along the shaft) at frame f"""
    import bpy
    bpy.context.scene.frame_set(f)
    body = k.main
    if not hasattr(k, "_tri_idx"):
        names = {g.index: g.name for g in body.vertex_groups}
        k._tri_idx = [v.index for v in body.data.vertices
                      if v.groups and names[max(v.groups, key=lambda g: g.weight).group] == "Trident"]
    dg = bpy.context.evaluated_depsgraph_get()
    ev = body.evaluated_get(dg)
    me = ev.to_mesh()
    mw = ev.matrix_world
    z = min((mw @ me.vertices[i].co).z for i in k._tri_idx)
    ev.to_mesh_clear()
    pb = k.arm.pose.bones["Trident"]
    shaft = (pb.matrix.to_3x3() @ Vector((0, 1, 0))).normalized()
    return z, (k.arm.matrix_world.to_3x3() @ shaft).z


def need(k, f, target=GRIP_Z):
    """slide (along the shaft, - = butt down) that puts the trident butt at `target` at frame f"""
    z, dz = _butt(k, f)
    return (target - z) / dz


def grip_slide(k, slides):
    """slide the trident through the fist: {frame: t}, t along its shaft (- = down). Keys only (location)."""
    import bpy
    k.bake_bezier_now()
    pb = k.arm.pose.bones["Trident"]
    rows = []
    for f, t in sorted(slides.items()):
        bpy.context.scene.frame_set(f)
        rows.append((f, t, pb.rotation_quaternion.copy(), pb.location.copy()))
    for f, t, q, loc in rows:
        pb.location = loc + (q @ Vector((0, 1, 0))) * t
        pb.keyframe_insert("location", frame=f, group="Trident")


def _ramp(a, b, u):
    u = min(1.0, max(0.0, u))
    return a + (b - a) * (3 * u * u - 2 * u * u * u)


def idle(k):
    """SURFACE BREATH: guard stance; at 15-40 the head lifts and GULPS a big breath (beak opens, chest swells) and
    slowly exhales; at 60-85 it taps the trident butt on the ground twice; the war-band tails flutter."""
    n = 120
    k.new_action("idle", n, True)
    for f in range(0, n + 1, 2):
        b = pk.wave(f, n, 0, 3)
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, 0.006 * b))
        band(k, f, n, amp=7, lift=-2 + 3 * pk.wave(f, n, 0.2, 4), cycles=4)
        arm(k, f, "L", pitch=GUARD_L["pitch"] + 1.5 * b, roll=GUARD_L["roll"], elbow=GUARD_L["elbow"],
            hand=GUARD_L["hand"])
    for f, ch, cz, nk, hd, jw in ((0, 0, 0, 0, 0, 2), (14, 0, 0, 0, 0, 2), (22, -4, 0.012, -6, -16, 26),
                                  (28, -6, 0.022, -8, -20, 4), (36, -6, 0.022, -8, -20, 3), (58, 0, 0, 0, 0, 2),
                                  (120, 0, 0, 0, 0, 2)):
        k.key("Chest", f, rot=(ch, 0, 0), loc=(0, 0, cz))
        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
    for f, p, el in ((0, -8, 12), (60, -8, 12), (64, -14, 32), (68, -8, 12), (72, -8, 12), (76, -14, 32), (80, -8, 12),
                     (120, -8, 12)):
        arm(k, f, "R", pitch=p, roll=4, elbow=el, hand=0)
        hold(k, f, p, 4, el)
    cm.plant(k, n, legs=LEGS2)
    k.bake_bezier_now()                                  # guard grip: the butt rests on the ground (taps lift it)
    k._grip_t = max(need(k, f) for f in range(0, n + 1))
    grip_slide(k, {f: k._grip_t for f in range(0, n + 1)})
    k.finish()
    k.meta["planted"] = LEGS2


def walk(k):
    n = 28

    def body(f):
        b = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)
        k.key("Spine", f, rot=(2, 4 * pk.wave(f, n, 0.0), 3 * pk.wave(f, n, 0.0)), loc=(0, 0, -0.02 * b))
        k.key("Chest", f, rot=(2, -5 * pk.wave(f, n, 0.0), -2 * pk.wave(f, n, 0.0)), loc=(0, 0, 0))
        k.key("Neck", f, rot=(0, 0, 0))
        k.key("Head", f, rot=(-2, 3 * pk.wave(f, n, 0.0), 0))
        k.key("Jaw", f, rot=(2, 0, 0))
        band(k, f, n, amp=10, lift=4, cycles=2)
        p = -12 + 2 * pk.wave(f, n, 0.0, 2)
        hold(k, f, p, 4, 16)
        arm(k, f, "L", pitch=-4 + 20 * pk.wave(f, n, 0.55), roll=10, elbow=24 + 8 * pk.wave(f, n, 0.7), hand=30)
        arm(k, f, "R", pitch=p, roll=4, elbow=16, hand=0)
    orig = k.solve_leg
    k.solve_leg = lambda leg, f, T, foot_z=0.0, toe=None: orig(leg, f, T, foot_z, toe=10.0 * min(1.0, max(0.0, T.z) / 0.1))
    try:
        stride = cm.biped_walk(k, n, 0.16, 0.10, body, legs=(("Leg_L", 0.0), ("Leg_R", 0.5)), duty=0.6)
    finally:
        del k.solve_leg
    k.bake_bezier_now()                                  # same grip as the guard, butt carried >= 0.02 off the floor
    t = max([k._grip_t] + [need(k, f, 0.02) for f in range(0, n + 1)])
    grip_slide(k, {f: t for f in range(0, n + 1)})
    k.finish()
    return stride


def roar(k):
    """TRIDENT THRUST: steps into a lunge stance and thrusts the trident forward at chest height twice, the left fist
    braced beside it, beak wide on each thrust, the war-band whipping; recovers."""
    import bpy
    from mathutils import Quaternion
    n = 60
    k.new_action("roar", n, False)
    # f, spine z, chest pitch, head pitch, jaw, right arm (pitch, roll, elbow), left arm (pitch, roll, elbow)
    P = [(0, 0.0, 0, 0, 2, (-8, 4, 12), (-4, 10, 22)),
         (10, -0.06, 2, 0, 4, (-6, 12, 40), (-30, 18, 70)),
         (16, -0.07, 10, -6, 34, (-46, 10, 18), (-58, 10, 40)),
         (22, -0.06, 2, 0, 6, (-8, 12, 40), (-32, 18, 70)),
         (28, -0.07, 12, -6, 36, (-48, 10, 16), (-60, 10, 40)),
         (36, -0.07, 12, -6, 34, (-48, 10, 16), (-60, 10, 40)),
         (46, -0.04, 2, 0, 4, (-10, 8, 30), (-20, 14, 40)),
         (60, 0.0, 0, 0, 2, (-8, 4, 12), (-4, 10, 22))]
    for f, z, ch, hd, jw, ra, la in P:
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(ch, 0, 0), loc=(0, 0, 0))
        k.key("Neck", f, rot=(0, 0, 0))
        k.key("Head", f, rot=(hd - ch * 0.6, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        arm(k, f, "R", pitch=ra[0], roll=ra[1], elbow=ra[2], hand=0)
        arm(k, f, "L", pitch=la[0], roll=la[1], elbow=la[2], hand=20)
        k.key("Trident", f, loc=(0, 0, 0))
    for f in range(0, n + 1, 2):
        band(k, f, n, amp=14, lift=2 + 10 * (12 <= f <= 40), cycles=3)
    k.bake_bezier_now()
    # trident: upright at rest, level and pointing forward (prongs first) during the thrusts
    up = Vector((0, 0, 1))
    fwd = Quaternion(up.rotation_difference(Vector((0, -1, 0.42)).normalized()))
    for f in (0, 4, 10, 16, 22, 28, 36, 46, 54, 60):
        Rf = _hand_q(k, f)
        w = 0.0 if f in (0, 60) else (0.5 if f in (4, 54) else 1.0)
        q = Quaternion((1, 0, 0, 0)).slerp(fwd, w)
        _key_q(k, "Trident", f, Rf.inverted() @ q)
    k.bake_bezier_now()
    sc = bpy.context.scene
    for f in range(0, n + 1):
        sc.frame_set(f)
        for leg in LEGS2:
            T = Vector((k.J[leg].x, k.J[leg].y, 0.0))
            if leg == "Leg_L":                                     # lunge step with the left foot
                if 2 <= f <= 10:
                    u = (f - 2) / 8
                    T = Vector((T.x, T.y - 0.16 * (0.5 - 0.5 * math.cos(math.pi * u)), 0.08 * math.sin(math.pi * u)))
                elif 10 < f < 48:
                    T = Vector((T.x, T.y - 0.16, 0.0))
                elif 48 <= f <= 56:
                    u = (f - 48) / 8
                    T = Vector((T.x, T.y - 0.16 * (0.5 + 0.5 * math.cos(math.pi * u)), 0.08 * math.sin(math.pi * u)))
            solve(k, leg, f, T)
    t0 = k._grip_t                                       # guard grip at both ends, slid back up for the thrusts
    grip_slide(k, {f: (_ramp(t0, 0.0, f / 8) if f <= 8 else _ramp(0.0, t0, (f - 48) / 12)) for f in range(0, n + 1)})
    k.finish(loop=False)


def twirl(k):
    """SIGNATURE - TIDE-SPRING TWIRL (Poseidon's spring strike): raises the trident overhead in both hands, tips it
    flat, spins it twice like a helicopter overhead (the left fist lets go and punches out on spin 2), catches it
    vertical, raises it high and DRIVES the butt into the ground with bent knees, then rises into a proud stance."""
    import bpy
    from mathutils import Quaternion
    n = 100
    k.new_action("act_twirl", n, False)
    for f, z, ch, hd, jw in ((0, 0, 0, 0, 2), (10, -0.03, 2, 0, 2), (16, 0.0, -4, 2, 2), (60, 0.0, -4, 2, 2),
                             (72, 0.01, -8, -16, 20), (80, 0.02, -8, -14, 8), (86, -0.12, 10, 4, 34), (92, -0.10, 8, 2, 10),
                             (100, 0, 0, 0, 2)):
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, z))
        k.key("Chest", f, rot=(ch, 0, 0), loc=(0, 0, 0))
        k.key("Neck", f, rot=(0, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
    UP = dict(pitch=-172, roll=10, elbow=0, hand=0)
    for f, a in ((0, GUARD_R), (8, dict(pitch=-40, roll=34, elbow=40, hand=0)), (12, dict(pitch=-110, roll=30, elbow=24,
                 hand=0)), (16, UP), (60, UP),
                 (66, dict(pitch=-166, roll=10, elbow=6, hand=0)), (72, dict(pitch=-150, roll=12, elbow=10, hand=0)),
                 (80, dict(pitch=-160, roll=12, elbow=4, hand=0)), (86, dict(pitch=-30, roll=6, elbow=20, hand=0)),
                 (92, dict(pitch=-24, roll=6, elbow=22, hand=0)), (100, GUARD_R)):
        arm(k, f, "R", **a)
    for f, p, ro, el, hd in ((0, -4, 10, 22, 30), (10, -60, 20, 70, 40), (16, -100, 40, 60, 40), (38, -100, 40, 60, 40),
                             (44, -20, 75, 10, 60), (58, -20, 75, 10, 60), (66, -10, 20, 40, 60), (80, -30, 16, 70, 60),
                             (86, -50, 30, 30, 60), (94, -20, 14, 40, 40), (100, -4, 10, 22, 30)):
        arm(k, f, "L", pitch=p, roll=ro, elbow=el, hand=hd)
    for f in range(0, n + 1, 2):
        spin = 16 <= f <= 60
        band(k, f, n, amp=10 if spin else 8, lift=2 if spin else 0, cycles=6)
    k.key("Trident", 0, rot=(GUARD_R["elbow"] - GUARD_R["pitch"], 0, -GUARD_R["roll"]), loc=(0, 0, 0))
    k.bake_bezier_now()
    sc = bpy.context.scene
    tb = k.arm.pose.bones["Trident"]
    R0 = k.arm.data.bones["Trident"].matrix_local.to_quaternion()

    def upright(f):
        return _hand_q(k, f).inverted()
    lean = Quaternion((0, 1, 0), math.radians(18))   # top leans in over the head, butt swings clear of the pauldron
    for f in (8, 12, 16):                            # stays (leaning) upright while the arm rises
        _key_q(k, "Trident", f, upright(f) @ lean if f > 8 else upright(f))
    Rh = _hand_q(k, 38)
    axis = Rh.inverted() @ Vector((0, 0, 1))
    flat = Vector((0, 0, 1)).rotation_difference(Rh.inverted() @ Vector((0, -1, 0)))
    sc.frame_set(38)
    gz = (k.arm.matrix_world @ tb.head).z           # spin plane clear above the crown (head top ~1.84)
    lift = R0.inverted() @ (Rh.inverted() @ Vector((0, 0, max(0.0, 1.98 - gz))))
    for f, l in ((0, Vector()), (16, Vector()), (22, lift), (60, lift), (66, Vector()), (n, Vector())):
        tb.location = l
        tb.keyframe_insert("location", frame=f, group="Trident")
    q16 = upright(16) @ lean
    if q16.dot(flat) < 0:
        flat = -flat
    _key_q(k, "Trident", 22, flat)                   # tipped flat over the head
    for f in range(23, 61):
        u = (f - 22) / 38
        deg = 720 * (0.5 - 0.5 * math.cos(math.pi * u))
        _key_q(k, "Trident", f, Quaternion(axis, math.radians(deg)) @ flat)
    prev = Quaternion(axis, math.radians(720)) @ flat
    for f in (66, 72, 80, 86, 92, 100):            # caught upright, raised high, driven down beside the body
        q = upright(f)
        if q.dot(prev) < 0:
            q = -q
        _key_q(k, "Trident", f, q)
        prev = q
    k.bake_bezier_now()
    for f in range(0, n + 1):
        sc.frame_set(f)
        for leg in LEGS2:
            T = Vector((k.J[leg].x, k.J[leg].y, 0.0))
            if leg == "Leg_L" and 78 <= f <= 86:                  # stomp with the strike
                T.z = 0.10 * math.sin(math.pi * (f - 78) / 8)
            solve(k, leg, f, T)
    k.bake_bezier_now()                                  # guard grip; the slam drives the butt onto the floor
    t0 = k._grip_t
    hit = {f: need(k, f) for f in range(86, 93)}
    sl = {f: t0 for f in range(0, 17)}
    sl.update({f: _ramp(t0, hit[86], (f - 66) / 20) for f in range(66, 86)})
    sl.update(hit)
    sl.update({f: _ramp(hit[92], t0, (f - 92) / 8) for f in range(93, n + 1)})
    grip_slide(k, sl)
    k.finish(loop=False)


def anim(k):
    idle(k)
    stride = walk(k)
    roar(k)
    twirl(k)
    return stride


HEAD_XF = []
