# Independent reviewer script for the DeadTrees FBX files (2026-10-12).
#   blender.exe -b --factory-startup --python rv.py -- stats  <fbx> <out.json>
#   blender.exe -b --factory-startup --python rv.py -- render <fbx> <out_prefix> <dead|haunted> [shot,shot,...]
# Imports the FBX fresh, scales the 0.01 import back to studs (x100, the hkit export convention), measures budgets /
# textures / pivot / UVs / face direction, and renders the hub look (sky, grass, light-green bed, warm sun, eye height 5).
import bpy, sys, json, math, os
import numpy as np
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree

A = sys.argv[sys.argv.index("--") + 1:]
MODE, FBX = A[0], A[1]
R2 = os.environ.get("RV_ROUND") == "2"


def srgb(c):
    def f(x):
        x /= 255.0
        return x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4
    return tuple(f(v) for v in c) + (1.0,)


# ------------------------------------------------------------------ import
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=FBX)
dg = bpy.context.evaluated_depsgraph_get()
meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
raw = np.concatenate([np.array([o.matrix_world @ v.co for v in o.data.vertices]) for o in meshes])
RAW_SIZE = (raw.max(0) - raw.min(0)).tolist()
RAW_SCALES = {o.name: [round(s, 5) for s in o.matrix_world.to_scale()] for o in meshes}
SCALE = 100.0  # hkit export_fbx: global_scale 0.01 -> Blender re-import is 1/100; Roblox reads 1 unit = 1 stud
for o in bpy.context.scene.objects:
    if o.parent is None:
        o.matrix_world = Matrix.Scale(SCALE, 4) @ o.matrix_world
bpy.context.view_layer.update()


def wverts(o):
    mw = o.matrix_world
    return np.array([mw @ v.co for v in o.data.vertices])


def r2b(p):  # Roblox (X,Y,Z) -> Blender (X,-Z... ) : Blender = (Rx, -Rz, Ry)
    return Vector((p[0], -p[2], p[1]))


def b2r(v):
    return [round(v[0], 3), round(v[2], 3), round(-v[1], 3)]


def bvh_of(objs):
    verts, polys, off = [], [], 0
    for o in objs:
        vs = wverts(o)
        verts.extend([Vector(v) for v in vs])
        polys.extend([[i + off for i in p.vertices] for p in o.data.polygons])
        off += len(vs)
    return BVHTree.FromPolygons(verts, polys)


def img_info(img):
    w, h = img.size
    px = np.array(img.pixels[:], dtype=np.float32).reshape(h, w, img.channels if img.channels else 4)
    d = dict(name=img.name, size=[w, h], channels=img.channels, packed=bool(img.packed_file),
             colorspace=img.colorspace_settings.name)
    if px.shape[2] == 4:
        a = px[:, :, 3]
        d.update(alpha_min=round(float(a.min()), 3), alpha_mean=round(float(a.mean()), 3),
                 alpha_lt099=round(float((a < 0.99).mean()), 4), alpha_lt05=round(float((a < 0.5).mean()), 4),
                 alpha_unique_levels=int(len(np.unique(np.round(a * 255)))))
    return d, px


def sample(px, uv):
    h, w = px.shape[:2]
    x = np.clip((uv[:, 0] % 1.0) * w, 0, w - 1).astype(int)
    y = np.clip((uv[:, 1] % 1.0) * h, 0, h - 1).astype(int)
    return px[y, x]


