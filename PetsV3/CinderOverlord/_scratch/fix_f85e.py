# f85: docstrings carry the new numbers (molt C1, idle T3)
import io
p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\CinderOverlord.py"
s = io.open(p, encoding="utf-8").read()


def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:80])
    s = s.replace(a, b)


rep('''    """THE CROWN SHEDS (plan; refs #9 + U1): the neck arches 25 deg with the head level; the blades lift one by one
    35 deg (2-frame lag, `lift1` f22); the centre blade lifts furthest and holds while the outer blades drop back
    (`lift2` f48, `shed` f56); a ripple runs along the body (tail -> head, 6 deg per bone, 3-bone lag); the blades
    reseat in reverse order, slower; exact rest."""''',
    '''    """THE CROWN SHEDS (plan; refs #9 + U1): the neck arches 22.5 deg with the head level; from f12 the blades lift one
    by one (3-frame lag; f85 C1: the four outer blades 45 deg and fan out like a crest, the centre 35; blade 1 is fully
    up at `lift1` f22); the centre blade rises to 40 and holds while the outer blades drop back (`lift2` f48, `shed`
    f56); a ripple runs along the body (tail -> head, 6 deg per bone, 3-bone lag); the blades reseat in reverse order,
    slower than they rose (centre f84-100, outers by f108); exact rest."""''')
rep('''    """EMBER BREATHING (plan; refs S2 C1/C2): two slow breaths - the neck rises and sinks back with the head held near
    level, a slow sway, the vents smoke on each breath; one quick tail flick at f80."""''',
    '''    """EMBER BREATHING (plan; refs S2 C1/C2): two slow breaths - the neck rises 3 deg per bone (f85 T3, was 2) and
    sinks back with the head held near level, a slow sway, the vents smoke on each breath; one quick tail flick at f80."""''')
io.open(p, "w", encoding="utf-8").write(s)
print("ok")
