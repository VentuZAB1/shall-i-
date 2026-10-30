# review 1, MUST 4 second pass (osprey stripe through the eye, no box) + CHAR down / SNOW up from behind
p = "pets/BlizzardRoc.py"
s = open(p, encoding="utf-8").read()


def rep(a, b, cnt=1):
    global s
    assert s.count(a) == cnt, (s.count(a), a[:90])
    s = s.replace(a, b)


rep('''        # osprey mask: a CHAR plate round the eye socket + a stripe back along the skull side to the nape
        ec = HC + Vector((s * 0.104, -0.128, 0.022))
        Re = Euler((0, math.radians(-s * 18), math.radians(s * 26)), "XYZ").to_matrix()
        B.add(ec + Re @ Vector((s * 0.006, 0.006, 0.002)), (0.070, 0.008, 0.028), CHAR, "Head", R=Re, studs=[],
              role="detail", bevel=0.006)
        B.bar(HC + Vector((s * 0.122, -0.08, 0.018)), HC + Vector((s * 0.122, 0.07, -0.006)), Vector((s, 0, 0)),
              0.07, 0.018, CHAR, "Head", studs=[], role="detail", bevel=0.005, top=(1, 0.45))''',
    '''        # osprey mask: ONE slanted CHAR stripe from the gape through the eye and back along the skull side to the
        # nape (no box round the eye): a front piece under the eye on the face, the side band, the nape tail
        ec = HC + Vector((s * 0.104, -0.128, 0.022))
        B.bar(HC + Vector((s * 0.084, -0.172, -0.022)), HC + Vector((s * 0.112, -0.108, 0.010)),
              Vector((s, -0.55, 0)), 0.042, 0.012, CHAR, "Head", studs=[], role="detail", bevel=0.004)
        B.bar(HC + Vector((s * 0.120, -0.105, 0.012)), HC + Vector((s * 0.124, 0.07, -0.010)), Vector((s, 0, 0)),
              0.058, 0.018, CHAR, "Head", studs=[], role="detail", bevel=0.005, top=(1, 0.5))''')
rep('''        B.add(HC + Vector((s * 0.080, -0.090, 0.068)), (0.075, 0.04, 0.024), CHAR, "Head",
              rot=(0, -s * 21, s * 22), top=(0.8, 0.85), role="detail", bevel=0.012)            # heavy V brow''',
    '''        B.add(HC + Vector((s * 0.080, -0.100, 0.064)), (0.072, 0.026, 0.019), CHAR, "Head",
              rot=(0, -s * 21, s * 22), top=(0.8, 0.85), role="detail", bevel=0.008)            # slim V brow''')
# CHAR down: a shorter dark trailing edge on the secondaries
rep('''        feather(B, a - nrm * 0.016, end - nrm * 0.016, nrm, 0.27, 0.034, STORM_GREY, wb, taper=0.35,
                bars=[(CHAR, 0.30)])''', '''        feather(B, a - nrm * 0.016, end - nrm * 0.016, nrm, 0.27, 0.034, STORM_GREY, wb, taper=0.35,
                bars=[(CHAR, 0.18)])''')
# SNOW up from behind: snowy-owl white shoulder coverts (the inner 3 of 7), violet bars kept on t > 0.22
rep('''        feather(B, a + nrm * 0.02, end + nrm * 0.02, nrm, 0.22, 0.034, STORM_GREY if t > 0.22 else SNOW, wb,''',
    '''        feather(B, a + nrm * 0.02, end + nrm * 0.02, nrm, 0.22, 0.034, STORM_GREY if t > 0.45 else SNOW, wb,''')
open(p, "w", encoding="utf-8").write(s)
print("ok")