def mesh_stats(o):
    me = o.data
    me.calc_loop_triangles()
    vs = wverts(o)
    tris = np.array([t.vertices[:] for t in me.loop_triangles])
    tl = np.array([t.loops[:] for t in me.loop_triangles])
    d = dict(name=o.name, tris=len(tris), verts=len(vs),
             bbox_roblox_size=[round(float(x), 3) for x in (lambda s: [s[0], s[2], s[1]])(vs.max(0) - vs.min(0))],
             min_blender=[round(float(x), 3) for x in vs.min(0)], max_blender=[round(float(x), 3) for x in vs.max(0)],
             smooth_frac=round(float(np.mean([p.use_smooth for p in me.polygons])), 3) if len(me.polygons) else 0)
    sh = me.attributes.get("sharp_edge")
    if sh:
        arr = np.zeros(len(me.edges), dtype=bool)
        sh.data.foreach_get("value", arr)
        d["sharp_edges"] = int(arr.sum())
    d["custom_normals"] = bool(getattr(me, "has_custom_normals", False))
    if not me.uv_layers:
        return d, None
    uvl = np.zeros(len(me.loops) * 2, dtype=np.float32)
    me.uv_layers.active.data.foreach_get("uv", uvl)
    uvl = uvl.reshape(-1, 2)
    d["uv_outside_01"] = round(float(((uvl < -0.001) | (uvl > 1.001)).any(1).mean()), 4)
    P = vs[tris]
    U = uvl[tl]
    e1 = P[:, 1] - P[:, 0]
    e2 = P[:, 2] - P[:, 0]
    area3 = 0.5 * np.linalg.norm(np.cross(e1, e2), axis=1)
    l1 = np.linalg.norm(e1, axis=1) + 1e-12
    x = e1 / l1[:, None]
    n = np.cross(e1, e2)
    n /= (np.linalg.norm(n, axis=1)[:, None] + 1e-12)
    y = np.cross(n, x)
    q1 = np.stack([l1, np.zeros_like(l1)], 1)
    q2 = np.stack([(e2 * x).sum(1), (e2 * y).sum(1)], 1)
    d1 = U[:, 1] - U[:, 0]
    d2 = U[:, 2] - U[:, 0]
    Q = np.stack([q1, q2], 2)  # 2x2, columns
    D = np.stack([d1, d2], 2)
    ok = (area3 > 1e-7) & (np.abs(np.linalg.det(Q)) > 1e-10)
    J = np.einsum("nij,njk->nik", D[ok], np.linalg.inv(Q[ok]))
    s = np.linalg.svd(J, compute_uv=False)
    aniso = s[:, 0] / np.maximum(s[:, 1], 1e-9)
    w = area3[ok] / area3[ok].sum()
    d["uv_aniso_area_gt2"] = round(float(w[aniso > 2].sum()), 4)
    d["uv_aniso_area_gt3"] = round(float(w[aniso > 3].sum()), 4)
    d["uv_flipped_area"] = round(float(w[np.linalg.det(J) < 0].sum()), 4)
    return d, dict(P=P, U=U, area=area3, ok=ok, s=s, w=w)


def mat_images(o):
    out = []
    for m in o.data.materials:
        if not (m and m.node_tree):
            continue
        for nd in m.node_tree.nodes:
            if nd.type == "TEX_IMAGE" and nd.image:
                to = [l.to_socket.name + "@" + l.to_node.type for l in m.node_tree.links if l.from_node == nd]
                out.append((nd.image, to, m.name))
    return out


