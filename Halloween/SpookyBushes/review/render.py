# Independent reviewer render script (read-only use of hkit). Usage:
#   blender -b --factory-startup --python render.py -- <mode>
# modes: lineup | player | close | web | clay | sil
import bpy, sys, os, math
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
sys.path.insert(0, r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween")
from hkit import review_setup, link, lin

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "renders" + os.environ.get("REVIEW_TAG", ""))
os.makedirs(OUT, exist_ok=True)
mode = sys.argv[sys.argv.index("--") + 1]

FBX = {"Thorn": r"C:\cdimp\Halloween_Bush_Thorn.fbx",
       "Autumn": r"C:\cdimp\Halloween_Bush_Autumn.fbx",
       "Bramble": r"C:\cdimp\Halloween_Bramble.fbx"}
POS = {"Thorn": -8.0, "Autumn": 0.0, "Bramble": 7.5}
ASSET = {}

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.world = bpy.data.worlds.new("W")
review_setup(res=(1920, 1080), sky=(0.36, 0.5, 0.72), sky_strength=0.9, sun=4.0)
sc.eevee.taa_render_samples = 32
sun = bpy.data.objects["Sun"]
sun.data.angle = math.radians(2.0)

for key, path in FBX.items():
    before = set(bpy.data.objects)
    bpy.ops.import_scene.fbx(filepath=path)
    new = [o for o in bpy.data.objects if o not in before]
    for o in new:
        o.scale = (1, 1, 1)                       # FBX came in at 0.01 (export global_scale 0.01): x100 = studs
        o.location.x += POS[key]
    ASSET[key] = new

for m in bpy.data.materials:
    m.use_backface_culling = True                  # Roblox renders single-sided
    m.surface_render_method = "DITHERED"           # alpha hashed (WebSilk alpha = Transparency mode)
    if not m.use_nodes:
        continue
    for n in m.node_tree.nodes:
        if n.type == "TEX_IMAGE" and n.image and ("normal" in n.image.name or "rough" in n.image.name):
            n.image.colorspace_settings.name = "Non-Color"

# ground: green grass + a round soil bed under each asset (the hub beds are soil patches)
bpy.ops.mesh.primitive_plane_add(size=600, location=(0, 0, 0))
g = bpy.context.active_object
g.name = "Ground"
gm = bpy.data.materials.new("Grass")
gm.use_nodes = True
nt = gm.node_tree
b = nt.nodes["Principled BSDF"]
nz = nt.nodes.new("ShaderNodeTexNoise")
nz.inputs["Scale"].default_value = 0.35
ramp = nt.nodes.new("ShaderNodeValToRGB")
ramp.color_ramp.elements[0].color = (*lin((72, 150, 52)), 1)
ramp.color_ramp.elements[1].color = (*lin((104, 178, 66)), 1)
nt.links.new(nz.outputs["Fac"], ramp.inputs["Fac"])
nt.links.new(ramp.outputs["Color"], b.inputs["Base Color"])
b.inputs["Roughness"].default_value = 0.9
g.data.materials.append(gm)
sm = bpy.data.materials.new("Soil")
sm.use_nodes = True
sm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (*lin((104, 74, 50)), 1)
sm.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.95
SOIL = {}
for key, x in POS.items():
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=4.2 if key != "Bramble" else 3.0, depth=0.2,
                                        location=(x, 0, 0.0))
    d = bpy.context.active_object
    d.name = "Soil_" + key
    d.data.materials.append(sm)
    SOIL[key] = d

# 5-stud reference "character" block (2 x 1 x 5 studs), Roblox medium stone grey
rm = bpy.data.materials.new("RefGrey")
rm.use_nodes = True
rm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (*lin((163, 162, 165)), 1)


def ref_block(x, y=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, 2.5))
    r = bpy.context.active_object
    r.scale = (2, 1, 5)
    r.name = "Ref5"
    r.data.materials.append(rm)
    return r


