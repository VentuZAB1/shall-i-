# Permafrost Titan final-8.5 round 5 (_review/PermafrostTitan_final85_r5.md + coordinator rulings)
import io
p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\PermafrostTitan.py"
s = io.open(p, encoding="utf-8").read()
n_ok = 0


def rep(a, b):
    global s, n_ok
    c = s.count(a)
    assert c == 1, (c, a[:100])
    s = s.replace(a, b)
    n_ok += 1


# ---------------- MD1: skull half-width 0.160 -> 0.172 (x1.075); brow, eye, cheek, jaw, cavity, lip X x1.075
rep("""    skull = B.add((0, -0.245, 1.86), (0.160, 0.160, 0.135), MAUVE, "Head", top=(0.84, 0.86), rnd=0.30)   # f85 9+ 2""",
    """    skull = B.add((0, -0.245, 1.86), (0.172, 0.160, 0.135), MAUVE, "Head", top=(0.84, 0.86), rnd=0.30)   # r5 MD1: x 0.160 -> 0.172""")
rep("""        B.add((s * 0.148, -0.284, 1.812), (0.048, 0.090, 0.068), MAUVE, "Head", rot=(0, 0, s * 8), rnd=0.42)  # cheek""",
    """        B.add((s * 0.148 * HX, -0.284, 1.812), (0.048, 0.090, 0.068), MAUVE, "Head", rot=(0, 0, s * 8), rnd=0.42)  # cheek""")
rep("""        B.add(fp + fn * 0.010 + Vector((s * 0.070, 0, -0.001)), (0.076, 0.032, 0.028), JOINT_D, "Head", R=Rb,""",
    """        B.add(fp + fn * 0.010 + Vector((s * 0.070 * HX, 0, -0.001)), (0.076, 0.032, 0.028), JOINT_D, "Head", R=Rb,""")
rep("""        ep, en = surf_hit(B, [skull], (s * 0.078, -1.0, 1.858), (0, 1, 0))""",
    """        ep, en = surf_hit(B, [skull], (s * 0.078 * HX, -1.0, 1.858), (0, 1, 0))""")
rep("""    B.add((0, -0.295, 1.732), (0.120, 0.105, 0.046), MAUVE, "Jaw", top=(1.0, 0.95), bot=(0.84, 0.86), rnd=0.34)""",
    """    B.add((0, -0.295, 1.732), (0.120 * HX, 0.105, 0.046), MAUVE, "Jaw", top=(1.0, 0.95), bot=(0.84, 0.86), rnd=0.34)""")
# ---------------- MC4': cavity (10, 10, 14) + a 0.012 upper-lip overhang (Head) over the cavity
rep("""    B.add((0, -0.335, 1.707), (0.086, 0.040, 0.018), (24, 26, 34), "Head", studs=[], nostud=True, role="detail",  # r4 MC4
          rnd=0.2)                                                          # mouth cavity""",
    """    B.add((0, -0.335, 1.707), (0.086 * HX, 0.040, 0.018), (10, 10, 14), "Head", studs=[], nostud=True, role="detail",  # r5 MC4'
          rnd=0.2)                                                          # mouth cavity
    # r5 MC4': upper lip on the skull, 0.012 proud of the cavity front (y -0.375 -> -0.387), so the open mouth sits in
    # its shadow (hidden inside the closed jaw)
    B.add((0, -0.369, 1.725), (0.086 * HX + 0.006, 0.018, 0.009), MAUVE, "Head", studs=[], nostud=True, role="detail",
          rnd=0.35)                                                         # upper lip""")
rep("""    B.add((0, -0.399, 1.727), (0.088, 0.008, 0.0045), MOUTH, "Jaw", studs=[], role="detail", bevel=0.002)  # lip""",
    """    B.add((0, -0.399, 1.727), (0.088 * HX, 0.008, 0.0045), MOUTH, "Jaw", studs=[], role="detail", bevel=0.002)  # lip""")
# ---------------- MD2: crusts -> two solid plates (smallest half-size >= 0.06: w * 0.8 >= 0.06, L / 2 >= 0.06)
rep("""        for gx, L, tw in ((-0.080, 0.060, 0.040), (0.0, 0.072, 0.044), (0.080, 0.060, 0.040)):        # ice knuckles
            base = fist.world((gx * s, -0.112, 0.112))
            ice_chunk(B, base, fist.R @ Vector((gx * s * 0.8, -0.75, 0.7)), L, tw, hand, top=(0.80, 0.72))""",
    """        for gx, L, tw in ((-0.072, 0.120, 0.076), (0.072, 0.120, 0.076)):                              # r5 MD2: 2 plates
            base = fist.world((gx * s, -0.100, 0.100))
            ice_chunk(B, base, fist.R @ Vector((gx * s * 0.5, -0.80, 0.55)), L, tw, hand, top=(0.82, 0.74))""")
rep("""        for dx, dy, L, w, lean in ((0.05, -0.06, 0.18, 0.070, 0.40), (0.085, 0.085, 0.12, 0.058, 0.70),
                                   (-0.05, 0.05, 0.09, 0.052, -0.15)):                          # f85 9+ 3""",
    """        for dx, dy, L, w, lean in ((0.05, -0.07, 0.17, 0.080, 0.40), (-0.02, 0.08, 0.13, 0.076, 0.30)):  # r5 MD2: 2 plates""")
