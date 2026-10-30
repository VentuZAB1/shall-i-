# blender -b --factory-startup --python CoralCrusher/_scratch/normals_check.py -- <Name>
# Flipped-face check: splits every mesh into connected islands; for each island compares each face normal with the
# direction from the island centroid to the face centre. Reports islands with > 2 % inward-facing area (likely
# inside-out parts) + the global count. Convex parts should be ~0 %.
import sys, runpy, json
argv = sys.argv[sys.argv.index("--") + 1:]
name = argv[0]
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
R3["model"](name, views=("tq",), res=120)
k = R3["STATE"]["k"]
import bpy, bmesh
from mathutils import Vector
out = {"islands": 0, "flagged": []}
for o in k.coll.objects:
    if o.type != "MESH":
        continue
    bm = bmesh.new()
    bm.from_mesh(o.data)
    bm.faces.ensure_lookup_table()
    seen = set()
    col = o.data.color_attributes.active_color if o.data.color_attributes else None
    for f0 in bm.faces:
        if f0.index in seen:
            continue
        stack, isl = [f0], []
        seen.add(f0.index)
        while stack:
            f = stack.pop()
            isl.append(f)
            for e in f.edges:
                for g in e.link_faces:
                    if g.index not in seen:
                        seen.add(g.index)
                        stack.append(g)
        out["islands"] += 1
        A = sum(f.calc_area() for f in isl)
        if A <= 0:
            continue
        c = sum((f.calc_center_median() * f.calc_area() for f in isl), Vector()) / A
        bad = sum(f.calc_area() for f in isl if (f.calc_center_median() - c).dot(f.normal) < -1e-6)
        if bad / A > 0.02:
            mw = o.matrix_world
            out["flagged"].append({"obj": o.name, "faces": len(isl), "inward_pct": round(100 * bad / A, 1),
                                   "centre": [round(v, 3) for v in (mw @ c)]})
    bm.free()
out["flagged"].sort(key=lambda d: -d["inward_pct"])
out["n_flagged"] = len(out["flagged"])
out["flagged"] = out["flagged"][:40]
print("NORMALS_RESULT " + json.dumps(out))
