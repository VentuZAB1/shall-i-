# clip pass 3: the bow droops the wings half-open LOW at the sides (DROOP, R3), not the lifted BREATH pose
p = "pets/BlizzardRoc.py"
s = open(p, encoding="utf-8").read()


def rep(a, b, cnt=1):
    global s
    assert s.count(a) == cnt, (s.count(a), a[:80])
    s = s.replace(a, b)


rep("BREATH = (80.0, 26.0, -65.0, -10.0)    # half-open, drooped at the sides (idle shed, the bow droop)",
    "BREATH = (80.0, 26.0, -65.0, -10.0)    # half-open, lifted at the sides (idle frost shed)\n"
    "DROOP = (65.0, 26.0, -75.0, 10.0)      # half-open, hanging low at the sides (the bow, R3)")
rep('''    for f, P in ((0, FOLD), (14, LIFT1), (22, BREATH), (44, BREATH), (48, LIFT2), (52, LIFT3), (55, LIFT2),
                 (57, LIFT1), (58, FOLD), (n, FOLD)):
        wp(k, f, P)
    for f, d in ((30, -5), (32, 4), (40, -5), (42, 4)):       # the drooped wings shudder on each bob (tips only)
        wp(k, f, (BREATH[0], BREATH[1], BREATH[2], BREATH[3] + d))''',
    '''    for f, P in ((0, FOLD), (14, LIFT1), (22, DROOP), (44, DROOP), (48, LIFT2), (52, LIFT3), (55, LIFT2),
                 (57, LIFT1), (58, FOLD), (n, FOLD)):
        wp(k, f, P)
    for f, d in ((30, -5), (32, 5), (40, -5), (42, 5)):       # the drooped wings shudder on each bob (tips only)
        wp(k, f, (DROOP[0], DROOP[1], DROOP[2], DROOP[3] + d))''')
open(p, "w", encoding="utf-8").write(s)
print("ok")
