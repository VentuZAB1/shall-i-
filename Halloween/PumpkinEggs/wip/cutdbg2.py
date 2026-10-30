import sys
sys.path.insert(0, r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween\PumpkinEggs")
from eggs import *
key = sys.argv[sys.argv.index("--") + 1]
E = EGGS[key]; P = E["P"]
fresh(8)
pl = PAL[E["pal"]]
skin, inner_m, flesh = mat_vc("Skin"), mat_inner(), mat_flesh()
Pi = inner_params(P, E["shell"])
outl = {k: clean(v) for k, v in E["face"]().items()}
def shell():
    return build_mesh("S", [sphere_surface(egg_field(dict(P, micro=0.0), pl), E["useg"][1], E["vseg"][1]) + (0, 1.0),
                            sphere_surface(egg_field(Pi, pl), E["iuseg"][1], E["ivseg"][1], flip=True) + (1, 0.0)], [skin, inner_m])
s0 = shell()
bm = bmesh.new(); bm.from_mesh(s0.data)
print("SHELL nonmanifold", sum(1 for e in bm.edges if not e.is_manifold), "vol", round(bm.calc_volume(signed=True), 3),
      "faces", len(bm.faces))
# self-intersection test via BVH
from mathutils.bvhtree import BVHTree
tree = BVHTree.FromBMesh(bm)
pairs = tree.overlap(tree)
bm.faces.ensure_lookup_table()
bad = [(a, b) for a, b in pairs if a != b and not (set(v.index for v in bm.faces[a].verts) & set(v.index for v in bm.faces[b].verts))]
print("SHELL self-overlapping face pairs", len(bad))
if bad:
    import collections
    zs = [bm.faces[a].calc_center_median() for a, b in bad[:20]]
    print("SAMPLE", [tuple(round(c, 2) for c in z) for z in zs[:8]], "mats", collections.Counter((bm.faces[a].material_index, bm.faces[b].material_index) for a, b in bad))
bm.free()
for k, v in outl.items():
    s = shell()
    cut = cutter_planar("C_" + k, {k: v}, P["R"], P["Rz"], flesh, egg=P["egg"])
    n0 = len(s.data.polygons)
    carve2(s, cut)
    print("BOOL", k, "faces", n0, "->", len(s.data.polygons), "holes", euler_holes(s))
