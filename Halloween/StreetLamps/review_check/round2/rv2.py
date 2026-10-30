# Independent visual-review renders for the Halloween street lamp (reviewer only; read-only on the builder's files).
# Usage: blender -b --factory-startup --python rv.py -- <stats|day|night|checks|sil>
import bpy, bmesh, sys, os, math, json
import numpy as np
from mathutils import Vector, Matrix

H = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween"
sys.path.insert(0, H)
from hkit import lin, fresh, link, review_setup, mat_noise, mat_flat  # read-only kit

OUT = os.path.join(H, "StreetLamps", "review_check", "round2")
FBX = r"C:\cdimp\Halloween_StreetLamp.fbx"
HANG_Y = -3.55
HEAD = Vector((0.0, HANG_Y, 13.19))   # round 2: head hangs 0.26 lower
PL = Vector((0.011, -3.528, 12.86))       # NOTES: suggested inside PointLight
FLAME = Vector((0.011, -3.528, 12.85))
GROUNDL = Vector((0.0, -3.55, 12.046))
GREEN = (118, 199, 104)
CREAM = (231, 222, 216)


def log(*a):
    print("[rv]", *a, flush=True)


def import_lamp():
    """Fresh FBX import. The re-import carries object scale 0.01 with the mesh in studs: render at studs."""
    bpy.ops.import_scene.fbx(filepath=FBX)
    objs = {o.name: o for o in bpy.context.scene.objects if o.type == "MESH"}
    for o in objs.values():
        o.scale = (1, 1, 1)
    bpy.context.view_layer.update()
    return objs


def roblox_mats(objs):
    for o in objs.values():
        for m in o.data.materials:
            if m:
                m.use_backface_culling = True
    for m in objs["WebSilk"].data.materials:
        m.surface_render_method = "BLENDED"
    for nm in ("Web", "WebSilk"):
        objs[nm].visible_shadow = False


def ground():
    g = mat_noise("Lawn", lin(GREEN), lin(tuple(int(c * 0.9) for c in GREEN)), nscale=0.35, detail=4, rough=0.9,
                  lo=0.3, hi=0.7)
    bpy.ops.mesh.primitive_plane_add(size=400, location=(0, 0, -0.01))
    gr = bpy.context.active_object
    gr.name = "Ground"
    gr.data.materials.append(g)
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, -5.25, -0.005))
    p = bpy.context.active_object
    p.name = "Path"
    p.scale = (400, 8, 1)
    p.data.materials.append(mat_flat("PathM", lin(CREAM), rough=0.85))


def blockman(x, y, rotz=0.0):
    """~5.2-stud Roblox-ish block player for scale."""
    m = mat_flat("Plr", lin((70, 110, 200)), rough=0.6)
    sk = mat_flat("Skin", lin((245, 205, 50)), rough=0.6)
    parts = [((0, -0.5, 1.0), (0.95, 1.0, 2.0), m), ((0, 0.5, 1.0), (0.95, 1.0, 2.0), m),
             ((0, 0, 3.0), (1.0, 2.0, 2.0), m), ((0, 0, 4.6), (1.1, 1.1, 1.2), sk)]
    for (px, py, pz), (sx, sy, sz), mt in parts:
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x + px, y + py, pz))
        c = bpy.context.active_object
        c.scale = (sx, sy, sz)
        c.data.materials.append(mt)
        c.name = "Player"


def point(name, loc, energy, col, radius=0.06, shadow=True):
    ld = bpy.data.lights.new(name, "POINT")
    ld.energy, ld.color, ld.shadow_soft_size = energy, col, radius
    ld.use_shadow = shadow
    o = link(bpy.data.objects.new(name, ld))
    o.location = loc
    return o


def spot(name, loc, energy, ang, col):
    ld = bpy.data.lights.new(name, "SPOT")
    ld.energy, ld.color = energy, col
    ld.spot_size, ld.spot_blend = math.radians(ang), 0.75
    ld.use_shadow = False
    o = link(bpy.data.objects.new(name, ld))
    o.location = loc
    return o


