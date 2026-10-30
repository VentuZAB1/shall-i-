import io, os
D = os.path.dirname(os.path.abspath(__file__))
P = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\IceMammoth.py"
s = io.open(P, encoding="utf-8").read()


def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:70])
    s = s.replace(a, b)


rep('''    k.joint("Tail3", TAILP[2], "Tail2", tail=(0, 0.01, -0.2))


def check_pairs():''', '''    k.joint("Tail3", TAILP[2], "Tail2", tail=(0, 0.01, -0.2))
    # VFX anchors (plan section 8): bones without mesh, parented to the bone that carries the effect
    k.joint("FX_SnowSpray", tuple(HX(Vector(TRUNK_TIP) + Vector((0, -0.04, 0.0)))), "Trunk_Tip", tail=(0, -0.08, 0))
    for s, side in ((1, "L"), (-1, "R")):
        k.joint("FX_TuskSparkle_" + side, tuple(HX(tusk_pts(s)[4])), "Tusk_" + side, tail=(0, 0, 0.06))
    k.joint("FX_FrostPuff", (0, -0.30, 1.62), "Back", tail=(0, 0, 0.1))
    k.joint("FX_IceCrack", (0.25, -0.49, 0.02), "Foot_FL", tail=(0, -0.1, 0))
    k.joint("FX_BreathCloud", tuple(HX((0, -1.34, 0.95))), "Breath", tail=(0, -0.1, 0))


def check_pairs():''')
block = io.open(os.path.join(D, "anim_block.py"), encoding="utf-8").read()
rep("HEAD_XF = []\n", block)
io.open(P, "w", encoding="utf-8").write(s)
print("ok")
