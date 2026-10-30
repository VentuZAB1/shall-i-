# Render a transparent 512px backpack icon for each egg FBX (baked textures) with a dark outline.
# Run: blender -b --factory-startup -P render_egg_icons.py
import bpy, os, math
from mathutils import Vector

SRC = r"C:\Users\ventu\Downloads\egg_models\export"
OUT = r"C:\Users\ventu\Downloads\egg_models\icons"
os.makedirs(OUT, exist_ok=True)
EGGS = ["WoodEgg", "TideEgg", "StormEgg", "MagmaEgg", "VoidEgg", "CelestialEgg"]
INK = (0.106, 0.122, 0.227, 1)  # #1B1F3A, same ink as the menu icons


def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = "BLENDER_EEVEE_NEXT" if "BLENDER_EEVEE_NEXT" in [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items] else "BLENDER_EEVEE"
    sc.render.film_transparent = True
    sc.render.resolution_x = sc.render.resolution_y = 512
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGBA"
    sc.view_settings.view_transform = "Standard"
    w = bpy.data.worlds.new("W")
    w.use_nodes = True
    w.node_tree.nodes["Background"].inputs[0].default_value = (1, 1, 1, 1)
    w.node_tree.nodes["Background"].inputs[1].default_value = 0.9
    sc.world = w
    return sc


def fix_material(o, egg):
    # bright, lightly-shaded look: baked colour into a principled BSDF + a bit of emission
    part = o.name.split(".")[0]
    img_path = os.path.join(SRC, part + ".png")
    if not os.path.exists(img_path):
        return
    img = bpy.data.images.load(img_path, check_existing=True)
    m = bpy.data.materials.new(part + "_icon")
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = img
    nt.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    nt.links.new(tex.outputs["Color"], bsdf.inputs["Emission Color"])
    bsdf.inputs["Emission Strength"].default_value = 0.35
    bsdf.inputs["Roughness"].default_value = 0.45
    o.data.materials.clear()
    o.data.materials.append(m)


def add_outline(o, thickness):
    ink = bpy.data.materials.get("Ink") or bpy.data.materials.new("Ink")
    ink.use_nodes = True
    ink.use_backface_culling = True
    nt = ink.node_tree
    nt.nodes.clear()
    e = nt.nodes.new("ShaderNodeEmission")
    e.inputs[0].default_value = INK
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(e.outputs[0], out.inputs[0])
    o.data.materials.append(ink)
    s = o.modifiers.new("Outline", "SOLIDIFY")
    s.thickness = thickness
    s.offset = 1
    s.use_flip_normals = True
    s.material_offset = len(o.data.materials) - 1


for egg in EGGS:
    sc = reset()
    bpy.ops.import_scene.fbx(filepath=os.path.join(SRC, egg + ".fbx"))
    meshes = [o for o in sc.objects if o.type == "MESH"]
    # bounds
    pts = [o.matrix_world @ Vector(c) for o in meshes for c in o.bound_box]
    lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    center = (lo + hi) / 2
    size = max(hi - lo)
    for o in meshes:
        fix_material(o, egg)
        add_outline(o, size * 0.022)
    # camera: slightly above, facing the egg's front (-Y in the source blend; try both and keep front)
    cam_data = bpy.data.cameras.new("C")
    cam_data.type = "ORTHO"
    cam_data.ortho_scale = size * 1.18
    cam = bpy.data.objects.new("C", cam_data)
    sc.collection.objects.link(cam)
    d = Vector((0.35, -1, 0.3)).normalized()
    cam.location = center + d * size * 4
    cam.rotation_euler = (center - cam.location).to_track_quat("-Z", "Y").to_euler()
    sc.camera = cam
    for name, rot, energy in (("Key", (math.radians(50), 0, math.radians(30)), 3.5), ("Rim", (math.radians(-60), 0, math.radians(200)), 2.0)):
        l = bpy.data.lights.new(name, "SUN")
        l.energy = energy
        lo_ = bpy.data.objects.new(name, l)
        lo_.rotation_euler = rot
        sc.collection.objects.link(lo_)
    sc.render.filepath = os.path.join(OUT, egg + ".png")
    bpy.ops.render.render(write_still=True)
    print("ICON", egg, size, tuple(round(v, 2) for v in center))
