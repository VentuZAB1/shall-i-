# Reviewer: where are the stretched-UV faces on the stone / mound (blades excluded)?
import bpy, bmesh, os, math, json
import numpy as np
res = {}
for n in ["Grave_A", "Grave_B", "Grave_C"]:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.fbx(filepath=os.path.join(r"C:\cdimp", "Halloween_" + n + ".fbx"))
    ob = [o for o in bpy.context.scene.objects if o.type == "MESH"][0]
    bm = bmesh.new(); bm.from_mesh(ob.data); bm.faces.ensure_lookup_table()
    uvl = bm.loops.layers.uv.active
    seen = set(); comps = []
    for f in bm.faces:
        if f.index in seen: continue
        st = [f]; comp = []; seen.add(f.index)
        while st:
            g = st.pop(); comp.append(g)
            for e in g.edges:
                for h in e.link_faces:
                    if h.index not in seen: seen.add(h.index); st.append(h)
        comps.append(comp)
    big = [c for c in comps if len(c) > 40]
    out = []
    for c in big:
        A = []; dens = []; an = []; cen = []
        for f in c:
            P = [l.vert.co for l in f.loops]; U = [l[uvl].uv for l in f.loops]
            for i in range(1, len(P) - 1):
                e1, e2 = P[i] - P[0], P[i + 1] - P[0]; f1, f2 = U[i] - U[0], U[i + 1] - U[0]
                det = f1.x * f2.y - f1.y * f2.x; a3 = e1.cross(e2).length / 2
                if a3 < 1e-8 or abs(det) < 1e-12: continue
                dPu = (e1 * f2.y - e2 * f1.y) / det; dPv = (e2 * f1.x - e1 * f2.x) / det
                s = np.linalg.svd(np.array([[dPu.x, dPv.x], [dPu.y, dPv.y], [dPu.z, dPv.z]]), compute_uv=False)
                A.append(a3); an.append(s[0] / max(s[1], 1e-9)); dens.append(512.0 / math.sqrt(s[0] * s[1]))
                cen.append(tuple(f.calc_center_median()))
        A = np.array(A); an = np.array(an); dens = np.array(dens); cen = np.array(cen)
        w = A / A.sum()
        bad = an > 2.5
        info = {"faces": len(c), "area": round(float(A.sum()), 2), "aniso_gt2.5_area_frac": round(float(w[bad].sum()), 4),
                "px_per_stud_pcts(5,50,95)": [round(float(np.percentile(dens, q)), 1) for q in (5, 50, 95)]}
        if bad.any():
            cb = cen[bad]; wb = A[bad]
            # cluster summary: bins by region
            info["bad_area"] = round(float(wb.sum()), 3)
            info["bad_centroid_mean_xyz"] = [round(float(v), 2) for v in (cb * wb[:, None]).sum(0) / wb.sum()]
            info["bad_bbox"] = [[round(float(v), 2) for v in cb.min(0)], [round(float(v), 2) for v in cb.max(0)]]
            # top 8 worst by area*aniso
            idx = np.argsort(-(A * (an > 2.5) * an))[:8]
            info["worst"] = [{"c": [round(float(v), 2) for v in cen[i]], "aniso": round(float(an[i]), 1), "area": round(float(A[i]), 4)} for i in idx if an[i] > 2.5]
        out.append(info)
    res[n] = out
print(json.dumps(res, indent=1))
with open(os.path.join(os.path.dirname(__file__), "stretch.json"), "w") as fh:
    json.dump(res, fh, indent=1)
