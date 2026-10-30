# Reviewer: save the FBX-embedded textures + UV stretch / texel-density stats.
# blender -b --factory-startup --python uvtex.py
import bpy, os, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TEX = os.path.join(HERE, "tex" + os.environ.get("REVIEW_TAG", ""))
os.makedirs(TEX, exist_ok=True)
FBX = [r"C:\cdimp\Halloween_Bush_Thorn.fbx", r"C:\cdimp\Halloween_Bush_Autumn.fbx", r"C:\cdimp\Halloween_Bramble.fbx"]
out = {}
for path in FBX:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.fbx(filepath=path)
    done = set()
    for img in bpy.data.images:
        base = img.name.split(".")[0]
        if base in done or img.size[0] == 0:
            continue
        done.add(base)
        cp = img.copy()
        cp.filepath_raw = os.path.join(TEX, base + ".png")
        cp.file_format = "PNG"
        cp.save()
    rec = {}
    for ob in bpy.context.scene.objects:
        if ob.type != "MESH":
            continue
        me = ob.data
        me.calc_loop_triangles()
        size = 1024
        for m in me.materials:
            for n in m.node_tree.nodes:
                if n.type == "TEX_IMAGE" and n.image and n.image.size[0]:
                    size = n.image.size[0]
                    break
        uv = me.uv_layers.active.data
        co = np.array([v.co[:] for v in me.vertices]) * 100.0 * np.array(ob.scale[:])  # studs
        dens, aniso, areas = [], [], []
        for t in me.loop_triangles:
            p = co[list(t.vertices)]
            q = np.array([uv[l].uv[:] for l in t.loops]) * size
            e1, e2 = p[1] - p[0], p[2] - p[0]
            a3 = np.linalg.norm(np.cross(e1, e2)) / 2
            f1, f2 = q[1] - q[0], q[2] - q[0]
            a2 = abs(f1[0] * f2[1] - f1[1] * f2[0]) / 2
            if a3 < 1e-9:
                continue
            areas.append(a3)
            if a2 < 1e-9:
                dens.append(0.0); aniso.append(99.0)
                continue
            dens.append(np.sqrt(a2 / a3))
            # Jacobian 3D (in tri plane) -> UV px
            n = np.cross(e1, e2); n /= np.linalg.norm(n)
            ex = e1 / np.linalg.norm(e1); ey = np.cross(n, ex)
            P = np.array([[e1 @ ex, e2 @ ex], [e1 @ ey, e2 @ ey]])
            Q = np.array([[f1[0], f2[0]], [f1[1], f2[1]]])
            J = Q @ np.linalg.inv(P)
            s = np.linalg.svd(J, compute_uv=False)
            aniso.append(float(s[0] / max(s[1], 1e-9)))
        dens = np.array(dens); aniso = np.array(aniso); areas = np.array(areas)
        w = areas / areas.sum()
        order = np.argsort(dens)
        cdf = np.cumsum(w[order])
        pct = lambda p: float(dens[order][np.searchsorted(cdf, p)])
        rec[ob.name] = {
            "tex_size": size,
            "px_per_stud_p10_p50_p90": [round(pct(0.1), 1), round(pct(0.5), 1), round(pct(0.9), 1)],
            "area_frac_aniso_gt2": round(float(w[aniso > 2].sum()), 3),
            "area_frac_aniso_gt3": round(float(w[aniso > 3].sum()), 3),
            "area_frac_zero_uv": round(float(w[dens == 0].sum()), 4),
        }
    out[os.path.basename(path)] = rec
with open(os.path.join(HERE, "uv_report" + os.environ.get("REVIEW_TAG", "") + ".json"), "w") as f:
    json.dump(out, f, indent=1)
print(json.dumps(out, indent=1))
