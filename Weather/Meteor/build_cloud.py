# SLINGSHOT - "Meteor Shower" storm cloud (StormCloud): a long black cumulonimbus bank that hovers over the weather's
# area; the meteors burst out of its base. Built procedurally from metaballs.
# Headless (does not touch the GUI Blender session):
#   "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b --factory-startup --python build_cloud.py -- all
#   steps: build | render | export | all
# Units: 1 Blender metre = 1 Roblox stud (FBX global_scale 0.01, like build_meteor.py). Blender (x, y, z) -> Roblox
# (x, z, -y): the bank's length runs along Blender Y = the runway (Roblox Z).
# Colour: a vertical gradient texture (UV v = height): near-black underside -> dark slate sides -> grey-violet tops.
# Owner rule: no emissive / neon. Lightning, the orange glow and the churning smoke come from VFX Studio effects.
import bpy, bmesh, math, os, sys, random, json
from mathutils import Vector, noise

OUT = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Weather\Meteor"
BLEND = os.path.join(OUT, "storm_cloud.blend")
GRAD = os.path.join(OUT, "storm_cloud_gradient.png")
W, L = 105.0, 220.0     # half width (Roblox X) and half length (Roblox Z) of the footprint
TARGET_TRIS = 8000

GRADIENT = [  # (v, sRGB) bottom -> top. Neutral-warm charcoal: Roblox's blue sky light tints it; a cooler ramp read navy
    (0.00, (14, 12, 13)),   # in game (2026-10-11), the owner asked for a BLACK storm
    (0.10, (19, 17, 18)),
    (0.30, (30, 27, 28)),
    (0.60, (46, 42, 43)),
    (0.85, (66, 61, 62)),
    (1.00, (82, 77, 78)),
]


def srgb_to_lin(c):
    return (c / 12.92) if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def grad_at(v):
    for (v0, c0), (v1, c1) in zip(GRADIENT, GRADIENT[1:]):
        if v <= v1:
            k = (v - v0) / (v1 - v0)
            return [(a + (b - a) * k) / 255.0 for a, b in zip(c0, c1)]
    return [c / 255.0 for c in GRADIENT[-1][1]]


def make_gradient():
    w, h = 8, 256
    img = bpy.data.images.new("storm_grad_tmp", w, h, alpha=False)
    px = []
    for y in range(h):
        r, g, b = grad_at(y / (h - 1))
        for _ in range(w):
            px += [r, g, b, 1.0]
    img.pixels[:] = px
    img.filepath_raw = GRAD
    img.file_format = "PNG"
    img.save()
    bpy.data.images.remove(img)
    img = bpy.data.images.load(GRAD, check_existing=False)
    img.name = "storm_cloud_gradient.png"
    return img


def material(img):
    m = bpy.data.materials.new("StormCloud_Mat")
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = img
    tex.interpolation = "Linear"
    tex.extension = "EXTEND"
    nt.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = 1.0
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    return m


def in_ellipse(rng, scale=1.0):
    while True:
        x, y = rng.uniform(-1, 1), rng.uniform(-1, 1)
        if x * x + y * y <= 1:
            return x * scale, y * scale


def metaball_cloud(sc, seed):
    rng = random.Random(seed)
    mb = bpy.data.metaballs.new("StormMB")
    mb.resolution = 2.6
    mb.render_resolution = 2.6
    mb.threshold = 0.6
    ob = bpy.data.objects.new("StormMB", mb)
    sc.collection.objects.link(ob)

    def add(x, y, z, r, stiff=2.0):
        e = mb.elements.new()
        e.co = (x, y, z)
        e.radius = r
        e.stiffness = stiff

    # base layer: a broad lumpy slab (tapers toward the ends of the bank)
    for _ in range(95):
        x, y = in_ellipse(rng, 0.9)
        taper = 1.0 - 0.38 * abs(y)
        add(x * W * 0.85, y * L, rng.uniform(10, 18), rng.uniform(24, 34) * taper)
    # body: billows stacked above the middle
    for _ in range(55):
        x, y = in_ellipse(rng, 0.72)
        add(x * W * 0.85, y * L, rng.uniform(26, 40), rng.uniform(22, 30) * (1.0 - 0.3 * abs(y)))
    # towers: 4 cumulus heads rising out of the bank (an anvil-ish storm silhouette)
    for c in range(4):
        cy = (-0.62 + c * 0.42 + rng.uniform(-0.08, 0.08)) * L
        cx = rng.uniform(-0.3, 0.3) * W
        hgt = rng.uniform(50, 64)
        for _ in range(7):
            add(cx + rng.uniform(-26, 26), cy + rng.uniform(-34, 34), hgt + rng.uniform(-10, 8), rng.uniform(20, 27))
    return ob


