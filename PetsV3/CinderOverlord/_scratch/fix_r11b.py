# Cinder r11 (b): cobra HOOD - the upper neck's cross-section widens sideways (x only; the y depth, the back spikes
# and the throat scutes keep their places), widest just under the head. Per-FRONT-point x multipliers HOOD_WX.
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


rep("""NECKS = ["Neck1", "Neck2", "Neck3"]""",
    """NECKS = ["Neck1", "Neck2", "Neck3"]
# r11 MUST 1 (cobra stance): a cobra HOOD - side (x) radius multiplier per FRONT point; the neck flares just under the
# head so the reared front reads as a hooded cobra from behind, not an even tube. y depth unchanged.
HOOD_WX = (1.0, 1.0, 1.0, 1.20, 1.60, 1.25)""")
# body_seg / band / surf_pt: optional side-radius multipliers (default 1.0 = unchanged for every other caller)
rep("""def body_seg(B, a, b, r0, r1, bone, color=None, ext0=0.0, ext1=0.0, flat=0.92, up=(0, 0, 1)):""",
    """def body_seg(B, a, b, r0, r1, bone, color=None, ext0=0.0, ext1=0.0, flat=0.92, up=(0, 0, 1), wx0=1.0, wx1=1.0):""")
rep("""        r = (r0 + (r1 - r0) * tt) * kf
        rings.append(oval(a + d * dist, side, upv, r, r * flat))
    return B.tube(rings, color or PLUM_OBS, bone)""",
    """        r = (r0 + (r1 - r0) * tt) * kf
        rings.append(oval(a + d * dist, side, upv, r * (wx0 + (wx1 - wx0) * tt), r * flat))
    return B.tube(rings, color or PLUM_OBS, bone)""")
rep("""def band(B, a, b, r0, r1, bone, color, a0, a1, off=0.012, thick=0.02, up=(0, 0, 1), seg=8, flat=0.92, nr=2,
         nostud=True):""",
    """def band(B, a, b, r0, r1, bone, color, a0, a1, off=0.012, thick=0.02, up=(0, 0, 1), seg=8, flat=0.92, nr=2,
         nostud=True, wx0=1.0, wx1=1.0):""")
rep("""        r = r0 + (r1 - r0) * t
        rings.append((oval(c, side, upv, r, r * flat, a0, a1, seg, off=off),
                      oval(c, side, upv, r, r * flat, a0, a1, seg, off=off - thick)))""",
    """        r = r0 + (r1 - r0) * t
        rx = r * (wx0 + (wx1 - wx0) * t)
        rings.append((oval(c, side, upv, rx, r * flat, a0, a1, seg, off=off),
                      oval(c, side, upv, rx, r * flat, a0, a1, seg, off=off - thick)))""")
rep("""def surf_pt(a, b, r0, r1, t, ang, off=0.0, flat=0.92, up=(0, 0, 1)):
    \"\"\"point + outward normal on the body segment surface at fraction t, angle ang (0 = +side, pi/2 = top)\"\"\"
    a, b = Vector(a), Vector(b)
    d = (b - a).normalized()
    side, upv = frame_of(d, up)
    r = r0 + (r1 - r0) * t
    n = (side * math.cos(ang) + upv * math.sin(ang) / flat).normalized()
    return a.lerp(b, t) + side * (r + off) * math.cos(ang) + upv * (r * flat + off) * math.sin(ang), n, d""",
    """def surf_pt(a, b, r0, r1, t, ang, off=0.0, flat=0.92, up=(0, 0, 1), wx=1.0):
    \"\"\"point + outward normal on the body segment surface at fraction t, angle ang (0 = +side, pi/2 = top)\"\"\"
    a, b = Vector(a), Vector(b)
    d = (b - a).normalized()
    side, upv = frame_of(d, up)
    r = r0 + (r1 - r0) * t
    n = (side * math.cos(ang) / wx + upv * math.sin(ang) / flat).normalized()
    return a.lerp(b, t) + side * (r * wx + off) * math.cos(ang) + upv * (r * flat + off) * math.sin(ang), n, d""")
