import bpy, sys, os
sys.path.insert(0, r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween\DeadTrees")
from treekit import *
a = sys.argv[sys.argv.index("--") + 1:]
bpy.ops.wm.open_mainfile(filepath=a[0])
sc = review_setup(res=(1280, 900))
sc.world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.3, 0.5, 0.8, 1)
for o in list(bpy.data.objects):
    if o.type == "LIGHT":
        o.hide_render = True
    if o.type != "MESH" or o.hide_render:
        continue
    for m in o.data.materials:
        if not m or not m.use_nodes:
            continue
        nt = m.node_tree
        tex = [n for n in nt.nodes if n.type == "TEX_IMAGE" and n.image and "albedo" in n.image.name.lower()]
        out = [n for n in nt.nodes if n.type == "OUTPUT_MATERIAL"]
        if tex and out:
            em = nt.nodes.new("ShaderNodeEmission")
            nt.links.new(tex[0].outputs["Color"], em.inputs["Color"])
            nt.links.new(em.outputs["Emission"], out[0].inputs["Surface"])
        m.use_backface_culling = True
shots = eval(a[1])
for nm, (loc, tgt) in shots.items():
    shoot_fov(os.path.join(WIP, "alb_" + nm + ".png"), loc, tgt, vfov=70)
