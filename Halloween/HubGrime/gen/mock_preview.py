# HubGrime - lit preview renders on studded mocks (headless Blender 5.2, Eevee).
#   "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b --factory-startup --python gen\mock_preview.py --
#        --shots all|calib|<name,name,...> [--res 1920x1080] [--samples 64]
# Mocks: floor patch 40 x 24 (green, with an 8-wide cream path + 1-stud brown edges) and a 40 x 24 blue wall section
# (6 thick, top trim 22.9-24.5) on a green floor strip; studs = flat plane + 1-stud normal/AO tile (as Roblox draws
# SurfaceType.Studs). Decals = one carrier plane each, 0.03 / 0.04 / 0.05 off the surface, image extension REPEAT
# (Roblox wraps), straight alpha, BLENDED (per-object sort, like Roblox), no shadow casting.
import json
import math
import os
import sys

import bpy
from mathutils import Euler, Matrix, Vector

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOCK = os.path.join(HERE, "mock")
OUT = os.path.join(HERE, "renders")

ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []


def arg(name, default):
    if name in ARGS:
        return ARGS[ARGS.index(name) + 1]
    return default


DEC = arg("--decals", os.path.join(HERE, "decals"))     # round 4: render other decal sets (e.g. the round-3 copy)
PREFIX = arg("--prefix", "")                             # output name prefix for those runs


SHOTS = arg("--shots", "all")
RES = tuple(int(v) for v in arg("--res", "1920x1080").split("x"))
SAMPLES = int(arg("--samples", "64"))

# ------------------------------------------------------------------ calibrated lighting (see BUILD_NOTES.md)
DAY = dict(sun=5.0, sun_col=(1.0, 0.93, 0.82), sun_dir=(-0.45, -0.55, 0.70), sky=(0.48, 0.58, 0.78), sky_str=1.6,
           exposure=0.0, vt="Khronos PBR Neutral", sky_display=(0.36, 0.5, 0.72))
NIGHT = dict(sun=2.2, sun_col=(0.8, 0.84, 1.0), sun_dir=(-0.35, -0.5, 0.6), sky=(0.32, 0.33, 0.55), sky_str=1.2,
             exposure=0.0, vt="Khronos PBR Neutral", sky_display=(0.012, 0.02, 0.07), stars=True)

WALL_X = 1000.0  # the wall mock lives far to the side so the two mocks never see each other

SRGB = lambda c: tuple(((v / 255 + 0.055) / 1.055) ** 2.4 if v / 255 > 0.04045 else v / 255 / 12.92 for v in c)
GREEN, BLUE, CREAM, BROWN, TRIM = (128, 170, 96), (96, 132, 170), (222, 205, 170), (150, 118, 88), (69, 95, 132)
PILLAR = TRIM

# round 4: lighting + wall/pillar albedo re-calibrated against the LIVE GAME screenshots (ingame_round3\): the back
# wall faces the hub with the sun BEHIND it, so the wall and the floor at its foot are in shade. gen\calib_fit.py fits
# these values; --cal points at another file (the fitter's trial runs).
CAL_PATH = arg("--cal", os.path.join(HERE, "gen", "calib_round4.json"))
CAL = json.load(open(CAL_PATH)) if os.path.exists(CAL_PATH) else None
if CAL:
    DAY = dict(DAY, **CAL["day"])
    NIGHT = dict(NIGHT, **CAL["night"])
    GREEN = tuple(CAL["albedo"].get("green", GREEN))
    BLUE = tuple(CAL["albedo"].get("blue", BLUE))
    PILLAR = tuple(CAL["albedo"].get("pillar", PILLAR))
    TRIM = tuple(CAL["albedo"].get("trim", TRIM))

