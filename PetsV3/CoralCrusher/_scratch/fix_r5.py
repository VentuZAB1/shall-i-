# review 4 NICE pass: 8-f held tops, 5-f down-strokes, act stays 120 f (time comes out of the rest tail), events on the
# hold centres; the act is keyed every frame so the odd-frame troughs land exactly
import io, shutil
P = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\CoralCrusher.py"
shutil.copy(P, r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\CoralCrusher\_scratch\CoralCrusher_r4.py")
t = io.open(P, encoding="utf-8").read()
a = t.index("def act_semaphore(k):")
b = t.index("def anim(k):")
NEW = '''def act_semaphore(k):
    """THE FIDDLER WAVE (plan; refs F1-F3 + the site refs S1 / S2 in ANIM_REFS.md): stand tall, the crusher unfolds up and
    waves three slow display arcs. Each top is HELD 8 f (f26-34 / f49-57 / f72-80, hold centres f30 / f53 / f76), the
    down-stroke takes 5 f (S2 H3: the drop is quick) and the up-sweep 10 f (H1, F3). Then the claw points out and holds
    while the cutter taps twice (f90 / f96), swings in, then folds down (f96-110); exact rest f110-120. Legs planted
    every frame."""
    n = 120
    k.new_action("act_semaphore", n, False)
    up = [(0, 0), (18, 1), (98, 1), (110, 0), (120, 0)]
    # the wave: top = the claw raised high (F1), held 8 f; trough = swung down and forward in front (F2, f39 / f62):
    # merus 16 <-> 40, spread 6 <-> 34, carpus -12 <-> 10, palm -40 <-> -6 deg; 10 f up, 5 f down (review 4 NICE 1-2)
    HOLD, DOWN, UP = 8, 5, 10
    TOPS = (26, 26 + HOLD + DOWN + UP, 26 + 2 * (HOLD + DOWN + UP))         # 26, 49, 72
    TROUGHS = tuple(t0 + HOLD + DOWN for t0 in TOPS[:2])                    # 39, 62

    def wave_keys(top, low, first, end):
        ks = [(0, 0), (18, first)]
        for i, t0 in enumerate(TOPS):
            ks += [(t0, top), (t0 + HOLD, top)]
            if i < len(TROUGHS):
                ks.append((TROUGHS[i], low))
        return ks + end

    lift_r = wave_keys(40, 16, 30, [(86, 38), (96, 38), (103, 30), (110, 0), (120, 0)])
    spread_r = wave_keys(34, 6, 30, [(86, 44), (96, 44), (103, 10), (110, 0), (120, 0)])  # in first, then down
    fore_r = wave_keys(10, -12, 0, [(86, 0), (120, 0)])
    wrist_r = wave_keys(-6, -40, -10, [(86, 0), (120, 0)])                     # the palm swings down at the trough
    pin_r = [(0, 0), (18, 10), (80, 10), (86, 2), (106, 0), (120, 0)]
    tap_l = [(0, 0), (18, -6), (86, -6), (88, 6), (90, -6), (94, 6), (96, -6), (102, -6), (110, 0), (120, 0)]
    for f in range(0, n + 1):
        u = curve(up, f)
        body(k, f, up=0.10 * u, pitch=-5 * u, roll=-2 * u)                          # review 3 N2: stand taller
        claw(k, f, "R", lift=curve(lift_r, f), spread=curve(spread_r, f), fore=curve(fore_r, f),
             wrist=curve(wrist_r, f), pinch=curve(pin_r, f))
        claw(k, f, "L", lift=curve(tap_l, f))
        eyes(k, f, up=6 * u, r=-8 * u)
        k.key("Mouth", f, rot=(0, 0, 0))
    plant6(k, range(0, n + 1))
    k.finish(loop=False)
    k.events["act_semaphore"] = {"wave1": round(30 / n, 3), "wave2": round(53 / n, 3), "wave3": round(76 / n, 3),
                                 "tap1": round(90 / n, 3), "tap2": round(96 / n, 3)}


'''
t = t[:a] + NEW + t[b:]
io.open(P, "w", encoding="utf-8", newline="\n").write(t)
print("ok")
