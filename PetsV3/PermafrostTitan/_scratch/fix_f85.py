# Titan final 8.5 gate (`_review/PermafrostTitan_final85.md`): MUST 1-6 + the TO-9+ items 1-5
import io, shutil
P = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\PermafrostTitan.py"
shutil.copy(P, r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\PermafrostTitan\_scratch\PermafrostTitan_exported1.py")
t = io.open(P, encoding="utf-8").read()
R = []
# ---- MUST 1 colour
R.append(("MAUVE = (146, 101, 178)     # body:", "MAUVE = (164, 116, 200)     # f85 MUST 1 (was 146,101,178) body:"))
R.append(("PLUM = (86, 56, 112)         # armour plates:", "PLUM = (98, 66, 130)         # f85 MUST 1 (was 86,56,112) armour plates:"))
# ---- ice_eye: a width factor (9+ item 2: slits 15 % wider)
R.append(('def ice_eye(B, c, s, n, bone="Head", tilt=20.0, sc=1.0):',
          'def ice_eye(B, c, s, n, bone="Head", tilt=20.0, sc=1.0, wx=1.0):'))
R.append(("    B.add(c, (0.060 * sc, 0.008, 0.030 * sc), JOINT_D, bone, bevel=0.005, top=(0.78, 1.0), **kw)   # socket",
          "    B.add(c, (0.060 * sc * wx, 0.008, 0.030 * sc), JOINT_D, bone, bevel=0.005, top=(0.78, 1.0), **kw)   # socket"))
R.append(("    B.add(c + nn * 0.006 + R @ Vector((0, 0, -0.004)), (0.047 * sc, 0.006, 0.0105 * sc), ICE_W, bone,",
          "    B.add(c + nn * 0.006 + R @ Vector((0, 0, -0.004)), (0.047 * sc * wx, 0.006, 0.0105 * sc), ICE_W, bone,"))
# ---- ice_chunk: optional top taper (9+ item 3: flat-topped blunt blocks)
R.append(("def ice_chunk(B, base, d, L, w, bone, side=(1, 0, 0), color=None):",
          "def ice_chunk(B, base, d, L, w, bone, side=(1, 0, 0), color=None, top=(0.62, 0.48)):"))
R.append(("                 top=(0.62, 0.48), nostud=True, role=\"limb\", rnd=0.10)",
          "                 top=top, nostud=True, role=\"limb\", rnd=0.10)"))
# ---- 9+ item 5: pale ICE_W belly band on the waist front (smooth)
R.append(("    B.add((0, 0.02, 1.10), (0.262, 0.19, 0.08), MAUVE, \"Spine\", bot=(0.95, 0.95), top=(1.08, 1.06), rnd=0.36)\n",
          "    B.add((0, 0.02, 1.10), (0.262, 0.19, 0.08), MAUVE, \"Spine\", bot=(0.95, 0.95), top=(1.08, 1.06), rnd=0.36)\n"
          "    B.add((0, -0.176, 1.098), (0.20, 0.016, 0.036), ICE_W, \"Spine\", top=(1.06, 1.0), nostud=True, role=\"limb\",\n"
          "          rnd=0.30)                                                         # f85 9+ 5: pale belly band\n"))
# ---- 9+ item 1: bigger chest hero
R.append(("    R_OUT, R_IN, DEPTH, PROUD = 0.240, 0.150, 0.10, 0.045              # r2 NICE 2: outer 0.225 -> 0.240",
          "    R_OUT, R_IN, DEPTH, PROUD = 0.265, 0.160, 0.10, 0.045              # f85 9+ 1: outer 0.240 -> 0.265"))
R.append(("        p1 = rc + rad * (R_OUT + 0.06) - rn * 0.012\n",
          "        p1 = rc + rad * (R_OUT + 0.045) - rn * 0.012                   # f85: shorter settings (bigger ring)\n"))
R.append(("            for a in [2 * math.pi * (j + 0.5) / 8 for j in range(8)]], 0.032, ICE_W, \"Chest\")      # octagon ice disc",
          "            for a in [2 * math.pi * (j + 0.5) / 8 for j in range(8)]], 0.032, ICE_W, \"Chest\")      # octagon ice disc"))
R.append(("            for a in [2 * math.pi * (j + 0.5) / 8 for j in range(8)]], 0.032, ICE_W, \"Chest\")",
          "            for a in [2 * math.pi * (j + 0.5) / 8 for j in range(8)]], 0.032, ICE_W, \"Chest\")"))
# ---- 9+ item 2: bigger head, raised 0.02
R.append(("    skull = B.add((0, -0.235, 1.84), (0.145, 0.150, 0.128), MAUVE, \"Head\", top=(0.84, 0.86), rnd=0.30)\n"
          "    B.add((0, -0.20, 1.962), (0.112, 0.112, 0.032), PLUM, \"Head\", top=(0.8, 0.8), rnd=0.42)            # crown cap\n"
          "    for s in (1, -1):\n"
          "        B.add((s * 0.134, -0.272, 1.795), (0.045, 0.085, 0.065), MAUVE, \"Head\", rot=(0, 0, s * 8), rnd=0.42)  # cheek\n"
          "    fp, fn = surf_hit(B, [skull], (0, -1.0, 1.87), (0, 1, 0))",
          "    skull = B.add((0, -0.245, 1.86), (0.160, 0.160, 0.135), MAUVE, \"Head\", top=(0.84, 0.86), rnd=0.30)   # f85 9+ 2\n"
          "    B.add((0, -0.21, 1.99), (0.122, 0.120, 0.032), PLUM, \"Head\", top=(0.8, 0.8), rnd=0.42)             # crown cap\n"
          "    for s in (1, -1):\n"
          "        B.add((s * 0.148, -0.284, 1.812), (0.048, 0.090, 0.068), MAUVE, \"Head\", rot=(0, 0, s * 8), rnd=0.42)  # cheek\n"
          "    fp, fn = surf_hit(B, [skull], (0, -1.0, 1.89), (0, 1, 0))"))
R.append(("        ep, en = surf_hit(B, [skull], (s * 0.072, -1.0, 1.838), (0, 1, 0))\n"
          "        ice_eye(B, ep + en * 0.003, s, en, tilt=20, sc=0.95)",
          "        ep, en = surf_hit(B, [skull], (s * 0.078, -1.0, 1.858), (0, 1, 0))\n"
          "        ice_eye(B, ep + en * 0.003, s, en, tilt=20, sc=0.95, wx=1.15)"))
# ---- MUST 3: jaw shows - the mouth slit rides the Jaw, a dark cavity on Head behind it
R.append(("    B.add((0, -0.384, 1.762), (0.088, 0.008, 0.0045), MOUTH, \"Head\", studs=[], role=\"detail\", bevel=0.002)",
          "    B.add((0, -0.372, 1.758), (0.086, 0.024, 0.030), JOINT_D, \"Head\", studs=[], nostud=True, role=\"detail\",\n"
          "          rnd=0.2)                                                          # f85 MUST 3: mouth cavity\n"
          "    B.add((0, -0.398, 1.773), (0.088, 0.008, 0.0045), MOUTH, \"Jaw\", studs=[], role=\"detail\", bevel=0.002)  # lip"))
# ---- MUST 2: limbs taper toward the joint below; deltoid rounder
R.append(("        B.add(Sv + Vector((s * 0.03, 0.0, -0.01)), (0.155, 0.165, 0.150), MAUVE, arm, rnd=0.45)        # deltoid",
          "        B.add(Sv + Vector((s * 0.03, 0.0, -0.01)), (0.155, 0.165, 0.150), MAUVE, arm, rnd=0.55)        # deltoid"))
R.append(("        B.seg(Ev, Wv, 0.130, 0.140, MAUVE, fore, ext=0.02, ext1=0.0, top=(1.12, 1.10), rnd=0.38)      # forearm",
          "        B.seg(Ev, Wv, 0.140, 0.148, MAUVE, fore, ext=0.02, ext1=0.0, top=(0.82, 0.82), rnd=0.40)      # forearm (f85)"))
R.append(("        br = B.seg(Ev + de * 0.11, Wv - de * 0.06, 0.150, 0.158, PLUM, fore, top=(1.07, 1.05), rnd=0.40)  # bracer",
          "        br = B.seg(Ev + de * 0.11, Wv - de * 0.06, 0.156, 0.164, PLUM, fore, top=(0.88, 0.88), rnd=0.42)  # bracer"))
R.append(("        B.seg(H + Vector((0, 0.0, 0.07)), K, 0.165, 0.180, MAUVE, leg, ext=0.0, ext1=0.02, top=(0.86, 0.84),",
          "        B.seg(H + Vector((0, 0.0, 0.07)), K, 0.172, 0.186, MAUVE, leg, ext=0.0, ext1=0.02, top=(0.80, 0.80),"))
R.append(("        B.seg(K, A, 0.143, 0.152, MAUVE, shin, ext=0.0, ext1=0.0, top=(1.14, 1.12), rnd=0.38)          # pillar shin",
          "        B.seg(K, A, 0.150, 0.158, MAUVE, shin, ext=0.0, ext1=0.0, top=(0.84, 0.84), rnd=0.40)          # shin (f85 taper)"))
R.append(("        B.seg(K + Vector((0, -0.128, -0.085)), A + Vector((0, -0.150, 0.07)), 0.116, 0.028, PLUM, shin,\n"
          "              top=(1.15, 1.0), rnd=0.40)",
          "        B.seg(K + Vector((0, -0.134, -0.085)), A + Vector((0, -0.128, 0.07)), 0.116, 0.028, PLUM, shin,\n"
          "              top=(0.86, 1.0), rnd=0.40)"))
# ---- 9+ item 4: short fingers and ice knuckles (no teeth read)
R.append(("            B.add(fist.world((gx * s, -0.155, -0.042)), (0.027, 0.032, 0.058), MAUVE, hand, R=fist.R, rnd=0.55)",
          "            B.add(fist.world((gx * s, -0.152, -0.030)), (0.027, 0.032, 0.035), MAUVE, hand, R=fist.R, rnd=0.55)"))
R.append(("        for gx, L, tw in ((-0.080, 0.090, 0.040), (0.0, 0.112, 0.044), (0.080, 0.090, 0.040)):        # ice knuckles",
          "        for gx, L, tw in ((-0.080, 0.060, 0.040), (0.0, 0.072, 0.044), (0.080, 0.060, 0.040)):        # ice knuckles"))
R.append(("            ice_chunk(B, base, fist.R @ Vector((gx * s * 0.8, -0.75, 0.7)), L, tw, hand)",
          "            ice_chunk(B, base, fist.R @ Vector((gx * s * 0.8, -0.75, 0.7)), L, tw, hand, top=(0.80, 0.72))"))
# ---- 9+ item 3: blunt, flat-topped ice blocks at the pauldron tips (~0.18 tall, no points)
R.append(("        for dx, dy, L, w, lean in ((0.05, -0.06, 0.13, 0.062, 0.45), (0.085, 0.085, 0.095, 0.052, 0.75),\n"
          "                                   (-0.05, 0.05, 0.075, 0.048, -0.15)):\n"
          "            ice_chunk(B, p1.world((s * dx, dy, 0.10)), p1.R @ Vector((s * lean, dy * 0.8, 1.0)), L, w, arm)",
          "        for dx, dy, L, w, lean in ((0.05, -0.06, 0.18, 0.070, 0.40), (0.085, 0.085, 0.12, 0.058, 0.70),\n"
          "                                   (-0.05, 0.05, 0.09, 0.052, -0.15)):                          # f85 9+ 3\n"
          "            ice_chunk(B, p1.world((s * dx, dy, 0.10)), p1.R @ Vector((s * lean, dy * 0.8, 1.0)), L, w, arm,\n"
          "                      top=(0.86, 0.80))                                                        # flat tops"))
R.append(("        ice_chunk(B, p2.world((0.0, -0.04, 0.12)), p2.R @ Vector((s * 0.35, -0.2, 1.0)), 0.085, 0.048, arm)",
          "        ice_chunk(B, p2.world((0.0, -0.04, 0.12)), p2.R @ Vector((s * 0.35, -0.2, 1.0)), 0.10, 0.050, arm,\n"
          "                  top=(0.86, 0.80))"))
# ---- MUST 5: idle life
R.append(("        yaw = 3 * sn(f, n)\n"
          "        br = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)\n"
          "        k.key(\"Spine\", f, rot=(0, yaw, 0), loc=(0, 0, -0.005 * br))\n"
          "        k.key(\"Chest\", f, rot=(-1.0 * br, -0.4 * yaw, 0))\n"
          "        k.key(\"Head\", f, rot=(1.0 * br, -0.6 * yaw, 0))\n"
          "        k.key(\"Jaw\", f, rot=(0, 0, 0))\n"
          "        arms_fk(k, f, out=curve(settle, f), bend=1.0 * br)",
          "        yaw = 4 * sn(f, n)                                                   # f85 MUST 5: 3 -> 4 deg\n"
          "        br = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)\n"
          "        k.key(\"Spine\", f, rot=(0, yaw, 0), loc=(0, 0, -0.015 * br))         # breath sink 0.005 -> 0.015\n"
          "        k.key(\"Chest\", f, rot=(-2.0 * br, -0.4 * yaw, 0))                   # breath 1 -> 2 deg\n"
          "        k.key(\"Head\", f, rot=(2.0 * br, -0.6 * yaw, 0))                     # the head stays level\n"
          "        k.key(\"Jaw\", f, rot=(0, 0, 0))\n"
          "        arms_fk(k, f, out=curve(settle, f), bend=2.0 * br)\n"
          "        for s, side in ((1, \"L\"), (-1, \"R\")):                             # f85: slow +/-8 deg fist flex\n"
          "            k.key(\"Hand_\" + side, f, rot=(8 * sn(f, 60, 0.25 if s > 0 else 0.0), 0, 0))"))
# ---- MUST 4: the roar reads (world: spine -4, chest -7 = local -3, head -15 local; arms out 22-24)
R.append(("        (22, 0.010, -1, -3, -10, 8, 8),\n"
          "        (27, 0.010, -1, -3, -10, 16, 8),\n"
          "        (34, 0.014, -1.5, -3.5, -10, 15, 9),\n"
          "        (50, 0.010, -1, -3, -9, 14, 8),\n"
          "        (58, 0.0, 0, -0.5, -2, 4, 3),",
          "        (22, 0.010, -4, -3, -15, 8, 22),                                     # f85 MUST 4\n"
          "        (27, 0.010, -4, -3, -15, 16, 22),\n"
          "        (34, 0.014, -4, -3, -15, 15, 24),\n"
          "        (50, 0.010, -3.5, -3, -14, 14, 22),\n"
          "        (58, 0.0, -1, -1, -4, 4, 10),"))
# ---- MUST 6: kneel - elbow bend 8 more in the hold, Foot_R 10 deg outward f18-50
R.append(("    ARM = [(0, 0, 0, 0), (18, 4, 14, 22), (30, 4, 14, 26), (50, 4, 14, 26), (62, 2, 6, 8), (80, 0, 0, 0), (100, 0, 0, 0)]",
          "    ARM = [(0, 0, 0, 0), (18, 4, 14, 22), (30, 4, 14, 30), (50, 4, 14, 30), (62, 2, 6, 8), (80, 0, 0, 0), (100, 0, 0, 0)]"))
R.append(("        ankle_to(k, \"Leg_R\", f, vcurve(R, f), toe=curve(TR, f))",
          "        ankle_to(k, \"Leg_R\", f, vcurve(R, f), toe=curve(TR, f), yaw=curve(YR, f))"))
R.append(("    TR = [(0, 0), (6, 0), (18, 26), (52, 26), (62, 18), (70, 6), (76, 0), (100, 0)]",
          "    TR = [(0, 0), (6, 0), (18, 26), (52, 26), (62, 18), (70, 6), (76, 0), (100, 0)]\n"
          "    YR = [(0, 0), (10, 0), (18, -10), (50, -10), (62, -4), (72, 0), (100, 0)]   # f85 MUST 6: right foot 10 deg out"))
R.append(("def ankle_to(k, leg, f, A, toe=0.0):\n"
          "    \"\"\"IK: put the ankle of `leg` at world point A; toe = foot pitch (deg, + = toes down)\"\"\"\n"
          "    foot = k.legs2[leg][\"foot\"]\n"
          "    hipR, ankR = k.J[leg], k.J[foot]\n"
          "    k.solve_leg(leg, f, Vector((A.x - (ankR.x - hipR.x), A.y - (ankR.y - hipR.y), A.z - ankR.z)), toe=toe)",
          "def ankle_to(k, leg, f, A, toe=0.0, yaw=0.0):\n"
          "    \"\"\"IK: put the ankle of `leg` at world point A; toe = foot pitch (deg, + = toes down); yaw = foot turn about Z\n"
          "    (deg, + = toes toward +x)\"\"\"\n"
          "    from mathutils import Quaternion\n"
          "    foot = k.legs2[leg][\"foot\"]\n"
          "    hipR, ankR = k.J[leg], k.J[foot]\n"
          "    k.solve_leg(leg, f, Vector((A.x - (ankR.x - hipR.x), A.y - (ankR.y - hipR.y), A.z - ankR.z)), toe=toe)\n"
          "    if yaw:\n"
          "        k._aim(foot, f, Quaternion((0, 0, 1), math.radians(yaw)) @ Quaternion((1, 0, 0), math.radians(toe)))"))
for a, b in R:
    if a == b:
        continue
    assert a in t, a[:90]
    t = t.replace(a, b, 1)
io.open(P, "w", encoding="utf-8", newline="\n").write(t)
print("ok", len(R))