# decal layouts: (texture, centre, size (w, h), yaw deg (floor) , layer offset, transparency, uv crop (u0, u1))
FLOOR_DECALS = [
    ("G_Stain_A", (-14.0, -4.6), 0, 30, 0.03, 0.0),
    ("G_Moss_A", (-14.6, -4.0), 0, 0, 0.05, 0.0),
    ("G_Crack_A", (-8.6, 3.4), 0, 15, 0.04, 0.0),
    ("G_Crack_B", (11.6, 5.2), 0, -20, 0.04, 0.12),   # on the cream path: Decal.Transparency 0.12 (NOTES)
    ("G_Crack_C", (-3.4, -7.2), 0, -8, 0.04, 0.0),
    ("G_Moss_B", (2.6, 7.6), 0, 25, 0.05, 0.0),
    ("G_Stain_B", (4.6, -6.4), 0, 10, 0.03, 0.0),
    ("G_Slime_A", (11.8, -2.6), 0, 0, 0.05, 0.0),      # on clean path: slime never overlaps (NOTES)
]
# wall mock (round 2) = the OWNER TEST PATCH bay, read from test_patch.json, + two side sections for the remaining
# wall decals. Roblox -> mock: mock x = -(X - bay centre), mock y = Z - 104 (wall face at y = 0, the hub at y < 0),
# mock z = Y. That is a proper rotation (no mirror): the mock camera at y < 0 looking +y sees what a player in the
# hub sees looking +Z (Roblox +X = the viewer's LEFT = mock -x).
PATCH = json.load(open(os.path.join(HERE, "test_patch.json")))
BAY_C = PATCH["assumptions"]["bay_centre_x"]
WALL_FACE_Z = PATCH["assumptions"]["wall_inner_face_z"]
PILLAR_MX = [-(x - BAY_C) for x in PATCH["assumptions"]["bay_pillar_centres_x"]]   # +-13.3
PILLAR_W, PILLAR_D = PATCH["assumptions"]["pillar_size_x_z"]
PILLAR_FRONT = PATCH["assumptions"]["pillar_front_z"] - WALL_FACE_Z                # -1.7
FACE_IN = abs(PILLAR_MX[0]) - PILLAR_W / 2                                         # 12.05
FACE_OUT = abs(PILLAR_MX[0]) + PILLAR_W / 2                                        # 14.55
WALL_HALF = 37.0


def patch_wall_decals():
    out = []
    for e in PATCH["wall"]:
        w, h, _ = e["size"]
        x = -(e["position"][0] - BAY_C)
        zb = e["position"][1] - h / 2
        ur = (0.0, w / e["texture_props"]["StudsPerTileU"]) if "texture_props" in e else (0.0, 1.0)
        out.append((e["texture"], x, zb, w, h, e["layer_studs"], ur, ""))
    return out


def patch_floor_decals():
    return [(e["texture"], (-(e["position"][0] - BAY_C), e["position"][2] - WALL_FACE_Z), e["rotation_y_deg"],
             e["layer_studs"], e["decal"]["Transparency"]) for e in PATCH["floor"]]


# side sections (catalog only, not part of the test patch): EndL | B (cut by the pillar) || bay || A (cut) | EndR
SIDE_W = WALL_HALF - 6.0 - FACE_OUT          # strip length between the pillar and the cap
WALL_DECALS = patch_wall_decals() + [
    ("W_MossBase_EndL", -(WALL_HALF - 3.0), -0.375, 6.0, 6.375, 0.05, (0.0, 1.0), "_side"),
    ("W_MossBase_B", -(FACE_OUT + SIDE_W / 2), -0.375, SIDE_W, 6.375, 0.05, (0.0, SIDE_W / 24.0), "_side"),
    ("W_MossBase_A", FACE_OUT + SIDE_W / 2, -0.375, SIDE_W, 6.375, 0.05, (1.0 - SIDE_W / 24.0, 1.0), "_side"),
    ("W_MossBase_EndR", WALL_HALF - 3.0, -0.375, 6.0, 6.375, 0.05, (0.0, 1.0), "_side"),
    ("W_Drip_B", -24.0, 23.25 - 8.35, 4.0, 8.35, 0.05, (0.0, 1.0), "_side"),
    ("W_Crack_A", 24.5, 3.2, 5.0, 10.0, 0.04, (0.0, 1.0), "_side"),
]
WALL_FLOOR_DECALS = patch_floor_decals()


# ------------------------------------------------------------------ scene helpers
def fresh():
    global STUD_N, STUD_AO
    STUD_N = STUD_AO = None
    CARRIERS.clear()
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = "BLENDER_EEVEE"
    sc.render.resolution_x, sc.render.resolution_y = RES
    sc.render.resolution_percentage = 100
    sc.eevee.taa_render_samples = SAMPLES
    sc.world = bpy.data.worlds.new("W")
    sc.render.image_settings.file_format = "PNG"
    try:
        bpy.context.preferences.system.anisotropic_filter = "FILTER_16"
    except Exception:
        pass
    return sc


def link(ob):
    bpy.context.scene.collection.objects.link(ob)
    return ob


def mesh_quad(name, corners, uvs, origin=(0, 0, 0)):
    me = bpy.data.meshes.new(name)
    o = Vector(origin)
    me.from_pydata([tuple(Vector(c) - o) for c in corners], [], [(0, 1, 2, 3)])
    uvl = me.uv_layers.new(name="UVMap")
    for i, l in enumerate(me.loops):
        uvl.data[i].uv = uvs[l.vertex_index]
    me.update()
    ob = link(bpy.data.objects.new(name, me))
    ob.location = o
    return ob