def stats():
    res = dict(fbx=FBX, kb=round(os.path.getsize(FBX) / 1024, 1), raw_import_size_blender=[round(x, 4) for x in RAW_SIZE],
               raw_object_scales=RAW_SCALES, applied_scale=SCALE, objects=[])
    allv = []
    for o in sorted(meshes, key=lambda o: o.name):
        d, geo = mesh_stats(o)
        vs = wverts(o)
        allv.append(vs)
        d["images"] = []
        for img, to, mname in mat_images(o):
            info, px = img_info(img)
            info["to"] = to
            info["material"] = mname
            if geo is not None and any("Base Color" in t for t in to):
                # area-weighted colour of the surface (sampled at triangle centroids), sRGB 0-1
                uvc = geo["U"].mean(1)
                c = sample(px, uvc)[:, :3]
                aw = geo["area"] / geo["area"].sum()
                mean = (c * aw[:, None]).sum(0)
                mx, mn = c.max(1), c.min(1)
                sat = np.where(mx > 1e-4, (mx - mn) / np.maximum(mx, 1e-4), 0)
                lum = 0.2126 * c[:, 0] + 0.7152 * c[:, 1] + 0.0722 * c[:, 2]
                order = np.argsort(lum)
                cw = np.cumsum(aw[order])
                pct = lambda q: float(lum[order][np.searchsorted(cw, q)])
                info["surface_mean_srgb255"] = [int(round(v * 255)) for v in mean]
                info["surface_mean_sat"] = round(float((sat * aw).sum()), 3)
                info["surface_lum_p5_p50_p95"] = [round(pct(0.05), 3), round(pct(0.5), 3), round(pct(0.95), 3)]
                info["surface_area_lum_lt_0.06"] = round(float(aw[lum < 0.06].sum()), 4)
                if px.shape[2] == 4:
                    a = sample(px, uvc)[:, 3]
                    info["surface_alpha_lt_0.99_area"] = round(float(aw[a < 0.99].sum()), 4)
                    info["surface_alpha_mean"] = round(float((a * aw).sum()), 3)
                # texel density
                s = geo["s"]
                dens = np.sqrt(s[:, 0] * s[:, 1]) * img.size[0]
                order2 = np.argsort(dens)
                cw2 = np.cumsum(geo["w"][order2])
                info["px_per_stud_p5_p50_p95"] = [round(float(dens[order2][np.searchsorted(cw2, q)]), 1)
                                                  for q in (0.05, 0.5, 0.95)]
            d["images"].append(info)
        res["objects"].append(d)
    V = np.concatenate(allv)
    res["total_tris"] = sum(o["tris"] for o in res["objects"])
    res["bbox_blender_min"] = [round(float(x), 3) for x in V.min(0)]
    res["bbox_blender_max"] = [round(float(x), 3) for x in V.max(0)]
    sz = V.max(0) - V.min(0)
    res["size_roblox_XYZ"] = [round(float(sz[0]), 2), round(float(sz[2]), 2), round(float(sz[1]), 2)]
    res["lowest_z"] = round(float(V[:, 2].min()), 3)
    res["verts_below_-0.3"] = int((V[:, 2] < -0.3).sum())
    trunk = [o for o in meshes if o.name.endswith("_Trunk")][0]
    tv = wverts(trunk)
    for lo, hi, key in ((-0.3, 0.2, "trunk_base_centroid_xy"), (1.4, 1.7, "trunk_z1.5_centroid_xy"),
                        (2.9, 3.1, "trunk_z3_centroid_xy")):
        sel = tv[(tv[:, 2] > lo) & (tv[:, 2] < hi)]
        if len(sel):
            res[key] = [round(float(x), 3) for x in sel[:, :2].mean(0)]
    # radial profile of the trunk (face / hollow direction): ray from outside toward the trunk axis
    bt = bvh_of([trunk])
    prof = {}
    for z in (1.6, 1.97, 2.5, 3.0, 3.51, 4.35, 4.95, 5.6):
        sel = tv[(tv[:, 2] > z - 0.15) & (tv[:, 2] < z + 0.15)]
        if not len(sel):
            continue
        c = sel[:, :2].mean(0)
        rs = []
        for k in range(180):
            th = math.radians(k * 2)
            dvec = Vector((math.cos(th), math.sin(th), 0))
            org = Vector((c[0], c[1], z)) + dvec * 8
            hit = bt.ray_cast(org, -dvec, 16)
            rs.append(8 - hit[3] if hit[0] is not None else float("nan"))
        rs = np.array(rs)
        med = np.nanmedian(rs)
        deep = [k * 2 for k in range(180) if rs[k] < med - 0.35]
        prof[str(z)] = dict(centre=[round(float(c[0]), 2), round(float(c[1]), 2)], median_r=round(float(med), 2),
                            min_r=round(float(np.nanmin(rs)), 2), min_az_deg=int(np.nanargmin(rs) * 2),
                            deep_az_deg=deep)
    res["trunk_profile_note"] = "az 270 = Blender -Y = Roblox +Z (front); az 90 = back; 0 = +X"
    res["trunk_profile"] = prof
    # spider points from NOTES (Roblox axes)
    pts = dict(dead=[(-5.46, 8.91, -5.65), (5.95, 10.14, -1.77), (-3.53, 11.22, 4.58)],
               haunted=[(-5.98, 7.60, 1.59), (5.51, 7.64, 1.98)])
    if R2:  # round-2 NOTES
        pts = dict(dead=[(4.40, 5.97, 6.79), (-5.46, 9.06, -5.69), (5.99, 10.18, -1.77)],
                   haunted=[(-5.98, 7.76, 1.64), (5.95, 7.63, 1.21)])
    key = "haunted" if "Haunted" in FBX else "dead"
    solid = [o for o in meshes if not o.name.endswith(("_Web", "_WebSilk"))]
    ball = bvh_of(meshes)
    bs = bvh_of(solid)
    sp = []
    for p in pts[key]:
        b = r2b(p)
        up = bs.ray_cast(b - Vector((0, 0, 0.02)), Vector((0, 0, 1)), 2.0)
        dn = ball.ray_cast(b - Vector((0, 0, 0.05)), Vector((0, 0, -1)), 30.0)
        ring_hits = 0
        for k in range(12):
            th = math.radians(k * 30)
            o2 = b + Vector((math.cos(th) * 1.2, math.sin(th) * 1.2, -0.3))
            if ball.ray_cast(o2, Vector((0, 0, -1)), 8.0)[0] is not None:
                ring_hits += 1
        sp.append(dict(roblox=p, branch_above_dist=None if up[0] is None else round(up[3], 3),
                       free_drop=round(dn[3], 2) if dn[0] is not None else "clear to ground (%.2f)" % b.z,
                       ring_rays_blocked_of_12=ring_hits))
    res["spider_points_check"] = sp
    print("RVSTATS " + json.dumps(res, indent=1))
    with open(A[2], "w") as f:
        json.dump(res, f, indent=1)


