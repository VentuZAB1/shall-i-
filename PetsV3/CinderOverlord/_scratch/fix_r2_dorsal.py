import io
P = "pets/CinderOverlord.py"
s = io.open(P, encoding="utf-8").read()
rep = [
('''    # ================= rear body on the ground (lateral S): lofted segments, obsidian rings, pale ventral scutes
''',
'''    def dorsal(a, b, r0, r1, bone, half_deg, up=(0, 0, 1)):
        """obsidian dorsal saddle along the top (r2: obsidian-dominant back; rings drop from it down the flanks)"""
        band(B, a.lerp(b, -0.05), a.lerp(b, 1.05), r0 + (r1 - r0) * -0.05, r0 + (r1 - r0) * 1.05, bone, OBS_D,
             math.radians(90 - half_deg), math.radians(90 + half_deg), off=0.0095, thick=0.024, up=up, seg=8,
             nostud=False)

    # ================= rear body on the ground (lateral S): lofted segments, obsidian rings + dorsal saddle, pale
    # ventral scutes
'''),
('''        a0, a1 = (195, 345) if i < 5 else ((205, 335) if i == 5 else (212, 328))
''',
'''        a0, a1 = (188, 352) if i < 5 else ((200, 340) if i == 5 else (212, 328))
        if i < 8:
            dorsal(a, b, RAD[i], RAD[i + 1], bone, 32 if i < 5 else 26)
'''),
('''        scutes(a, b, FRAD[i], FRAD[i + 1], fb[i], 232, 308, up=(0, 1, 0), ts=((0.04, 0.46), (0.52, 0.94)))
        if i >= 1:
            ring_band(a, b, FRAD[i], FRAD[i + 1], fb[i], 0.50, 0.84, up=(0, 1, 0))''',
'''        scutes(a, b, FRAD[i], FRAD[i + 1], fb[i], 238, 302, up=(0, 1, 0), ts=((0.04, 0.46), (0.52, 0.94)))
        if i >= 1:
            ring_band(a, b, FRAD[i], FRAD[i + 1], fb[i], 0.50, 0.84, up=(0, 1, 0))
            dorsal(a, b, FRAD[i], FRAD[i + 1], fb[i], 32, up=(0, 1, 0))'''),
('''            ang = math.radians(18 if s > 0 else 162)''', '''            ang = math.radians(24 if s > 0 else 156)'''),
]
for a, b in rep:
    assert a in s, a[:70]
    s = s.replace(a, b)
io.open(P, "w", encoding="utf-8").write(s)
print("ok")
