# Thunder Rex v2 -> v3: review 2 fixes 1-5 + animation-safety A-E + pose limits (PetsV3/_review/ThunderRex_review2.md)
import re
p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\ThunderRex.py"
s = open(p, encoding="utf-8").read()
R = []

def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:90])
    s = s.replace(a, b)

# shard() returns its HOT tip end (VFX anchors)
rep("""    B.add(p4 + d * tipL / 2, (w * 0.30, w * 0.66, tipL / 2), HOT, bone, R=bk.frame_from(p4, p4 + d, side),
          top=(0.12, 0.10), studs=[], nostud=True, role="limb")
""", """    B.add(p4 + d * tipL / 2, (w * 0.30, w * 0.66, tipL / 2), HOT, bone, R=bk.frame_from(p4, p4 + d, side),
          top=(0.12, 0.10), studs=[], nostud=True, role="limb")
    return p4 + d * tipL
""")
rep("""CORE = (0, -0.50, 1.08)      # filled in by model(): chest core centre (VFX anchor)""",
    """CORE = (0, -0.50, 1.08)      # filled in by model(): chest core centre (VFX anchor)
RIDGE_TIPS = [(0, -0.30, 1.75), (0, -0.05, 1.70), (0, 0.10, 1.60)]   # filled in by model(): big shard tips""")
rep("""    global CORE
""", """    global CORE, RIDGE_TIPS
""")
# FIX 4 belly strip deeper + lower, gap bars follow
rep("""    B.seg((0, -0.36, 0.875), (0, 0.32, 0.81), 0.17, 0.03, BELLY, "Chest", side=(1, 0, 0), top=(0.75, 0.9),
          ext=0.03)
    for t, w in ((0.12, 0.15), (0.36, 0.15), (0.60, 0.13), (0.84, 0.11)):
        p = Vector((0, -0.36, 0.842)).lerp(Vector((0, 0.32, 0.777)), t)""",
    """    B.seg((0, -0.36, 0.85), (0, 0.32, 0.785), 0.17, 0.05, BELLY, "Chest", side=(1, 0, 0), top=(0.75, 0.9),
          ext=0.03)
    for t, w in ((0.12, 0.15), (0.36, 0.15), (0.60, 0.13), (0.84, 0.11)):
        p = Vector((0, -0.36, 0.797)).lerp(Vector((0, 0.32, 0.737)), t)""")
# FIX 5 keel lower + smaller, core lower (fully under the jaw)
rep("""    kp, kn = fpt(rib, 0, -0.13, off=0.0)
    keel = B.add(kp + kn * 0.01, (0.013, 0.13, 0.11), BELLY""", """    kp, kn = fpt(rib, 0, -0.19, off=0.0)
    keel = B.add(kp + kn * 0.01, (0.013, 0.13, 0.09), BELLY""")
rep("""    for v in (-0.06, 0.02):
        B.add(keel.world((0.014, 0, v)), (0.004, 0.12 * (0.8 + 0.2 * (v + 0.11) / 0.22), 0.008), BELLY_D, "Chest",""",
    """    for v in (-0.045, 0.025):
        B.add(keel.world((0.014, 0, v)), (0.004, 0.12 * (0.8 + 0.2 * (v + 0.09) / 0.18), 0.008), BELLY_D, "Chest",""")
