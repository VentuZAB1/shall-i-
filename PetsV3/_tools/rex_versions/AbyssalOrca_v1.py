# Abyssal Orca (Tide egg SECRET 1.5%, 2026-10-14) - FIERCE style "the deep sovereign": a killer whale from the abyss,
# built from tapered blocks under a Roblox stud skin, swimming through the air like our Kraken (MOTION Swim). The
# iconic black/white orca pattern (reads at 64 px), a huge blade dorsal fin split by glowing abyssal veins, a deep-sea
# ANGLER LURE (hero piece) curving over the head: a mint bioluminescent bulb inside a gold fang cage, rows of mint
# photophores down the flanks, fierce mint eyes under heavy brows, conical teeth, horizontal flukes.
# No glow (Studio VFX on the anchor bones Lure / Fin / Blow).
import math
from mathutils import Vector

DISPLAY = "Abyssal Orca"
MOTION = "Swim"
RIG = "fish"
HEIGHT = 9.0

# Blender colours (Roblox renders ~0.6x darker)
INK = (40, 44, 64)           # orca black (brightened)
INK_D = (24, 26, 40)         # fin blades, brows
WHITE = (238, 240, 246)      # eye patch, belly, flank sweep
GREY = (150, 160, 186)       # saddle patch
MINT = (64, 255, 196)        # accent: abyssal bioluminescence
MINT_D = (22, 150, 140)
MINT_HOT = (214, 255, 240)
GOLD = (255, 196, 50)        # lure cage (secret hero gold)
BLACK = (12, 12, 20)
TEETH = (240, 236, 222)
MOUTH = (110, 26, 44)
H_MODEL = 1.55
PITCH = round(0.042 * (H_MODEL / HEIGHT) / (1.498 / 8.0), 4)
Z0 = 0.64
LURE_TIP = (0, -1.38, Z0 + 0.42)