# the scute / ring helpers pass the multipliers through
rep("""    def scutes(a, b, r0, r1, bone, a0, a1, up=(0, 0, 1), ts=((0.04, 0.30), (0.36, 0.62), (0.68, 0.94))):
        for t0, t1 in ts:                                    # transverse ventral scute plates (gaps between)
            band(B, a.lerp(b, t0), a.lerp(b, t1), r0 + (r1 - r0) * t0, r0 + (r1 - r0) * t1, bone, PALE_S,
                 math.radians(a0), math.radians(a1), off=0.009, thick=0.022, up=up)""",
    """    def scutes(a, b, r0, r1, bone, a0, a1, up=(0, 0, 1), ts=((0.04, 0.30), (0.36, 0.62), (0.68, 0.94)), wx=(1.0, 1.0)):
        for t0, t1 in ts:                                    # transverse ventral scute plates (gaps between)
            band(B, a.lerp(b, t0), a.lerp(b, t1), r0 + (r1 - r0) * t0, r0 + (r1 - r0) * t1, bone, PALE_S,
                 math.radians(a0), math.radians(a1), off=0.009, thick=0.022, up=up,
                 wx0=wx[0] + (wx[1] - wx[0]) * t0, wx1=wx[0] + (wx[1] - wx[0]) * t1)""")
rep("""    def ring_band(a, b, r0, r1, bone, t0, t1, up=(0, 0, 1)):
        \"\"\"obsidian scale band wrapping the back and the flanks (banded-krait rings)\"\"\"
        band(B, a.lerp(b, t0), a.lerp(b, t1), r0 + (r1 - r0) * t0, r0 + (r1 - r0) * t1, bone, OBS_D,
             math.radians(8), math.radians(172), off=0.011, thick=0.026, up=up, seg=12, nostud=False)""",
    """    def ring_band(a, b, r0, r1, bone, t0, t1, up=(0, 0, 1), wx=(1.0, 1.0)):
        \"\"\"obsidian scale band wrapping the back and the flanks (banded-krait rings)\"\"\"
        band(B, a.lerp(b, t0), a.lerp(b, t1), r0 + (r1 - r0) * t0, r0 + (r1 - r0) * t1, bone, OBS_D,
             math.radians(8), math.radians(172), off=0.011, thick=0.026, up=up, seg=12, nostud=False,
             wx0=wx[0] + (wx[1] - wx[0]) * t0, wx1=wx[0] + (wx[1] - wx[0]) * t1)""")
rep("""        body_seg(B, a, b, FRAD[i], FRAD[i + 1], fb[i], ext0=FRAD[i] * 0.5 if i else 0.0, ext1=FRAD[i + 1] * 0.5,
                 up=(0, 1, 0))
        scutes(a, b, FRAD[i], FRAD[i + 1], fb[i], 238, 302, up=(0, 1, 0), ts=((0.04, 0.46), (0.52, 0.94)))
        if i == 2:                                        # r3 MUST 2: a full ring on Neck1 only
            ring_band(a, b, FRAD[i], FRAD[i + 1], fb[i], 0.50, 0.84, up=(0, 1, 0))
        elif i == 3:                                      # r4: Neck2 a thin band (0.70-0.80); Neck3 has none
            ring_band(a, b, FRAD[i], FRAD[i + 1], fb[i], 0.70, 0.80, up=(0, 1, 0))""",
    """        wx = (HOOD_WX[i], HOOD_WX[i + 1])                 # r11: the cobra hood (x only)
        body_seg(B, a, b, FRAD[i], FRAD[i + 1], fb[i], ext0=FRAD[i] * 0.5 if i else 0.0, ext1=FRAD[i + 1] * 0.5,
                 up=(0, 1, 0), wx0=wx[0], wx1=wx[1])
        scutes(a, b, FRAD[i], FRAD[i + 1], fb[i], 238, 302, up=(0, 1, 0), ts=((0.04, 0.46), (0.52, 0.94)), wx=wx)
        if i == 2:                                        # r3 MUST 2: a full ring on Neck1 only
            ring_band(a, b, FRAD[i], FRAD[i + 1], fb[i], 0.50, 0.84, up=(0, 1, 0), wx=wx)
        elif i == 3:                                      # r4: Neck2 a thin band (0.70-0.80); Neck3 has none
            ring_band(a, b, FRAD[i], FRAD[i + 1], fb[i], 0.70, 0.80, up=(0, 1, 0), wx=wx)""")
io.open(p, "w", encoding="utf-8").write(s)
print("patched", n_ok)
