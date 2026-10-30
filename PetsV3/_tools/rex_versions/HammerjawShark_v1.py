# Hammerjaw Shark (Tide egg, NEW 5.5% pet, 2026-10-14) - FIERCE style "the reef breaker": an armoured hammerhead
# built from tapered blocks under a Roblox stud skin, swimming through the air like our Kraken (MOTION Swim): a wide
# hammer head (cephalofoil) capped with a dark armour plate, narrow coral-orange eyes at the hammer tips, a deep jaw
# with rows of white teeth, a steel-blue back over a white countershaded belly, 5 coral gill slashes per side, a tall
# swept dorsal fin, long pectorals, a crescent tail fin; coral fin edges. No glow (Studio VFX: bubbles / water trail).
import math
from mathutils import Vector

DISPLAY = "Hammerjaw Shark"
MOTION = "Swim"
RIG = "fish"
HEIGHT = 7.0

# Blender colours (Roblox renders ~0.6x darker)
STEEL = (78, 118, 170)       # back + flanks
STEEL_D = (44, 64, 102)      # dorsal saddle, hammer armour, fin roots
BELLY = (232, 236, 244)      # countershaded underside
BELLY_D = (196, 204, 222)
CORAL = (255, 116, 52)       # accent: gill slashes, fin edges, eyes
CORAL_HOT = (255, 214, 160)
BLACK = (14, 14, 22)
TEETH = (240, 236, 222)
MOUTH = (110, 24, 34)
H_MODEL = 1.20
PITCH = round(0.042 * (H_MODEL / HEIGHT) / (1.498 / 8.0), 4)
Z0 = 0.62                    # body axis height (it hovers)