def mesh_from(ob, name):
    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(ob.evaluated_get(dg))
    me.name = name
    return me


def build_cloud(seed=11):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.name = "Storm"
    mb_ob = metaball_cloud(sc, seed)
    me = mesh_from(mb_ob, "StormRaw")
    bpy.data.objects.remove(mb_ob)

    # 1. flatten the underside into a storm base with hanging mammatus pouches
    rng = random.Random(seed * 7)
    pouches = []
    for _ in range(34):
        x, y = in_ellipse(rng, 0.78)
        pouches.append((x * W * 0.85, y * L, rng.uniform(9, 15), rng.uniform(3.5, 8.0)))

    def base_z(x, y):
        z = 2.0 + noise.noise(Vector((x * 0.03, y * 0.03, 0.5))) * 1.5
        for px, py, pr, pd in pouches:
            d2 = ((x - px) ** 2 + (y - py) ** 2) / (pr * pr)
            if d2 < 4:
                z -= pd * math.exp(-d2 * 1.6)
        return z

    bm = bmesh.new()
    bm.from_mesh(me)
    for v in bm.verts:
        bz = base_z(v.co.x, v.co.y)
        if v.co.z < bz:
            v.co.z = bz
    # 2. billow detail: push along the normal with low-frequency noise (no smooth metaball balls)
    bm.normal_update()
    for v in bm.verts:
        n = noise.noise(v.co * 0.045) * 4.0 + noise.noise(v.co * 0.11 + Vector((3, 1, 2))) * 1.6
        if v.co.z > 4:
            v.co += v.normal * n
    bm.to_mesh(me)
    bm.free()

    ob = bpy.data.objects.new("StormCloud", me)
    sc.collection.objects.link(ob)
    # 3. clean surface (voxel remesh), then decimate to the triangle budget
    rem = ob.modifiers.new("Remesh", "REMESH")
    rem.mode = "VOXEL"
    rem.voxel_size = 2.4
    me2 = mesh_from(ob, "StormRemeshed")
    ob.modifiers.clear()
    ob.data = me2
    tris = sum(len(p.vertices) - 2 for p in me2.polygons)
    dec = ob.modifiers.new("Decimate", "DECIMATE")
    dec.decimate_type = "COLLAPSE"
    dec.ratio = min(1.0, TARGET_TRIS / max(tris, 1))
    tri = ob.modifiers.new("Tri", "TRIANGULATE")
    me3 = mesh_from(ob, "StormCloud")
    ob.modifiers.clear()
    ob.data = me3
    for p in me3.polygons:
        p.use_smooth = True

    # 4. centre the bounding box on the origin (Studio pivots MeshParts at the bbox centre)
    xs = [v.co.x for v in me3.vertices]
    ys = [v.co.y for v in me3.vertices]
    zs = [v.co.z for v in me3.vertices]
    c = Vector(((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2, (min(zs) + max(zs)) / 2))
    for v in me3.vertices:
        v.co -= c
    zmin, zmax = min(zs) - c.z, max(zs) - c.z

    # 5. UVs: v = height (plus a little noise so the bands aren't ruler-straight), u = 0.5
    uv = me3.uv_layers.new(name="UVMap")
    for loop in me3.loops:
        co = me3.vertices[loop.vertex_index].co
        k = (co.z - zmin) / (zmax - zmin)
        k += noise.noise(co * 0.05) * 0.06
        uv.data[loop.index].uv = (0.5, min(0.995, max(0.005, k)))

    img = make_gradient()
    me3.materials.append(material(img))
    for m in list(bpy.data.meshes):
        if m.users == 0:
            bpy.data.meshes.remove(m)
    bpy.ops.wm.save_as_mainfile(filepath=BLEND)
    return {"tris": sum(len(p.vertices) - 2 for p in me3.polygons), "size": [round(v, 1) for v in ob.dimensions],
            "base_drop": round(zmin, 1)}


# ------------------------------------------------------------------ review renders
def eevee(sc, res):
    sc.render.engine = "BLENDER_EEVEE"
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.render.resolution_percentage = 100
    sc.render.film_transparent = False
    sc.view_settings.view_transform = "Standard"
    try:
        sc.eevee.taa_render_samples = 48
    except Exception:
        pass


def world(sc, col=(0.42, 0.62, 0.9), strength=0.9):
    w = bpy.data.worlds.new("Sky")
    w.use_nodes = True
    bg = w.node_tree.nodes.get("Background")
    bg.inputs["Color"].default_value = (*col, 1.0)
    bg.inputs["Strength"].default_value = strength
    sc.world = w


def sun(sc, name, rot, energy, col=(1, 1, 1), ang=8):
    ld = bpy.data.lights.new(name, "SUN")
    ld.energy, ld.color, ld.angle = energy, col, math.radians(ang)
    o = bpy.data.objects.new(name, ld)
    o.rotation_euler = [math.radians(a) for a in rot]
    sc.collection.objects.link(o)
    return o


def camera(sc, loc, target, lens=28):
    cd = bpy.data.cameras.new("Cam")
    cam = bpy.data.objects.new("Cam", cd)
    sc.collection.objects.link(cam)
    cam.location = Vector(loc)
    cam.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    cd.lens = lens
    cd.clip_end = 6000
    sc.camera = cam
    return cam


def render_all():
    bpy.ops.wm.open_mainfile(filepath=BLEND)
    sc = bpy.data.scenes["Storm"]
    ob = bpy.data.objects["StormCloud"]
    base = 110.0 - (-ob.dimensions.z / 2)  # cloud bbox centre so that the bbox bottom sits at y = 110 (the game)
    ob.location = (0, 0, 110.0 + ob.dimensions.z / 2)
    eevee(sc, (1600, 900))
    world(sc)
    sun(sc, "Key", (35, 0, 30), 3.5, (1, 0.97, 0.92))
    sun(sc, "Fill", (150, 0, -140), 0.6, (0.75, 0.8, 1.0), 30)
    # a runway (120 x 400, walls 40 high) for scale, Roblox Z = -Blender Y
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0))
    floor = bpy.context.active_object
    floor.scale = (120, 400, 1)
    for sx in (-1, 1):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(sx * 62, 0, 20))
        wall = bpy.context.active_object
        wall.scale = (4, 400, 40)
    mfl = bpy.data.materials.new("Floor")
    mfl.use_nodes = True
    mfl.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.55, 0.75, 0.55, 1)
    floor.data.materials.append(mfl)
    out = []
    views = {
        "storm_player_view": ((8, 170, 6), (0, -60, 95), 22),         # on the runway, looking ahead and up
        "storm_from_below": ((30, 60, 4), (0, 0, 140), 16),             # straight up under the bank
        "storm_side": ((520, -160, 120), (0, 0, 120), 35),              # from the side
        "storm_far": ((60, 1200, 60), (0, 0, 110), 40),                 # from the hub, 1200 studs away
    }
    for name, (loc, tgt, lens) in views.items():
        cam = camera(sc, loc, tgt, lens)
        p = os.path.join(OUT, name + ".png")
        sc.render.filepath = p
        sc.render.image_settings.file_format = "PNG"
        bpy.ops.render.render(write_still=True, scene=sc.name)
        bpy.data.objects.remove(cam)
        out.append(p)
    return out


FBX_ARGS = dict(use_selection=True, global_scale=0.01, apply_unit_scale=True, apply_scale_options="FBX_SCALE_NONE",
                axis_forward="-Z", axis_up="Y", object_types={"MESH"}, use_mesh_modifiers=True,
                mesh_smooth_type="FACE", add_leaf_bones=False, bake_anim=False, path_mode="COPY",
                embed_textures=True)


def export():
    bpy.ops.wm.open_mainfile(filepath=BLEND)
    sc = bpy.data.scenes["Storm"]
    ob = bpy.data.objects["StormCloud"]
    for o in sc.objects:
        o.select_set(o is ob)
    bpy.context.view_layer.objects.active = ob
    path = os.path.join(OUT, "StormCloud.fbx")
    bpy.ops.export_scene.fbx(filepath=path, **FBX_ARGS)
    return {"fbx": path, "kb": round(os.path.getsize(path) / 1024, 1)}


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else ["all"]
    step = argv[0]
    rep = {}
    if step in ("build", "all"):
        rep["build"] = build_cloud()
    if step in ("render", "all"):
        rep["render"] = render_all()
    if step in ("export", "all"):
        rep["export"] = export()
    print("CLOUD_REPORT " + json.dumps(rep))
