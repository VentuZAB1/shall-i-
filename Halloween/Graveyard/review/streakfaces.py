# Reviewer: which 3D faces of Grave_C sample the streaky atlas band (u 0.47-0.76, v 0.41-0.55)? + debug render
import bpy, bmesh, os, math, sys
import numpy as np
from mathutils import Vector
sys.path.insert(0, r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween")
from hkit import review_setup, link
D = os.path.dirname(os.path.abspath(__file__))
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=r"C:\cdimp\Halloween_Grave_C.fbx")
ob = [o for o in bpy.context.scene.objects if o.type == "MESH"][0]
ob.scale = (1, 1, 1)
me = ob.data
uv = me.uv_layers.active.data
hits = []
for p in me.polygons:
    u = sum(uv[l].uv.x for l in p.loop_indices) / p.loop_total
    v = sum(uv[l].uv.y for l in p.loop_indices) / p.loop_total
    if 0.47 < u < 0.76 and 0.41 < v < 0.55:
        hits.append((tuple(round(c, 2) for c in p.center), tuple(round(c, 2) for c in p.normal), round(p.area, 4)))
print("N faces in band", len(hits))
c = np.array([h[0] for h in hits]); n = np.array([h[1] for h in hits])
if len(c):
    print("centroid bbox", c.min(0), c.max(0)); print("mean normal", n.mean(0))
# debug renders: normal map / albedo as emission
sc = bpy.context.scene; sc.world = bpy.data.worlds.new("W"); review_setup(res=(1200, 900))
mat = me.materials[0]; nt = mat.node_tree
for key in ("normal", "albedo"):
    img = [nd for nd in nt.nodes if nd.type == "TEX_IMAGE" and key in nd.image.name][0]
    out = [nd for nd in nt.nodes if nd.type == "OUTPUT_MATERIAL"][0]
    em = nt.nodes.new("ShaderNodeEmission")
    nt.links.new(img.outputs["Color"], em.inputs["Color"]); nt.links.new(em.outputs["Emission"], out.inputs["Surface"])
    sc.view_settings.view_transform = "Standard"
    cd = bpy.data.cameras.new("C"); cam = link(bpy.data.objects.new("C", cd)); cd.lens = 50
    for tag, loc in (("r34", (5.0, -4.6, 4.2)), ("right", (7.0, 0.3, 3.4))):
        cam.location = loc; cam.rotation_euler = (Vector((0.4, 0, 2.6)) - cam.location).to_track_quat("-Z", "Y").to_euler()
        sc.camera = cam; sc.render.filepath = os.path.join(D, f"debug_GraveC_{key}_{tag}.png"); bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(cam)
