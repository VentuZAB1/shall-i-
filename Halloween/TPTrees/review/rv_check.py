# Independent reviewer: technical checks on a fresh FBX import (TPTrees row).
# blender.exe -b --factory-startup --python rv_check.py -- <fbx> <tag> <outdir> [reference.fbx]
import bpy, bmesh, sys, os, math, json, random
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree

argv = sys.argv[sys.argv.index("--") + 1:]
FBX, TAG, OUT = argv[0], argv[1], argv[2]
REF = argv[3] if len(argv) > 3 else None
os.makedirs(OUT, exist_ok=True)
random.seed(7)
np.random.seed(7)


def log(*a):
    print("[rv]", *a, flush=True)


def unit_scale_factor(path):
    try:
        from io_scene_fbx import parse_fbx
        root, ver = parse_fbx.parse(path)
        for e in root.elems:
            if e.id == b"GlobalSettings":
                for p70 in e.elems:
                    if p70.id == b"Properties70":
                        for p in p70.elems:
                            if p.props and p.props[0] in (b"UnitScaleFactor", b"OriginalUnitScaleFactor"):
                                yield p.props[0].decode(), p.props[-1]
    except Exception as ex:  # noqa
        yield "error", str(ex)


def import_fbx(path):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.fbx(filepath=path)
    return [o for o in bpy.data.objects if o.type == "MESH"]


def local_verts(me):
    V = np.empty(len(me.vertices) * 3)
    me.vertices.foreach_get("co", V)
    return V.reshape(-1, 3)


def islands(me):
    n = len(me.vertices)
    par = list(range(n))

    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a
    E = np.empty(len(me.edges) * 2, dtype=np.int64)
    me.edges.foreach_get("vertices", E)
    E = E.reshape(-1, 2)
    for a, b in E:
        ra, rb = find(int(a)), find(int(b))
        if ra != rb:
            par[ra] = rb
    roots = {}
    for i in range(n):
        r = find(i)
        roots[r] = roots.get(r, 0) + 1
    return roots, [find(i) for i in range(n)]


def tri_arrays(me):
    me.calc_loop_triangles()
    nt = len(me.loop_triangles)
    TV = np.empty(nt * 3, dtype=np.int64)
    me.loop_triangles.foreach_get("vertices", TV)
    TL = np.empty(nt * 3, dtype=np.int64)
    me.loop_triangles.foreach_get("loops", TL)
    return TV.reshape(-1, 3), TL.reshape(-1, 3)


def img_np(img):
    w, h = img.size
    P = np.empty(w * h * 4, dtype=np.float32)
    img.pixels.foreach_get(P)
    return P.reshape(h, w, 4)


def mat_info(m):
    d = {"name": m.name, "textures": [], "backface_culling": m.use_backface_culling}
    nt = m.node_tree
    if not nt:
        return d, {}
    by_socket = {}
    for n in nt.nodes:
        if n.type == "TEX_IMAGE" and n.image:
            tos = []
            for l in nt.links:
                if l.from_node == n:
                    s = l.to_socket.name
                    if l.to_node.type == "NORMAL_MAP":
                        s = "Normal(via NormalMap)"
                    tos.append("%s.%s<-%s" % (l.to_node.type, s, l.from_socket.name))
            d["textures"].append(dict(image=n.image.name, size=list(n.image.size), packed=bool(n.image.packed_file),
                                      colorspace=n.image.colorspace_settings.name, links=tos,
                                      channels=n.image.channels, depth=n.image.depth))
            for t in tos:
                if "Base Color" in t:
                    by_socket["albedo"] = n.image
                elif "Normal" in t:
                    by_socket["normal"] = n.image
                elif "Roughness" in t:
                    by_socket["rough"] = n.image
                elif "Alpha" in t:
                    by_socket["alpha"] = n.image
    for n in nt.nodes:
        if n.type == "BSDF_PRINCIPLED":
            es = n.inputs.get("Emission Strength")
            ec = n.inputs.get("Emission Color")
            d["emission_strength"] = es.default_value if es else None
            d["emission_color"] = list(ec.default_value)[:3] if ec else None
            d["emission_linked"] = bool(ec and ec.is_linked) or bool(es and es.is_linked)
            d["metallic"] = n.inputs["Metallic"].default_value
            d["metallic_linked"] = n.inputs["Metallic"].is_linked
            d["alpha_linked"] = n.inputs["Alpha"].is_linked
            d["alpha"] = n.inputs["Alpha"].default_value
    return d, by_socket