def flame(loc):
    """Review-only flame stand-in (never exported)."""
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.05, location=loc + Vector((0, 0, 0.07)), segments=12, ring_count=8)
    f = bpy.context.active_object
    f.scale = (1, 1, 2.2)
    m = bpy.data.materials.new("FlameRV")
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    e = nt.nodes.new("ShaderNodeEmission")
    e.inputs["Color"].default_value = (1.0, 0.55, 0.15, 1)
    e.inputs["Strength"].default_value = 30.0
    o = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(e.outputs[0], o.inputs[0])
    f.data.materials.append(m)
    f.visible_shadow = False
    f.name = "FlameRV"
    return f


def lamp_lights(night, k=0):
    pl, fl = PL.copy(), FLAME.copy()
    if k:
        R = turn_mat(k)
        pl, fl = R @ pl, R @ fl
    out = [point("InLight", pl, 40.0, lin((255, 150, 60)))]
    if night:
        out.append(spot("GroundSpot", GROUNDL, 2500.0, 110.0, lin((255, 176, 104))))
        out.append(flame(fl))
    return out


def turn_mat(k):
    return Matrix.Translation((0, HANG_Y, 0)) @ Matrix.Rotation(math.radians(90 * k), 4, "Z") @ \
        Matrix.Translation((0, -HANG_Y, 0))


def turn_pumpkin(objs, k):
    objs["Pumpkin"].matrix_world = turn_mat(k) @ objs["Pumpkin"].matrix_world
    for o in bpy.context.scene.objects:
        if o.name.startswith(("InLight", "FlameRV")):
            o.matrix_world = turn_mat(k) @ o.matrix_world


def night_world(sc):
    w = sc.world
    w.use_nodes = True
    nt = w.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputWorld")
    bl = nt.nodes.new("ShaderNodeBackground")
    bl.inputs["Color"].default_value = (0.372, 0.372, 0.434, 1)   # builder's calibrated Moonlit fill
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["Generated"], sep.inputs["Vector"])
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].color = (*lin((58, 72, 138)), 1)
    ramp.color_ramp.elements[1].position = 0.55
    ramp.color_ramp.elements[1].color = (*lin((16, 22, 62)), 1)
    nt.links.new(sep.outputs["Z"], ramp.inputs["Fac"])
    bs = nt.nodes.new("ShaderNodeBackground")
    nt.links.new(ramp.outputs["Color"], bs.inputs["Color"])
    lp = nt.nodes.new("ShaderNodeLightPath")
    mx = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(lp.outputs["Is Camera Ray"], mx.inputs["Fac"])
    nt.links.new(bl.outputs[0], mx.inputs[1])
    nt.links.new(bs.outputs[0], mx.inputs[2])
    nt.links.new(mx.outputs[0], out.inputs[0])
    for o in [o for o in sc.objects if o.type == "LIGHT" and o.data.type == "SUN"]:
        bpy.data.objects.remove(o)
    ld = bpy.data.lights.new("Moon", "SUN")
    ld.energy, ld.color = 1.0909, (0.857, 0.857, 1.0)
    mo = link(bpy.data.objects.new("Moon", ld))
    mo.rotation_euler = (math.radians(40), 0, math.radians(-35))
    sc.view_settings.view_transform = "Standard"


def scene(night=False, res=(1920, 1080)):
    sc = fresh(16)
    review_setup(res=res)
    sc.eevee.taa_render_samples = 64
    objs = import_lamp()
    roblox_mats(objs)
    ground()
    if night:
        night_world(sc)
    lamp_lights(night)
    return sc, objs