def load_img(path, colorspace="sRGB", alpha=True):
    img = bpy.data.images.load(path, check_existing=True)
    img.colorspace_settings.name = colorspace
    img.alpha_mode = "STRAIGHT" if alpha else "NONE"
    return img


STUD_N = None
STUD_AO = None


def stud_material(name, col, rough=0.72):
    global STUD_N, STUD_AO
    if STUD_N is None:
        STUD_N = load_img(os.path.join(MOCK, "stud_normal.png"), "Non-Color", False)
        STUD_AO = load_img(os.path.join(MOCK, "stud_ao.png"), "Non-Color", False)
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    uv = nt.nodes.new("ShaderNodeUVMap")
    uv.uv_map = "UVMap"
    tn = nt.nodes.new("ShaderNodeTexImage")
    tn.image = STUD_N
    tn.interpolation = "Linear"
    ta = nt.nodes.new("ShaderNodeTexImage")
    ta.image = STUD_AO
    for t in (tn, ta):
        nt.links.new(uv.outputs["UV"], t.inputs["Vector"])
    nm = nt.nodes.new("ShaderNodeNormalMap")
    nm.inputs["Strength"].default_value = 0.8
    nt.links.new(tn.outputs["Color"], nm.inputs["Color"])
    nt.links.new(nm.outputs["Normal"], bsdf.inputs["Normal"])
    mul = nt.nodes.new("ShaderNodeMix")
    mul.data_type = "RGBA"
    mul.blend_type = "MULTIPLY"
    mul.inputs["Factor"].default_value = 1.0
    mul.inputs[6].default_value = (*SRGB(col), 1)
    nt.links.new(ta.outputs["Color"], mul.inputs[7])
    nt.links.new(mul.outputs[2], bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Specular IOR Level"].default_value = 0.35
    return m


def flat_material(name, col, rough=0.7):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*SRGB(col), 1)
    b.inputs["Roughness"].default_value = rough
    return m


