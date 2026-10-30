p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\PermafrostTitan.py"
s = open(p, encoding="utf-8").read()
a = '''    """WEIGHT SHIFT (plan): hip yaw +/-3 deg over one cycle, two slow breaths, the shoulders (pauldrons) settle 2 deg at
    f30 and f70, core pulses f40 / f100. No head tilt (the head stays level and forward). Feet planted."""'''
b = '''    """WEIGHT SHIFT (plan, f85 MUST 5): hip yaw +/-4 deg over one cycle, two breaths (chest 2 deg, the body sinks
    0.015), the shoulders (pauldrons) settle 2 deg at f30 and f70, a slow +/-8 deg fist flex (60 f, the fists offset),
    core pulses f40 / f100. No head tilt (the head stays level and forward). Feet planted."""'''
c = '''    """CORE BELLOW (plan; refs #3 + #9): lean in and tuck (anticipation), then the head lifts 10 deg and the arms go out
    8 deg; the jaw opens late; the core pulses f22 / f34; hold to f50; a slower settle."""'''
d = '''    """CORE BELLOW (plan; refs #3 + #9; f85 MUST 4): lean in and tuck (anticipation), then the body pushes forward
    (Spine -4, Chest -3 local = -7 world), the head lifts 15 deg and the arms go out 22 deg (24 at f34); the jaw opens
    late (24 deg at f27); the core pulses f22 / f34; hold to f50; a slower settle."""'''
assert s.count(a) == 1 and s.count(c) == 1
s = s.replace(a, b).replace(c, d)
open(p, "w", encoding="utf-8").write(s)
print("ok")
