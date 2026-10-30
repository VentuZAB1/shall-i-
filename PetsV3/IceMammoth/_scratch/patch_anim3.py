import io
P = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\IceMammoth.py"
s = io.open(P, encoding="utf-8").read()
a = s.index("    (60, -13, -2, (-50, -52, -50, -40), 14, 0),      # follow-through drift")
b = s.index("    (95, 0, 0, (-2, -1, 0, 0), 14, 22),              # one tail flick")
new = '''    (59, -14, -2, (-51, -54, -52, -43), 14, 0),      # follow-through drift
    (66, 2, 1, (-10, 0, 6, 8), 8, 0),                # scoop 2 (smaller)
    (70, -6, -1, (-28, -24, -14, -4), 9, 0),
    (74, -10, -2, (-42, -42, -38, -28), 11, 0),      # flick 2: dust2
    (80, 1, 0, (-8, -2, 4, 8), 8, 0),                # scoop 3 (smaller)
    (83, -4, -1, (-24, -20, -12, -4), 8, 0),
    (86, -8, -1, (-38, -38, -32, -22), 9, 0),        # flick 3: dust3
    (92, -2, 0, (-12, -8, -6, -4), 6, 0),
'''
s = s[:a] + new + s[b:]
s = s.replace('''"scoop3": round(78 / n, 3)''', '''"scoop3": round(80 / n, 3)''')
io.open(P, "w", encoding="utf-8").write(s)
print("ok")
