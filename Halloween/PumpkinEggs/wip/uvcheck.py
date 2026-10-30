import bpy, bmesh, sys, math
from collections import defaultdict
path, name = sys.argv[sys.argv.index("--") + 1:][:2]
bpy.ops.wm.open_mainfile(filepath=path)
ob = bpy.data.objects[name]
me = ob.data
bm = bmesh.new(); bm.from_mesh(me)
uvl = bm.loops.layers.uv.active
# islands via shared UV coords on edges
parent = list(range(len(bm.faces)))
def find(a):
    while parent[a] != a:
        parent[a] = parent[parent[a]]; a = parent[a]
    return a
bm.faces.ensure_lookup_table()
for e in bm.edges:
    lf = e.link_faces
    if len(lf) != 2: continue
    f0, f1 = lf
    def uvs(f):
        d = {}
        for l in f.loops: d[l.vert.index] = l[uvl].uv.copy()
        return d
    a, b = uvs(f0), uvs(f1)
    ok = all((a[v.index] - b[v.index]).length < 1e-5 for v in e.verts)
    if ok: parent[find(f0.index)] = find(f1.index)
isl = defaultdict(list)
for f in bm.faces: isl[find(f.index)].append(f)
names = [m.name for m in ob.material_slots and [s.material for s in ob.material_slots]]
print("islands", len(isl))
rows = []
for k, fs in isl.items():
    a3 = sum(f.calc_area() for f in fs)
    a2 = 0
    for f in fs:
        uv = [l[uvl].uv for l in f.loops]
        s = 0
        for i in range(len(uv)):
            x1, y1 = uv[i]; x2, y2 = uv[(i + 1) % len(uv)]
            s += x1 * y2 - x2 * y1
        a2 += abs(s) / 2
    mats = sorted({f.material_index for f in fs})
    rows.append((a3, a2, len(fs), mats))
rows.sort(reverse=True)
for r in [r for r in rows if not (0.0040 < r[1] / max(r[0], 1e-9) < 0.0046)]:
    print("3D %.3f  UV %.5f  ratio %.4f  faces %d  mats %s" % (r[0], r[1], r[1] / max(r[0], 1e-9), r[2], r[3]))
