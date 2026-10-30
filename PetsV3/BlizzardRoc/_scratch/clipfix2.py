# clip pass 2: walk knee clear of the belly (lower lift, wider pass, smaller dip), walk claws >= -0.02, idle re-grip
p = "pets/BlizzardRoc.py"
s = open(p, encoding="utf-8").read()


def rep(a, b, cnt=1):
    global s
    assert s.count(a) == cnt, (s.count(a), a[:90])
    s = s.replace(a, b)


rep("        T = Vector(T) + Vector((sx * 0.04 * min(1.0, lift / 0.05), 0, FOOT_LIFT))",
    "        T = Vector(T) + Vector((sx * 0.06 * min(1.0, lift / 0.05), 0, FOOT_LIFT + 0.004))")
rep("        return cm.biped_walk(k, n, 0.15, 0.07, body, legs=((\"Leg_L\", 0.0), (\"Leg_R\", 0.5)), duty=0.6)",
    "        return cm.biped_walk(k, n, 0.15, 0.06, body, legs=((\"Leg_L\", 0.0), (\"Leg_R\", 0.5)), duty=0.6)")
rep("            return -0.03 * (u * u * (3 - 2 * u))", "            return -0.02 * (u * u * (3 - 2 * u))")
rep("        return -0.03 * (1 - u * u * (3 - 2 * u))", "        return -0.02 * (1 - u * u * (3 - 2 * u))")
rep("                z, toe = FOOT_LIFT + 0.04 * math.sin(math.pi * u), 14 * math.sin(math.pi * u)",
    "                z, toe = FOOT_LIFT + 0.06 * math.sin(math.pi * u), 8 * math.sin(math.pi * u)")
open(p, "w", encoding="utf-8").write(s)
print("ok")