def bbox(objs):
    mn = Vector((1e9,) * 3)
    mx = Vector((-1e9,) * 3)
    for o in objs:
        for c in o.bound_box:
            w = o.matrix_world @ Vector(c)
            mn = Vector(map(min, mn, w))
            mx = Vector(map(max, mx, w))
    return mn, mx


def only_assets(keys):
    for k, objs in ASSET.items():
        for o in objs:
            o.hide_render = k not in keys
        SOIL[k].hide_render = k not in keys


def cam_player(target, dist, yaw_deg=0.0, eye=5.0, fov=70.0):
    """Player view: camera `dist` studs (horizontal) from target, `eye` studs up, Roblox-like vertical FOV."""
    cd = bpy.data.cameras.new("Cam")
    cam = link(bpy.data.objects.new("Cam", cd))
    yaw = math.radians(yaw_deg)
    t = Vector(target)
    cam.location = Vector((t.x + math.sin(yaw) * dist, t.y - math.cos(yaw) * dist, eye))
    cam.rotation_euler = (t - cam.location).to_track_quat("-Z", "Y").to_euler()
    cd.sensor_fit = "VERTICAL"
    cd.angle_y = math.radians(fov)
    cd.clip_end = 5000
    sc.camera = cam
    return cam


def cam_lens(target, direction, dist, lens):
    cd = bpy.data.cameras.new("Cam")
    cam = link(bpy.data.objects.new("Cam", cd))
    cam.location = Vector(target) + Vector(direction).normalized() * dist
    cam.rotation_euler = (Vector(target) - cam.location).to_track_quat("-Z", "Y").to_euler()
    cd.lens = lens
    cd.clip_end = 5000
    sc.camera = cam
    return cam


def render(path, cam, crop_objs=None, margin=0.35, res=(1920, 1080)):
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.render.use_border = False
    sc.render.use_crop_to_border = False
    if crop_objs:
        bpy.context.view_layer.update()
        mn, mx = bbox(crop_objs)
        pts = [world_to_camera_view(sc, cam, Vector((x, y, z))) for x in (mn.x, mx.x) for y in (mn.y, mx.y)
               for z in (mn.z, mx.z)]
        x0 = min(p.x for p in pts); x1 = max(p.x for p in pts)
        y0 = min(p.y for p in pts); y1 = max(p.y for p in pts)
        w, h = x1 - x0, y1 - y0
        sc.render.use_border = True
        sc.render.use_crop_to_border = True
        sc.render.border_min_x = max(0, x0 - w * margin)
        sc.render.border_max_x = min(1, x1 + w * margin)
        sc.render.border_min_y = max(0, y0 - h * margin)
        sc.render.border_max_y = min(1, y1 + h * margin)
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(cam)
    print("RENDERED", path, flush=True)


def ctr(key):
    mn, mx = bbox(ASSET[key])
    return Vector(((mn.x + mx.x) / 2, (mn.y + mx.y) / 2, (mn.z + mx.z) / 2))


def P(n):
    return os.path.join(OUT, n)


if mode == "lineup":
    ref_block(12.5)
    only_assets(set(FBX))
    for d in (25, 45):
        render(P(f"lineup_{d}.png"), cam_player((0, 0, 2.5), d))
    render(P("lineup_25_back.png"), cam_player((0, 0, 2.5), 25, yaw_deg=180))

elif mode == "player":
    # per asset: true pixel size on a 1920x1080 screen at 70 deg vertical FOV, cropped around the asset
    for key in FBX:
        only_assets({key})
        c = ctr(key)
        r = ref_block(c.x + 4.6, 0.8)
        for d in (25, 40):
            for yaw, tag in ((0, "front"), (90, "sideR"), (180, "back"), (270, "sideL")):
                render(P(f"{key}_{d}_{tag}_truepx.png"), cam_player((c.x, 0, 2.5), d, yaw),
                       crop_objs=ASSET[key] + [r], margin=0.25)
        # same 40-stud viewpoint through a long lens, to judge what those pixels contain
        render(P(f"{key}_40_front_zoom.png"), cam_lens((c.x + 1.2, 0, 2.6), (0, -40, 2.4), 40.1, 520),
               res=(1400, 1000))
        bpy.data.objects.remove(r)

