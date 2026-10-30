import bpy, os, sys, time, math
import numpy as np
sys.path.insert(0, r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween")
OSL = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween\vfx\osl"
OUT = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween\vfx\_work"
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.shading_system = True
sc.cycles.samples = int(sys.argv[-1]); sc.cycles.use_denoising = False; sc.cycles.use_adaptive_sampling = False
sc.cycles.max_bounces = 1; sc.cycles.volume_bounces = 1; sc.cycles.volume_step_rate = float(sys.argv[-2])
sc.render.resolution_x = sc.render.resolution_y = 256
sc.render.film_transparent = True
w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True
w.node_tree.nodes["Background"].inputs["Color"].default_value = (0.55, 0.6, 0.7, 1)
w.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.5
ld = bpy.data.lights.new("Sun", "SUN"); ld.energy = 3.0; ld.angle = math.radians(8)
lo = bpy.data.objects.new("Sun", ld); sc.collection.objects.link(lo)
lo.rotation_euler = (math.radians(-40), math.radians(-30), 0)   # from up-left-front
bpy.ops.mesh.primitive_cube_add(size=2.0)
cube = bpy.context.active_object
txt = bpy.data.texts.new("s.osl")
txt.write(open(os.path.join(OSL, "common.h")).read() + "\n" + open(os.path.join(OSL, "smoke_vol.osl")).read())
mat = bpy.data.materials.new("V"); mat.use_nodes = True; nt = mat.node_tree
for n in list(nt.nodes):
    if n.type != "OUTPUT_MATERIAL": nt.nodes.remove(n)
out = nt.nodes["Material Output"]
sn = nt.nodes.new("ShaderNodeScript"); sn.mode = "INTERNAL"; sn.script = txt
pv = nt.nodes.new("ShaderNodeVolumePrincipled")
nt.links.new(sn.outputs["Density"], pv.inputs["Density"])
nt.links.new(sn.outputs["Albedo"], pv.inputs["Color"])
nt.links.new(pv.outputs[0], out.inputs["Volume"])
cube.data.materials.append(mat)
cd = bpy.data.cameras.new("C"); cd.type = "ORTHO"; cd.ortho_scale = 2
cam = bpy.data.objects.new("C", cd); sc.collection.objects.link(cam); cam.location = (0, 0, 10); sc.camera = cam
sc.render.image_settings.file_format = "OPEN_EXR"; sc.render.image_settings.color_depth = "32"
sc.render.image_settings.color_mode = "RGBA"
for f in (2, 8):
    sn.inputs["frame"].default_value = f
    sc.render.filepath = os.path.join(OUT, f"vol_test_{f}.exr")
    t = time.time(); bpy.ops.render.render(write_still=True); print("FRAME", f, "s", round(time.time() - t, 1))
    img = bpy.data.images.load(sc.render.filepath)
    a = np.empty(256 * 256 * 4, np.float32); img.pixels.foreach_get(a); a = a.reshape(256, 256, 4)
    print("alpha max", a[..., 3].max(), "rgb max", a[..., :3].max())
