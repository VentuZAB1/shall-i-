# Reviewer: blade segmentation / bend angles in the dead grass FBX (and the grave clumps).
import bpy, bmesh, os, math, json
import numpy as np
out = {}
for n in ["Halloween_DeadGrass_A", "Halloween_DeadGrass_B", "Halloween_Grave_C"]:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.fbx(filepath=os.path.join(r"C:\cdimp", n + ".fbx"))
    ob = [o for o in bpy.context.scene.objects if o.type == "MESH"][0]
    bm = bmesh.new(); bm.from_mesh(ob.data); bm.faces.ensure_lookup_table()
    # connected components by edges
    seen = set(); comps = []
    for f in bm.faces:
        if f.index in seen: continue
        st = [f]; comp = []; seen.add(f.index)
        while st:
            g = st.pop(); comp.append(g)
            for e in g.edges:
                for h in e.link_faces:
                    if h.index not in seen:
                        seen.add(h.index); st.append(h)
        comps.append(comp)
    sizes = sorted(len(c) for c in comps)
    # bend: for each component of <= 20 faces (blade strip), angle between adjacent face normals across shared edges
    bends = []; maxb = []; lens = []
    for c in comps:
        if len(c) > 30: continue
        ids = {f.index for f in c}
        mb = 0
        for f in c:
            for e in f.edges:
                for h in e.link_faces:
                    if h.index in ids and h.index > f.index:
                        a = math.degrees(f.normal.angle(h.normal, 0))
                        bends.append(a); mb = max(mb, a)
        maxb.append(mb)
        vs = {v for f in c for v in f.verts}
        zs = [v.co.z for v in vs]
        lens.append((max(zs) - min(zs)))
    bends = np.array(bends); maxb = np.array(maxb)
    out[n] = {"components": len(comps), "comp_face_sizes_hist": {str(k): sizes.count(k) for k in sorted(set(sizes)) if k <= 40},
              "big_components": [s for s in sizes if s > 40],
              "bend_deg_pcts(50,75,90,95,99)": [round(float(np.percentile(bends, q)), 1) for q in (50, 75, 90, 95, 99)] if len(bends) else None,
              "frac_adjacent_faces_bend_gt_20": float((bends > 20).mean()) if len(bends) else None,
              "frac_blades_with_max_bend_gt_30": float((maxb > 30).mean()) if len(maxb) else None,
              "blade_strips": int(len(maxb))}
print(json.dumps(out, indent=1))
with open(os.path.join(os.path.dirname(__file__), "grasscheck_round2.json"), "w") as fh:
    json.dump(out, fh, indent=1)
