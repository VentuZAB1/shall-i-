# Independent reviewer renders: fresh FBX import, sunny hub look, player eye height, Roblox-like FOV, backface culling.
# blender.exe -b --factory-startup --python rv_render.py -- <fbx> <tree|bush> <outdir> [shot,shot,...]
import bpy, sys, os, math
import numpy as np
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

HW = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween"
sys.path.insert(0, HW)
from hkit import review_setup, link, lin  # read-only use

argv = sys.argv[sys.argv.index("--") + 1:]
FBX, TAG, OUT = argv[0], argv[1], argv[2]
ONLY = set(argv[3].split(",")) if len(argv) > 3 and argv[3] else None
os.makedirs(OUT, exist_ok=True)
RES = (1600, 900)


def log(*a):
    print("[rv]", *a, flush=True)


bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=FBX)
assets = [o for o in bpy.data.objects if o.type == "MESH"]
for o in assets:
    o.scale = (1, 1, 1)  # FBX is in the pipeline's cm convention; 1 local unit = 1 stud
for m in bpy.data.materials:
    m.use_backface_culling = True  # Roblox renders single-sided
    try:
        m.use_backface_culling_shadow = False
    except Exception:
        pass

VARIANT = os.environ.get("RV_VARIANT", "")
if VARIANT:
    for m in bpy.data.materials:
        nt = m.node_tree
        if not nt:
            continue
        bs = next((n for n in nt.nodes if n.type == "BSDF_PRINCIPLED"), None)
        if VARIANT == "nonormal" and bs:
            for l in list(bs.inputs["Normal"].links):
                nt.links.remove(l)
        if VARIANT == "rough09" and bs and m.name.startswith("Canopy"):
            for l in list(bs.inputs["Roughness"].links):
                nt.links.remove(l)
            bs.inputs["Roughness"].default_value = 0.9
        if VARIANT == "albedo" and bs:
            src = bs.inputs["Base Color"].links[0].from_socket if bs.inputs["Base Color"].links else None
            em = nt.nodes.new("ShaderNodeEmission")
            out = next(n for n in nt.nodes if n.type == "OUTPUT_MATERIAL")
            if src:
                nt.links.new(src, em.inputs["Color"])
            nt.links.new(em.outputs["Emission"], out.inputs["Surface"])
    OUT = os.path.join(OUT, "variant_" + VARIANT)
    os.makedirs(OUT, exist_ok=True)

sc = bpy.context.scene
if sc.world is None:
    sc.world = bpy.data.worlds.new("World")
review_setup(res=RES)  # sky-blue world fill + warm sun (same as the builders)
sc.eevee.taa_render_samples = 48
sc.render.image_settings.file_format = "PNG"


def mat_noise2(name, c1, c2, scale, rough=0.9):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    bs = nt.nodes["Principled BSDF"]
    bs.inputs["Roughness"].default_value = rough
    tx = nt.nodes.new("ShaderNodeTexNoise")
    tx.inputs["Scale"].default_value = scale
    tx.inputs["Detail"].default_value = 6
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].color = (*lin(c1), 1)
    ramp.color_ramp.elements[1].color = (*lin(c2), 1)
    ramp.color_ramp.elements[0].position = 0.35
    ramp.color_ramp.elements[1].position = 0.65
    nt.links.new(tx.outputs["Fac"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], bs.inputs["Base Color"])
    return m


# ground: bright grass
bpy.ops.mesh.primitive_plane_add(size=800, location=(0, 0, 0))
g = bpy.context.active_object
g.data.materials.append(mat_noise2("Grass", (78, 150, 62), (96, 168, 74), 0.08))
# soil bed disc
R = 8.6 if TAG == "tree" else 4.2
bpy.ops.mesh.primitive_cylinder_add(vertices=128, radius=R, depth=0.1, location=(0, 0, -0.045))
s = bpy.context.active_object
s.data.materials.append(mat_noise2("Soil", (88, 60, 40), (112, 78, 52), 0.9, 0.95))
# 5-stud reference block (Roblox character height)
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 2.5))
ref = bpy.context.active_object
ref.scale = (2, 1, 5)
ref.data.materials.append(mat_noise2("Ref", (160, 160, 168), (150, 150, 158), 2.0, 0.6))