def model(k):
    import blockkit as bk
    B = bk.Blocks(k, seed=401, tier=5, plates=False)
    z = Z0
    # ---------------- body: one smooth torpedo (head -> chest -> rear), rounded; orca pattern
    B.seg((0, -0.78, z), (0, -0.06, z), 0.275, 0.275, INK, "Chest", top=(0.96, 0.96), rnd=0.6, ext=0.03)
    B.seg((0, -0.08, z), (0, 0.54, z + 0.01), 0.262, 0.262, INK, "Spine", top=(0.58, 0.58), rnd=0.6, ext=0.02)
    B.seg((0, -0.76, z + 0.0), (0, -1.22, z - 0.04), 0.255, 0.24, INK, "Head", top=(0.66, 0.62), rnd=0.6, ext=0.02)
    # white belly + chin: a broad pale keel visible in profile, sweeping up the flank behind the dorsal fin
    B.seg((0, -1.16, z - 0.20), (0, -0.80, z - 0.22), 0.15, 0.06, WHITE, "Jaw", side=(1, 0, 0), top=(1.0, 1.0),
          ext=0.02)
    B.seg((0, -0.80, z - 0.20), (0, 0.10, z - 0.20), 0.20, 0.08, WHITE, "Chest", side=(1, 0, 0), top=(0.8, 0.9),
          ext=0.02)
    B.seg((0, 0.10, z - 0.19), (0, 0.50, z - 0.12), 0.15, 0.06, WHITE, "Spine", side=(1, 0, 0), top=(0.6, 0.8))
    for s_ in (1, -1):                                                                          # flank sweep
        B.seg((s_ * 0.235, 0.10, z - 0.13), (s_ * 0.17, 0.46, z + 0.04), 0.03, 0.075, WHITE, "Spine",
              side=(1, 0, 0), top=(0.5, 0.35), studs=[])
        # big tilted eye patch above and behind the eye
        B.seg((s_ * 0.245, -0.98, z + 0.04), (s_ * 0.255, -0.80, z + 0.10), 0.03, 0.06, WHITE, "Head",
              side=(1, 0, 0), top=(0.8, 0.55), studs=[])
    B.add((0, 0.24, z + 0.245), (0.15, 0.17, 0.02), GREY, "Spine", top=(0.7, 0.8))                  # grey saddle
    for s_ in (1, -1):                                       # white lower flanks: chin -> throat -> belly (profile)
        B.seg((s_ * 0.17, -1.17, z - 0.115), (s_ * 0.215, -0.82, z - 0.14), 0.05, 0.07, WHITE, "Jaw", side=(1, 0, 0),
              top=(1.0, 1.0), rnd=0.5)
        B.seg((s_ * 0.215, -0.80, z - 0.15), (s_ * 0.225, 0.02, z - 0.17), 0.055, 0.085, WHITE, "Chest", side=(1, 0, 0),
              top=(0.9, 0.8), rnd=0.5)
    # fierce mint eyes just ahead of the patches under heavy brows
    for s_ in (1, -1):
        c = Vector((s_ * 0.235, -1.03, z + 0.02))
        B.add(c, (0.008, 0.05, 0.024), BLACK, "Head", rot=(0, 0, -s_ * 14), studs=[], role="detail", bevel=0.004)
        B.add(c + Vector((s_ * 0.006, -0.002, 0)), (0.006, 0.042, 0.012), MINT, "Head", rot=(0, 0, -s_ * 14),
              studs=[], role="detail", bevel=0.003)
        B.add(c + Vector((s_ * 0.009, -0.02, 0.002)), (0.004, 0.016, 0.006), MINT_HOT, "Head", rot=(0, 0, -s_ * 14),
              studs=[], role="detail", bevel=0.002)
        B.add(c + Vector((0, -0.005, 0.045)), (0.04, 0.075, 0.026), INK_D, "Head", rot=(10 * s_, 0, -s_ * 16),
              role="detail", bevel=0.01)
    # mouth: rest slightly open, dark inside, rows of conical teeth top + bottom
    B.add((0, -1.04, z - 0.135), (0.16, 0.15, 0.008), MOUTH, "Jaw", studs=[], role="detail", bevel=0.004)
    B.seg((0, -0.86, z - 0.09), (0, -1.20, z - 0.085), 0.18, 0.012, MOUTH, "Head", side=(1, 0, 0), studs=[],
          role="detail")
    for s_ in (1, -1):
        for i, y in enumerate((-1.18, -1.12, -1.06, -1.00, -0.94, -0.88)):
            x = s_ * (0.08 + 0.02 * i)
            B.spike((x, y, z - 0.085), (s_ * 0.1, 0, -1), 0.05, 0.016, TEETH, "Head")
            B.spike((x * 0.96, y, z - 0.145), (s_ * 0.1, 0, 1), 0.045, 0.015, TEETH, "Jaw")
    B.add((0, -0.90, z + 0.255), (0.03, 0.02, 0.008), BLACK, "Head", studs=[], role="detail", bevel=0.003)  # blowhole
    # ---------------- ANGLER LURE: black stalk curving forward over the head, gold fang cage, mint bulb
    P = [Vector((0, -0.84, z + 0.22)), Vector((0, -0.98, z + 0.42)), Vector((0, -1.18, z + 0.50)),
         Vector((0, -1.32, z + 0.46))]
    for i, (a, b) in enumerate(zip(P, P[1:])):
        B.seg(a, b, 0.034 - 0.006 * i, 0.034 - 0.006 * i, INK_D, "Lure", side=(1, 0, 0), ext=0.03, role="limb")
    bulb = Vector(LURE_TIP)
    B.add(bulb, (0.07, 0.07, 0.075), MINT_D, "Lure", rnd=0.6, studs=[], nostud=True, role="limb")
    B.add(bulb + Vector((0, -0.01, 0.005)), (0.055, 0.055, 0.06), MINT, "Lure", rnd=0.6, studs=[], nostud=True,
          role="limb")
    B.add(bulb + Vector((0, -0.045, 0.012)), (0.026, 0.02, 0.028), MINT_HOT, "Lure", rnd=0.6, studs=[], nostud=True,
          role="detail")
    for a in range(6):                                                             # gold fang cage around the bulb
        ang = math.radians(a * 60)
        d = Vector((math.cos(ang), 0, math.sin(ang)))
        base = bulb + d * 0.07 + Vector((0, 0.01, 0))
        B.spike(base, d * 0.4 + Vector((0, -1.0, 0)), 0.10, 0.016, GOLD, "Lure", top=(0.15, 0.15), nostud=True)
    B.add(bulb + Vector((0, 0.06, 0)), (0.045, 0.02, 0.045), GOLD, "Lure", rnd=0.4, studs=[], nostud=True,
          role="limb")                                                                         # cage collar
    # ---------------- photophores: mint lights in 2 rows down each flank + under the jaw
    for s in (1, -1):
        for i in range(7):
            y = -0.74 + i * 0.16
            zz = z - 0.05 - 0.03 * math.sin(i * 0.8)
            x = 0.265 - 0.025 * max(0, i - 3)
            B.add((s * x, y, zz), (0.006, 0.022, 0.022), MINT, "Chest" if y < -0.05 else "Spine", studs=[],
                  role="detail", bevel=0.006, nostud=True)
        for i in range(5):
            y = -0.60 + i * 0.18
            B.add((s * (0.24 - 0.02 * max(0, i - 2)), y, z - 0.15), (0.006, 0.016, 0.016), MINT_D,
                  "Chest" if y < -0.05 else "Spine", studs=[], role="detail", bevel=0.005, nostud=True)
    # ---------------- huge blade dorsal fin with abyssal veins (Fin bone, also a VFX anchor)
    D = [Vector((0, -0.10, z + 0.22)), Vector((0, 0.04, z + 0.95)), Vector((0, 0.16, z + 0.98)),
         Vector((0, 0.30, z + 0.20))]
    B.poly(D, 0.07, INK_D, "Dorsal")
    for (a, b) in ((D[0].lerp(D[3], 0.3), D[1].lerp(D[2], 0.4)), (D[0].lerp(D[3], 0.65), D[1].lerp(D[2], 0.85))):
        for sx in (1, -1):
            m = a.lerp(b, 0.5) + Vector((0.035 * sx, 0.03, 0))
            B.seg(a + Vector((0.037 * sx, 0, 0)), m, 0.006, 0.014, MINT, "Dorsal", side=(1, 0, 0), studs=[], nostud=True,
                  role="detail")
            B.seg(m, b + Vector((0.037 * sx, 0, 0)), 0.006, 0.012, MINT, "Dorsal", side=(1, 0, 0), studs=[],
                  nostud=True, role="detail", top=(1, 0.2))
    for t in (0.25, 0.55, 0.85):                                                # jagged trailing-edge teeth
        p = D[2].lerp(D[3], t)
        B.spike(p, (0, 1, -0.2), 0.08, 0.03, INK_D, "Dorsal", side=(1, 0, 0), top=(0.15, 0.4))
    # ---------------- pectoral paddles (black), tail stock + horizontal flukes
    for s, side in ((1, "L"), (-1, "R")):
        r0 = Vector((s * 0.22, -0.56, z - 0.16))
        B.poly([r0, Vector((s * 0.58, -0.40, z - 0.40)), Vector((s * 0.62, -0.26, z - 0.42)),
                Vector((s * 0.26, -0.36, z - 0.18))], 0.05, INK, "Fin_" + side)
        B.seg(r0, Vector((s * 0.58, -0.40, z - 0.40)), 0.022, 0.025, MINT_D, "Fin_" + side, side=(0, 0, 1), studs=[],
              nostud=True, role="limb", top=(0.5, 0.5))
    B.seg((0, 0.50, z), (0, 0.92, z + 0.03), 0.15, 0.14, INK, "Tail1", top=(0.6, 0.6), ext=0.08, rnd=0.5)
    B.seg((0, 0.92, z + 0.03), (0, 1.22, z + 0.05), 0.09, 0.08, INK, "Tail2", top=(0.6, 0.6), ext=0.04, rnd=0.5)
    B.seg((0, 0.52, z - 0.10), (0, 0.88, z - 0.05), 0.09, 0.03, WHITE, "Tail1", side=(1, 0, 0), top=(0.5, 1))
    for s in (1, -1):
        root = Vector((0, 1.20, z + 0.05))
        B.poly([root + Vector((s * 0.02, -0.04, 0)), Vector((s * 0.46, 1.40, z + 0.08)),
                Vector((s * 0.40, 1.52, z + 0.06)), Vector((s * 0.06, 1.40, z + 0.05))], 0.05, INK, "Tail3")
        B.seg(Vector((s * 0.08, 1.38, z + 0.06)), Vector((s * 0.43, 1.50, z + 0.07)), 0.012, 0.02, MINT,
              "Tail3", side=(0, 0, 1), studs=[], nostud=True, role="detail")                    # fluke edge light
    B.build()
    bk.stud_skin(k, PITCH)
    return {"TH": round(B.th, 3), "PITCH": PITCH}


