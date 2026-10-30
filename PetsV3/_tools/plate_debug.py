import sys, runpy, json
argv = sys.argv[sys.argv.index("--") + 1:]
name = argv[0]
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
bk = R3["blockkit"]
B0 = bk.Blocks
orig = B0._studs_for
log = []
def wrapped(self, blk, bm, L):
    c0 = self.stud_count
    faces = self._plate_faces(blk) if blk._role != "detail" else []
    info = []
    for P, n in faces:
        lu = ((P[1] - P[0]).length + (P[2] - P[3]).length) / 2
        lv = ((P[3] - P[0]).length + (P[2] - P[1]).length) / 2
        margin = blk._off + bk.STYLE["plate_margin"] * self.pcell
        info.append((round(lu, 2), round(lv, 2), round(margin, 3)))
    orig(self, blk, bm, L)
    log.append((blk.bone, blk._role, [round(v, 2) for v in blk.h], self.stud_count - c0, info))
B0._studs_for = wrapped
m = R3["spec"](name)
k = R3["new_pet"](m, name)
m.model(k)
for row in log:
    if row[1] != "detail":
        print("DBG", row)
