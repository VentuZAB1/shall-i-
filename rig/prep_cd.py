"""Turn a Claude Design GLB (many flat-coloured / palette-textured parts) into ONE mesh with ONE palette
texture, so rigger.py can skin it like the Meshy models.
blender -b -P prep_cd.py -- <in.glb> <out.glb>
Every face gets the colour of its material (or the texel under its UV centre if the material is
textured); the colours go into a small palette image and the face UVs point at their colour's cell."""
import bpy, bmesh, sys, os
from mathutils import Vector

src, dst = sys.argv[sys.argv.index("--") + 1:][:2]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=src)
bpy.context.scene.frame_set(0)
# rest pose: drop animation so parts sit where the export put them
for o in bpy.context.scene.objects:
    if o.animation_data:
        o.animation_data_clear()
meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
for o in meshes:  # instanced parts (legs, eyes) share mesh data: give each its own copy
    if o.data.users > 1:
        o.data = o.data.copy()


def tex_of(mat):
    if not (mat and mat.use_nodes):
        return None
    for n in mat.node_tree.nodes:
        if n.type == "TEX_IMAGE" and n.image and n.image.size[0] > 0:
            return n.image
    return None


def to_srgb(c):
    return tuple((12.92 * v) if v <= 0.0031308 else (1.055 * v ** (1 / 2.4) - 0.055) for v in c)


def col_of(mat):
    if not mat:
        return (0.6, 0.6, 0.6)
    if mat.use_nodes:
        for n in mat.node_tree.nodes:
            if n.type == "BSDF_PRINCIPLED":
                c = n.inputs["Base Color"].default_value
                e = n.inputs.get("Emission Color")
                es = n.inputs.get("Emission Strength")
                if e is not None and es is not None and es.default_value > 0 and max(e.default_value[:3]) > 0.05:
                    return to_srgb(e.default_value[:3])  # glowing bits keep their glow colour
                return to_srgb(c[:3])
    return to_srgb(mat.diffuse_color[:3])


pix_cache = {}


def sample(img, uv):
    if img.name not in pix_cache:
        pix_cache[img.name] = (img.size[0], img.size[1], list(img.pixels))
    w, h, px = pix_cache[img.name]
    x = min(w - 1, max(0, int((uv.x % 1.0) * w)))
    y = min(h - 1, max(0, int((uv.y % 1.0) * h)))
    i = (y * w + x) * 4
    return tuple(px[i:i + 3])


# per-face colours, collected per object
palette, index = [], {}


def cell(c):
    key = tuple(round(v, 3) for v in c)
    if key not in index:
        index[key] = len(palette)
        palette.append(key)
    return index[key]


face_cells = {}
for o in meshes:
    me = o.data
    uv = me.uv_layers.active
    cells = []
    for poly in me.polygons:
        mat = o.material_slots[poly.material_index].material if o.material_slots else None
        img = tex_of(mat)
        if img and uv:
            ctr = sum((uv.data[li].uv for li in poly.loop_indices), Vector((0, 0))) / poly.loop_total
            c = sample(img, ctr)
        else:
            c = col_of(mat)
        cells.append(cell(c))
    face_cells[o.name] = cells

N = 1
while N * N < len(palette):
    N *= 2
N = max(N, 4)
img = bpy.data.images.new("Palette", N * 4, N * 4)  # 4x4 texels per colour
px = [0.0] * (N * 4 * N * 4 * 4)
for k, c in enumerate(palette):
    cx, cy = k % N, k // N
    for dy in range(4):
        for dx in range(4):
            x, y = cx * 4 + dx, cy * 4 + dy
            i = (y * N * 4 + x) * 4
            # palette holds sRGB values (material colours converted, texture samples already sRGB)
            px[i:i + 4] = [c[0], c[1], c[2], 1.0]
img.pixels = px
img.filepath_raw = os.path.splitext(dst)[0] + "_palette.png"
img.file_format = "PNG"
img.save()

mat = bpy.data.materials.new("PaletteMat")
mat.use_nodes = True
bsdf = mat.node_tree.nodes["Principled BSDF"]
tex = mat.node_tree.nodes.new("ShaderNodeTexImage")
tex.image = img
tex.interpolation = "Closest"
mat.node_tree.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
bsdf.inputs["Roughness"].default_value = 0.8

for o in meshes:
    me = o.data
    while len(me.uv_layers) > 1:
        me.uv_layers.remove(me.uv_layers[-1])
    uv = me.uv_layers[0] if me.uv_layers else me.uv_layers.new()
    for poly, k in zip(me.polygons, face_cells[o.name]):
        u = ((k % N) * 4 + 2) / (N * 4)
        v = ((k // N) * 4 + 2) / (N * 4)
        for li in poly.loop_indices:
            uv.data[li].uv = (u, v)
    me.materials.clear()
    me.materials.append(mat)

# join into one object with transforms applied
bpy.ops.object.select_all(action="DESELECT")
for o in meshes:
    o.select_set(True)
bpy.context.view_layer.objects.active = meshes[0]
for o in meshes:
    if o.parent:
        mw = o.matrix_world.copy()
        o.parent = None
        o.matrix_world = mw
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
bpy.ops.object.join()
for o in list(bpy.context.scene.objects):
    if o.type != "MESH":
        bpy.data.objects.remove(o)
bpy.ops.export_scene.gltf(filepath=dst, export_format="GLB", export_animations=False)
print("PREP", os.path.basename(src), "colours", len(palette), "palette", N * 4, "faces", sum(len(v) for v in face_cells.values()))