rep("""    cp, cn = fpt(rib, 0, 0.0, off=0.03)""", """    cp, cn = fpt(rib, 0, -0.07, off=0.03)""")
# FIX 2 torso shells lower (storm-black top), 3 jagged teeth per side, seams + cracks follow
rep("""    for b, y0, y1, za, lift in ((rib, -0.31, -0.085, 0.02, 0.02), (rib, -0.035, 0.31, 0.0, 0.0),
                                (hips, -0.10, 0.25, 0.02, 0.0)):
        sh = shell(B, b, y0, y1, za, ARMOR, rnd=0.42, lift=lift)
        shells.append(sh)
        for s in (1, -1):
            for i, ly in enumerate((y0 * 0.55 + y1 * 0.45, y0 * 0.15 + y1 * 0.85)):
                p0, nrm = side_pt(b, s, ly, za + 0.03, off=0.030)
                p1 = p0 + Vector((0, 0.015, -0.10 if i % 2 == 0 else -0.075))
                B.add((p0 + p1) / 2, (0.014, 0.045, (p1 - p0).length / 2), ARMOR, b.bone,
                      R=bk.frame_from(p0, p1, nrm), top=(1, 0.10), role="detail", bevel=0.006)
    for b, y0, y1, za in ((rib, -0.085, -0.035, 0.0), (hips, -0.15, -0.10, 0.02)):
        shell(B, b, y0, y1, za - 0.02, CYAN, pad=0.012, rnd=0.30, studs=[], nostud=True)       # seam bands
    for s in (1, -1):
        crack(B, rib, s, ((-0.06, 0.0), (-0.02, -0.08), (-0.08, -0.13), (-0.03, -0.20)))
        crack(B, rib, s, ((-0.31 + 0.02, 0.02), (-0.24, -0.06), (-0.27, -0.12)), w=0.03)
        crack(B, hips, s, ((-0.125, 0.02), (-0.08, -0.06), (-0.12, -0.12), (-0.07, -0.18)))""",
    """    for b, y0, y1, za, lift in ((rib, -0.31, -0.085, -0.07, 0.02), (rib, -0.035, 0.31, -0.09, 0.0),
                                (hips, -0.10, 0.25, -0.06, 0.0)):
        sh = shell(B, b, y0, y1, za, ARMOR, rnd=0.42, lift=lift)
        shells.append(sh)
        for s in (1, -1):
            for t, L in ((0.2, 0.10), (0.5, 0.07), (0.8, 0.09)):
                ly = y0 + (y1 - y0) * t
                p0, nrm = side_pt(b, s, ly, za + 0.03, off=0.030)
                p1 = p0 + Vector((0, 0.015, -L))
                B.add((p0 + p1) / 2, (0.014, 0.05, (p1 - p0).length / 2), ARMOR, b.bone,
                      R=bk.frame_from(p0, p1, nrm), top=(1, 0.10), role="detail", bevel=0.006)
    for b, y0, y1, za in ((rib, -0.085, -0.035, -0.09), (hips, -0.15, -0.10, -0.06)):
        shell(B, b, y0, y1, za - 0.02, CYAN, pad=0.012, rnd=0.30, studs=[], nostud=True)       # seam bands
    for s in (1, -1):
        crack(B, rib, s, ((-0.06, -0.10), (-0.02, -0.16), (-0.08, -0.20), (-0.03, -0.25)))
        crack(B, rib, s, ((-0.29, -0.08), (-0.24, -0.14), (-0.27, -0.19)), w=0.03)
        crack(B, hips, s, ((-0.125, -0.07), (-0.08, -0.12), (-0.12, -0.17), (-0.07, -0.21)))""")
# FIX 2 skull cap
rep("""    B.add((0, -0.78, 1.73), (0.15, 0.15, 0.03), ARMOR, "Head", top=(0.75, 0.8))                         # skull cap""",
    """    B.add((0, -0.78, 1.715), (0.165, 0.165, 0.05), ARMOR, "Head", top=(0.75, 0.8))                      # skull cap""")
# polish: narrower nasal plate
rep("""    B.seg((0, -0.95, 1.585), (0, -1.29, 1.50), 0.065, 0.02, ARMOR""", """    B.seg((0, -0.95, 1.585), (0, -1.29, 1.50), 0.045, 0.02, ARMOR""")
# E: upper fangs outside the lower jaw walls, front lower tooth in
rep("""            B.spike((s * 0.112, y, z), (s * dx, dy, -1), L, w, TEETH, "Head")""",
    """            B.spike((s * 0.13, y, z), (s * dx, dy, -1), L, w, TEETH, "Head")""")
rep("""            B.spike((s * 0.098, y, z), (s * dx, -0.08, 1), L, 0.014, TEETH, "Jaw")""",
    """            B.spike((s * (0.085 if y < -1.24 else 0.098), y, z), (s * dx, -0.08, 1), L, 0.014, TEETH, "Jaw")""")
