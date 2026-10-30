# Reviewer: texture + UV analysis of the imported FBX (alpha, black patches, value ranges, UV stretch).
import bpy, os, json, math
import numpy as np
from mathutils import Vector
names = ["Halloween_Grave_A", "Halloween_Grave_B", "Halloween_Grave_C", "Halloween_DeadGrass_A", "Halloween_DeadGrass_B"]
out = {}
D = os.path.dirname(__file__)
def s2l(x): return np.where(x <= 0.04045, x/12.92, ((x+0.055)/1.055)**2.4)
for n in names:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.fbx(filepath=os.path.join(r"C:\cdimp", n + ".fbx"))
    ob = [o for o in bpy.context.scene.objects if o.type == "MESH"][0]
    me = ob.data
    rec = {}
    # UV coverage mask
    uv = me.uv_layers.active.data
    me.calc_loop_triangles()
    R = 512
    cover = np.zeros((R, R), bool)
    ratios = []; aniso = []; areas = []
    uvmin = [9, 9]; uvmax = [-9, -9]
    for t in me.loop_triangles:
        P = [me.vertices[i].co * 1.0 for i in t.vertices]  # raw coords (studs)
        U = [Vector(uv[l].uv) for l in t.loops]
        for u in U:
            uvmin = [min(uvmin[0], u.x), min(uvmin[1], u.y)]; uvmax = [max(uvmax[0], u.x), max(uvmax[1], u.y)]
        e1, e2 = P[1] - P[0], P[2] - P[0]
        a3 = e1.cross(e2).length / 2
        f1, f2 = U[1] - U[0], U[2] - U[0]
        a2 = abs(f1.x * f2.y - f1.y * f2.x) / 2
        if a3 < 1e-9:
            continue
        areas.append(a3)
        ratios.append(math.sqrt(a2 / a3) if a2 > 0 else 0)
        # anisotropy: jacobian 3D per UV
        det = f1.x * f2.y - f1.y * f2.x
        if abs(det) < 1e-12:
            aniso.append(99); continue
        # dP/du, dP/dv
        dPu = (e1 * f2.y - e2 * f1.y) / det
        dPv = (e2 * f1.x - e1 * f2.x) / det
        M = np.array([[dPu.x, dPv.x], [dPu.y, dPv.y], [dPu.z, dPv.z]])
        s = np.linalg.svd(M, compute_uv=False)
        aniso.append(float(s[0] / max(s[1], 1e-9)))
        # rasterise coverage (bbox approx with barycentric test)
        xs = [u.x * R for u in U]; ys = [u.y * R for u in U]
        x0, x1 = int(max(0, math.floor(min(xs)))), int(min(R - 1, math.ceil(max(xs))))
        y0, y1 = int(max(0, math.floor(min(ys)))), int(min(R - 1, math.ceil(max(ys))))
        if x1 - x0 > 200 or y1 - y0 > 200:
            pass
        gx, gy = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
        (ax, ay), (bx, by), (cx, cy) = (xs[0], ys[0]), (xs[1], ys[1]), (xs[2], ys[2])
        d = (by - cy) * (ax - cx) + (cx - bx) * (ay - cy)
        if abs(d) < 1e-12: continue
        l1 = ((by - cy) * (gx - cx) + (cx - bx) * (gy - cy)) / d
        l2 = ((cy - ay) * (gx - cx) + (ax - cx) * (gy - cy)) / d
        l3 = 1 - l1 - l2
        m = (l1 >= -0.01) & (l2 >= -0.01) & (l3 >= -0.01)
        cover[y0:y1 + 1, x0:x1 + 1] |= m
    areas = np.array(areas); ratios = np.array(ratios); aniso = np.array(aniso)
    w = areas / areas.sum()
    med = float(np.median(ratios[ratios > 0]))
    rec["uv_bounds"] = [uvmin, uvmax]
    rec["uv_coverage_frac"] = float(cover.mean())
    rec["texel_ratio_median_px_per_stud"] = med * R
    rec["area_frac_texel_lt_half_median"] = float(w[ratios < 0.5 * med].sum())
    rec["area_frac_texel_gt_2x_median"] = float(w[ratios > 2 * med].sum())
    rec["area_frac_aniso_gt_2"] = float(w[aniso > 2].sum())
    rec["area_frac_aniso_gt_4"] = float(w[aniso > 4].sum())
    # images
    mat = me.materials[0]
    for nd in mat.node_tree.nodes:
        if nd.type != "TEX_IMAGE": continue
        im = nd.image
        px = np.array(im.pixels[:], dtype=np.float32).reshape(im.size[1], im.size[0], im.channels)
        key = im.name.split("_")[-1]
        a = px[..., 3]
        cv = cover if px.shape[0] == R else None
        r = {"alpha_min_all": float(a.min()), "alpha_lt1_frac_all": float((a < 0.999).mean())}
        if cv is not None:
            r["alpha_lt1_frac_in_uv"] = float((a[cv] < 0.999).mean())
            r["alpha_min_in_uv"] = float(a[cv].min())
            rgb = px[..., :3][cv]
            lum = rgb @ np.array([0.2126, 0.7152, 0.0722])
            r["in_uv_mean_rgb_srgb255"] = [round(float(v) * 255, 1) for v in rgb.mean(0)]
            r["in_uv_lum_pcts"] = [round(float(np.percentile(lum, q)), 3) for q in (1, 5, 50, 95, 99)]
            r["in_uv_frac_lum_lt_0.05"] = float((lum < 0.05).mean())
            r["in_uv_frac_lum_lt_0.10"] = float((lum < 0.10).mean())
            if key == "albedo":
                mx_ = rgb.max(1); mn_ = rgb.min(1)
                sat = np.where(mx_ > 1e-4, (mx_ - mn_) / np.maximum(mx_, 1e-4), 0)
                r["in_uv_sat_pcts"] = [round(float(np.percentile(sat, q)), 3) for q in (5, 50, 95)]
            if key == "normal":
                nz = px[..., 2][cv] * 2 - 1
                r["normal_z_pcts"] = [round(float(np.percentile(nz, q)), 3) for q in (1, 5, 50)]
                r["normal_frac_z_lt_0.3"] = float((nz < 0.3).mean())
            # outside-UV fill (padding / bleed)
            rgbo = px[..., :3][~cv]
            r["outside_uv_mean"] = [round(float(v), 3) for v in rgbo.mean(0)] if rgbo.size else None
        rec[key] = r
    # save coverage mask
    img = bpy.data.images.new(n + "_cov", R, R)
    c = np.repeat(cover[..., None].astype(np.float32), 4, axis=2); c[..., 3] = 1
    img.pixels[:] = c.ravel()
    img.filepath_raw = os.path.join(D, "uvcov_" + n + ".png"); img.file_format = "PNG"; img.save()
    out[n] = rec
with open(os.path.join(D, "texcheck.json"), "w") as f:
    json.dump(out, f, indent=1)
print(json.dumps(out, indent=1))
