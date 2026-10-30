# Independent reviewer renders: imports the exported FBX files fresh, hub-like sunny lighting, backface culling on.
# Usage: blender -b --factory-startup --python render.py -- <shot> [<shot> ...]
import bpy, sys, os, math
from mathutils import Vector
sys.path.insert(0, r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween")
from hkit import review_setup, link, lin   # read-only use
D = os.path.dirname(os.path.abspath(__file__))
ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
NAMES = ["Grave_A", "Grave_B", "Grave_C", "DeadGrass_A", "DeadGrass_B"]


def base_scene(res=(1920, 1080), sun_rot=None, soil=None):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.world = bpy.data.worlds.new("W")
    review_setup(res=res)
    sc.eevee.taa_render_samples = 32
    if sun_rot:
        sun = bpy.data.objects["Sun"]
        sun.rotation_euler = tuple(math.radians(a) for a in sun_rot)
    bpy.data.lights["Sun"].angle = math.radians(3)
    # green grass ground
    bpy.ops.mesh.primitive_plane_add(size=600, location=(0, 0, 0))
    g = bpy.context.active_object; g.name = "Ground"
    m = bpy.data.materials.new("Grass"); m.use_nodes = True
    nt = m.node_tree; bs = nt.nodes["Principled BSDF"]
    bs.inputs["Roughness"].default_value = 0.95
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 0.35
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].color = (*lin((78, 138, 56)), 1)
    ramp.color_ramp.elements[1].color = (*lin((98, 158, 64)), 1)
    nt.links.new(nz.outputs["Fac"], ramp.inputs["Fac"]); nt.links.new(ramp.outputs["Color"], bs.inputs["Base Color"])
    g.data.materials.append(m)
    if soil:
        for (x, y, r) in soil:
            bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=r, depth=0.2, location=(x, y, -0.09))
            s = bpy.context.active_object
            sm = bpy.data.materials.get("Soil") or bpy.data.materials.new("Soil")
            sm.use_nodes = True
            sb = sm.node_tree.nodes["Principled BSDF"]
            sb.inputs["Base Color"].default_value = (*lin((96, 70, 48)), 1); sb.inputs["Roughness"].default_value = 1
            s.data.materials.append(sm)
    return sc


def imp(name, loc=(0, 0, 0), yaw=0.0):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.fbx(filepath=os.path.join(r"C:\cdimp", "Halloween_" + name + ".fbx"))
    obs = [o for o in bpy.data.objects if o not in before and o.type == "MESH"]
    for o in obs:
        o.scale = (1, 1, 1)          # FBX imports at 0.01: raw units are studs
        o.location = Vector(loc)
        o.rotation_euler = (0, 0, math.radians(yaw))
        for mt in o.data.materials:
            mt.use_backface_culling = True
    return obs


def ref_block(loc, h=5.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(loc[0], loc[1], h / 2))
    b = bpy.context.active_object; b.name = "Ref5"
    b.scale = (2.0, 1.0, h)
    m = bpy.data.materials.new("Ref"); m.use_nodes = True
    m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (*lin((210, 60, 60)), 1)
    b.data.materials.append(m)
    # 1-stud tick marks: thin dark bands every stud
    for z in range(1, int(h)):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(loc[0], loc[1] - 0.505, z))
        t = bpy.context.active_object; t.scale = (2.02, 0.02, 0.05)
        tm = bpy.data.materials.get("Tick") or bpy.data.materials.new("Tick")
        tm.use_nodes = True
        tm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.02, 0.02, 0.02, 1)
        t.data.materials.append(tm)
    return b


def cam_shot(path, loc, target, fov_v=None, lens=None):
    sc = bpy.context.scene
    cd = bpy.data.cameras.new("Cam")
    cam = link(bpy.data.objects.new("Cam", cd))
    cam.location = Vector(loc)
    cam.rotation_euler = (Vector(target) - cam.location).to_track_quat("-Z", "Y").to_euler()
    cd.clip_end = 5000
    if fov_v:
        cd.sensor_fit = "VERTICAL"; cd.angle_y = math.radians(fov_v)   # Roblox default FieldOfView = 70 (vertical)
    else:
        cd.lens = lens or 50
    sc.camera = cam
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(cam)
    print("WROTE", path)


LINEUP = [("Grave_A", -8.5), ("Grave_B", -3.6), ("Grave_C", 1.2), ("DeadGrass_A", 6.0), ("DeadGrass_B", 10.0)]


def lineup(soil=False):
    sc = base_scene(soil=[(0.8, 0.5, 13)] if soil else None)
    for n, x in LINEUP:
        imp(n, (x, 0, 0))
    ref_block((14.0, 0.0))
    return sc


