# one-off patch: Abyss Weaver review 2 C1-C5 (roar thrum / rasp sines, act cast snap, one-segment flare, legs 1 land
# from above); C6 (optional draw target) not taken
import os
os.chdir(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3")
p = "pets/AbyssWeaver.py"
s = open(p, encoding="utf-8").read()
reps = [
    # C2: curve() with an "in" ease
    ('''def curve(keys, f):
    """smoothstep through (frame, value) keys"""
    for (f0, v0), (f1, v1) in zip(keys, keys[1:]):
        if f0 <= f <= f1:
            u = (f - f0) / float(f1 - f0) if f1 > f0 else 1.0
            return v0 + (v1 - v0) * u * u * (3 - 2 * u)
    return keys[-1][1] if f > keys[-1][0] else keys[0][1]''',
     '''def curve(keys, f):
    """smoothstep through (frame, value[, ease]) keys; a 3rd item "in" on a key = accelerate INTO it (u * u: a snap
    with a hard stop on that key - review 2 C2)"""
    for k0, k1 in zip(keys, keys[1:]):
        (f0, v0), (f1, v1) = k0[:2], k1[:2]
        if f0 <= f <= f1:
            u = (f - f0) / float(f1 - f0) if f1 > f0 else 1.0
            e = u * u if (len(k1) > 2 and k1[2] == "in") else u * u * (3 - 2 * u)
            return v0 + (v1 - v0) * e
    return keys[-1][1] if f > keys[-1][0] else keys[0][1]'''),
    # C1
    ('''        thrum = (2 if (f // 3) % 2 else -2) if 24 <= f <= 54 else 0''',
     '''        thrum = 2 * math.sin(2 * math.pi * (f - 24) / 6.0) if 24 <= f <= 54 else 0      # +-2 every 3 f (C1)'''),
    ('''        rasp = (7 if (f // 2) % 2 else -7) if 26 <= f <= 50 else 0''',
     '''        rasp = 7 * math.sin(2 * math.pi * (f - 26) / 4.0) if 26 <= f <= 50 else 0       # +-7, period 4 f (C1)'''),
    # C4
    ('''    unf = [(0, 0), (18, 0), (22, 45), (24, 65), (38, 65), (40, 53), (44, 65), (54, 65), (62, 0), (72, 0)]''',
     '''    unf = [(0, 0), (18, 0), (24, 65), (38, 65), (40, 53), (44, 65), (54, 65), (62, 0), (72, 0)]      # one segment (C4)'''),
    # C5
    ('''    plant8(k, list(range(0, 16)) + list(range(62, n + 1)), ["Leg2_L", "Leg2_R"])
    k.finish()
    k.events["roar"]''',
     '''    plant8(k, list(range(0, 16)) + list(range(62, n + 1)), ["Leg2_L", "Leg2_R"])
    k.bake_bezier_now()
    for leg in ("Leg1_L", "Leg1_R"):                 # C5: land from above: f64 over the spot, f65 just above, f66 planted
        foot = k.legs2[leg]["foot"]
        spot = k.J[foot].copy()
        bpy.context.scene.frame_set(64)
        fk64 = k.arm.matrix_world @ k.arm.pose.bones[foot].head
        for f, P in ((64, spot.lerp(fk64, 0.25) + Vector((0, 0, 0.10))), (65, spot + Vector((0, 0, 0.03)))):
            bpy.context.scene.frame_set(f)
            ankle_to(k, leg, f, P)
    k.finish()
    k.events["roar"]'''),
    # C2 + C3 act keys
    ('''    pc = [(0, 0), (12, 3), (24, -6), (74, -6), (80, 2), (96, 0), (120, 0)]
    ped = [(0, 0), (12, 0), (24, -4), (74, -4), (80, 2), (100, 0), (120, 0)]
    abd = [(0, 0), (12, 8), (18, 0), (24, -8), (74, -8), (77, 1), (80, 10), (92, -2), (100, 0), (120, 0)]''',
     '''    pc = [(0, 0), (12, 3), (24, -6), (74, -6), (80, 2, "in"), (96, 0), (120, 0)]          # C2: snap into f80
    ped = [(0, 0), (12, 0), (24, -4), (74, -4), (80, 2, "in"), (100, 0), (120, 0)]
    abd = [(0, 0), (12, 8), (24, -8), (74, -8), (80, 10, "in"), (92, -2), (100, 0), (120, 0)]    # C3: one swing'''),
]
for a, b in reps:
    assert s.count(a) == 1, a[:70]
    s = s.replace(a, b)
open(p, "w", encoding="utf-8").write(s)
print("C1-C5 ok")
