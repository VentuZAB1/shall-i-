import re
D = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets"
CH = {
    "PermafrostTitan": [
        ("MAUVE = (184, 150, 200)      # body: stone masses, pauldron bodies, head, limbs (studded)",
         "MAUVE = (150, 104, 176)      # body: stone masses, pauldron bodies, head, limbs (studded); plan (184,150,200)\n"
         "                             # deepened 2026-10-27 (same hue 278-281): the plan value read pastel next to\n"
         "                             # every approved pet in the 64 px strip"),
        ("PLUM = (124, 92, 150)        # armour plates",
         "PLUM = (96, 62, 124)         # armour plates"),
    ],
    "CinderOverlord": [
        ("PLUM_OBS = (182, 132, 172)   # body scales (studded)",
         "PLUM_OBS = (172, 104, 150)   # body scales (studded); plan (182,132,172) deepened (H 319, away from the\n"
         "                             # Cosmic Leviathan's H 300 magenta hide)"),
        ("OBS_D = (96, 84, 96)         # crown plates, brow ridges, dorsal spikes, scale bands",
         "OBS_D = (62, 50, 64)         # obsidian: crown plates, brow ridges, dorsal spikes, scale bands (plan 96,84,96)"),
    ],
    "CoralCrusher": [
        ("BRONZE = (196, 150, 104)     # carapace top, claw bodies (studded)",
         "BRONZE = (186, 124, 80)      # carapace top, claw bodies (studded); plan (196,150,104) deepened (H 25)"),
        ("SHELL_D = (132, 96, 66)      # legs, seams / ridges, claw knuckles, brow plate, fingertips",
         "SHELL_D = (100, 66, 46)      # legs, seams / ridges, claw knuckles, brow plate, fingertips (plan 132,96,66)"),
    ],
}
for pet, reps in CH.items():
    p = D + "\\" + pet + ".py"
    t = open(p, encoding="utf-8").read()
    for a, b in reps:
        if a not in t:
            print("MISSING", pet, a[:60])
        t = t.replace(a, b)
    open(p, "w", encoding="utf-8").write(t)
print("ok")
