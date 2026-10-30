import io
p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\PermafrostTitan\ANIM_REFS.md"
t = io.open(p, encoding="utf-8").read()
SEC = open(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\PermafrostTitan\_scratch\refs_k8.md", encoding="utf-8").read()
assert "## C. Kaiju No. 8" not in t
t = t.replace("## How each clip uses them\n", SEC + "\n## How each clip uses them\n")
fixes = [
    ("`icedust` f22 on the fists);", "`icedust` f24 on the fists);"),
    ("f50-66 the forward lean (K3, chest 10 deg) then the front leg drives up; f66-84 the left foot steps back to rest;",
     "f50-58 the forward lean (K3, spine 10 deg + chest 4) then the front leg drives up (f58-76); f70-79 the left foot steps back;"),
]
for a, b in fixes:
    assert a in t, a
    t = t.replace(a, b)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("ok")