# C: mouth roof + cyan throat (no blue studs inside an open mouth)
rep("""    B.seg((0, -0.86, 1.39), (0, -1.24, 1.293), 0.10, 0.02, MOUTH, "Jaw", studs=[], role="detail", bevel=0.004)""",
    """    B.seg((0, -0.86, 1.39), (0, -1.24, 1.293), 0.10, 0.02, MOUTH, "Jaw", studs=[], role="detail", bevel=0.004)
    B.seg((0, -0.94, 1.385), (0, -1.24, 1.31), 0.10, 0.012, MOUTH, "Head", studs=[], role="detail", bevel=0.004)
    B.add((0, -0.86, 1.36), (0.06, 0.02, 0.04), CYAN, "Head", studs=[], nostud=True, role="detail", bevel=0.006)""")
# B: jaw-hinge horn tips re-aimed (clear the first side shards on head yaw)
rep("""Vector((s * 0.35, -0.48, 1.58))]""", """Vector((s * 0.37, -0.56, 1.55))]""")
# FIX 1: GOLD crown - bigger band, gold prongs (taller), closed circlet (side bars + back plate + gem)
rep("""    B.add((0, -0.935, 1.735), (0.155, 0.05, 0.03), GOLD, "Head", top=(0.9, 0.9), role="limb", bevel=0.01,
          studs=[], nostud=True)
    for x, h, kink in ((-0.11, 0.10, False), (-0.055, 0.15, True), (0.0, 0.21, True), (0.055, 0.15, True),
                       (0.11, 0.10, False)):""",
    """    B.add((0, -0.935, 1.735), (0.165, 0.055, 0.045), GOLD, "Head", top=(0.9, 0.9), role="limb", bevel=0.01,
          studs=[], nostud=True)
    for s in (1, -1):                                                                     # circlet side bars
        B.seg((s * 0.165, -0.93, 1.735), (s * 0.155, -0.665, 1.745), 0.022, 0.03, GOLD, "Head", studs=[],
              nostud=True, role="limb")
    B.add((0, -0.655, 1.74), (0.10, 0.02, 0.035), GOLD, "Head", studs=[], nostud=True, role="limb", bevel=0.008)
    B.add((0, -0.633, 1.74), (0.022, 0.006, 0.022), CYAN, "Head", rot=(0, 45, 0), studs=[], role="detail",
          bevel=0.004)                                                                   # back gem
    for x, h, kink in ((-0.11, 0.12, False), (-0.055, 0.18, True), (0.0, 0.24, True), (0.055, 0.18, True),
                       (0.11, 0.12, False)):""")
rep("""            B.seg(base, m1, 0.024, 0.02, CYAN, "Head", side=(0, 1, 0), ext=0.02, studs=[], nostud=True, role="limb")
            B.seg(m1 - d * 0.01, m2, 0.02, 0.018, CYAN, "Head", side=(0, 1, 0), studs=[], nostud=True, role="limb")""",
    """            B.seg(base, m1, 0.028, 0.02, GOLD, "Head", side=(0, 1, 0), ext=0.02, studs=[], nostud=True, role="limb")
            B.seg(m1 - d * 0.01, m2, 0.026, 0.018, GOLD, "Head", side=(0, 1, 0), studs=[], nostud=True, role="limb")""")
rep("""            B.seg(base, base + d * h * 0.55, 0.022, 0.02, CYAN, "Head", side=(0, 1, 0), ext=0.02, studs=[],""",
    """            B.seg(base, base + d * h * 0.55, 0.028, 0.02, GOLD, "Head", side=(0, 1, 0), ext=0.02, studs=[],""")
# walk safety: ankle spur re-aimed
rep("""        B.spike(A + Vector((0, 0.07, 0.02)), (0, 1, 0.25), 0.10, 0.03, ARMOR""", """        B.spike(A + Vector((0, 0.07, 0.02)), (0, 1, -0.2), 0.10, 0.03, ARMOR""")
# FIX 4 tail belly wider/deeper; FIX 2 tail shells wider than the hide + joint bands proud
rep("""        B.seg(a + dn * hw * 0.82, b + dn * hw * tp * 0.82, hw * 0.6, hw * 0.22, BELLY, bone,""",
    """        B.seg(a + dn * hw * 0.80, b + dn * hw * tp * 0.80, hw * 1.0, hw * 0.26, BELLY, bone,""")