# ------------------------------------------------------------------ hub look
def hub_scene():
    sc = bpy.context.scene
    sc.render.engine = "BLENDER_EEVEE"
    try:
        sc.eevee.taa_render_samples = 48
    except Exception:
        pass
    sc.render.resolution_x, sc.render.resolution_y = 1280, 900
    sc.view_settings.view_transform = "AgX"
    for lk in ("AgX - Punchy", "Punchy"):
        try:
            sc.view_settings.look = lk
            break
        except Exception:
            pass
    sc.render.film_transparent = False
    w = bpy.data.worlds.new("Hub")
    sc.world = w
    try:
        w.use_nodes = True
    except Exception:
        pass
    nt = w.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputWorld")
    bg = nt.nodes.new("ShaderNodeBackground")
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    lp = nt.nodes.new("ShaderNodeLightPath")
    mixc = nt.nodes.new("ShaderNodeMix")
    mixc.data_type = "RGBA"
    mixs = nt.nodes.new("ShaderNodeMath")
    mixs.operation = "MULTIPLY_ADD"
    nt.links.new(tc.outputs["Generated"], sep.inputs[0])
    nt.links.new(sep.outputs["Z"], ramp.inputs["Fac"])
    ramp.color_ramp.elements[0].position = 0.0
    ramp.color_ramp.elements[0].color = srgb((176, 214, 246))   # hazy horizon
    ramp.color_ramp.elements[1].position = 0.55
    ramp.color_ramp.elements[1].color = srgb((92, 160, 232))    # saturated zenith sky-blue
    # camera sees the gradient sky; lighting gets a softer sky fill
    nt.links.new(lp.outputs["Is Camera Ray"], mixc.inputs["Factor"])
    mixc.inputs["A"].default_value = srgb((150, 185, 225))
    nt.links.new(ramp.outputs["Color"], mixc.inputs["B"])
    nt.links.new(mixc.outputs["Result"], bg.inputs["Color"])
    nt.links.new(lp.outputs["Is Camera Ray"], mixs.inputs[0])
    mixs.inputs[1].default_value = 0.2   # camera: 0.2+0.85 = 1.05
    mixs.inputs[2].default_value = 0.85  # lighting fill: 0.85
    nt.links.new(mixs.outputs[0], bg.inputs["Strength"])
    nt.links.new(bg.outputs[0], out.inputs[0])
    # warm sun key
    ld = bpy.data.lights.new("Sun", "SUN")
    ld.energy, ld.color = 4.2, (1.0, 0.94, 0.84)
    ld.angle = math.radians(1.5)
    ld.use_shadow = os.environ.get("RV_NOSHADOW") != "1"
    sun = bpy.data.objects.new("Sun", ld)
    sc.collection.objects.link(sun)
    sun.rotation_euler = (math.radians(42), 0, math.radians(-35))  # from front-left-above (front = -Y)

    def mat(name, c1, c2, rough, scale):
        m = bpy.data.materials.new(name)
        m.use_nodes = True
        t = m.node_tree
        b = t.nodes["Principled BSDF"]
        nz = t.nodes.new("ShaderNodeTexNoise")
        nz.inputs["Scale"].default_value = scale
        r = t.nodes.new("ShaderNodeValToRGB")
        r.color_ramp.elements[0].color = srgb(c1)
        r.color_ramp.elements[1].color = srgb(c2)
        t.links.new(nz.outputs["Fac"], r.inputs["Fac"])
        t.links.new(r.outputs["Color"], b.inputs["Base Color"])
        b.inputs["Roughness"].default_value = rough
        return m

    bpy.ops.mesh.primitive_plane_add(size=800, location=(0, 0, -0.04))
    g = bpy.context.object
    g.name = "Grass"
    g.data.materials.append(mat("GrassM", (62, 128, 46), (84, 150, 58), 0.92, 0.6))
    bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=7.5, depth=0.2, location=(0, 0, -0.1))
    bd = bpy.context.object
    bd.name = "Bed"
    bpy.ops.object.shade_smooth()
    bd.data.materials.append(mat("BedM", (86, 160, 64), (98, 176, 76), 0.9, 1.5))
    # 5-stud reference "player" block (2 x 1 x 5)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(9.0, -2.5, 2.5))
    rb = bpy.context.object
    rb.name = "Ref5"
    rb.scale = (2, 1, 5)
    m = bpy.data.materials.new("RefM")
    m.use_nodes = True
    m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = srgb((226, 120, 52))
    m.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.6
    rb.data.materials.append(m)
    return sc


