# SLINGSHOT Halloween hub decoration - shared Blender kit (2026-10-12).
# HQ game-art pipeline (same as Weather/Meteor/HQ/build_hq.py): dense procedural sculpt with per-vertex colour /
# roughness + procedural shaders -> game mesh (decimated, Smart UV) -> Cycles bakes (tangent normal, colour x AO,
# roughness) -> FBX with embedded textures -> Studio 3D importer (creator ZAB Studio) builds the SurfaceAppearance.
# Units: 1 Blender metre = 1 Roblox stud (FBX global_scale 0.01). Blender +Y = Roblox -Z (the side that faces the hub).
# No Neon / emissive (owner rule): every "glow" is a Roblox particle or light.
import bpy, bmesh, math, os, random
from mathutils import Vector, noise
import numpy as np

HERE = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween"
CDIMP = r"C:\cdimp"


def lin(c):
    """sRGB 0-255 -> linear 0-1."""
    def f(x):
        x /= 255.0
        return x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4
    return tuple(f(v) for v in c)


def smoothstep(a, b, x):
    t = max(0.0, min(1.0, (x - a) / (b - a)))
    return t * t * (3 - 2 * t)


def fbm(p, octaves, lac=2.03, gain=0.5):
    s, a, f = 0.0, 1.0, 1.0
    for _ in range(octaves):
        s += a * noise.noise(p * f)
        a *= gain
        f *= lac
    return s


def mix(a, b, t):
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(len(a)))


def fresh(samples=24):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = samples
    sc.world = bpy.data.worlds.new("W")
    return sc


def link(ob):
    bpy.context.scene.collection.objects.link(ob)
    return ob


def only(ob):
    for o in bpy.context.scene.objects:
        o.select_set(False)
    ob.select_set(True)
    bpy.context.view_layer.objects.active = ob


def mesh_from(ob, name):
    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(ob.evaluated_get(dg))
    me.name = name
    return me


def apply_mods(ob):
    me = mesh_from(ob, ob.data.name)
    ob.modifiers.clear()
    ob.data = me
    return ob


def obj_from_bm(bm, name, smooth=True):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    if smooth:
        for p in me.polygons:
            p.use_smooth = True
    return link(bpy.data.objects.new(name, me))


def set_colors(me, name, values):
    """values: list of (r, g, b) per vertex (linear)."""
    ca = me.color_attributes.new(name, "FLOAT_COLOR", "POINT")
    arr = np.ones((len(values), 4), dtype=np.float32)
    arr[:, :3] = np.array(values, dtype=np.float32)
    ca.data.foreach_set("color", arr.ravel())


def quad_bezier(a, c, b, n):
    out = []
    for i in range(n + 1):
        t = i / n
        out.append(((1 - t) ** 2 * a[0] + 2 * (1 - t) * t * c[0] + t * t * b[0],
                    (1 - t) ** 2 * a[1] + 2 * (1 - t) * t * c[1] + t * t * b[1]))
    return out


