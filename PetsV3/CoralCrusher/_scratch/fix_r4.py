# review 3 (round 4): M2 the wave re-timed to 3 slow display arcs with top holds (act 120 f), N2 stand taller,
# N3 roar claws lift 30
import io, shutil
P = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\CoralCrusher.py"
shutil.copy(P, r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\CoralCrusher\_scratch\CoralCrusher_r3.py")
t = io.open(P, encoding="utf-8").read()

a = t.index("def act_semaphore(k):")
b = t.index("def anim(k):")
NEW = '''def act_semaphore(k):
    """THE FIDDLER WAVE (plan; refs F1-F3 + the site refs in ANIM_REFS.md): stand tall, the crusher unfolds up and waves
    three SLOW display arcs (review 3 M2): each top is held 4 f (peaks f28 / f50 / f72), the up-sweep takes 10 f and the
    return 8 f (slow up, quicker down, F3); then the claw points out and holds while the cutter taps twice (f84 / f90),
    swings in, then folds down (f90-104); exact rest f104-120. Legs planted every frame."""
    n = 120
    k.new_action("act_semaphore", n, False)
    up = [(0, 0), (18, 1), (92, 1), (104, 0), (120, 0)]
    lift_r = [(0, 0), (18, 45), (74, 45), (80, 32), (90, 32), (97, 28), (104, 0), (120, 0)]
    fore_r = [(0, 0), (18, 12), (26, 44), (30, 44), (38, 6), (48, 44), (52, 44), (60, 6), (70, 44), (74, 44),
              (80, 0), (120, 0)]
    spread_r = [(0, 0), (18, 30), (74, 30), (80, 44), (90, 44), (97, 10), (104, 0), (120, 0)]   # in first, then down
    wrist_r = [(0, 0), (18, -10), (74, -10), (80, 0), (120, 0)]
    pin_r = [(0, 0), (18, 10), (74, 10), (80, 2), (100, 0), (120, 0)]
    tap_l = [(0, 0), (18, -6), (80, -6), (82, 6), (84, -6), (88, 6), (90, -6), (96, -6), (104, 0), (120, 0)]
    for f in range(0, n + 1, 2):
        u = curve(up, f)
        body(k, f, up=0.10 * u, pitch=-5 * u, roll=-2 * u)                          # review 3 N2: stand taller
        claw(k, f, "R", lift=curve(lift_r, f), spread=curve(spread_r, f), fore=curve(fore_r, f),
             wrist=curve(wrist_r, f), pinch=curve(pin_r, f))
        claw(k, f, "L", lift=curve(tap_l, f))
        eyes(k, f, up=6 * u, r=-8 * u)
        k.key("Mouth", f, rot=(0, 0, 0))
    plant6(k, range(0, n + 1))
    k.finish(loop=False)
    k.events["act_semaphore"] = {"wave1": round(28 / n, 3), "wave2": round(50 / n, 3), "wave3": round(72 / n, 3),
                                 "tap1": round(84 / n, 3), "tap2": round(90 / n, 3)}


'''
t = t[:a] + NEW + t[b:]

old = "lift = [(0, 0), (4, -4), (14, 25), (40, 25), (52, 0), (60, 0)]"
assert old in t
t = t.replace(old, "lift = [(0, 0), (4, -4), (14, 30), (40, 30), (52, 0), (60, 0)]            # review 3 N3: 25 -> 30")
old = "three clacks (cocked open 2 f -> snap shut 2 f -> hard stop)"
assert old in t
t = t.replace("    \"\"\"CLACK THREAT (plan; refs #6 + #5): a short crouch, the body rises 0.05 H and both claws lift forward 25 deg;",
              "    \"\"\"CLACK THREAT (plan; refs #6 + #5): a short crouch, the body rises 0.05 H and both claws lift forward 30 deg;")
io.open(P, "w", encoding="utf-8", newline="\n").write(t)
print("ok")
