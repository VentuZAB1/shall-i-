# review 2 (REVISE 7/10) round 3: M1 upper primaries lilac + a 3-feather WING_IN hand-covert highlight, M2 BLOOD tail
# brush (red from the game camera), M3 outer mane ring +7 % / 26 tufts, M4 BODY_MID chroma (190,120,226)
p = "pets/EclipseSeraph.py"
s = open(p, encoding="utf-8").read()


def rep(a, b, cnt=1):
    global s
    assert s.count(a) == cnt, (s.count(a), a[:90])
    s = s.replace(a, b)


rep("BODY_MID = (184, 128, 214)    # rich lilac (H 278): chest, tuck, waist, hips, legs, paws, tail, coverts of B + C",
    "BODY_MID = (190, 120, 226)    # rich lilac (H 280, S 0.47): chest, tuck, waist, hips, legs, paws, tail, B + C coverts")
rep("fw * 0.90, 0.03, WING_IN if rows3 else WING_LILAC,", "fw * 0.90, 0.03, WING_LILAC,")
rep("nrm, 0.20, 0.03, WING_LILAC, tb,", "nrm, 0.20, 0.03, WING_IN, tb,")
rep('(0.29, 0.34, 0.10, 24, 0.19, "Mane", 1.1))):', '(0.31, 0.36, 0.10, 26, 0.19, "Mane", 1.1))):')
rep('    B.add(tip + Vector((0, 0.02, -0.01)), (0.10, 0.11, 0.095), OBSID, "Tail4", rnd=0.4)',
    '    B.add(tip + Vector((0, 0.02, -0.01)), (0.10, 0.11, 0.095), BLOOD, "Tail4", rnd=0.4)        # blood brush')
rep('        tuft(B, tip + Vector((0, 0.02, -0.01)), d, L, 0.06, OBSID, "Tail4")',
    '        tuft(B, tip + Vector((0, 0.02, -0.01)), d, L, 0.06, BLOOD, "Tail4")')
rep("WING_LILAC = (190, 150, 226)  # flight feathers of B + C, the upper pair's coverts + secondaries",
    "WING_LILAC = (190, 150, 226)  # all flight feathers + the upper pair's coverts (WING_IN = 3 hand coverts only)")
open(p, "w", encoding="utf-8").write(s)
print("ok")
