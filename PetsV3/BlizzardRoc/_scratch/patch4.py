# round 2b: value targets (review 1 MUST 2 / MUST 5 numbers): CHAR <= 28 side / 22 game, SNOW >= 15 game
p = "pets/BlizzardRoc.py"
s = open(p, encoding="utf-8").read()


def rep(a, b, cnt=1):
    global s
    assert s.count(a) == cnt, (s.count(a), a[:90])
    s = s.replace(a, b)


# white nape collar continued down the whole neck back (head + neck white from behind, grey from the mantle)
rep('    neck_cape(B, n2a, n2b, 0.13, [(0.50, (-0.065, 0.0, 0.065))], "Neck2")',
    '    neck_cape(B, n2a, n2b, 0.13, [(0.50, (-0.065, 0.0, 0.065))], "Neck2", col=SNOW)')
rep('    neck_cape(B, n1a, n1b, 0.155, [(0.85, (-0.09, -0.03, 0.03, 0.09)), (0.45, (-0.06, 0.06))], "Neck")',
    '    neck_cape(B, n1a, n1b, 0.155, [(0.85, (-0.09, -0.03, 0.03, 0.09))], "Neck", col=SNOW)\n'
    '    neck_cape(B, n1a, n1b, 0.155, [(0.45, (-0.06, 0.06))], "Neck")')
# primaries: storm-grey root, the outer 60 % dark (CHAR band, FROST_V bar, CHAR point) - dark wing tips, less slab
rep("PBARS = [(CHAR, 0.11), (FROST_V, 0.17)]          # primaries: a frost-violet bar, then a charcoal point",
    "PBARS = [(CHAR, 0.11), (FROST_V, 0.17), (CHAR, 0.32)]   # primaries: grey root, CHAR band, violet bar, CHAR point")
rep("0.25, 0.034, CHAR, wb, bars=PBARS)", "0.25, 0.034, STORM_GREY, wb, bars=PBARS)")
rep("0.23, 0.034, CHAR, tb, bars=PBARS)", "0.23, 0.034, STORM_GREY, tb, bars=PBARS)")
# white rump + uppertail coverts (seen by the game camera); the four tail feathers keep grey bases
rep('B.add((0, 0.31, 0.62), (0.12, 0.11, 0.08), STORM_GREY, "Spine"', 'B.add((0, 0.31, 0.62), (0.12, 0.11, 0.08), SNOW, "Spine"')
rep('B.seg(T[0], T[1], 0.13, 0.085, STORM_GREY, "Tail1"', 'B.seg(T[0], T[1], 0.13, 0.085, SNOW, "Tail1"')
rep('(0.06, 0.085, 0.02), STORM_GREY, "Tail1",', '(0.06, 0.085, 0.02), SNOW, "Tail1",')
rep("secondaries with a CHAR trailing edge; CHAR primaries fanned from the wrist, each with a FROST_V bar + CHAR point.",
    "secondaries with a CHAR trailing edge; primaries fanned from the wrist: grey root, CHAR band, FROST_V bar, CHAR point.")
open(p, "w", encoding="utf-8").write(s)
print("ok")
