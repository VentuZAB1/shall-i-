# Cvetibara export: bake vertex colours (x soft AO) into one texture, then a Roblox-ready skinned FBX
# (Armature + Body + Glow_ffc840) like Claude Design/_pipeline/cd_build.py, plus the CreatureClips Luau module.
import bpy, os, json
import numpy as np

OUT = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\FriendPets\Cvetibara"
IMP = r"C:\cdimp"
NAME = "Cvetibara"
TEX = 1024


def bake_body(body):
    sc = bpy.context.scene
    old_engine = sc.render.engine
    sc.render.engine = "CYCLES"
    sc.cycles.samples = 64
    sc.cycles.device = "CPU"
    # UVs
    me = body.data
    if not me.uv_layers:
        me.uv_layers.new(name="UVMap")
    for o in bpy.context.view_layer.objects:
        o.select_set(False)
    body.select_set(True)
    bpy.context.view_layer.objects.active = body
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.smart_project(angle_limit=1.15, island_margin=0.012)
    bpy.ops.object.mode_set(mode="OBJECT")
    # bake material: emission = vertex colour; the active image node is the bake target
    col_img = bpy.data.images.get(NAME + "_col") or bpy.data.images.new(NAME + "_col", TEX, TEX)
    ao_img = bpy.data.images.get(NAME + "_ao") or bpy.data.images.new(NAME + "_ao", TEX, TEX)
    bm = bpy.data.materials.new("BakeMat")
    bm.use_nodes = True
    nt = bm.node_tree
    nt.nodes.clear()
    outn = nt.nodes.new("ShaderNodeOutputMaterial")
    em = nt.nodes.new("ShaderNodeEmission")
    vc = nt.nodes.new("ShaderNodeVertexColor")
    vc.layer_name = "Col"
    nt.links.new(vc.outputs["Color"], em.inputs["Color"])
    nt.links.new(em.outputs["Emission"], outn.inputs["Surface"])
    imgn = nt.nodes.new("ShaderNodeTexImage")
    nt.nodes.active = imgn
    old_mats = list(me.materials)
    me.materials.clear()
    me.materials.append(bm)
    # hide everything else so the AO only comes from the creature itself
    hidden = []
    for o in bpy.context.view_layer.objects:
        if o is not body and o.type == "MESH" and not o.hide_render:
            o.hide_render = True
            hidden.append(o)
    imgn.image = col_img
    bpy.ops.object.bake(type="EMIT", margin=6)
    sc.cycles.samples = 96
    imgn.image = ao_img
    sc.world.light_settings.distance = 0.6
    bpy.ops.object.bake(type="AO", margin=6)
    for o in hidden:
        o.hide_render = False
    # final = colour x (0.72 + 0.28 AO). Byte images bake straight into sRGB, so .pixels are already sRGB.
    c = np.array(col_img.pixels[:], dtype=np.float32).reshape(-1, 4)
    a = np.array(ao_img.pixels[:], dtype=np.float32).reshape(-1, 4)[:, :1]
    srgb = c[:, :3] * (0.72 + 0.28 * a)
    final = bpy.data.images.get(NAME + "_tex") or bpy.data.images.new(NAME + "_tex", TEX, TEX)
    final.colorspace_settings.name = "sRGB"
    px = np.concatenate([np.clip(srgb, 0, 1), np.ones((srgb.shape[0], 1), np.float32)], axis=1)
    final.pixels[:] = px.ravel().tolist()
    path = os.path.join(OUT, NAME + "_tex.png")
    final.filepath_raw = path
    final.file_format = "PNG"
    final.save()
    # final material: the texture as base colour
    fm = bpy.data.materials.get(NAME + "_Body") or bpy.data.materials.new(NAME + "_Body")
    fm.use_nodes = True
    fnt = fm.node_tree
    fnt.nodes.clear()
    fo = fnt.nodes.new("ShaderNodeOutputMaterial")
    pb = fnt.nodes.new("ShaderNodeBsdfPrincipled")
    ti = fnt.nodes.new("ShaderNodeTexImage")
    ti.image = bpy.data.images.load(path, check_existing=True)
    fnt.links.new(ti.outputs["Color"], pb.inputs["Base Color"])
    fnt.links.new(pb.outputs["BSDF"], fo.inputs["Surface"])
    me.materials.clear()
    me.materials.append(fm)
    bpy.data.materials.remove(bm)
    sc.render.engine = old_engine
    return path