rep("""- dn * hw * tp * 0.42, hw * 0.92, hw * 0.62,""", """- dn * hw * tp * 0.42, hw * 1.06, hw * 0.62,""")
rep("""            B.seg(a - dv * 0.025, a + dv * 0.025, hw * 1.13, hw * 1.05, CYAN""", """            B.seg(a - dv * 0.025, a + dv * 0.025, hw * 1.16, hw * 1.10, CYAN""")
# FIX 3 thunder blade thicker + side shards
rep("""    B.seg(tip - Vector((0, 0.04, 0)), b1, 0.028, 0.07, DEEP""", """    B.seg(tip - Vector((0, 0.04, 0)), b1, 0.040, 0.07, DEEP""")
rep("""    B.seg(b1 - Vector((0, 0.03, -0.03)), b2, 0.026, 0.06, CYAN""", """    B.seg(b1 - Vector((0, 0.03, -0.03)), b2, 0.040, 0.06, CYAN""")
rep("""    B.seg(b2 - Vector((0, 0.03, 0.03)), b3, 0.024, 0.065, CYAN""", """    B.seg(b2 - Vector((0, 0.03, 0.03)), b3, 0.040, 0.065, CYAN""")
rep("""    B.spike(b3 - (b3 - b2).normalized() * 0.06, b3 - b2, 0.10, 0.022, HOT, "Tail4", top=(0.12, 0.12), nostud=True)""",
    """    B.spike(b3 - (b3 - b2).normalized() * 0.06, b3 - b2, 0.10, 0.03, HOT, "Tail4", top=(0.12, 0.12), nostud=True)
    for s in (1, -1):
        shard(B, b1, (s * 0.55, 0.45, 0.70), 0.15, 0.05, "Tail4", socket=False)""")
# A: drop centre shard 1 (skull hit), shard 2 -> Chest; kink flags explicit; side pairs on Tail1/Tail2; ridge tips
rep("""    centre = [(-0.585, 0.20, 26, "Neck"), (-0.47, 0.27, 27, "Neck"), (-0.335, 0.36, 28, "Chest"),
              (-0.20, 0.42, 29, "Chest"), (-0.065, 0.40, 30, "Chest"), (0.07, 0.34, 31, "Chest"),
              (0.21, 0.28, 32, "Spine"), (0.35, 0.22, 33, "Spine"), (0.58, 0.18, 35, "Tail1"),
              (0.92, 0.15, 35, "Tail2"), (1.24, 0.12, 35, "Tail3")]
    for i, (y, L, ang, bone) in enumerate(centre):
        p, _ = surf_hit(B, body_tops, (0, y, 3.0), (0, 0, -1))
        d = Vector((0, math.sin(math.radians(ang)), math.cos(math.radians(ang))))
        shard(B, p, d, L, 0.045 + 0.075 * L, bone, kink=(i % 2 == 1))
    for s in (1, -1):
        for y, L, ang, bone in centre[2:8]:
            p, _ = surf_hit(B, body_tops, (s * 0.13, y, 3.0), (0, 0, -1))
            sp = math.radians(28)
            d = Vector((s * math.sin(sp), math.sin(math.radians(ang)) * math.cos(sp),
                        math.cos(math.radians(ang)) * math.cos(sp)))
            shard(B, p, d, L * 0.55, 0.035 + 0.06 * L, bone, kink=False)""",
    """    centre = [(-0.47, 0.27, 27, "Chest", True), (-0.335, 0.36, 28, "Chest", False),
              (-0.20, 0.42, 29, "Chest", True), (-0.065, 0.40, 30, "Chest", False), (0.07, 0.34, 31, "Chest", True),
              (0.21, 0.28, 32, "Spine", False), (0.35, 0.22, 33, "Spine", True), (0.58, 0.18, 35, "Tail1", False),
              (0.92, 0.15, 35, "Tail2", True), (1.24, 0.12, 35, "Tail3", False)]
    tips = {}
    for y, L, ang, bone, kink in centre:
        p, _ = surf_hit(B, body_tops, (0, y, 3.0), (0, 0, -1))
        d = Vector((0, math.sin(math.radians(ang)), math.cos(math.radians(ang))))
        tips[y] = shard(B, p, d, L, 0.045 + 0.075 * L, bone, kink=kink)
    RIDGE_TIPS = [tuple(round(v, 4) for v in tips[y]) for y in (-0.335, -0.20, -0.065)]
    for s in (1, -1):
        for (y, L, ang, bone, _), sx, f in [(c, 0.13, 0.55) for c in centre[1:7]] + [(centre[7], 0.12, 0.6),
                                                                                     (centre[8], 0.09, 0.6)]:
            p, _ = surf_hit(B, body_tops, (s * sx, y, 3.0), (0, 0, -1))
            sp = math.radians(28)
            d = Vector((s * math.sin(sp), math.sin(math.radians(ang)) * math.cos(sp),
                        math.cos(math.radians(ang)) * math.cos(sp)))
            shard(B, p, d, L * f, 0.035 + 0.06 * L, bone, kink=False)""")