# ------------------------------------------------------------------ materials for the sculpt
def mat_vc(name, col="Col", rough="Rough", metallic=0.0):
    """Principled driven by colour attributes (the sculpt's per-vertex colour + roughness)."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    vc = nt.nodes.new("ShaderNodeVertexColor")
    vc.layer_name = col
    nt.links.new(vc.outputs["Color"], bsdf.inputs["Base Color"])
    if rough:
        vr = nt.nodes.new("ShaderNodeVertexColor")
        vr.layer_name = rough
        sep = nt.nodes.new("ShaderNodeSeparateColor")
        nt.links.new(vr.outputs["Color"], sep.inputs["Color"])
        nt.links.new(sep.outputs["Red"], bsdf.inputs["Roughness"])
    bsdf.inputs["Metallic"].default_value = metallic
    return m


def mat_noise(name, c1, c2, scale=(1, 1, 1), nscale=4.0, detail=6.0, rough=0.6, lo=0.35, hi=0.65,
              bump=0.0, coords="Object"):
    """Procedural two-colour material (object-space noise stretched by `scale`)."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = scale
    nt.links.new(tc.outputs[coords], mp.inputs["Vector"])
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = nscale
    nz.inputs["Detail"].default_value = detail
    nt.links.new(mp.outputs["Vector"], nz.inputs["Vector"])
    cr = nt.nodes.new("ShaderNodeValToRGB")
    cr.color_ramp.elements[0].position = lo
    cr.color_ramp.elements[0].color = (*c1, 1)
    cr.color_ramp.elements[1].position = hi
    cr.color_ramp.elements[1].color = (*c2, 1)
    nt.links.new(nz.outputs["Fac"], cr.inputs["Fac"])
    nt.links.new(cr.outputs["Color"], bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = rough
    if bump > 0:
        bp = nt.nodes.new("ShaderNodeBump")
        bp.inputs["Strength"].default_value = bump
        nt.links.new(nz.outputs["Fac"], bp.inputs["Height"])
        nt.links.new(bp.outputs["Normal"], bsdf.inputs["Normal"])
    return m


def mat_flat(name, col, rough=0.5, metallic=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*col, 1)
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metallic
    return m


# ------------------------------------------------------------------ the game mesh
def decimate_copy(hi, name, target):
    lo = link(bpy.data.objects.new(name, hi.data.copy()))
    lo.location = hi.location
    dec = lo.modifiers.new("Decimate", "DECIMATE")
    dec.ratio = min(1.0, target / max(1, len(hi.data.polygons)))
    lo.modifiers.new("Tri", "TRIANGULATE")
    apply_mods(lo)
    me = lo.data
    me.name = name
    for a in list(me.color_attributes):
        me.color_attributes.remove(a)
    for p in me.polygons:
        p.use_smooth = True
    return lo


def split_faces(ob, groups):
    """groups: {name: predicate(face, bm) -> bool}, first match wins. Returns {name: object}. ob is consumed."""
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    bm.faces.ensure_lookup_table()
    assign = {}
    for f in bm.faces:
        for nm, pred in groups.items():
            if pred(f):
                assign.setdefault(nm, []).append(f.index)
                break
    out = {}
    for nm, idx in assign.items():
        b2 = bm.copy()
        b2.faces.ensure_lookup_table()
        keep = set(idx)
        bmesh.ops.delete(b2, geom=[f for f in b2.faces if f.index not in keep], context="FACES")
        o = obj_from_bm(b2, nm, smooth=False)  # keep the source's smooth/sharp flags
        o.location = ob.location
        out[nm] = o
    bm.free()
    bpy.data.objects.remove(ob)
    return out


def smart_uv(ob, angle=66, margin=0.003):
    only(ob)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.smart_project(angle_limit=math.radians(angle), island_margin=margin)
    bpy.ops.object.mode_set(mode="OBJECT")


# ------------------------------------------------------------------ bakes
def fill_misses(arr, hit, iters=32):
    """Grow hit pixels into miss pixels (4-neighbour average), then fill any rest with the hit mean."""
    a = arr.copy()
    h = hit.copy()
    for _ in range(iters):
        if h.all():
            break
        acc = np.zeros_like(a)
        cnt = np.zeros(h.shape, np.float32)
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            hs = np.roll(h, (dy, dx), (0, 1))
            acc += np.roll(a, (dy, dx), (0, 1)) * hs[..., None]
            cnt += hs
        new = (~h) & (cnt > 0)
        a[new] = acc[new] / cnt[new][:, None]
        h |= new
    if not h.all() and hit.any():
        a[~h] = a[hit].mean(0)
    return a


def save_png(img, path):
    img.filepath_raw = path
    img.file_format = "PNG"
    img.save()


def bake_set(lo, hi_list, size, prefix, cage, maxray, ao_strength=0.6, ao_dist=1.0, outdir=None):
    """Bake hi_list (selected) -> lo (active): normal, AO, colour, roughness. AO is multiplied into the colour."""
    sc = bpy.context.scene
    outdir = outdir or os.path.join(HERE, "maps")
    os.makedirs(outdir, exist_ok=True)
    imgs = {}
    for key, cs in (("albedo", "sRGB"), ("normal", "Non-Color"), ("rough", "Non-Color"), ("ao", "Non-Color")):
        img = bpy.data.images.new(prefix + "_" + key, size, size, alpha=False)
        img.colorspace_settings.name = cs
        imgs[key] = img
    mat = bpy.data.materials.new(prefix + "_bake")
    mat.use_nodes = True
    nt = mat.node_tree
    tex = nt.nodes.new("ShaderNodeTexImage")
    lo.data.materials.clear()
    lo.data.materials.append(mat)
    sc.world.light_settings.distance = ao_dist
    for o in sc.objects:
        o.select_set(False)
    for h in hi_list:
        h.hide_render = False
        h.select_set(True)
    lo.select_set(True)
    bpy.context.view_layer.objects.active = lo

    def run(kind, img, **kw):
        tex.image = img
        nt.nodes.active = tex
        bpy.ops.object.bake(type=kind, use_selected_to_active=True, cage_extrusion=cage,
                            max_ray_distance=maxray, margin=6, **kw)

    run("NORMAL", imgs["normal"], normal_space="TANGENT")
    run("AO", imgs["ao"])
    run("DIFFUSE", imgs["albedo"], pass_filter={"COLOR"})
    run("ROUGHNESS", imgs["rough"])
    # hit mask: rays that pass through a hole / past an edge MISS and Cycles writes black there (= a black normal,
    # black AO, black colour: the serrated dark rims seen around the carved holes). Bake EMIT with white emission on
    # every sculpt material -> 0 = miss; misses get a flat normal, AO 1 and colour/roughness grown in from neighbours.
    mask = bpy.data.images.new(prefix + "_mask", size, size, alpha=False)
    mask.colorspace_settings.name = "Non-Color"
    saved = []
    for h in hi_list:
        for m in h.data.materials:
            if m and m.use_nodes:
                for n in m.node_tree.nodes:
                    if n.type == "BSDF_PRINCIPLED":
                        saved.append((n, tuple(n.inputs["Emission Color"].default_value),
                                      n.inputs["Emission Strength"].default_value,
                                      [l for l in m.node_tree.links if l.to_socket == n.inputs["Emission Color"]]))
                        for l in saved[-1][3]:
                            m.node_tree.links.remove(l)
                        n.inputs["Emission Color"].default_value = (1, 1, 1, 1)
                        n.inputs["Emission Strength"].default_value = 1.0
    run("EMIT", mask)
    for n, col, strength, _links in saved:
        n.inputs["Emission Color"].default_value = col
        n.inputs["Emission Strength"].default_value = strength
    hit = np.array(mask.pixels[:], dtype=np.float32).reshape(size, size, 4)[..., 0] > 0.5
    shp = (size, size, 4)
    nrm = np.array(imgs["normal"].pixels[:], dtype=np.float32).reshape(shp)
    nrm[~hit] = (0.5, 0.5, 1.0, 1.0)
    imgs["normal"].pixels[:] = nrm.ravel()
    ao = np.array(imgs["ao"].pixels[:], dtype=np.float32).reshape(shp)
    ao[~hit] = 1.0
    imgs["ao"].pixels[:] = ao.ravel()
    for key in ("albedo", "rough"):
        arr = fill_misses(np.array(imgs[key].pixels[:], dtype=np.float32).reshape(shp), hit)
        imgs[key].pixels[:] = arr.ravel()
    a = np.array(imgs["albedo"].pixels[:], dtype=np.float32).reshape(-1, 4)
    o = ao.reshape(-1, 4)
    a[:, :3] *= (1 - ao_strength) + ao_strength * o[:, :1]
    imgs["albedo"].pixels[:] = a.ravel()
    imgs["miss_fraction"] = float(1 - hit.mean())
    for key in ("albedo", "normal", "rough", "ao"):
        save_png(imgs[key], os.path.join(outdir, f"{prefix}_{key}.png"))
    return imgs


def pbr_material(lo, name, imgs):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    t_a = nt.nodes.new("ShaderNodeTexImage")
    t_a.image = imgs["albedo"]
    nt.links.new(t_a.outputs["Color"], bsdf.inputs["Base Color"])
    t_n = nt.nodes.new("ShaderNodeTexImage")
    t_n.image = imgs["normal"]
    nmap = nt.nodes.new("ShaderNodeNormalMap")
    nt.links.new(t_n.outputs["Color"], nmap.inputs["Color"])
    nt.links.new(nmap.outputs["Normal"], bsdf.inputs["Normal"])
    t_r = nt.nodes.new("ShaderNodeTexImage")
    t_r.image = imgs["rough"]
    # linked straight in (a Separate node in between stops the FBX exporter from embedding the roughness map)
    nt.links.new(t_r.outputs["Color"], bsdf.inputs["Roughness"])
    bsdf.inputs["Metallic"].default_value = 0.0
    lo.data.materials.clear()
    lo.data.materials.append(m)


# ------------------------------------------------------------------ review renders + export
def review_setup(res=(1400, 1000), sky=(0.36, 0.5, 0.72), sky_strength=0.8, sun=4.0):
    sc = bpy.context.scene
    sc.render.engine = "BLENDER_EEVEE"
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.view_settings.view_transform = "AgX"
    sc.render.film_transparent = False
    w = sc.world
    w.use_nodes = True
    w.node_tree.nodes["Background"].inputs["Color"].default_value = (*sky, 1)
    w.node_tree.nodes["Background"].inputs["Strength"].default_value = sky_strength
    ld = bpy.data.lights.new("Sun", "SUN")
    ld.energy, ld.color = sun, (1, 0.96, 0.9)
    lo = link(bpy.data.objects.new("Sun", ld))
    lo.rotation_euler = (math.radians(50), 0, math.radians(30))
    return sc


def shoot(path, target, direction, dist, lens=50, up_target=None):
    sc = bpy.context.scene
    cd = bpy.data.cameras.new("Cam")
    cam = link(bpy.data.objects.new("Cam", cd))
    cam.location = Vector(target) + Vector(direction).normalized() * dist
    cam.rotation_euler = (Vector(target) - cam.location).to_track_quat("-Z", "Y").to_euler()
    cd.lens = lens
    cd.clip_end = 5000
    sc.camera = cam
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(cam)
    return path


FBX_ARGS = dict(use_selection=True, global_scale=0.01, apply_unit_scale=True, apply_scale_options="FBX_SCALE_NONE",
                axis_forward="-Z", axis_up="Y", object_types={"MESH"}, use_mesh_modifiers=True,
                mesh_smooth_type="FACE", add_leaf_bones=False, bake_anim=False, path_mode="COPY",
                embed_textures=True)


def export_fbx(objs, path):
    for o in bpy.context.scene.objects:
        o.select_set(o in objs)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.export_scene.fbx(filepath=path, **FBX_ARGS)
    return {"fbx": path, "kb": round(os.path.getsize(path) / 1024, 1),
            "tris": {o.name: len(o.data.polygons) for o in objs}}
