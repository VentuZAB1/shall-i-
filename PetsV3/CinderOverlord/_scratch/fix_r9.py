# Cinder Overlord final-8.5 round 9 (_review/CinderOverlord_final85_r9.md + coordinator)
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


# MUST 1a: forearms out (elbow x 0.28 -> 0.40, hand 0.24 -> 0.36), model + rig fallback + joints list
rep("""        el = Vector((s * 0.28, -0.82, 0.65))
        ha = Vector((s * 0.24, -0.93, 0.59))""",
    """        el = Vector((s * 0.40, -0.82, 0.65))                  # r9 MUST 1a: out of the neck silhouette (was 0.28)
        ha = Vector((s * 0.36, -0.93, 0.59))                  # r9 (was 0.24): claws braced forward beside the neck""")
rep("""        h, e, sh = ANCH.get("Claw_" + side, ((s * 0.24, -0.93, 0.59), (s * 0.28, -0.82, 0.65),""",
    """        h, e, sh = ANCH.get("Claw_" + side, ((s * 0.36, -0.93, 0.59), (s * 0.40, -0.82, 0.65),""")
rep("""        out.append(((s * 0.28, -0.82, 0.65), (s * 0.28, -0.82, 0.65), 0.07, "Claw_" + side))""",
    """        out.append(((s * 0.40, -0.82, 0.65), (s * 0.40, -0.82, 0.65), 0.07, "Claw_" + side))""")
# MUST 1c: the Tail4 ring goes too - the back shows two bands (Spine base + Body1)
rep("""        if i not in (2, 3, 4, 5, 6, 7):  # r8: rings only on Spine / Body1 / Tail4 (r6 skip 2, 3, 5, 6, 7; worm read)""",
    """        if i not in (2, 3, 4, 5, 6, 7, 8):  # r9: rings only on Spine / Body1 (r8 + Tail4; r6 skip 2, 3, 5, 6, 7)""")
# MUST 2: the chin tapers into the jaw (0.85 station rh 0.040 -> 0.032) and its front sits 0.02 further back
rep("""    _jaw, jkf = loft(B, jp((0, 0.03, -0.01)), jp((0, -0.48, -0.035)), ((0.0, 0.118, 0.044, 0.0), (0.12, 0.148, 0.054, 0.0),
                                                            (0.55, 0.126, 0.052, 0.0), (0.85, 0.098, 0.040, 0.0),""",
    """    _jaw, jkf = loft(B, jp((0, 0.03, -0.01)), jp((0, -0.46, -0.035)), ((0.0, 0.118, 0.044, 0.0), (0.12, 0.148, 0.054, 0.0),
                                                            (0.55, 0.126, 0.052, 0.0), (0.85, 0.098, 0.032, 0.0),   # r9 MUST 2: rh 0.040 -> 0.032, tip 0.02 back""")
# MUST 1b: Head + Jaw (+ Mouth) x1.15 in x only (about x = 0, the throat), the Crown_1..5 bones untouched
rep("""    B.build()
    global H_MODEL""",
    """    _xscale(B, ("Head", "Jaw", "Mouth"), HEAD_WX)                 # r9 MUST 1b: a broader, heavier skull
    B.build()
    global H_MODEL""")
rep("""def vent_flush(B, j, t, ang, L, w, bone, side, seg_blk=None):""",
    """HEAD_WX = 1.15              # r9 MUST 1b: skull + jaw width (x only); the crown blades keep their socket spacing


def _xscale(B, bones, sx):
    \"\"\"x-only scale about x = 0 for every part of the given bones (blockkit's HEAD_XF is uniform only). Boxes keep
    their rotation; each local half-size grows by the length of its scaled local axis.\"\"\"
    import blockkit as bk
    S = Matrix(((sx, 0, 0), (0, 1, 0), (0, 0, 1)))
    for blk in B.items:
        if blk.bone not in bones:
            continue
        if isinstance(blk, bk.Tube):
            blk.map(lambda q: Vector((q.x * sx, q.y, q.z)))
            blk.pts = [Vector((q.x * sx, q.y, q.z)) for q in blk.pts]
            blk.c = sum(blk.pts, Vector()) / len(blk.pts)
        elif isinstance(blk, bk.Poly):
            blk.pts = [Vector((q.x * sx, q.y, q.z)) for q in blk.pts]
            blk.c = sum(blk.pts, Vector()) / len(blk.pts)
        else:
            blk.c = Vector((blk.c.x * sx, blk.c.y, blk.c.z))
            blk.h = Vector([blk.h[i] * (S @ blk.R.col[i]).length for i in range(3)])


def vent_flush(B, j, t, ang, L, w, bone, side, seg_blk=None):""")
io.open(p, "w", encoding="utf-8").write(s)
print("patched", n_ok)