def model(k):
    import blockkit as bk
    B = bk.Blocks(k, seed=307, tier=3, plates=False)
    z = Z0
    # ---------------- body: deep front body, tapering mid body, countershaded belly
    B.add((0, -0.50, z), (0.225, 0.34, 0.235), STEEL, "Chest", bot=(0.58, 0.78), top=(0.80, 0.86), rnd=0.50)
    B.add((0, 0.06, z + 0.005), (0.18, 0.28, 0.195), STEEL, "Spine", bot=(0.58, 0.78), top=(0.78, 0.86), rnd=0.50)
    # HAMMERJAW war-plates: dark armour shells along the back, coral seams between them, jagged rear edges
    for y, hy, hx, zt, bone in ((-0.70, 0.12, 0.17, 0.205, "Chest"), (-0.44, 0.12, 0.18, 0.21, "Chest"),
                                (-0.18, 0.11, 0.165, 0.19, "Chest"), (0.08, 0.11, 0.145, 0.17, "Spine"),
                                (0.30, 0.09, 0.12, 0.14, "Spine")):
        B.add((0, y, z + zt - 0.035), (hx, hy, 0.065), STEEL_D, bone, top=(0.62, 0.9), bot=(1.0, 1.0), rnd=0.45)
        for sx in (1, -1):
            B.spike((sx * hx * 0.8, y + hy * 0.6, z + zt - 0.07), (sx * 0.5, 0.6, -0.45), 0.09, 0.028, STEEL_D, bone,
                    top=(0.15, 0.4))
    for y, w, zt, bone in ((-0.575, 0.15, 0.215, "Chest"), (-0.31, 0.15, 0.205, "Chest"), (-0.05, 0.13, 0.18, "Spine"),
                           (0.195, 0.11, 0.155, "Spine")):
        B.bar((-w, y, z + zt), (w, y, z + zt), Vector((0, 0, 1)), 0.03, 0.012, CORAL, bone, studs=[], bevel=0.004,
              nostud=True)
    # battle scars on the flanks (reef breaker)
    for s_ in (1, -1):
        for (y0, z0), (y1, z1) in (((-0.40, z + 0.10), (-0.28, z - 0.02)), ((-0.36, z + 0.12), (-0.22, z + 0.0)),
                                   ((0.0, z + 0.08), (0.12, z - 0.03))):
            B.bar((s_ * 0.218, y0, z0), (s_ * 0.218, y1, z1), Vector((s_, 0, 0)), 0.018, 0.01, BELLY_D,
                  "Chest" if y0 < -0.1 else "Spine", studs=[], bevel=0.003, nostud=True)
    B.seg((0, -0.78, z - 0.17), (0, -0.16, z - 0.19), 0.15, 0.04, BELLY, "Chest", side=(1, 0, 0), top=(0.8, 0.9),
          ext=0.02)
    B.seg((0, -0.16, z - 0.16), (0, 0.32, z - 0.12), 0.12, 0.035, BELLY, "Spine", side=(1, 0, 0), top=(0.7, 0.9),
          ext=0.03)
    for s in (1, -1):                                                  # pale lower flank band
        B.seg((s * 0.155, -0.74, z - 0.10), (s * 0.13, -0.18, z - 0.11), 0.02, 0.07, BELLY, "Chest", side=(1, 0, 0),
              studs=[], ext=0.0)
    # 5 coral gill slashes per side (curved, smooth)
    for s in (1, -1):
        for i in range(5):
            y = -0.70 + i * 0.055
            a = Vector((s * 0.215, y, z + 0.08))
            b = Vector((s * 0.205, y + 0.025, z - 0.08))
            B.bar(a, b, Vector((s, 0, 0)), 0.024, 0.012, CORAL, "Chest", studs=[], bevel=0.004, nostud=True)
    # ---------------- hammer head (Head bone): flat wide cephalofoil, armour cap, eyes at the tips, snout + jaw
    B.add((0, -0.92, z + 0.05), (0.16, 0.14, 0.12), STEEL, "Head", top=(0.8, 0.85), rnd=0.35)          # head core
    ham = B.add((0, -1.00, z + 0.10), (0.40, 0.11, 0.055), STEEL, "Head", top=(0.92, 0.85), rnd=0.35)  # hammer
    B.add((0, -0.99, z + 0.165), (0.34, 0.09, 0.02), STEEL_D, "Head", top=(0.92, 0.8))              # armour cap
    for x in (-0.24, -0.12, 0.0, 0.12, 0.24):                                                          # cap ridges
        B.spike((x, -1.02, z + 0.18), (0, 0.4, 1), 0.06, 0.028, STEEL_D, "Head", top=(0.2, 0.4))
    B.add((0, -1.11, z + 0.08), (0.36, 0.012, 0.04), STEEL_D, "Head", top=(0.9, 0.9), studs=[])      # leading edge
    for s in (1, -1):
        tip = Vector((s * 0.40, -1.00, z + 0.10))
        B.add(tip + Vector((s * 0.01, 0, 0)), (0.04, 0.09, 0.06), STEEL_D, "Head", rnd=0.45)            # tip lobe
        # narrow coral eye on the outer face of the hammer tip, under a heavy ridge
        B.add(tip + Vector((s * 0.052, -0.01, 0.0)), (0.008, 0.055, 0.022), BLACK, "Head", studs=[], role="detail",
              rot=(14 * s, 0, 0), bevel=0.004)
        B.add(tip + Vector((s * 0.058, -0.012, 0.0)), (0.006, 0.046, 0.012), CORAL, "Head", studs=[], role="detail",
              rot=(14 * s, 0, 0), bevel=0.003)
        B.add(tip + Vector((s * 0.062, -0.03, 0.002)), (0.004, 0.018, 0.006), CORAL_HOT, "Head", studs=[],
              role="detail", rot=(14 * s, 0, 0), bevel=0.002)
        B.add(tip + Vector((s * 0.045, -0.01, 0.045)), (0.03, 0.07, 0.022), STEEL_D, "Head", rot=(10 * s, 0, 0),
              role="detail", bevel=0.01)                                                                 # brow ridge
    for s in (1, -1):                                                                                     # nostrils
        B.add((s * 0.22, -1.115, z + 0.07), (0.035, 0.006, 0.008), BLACK, "Head", studs=[], role="detail",
              bevel=0.003)
    # mouth under the hammer: upper jaw edge with teeth, dark mouth, lower jaw (opens) with teeth
    B.seg((0, -0.80, z - 0.06), (0, -1.02, z - 0.04), 0.14, 0.04, BELLY, "Head", side=(1, 0, 0), top=(0.8, 1))
    B.add((0, -0.93, z - 0.11), (0.12, 0.08, 0.008), MOUTH, "Jaw", studs=[], role="detail", bevel=0.004)
    B.seg((0, -0.78, z - 0.155), (0, -0.99, z - 0.145), 0.13, 0.035, BELLY, "Jaw", side=(1, 0, 0), top=(0.8, 1),
          ext=0.02)
    B.seg((0, -0.80, z - 0.19), (0, -0.98, z - 0.18), 0.11, 0.02, STEEL_D, "Jaw", side=(1, 0, 0), top=(0.8, 1))  # jaw plate
    for s in (1, -1):
        for i, y in enumerate((-0.98, -0.94, -0.90, -0.86, -0.82)):
            x = s * (0.05 + 0.02 * i)
            B.spike((x, y, z - 0.085), (s * 0.1, 0, -1), 0.045 - 0.004 * i, 0.013, TEETH, "Head")
            B.spike((x * 0.95, y, z - 0.118), (s * 0.1, 0, 1), 0.035 - 0.003 * i, 0.012, TEETH, "Jaw")
        B.spike((s * 0.02, -1.0, z - 0.085), (0, -0.2, -1), 0.05, 0.014, TEETH, "Head")
    # ---------------- fins: tall swept dorsal with coral edge, long pectorals, pelvics, 2nd dorsal, anal
    dors = [Vector((0, -0.30, z + 0.20)), Vector((0, -0.12, z + 0.62)), Vector((0, 0.02, z + 0.60)),
            Vector((0, 0.08, z + 0.17))]
    B.poly(dors, 0.05, STEEL, "Spine")
    B.seg(dors[0].lerp(dors[1], 0.05), dors[1], 0.028, 0.03, CORAL, "Spine", side=(1, 0, 0), studs=[], nostud=True,
          role="limb", top=(0.5, 0.5))                                                              # leading edge
    B.seg(dors[1], dors[2], 0.03, 0.03, CORAL, "Spine", side=(1, 0, 0), studs=[], nostud=True, role="limb")
    for s, side in ((1, "L"), (-1, "R")):
        root = Vector((s * 0.17, -0.50, z - 0.12))
        tipp = Vector((s * 0.66, -0.26, z - 0.36))
        back = Vector((s * 0.20, -0.22, z - 0.14))
        B.poly([root, tipp, back], 0.045, STEEL, "Fin_" + side)
        B.seg(root, tipp, 0.025, 0.03, CORAL, "Fin_" + side, side=(0, 0, 1), studs=[], nostud=True, role="limb",
              top=(0.5, 0.5))
        B.poly([Vector((s * 0.10, 0.22, z - 0.12)), Vector((s * 0.26, 0.40, z - 0.26)),
                Vector((s * 0.10, 0.38, z - 0.12))], 0.035, STEEL, "Spine")                           # pelvic fin
    B.poly([Vector((0, 0.48, z + 0.10)), Vector((0, 0.60, z + 0.26)), Vector((0, 0.66, z + 0.08))], 0.035, STEEL_D,
           "Tail1")                                                                                  # 2nd dorsal
    B.poly([Vector((0, 0.50, z - 0.09)), Vector((0, 0.64, z - 0.22)), Vector((0, 0.68, z - 0.07))], 0.035, STEEL_D,
           "Tail1")                                                                                  # anal fin
    # ---------------- tail: 2 tapering segments + crescent caudal fin (upper lobe longer) with coral edges
    B.seg((0, 0.30, z + 0.005), (0, 0.70, z + 0.02), 0.13, 0.13, STEEL, "Tail1", top=(0.62, 0.62), ext=0.06, rnd=0.4)
    B.seg((0, 0.70, z + 0.02), (0, 1.02, z + 0.04), 0.08, 0.08, STEEL, "Tail2", top=(0.6, 0.6), ext=0.04, rnd=0.4)
    B.seg((0, 0.30, z - 0.08), (0, 0.66, z - 0.04), 0.08, 0.025, BELLY, "Tail1", side=(1, 0, 0), top=(0.6, 1))
    root = Vector((0, 1.02, z + 0.04))
    up_t, lo_t = Vector((0, 1.38, z + 0.50)), Vector((0, 1.26, z - 0.26))
    B.poly([root + Vector((0, -0.03, 0.02)), up_t, Vector((0, 1.18, z + 0.08)), lo_t,
            root + Vector((0, -0.03, -0.03))], 0.05, STEEL, "Tail3")
    for a, b in ((root, up_t), (root, lo_t)):
        B.seg(a, b, 0.028, 0.03, CORAL, "Tail3", side=(1, 0, 0), studs=[], nostud=True, role="limb", top=(0.5, 0.5))
    B.build()
    bk.stud_skin(k, PITCH)
    return {"TH": round(B.th, 3), "PITCH": PITCH}


