p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\CinderOverlord.py"
t = open(p, encoding="utf-8").read()
rep = [
# nostrils: small dark pits on TOP of the snout tip (no eye read from the front)
("""        B.add((s * 0.046, -1.05, 1.665), (0.022, 0.010, 0.009), BLACK, "Head", rot=(0, -s * 25, -s * 20),
              studs=[], role="detail", bevel=0.003)                                     # nostril slits""",
 """        B.add((s * 0.040, -0.995, 1.712), (0.014, 0.020, 0.008), BLACK, "Head", rot=(-28, 0, s * 18),
              studs=[], role="detail", bevel=0.003)                                     # nostril pits (on top)
        for z, dz, L, w in ((1.60, -0.35, 0.15, 0.040), (1.67, -0.05, 0.18, 0.044), (1.74, 0.25, 0.13, 0.036)):
            B.spike((s * 0.20, -0.53, z), (s * 0.55, 0.85, dz), L, w, OBS_D, "Head", top=(0.12, 0.35))  # cheek spikes"""),
# eyes further forward, facing more forward; brows lifted off the eye
("""        ep, en = surf_hit(B, [skull], (s * 0.6, -0.74, 1.725), (-s, 0, 0))
        en = (en + Vector((0, -0.75, 0))).normalized()""",
 """        ep, en = surf_hit(B, [skull], (s * 0.6, -0.80, 1.722), (-s, 0, 0))
        en = (en + Vector((0, -1.1, 0.15))).normalized()"""),
("""        B.add(ep + en * 0.028 + Vector((0, 0, 0.048)), (0.112, 0.042, 0.032), OBS_D, "Head", R=Rb, role="limb",
              rnd=0.2, studs=[], nostud=True)                                                   # heavy brow""",
 """        B.add(ep + en * 0.020 + Vector((0, 0, 0.056)), (0.108, 0.036, 0.030), OBS_D, "Head", R=Rb, role="limb",
              rnd=0.2, studs=[], nostud=True)                                                   # heavy brow"""),
]
for a, b in rep:
    if a not in t:
        print("MISSING", a[:80])
    t = t.replace(a, b)
open(p, "w", encoding="utf-8").write(t)
print("ok")