V = np.vstack([np.array([tuple(o.matrix_world @ v.co) for v in o.data.vertices]) for o in assets])
mn, mx = V.min(0), V.max(0)
half_w = float(max(mx[0] - mn[0], mx[1] - mn[1]) / 2)
H = float(mx[2])
log("asset bbox", mn, mx)
corners = [Vector((x, y, z)) for x in (mn[0], mx[0]) for y in (mn[1], mx[1]) for z in (max(mn[2], 0), mx[2])]
# also sample real verts for a tighter crop
samp = [Vector(tuple(p)) for p in V[:: max(1, len(V) // 3000)]]


def shoot(name, cam_pos, target, fov_v=70.0, ref_side=1.0, crop=False, ref_on=True):
    if ONLY and name not in ONLY and not name.startswith("diag_"):
        return
    cd = bpy.data.cameras.new("Cam")
    cd.sensor_fit = "VERTICAL"
    cd.sensor_height = 24.0
    cd.lens = 12.0 / math.tan(math.radians(fov_v) / 2)
    cd.clip_start = 0.05
    cd.clip_end = 3000
    cam = link(bpy.data.objects.new("Cam", cd))
    cam.location = Vector(cam_pos)
    d = (Vector(target) - cam.location)
    cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    sc.camera = cam
    # reference block beside the asset, to the camera's right (perpendicular to the view, on the ground)
    fwd = Vector((d.x, d.y, 0)).normalized()
    right = Vector((fwd.y, -fwd.x, 0))
    ref.hide_render = not ref_on
    ref.location = right * (half_w + 2.5) * ref_side + Vector((0, 0, 2.5))
    ref.rotation_euler = (0, 0, math.atan2(fwd.y, fwd.x) + math.pi / 2)
    bpy.context.view_layer.update()
    path = os.path.join(OUT, "rv_%s_%s.png" % (TAG, name))
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
    log("wrote", path)
    if crop:
        pts = [world_to_camera_view(sc, cam, p) for p in samp] + [world_to_camera_view(sc, cam, ref.location + Vector((0, 0, 2.5)))]
        xs = [p.x for p in pts if p.z > 0]
        ys = [p.y for p in pts if p.z > 0]
        x0, x1 = max(0, min(xs) - 0.03), min(1, max(xs) + 0.03)
        y0, y1 = max(0, min(ys) - 0.04), min(1, max(ys) + 0.03)
        img = bpy.data.images.load(path)
        w, h = img.size
        P = np.empty(w * h * 4, dtype=np.float32)
        img.pixels.foreach_get(P)
        P = P.reshape(h, w, 4)
        X0, X1, Y0, Y1 = int(x0 * w), int(x1 * w), int(y0 * h), int(y1 * h)
        C = P[Y0:Y1, X0:X1].copy()
        ci = bpy.data.images.new("crop", X1 - X0, Y1 - Y0, alpha=True)
        ci.pixels.foreach_set(C.ravel())
        ci.filepath_raw = path.replace(".png", "_crop.png")
        ci.file_format = "PNG"
        ci.save()
        log("crop", ci.filepath_raw, X1 - X0, Y1 - Y0)
    bpy.data.objects.remove(cam)


EYE = 5.0
if os.environ.get("RV_ROUND") == "2d":
    if TAG == "tree":
        shoot("gap_frontleft", (-9.0, -13.0, EYE), (-3.94, -4.39, 8.17), fov_v=16, ref_on=False)
        shoot("gap_frontleft_b", (-13.0, -4.0, EYE), (-3.94, -4.39, 8.17), fov_v=16, ref_on=False)
        shoot("gap_backleft", (-9.0, 13.0, EYE), (-2.85, 3.1, 12.5), fov_v=18, ref_on=False)
        shoot("left_12", (-12.0, 0.0, EYE), (0, 0, 9.0), fov_v=70, ref_on=False)
    else:
        shoot("gap_loop", (3.0, 8.0, 3.5), (0.65, 2.13, 0.7), fov_v=26, ref_on=False)
        shoot("gap_right", (8.0, 3.0, 4.0), (2.05, 1.54, 2.28), fov_v=24, ref_on=False)
    log("DONE")
    raise SystemExit
if os.environ.get("RV_ROUND") == "2":
    # Round 2: same player-view set (front/back/side at 25/45, plus left at 25) + close-ups at the new roll positions.
    dirs = (("front", (0, -1)), ("back", (0, 1)), ("side", (1, 0)), ("left", (-1, 0)))
    if TAG == "tree":
        for side, dv in dirs:
            for dist, tz in ((25, 7.0), (45, 6.5)):
                if side == "left" and dist == 45:
                    continue
                shoot("%s_%d" % (side, dist), (dv[0] * dist, dv[1] * dist, EYE), (0, 0, tz), crop=True)
        shoot("under_lookup", (2.0, -8.5, EYE), (0, 0, 10.5), ref_on=False)
        shoot("back_close_lookup", (-1.5, 9.0, EYE), (0, 0, 10.0), ref_on=False)
        shoot("close_twigroll", (7.0, -14.0, EYE), (3.11, -5.35, 7.33), fov_v=24, ref_on=False)
        shoot("close_twigroll_34", (11.0, -9.0, EYE), (3.11, -5.35, 7.1), fov_v=24, ref_on=False)
        shoot("close_fallenroll", (-3.5, -9.5, 4.0), (-1.34, -1.99, 0.55), fov_v=26, ref_on=False)
        shoot("close_canopy", (3.0, -14.0, EYE), (0.5, -4.5, 10.5), fov_v=34, ref_on=False)
        shoot("close_rim_front", (0.5, -12.0, EYE), (0.0, -5.5, 7.8), fov_v=30, ref_on=False)
        shoot("close_rim_back", (-0.5, 12.0, EYE), (0.0, 5.5, 7.8), fov_v=30, ref_on=False)
        shoot("diag_canopy_under", (3.5, -9.0, 4.0), (2.0, -3.5, 8.0), fov_v=30, ref_on=False)
        shoot("close_trunk", (1.5, -6.0, 4.5), (0.4, -0.4, 3.2), fov_v=40, ref_on=False)
    else:
        for side, dv in dirs:
            for dist in (25, 45):
                if side == "left" and dist == 45:
                    continue
                shoot("%s_%d" % (side, dist), (dv[0] * dist, dv[1] * dist, EYE), (0, 0, 2.6), crop=True)
        shoot("close", (2.5, -8.0, EYE), (0, 0, 2.2), fov_v=50, ref_on=False)
        shoot("close_back", (-2.0, 8.0, EYE), (0, 0, 2.4), fov_v=50, ref_on=False)
        shoot("close_right", (8.0, 1.5, EYE), (0, 0, 2.2), fov_v=50, ref_on=False)
        shoot("close_left", (-8.0, -1.5, EYE), (0, 0, 2.2), fov_v=50, ref_on=False)
        shoot("close_roll", (1.8, -8.5, 3.0), (0.44, -3.11, 0.55), fov_v=26, ref_on=False)
        shoot("close_roll_34", (5.5, -7.5, 3.0), (0.44, -3.11, 0.55), fov_v=26, ref_on=False)
        shoot("diag_top", (1.5, -4.5, 6.5), (0.3, -0.6, 4.2), fov_v=45, ref_on=False)
    log("DONE")
    raise SystemExit
if ONLY and any(n.startswith("diag_") for n in ONLY):
    def hide(names, flag=True):
        for o in assets:
            if o.name in names:
                o.hide_render = flag
    if TAG == "tree":
        hide({"TP"})
        shoot("diag_trunk_noTP", (1.5, -6.0, 4.5), (0.4, -0.4, 4.2), fov_v=40, ref_on=False)
        shoot("diag_trunk_noTP_back", (-1.0, 6.0, 4.5), (0.0, 0.3, 4.2), fov_v=40, ref_on=False)
        hide({"TP"}, False)
        shoot("diag_festoon_end", (3.0, -14.0, 5.0), (-1.66, -5.63, 8.9), fov_v=10, ref_on=False)
        shoot("diag_rollA_side", (5.0, -5.0, 5.5), (0.43, -0.65, 6.3), fov_v=20, ref_on=False)
        shoot("diag_canopy_under", (3.5, -9.0, 4.0), (2.0, -3.5, 8.0), fov_v=30, ref_on=False)
    else:
        shoot("diag_top", (1.5, -4.5, 6.5), (0.3, -0.6, 4.2), fov_v=45, ref_on=False)
        shoot("diag_end_right", (4.5, -3.5, 2.0), (2.7, -0.5, 0.2), fov_v=30, ref_on=False)
    log("DONE")
    raise SystemExit
if TAG == "tree":
    tz25, tz45 = 7.0, 6.5
    for side, dv in (("front", (0, -1)), ("back", (0, 1)), ("side", (1, 0))):
        for dist, tz in ((25, tz25), (45, tz45)):
            shoot("%s_%d" % (side, dist), (dv[0] * dist, dv[1] * dist, EYE), (0, 0, tz), crop=True)
    # player standing near the trunk, looking up
    shoot("under_lookup", (2.0, -8.5, EYE), (0, 0, 10.5), ref_on=False)
    # detail: the fork roll (roll A) and roll B, the front festoon, from eye height
    shoot("close_fork", (2.5, -10.0, EYE), (0.43, -0.65, 6.6), fov_v=32, ref_on=False)
    shoot("close_rollB", (-7.0, 17.0, EYE), (-2.98, 5.75, 10.4), fov_v=26, ref_on=False)
    shoot("close_canopy", (3.0, -14.0, EYE), (0.5, -4.5, 10.5), fov_v=34, ref_on=False)
    shoot("back_close_lookup", (-1.5, 9.0, EYE), (0, 0, 10.0), ref_on=False)
else:
    for side, dv in (("front", (0, -1)), ("back", (0, 1)), ("side", (1, 0))):
        for dist in (25, 45):
            shoot("%s_%d" % (side, dist), (dv[0] * dist, dv[1] * dist, EYE), (0, 0, 2.6), crop=True)
    shoot("close", (2.5, -8.0, EYE), (0, 0, 2.2), fov_v=50, ref_on=False)
    shoot("close_roll", (1.8, -7.5, 3.0), (0.4, -2.83, 0.6), fov_v=26, ref_on=False)
    shoot("close_back", (-2.0, 8.0, EYE), (0, 0, 2.4), fov_v=50, ref_on=False)
log("DONE")