def shot(name, loc, tgt, vfov=70.0, res=None):
    sc = bpy.context.scene
    if res:
        sc.render.resolution_x, sc.render.resolution_y = res
    cd = bpy.data.cameras.new("Cam")
    cam = link(bpy.data.objects.new("Cam", cd))
    cam.location = Vector(loc)
    cam.rotation_euler = (Vector(tgt) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    cd.sensor_fit = "VERTICAL"
    cd.angle_y = math.radians(vfov)
    cd.clip_start, cd.clip_end = 0.05, 5000
    sc.camera = cam
    p = os.path.join(OUT, name + ".png")
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(cam)
    log("shot", p)
    return p


AIM = Vector((0, -1.8, 9.5))


def eye(direction, dist, frm=Vector((0, HANG_Y, 0))):
    d = Vector((direction[0], direction[1], 0)).normalized()
    return Vector((frm.x + d.x * dist, frm.y + d.y * dist, 5.0))


# ------------------------------------------------------------------ stats
def step_stats():
    fresh(8)
    objs = import_lamp()
    rep = {}
    tot = 0
    for n, o in sorted(objs.items()):
        me = o.data
        me.calc_loop_triangles()
        tris = len(me.loop_triangles)
        tot += tris
        M = np.array(o.matrix_world)
        co = np.empty(len(me.vertices) * 3, np.float32)
        me.vertices.foreach_get("co", co)
        co = co.reshape(-1, 3)
        w = (np.c_[co, np.ones(len(co))] @ M.T)[:, :3]
        imgs = []
        for m in me.materials:
            if not m or not m.node_tree:
                continue
            for nd in m.node_tree.nodes:
                if nd.type == "TEX_IMAGE" and nd.image:
                    to = [l.to_socket.name + "@" + l.to_node.type for l in nd.outputs["Color"].links] + \
                         [l.to_socket.name + "@" + l.to_node.type for l in nd.outputs["Alpha"].links]
                    imgs.append(dict(name=nd.image.name, size=list(nd.image.size), packed=nd.image.packed_file is not None,
                                     to=to))
        # edge (dihedral) angles on the world-space mesh
        bm = bmesh.new()
        bm.from_mesh(me)
        bm.transform(o.matrix_world)
        bm.normal_update()
        angs, zs = [], []
        for e in bm.edges:
            if len(e.link_faces) == 2:
                a = e.calc_face_angle(None)
                if a is not None:
                    angs.append(math.degrees(a))
                    zs.append((e.verts[0].co + e.verts[1].co) / 2)
        angs = np.array(angs)
        # UV stretch: per-triangle singular values of the 3D->UV Jacobian
        uvl = me.uv_layers.active
        an = []
        dens = []
        if uvl:
            uv = np.empty(len(me.loops) * 2, np.float32)
            uvl.data.foreach_get("uv", uv)
            uv = uv.reshape(-1, 2)
            for t in me.loop_triangles:
                P = [Vector(w[me.loops[li].vertex_index]) for li in t.loops]
                U = [uv[li] for li in t.loops]
                e1, e2 = P[1] - P[0], P[2] - P[0]
                a3 = e1.cross(e2).length / 2
                if a3 < 1e-7:
                    continue
                ex = e1.normalized()
                ey = e1.cross(e2).cross(e1).normalized()
                p = np.array([[e1.dot(ex), e2.dot(ex)], [e1.dot(ey), e2.dot(ey)]])
                q = np.array([U[1] - U[0], U[2] - U[0]]).T
                try:
                    J = q @ np.linalg.inv(p)
                except np.linalg.LinAlgError:
                    continue
                s = np.linalg.svd(J, compute_uv=False)
                cz = (P[0].z + P[1].z + P[2].z) / 3
                if s[1] < 1e-9:
                    an.append((99.0, a3, cz))
                    continue
                an.append((s[0] / s[1], a3, cz))
                dens.append((math.sqrt(s[0] * s[1]), a3))
        an = np.array(an) if an else np.zeros((1, 3))
        dens = np.array(dens) if dens else np.zeros((1, 2))
        area = an[:, 1].sum() or 1
        bad = an[an[:, 0] > 4]
        zh = np.histogram(bad[:, 2], bins=np.arange(0, 20, 1.0), weights=bad[:, 1])[0] if len(bad) else []
        aniso_z = {int(i): round(float(v / area), 3) for i, v in enumerate(zh) if v / area > 0.01}
        res = max([i["size"][0] for i in imgs] or [0])
        rep[n] = dict(tris=tris, verts=len(me.vertices), min=w.min(0).round(3).tolist(), max=w.max(0).round(3).tolist(),
                      size=(w.max(0) - w.min(0)).round(3).tolist(), loc=list(o.location), scale=list(o.scale),
                      rot=[round(math.degrees(r), 2) for r in o.rotation_euler], images=imgs,
                      edge_angle_p50=round(float(np.percentile(angs, 50)), 1),
                      edge_angle_p95=round(float(np.percentile(angs, 95)), 1),
                      edges_over_30=int((angs > 30).sum()), edges_over_45=int((angs > 45).sum()), edges=len(angs),
                      uv_aniso_area_over2=round(float(an[an[:, 0] > 2, 1].sum() / area), 3),
                      uv_aniso_area_over4=round(float(an[an[:, 0] > 4, 1].sum() / area), 3),
                      uv_aniso4_area_by_z=aniso_z,
                      texel_px_per_stud_median=round(float(np.median(dens[:, 0]) * res), 1) if res else None,
                      sharp_edges=int(sum(1 for e in me.edges if e.use_edge_sharp)),
                      custom_normals=me.has_custom_normals)
        bm.free()
    rep["total_tris"] = tot
    with open(os.path.join(OUT, "stats.json"), "w") as fh:
        json.dump(rep, fh, indent=1)
    log(json.dumps(rep, indent=1))


# ------------------------------------------------------------------ day
def step_day():
    sc, objs = scene(False)
    blockman(3.0, -6.0)
    # face side (-Y) at 25 and 40, player eye height
    shot("D01_front25", eye((0, -1), 25), AIM)
    shot("D02_front40", eye((0, -1), 40), AIM)
    # along the path (+X), face default (edge-on) at 25 and 40
    shot("D03_side25_default", eye((1, 0), 25), AIM)
    shot("D04_side40_default", eye((1, 0), 40), AIM)
    # 3/4
    shot("D05_34_30", eye((0.7, -0.7), 30), AIM)
    shot("D06_back34_30", eye((-0.6, 0.8), 30), AIM)
    # head close-ups ~8 studs
    shot("D07_head8_front", HEAD + Vector((0, -7.6, -2.4)), HEAD, vfov=30, res=(1600, 1200))
    shot("D08_head8_34below", HEAD + Vector((5.0, -5.0, -3.6)), HEAD, vfov=30, res=(1600, 1200))
    # walker standing on the path, 6 studs off the head, looking up
    shot("D09_walker_under", Vector((6.0, -5.25, 5.0)), HEAD + Vector((0, 0, 0.3)), vfov=70)
    shot("D10_crook10", Vector((10.0, -2.0, 13.5)), Vector((0, -1.9, 16.0)), vfov=35, res=(1600, 1200))
    shot("D11_base6", Vector((-3.5, -5.0, 3.2)), Vector((0, 0, 1.2)), vfov=40, res=(1600, 1200))
    # face turned toward the path camera (+X), the lead's recommended placement
    turn_pumpkin(objs, 1)
    shot("D12_side25_faceturned", eye((1, 0), 25), AIM)
    shot("D13_side40_faceturned", eye((1, 0), 40), AIM)
    shot("D14_head8_side_faceturned", HEAD + Vector((7.6, 0.0, -2.4)), HEAD, vfov=30, res=(1600, 1200))
    turn_pumpkin(objs, -1)
    # inner light OFF (worst case / light not yet streamed), face front close
    for o in [o for o in sc.objects if o.name.startswith("InLight")]:
        o.hide_render = True
    shot("D15_head8_front_lightoff", HEAD + Vector((0, -7.6, -2.4)), HEAD, vfov=30, res=(1600, 1200))


# ------------------------------------------------------------------ night
def step_night():
    sc, objs = scene(True)
    blockman(3.0, -6.0)
    shot("N01_front25", eye((0, -1), 25), AIM)
    shot("N02_front40", eye((0, -1), 40), AIM)
    shot("N03_head8_front", HEAD + Vector((0, -7.6, -2.4)), HEAD, vfov=30, res=(1600, 1200))
    shot("N04_34_30", eye((0.7, -0.7), 30), AIM)
    turn_pumpkin(objs, 1)
    shot("N05_side25_faceturned", eye((1, 0), 25), AIM)
    shot("N06_side40_faceturned", eye((1, 0), 40), AIM)
    shot("N07_walker_under", Vector((6.0, -5.25, 5.0)), HEAD + Vector((0, 0, 0.3)), vfov=70)


# ------------------------------------------------------------------ checks (clay / albedo-only / normal-only)
def material_variant(m, mode):
    m2 = m.copy()
    nt = m2.node_tree
    bsdf = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    if mode in ("clay", "nrm"):
        for s in ("Base Color", "Roughness", "Metallic"):
            for l in list(bsdf.inputs[s].links):
                nt.links.remove(l)
        bsdf.inputs["Base Color"].default_value = (0.45, 0.45, 0.45, 1)
        bsdf.inputs["Roughness"].default_value = 0.45
        if mode == "clay":
            for l in list(bsdf.inputs["Normal"].links):
                nt.links.remove(l)
    elif mode == "albedo":
        src = bsdf.inputs["Base Color"].links[0].from_socket if bsdf.inputs["Base Color"].links else None
        out = next(n for n in nt.nodes if n.type == "OUTPUT_MATERIAL")
        e = nt.nodes.new("ShaderNodeEmission")
        if src:
            nt.links.new(src, e.inputs["Color"])
        else:
            e.inputs["Color"].default_value = bsdf.inputs["Base Color"].default_value
        if bsdf.inputs["Alpha"].links:
            mx = nt.nodes.new("ShaderNodeMixShader")
            tr = nt.nodes.new("ShaderNodeBsdfTransparent")
            nt.links.new(bsdf.inputs["Alpha"].links[0].from_socket, mx.inputs["Fac"])
            nt.links.new(tr.outputs[0], mx.inputs[1])
            nt.links.new(e.outputs[0], mx.inputs[2])
            nt.links.new(mx.outputs[0], out.inputs["Surface"])
        else:
            nt.links.new(e.outputs[0], out.inputs["Surface"])
    return m2


def set_mode(objs, mode, names=None):
    for n, o in objs.items():
        if names and n not in names:
            continue
        o.data.materials[0] = material_variant(o["orig_mat"], mode) if mode != "orig" else o["orig_mat"]


def step_checks():
    sc, objs = scene(False, res=(1600, 1200))
    for o in objs.values():
        o["orig_mat"] = o.data.materials[0]
    # albedo only (flat, unlit): baked colour faults (dark rims, black patches, seams)
    set_mode(objs, "albedo")
    sc.view_settings.view_transform = "Standard"
    shot("C01_albedo_head_front", HEAD + Vector((0, -6.0, -1.0)), HEAD, vfov=28)
    shot("C02_albedo_head_below", HEAD + Vector((2.0, -4.5, -4.5)), HEAD, vfov=34)
    shot("C03_albedo_crook", Vector((9.0, -2.0, 15.0)), Vector((0, -1.9, 16.0)), vfov=30)
    shot("C04_albedo_base", Vector((-3.0, -4.2, 2.6)), Vector((0, 0, 1.2)), vfov=36)
    shot("C05_albedo_head_top", HEAD + Vector((2.5, -3.0, 4.5)), HEAD, vfov=34)
    # clay (no maps): geometric faceting
    sc.view_settings.view_transform = "AgX"
    set_mode(objs, "clay")
    shot("C06_clay_head_front12", HEAD + Vector((0, -11.0, -4.0)), HEAD, vfov=24)
    shot("C07_clay_head_34_8", HEAD + Vector((5.0, -5.0, -3.6)), HEAD, vfov=30)
    shot("C08_clay_crook12", Vector((12.0, -2.0, 13.0)), Vector((0, -1.9, 16.0)), vfov=28)
    shot("C09_clay_base8", Vector((-4.5, -6.0, 4.0)), Vector((0, 0, 1.2)), vfov=32)
    shot("C10_clay_full25_side", eye((1, 0), 25), AIM)
    # normal map only on grey: normal-map seams / artefacts
    set_mode(objs, "nrm")
    shot("C11_nrm_head_front", HEAD + Vector((0, -6.0, -1.0)), HEAD, vfov=28)
    shot("C12_nrm_crook", Vector((9.0, -2.0, 15.0)), Vector((0, -1.9, 16.0)), vfov=30)
    shot("C13_nrm_base", Vector((-3.0, -4.2, 2.6)), Vector((0, 0, 1.2)), vfov=36)
    shot("C14_nrm_mid_pole", Vector((-3.0, -3.5, 7.0)), Vector((0, 0, 7.5)), vfov=36)


# ------------------------------------------------------------------ silhouettes
def step_sil():
    sc = fresh(8)
    sc.render.engine = "BLENDER_EEVEE"
    sc.render.resolution_x, sc.render.resolution_y = 1920, 1080
    sc.view_settings.view_transform = "Standard"
    w = sc.world
    w.use_nodes = True
    w.node_tree.nodes["Background"].inputs["Color"].default_value = (1, 1, 1, 1)
    w.node_tree.nodes["Background"].inputs["Strength"].default_value = 1.0
    objs = import_lamp()
    blk = bpy.data.materials.new("Blk")
    blk.use_nodes = True
    nt = blk.node_tree
    nt.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0, 0, 0, 1)
    nt.nodes["Principled BSDF"].inputs["Roughness"].default_value = 1.0
    nt.nodes["Principled BSDF"].inputs["Specular IOR Level"].default_value = 0.0
    for n, o in objs.items():
        if n == "WebSilk":
            m = o.data.materials[0]
            m.surface_render_method = "BLENDED"
            bsdf = next(x for x in m.node_tree.nodes if x.type == "BSDF_PRINCIPLED")
            for l in list(bsdf.inputs["Base Color"].links):
                m.node_tree.links.remove(l)
            bsdf.inputs["Base Color"].default_value = (0, 0, 0, 1)
            bsdf.inputs["Specular IOR Level"].default_value = 0.0
        else:
            o.data.materials[0] = blk
    blockman(3.0, -6.0)
    for o in sc.objects:
        if o.name.startswith("Player"):
            o.data.materials[0] = blk
    shot("S01_sil_side40", eye((1, 0), 40), AIM)
    shot("S02_sil_front40", eye((0, -1), 40), AIM)
    shot("S03_sil_34_40", eye((0.7, -0.7), 40), AIM)