def sample_surface(V, TV, UVt, n=40000):
    """area-weighted random samples: returns uv (n,2), tri index, 3D points"""
    a, b, c = V[TV[:, 0]], V[TV[:, 1]], V[TV[:, 2]]
    area = 0.5 * np.linalg.norm(np.cross(b - a, c - a), axis=1)
    p = area / area.sum()
    idx = np.random.choice(len(TV), n, p=p)
    r1, r2 = np.random.rand(n), np.random.rand(n)
    s = np.sqrt(r1)
    w0, w1, w2 = 1 - s, s * (1 - r2), s * r2
    uv = UVt[idx, 0] * w0[:, None] + UVt[idx, 1] * w1[:, None] + UVt[idx, 2] * w2[:, None]
    P3 = a[idx] * w0[:, None] + b[idx] * w1[:, None] + c[idx] * w2[:, None]
    return uv, idx, P3, area


def lookup(I, uv):
    h, w = I.shape[:2]
    x = np.clip((uv[:, 0] % 1.0) * w, 0, w - 1).astype(int)
    y = np.clip((uv[:, 1] % 1.0) * h, 0, h - 1).astype(int)
    return I[y, x]


def hsv(rgb):
    mx, mn = rgb.max(1), rgb.min(1)
    v = mx
    s = np.where(mx > 1e-6, (mx - mn) / np.maximum(mx, 1e-6), 0)
    r, g, b = rgb[:, 0], rgb[:, 1], rgb[:, 2]
    d = np.maximum(mx - mn, 1e-6)
    h = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) * 60
    return h, s, v


