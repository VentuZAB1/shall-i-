import runpy, collections
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
R3["full"]("BrambleBadger", save=False)
k = R3["STATE"]["k"]
body = k.main
names = {g.index: g.name for g in body.vertex_groups}
c = collections.Counter(); zmax = {}
for v in body.data.vertices:
    p = body.matrix_world @ v.co
    if 0.08 <= abs(p.x) < 0.16 and -0.36 < p.y < -0.28 and p.z > 0.40:
        o = names[max(v.groups, key=lambda g: g.weight).group] if len(v.groups) else None
        ws = tuple(sorted((names[g.group], round(g.weight, 2)) for g in v.groups))
        c[ws] += 1
        zmax[ws] = max(zmax.get(ws, 0), round(p.z, 3))
print("DBG", [(w, n, zmax[w]) for w, n in c.most_common(8)])
print("DBG verts", len(body.data.vertices), "objs", [o.name for o in k.coll.objects if o.type == "MESH"])