def step_extra():
    sc, objs = scene(False)
    blockman(3.0, -6.0)
    # typical Roblox 3rd-person camera: ~12 studs back, ~8 up, player walking past the base
    shot("E01_base_3rdperson12", Vector((-7.0, -9.5, 7.5)), Vector((0, 0, 2.0)), vfov=70, res=(1920, 1080))
    turn_pumpkin(objs, 1)
    shot("E02_side40_faceturned_1080", eye((1, 0), 40), AIM, res=(1920, 1080))
    # base with sun shadows off: separates geometry/normal faults from shadow-terminator artefacts
    for o in sc.objects:
        if o.type == "LIGHT" and o.data.type == "SUN":
            o.data.use_shadow = False
    shot("E03_base6_noshadow", Vector((-3.5, -5.0, 3.2)), Vector((0, 0, 1.2)), vfov=40, res=(1600, 1200))
    for o in sc.objects:
        if o.type == "LIGHT" and o.data.type == "SUN":
            o.data.use_shadow = True
    # interior lit like Roblox (no ambient occlusion of the cavity): flat bright world, sun off, inside light on
    for o in sc.objects:
        if o.type == "LIGHT" and o.data.type == "SUN":
            o.data.energy = 0.0
    shot("E04_head8_faceturned_ambientonly", HEAD + Vector((7.6, 0.0, -2.4)), HEAD, vfov=30, res=(1600, 1200))
    sc2, objs2 = scene(True)
    turn_pumpkin(objs2, 1)
    shot("E05_night_side40_faceturned_1080", eye((1, 0), 40), AIM, res=(1920, 1080))


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    step = argv[0] if argv else "stats"
    {"stats": step_stats, "day": step_day, "night": step_night, "checks": step_checks, "sil": step_sil, "extra": step_extra}[step]()
    log("done", step)
