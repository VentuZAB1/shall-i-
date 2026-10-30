import re
p = r"pets/BlizzardRoc.py"
s = open(p, encoding="utf-8").read()
# 1. head mask: CHAR plate around each eye socket + a stripe back along the skull side, mask tail on the nape
old = s[s.index("    for s in (1, -1):\n        # osprey mask"):s.index("    B.add(HC + Vector((0, -0.16, -0.015))")]
new = '''    for s in (1, -1):
        # osprey mask: a CHAR plate round the eye socket + a stripe back along the skull side to the nape
        ec = HC + Vector((s * 0.104, -0.128, 0.022))
        Re = Euler((0, math.radians(-s * 18), math.radians(s * 26)), "XYZ").to_matrix()
        B.add(ec + Re @ Vector((s * 0.006, 0.006, 0.002)), (0.088, 0.008, 0.044), CHAR, "Head", R=Re, studs=[],
              role="detail", bevel=0.006)
        B.bar(HC + Vector((s * 0.122, -0.08, 0.018)), HC + Vector((s * 0.122, 0.07, -0.006)), Vector((s, 0, 0)),
              0.07, 0.014, CHAR, "Head", studs=[], role="detail", bevel=0.005, top=(1, 0.6))
        B.bar(HC + Vector((s * 0.10, 0.10, -0.02)), HC + Vector((s * 0.085, 0.16, -0.10)), Vector((s, 0.6, 0)),
              0.05, 0.012, CHAR, "Head", studs=[], role="detail", bevel=0.004, top=(1, 0.3))
        eye(B, ec, s, sc=1.25)
        B.add(HC + Vector((s * 0.080, -0.090, 0.072)), (0.088, 0.04, 0.034), CHAR, "Head",
              rot=(0, -s * 21, s * 22), top=(0.8, 0.85), role="detail", bevel=0.012)            # heavy V brow
'''
s = s.replace(old, new)
s = s.replace("B.add(HC + Vector((s * 0.062, -0.215, -0.060)), (0.004, 0.062, 0.008), MOUTH",
              "B.add(HC + Vector((s * 0.050, -0.215, -0.062)), (0.004, 0.058, 0.007), MOUTH")
# 2. crest bigger
s = s.replace('(("C", (0, -0.47, 1.70), (0, 0.30, 0.95), 0.27, 0.085),', '(("C", (0, -0.47, 1.70), (0, 0.30, 0.95), 0.31, 0.10),')
s = s.replace('("L", (0.045, -0.45, 1.69), (0.36, 0.34, 0.87), 0.22, 0.075),', '("L", (0.05, -0.45, 1.69), (0.36, 0.34, 0.87), 0.25, 0.088),')
s = s.replace('("R", (-0.045, -0.45, 1.69), (-0.36, 0.34, 0.87), 0.22, 0.075)):', '("R", (-0.05, -0.45, 1.69), (-0.36, 0.34, 0.87), 0.25, 0.088)):')
# 3. tail broader
s = s.replace("((-0.105, -7.0, 0.74), (-0.035, -2.5, 0.80), (0.035, 2.5, 0.80),\n                                     (0.105, 7.0, 0.74))",
              "((-0.14, -8.0, 0.74), (-0.047, -2.5, 0.80), (0.047, 2.5, 0.80),\n                                     (0.14, 8.0, 0.74))")
s = s.replace("tp = feather(B, root, root + d * L, fan_n, 0.105, 0.03, STORM_GREY", "tp = feather(B, root, root + d * L, fan_n, 0.15, 0.03, STORM_GREY")
# 4. shorter chevron bars
s = s.replace("for lz, hw in ((0.11, 0.62), (0.0, 0.70), (-0.11, 0.62)):\n        face_bar(B, keel, -1, lz, hw * keel.h.x * 2, 0.034, CHAR, \"Chest\", vee=12.0, proud=0.026)",
              "for lz, hw in ((0.12, 0.46), (0.01, 0.56), (-0.10, 0.46)):\n        face_bar(B, keel, -1, lz, hw * keel.h.x * 2, 0.03, CHAR, \"Chest\", vee=20.0, proud=0.026)")
# 5. mantle + coverts barred: CHAR tips
s = s.replace('''    face_shingles(B, chest, 1, [(0.20, (0.0,)), (0.08, xs4), (-0.06, xs3)], lambda r, x: STORM_GREY, "Chest",
                  size=(0.065, 0.022, 0.09))
    face_shingles(B, low, 1, [(0.08, (-0.09, 0.0, 0.09)), (-0.06, (-0.045, 0.045))], lambda r, x: STORM_GREY,
                  "Spine", size=(0.06, 0.02, 0.08))''',
'''    face_shingles(B, chest, 1, [(0.20, (0.0,)), (0.08, xs4), (-0.06, xs3)], lambda r, x: STORM_GREY, "Chest",
                  size=(0.065, 0.022, 0.09), tip=CHAR)
    face_shingles(B, low, 1, [(0.08, (-0.09, 0.0, 0.09)), (-0.06, (-0.045, 0.045))], lambda r, x: STORM_GREY,
                  "Spine", size=(0.06, 0.02, 0.08), tip=CHAR)''')
s = s.replace('''def face_shingles(B, blk, face, rows, color_of, bone, size=(0.055, 0.02, 0.07)):
    """down-pointing shingles on the -y (face=-1, breast) or +y (face=+1, back) face of a rotated tapered block"""''',
'''def face_shingles(B, blk, face, rows, color_of, bone, size=(0.055, 0.02, 0.07), tip=None):
    """down-pointing shingles on the -y (face=-1, breast) or +y (face=+1, back) face of a rotated tapered block;
    tip = a colour for a pointed lower tip (barred feathers)"""''')
s = s.replace('''            B.add(p, size, color_of(r, x), bone, R=Rf, bot=(0.2, 1.0), role="detail", bevel=0.008)


def face_bar''', '''            B.add(p, size, color_of(r, x), bone, R=Rf, bot=(0.2, 1.0), role="detail", bevel=0.008)
            if tip:
                q = p + Rf @ Vector((0, face * 0.004, -size[2] * 0.62))
                B.add(q, (size[0] * 0.52, size[1] * 0.75, size[2] * 0.40), tip, bone, R=Rf, bot=(0.15, 1.0),
                      top=(0.75, 1.0), role="detail", bevel=0.006)


def face_bar''')
s = s.replace('''        feather(B, a + nrm * 0.02, end + nrm * 0.02, nrm, 0.22, 0.034, STORM_GREY if t > 0.22 else SNOW, wb,
                taper=0.5)''', '''        feather(B, a + nrm * 0.02, end + nrm * 0.02, nrm, 0.22, 0.034, STORM_GREY if t > 0.22 else SNOW, wb,
                taper=0.5, bars=[(CHAR, 0.24)] if t > 0.22 else None)''')
open(p, "w", encoding="utf-8").write(s)
print("ok")