def prep_asset_materials():
    for o in meshes:
        silk = o.name.endswith("_WebSilk")
        web = o.name.endswith(("_Web", "_WebSilk"))
        if web:
            o.visible_shadow = False  # lead sets CastShadow false on Web / WebSilk
        for m in o.data.materials:
            if not m:
                continue
            m.use_backface_culling = os.environ.get("RV_NOCULL") != "1"  # Roblox renders single-sided
            for nd in m.node_tree.nodes:
                if nd.type == "TEX_IMAGE" and nd.image:
                    to = [l.to_node.type for l in m.node_tree.links if l.from_node == nd]
                    tos = [l.to_socket.name for l in m.node_tree.links if l.from_node == nd]
                    if "NORMAL_MAP" in to or "Roughness" in tos:
                        nd.image.colorspace_settings.name = "Non-Color"
            if silk:
                try:
                    m.surface_render_method = "BLENDED"
                except Exception:
                    m.blend_method = "BLEND"
                # Roblox AlphaMode=Transparency: alpha comes from the ColorMap alpha
                nt = m.node_tree
                b = [n for n in nt.nodes if n.type == "BSDF_PRINCIPLED"][0]
                has_alpha = any(l.to_node == b and l.to_socket.name == "Alpha" for l in nt.links)
                if not has_alpha:
                    tex = [n for n in nt.nodes if n.type == "TEX_IMAGE"][0]
                    nt.links.new(tex.outputs["Alpha"], b.inputs["Alpha"])
                    print("RV: silk alpha was NOT linked on import; linked it for the render")


def cam_shot(path, loc, target, fov=70):
    sc = bpy.context.scene
    cd = bpy.data.cameras.new("Cam")
    cd.sensor_fit = "VERTICAL"
    cd.angle_y = math.radians(fov)
    cd.clip_start, cd.clip_end = 0.05, 2000
    cam = bpy.data.objects.new("Cam", cd)
    sc.collection.objects.link(cam)
    cam.location = Vector(loc)
    cam.rotation_euler = (Vector(target) - cam.location).to_track_quat("-Z", "Y").to_euler()
    sc.camera = cam
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(cam)
    print("RV: wrote", path, flush=True)