# ------------------------------------------------------------------ rig
def rig(k):
    z = Z0
    k.joint("Spine", (0, 0.05, z), "Root", tail=(0, -0.4, 0))
    k.joint("Chest", (0, -0.22, z), "Spine", tail=(0, -0.4, 0))
    k.joint("Head", (0, -0.80, z + 0.02), "Chest", tail=(0, -0.3, 0))
    k.joint("Jaw", (0, -0.80, z - 0.11), "Head", tail=(0, -0.2, 0))
    for s, side in ((1, "L"), (-1, "R")):
        k.joint("Fin_" + side, (s * 0.17, -0.48, z - 0.12), "Chest", tail=(s * 0.3, 0.15, -0.1))
    k.joint("Tail1", (0, 0.32, z), "Spine", tail=(0, 0.38, 0.02))
    k.joint("Tail2", (0, 0.70, z + 0.02), "Tail1", tail=(0, 0.32, 0.02))
    k.joint("Tail3", (0, 1.00, z + 0.04), "Tail2", tail=(0, 0.3, 0.05))


def check_pairs():
    return [("Head", "Fin_L"), ("Head", "Fin_R"), ("Jaw", "Fin_L"), ("Jaw", "Fin_R"), ("Tail3", "Spine"),
            ("Tail3", "Chest"), ("Tail2", "Chest"), ("Fin_L", "Spine"), ("Fin_R", "Spine")]


HEAD_XF = []