def decal_material(name, tex, transparency=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    t = nt.nodes.new("ShaderNodeTexImage")
    t.image = load_img(os.path.join(DEC, tex + ".png"))
    t.interpolation = "Linear"
    t.extension = "REPEAT"   # Roblox wraps texture coordinates
    uv = nt.nodes.new("ShaderNodeUVMap")
    uv.uv_map = "UVMap"
    nt.links.new(uv.outputs["UV"], t.inputs["Vector"])
    nt.links.new(t.outputs["Color"], bsdf.inputs["Base Color"])
    if transparency > 0:
        mm = nt.nodes.new("ShaderNodeMath")
        mm.operation = "MULTIPLY"
        mm.inputs[1].default_value = 1 - transparency
        nt.links.new(t.outputs["Alpha"], mm.inputs[0])
        nt.links.new(mm.outputs[0], bsdf.inputs["Alpha"])
    else:
        nt.links.new(t.outputs["Alpha"], bsdf.inputs["Alpha"])
    bsdf.inputs["Roughness"].default_value = 0.8
    bsdf.inputs["Specular IOR Level"].default_value = 0.25
    m.surface_render_method = "BLENDED"
    m.use_backface_culling = True
    # no per-object depth prepass: transparent decals must not occlude each other (pure sorted blending, as in Roblox)
    m.use_transparency_overlap = True
    return m


def studded_plane(name, x0, x1, y0, y1, col, z=0.0):
    corners = [(x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z)]
    uvs = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    ob = mesh_quad(name, corners, uvs)
    ob.data.materials.append(stud_material(name + "_m", col))
    return ob


def box(name, x0, x1, y0, y1, z0, z1, mat):
    bpy.ops.mesh.primitive_cube_add(size=1)
    ob = bpy.context.active_object
    ob.name = name
    ob.scale = (x1 - x0, y1 - y0, z1 - z0)
    ob.location = ((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2)
    ob.data.materials.append(mat)
    return ob


# ------------------------------------------------------------------ mocks
CARRIERS = {}


def floor_decal(tex, centre, yaw, z, transparency, tag=""):
    from make_specs import SPEC_STUDS
    w, h = SPEC_STUDS[tex]
    c = Vector((centre[0], centre[1], z))
    R = Matrix.Rotation(math.radians(yaw), 3, "Z")
    corners = [c + R @ Vector(v) for v in ((-w / 2, -h / 2, 0), (w / 2, -h / 2, 0), (w / 2, h / 2, 0), (-w / 2, h / 2, 0))]
    ob = mesh_quad("D_" + tex + tag, corners, [(0, 0), (1, 0), (1, 1), (0, 1)], origin=c)
    ob.data.materials.append(decal_material("M_" + tex + tag, tex, transparency))
    ob.visible_shadow = False
    CARRIERS[ob.name] = ob
    return ob


def wall_decal(tex, x, zb, w, h, layer, urange, tag=""):
    xa, xb = WALL_X + x - w / 2, WALL_X + x + w / 2
    y = -layer
    corners = [(xa, y, zb), (xb, y, zb), (xb, y, zb + h), (xa, y, zb + h)]
    u0, u1 = urange
    c = Vector(((xa + xb) / 2, y, zb + h / 2))
    ob = mesh_quad("D_" + tex + tag, corners, [(u0, 0), (u1, 0), (u1, 1), (u0, 1)], origin=c)
    ob.data.materials.append(decal_material("M_" + tex + tag, tex))
    ob.visible_shadow = False
    CARRIERS[ob.name] = ob
    return ob


def dummy(x, y, yaw=0.0):
    mat = flat_material("Dummy", (163, 162, 165), 0.6)
    parts = [(-0.5, 0, 1.0, 1, 1, 2), (0.5, 0, 1.0, 1, 1, 2), (0, 0, 3.0, 2, 1, 2), (-1.5, 0, 3.0, 1, 1, 2),
             (1.5, 0, 3.0, 1, 1, 2), (0, 0, 4.6, 1.2, 1.2, 1.2)]
    R = Matrix.Rotation(math.radians(yaw), 3, "Z")
    for i, (px, py, pz, sx, sy, sz) in enumerate(parts):
        p = R @ Vector((px, py, 0))
        ob = box(f"Dummy{i}", x + p.x - sx / 2, x + p.x + sx / 2, y + p.y - sy / 2, y + p.y + sy / 2, pz - sz / 2,
                 pz + sz / 2, mat)
        ob.rotation_euler = (0, 0, math.radians(yaw))


def garland(x0, x1, zt, yfront):
    """Placeholder garland (keep-out band reference): sagging rope + pennants."""
    cu = bpy.data.curves.new("Rope", "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = 0.14
    sp = cu.splines.new("POLY")
    n = 24
    sp.points.add(n)
    for i in range(n + 1):
        t = i / n
        x = x0 + (x1 - x0) * t
        z = zt - 2.6 * (1 - (2 * t - 1) ** 2)
        sp.points[i].co = (x, yfront, z, 1)
    rope = link(bpy.data.objects.new("Rope", cu))
    rope.data.materials.append(flat_material("RopeM", (92, 70, 50), 0.8))
    cols = [(232, 120, 30), (30, 26, 30), (120, 60, 150)]
    k = 0
    for i in range(1, 12):
        t = i / 12
        x = x0 + (x1 - x0) * t
        z = zt - 2.6 * (1 - (2 * t - 1) ** 2)
        me = bpy.data.meshes.new(f"Pen{i}")
        me.from_pydata([(x - 0.6, yfront, z), (x + 0.6, yfront, z), (x, yfront, z - 1.5)], [], [(0, 1, 2)])
        ob = link(bpy.data.objects.new(f"Pen{i}", me))
        ob.data.materials.append(flat_material(f"PenM{i}", cols[k % 3], 0.85))
        k += 1


def build_floor(with_decals=True):
    studded_plane("Floor_G1", -160, 6, -160, 160, GREEN)
    studded_plane("Floor_E1", 6, 7, -160, 160, BROWN)
    studded_plane("Floor_P", 7, 15, -160, 160, CREAM)
    studded_plane("Floor_E2", 15, 16, -160, 160, BROWN)
    studded_plane("Floor_G2", 16, 160, -160, 160, GREEN)
    dummy(-10.5, -12.0, 0)
    if with_decals:
        for (tex, c, _s, yaw, z, tr) in FLOOR_DECALS:
            floor_decal(tex, c, yaw, z, tr)


def build_wall(with_decals=True, tp_dummy=False):
    studded_plane("WFloor", WALL_X - 120, WALL_X + 120, -120, 0.0, GREEN)
    studded_plane("WFloorBack", WALL_X - 120, WALL_X + 120, 0.0, 120, GREEN)
    # wall: studded front face + plain body
    H = WALL_HALF
    corners = [(WALL_X - H, 0, 0), (WALL_X + H, 0, 0), (WALL_X + H, 0, 24), (WALL_X - H, 0, 24)]
    uvs = [(-H, 0), (H, 0), (H, 24), (-H, 24)]
    face = mesh_quad("WallFace", corners, uvs)
    face.data.materials.append(stud_material("WallFaceM", BLUE))
    box("WallBody", WALL_X - H, WALL_X + H, 0.001, 6, 0, 24, flat_material("WallBodyM", BLUE, 0.72))
    box("Trim", WALL_X - H - 0.3, WALL_X + H + 0.3, -0.3, 6.3, 22.9, 24.5, flat_material("TrimM", TRIM, 0.7))
    # the bay's pillars (2.5 wide, standing 1.7 proud of the wall face), as in the hub
    pm = flat_material("PillarM", PILLAR, 0.7)
    for i, px in enumerate(PILLAR_MX):
        box(f"Pillar{i}", WALL_X + px - PILLAR_W / 2, WALL_X + px + PILLAR_W / 2, PILLAR_FRONT, 0.3, 0, 24.5, pm)
    garland(WALL_X - FACE_IN, WALL_X + FACE_IN, 20.5, -0.9)
    dummy(WALL_X + 16.0, -4.0, 0)
    if tp_dummy:
        dummy(WALL_X - 1.0, -12.0, 0)        # the player's character for the third-person view
    if with_decals:
        for (tex, x, zb, w, h, layer, ur, tag) in WALL_DECALS:
            wall_decal(tex, x, zb, w, h, layer, ur, tag=tag)
        for (tex, c, yaw, z, tr) in WALL_FLOOR_DECALS:
            floor_decal(tex, (WALL_X + c[0], c[1]), yaw, z, tr, tag="_wf")


# ------------------------------------------------------------------ lighting
def lighting(cfg):
    cfg = dict(cfg)
    for k in ("sun", "sky_str", "exposure", "haze"):
        if "--" + k in ARGS:
            cfg[k] = float(arg("--" + k, 0))
    if "--vt" in ARGS:
        cfg["vt"] = arg("--vt", "AgX").replace("_", " ")
    if "--skycol" in ARGS:
        cfg["sky"] = tuple(float(v) for v in arg("--skycol", "").split(","))
    if "--suncol" in ARGS:
        cfg["sun_col"] = tuple(float(v) for v in arg("--suncol", "").split(","))
    sc = bpy.context.scene
    sc.view_settings.view_transform = cfg.get("vt", "AgX")
    try:
        sc.view_settings.look = cfg["look"] if sc.view_settings.view_transform == "AgX" else "None"
    except Exception:
        pass
    sc.view_settings.exposure = cfg["exposure"]
    w = sc.world
    w.use_nodes = True
    nt = w.node_tree
    bg = nt.nodes["Background"]
    # lighting rays see the ambient colour; camera rays see the displayed sky (night: dark blue + stars)
    amb = nt.nodes.new("ShaderNodeBackground")
    amb.inputs["Color"].default_value = (*cfg["sky"], 1)
    amb.inputs["Strength"].default_value = cfg["sky_str"]
    disp = nt.nodes.new("ShaderNodeBackground")
    disp.inputs["Strength"].default_value = 1.0
    dcol = cfg.get("sky_display", cfg["sky"])
    if cfg.get("stars"):
        tc = nt.nodes.new("ShaderNodeTexCoord")
        vor = nt.nodes.new("ShaderNodeTexVoronoi")
        vor.inputs["Scale"].default_value = 420.0
        nt.links.new(tc.outputs["Generated"], vor.inputs["Vector"])
        mr = nt.nodes.new("ShaderNodeMapRange")
        mr.inputs["From Min"].default_value = 0.0
        mr.inputs["From Max"].default_value = 0.05
        mr.inputs["To Min"].default_value = 1.0
        mr.inputs["To Max"].default_value = 0.0
        nt.links.new(vor.outputs["Distance"], mr.inputs["Value"])
        mix = nt.nodes.new("ShaderNodeMix")
        mix.data_type = "RGBA"
        mix.inputs[6].default_value = (*dcol, 1)
        mix.inputs[7].default_value = (0.9, 0.92, 1.0, 1)
        nt.links.new(mr.outputs["Result"], mix.inputs["Factor"])
        nt.links.new(mix.outputs[2], disp.inputs["Color"])
    else:
        disp.inputs["Color"].default_value = (*dcol, 1)
    lp = nt.nodes.new("ShaderNodeLightPath")
    ms = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(lp.outputs["Is Camera Ray"], ms.inputs["Fac"])
    nt.links.new(amb.outputs["Background"], ms.inputs[1])
    nt.links.new(disp.outputs["Background"], ms.inputs[2])
    nt.links.new(ms.outputs["Shader"], nt.nodes["World Output"].inputs["Surface"])
    ld = bpy.data.lights.new("Sun", "SUN")
    ld.energy = cfg["sun"]
    ld.color = cfg["sun_col"]
    ld.angle = math.radians(1.5)
    sun = link(bpy.data.objects.new("Sun", ld))
    d = Vector(cfg["sun_dir"]).normalized()
    sun.rotation_euler = (-d).to_track_quat("-Z", "Y").to_euler()


def lamp_pool(pos):
    ld = bpy.data.lights.new("Lamp", "SPOT")
    ld.energy = 9000
    ld.color = (1.0, 0.72, 0.42)
    ld.spot_size = math.radians(80)
    ld.spot_blend = 0.6
    ld.shadow_soft_size = 0.4
    ob = link(bpy.data.objects.new("Lamp", ld))
    ob.location = Vector(pos)
    ob.rotation_euler = (0, 0, 0)
    # a simple lamp post
    m = flat_material("PostM", (30, 28, 30), 0.6)
    box("Post", pos[0] - 0.25, pos[0] + 0.25, pos[1] + 1.8, pos[1] + 2.3, 0, pos[2] + 0.4, m)
    box("Arm", pos[0] - 0.2, pos[0] + 0.2, pos[1] - 0.2, pos[1] + 2.3, pos[2] + 0.2, pos[2] + 0.6, m)


# ------------------------------------------------------------------ cameras
def camera(loc, aim, fov=70.0, ortho=None):
    cd = bpy.data.cameras.new("Cam")
    cd.sensor_fit = "VERTICAL"
    cd.sensor_height = 24.0
    cd.clip_start = 0.1
    cd.clip_end = 3000
    if ortho:
        cd.type = "ORTHO"
        cd.ortho_scale = ortho
    else:
        cd.lens = 12.0 / math.tan(math.radians(fov / 2))
    cam = link(bpy.data.objects.new("Cam", cd))
    cam.location = Vector(loc)
    cam.rotation_euler = (Vector(aim) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    bpy.context.scene.camera = cam
    return cam


def render(path, border=None, pct=100):
    sc = bpy.context.scene
    sc.render.resolution_percentage = pct
    if border:
        sc.render.use_border = True
        sc.render.use_crop_to_border = True
        sc.render.border_min_x, sc.render.border_max_x, sc.render.border_min_y, sc.render.border_max_y = border
    else:
        sc.render.use_border = False
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
    sc.render.use_border = False
    sc.render.resolution_percentage = 100
    print("RENDERED", path, flush=True)


def force_order(top_name, cam_loc, bottom_name):
    """Blended surfaces sort per object (origin depth). Force a draw order by moving the BOTTOM decal's origin far
    behind the scene along the view ray (geometry unchanged), so it is drawn first and the top decal over it."""
    ob = CARRIERS[bottom_name]
    away = (ob.matrix_world.translation - Vector(cam_loc)).normalized()
    delta = away * 400.0
    ob.data.transform(Matrix.Translation(-delta))
    ob.location = ob.location + delta
    ob.data.update()
    return bottom_name, delta


def unforce(state):
    name, delta = state
    ob = CARRIERS[name]
    ob.data.transform(Matrix.Translation(delta))
    ob.location = ob.location - delta
    ob.data.update()


# ------------------------------------------------------------------ shot list
F_EYE25 = ((0, -25, 5), (0, 0, 0))
F_EYE60 = ((0, -60, 5), (0, 0, 0))
F_TP = ((-10.5, -12.0 - 11.7, 8.8), (-10.5, -12.0 + 6, 1.5))
W = WALL_X
W_EYE25 = ((W, -25, 5), (W, 0, 7))
W_EYE60 = ((W, -60, 5), (W, 0, 10))
W_OBL = ((W + 12.9, -15.3, 5), (W, 0, 6))
W_CLOSE8 = ((W - 3.55, -8, 3.0), (W - 3.55, 0, 1.6))   # crack C notch + the moss slot
W_TP4 = ((W - 2.0, -4.0, 5.5), (W - 3.0, 0, 0.8))
W_TP = ((W - 1.0, -23.7, 8.8), (W - 1.0, -12.0, 4.5))     # Roblox default third-person camera behind the dummy
# round 4: the two framings of the owner's live-game screenshots (ingame_round3\), 1520 x 752 like the captures
W_GAME_TP = ((W, -27.5, 9.0), (W, 0, 2.65))
W_GAME_CLOSE = ((W + 9.5, -9.5, 6.0), (W - 4.0, 0, 2.6))
GAME_RES = (1520, 752)
SAMPLES4 = {"wall": (W + 4.0, -0.02, 12.0), "wall2": (W - 6.0, -0.02, 14.0), "floor_shade": (W + 4.0, -3.5, 0.0),
            "floor_shade2": (W - 5.0, -4.0, 0.0), "floor_sun": (W + 3.0, -17.5, 0.0), "floor_sun2": (W - 5.0, -18.5, 0.0),
            "pillar": (W + 13.3, -1.72, 10.0)}


def shots_day(want):
    out = []
    S = lambda n: (SHOTS == "all" or n in want)
    return S


def run(set_name, cfg, shots, decals=True, lamp=None, tp_dummy=False):
    sc = fresh()
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    build_floor(decals)
    build_wall(decals, tp_dummy)
    lighting(cfg)
    if lamp:
        lamp_pool(lamp)
    for (name, loc, aim, kw) in shots:
        cam = camera(loc, aim, **kw.get("cam", {}))
        name = PREFIX + name
        res0 = (sc.render.resolution_x, sc.render.resolution_y)
        if "res" in kw:
            sc.render.resolution_x, sc.render.resolution_y = kw["res"]
        if "samples" in kw:                    # round 4: pixel positions of calibration sample points
            from bpy_extras.object_utils import world_to_camera_view
            bpy.context.view_layer.update()
            W_, H_ = sc.render.resolution_x, sc.render.resolution_y
            pix = {}
            for k, p in kw["samples"].items():
                v = world_to_camera_view(sc, cam, Vector(p))
                pix[k] = [round(v.x * W_, 1), round((1 - v.y) * H_, 1)]
            json.dump(pix, open(os.path.join(OUT, name + "_samples.json"), "w"), indent=1)
        if "order" in kw:
            st = force_order(kw["order"], loc, kw["under"])
            render(os.path.join(OUT, name + ".png"), kw.get("border"), kw.get("pct", 100))
            unforce(st)
        else:
            render(os.path.join(OUT, name + ".png"), kw.get("border"), kw.get("pct", 100))
        sc.render.resolution_x, sc.render.resolution_y = res0
        bpy.data.objects.remove(cam)


def main():
    os.makedirs(OUT, exist_ok=True)
    want = set(SHOTS.split(","))
    allw = SHOTS == "all"
    sel = lambda lst: [s for s in lst if allw or s[0] in want or (SHOTS == "calib" and s[0].startswith("calib"))]
    crop60 = (0.36, 0.64, 0.38, 0.62)
    day = [
        ("floor_eye25_day", *F_EYE25, {}),
        ("floor_eye25_day_half", *F_EYE25, {"pct": 50}),
        ("floor_eye60_day", *F_EYE60, {}),
        ("floor_eye60_day_crop", *F_EYE60, {"border": crop60}),
        ("floor_tp_day", *F_TP, {}),
        ("floor_top_ortho", (0, 0, 60), (0, 0.0001, 0), {"cam": {"ortho": 26}}),
        ("floor_close6_slime", (11.8, -8.6, 5), (11.8, -2.6, 0), {}),
        ("floor_close6_crack", (-3.4, -13.2, 5), (-3.4, -7.2, 0), {}),
        ("wall_eye25_day", *W_EYE25, {}),
        ("wall_eye25_day_half", *W_EYE25, {"pct": 50}),
        ("wall_eye60_day", *W_EYE60, {}),
        ("wall_eye60_day_crop", *W_EYE60, {"border": (0.33, 0.67, 0.3, 0.7)}),
        ("wall_oblique20_day", *W_OBL, {}),
        ("wall_close8_day", *W_CLOSE8, {}),
        ("wall_tp4_day", *W_TP4, {}),
        ("moss_close6_floor", (-14.6, -10.0, 5), (-14.6, -4.0, 0), {}),
        ("moss_close6_wall", (W + 0.4, -6.0, 4.0), (W + 0.4, 0, 1.2), {}),
        ("wall_foot_top_ortho", (W, -5.0, 40), (W, -4.9999, 0), {"cam": {"ortho": 30}}),
        # overlap pairs in BOTH draw orders (Roblox sorts transparent parts per part)
        ("order_floor_moss_over_stain", (-14.6, -14.0, 6), (-14.3, -4.3, 0), {"order": "D_G_Moss_A", "under": "D_G_Stain_A"}),
        ("order_floor_stain_over_moss", (-14.6, -14.0, 6), (-14.3, -4.3, 0), {"order": "D_G_Stain_A", "under": "D_G_Moss_A"}),
        ("order_floor_crack_over_stain", (2.0, -15.0, 6), (2.0, -6.5, 0), {"order": "D_G_Crack_C", "under": "D_G_Stain_B"}),
        ("order_floor_stain_over_crack", (2.0, -15.0, 6), (2.0, -6.5, 0), {"order": "D_G_Stain_B", "under": "D_G_Crack_C"}),
        ("order_wall_moss_over_crack", (W - 3.55, -9.0, 4.0), (W - 3.55, 0, 2.5), {"order": "D_W_MossBase_A", "under": "D_W_Crack_C"}),
        ("order_wall_crack_over_moss", (W - 3.55, -9.0, 4.0), (W - 3.55, 0, 2.5), {"order": "D_W_Crack_C", "under": "D_W_MossBase_A"}),
        ("order_wallfoot_moss_over_stain", (W + 2.0, -13.0, 6), (W + 1.5, -4.0, 0), {"order": "D_G_Moss_A_wf", "under": "D_G_Stain_A_wf"}),
        ("order_wallfoot_stain_over_moss", (W + 2.0, -13.0, 6), (W + 1.5, -4.0, 0), {"order": "D_G_Stain_A_wf", "under": "D_G_Moss_A_wf"}),
    ]
    night = [
        ("floor_eye25_night", *F_EYE25, {}),
        ("floor_eye60_night", *F_EYE60, {}),
        ("floor_tp_night", *F_TP, {}),
        ("wall_eye25_night", *W_EYE25, {}),
        ("wall_eye60_night", *W_EYE60, {}),
    ]
    before_day = [("floor_eye25_day_before", *F_EYE25, {}), ("floor_eye60_day_before", *F_EYE60, {}),
                  ("wall_eye25_day_before", *W_EYE25, {}), ("wall_eye60_day_before", *W_EYE60, {})]
    before_night = [("floor_eye25_night_before", *F_EYE25, {}), ("wall_eye25_night_before", *W_EYE25, {})]
    lamp = [("floor_night_lamp", (-27.0, -17.0, 8.5), (-13.0, -4.0, 0), {})]
    tp_day = [("wall_tp_day", *W_TP, {})]
    tp_night = [("wall_tp_night", *W_TP, {})]
    calib = [("calib_floor_day", *F_EYE25, {}), ("calib_wall_day", *W_EYE25, {})]
    calibn = [("calib_floor_night", *F_EYE25, {}), ("calib_wall_night", *W_EYE25, {})]
    if SHOTS == "calib":
        run("calib", DAY, calib, decals=False)
        run("calibn", NIGHT, calibn, decals=False)
        return
    if SHOTS == "calib4":                       # round 4 fitter: plain wall bay, live-game framing, sample points
        g = {"res": GAME_RES, "samples": SAMPLES4}
        run("calib4", DAY, [("calib4_day", *W_GAME_TP, g)], decals=False)
        run("calib4n", NIGHT, [("calib4_night", *W_GAME_TP, g)], decals=False)
        # round 5: the same framing WITH the decal set given by --decals (the round-3 set the owner's screenshots
        # show): the wall moss is a second, known material for the night sky colour
        run("calib4m", DAY, [("calib4m_day", *W_GAME_TP, {"res": GAME_RES})])
        run("calib4mn", NIGHT, [("calib4m_night", *W_GAME_TP, {"res": GAME_RES})])
        return
    game_day = [("game_tp_day", *W_GAME_TP, {"res": GAME_RES}), ("game_close_day", *W_GAME_CLOSE, {"res": GAME_RES})]
    game_night = [("game_tp_night", *W_GAME_TP, {"res": GAME_RES})]
    game_before = [("game_tp_day_before", *W_GAME_TP, {"res": GAME_RES})]
    if SHOTS == "game" or allw:
        run("game_day", DAY, game_day)
        run("game_night", NIGHT, game_night)
        run("game_before", DAY, game_before, decals=False)
        if SHOTS == "game":
            return
    if sel(day):
        run("day", DAY, sel(day))
    if sel(night):
        run("night", NIGHT, sel(night))
    if sel(before_day):
        run("before_day", DAY, sel(before_day), decals=False)
    if sel(before_night):
        run("before_night", NIGHT, sel(before_night), decals=False)
    if sel(tp_day):
        run("tp_day", DAY, sel(tp_day), tp_dummy=True)
    if sel(tp_night):
        run("tp_night", NIGHT, sel(tp_night), tp_dummy=True)
    if sel(lamp):
        run("lamp", NIGHT, sel(lamp), lamp=(-13.0, -3.0, 10.0))


main()
