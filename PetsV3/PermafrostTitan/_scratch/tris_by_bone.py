# blender -b --factory-startup --python PermafrostTitan/_scratch/tris_by_bone.py -- <Name>
# model-only build (one 200 px view) -> triangle count of the body mesh per owning bone (majority vertex group)
import sys, runpy, json
argv = sys.argv[sys.argv.index("--") + 1:]
name = argv[0]
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
R3["full"](name, save=False)
k = R3["STATE"]["k"]
me = k.main.data
vg = {g.index: g.name for g in k.main.vertex_groups}
own = [vg.get(max(v.groups, key=lambda g: g.weight).group, "?") if v.groups else "?" for v in me.vertices]
cnt = {}
for pl in me.polygons:
    c = {}
    for i in pl.vertices:
        c[own[i]] = c.get(own[i], 0) + 1
    b = max(c, key=c.get)
    cnt[b] = cnt.get(b, 0) + len(pl.vertices) - 2
print("TRIS " + json.dumps({"total": sum(cnt.values()), "by_bone": dict(sorted(cnt.items()))}))
