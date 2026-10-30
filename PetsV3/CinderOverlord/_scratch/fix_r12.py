# Cinder Overlord final-8.5 round 12 (_review/CinderOverlord_final85_r12.md + coordinator: OWNER -> COBRA HOOD)
import io
p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\CinderOverlord.py"
s = io.open(p, encoding="utf-8").read()
n_ok = 0


def rep(a, b):
    global s
    global n_ok
    c = s.count(a)
    assert c == 1, (c, a[:100])
    s = s.replace(a, b)
    n_ok += 1


HOOD_CODE = '''
# ---- r12 MUST 1 (owner: COBRA HOOD): two flat, studded hood panels per side on Neck2 (lower) and Neck3 (upper) - thin
# lofted shells (NOT a neck-radius scale), ember front / back with studs on the back, an obsidian rim, two obsidian
# ribs and a sulfur-blue eye spot per side on the back. The panels sit just behind the neck axis and cup forward at the
# rim (a fan from behind); they reach |x| 0.47 (neck side 0.21, skull side 0.37), widest just below the head.
HOOD_BACK, HOOD_CUP, HOOD_STACK, HOOD_T = 0.07, 0.10, 0.028, 0.026   # behind the axis, rim forward, upper behind, thick
HOOD_ROOT = 0.10                                                     # inner edge (buried in the neck)
HOOD_PANELS = (                       # bone, (z, outer |x|) outline from bottom to top
    ("Neck2", ((0.98, 0.17), (1.04, 0.24), (1.10, 0.31), (1.17, 0.38), (1.24, 0.42), (1.31, 0.45))),
    ("Neck3", ((1.27, 0.45), (1.32, 0.465), (1.36, 0.47), (1.41, 0.455), (1.46, 0.43), (1.50, 0.38), (1.53, 0.32),
               (1.57, 0.16))))
HOOD_RIBS = (("Neck2", 0.17, 1.12, 0.39, 1.21), ("Neck3", 0.18, 1.31, 0.44, 1.345), ("Neck3", 0.18, 1.45, 0.38, 1.495))
HOOD_SPOT = ("Neck3", 0.295, 1.395, 0.052, 0.036)                    # bone, |x|, z, half width, half height


def hood_axis_y(z):
    """y of the neck axis at height z (FRONT[3] -> FRONT[4] -> FRONT[5])"""
    for a, b in ((FRONT[3], FRONT[4]), (FRONT[4], FRONT[5])):
        if z <= b.z:
            u = (z - a.z) / (b.z - a.z)
            return a.y + (b.y - a.y) * u
    return FRONT[5].y


def hood_pt(sx, x, z, stack):
    return Vector((sx * x, hood_axis_y(z) + HOOD_BACK + stack - HOOD_CUP * (x - HOOD_ROOT) / 0.37, z))


def hood_n(sx, z, stack):
    """outward (back-facing, +y) normal of a panel"""
    dx = hood_pt(sx, 0.40, z, stack) - hood_pt(sx, 0.20, z, stack)
    dz = hood_pt(sx, 0.30, z + 0.05, stack) - hood_pt(sx, 0.30, z - 0.05, stack)
    n = dx.cross(dz).normalized()
    return n if n.y > 0 else -n


def cobra_hood(B):
    for sx in (1, -1):
        for pi, (bone, outline) in enumerate(HOOD_PANELS):
            stack = HOOD_STACK if pi == 1 else 0.0
            rings = []
            for z, xo in outline:
                n = hood_n(sx, z, stack)
                xs = [HOOD_ROOT + (xo - HOOD_ROOT) * i / 5.0 for i in range(6)]
                pts = [hood_pt(sx, x, z, stack) for x in xs]
                rings.append(([q + n * HOOD_T / 2 for q in pts], [q - n * HOOD_T / 2 for q in pts]))
            B.tube(rings, PLUM_OBS, bone, closed=False, nostud=False)          # studded ember panel
            rim = [hood_pt(sx, xo, z, stack) for z, xo in outline if xo >= 0.20]
            for a, b in zip(rim, rim[1:]):                                     # obsidian rim
                n = hood_n(sx, (a.z + b.z) / 2, stack)
                dv = (b - a).normalized()
                B.seg(a, b, 0.018, HOOD_T / 2 + 0.008, OBS_D, bone, side=n.cross(dv), ext=0.012, ext1=0.012,
                      studs=[], nostud=True, role="limb", rnd=0.3)
        for bone, x0, z0, x1, z1 in HOOD_RIBS:                                # obsidian ribs on the back
            stack = HOOD_STACK if bone == "Neck3" else 0.0
            n = hood_n(sx, (z0 + z1) / 2, stack)
            a = hood_pt(sx, x0, z0, stack) + n * (HOOD_T / 2 + 0.004)
            b = hood_pt(sx, x1, z1, stack) + n * (HOOD_T / 2 + 0.004)
            B.bar(a, b, n, 0.026, 0.012, OBS_D, bone, studs=[], nostud=True, role="detail", bevel=0.004)
        bone, x, z, hw, hh = HOOD_SPOT                                         # sulfur-blue eye spot (cobra marking)
        n = hood_n(sx, z, HOOD_STACK)
        c = hood_pt(sx, x, z, HOOD_STACK) + n * (HOOD_T / 2 + 0.005)
        B.add(c, (hw, 0.006, hh), ROSE, bone, R=face_R(n), studs=[], role="detail", bevel=0.004, top=(0.8, 0.8))
        B.add(c + n * 0.007, (hw * 0.42, 0.004, hh * 0.42), LAVA, bone, R=face_R(n), studs=[], role="detail",
              bevel=0.003)


def model(k):'''
rep("""
def model(k):""", HOOD_CODE)
rep("""    # ================= rose lava vents: 6 pairs along the flanks, double slits in the plum gap before each ring""",
    """    cobra_hood(B)                                                  # r12 MUST 1: the cobra hood (Neck2 / Neck3)
    # ================= rose lava vents: 6 pairs along the flanks, double slits in the plum gap before each ring""")
# MUST 2: snout stations 0.82 / 0.96 lower (0.082 -> 0.066, 0.040 -> 0.028)
rep("""(0.62, 0.150, 0.112, -0.014), (0.82, 0.112, 0.082, -0.026), (0.96, 0.060, 0.040, -0.034),""",
    """(0.62, 0.150, 0.112, -0.014), (0.82, 0.112, 0.066, -0.026), (0.96, 0.060, 0.028, -0.034),   # r12 MUST 2: 0.082 / 0.040 -> 0.066 / 0.028""")
io.open(p, "w", encoding="utf-8").write(s)
print("patched", n_ok)
