import io, os
D = os.path.dirname(os.path.abspath(__file__))
P = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\GlacierYeti.py"
s = io.open(P, encoding="utf-8").read()


def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:70])
    s = s.replace(a, b)


rep('''        k.add_leg2("Leg_" + side, "Shin_" + side, "Foot_" + side, knee=(0, -1, 0))


def check_pairs():''', '''        k.add_leg2("Leg_" + side, "Shin_" + side, "Foot_" + side, knee=(0, -1, 0))
        # VFX anchors (plan section 8): bones without mesh
        k.joint("FX_ShardBurst_" + side, tuple(X(FIST, s) + Vector((0, -0.10, -0.08))), "Hand_" + side,
                tail=(0, -0.1, 0))
        k.joint("FX_AuroraDust_" + side, tuple(Sv + Vector((s * 0.20, 0, 0.12))), "Plate_" + side, tail=(s * 0.1, 0, 0))
    k.joint("FX_SnowPuff", (0, -0.30, 0.95), "Chest", tail=(0, -0.1, 0))
    k.joint("FX_BreathCloud", (0, -0.84, 1.37), "Mouth", tail=(0, -0.1, 0))


def check_pairs():''')
rep('''         ("Jaw", "Chest")]''', '''         ("Jaw", "Chest"), ("Plate_L", "Head"), ("Plate_R", "Head")]''')
block = io.open(os.path.join(D, "anim_block.py"), encoding="utf-8").read()
rep("HEAD_XF = []\n", block)
io.open(P, "w", encoding="utf-8").write(s)
print("ok")