for shot in ARGS:
    if shot == "lineup":
        lineup()
        tgt = (1.0, 0, 1.6)
        for d in (25, 45):
            cam_shot(os.path.join(D, f"lineup_{d}studs_fov70.png"), (1.0, -d, 5.0), tgt, fov_v=70)
            cam_shot(os.path.join(D, f"lineup_{d}studs_tele.png"), (1.0, -d, 5.0), tgt, lens=1.25 * d)
            cam_shot(os.path.join(D, f"graves_{d}studs_tele.png"), (-3.6, -d, 5.0), (-3.6, 0, 1.8), lens=2.0 * d)
    elif shot == "lineup_side":     # sun from behind-left: front faces in shade
        lineup()
        bpy.data.objects["Sun"].rotation_euler = (math.radians(55), 0, math.radians(200))
        cam_shot(os.path.join(D, "lineup_25studs_backlit_tele.png"), (1.0, -25, 5.0), (1.0, 0, 1.6), lens=31)
        cam_shot(os.path.join(D, "graves_40studs_backlit_tele.png"), (-3.6, -40, 5.0), (-3.6, 0, 1.8), lens=80)
    elif shot == "bed":             # in a soil bed like the hub, 3rd-person camera height
        sc = base_scene(soil=[(0, 0, 9)])
        imp("Grave_A", (-3.2, 1.0, 0), 8); imp("Grave_B", (0.6, 2.4, 0), -6); imp("Grave_C", (4.2, 0.6, 0), -14)
        for (n, x, y, r) in [("DeadGrass_A", -6.5, -1.5, 0), ("DeadGrass_B", -0.9, -2.2, 40), ("DeadGrass_B", 2.6, -3.0, 140),
                             ("DeadGrass_A", 7.0, -2.0, 200), ("DeadGrass_B", 6.6, 3.2, 300), ("DeadGrass_A", -1.5, 4.8, 90)]:
            imp(n, (x, y, 0), r)
        ref_block((-9.0, 2.0))
        cam_shot(os.path.join(D, "bed_40studs_fov70.png"), (2, -40, 5.0), (0, 0, 1.5), fov_v=70)
        cam_shot(os.path.join(D, "bed_40studs_tele.png"), (2, -40, 5.0), (0, 0, 1.5), lens=85)
        cam_shot(os.path.join(D, "bed_20studs_high.png"), (6, -18, 12.0), (0, 0, 1.2), lens=35)
    elif shot.startswith("close_"):
        n = shot[6:]
        base_scene()
        imp(n)
        h = 2.0 if n.startswith("Grave") else 1.2
        dist = 7.5 if n.startswith("Grave") else 5.5
        cam_shot(os.path.join(D, f"close_{n}_front.png"), (0, -dist, 4.2), (0, 0, h), lens=50)
        cam_shot(os.path.join(D, f"close_{n}_34.png"), (dist * 0.75, -dist * 0.7, 3.8), (0, 0, h), lens=50)
        cam_shot(os.path.join(D, f"close_{n}_back.png"), (-dist * 0.6, dist * 0.85, 3.6), (0, 0, h), lens=50)
    elif shot.startswith("mid_"):
        n = shot[4:]
        base_scene()
        imp(n)
        cam_shot(os.path.join(D, f"mid12_{n}_34.png"), (12 * 0.6, -12 * 0.8, 5.0), (0, 0, 1.6), lens=40)
    elif shot == "scale2":
        base_scene(res=(1920, 820))
        g = bpy.data.objects["Ground"]; g.hide_render = True        # show the buried parts against the sky
        bpy.data.worlds["W"].node_tree.nodes["Background"].inputs["Color"].default_value = (0.75, 0.78, 0.8, 1)
        xs = [("Grave_A", -14.0), ("Grave_B", -8.5), ("Grave_C", -3.0), ("DeadGrass_A", 2.8), ("DeadGrass_B", 7.6)]
        for n, x in xs:
            imp(n, (x, 0, 0))
        ref_block((12.0, 0.0))
        for z, nm in ((0.0, "Z0"), (-0.3, "Zm03")):
            bpy.ops.mesh.primitive_cube_add(size=1, location=(-1, -3, z)); b = bpy.context.active_object
            b.scale = (36, 0.01, 0.015)
            mm = bpy.data.materials.new(nm); mm.use_nodes = True
            mm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0, 0, 0, 1) if z == 0 else (0.8, 0, 0, 1)
            b.data.materials.append(mm)
        cd = bpy.data.cameras.new("Cam"); cam = link(bpy.data.objects.new("Cam", cd))
        cd.type = "ORTHO"; cd.ortho_scale = 34
        cam.location = (-1, -60, 2.0); cam.rotation_euler = (math.radians(90), 0, 0)
        sc = bpy.context.scene; sc.camera = cam
        sc.render.filepath = os.path.join(D, "scale_front_ortho.png"); bpy.ops.render.render(write_still=True)
        print("WROTE", sc.render.filepath)
        cam.location = (40, 0, 2.0); cam.rotation_euler = (math.radians(90), 0, math.radians(90))
        for o in list(bpy.data.objects):
            if o.type == "MESH" and (o.name.startswith("DeadGrass") or o.name.startswith("Ref") or o.name.startswith("Cube")):
                o.hide_render = True
        cd.ortho_scale = 8
        for nm_, x in xs[:3]:
            cam.location = (x + 40, 0, 2.0)
            for o in bpy.data.objects:
                if o.type == "MESH" and o.name.startswith("Grave"):
                    o.hide_render = not o.name.startswith(nm_)
            sc.render.resolution_x, sc.render.resolution_y = 900, 900
            sc.render.filepath = os.path.join(D, f"side_ortho_{nm_}.png"); bpy.ops.render.render(write_still=True)
            print("WROTE", sc.render.filepath)
    elif shot == "scale":
        base_scene(res=(1920, 900))
        for n, x in LINEUP:
            imp(n, (x, 0, 0))
        ref_block((14.0, 0.0))
        cam_shot(os.path.join(D, "scale_front_ortho.png"), (1.0, -60, 2.2), (1.0, 0, 2.2), lens=150)
        cam_shot(os.path.join(D, "scale_side.png"), (60, -0.0, 2.2), (0, 0, 2.2), lens=95)
