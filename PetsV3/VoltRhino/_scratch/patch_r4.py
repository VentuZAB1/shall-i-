# clip review 3: braced taps (forequarters drop at each strike), tap 2 shallower with a lateral horn drag, smoother
# idle tail flick, TRUE lateral-sequence walk (measured: cm.quad_walk "walk" touches down BL, FR, BR, FL = diagonal)
import io
P = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\VoltRhino.py"
s = io.open(P, encoding="utf-8").read()


def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:70])
    s = s.replace(a, b)


a = s.index("TAP_P = [")
b = s.index("def horntap(k):")
s = s[:a] + '''TAP_P = [  # f, spine z, spine pitch, chest pitch, neck, head pitch, head yaw, jaw, tail pitch, ears
    (0, 0.0, 0.0, 0.0, 0, 0, 0, 0, 0, 0),
    (8, -0.006, 0.0, 1.5, 3, 14, 0, 0, 4, 0),
    (16, -0.006, 0.0, 1.5, 4, 44, 0, 0, 10, -8),
    (22, -0.002, 0.0, 2.0, 6, 62, 0, 0, 14, -10),     # face down, horn forward just above the snow
    (27, -0.002, 0.0, 2.0, 6, 57, 0, 0, 14, -10),     # cocked: the tip lifts
    (30, SZ, SP, CP, 6, HT, 0, 0, 16, -10),            # tap1: braced strike (forequarters drop, front knees fold)
    (34, -0.006, 0.5, 2.5, 6, 59, 0, 0, 16, -10),
    (39, -0.002, 0.0, 2.0, 6, 57, 0, 0, 16, -10),
    (42, SZ, SP, CP, 6, HT - 2.0, 0, 0, 18, -10),      # tap2: a little shallower ...
    (46, -0.010, 0.8, 3.0, 6, HT - 4.0, 6, 0, 18, -10),  # ... and the horn drags sideways
    (51, -0.002, 0.0, 2.0, 6, 57, 2, 0, 18, -10),
    (54, SZ, SP, CP, 6, HT, 0, 0, 20, -10),            # tap3
    (56, SZ, SP, CP, 6, HT, 0, 0, 20, -10),
    (58, -0.002, 0.0, 1.0, 3, 32, 0, 2, 26, 0),        # SNAP UP (in-betweens every 2 f)
    (60, -0.006, 0.0, -0.5, -1, 2, 0, 6, 30, 8),
    (62, 0.0, 0.0, -1.0, -4, -11, 0, 8, 32, 12),       # horn to the sky
    (66, 0.0, 0.0, -1.0, -4, -10.5, 0, 6, 30, 12),
    (86, 0.0, 0.0, -1.0, -4, -10.5, 0, 5, 26, 10),
    (94, 0.0, 0.0, -0.3, -1, -3, 0, 2, 8, 3),
    (100, 0.0, 0.0, 0.0, 0, 0, 0, 0, 0, 0)]


''' + s[b:]
rep('''TAP_P = [  # f, spine z, spine pitch''', '''SZ, SP, CP, HT = -0.024, 1.5, 3.8, 57.0   # the braced strike: spine drop + pitch, chest pitch, head pitch
TAP_P = [  # f, spine z, spine pitch''')
rep('''    for f, sz, cp, nk, hd, jw, tp, er in TAP_P:
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, sz))
        k.key("Chest", f, rot=(cp, 0, 0))
        k.key("Neck", f, rot=(nk, 0, 0), loc=neck_lift(-(nk + hd)))
        k.key("Head", f, rot=(hd, 0, 0))''', '''    for f, sz, sp, cp, nk, hd, hy, jw, tp, er in TAP_P:
        k.key("Spine", f, rot=(sp, 0, 0), loc=(0, 0, sz))
        k.key("Chest", f, rot=(cp, 0, 0))
        k.key("Neck", f, rot=(nk, 0, 0), loc=neck_lift(-(nk + hd)))
        k.key("Head", f, rot=(hd, hy, 0))''')
# smoother idle tail flick (review 3 NICE 1)
rep('''    for f, p, r in ((0, 4, 0), (84, 4, 0), (88, 22, 30), (90, 28, 38), (93, 18, 22), (98, 6, 4), (104, 4, 0),
                    (120, 4, 0)):''', '''    for f, p, r in ((0, 4, 0), (82, 4, 0), (86, 12, 14), (89, 22, 28), (92, 26, 34), (96, 15, 18), (101, 7, 5),
                    (107, 4, 0), (120, 4, 0)):''')
# true lateral-sequence walk: LH, LF, RH, RF touch-downs at 0, 0.25, 0.5, 0.75 of the cycle
rep('''    stride = cm.quad_walk(k, n, 0.12, 0.08, body, gait="walk", duty=0.70)
    return stride''', '''    legs = [("Leg_BL", 0.0), ("Leg_FL", 0.75), ("Leg_BR", 0.5), ("Leg_FR", 0.25)]   # touch-down at f0, 10, 20, 30
    k.meta["legs"], k.meta["duty"] = legs, 0.70
    return pk.walk_cycle(k, n, legs, 0.12, 0.08, body, duty=0.70)''')
rep('''        k.key("Spine", f, rot=(0.5 * pk.wave(f, n, 0.1, 2), 1.2 * pk.wave(f, n, 0.0), 2.0 * pk.wave(f, n, 0.05)),
              loc=(0, 0, -0.022 - 0.014 * b))''', '''        k.key("Spine", f, rot=(0.5 * pk.wave(f, n, 0.1, 2), 1.2 * pk.wave(f, n, 0.0), -2.0 * pk.wave(f, n, 0.25)),
              loc=(0, 0, -0.022 - 0.014 * b))              # rolls toward the planted side (left legs swing ~f35-f5)''')
rep('''        k.key("Head", f, rot=(1.5 * pk.wave(f, n, 0.18, 2), 1.5 * pk.wave(f, n, 0.3), 0))''',
    '''        k.key("Head", f, rot=(1.5 * pk.wave(f, n, 0.65, 2), 1.5 * pk.wave(f, n, 0.3), 0))   # dips 2 f after FL/FR touch''')
io.open(P, "w", encoding="utf-8").write(s)
print("ok")