rep("""        ice_chunk(B, p2.world((0.0, -0.04, 0.12)), p2.R @ Vector((s * 0.35, -0.2, 1.0)), 0.10, 0.050, arm,""",
    """        ice_chunk(B, p2.world((0.0, -0.04, 0.12)), p2.R @ Vector((s * 0.35, -0.2, 1.0)), 0.12, 0.076, arm,   # r5 MD2""")
# HX constant
rep("""def ice_eye(B, c, s, n, bone="Head", tilt=20.0, sc=1.0, wx=1.0):""",
    """HX = 1.075                    # r5 MD1: skull width x1.075; the face X offsets follow
FORE_IDLE, FORE_WALK = 4.0, 6.0  # r5 MC2' / MC3': forearm bend amplitude (deg), opposite phase to the shoulder swing
YAW_K = 18.0                  # r5 MC1': whole-body yaw during the kneel (pivot = the planted right ankle)


def ice_eye(B, c, s, n, bone="Head", tilt=20.0, sc=1.0, wx=1.0):""")
# ---------------- idle: forearm bend +/-4 opposite the arm sway; 9+ K8c: one slow heavy head turn (look) f44-100
rep("""        k.key("Head", f, rot=(1.8 * br, -0.25 * yaw, 0))                    # the head stays level and forward""",
    """        look = curve([(0, 0), (44, 0), (60, 12), (84, 12), (100, 0), (120, 0)], f)   # r5 9+ (K8c): a slow heavy look
        k.key("Head", f, rot=(1.8 * br, -0.25 * yaw + look, 0))             # the head stays level""")
rep("""            k.key("Arm_" + side, f, rot=(-s_ * sway, 0, -s_ * curve(settle, f)))   # hip-yaw sine (the chest counter""",
    """            k.key("Arm_" + side, f, rot=(-s_ * sway, 0, -s_ * curve(settle, f)))   # hip-yaw sine (the chest counter
            k.key("Fore_" + side, f, rot=(-2.0 * br + s_ * FORE_IDLE * sn(f, n), 0, 0))  # r5 MC2': opposite phase""")
# ---------------- walk: forearm bend +/-6 opposite the arm swing (was 2); 9+: shoulder roll 1.5 -> 3 per step
rep("""            k.key("Fore_" + side, f, rot=(-3 - 2 * s * sn(f, n, 0.05), 0, 0))""",
    """            k.key("Fore_" + side, f, rot=(-3 - FORE_WALK * s * sn(f, n, 0.05), 0, 0))   # r5 MC3': +/-6 (was 2)""")
rep("""        k.key("Chest", f, rot=(0, -2 * sn(f, n, 0.0), -1.5 * sn(f, n, 0.0)))""",
    """        k.key("Chest", f, rot=(0, -2 * sn(f, n, 0.0), -3.0 * sn(f, n, 0.0)))   # r5 9+: shoulder roll 1.5 -> 3 per step""")
# ---------------- MC1': the kneel yaws the whole body YAW_K about the planted right ankle (ease f12-18, out by f62)
rep("""    for f in range(0, n + 1, 2):
        x = curve([(a[0], a[1]) for a in SP], f)
        y = curve([(a[0], a[2]) for a in SP], f)
        z = curve([(a[0], a[3]) for a in SP], f)
        k.key("Spine", f, rot=(curve([(a[0], a[4]) for a in SP], f), 0, curve(ROLL_S, f)), loc=(x, y, z))""",
    """    # r5 MC1' (lead ruling): yaw the WHOLE body (the Spine = the top exported bone; the kit never exports Root) by
    # YAW_K toward the L side about a vertical axis through the planted right ankle, so the game camera behind sees the
    # kneeling leg side-on. The foot targets rotate with it (the knee stays pinned, the right foot does not slide).
    PSI = [(0, 0), (12, 0), (18, YAW_K), (52, YAW_K), (62, 0), (100, 0)]
    PIV = k.J["Foot_R"] + STEP_R
    PIV = Vector((PIV.x, PIV.y, 0.0))
    O = Vector((k.J["Spine"].x, k.J["Spine"].y, 0.0))

    def rz(v, a):
        return Matrix.Rotation(math.radians(a), 3, "Z") @ Vector(v)
    for f in range(0, n + 1, 2):
        x = curve([(a[0], a[1]) for a in SP], f)
        y = curve([(a[0], a[2]) for a in SP], f)
        z = curve([(a[0], a[3]) for a in SP], f)
        psi = curve(PSI, f)
        loc = rz((x, y, z), psi) + (PIV - O) - rz(PIV - O, psi)
        k.key("Spine", f, rot=(curve([(a[0], a[4]) for a in SP], f), psi, curve(ROLL_S, f)), loc=tuple(loc))""")
rep("""    for f in range(0, n + 1):
        bpy.context.scene.frame_set(f)
        ankle_to(k, "Leg_R", f, vcurve(R, f), toe=curve(TR, f))
        ankle_to(k, "Leg_L", f, vcurve(L, f), toe=curve(TL, f), yaw=curve(YL, f))""",
    """    for f in range(0, n + 1):
        bpy.context.scene.frame_set(f)
        psi = curve(PSI, f)
        ankle_to(k, "Leg_R", f, PIV + rz(vcurve(R, f) - PIV, psi), toe=curve(TR, f))
        ankle_to(k, "Leg_L", f, PIV + rz(vcurve(L, f) - PIV, psi), toe=curve(TL, f), yaw=curve(YL, f) + psi)""")
io.open(p, "w", encoding="utf-8").write(s)
print("patched", n_ok)
