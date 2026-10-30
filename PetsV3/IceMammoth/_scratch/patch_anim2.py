import io
P = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\IceMammoth.py"
s = io.open(P, encoding="utf-8").read()


def rep(a, b, cnt=1):
    global s
    assert s.count(a) == cnt, (s.count(a), a[:70])
    s = s.replace(a, b)


# throat hinge: the skull's lower back corner and the chest bib meet at the head pivot (slivers only)
rep('''    P += [("Trunk3", "Trunk1"), ("Trunk4", "Trunk1"), ("Trunk4", "Trunk2"), ("Head", "Shin_FL"), ("Head", "Shin_FR")]
    return P
''', '''    P += [("Trunk3", "Trunk1"), ("Trunk4", "Trunk1"), ("Trunk4", "Trunk2"), ("Head", "Shin_FL"), ("Head", "Shin_FR")]
    return P


def joints():
    """throat hinge carried by the Head: the skull's lower back corner meets the chest bib at the pivot"""
    return [((-0.24, -0.88, 1.03), (0.24, -0.88, 1.03), 0.09, "Head")]
''')


# head lift = neck stretches forward / up + head pitch (keeps the wool dome off the hump)
rep('''def bell(f, c, w):''', '''def neck_lift(hd):
    """neck offset that goes with a head pitch-up of -hd deg: the neck reaches forward and up so the back of the
    wool dome clears the shoulder hump"""
    u = max(0.0, -hd) / 15.0
    return (0, -0.05 * u, 0.045 * u)


def bell(f, c, w):''')
rep('''        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))''', '''        k.key("Neck", f, rot=(nk, 0, 0), loc=neck_lift(hd + nk))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))''')
rep('''        k.key("Neck", f, rot=(nk, 0, 0))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(2 if hd < -8 else 0, 0, 0))''', '''        k.key("Neck", f, rot=(nk, 0, 0), loc=neck_lift(hd + nk))
        k.key("Head", f, rot=(hd, 0, 0))
        k.key("Jaw", f, rot=(2 if hd < -8 else 0, 0, 0))''')
# roar: head -13 + neck -2 (= 15 up)
rep('''    (16, -0.010, -0.6, -2, -10, 2, (-34, -24, -20, -12), 30, 8),
    (22, -0.010, -1.0, -3, -15, 8, (-50, -35, -30, -25), 42, 14),
    (26, -0.010, -1.0, -3, -15, 14, (-52, -37, -32, -30), 45, 16),
    (50, -0.010, -1.0, -3, -15, 13, (-52, -37, -32, -30), 45, 16),''', '''    (16, -0.010, -0.6, -2, -9, 2, (-34, -24, -20, -12), 30, 8),
    (22, -0.010, -1.0, -2, -13, 8, (-50, -35, -30, -25), 42, 14),
    (26, -0.010, -1.0, -2, -13, 14, (-52, -37, -32, -30), 45, 16),
    (50, -0.010, -1.0, -2, -13, 13, (-52, -37, -32, -30), 45, 16),''')
io.open(P, "w", encoding="utf-8").write(s)
print("ok")
