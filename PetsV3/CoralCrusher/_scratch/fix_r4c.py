# r4c: the wave arcs UP AND OUT to the side (F1, the fiddler's display) and back DOWN AND IN in front (F2):
# the merus lift and the spread rise together; the held top is the claw high and out at the side.
import io
P = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\CoralCrusher.py"
t = io.open(P, encoding="utf-8").read()
a = t.index("    lift_r = [(0, 0), (18, 40)")
b = t.index("    wrist_r = [(0, 0), (18, -10)")
NEW = '''    # the wave (review 3 M2): top = up and OUT at the side, held 4 f (f26-30 / f48-52 / f70-74, peaks f28 / f50 /
    # f72); trough = down and IN in front (f38 / f60); 10 f up-sweep, 8 f return (slow up, quicker down, F3)
    TOPS, TROUGHS = (26, 48, 70), (38, 60)

    def wave_keys(rest, top, low, first, end):
        ks = [(0, 0), (18, first)]
        for i, t0 in enumerate(TOPS):
            ks += [(t0, top), (t0 + 4, top)]
            if i < len(TROUGHS):
                ks.append((TROUGHS[i], low))
        return ks + end

    lift_r = wave_keys(0, 48, 24, 36, [(80, 32), (90, 32), (97, 28), (104, 0), (120, 0)])
    spread_r = wave_keys(0, 62, 12, 30, [(80, 44), (90, 44), (97, 10), (104, 0), (120, 0)])   # in first, then down
    fore_r = wave_keys(0, 10, -4, 6, [(80, 0), (120, 0)])
'''
t = t[:a] + NEW + t[b:]
io.open(P, "w", encoding="utf-8", newline="\n").write(t)
print("ok")