def export(arm, body, glow):
    os.makedirs(IMP, exist_ok=True)
    arm.data.pose_position = "REST"
    bpy.context.view_layer.update()
    tex = bake_body(body)
    gm = bpy.data.materials.get("Glow_ffc840") or bpy.data.materials.new("Glow_ffc840")
    gm.diffuse_color = (1.0, 0.578, 0.051, 1)
    glow.data.materials.clear()
    glow.data.materials.append(gm)
    for o in bpy.context.view_layer.objects:
        o.select_set(False)
    for o in (arm, body, glow):
        o.select_set(True)
    bpy.context.view_layer.objects.active = arm
    fbx = os.path.join(IMP, NAME + ".fbx")
    bpy.ops.export_scene.fbx(filepath=fbx, use_selection=True, add_leaf_bones=False, bake_anim=False,
                             path_mode="COPY", embed_textures=True, object_types={"ARMATURE", "MESH"},
                             mesh_smooth_type="FACE")
    bpy.ops.export_scene.fbx(filepath=os.path.join(OUT, NAME + ".fbx"), use_selection=True, add_leaf_bones=False,
                             bake_anim=False, path_mode="COPY", embed_textures=True,
                             object_types={"ARMATURE", "MESH"}, mesh_smooth_type="FACE")
    arm.data.pose_position = "POSE"
    return {"fbx": fbx, "tex": tex, "size_kb": round(os.path.getsize(fbx) / 1024, 1)}


# ------------------------------------------------------------------ clips JSON -> Luau (same packing as cd_luau.py)
ALPHA = "".join(chr(c) for c in range(33, 127) if c not in (34, 92))
B = len(ALPHA)
LEVELS = B * B - 1


def enc(v):
    v = max(-1.0, min(1.0, v))
    i = round((v + 1) / 2 * LEVELS)
    return ALPHA[i // B] + ALPHA[i % B]


def pack_q(seq):
    out = []
    for k in range(0, len(seq), 4):
        x, y, z, w = seq[k:k + 4]
        if w < 0:
            x, y, z = -x, -y, -z
        out.append(enc(x) + enc(y) + enc(z))
    return "".join(out)


def luau():
    d = json.load(open(os.path.join(OUT, NAME + ".json")))
    L = ["-- generated by FriendPets/Cvetibara/cvetibara_export.py from the Blender clips. Do not edit by hand.",
         "return {", f'\tfps = {d["fps"]}, rig = "cd", style = "cd",',
         f'\tref = {{bone = "{d["ref"]["bone"]}", dist = {d["ref"]["dist"]:.5f}}},', "\tclips = {"]
    for cn, c in d["clips"].items():
        L.append(f'\t\t{cn} = {{n = {c["n"]}, loop = {"true" if c["loop"] else "false"}, len = {c["len"]:.3f}, '
                 f'stride = {c.get("stride", 0):.4f}, ps = {c["ps"]:.5f},')
        L.append("\t\t\trot = {")
        for b, seq in c["rot"].items():
            L.append(f'\t\t\t\t["{b}"] = "{pack_q(seq)}",')
        L.append("\t\t\t},")
        if c["pos"]:
            L.append("\t\t\tpos = {")
            for b, seq in c["pos"].items():
                L.append(f'\t\t\t\t["{b}"] = "' + "".join(enc(v / c["ps"]) for v in seq) + '",')
            L.append("\t\t\t},")
        L.append("\t\t},")
    L += ["\t},", "\tevents = {},", "}"]
    src = "\n".join(L)
    with open(os.path.join(OUT, NAME + ".lua"), "w", encoding="utf-8") as fh:
        fh.write(src)
    return {"lua_bytes": len(src), "clips": {cn: [c["n"], c["len"]] for cn, c in d["clips"].items()},
            "stride": d["stride"], "height": d["height"], "length": d["length"], "width": d["width"]}


def run():
    arm = bpy.data.objects["Armature"]
    body = bpy.data.objects["Body"]
    glow = bpy.data.objects["Glow_ffc840"]
    info = export(arm, body, glow)
    info.update(luau())
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, NAME + "_rigged.blend"))
    return info