elif mode == "zoom":
    # 40 studs away at player eye height (5 up), long lens: what the 40-stud pixels contain, framed on the asset
    for key in FBX:
        only_assets({key})
        c = ctr(key)
        r = ref_block(c.x + 4.6, 0.8)
        for yaw, tag in ((0, ""), (90, "_sideR"), (180, "_back"), (270, "_sideL")):
            cam = cam_player((c.x + (1.2 if yaw == 0 else 0), 0, 2.6), 40, yaw_deg=yaw)
            cam.data.sensor_fit = "AUTO"
            cam.data.lens = 150 if key != "Bramble" else 190
            render(P(f"{key}_40_zoom150{tag}.png"), cam, res=(1400, 1000))
        bpy.data.objects.remove(r)

elif mode == "close":
    for key in FBX:
        only_assets({key})
        c = ctr(key)
        h = 2.6 if key != "Bramble" else 1.6
        dist = 11 if key != "Bramble" else 8
        render(P(f"{key}_close_front34.png"), cam_lens((c.x, 0, h), (0.55, -1, 0.42), dist, 50), res=(1400, 1000))
        render(P(f"{key}_close_back34.png"), cam_lens((c.x, 0, h), (-0.7, 1, 0.35), dist, 50), res=(1400, 1000))
        render(P(f"{key}_close_low.png"), cam_lens((c.x, 0, h * 0.55), (0.2, -1, 0.06), dist, 50), res=(1400, 1000))

elif mode == "web":
    only_assets({"Thorn"})
    c = ctr("Thorn")
    render(P("Thorn_web_front_eye.png"), cam_lens((c.x, 0, 3.2), (0, -1, 0.18), 10, 50), res=(1400, 1000))
    render(P("Thorn_web_left_eye.png"), cam_lens((c.x - 0.5, 0, 3.0), (-1, -0.1, 0.18), 10, 50), res=(1400, 1000))
    render(P("Thorn_web_top.png"), cam_lens((c.x, 0, 3.6), (0.3, -0.8, 1.0), 9, 50), res=(1400, 1000))
    render(P("Thorn_web_side.png"), cam_lens((c.x, 0, 3.4), (1, -0.25, 0.25), 9, 50), res=(1400, 1000))
    for o in ASSET["Thorn"]:
        if o.name.startswith("WebSilk"):
            o.hide_render = True
    render(P("Thorn_web_nosilk.png"), cam_lens((c.x, 0, 3.6), (0.3, -0.8, 1.0), 9, 50), res=(1400, 1000))

elif mode in ("clay", "sil"):
    sc.render.engine = "BLENDER_WORKBENCH"
    sh = sc.display.shading
    sh.show_backface_culling = True
    sh.show_cavity = False
    sh.show_shadows = False
    if mode == "clay":
        sh.light = "STUDIO"
        sh.color_type = "SINGLE"
        sh.single_color = (0.7, 0.68, 0.64)
        sc.world.color = (0.36, 0.5, 0.72)
    else:
        sh.light = "FLAT"
        sh.color_type = "SINGLE"
        sh.single_color = (0, 0, 0)
        sc.world.color = (1, 1, 1)
        bpy.data.objects["Ground"].hide_render = True
    for key in FBX:
        only_assets({key})
        if mode == "sil":
            SOIL[key].hide_render = True
            for o in ASSET[key]:
                if o.name.startswith("WebSilk"):
                    o.hide_render = True
        c = ctr(key)
        h = 2.6 if key != "Bramble" else 1.5
        dist = 12 if key != "Bramble" else 8.5
        for yaw in (0, 90, 200):
            d3 = Vector((math.sin(math.radians(yaw)), -math.cos(math.radians(yaw)), 0.18))
            render(P(f"{key}_{mode}_{yaw}.png"), cam_lens((c.x, 0, h), d3, dist, 50), res=(1000, 800))
