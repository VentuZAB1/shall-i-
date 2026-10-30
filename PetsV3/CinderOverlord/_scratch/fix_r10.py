# Cinder Overlord final-8.5 round 10 (_review/CinderOverlord_final85_r10.md + coordinator)
import io
p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\CinderOverlord.py"
s = io.open(p, encoding="utf-8").read()
n_ok = 0


def rep(a, b):
    global s
    global n_ok
    c = s.count(a)
    assert c == 1, (c, a[:100])
    s = s.replace(a, b)
    n_ok += 1


# MUST 1a: bigger clawed paws (box 0.052 x 0.046 x 0.042 -> 0.070 x 0.062 x 0.056, claws 0.075 / 0.015 -> 0.110 / 0.020),
# the forearm segments a touch thicker so the bigger paw does not sit on a stick
rep("""        B.seg(sh, el, 0.054, 0.060, PLUM_OBS, "Arm_" + side, ext=0.03, ext1=0.02, top=(0.9, 0.9), rnd=0.4)
        B.seg(el, ha, 0.048, 0.052, OBS_D, "Claw_" + side, ext=0.02, ext1=0.02, top=(0.9, 0.9), rnd=0.4)
        B.add(ha, (0.052, 0.046, 0.042), OBS_D, "Claw_" + side, rnd=0.4)
        for gx in (-0.03, 0.0, 0.03):
            B.spike(ha + Vector((gx, -0.03, -0.01)), (gx * 2.5, -0.7, -0.9), 0.075, 0.015, BLACK, "Claw_" + side)""",
    """        B.seg(sh, el, PAW_ARM[0], PAW_ARM[1], PLUM_OBS, "Arm_" + side, ext=0.03, ext1=0.02, top=(0.9, 0.9), rnd=0.4)
        B.seg(el, ha, PAW_ARM[2], PAW_ARM[3], OBS_D, "Claw_" + side, ext=0.02, ext1=0.02, top=(0.9, 0.9), rnd=0.4)
        B.add(ha, PAW_BOX, OBS_D, "Claw_" + side, rnd=0.4)           # r10 MUST 1a (r9 0.052 x 0.046 x 0.042)
        for gx in (-PAW_GX, 0.0, PAW_GX):                                # r10 MUST 1a: claws 0.075 / 0.015 -> 0.110 / 0.020
            B.spike(ha + Vector((gx, -PAW_BOX[1] + 0.016, -0.014)), (gx * 2.5, -0.7, -0.9), PAW_CLAW[0], PAW_CLAW[1],
                    BLACK, "Claw_" + side)""")
rep("""HEAD_WX = 1.15              # r9 MUST 1b""",
    """PAW_BOX = (0.070, 0.062, 0.056)        # r10 MUST 1a: paw half-size (r9 0.052, 0.046, 0.042)
PAW_CLAW = (0.110, 0.020)              # r10 MUST 1a: claw spike length / half-width (r9 0.075 / 0.015)
PAW_GX = 0.042                         # claw spacing across the wider paw (r9 0.03)
PAW_ARM = (0.060, 0.066, 0.056, 0.060)  # r10: upper arm / forearm segment widths (r9 0.054, 0.060, 0.048, 0.052)
# r10 MUST 1b: swept-back obsidian skull FRILL, one pair per side on the rear skull above the cheek spikes:
# (base x, y, z), (dir x, y, z), length, half-width - built at head scale 1.0 (then x1.15 wide, x1.45 HEAD_XF)
FRILL = (((0.150, -0.470, 1.790), (0.80, 0.56, 0.28), 0.22, 0.050),
         ((0.165, -0.465, 1.715), (0.86, 0.50, 0.04), 0.17, 0.045))
HEAD_WX = 1.15              # r9 MUST 1b""")
# MUST 1b: the frill (same B.spike call as the cheek spikes)
rep("""            B.spike((s * 0.20, -0.53, z), (s * 0.55, 0.85, dz), L, w, OBS_D, "Head", top=(0.12, 0.35))  # cheek spikes""",
    """            B.spike((s * 0.20, -0.53, z), (s * 0.55, 0.85, dz), L, w, OBS_D, "Head", top=(0.12, 0.35))  # cheek spikes
        for (bx, by, bz), (dx, dy, dz), L, w in FRILL:                  # r10 MUST 1b: swept-back skull frill
            B.spike((s * bx, by, bz), (s * dx, dy, dz), L, w, OBS_D, "Head", top=(0.12, 0.35))""")
# MUST 2: one taper nose -> chin: jaw tip 0.046 / 0.020 -> 0.034 / 0.016, the 0.85 station 0.098 -> 0.078
rep("""(0.85, 0.098, 0.032, 0.0),   # r9 MUST 2: rh 0.040 -> 0.032, tip 0.02 back""",
    """(0.85, 0.078, 0.032, 0.0),   # r10 MUST 2: rw 0.098 -> 0.078 (r9: rh 0.040 -> 0.032, tip 0.02 back)""")
rep("""(1.0, 0.046, 0.020, 0.0)), PLUM_OBS, "Jaw", n=2.8)  # r5-r9 T-b: tip flatter / narrower""",
    """(1.0, 0.034, 0.016, 0.0)), PLUM_OBS, "Jaw", n=2.8)  # r10 MUST 2: tip 0.046 / 0.020 -> 0.034 / 0.016 (< nose 0.044)""")
# the lower fangs follow the narrower jaw rim (x 0.075 -> 0.064) so they stay on it, not outside it
rep("""        B.spike(jp((s * 0.075, -0.37, 0.012)), JR @ Vector((0, -0.12, 1)), 0.12, 0.025, IVORY, "Jaw", nostud=True)""",
    """        B.spike(jp((s * 0.064, -0.37, 0.012)), JR @ Vector((0, -0.12, 1)), 0.12, 0.025, IVORY, "Jaw", nostud=True)  # r10: on the narrower rim (was 0.075)""")
io.open(p, "w", encoding="utf-8").write(s)
print("patched", n_ok)
