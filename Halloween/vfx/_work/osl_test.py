import bpy, os, sys, time
import numpy as np
OUT = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween\vfx\_work"
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = "CYCLES"
sc.cycles.device = "CPU"
sc.cycles.shading_system = True
sc.cycles.samples = 16
sc.render.resolution_x = sc.render.resolution_y = 256
sc.render.film_transparent = True
osl = '''
shader flame(float T = 0.0, output color Col = 0, output float A = 0) {
    point p = P;
    float n = noise("perlin", point(p[0]*4, p[1]*4 - T*3, 0), T);
    Col = color(1, 0.5, 0.1) * (0.5 + 0.5*n);
    A = clamp(1.0 - length(vector(p[0], p[1], 0)), 0, 1);
}
'''
txt = bpy.data.texts.new("flame.osl"); txt.write(osl)
mat = bpy.data.materials.new("M")
nt = mat.node_tree if mat.node_tree else None
mat.use_nodes = True
nt = mat.node_tree
for n in list(nt.nodes):
    if n.type != "OUTPUT_MATERIAL": nt.nodes.remove(n)
sn = nt.nodes.new("ShaderNodeScript"); sn.mode = "INTERNAL"; sn.script = txt
bpy.ops.wm.context_toggle  # noop
try:
    sn.update()
except Exception as e:
    print("update err", e)
print("script outputs", [o.name for o in sn.outputs], "inputs", [i.name for i in sn.inputs])
em = nt.nodes.new("ShaderNodeEmission")
nt.links.new(sn.outputs["Col"], em.inputs["Color"])
nt.links.new(em.outputs[0], nt.nodes["Material Output"].inputs["Surface"])
bpy.ops.mesh.primitive_plane_add(size=2.0)
pl = bpy.context.active_object
pl.data.materials.append(mat)
cd = bpy.data.cameras.new("C"); cd.type = "ORTHO"; cd.ortho_scale = 2
cam = bpy.data.objects.new("C", cd); sc.collection.objects.link(cam); cam.location = (0,0,5); sc.camera = cam
sc.render.image_settings.file_format = "OPEN_EXR"
sc.render.filepath = os.path.join(OUT, "osl_test.exr")
t = time.time()
bpy.ops.render.render(write_still=True)
print("render s", time.time() - t)
img = bpy.data.images.load(os.path.join(OUT, "osl_test.exr"))
a = np.array(img.pixels[:], dtype=np.float32).reshape(256, 256, 4)
print("px center", a[128,128], "corner", a[0,0], "max", a[..., :3].max())