def analyse(objs):
    rep = {"file": FBX, "unit_scale": dict(unit_scale_factor(FBX)), "objects": {}}
    allV = []
    geo = {}
    for o in objs:
        me = o.data
        V = local_verts(me)  # object space = studs (object scale is the FBX 0.01 unit scale)
        allV.append(V)
        TV, TL = tri_arrays(me)
        roots, comp = islands(me)
        a, b, c = V[TV[:, 0]], V[TV[:, 1]], V[TV[:, 2]]
        svol = float(np.einsum("ij,ij->i", a, np.cross(b, c)).sum() / 6.0)
        r = dict(tris=int(len(TV)), verts=len(me.vertices), islands=len(roots),
                 location=[round(x, 4) for x in o.location], rotation_deg=[round(math.degrees(x), 3) for x in o.rotation_euler],
                 scale=[round(x, 5) for x in o.scale], uv_layers=len(me.uv_layers),
                 bbox_min=[round(float(x), 3) for x in V.min(0)], bbox_max=[round(float(x), 3) for x in V.max(0)],
                 verts_below_minus0_3=int((V[:, 2] < -0.3).sum()), signed_volume=round(svol, 2),
                 has_custom_normals=me.has_custom_normals, materials=[])
        mats = {}
        for m in me.materials:
            if m:
                d, socks = mat_info(m)
                r["materials"].append(d)
                mats.update(socks)
        # UV / texel density
        if me.uv_layers:
            UV = np.empty(len(me.loops) * 2)
            me.uv_layers.active.data.foreach_get("uv", UV)
            UV = UV.reshape(-1, 2)
            UVt = UV[TL]
            ua, ub, uc = UVt[:, 0], UVt[:, 1], UVt[:, 2]
            auv = 0.5 * np.abs((ub[:, 0] - ua[:, 0]) * (uc[:, 1] - ua[:, 1]) - (uc[:, 0] - ua[:, 0]) * (ub[:, 1] - ua[:, 1]))
            a3 = 0.5 * np.linalg.norm(np.cross(b - a, c - a), axis=1)
            S = mats["albedo"].size[0] if "albedo" in mats else 1024
            dens = np.sqrt(np.maximum(auv, 1e-14) * S * S / np.maximum(a3, 1e-12))
            order = np.argsort(dens)
            cw = np.cumsum(a3[order]) / a3.sum()
            pct = lambda q: float(dens[order][np.searchsorted(cw, q)])
            med = pct(0.5)
            r["texel_px_per_stud"] = dict(p5=round(pct(0.05), 1), median=round(med, 1), p95=round(pct(0.95), 1),
                                          area_frac_below_half_median=round(float(a3[dens < 0.5 * med].sum() / a3.sum()), 4),
                                          area_frac_below_quarter_median=round(float(a3[dens < 0.25 * med].sum() / a3.sum()), 4))
            r["uv_outside_0_1"] = int(((UV < -0.001) | (UV > 1.001)).any(1).sum())
            r["uv_total_area"] = round(float(auv.sum()), 3)
            # texture sampling over the visible surface
            uv, idx, P3, area = sample_surface(V, TV, UVt)
            tx = {}
            if "albedo" in mats:
                I = img_np(mats["albedo"])
                rgba = lookup(I, uv)
                rgb = rgba[:, :3]
                luma = 0.2126 * rgb[:, 0] + 0.7152 * rgb[:, 1] + 0.0722 * rgb[:, 2]
                h, s, v = hsv(rgb)
                tx["albedo_mean_srgb255"] = [round(float(x) * 255) for x in rgb.mean(0)]
                tx["albedo_luma_pcts(5,25,50,75,95)"] = [round(float(np.percentile(luma, q)), 3) for q in (5, 25, 50, 75, 95)]
                tx["frac_near_black(luma<0.05)"] = round(float((luma < 0.05).mean()), 4)
                tx["frac_very_dark(luma<0.10)"] = round(float((luma < 0.10).mean()), 4)
                tx["sat_mean"] = round(float(s.mean()), 3)
                tx["alpha_min_on_surface"] = round(float(rgba[:, 3].min()), 3)
                tx["alpha_frac_below_0.99_on_surface"] = round(float((rgba[:, 3] < 0.99).mean()), 4)
                tx["alpha_min_whole_image"] = round(float(I[:, :, 3].min()), 3)
                # hue buckets for coloured (non-dark) texels
                col = v > 0.25
                tx["hue_buckets_of_bright(red<15|orange15-40|amber/yellow40-65|green65-170|other)"] = [
                    round(float(((h < 15) | (h >= 345))[col].mean()), 3), round(float(((h >= 15) & (h < 40))[col].mean()), 3),
                    round(float(((h >= 40) & (h < 65))[col].mean()), 3), round(float(((h >= 65) & (h < 170))[col].mean()), 3),
                    round(float(((h >= 170) & (h < 345))[col].mean()), 3)]
                tx["frac_muddy(sat<0.4 & 0.12<v<0.45)"] = round(float(((s < 0.4) & (v > 0.12) & (v < 0.45)).mean()), 4)
                med_l = float(np.median(luma))
                tx["frac_darker_than_60pct_median"] = round(float((luma < 0.6 * med_l).mean()), 4)
                geo[o.name + "_dark_pts"] = P3[luma < 0.6 * med_l]
            if "normal" in mats:
                N = lookup(img_np(mats["normal"]), uv)[:, :3] * 2 - 1
                tx["normal_frac_z<0.35"] = round(float((N[:, 2] < 0.35).mean()), 4)
                tx["normal_frac_z<0"] = round(float((N[:, 2] < 0).mean()), 4)
                tx["normal_mean_z"] = round(float(N[:, 2].mean()), 3)
            if "rough" in mats:
                R = lookup(img_np(mats["rough"]), uv)[:, 0]
                tx["rough_mean"] = round(float(R.mean()), 3)
                tx["rough_p5_p95"] = [round(float(np.percentile(R, 5)), 3), round(float(np.percentile(R, 95)), 3)]
            r["texture_on_surface"] = tx
        rep["objects"][o.name] = r
        geo[o.name] = (V, TV, comp, roots)
    V = np.vstack(allV)
    mn, mx = V.min(0), V.max(0)
    rep["total_tris"] = sum(v["tris"] for v in rep["objects"].values())
    rep["bbox_local_min"] = [round(float(x), 3) for x in mn]
    rep["bbox_local_max"] = [round(float(x), 3) for x in mx]
    rep["size_roblox_XYZ(studs)"] = [round(float(mx[0] - mn[0]), 2), round(float(mx[2] - mn[2]), 2), round(float(mx[1] - mn[1]), 2)]
    rep["min_z"] = round(float(mn[2]), 3)
    # base centre: lowest verts of the non-TP parts
    base = np.vstack([geo[k][0] for k in geo if not k.endswith("_dark_pts") and not k.startswith("TP")])
    low = base[base[:, 2] < mn[2] + 0.6]
    rep["base_centroid_xy(lowest 0.6)"] = [round(float(x), 3) for x in low[:, :2].mean(0)]
    # foliage only bbox
    can = [k for k in geo if k.startswith("Canopy") and not k.endswith("_dark_pts")]
    if can:
        CV = np.vstack([geo[k][0] for k in can])
        rep["canopy_bbox_min"] = [round(float(x), 2) for x in CV.min(0)]
        rep["canopy_bbox_max"] = [round(float(x), 2) for x in CV.max(0)]
    # TP clipping / floating vs everything else
    if "TP" in geo:
        others = [k for k in geo if not k.endswith("_dark_pts") and k != "TP"]
        verts, polys, off = [], [], 0
        for k in others:
            Vk, TVk = geo[k][0], geo[k][1]
            verts += [Vector(p) for p in Vk]
            polys += [tuple(int(i) + off for i in t) for t in TVk]
            off += len(Vk)
        bvh = BVHTree.FromPolygons(verts, polys)
        TPV, _, comp, roots = geo["TP"]
        res = []
        for i, p in enumerate(TPV):
            v = Vector(p)
            loc, nrm, fi, dist = bvh.find_nearest(v, 5.0)
            sd = None if loc is None else (v - loc).dot(nrm)
            hit = bvh.ray_cast(v + Vector((0, 0, -0.001)), Vector((0, 0, -1)), 1.2)
            down = None if hit[0] is None else (hit[3], hit[1].z)
            res.append((dist if loc is not None else 99, sd, down))
        dist = np.array([r_[0] for r_ in res])
        sd = np.array([r_[1] if r_[1] is not None else 99 for r_ in res])
        inside = (sd < -0.04) & (dist < 0.8)
        inside_deep = (sd < -0.12) & (dist < 0.8)
        downd = np.array([r_[2][0] if r_[2] else 99 for r_ in res])
        downz = np.array([r_[2][1] if r_[2] else 0 for r_ in res])
        resting = (downd < 1.2) & (downz > 0.45)
        # per vertex: the "lowest gap" for draped parts: the min over each island neighbourhood is handled by islands
        hover = resting & (dist > 0.22)
        hover_big = resting & (dist > 0.4)
        tp = dict(verts=len(TPV), strips_islands=len(roots), island_sizes=sorted(roots.values(), reverse=True)[:20],
                  frac_inside_gt0_04=round(float(inside.mean()), 4), frac_inside_gt0_12=round(float(inside_deep.mean()), 4),
                  max_penetration=round(float(-sd[dist < 0.8].min()), 3) if (dist < 0.8).any() else None,
                  frac_resting_over_surface=round(float(resting.mean()), 4),
                  frac_hover_gap_gt0_22=round(float(hover.mean()), 4), frac_hover_gap_gt0_4=round(float(hover_big.mean()), 4),
                  dist_pcts_resting=[round(float(np.percentile(dist[resting], q)), 3) for q in (25, 50, 75, 90, 99)] if resting.any() else None)
        # cluster hover / inside points (0.75 grid) for spot renders
        def clusters(mask):
            P = TPV[mask]
            if not len(P):
                return []
            keys = {}
            for p in P:
                k = tuple((p / 0.75).round().astype(int))
                keys.setdefault(k, []).append(p)
            cl = sorted(keys.values(), key=len, reverse=True)[:8]
            return [dict(n=len(c), centre_blender=[round(float(x), 2) for x in np.mean(c, 0)]) for c in cl]
        tp["hover_clusters"] = clusters(hover)
        tp["inside_clusters"] = clusters(inside)
        # how much paper is visible below the canopy (hanging) vs on top
        if can:
            zc = float(CV[:, 2].min())
            tp["frac_tp_verts_below_canopy_bottom"] = round(float((TPV[:, 2] < zc).mean()), 3)
            tp["canopy_bottom_z"] = round(zc, 2)
        # strip width check: per island PCA thickness / width
        widths = []
        comp = np.array(comp)
        for rt, cnt in roots.items():
            P = TPV[comp == rt]
            if len(P) < 16:
                continue
            widths.append(len(P))
        rep["TP"] = tp
    return rep


objs = import_fbx(FBX)
rep = analyse(objs)
if REF:
    ro = import_fbx(REF)
    rep["reference_fbx"] = dict(file=REF, unit_scale=dict(unit_scale_factor(REF)),
                                scales=sorted(set(tuple(round(x, 4) for x in o.scale) for o in ro)),
                                size_local=[round(float(x), 2) for x in np.ptp(np.vstack([local_verts(o.data) for o in ro]), 0)])
path = os.path.join(OUT, "check_%s.json" % TAG)
with open(path, "w") as f:
    json.dump(rep, f, indent=1, default=str)
print("RV_REPORT " + json.dumps(rep, indent=1, default=str))