def shots(kind):
    S = {}
    E = 5.0  # player eye height
    S["front_25"] = ((0, -25, E), (0, 0, 7.0))
    S["back_25"] = ((0, 25, E), (0, 0, 7.0))
    S["left_25"] = ((-25, 0, E), (0, 0, 7.0))
    S["right_25"] = ((25, 0, E), (0, 0, 7.0))
    S["front_45"] = ((0, -45, E), (0, 0, 6.5))
    S["left_45"] = ((-45, 0, E), (0, 0, 6.5))
    S["q34_40"] = ((-28.3, -28.3, E), (0, 0, 6.5))
    if kind == "dead":
        hc = r2b((0.59, 1.97, 1.11))
        hd = Vector((0.47, -0.88, 0)).normalized()
        S["close_hollow_7"] = (tuple(hc + hd * 7 + Vector((0, 0, E - hc.z))), tuple(hc + Vector((0, 0, 0.6))))
        w1 = r2b((-0.65, 7.19, 0.37))
        n1 = Vector((-0.86, 0.50, 0)).normalized()
        S["close_web1_7"] = (tuple(w1 + n1 * 7 + Vector((0, 0, E - w1.z))), tuple(w1))
        w2 = r2b((0.43, 12.80, -2.40))
        n2 = Vector((-0.85, -0.43, 0)).normalized()
        S["close_web2_10"] = (tuple(w2 + n2 * 9 + Vector((0, 0, E - w2.z))), tuple(w2))
        S["close_bark_6"] = ((-1.5, -6.5, E), (0, 0, 5.8))
        S["close_crown_12"] = ((-6, -10, E), (0, 0, 9.5))
        S["seam_5"] = ((-0.1, -5.0, E), (-0.1, 0.25, 6.6))
        S["seam_back_5"] = ((-0.1, 5.5, E), (-0.1, 0.25, 6.6))
        S["base_5"] = ((-3.0, -4.0, 2.5), (0, 0, 0.6))
        S["hole_z3"] = ((-4.5, -4.0, 3.5), (-1.17, -0.98, 3.03))
        S["limbhole_7"] = ((6.0, -2.0, E), (2.16, -0.22, 7.02))
        S["limbhole_8"] = ((-5.0, -5.0, E), (-1.98, -1.58, 8.31))
    else:
        fc = r2b((0.09, 4.35, 1.43))
        S["face_18"] = ((0.09, -18, E), tuple(fc))
        S["face_8"] = ((0.09, -8, E), tuple(fc))
        S["face_q34_15"] = ((-9, -12, E), tuple(fc))
        w1 = r2b((-0.90, 7.61, 0.84))
        S["close_web_7"] = (tuple(w1 + Vector((0.3, -0.95, 0)).normalized() * 7 + Vector((0, 0, E - w1.z))), tuple(w1))
        S["close_leaves_L"] = ((-4.5, -8.0, E), (-4.8, -0.8, 8.3))
        S["close_leaves_R"] = ((5.0, -8.0, E), (4.6, -0.8, 8.3))
        S["face_5"] = ((0.09, -5.0, 4.4), (0.09, -1.3, 4.3))
        S["face_side_R_6"] = ((6.0, -1.6, 4.3), (0.0, -1.2, 4.2))
        S["face_side_L_6"] = ((-6.0, -1.6, 4.3), (0.0, -1.2, 4.2))
        S["mouth_low_4"] = ((1.6, -4.0, 3.0), (0.05, -1.3, 3.5))
        S["seam_5"] = ((0.27, -5.0, E), (0.27, -0.23, 7.3))
        S["seam_back_5"] = ((0.27, 5.0, E), (0.27, -0.23, 7.3))
        S["base_5"] = ((-3.0, -4.0, 2.5), (0, 0, 0.6))
        S["back_hole_4"] = ((-3.0, 4.0, 3.0), (-0.99, 1.08, 2.42))
    if R2:
        S2 = {k: S[k] for k in ("front_25", "back_25", "left_25", "right_25", "front_45", "left_45", "q34_40")}
        S2["back_45"] = ((0, 45, E), (0, 0, 6.5))
        S2["right_45"] = ((45, 0, E), (0, 0, 6.5))

        def web_shot(hub_r, n_r, dist, flip=False):
            h = r2b(hub_r)
            n = r2b(n_r)
            nh = Vector((n.x, n.y, 0)).normalized() * (-1 if flip else 1)
            return (tuple(h + nh * dist + Vector((0, 0, E - h.z))), tuple(h))

        if kind == "dead":
            S2["close_hollow_7"] = S["close_hollow_7"]
            S2["close_bark_6"] = S["close_bark_6"]
            S2["base_5"] = S["base_5"]
            S2["web1_front_8"] = web_shot((1.19, 8.03, -0.53), (0.07, 0.34, 0.94), 8)
            S2["web1_back_8"] = web_shot((1.19, 8.03, -0.53), (0.07, 0.34, 0.94), 8, True)
            S2["web2_side_8"] = web_shot((-0.93, 7.97, 0.69), (-0.89, -0.07, -0.45), 8)
            S2["web3_8"] = web_shot((-1.06, 7.20, -1.14), (-0.72, 0.27, 0.64), 8, True)
            S2["web3_other_8"] = web_shot((-1.06, 7.20, -1.14), (-0.72, 0.27, 0.64), 8)
            S2["joint_up_front_4"] = ((1.5, -4.0, 3.5), (0.2, 0.0, 8.5))
            S2["joint_up_back_4"] = ((-1.0, 4.0, 3.5), (-0.2, 0.3, 8.5))
            S2["joint_up_left_4"] = ((-4.0, 0.5, 3.5), (-1.0, 0.0, 8.5))
            S2["joint_up_right_4"] = ((4.0, -0.5, 3.5), (1.5, 0.0, 8.5))
            S2["crown_12"] = S["close_crown_12"]
        else:
            fc = r2b((0.09, 4.35, 1.85))
            S2["face_18"] = ((0.09, -18, E), tuple(fc))
            S2["face_8"] = ((0.09, -8.5, E), tuple(fc))
            S2["face_5"] = ((0.09, -5.5, 4.4), tuple(fc))
            S2["face_q34_15"] = ((-9, -12, E), tuple(fc))
            S2["face_q45R_6"] = ((0.09 + 4.24, -1.85 - 4.24, 4.4), tuple(fc))
            S2["face_q45L_6"] = ((0.09 - 4.24, -1.85 - 4.24, 4.4), tuple(fc))
            S2["face_side_R_6"] = ((6.0, -1.9, 4.3), (0.0, -1.6, 4.2))
            S2["face_side_L_6"] = ((-6.0, -1.9, 4.3), (0.0, -1.6, 4.2))
            S2["face_side_R_25"] = ((25.0, -1.9, E), (0.0, -1.6, 4.4))
            S2["face_side_L_25"] = ((-25.0, -1.9, E), (0.0, -1.6, 4.4))
            S2["face_q60R_10"] = ((0.09 + 8.66, -1.85 - 5.0, 4.4), tuple(fc))
            S2["face_q60L_10"] = ((0.09 - 8.66, -1.85 - 5.0, 4.4), tuple(fc))
            S2["mouth_low_4"] = ((1.6, -4.4, 3.0), (0.05, -1.7, 3.5))
            S2["mouth_lowL_4"] = ((-1.6, -4.4, 3.0), (0.05, -1.7, 3.5))
            # normal (-0.04, 0.51, -0.86) Roblox -> Blender (-0.04, 0.86, 0.51): +Y side is the back, so flip = front
            S2["web_front_8"] = web_shot((-1.33, 8.11, 1.08), (-0.04, 0.51, -0.86), 8, True)
            S2["web_back_8"] = web_shot((-1.33, 8.11, 1.08), (-0.04, 0.51, -0.86), 8)
            S2["close_leaves_L"] = S["close_leaves_L"]
            S2["close_leaves_R"] = S["close_leaves_R"]
            S2["base_5"] = S["base_5"]
            S2["joint_up_front_4"] = ((1.5, -4.2, 3.5), (0.2, 0.0, 8.8))
            S2["joint_up_back_4"] = ((-1.0, 4.0, 3.5), (-0.2, 0.3, 8.8))
            S2["start_flagged_4"] = ((-3.5, 3.5, 5.0), (-1.58, 1.28, 8.86))
        return S2
    return S


def render():
    prefix, kind = A[2], A[3]
    only = A[4].split(",") if len(A) > 4 and A[4] else None
    hub_scene()
    prep_asset_materials()
    for name, (loc, tgt) in shots(kind).items():
        if only and name not in only:
            continue
        cam_shot(prefix + name + ".png", loc, tgt)


if MODE == "stats":
    stats()
elif MODE == "render":
    render()