rep("""    return {"TH": round(B.th, 3), "PITCH": PITCH, "CORE": [round(v, 3) for v in CORE]}""",
    """    return {"TH": round(B.th, 3), "PITCH": PITCH, "CORE": [round(v, 3) for v in CORE], "RIDGE": RIDGE_TIPS}""")
# D: VFX anchors at the real shard tips + breath at the mouth
rep("""    k.joint("Breath", (0, -1.20, 1.36), "Head", tail=(0, -0.2, 0))""", """    k.joint("Breath", (0, -1.26, 1.31), "Head", tail=(0, -0.2, 0))""")
rep("""    k.joint("Ridge1", (0, -0.30, 1.75), "Chest", tail=(0, 0, 0.2))
    k.joint("Ridge2", (0, -0.05, 1.70), "Chest", tail=(0, 0, 0.2))
    k.joint("Ridge3", (0, 0.25, 1.50), "Spine", tail=(0, 0, 0.2))""",
    """    for i, tp in enumerate(RIDGE_TIPS):
        k.joint("Ridge%d" % (i + 1), tp, "Chest", tail=(0, 0, 0.2))""")
# collision check: tail root vs the thighs
rep("""    for t in ("Tail2", "Tail3", "Tail4"):
        for b in ("Shin_L", "Shin_R", "Foot_L", "Foot_R"):
            P.append((t, b))
    return P""", """    for t in ("Tail2", "Tail3", "Tail4"):
        for b in ("Shin_L", "Shin_R", "Foot_L", "Foot_R"):
            P.append((t, b))
    P += [("Tail1", "Leg_L"), ("Tail1", "Leg_R")]
    return P""")
# pose limits: Neck <= 8, Chest vs Spine <= 5 (roar lift by the Spine)
rep("""        (14, -0.10, 9, 4, 16, 10, 5, 10, -10, 0, 10),
        (20, -0.10, 10, 5, 18, 12, 6, 12, -12, 0, 12),
        (27, 0.02, -6, -4, -6, 4, 18, 8, 10, 14, 20),
        (32, 0.03, -8, -5, -10, -14, 40, 12, 16, 24, 32),
        (60, 0.02, -7, -5, -9, -12, 38, 12, 16, 24, 32),""",
    """        (14, -0.10, 14, 4, 8, 12, 5, 10, -10, 0, 10),
        (20, -0.10, 16, 5, 8, 14, 6, 12, -12, 0, 12),
        (27, 0.02, -8, -4, -4, 4, 18, 8, 10, 14, 20),
        (32, 0.03, -11, -5, -8, -16, 40, 12, 16, 24, 32),
        (60, 0.02, -10, -5, -7, -14, 38, 12, 16, 24, 32),""")
# tailspin: pitch moves into the Spine (extra quaternion), Chest capped at 5, Neck at 8
rep("""    for f, z, yaw, p, nk, hd, jw, tp, ty, au, sp in K:
        cm.key_axis(k, "Spine", f, Z, yaw, loc=(0, 0, z))
        k.key("Chest", f, rot=(p, 0, 0))
        k.key("Neck", f, rot=(nk, 0, 0))""",
    """    from mathutils import Quaternion
    for f, z, yaw, p, nk, hd, jw, tp, ty, au, sp in K:
        cm.key_axis(k, "Spine", f, Z, yaw, loc=(0, 0, z), extra=Quaternion((1, 0, 0), math.radians(p * 0.6)))
        k.key("Chest", f, rot=(max(-5, min(5, p * 0.4)), 0, 0))
        k.key("Neck", f, rot=(max(-8, min(8, nk)), 0, 0))""")
open(p, "w", encoding="utf-8").write(s)
print("v3 patched")