# ------------------------------------------------------------------ rig
def rig(k):
    z = Z0
    k.joint("Spine", (0, 0.10, z), "Root", tail=(0, -0.4, 0))
    k.joint("Chest", (0, -0.30, z), "Spine", tail=(0, -0.4, 0))
    k.joint("Head", (0, -0.78, z), "Chest", tail=(0, -0.3, 0))
    k.joint("Jaw", (0, -0.84, z - 0.10), "Head", tail=(0, -0.25, 0))
    k.joint("Lure", (0, -0.84, z + 0.22), "Head", tail=(0, -0.1, 0.2))
    k.joint("Dorsal", (0, 0.08, z + 0.22), "Spine", tail=(0, 0.05, 0.3))
    for s, side in ((1, "L"), (-1, "R")):
        k.joint("Fin_" + side, (s * 0.22, -0.52, z - 0.16), "Chest", tail=(s * 0.3, 0.1, -0.2))
    k.joint("Tail1", (0, 0.52, z), "Spine", tail=(0, 0.4, 0.02))
    k.joint("Tail2", (0, 0.92, z + 0.03), "Tail1", tail=(0, 0.3, 0.02))
    k.joint("Tail3", (0, 1.20, z + 0.05), "Tail2", tail=(0, 0.3, 0.0))
    k.joint("Blow", (0, -0.92, z + 0.24), "Head", tail=(0, 0, 0.2))                 # VFX anchor (spout)


def check_pairs():
    return [("Head", "Fin_L"), ("Head", "Fin_R"), ("Jaw", "Fin_L"), ("Jaw", "Fin_R"), ("Lure", "Chest"),
            ("Lure", "Dorsal"), ("Tail3", "Spine"), ("Tail3", "Chest"), ("Tail2", "Chest"), ("Fin_L", "Spine"),
            ("Fin_R", "Spine")]


HEAD_XF = []
