# blender -b --factory-startup --python _tools/headless_pack.py -- <Name> [views=side,tq,game] [res=400]
# Review-pack renders for a rigged pet (idle f0): <Name>_portrait_raw.png (the game portrait camera) and FLAT palette
# ID renders renders/flat_<view>.png (emission = the block vertex colour, no light / AO / studs) for exact value shares.
# Then run (system python): python _tools/pack_post.py <Name> <CmpA,CmpB,...>
import sys, runpy, json, os
argv = sys.argv[sys.argv.index("--") + 1:]
name = argv[0]
opts = dict(a.split("=", 1) for a in argv[1:] if "=" in a)
views = opts.get("views", "side,tq,game").split(",")
res = int(opts.get("res", "400"))
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
pk = R3["pk"]
if hasattr(R3["spec"](name), "anim"):
    R3["full"](name, save=False)
    k = R3["STATE"]["k"]
    k.set_action("idle")
    bpy.context.scene.frame_set(0)
    pk.portrait(k)
else:                                   # model-only round (no clips yet): portrait at rest, same camera
    R3["model"](name, views=("tq",), res=200)
    k = R3["STATE"]["k"]
    sc0 = bpy.context.scene
    g0 = bpy.data.objects.get("Ground")
    if g0:
        g0.hide_render = True
    sc0.render.film_transparent = True
    sc0.render.resolution_x = sc0.render.resolution_y = 512
    loc, tgt = pk.camera_for(k, "tq")
    pk.aim(sc0.camera, loc, tgt)
    sc0.render.filepath = os.path.join(k.dir, name + "_portrait_raw.png")
    sc0.render.image_settings.color_mode = "RGBA"
    bpy.ops.render.render(write_still=True)
    sc0.render.film_transparent = False
    sc0.render.image_settings.color_mode = "RGB"
sc = bpy.context.scene
ground = bpy.data.objects.get("Ground")
if ground:
    ground.hide_render = True
w = sc.world
w.node_tree.nodes["Background"].inputs["Color"].default_value = (0, 0, 0, 1)
for o in bpy.data.objects:
    if o.type == "LIGHT":
        o.hide_render = True
flat = bpy.data.materials.new("FlatID")
flat.use_nodes = True
nt = flat.node_tree
for n in list(nt.nodes):
    nt.nodes.remove(n)
attr = nt.nodes.new("ShaderNodeAttribute")
attr.attribute_name = "Col"
em = nt.nodes.new("ShaderNodeEmission")
outn = nt.nodes.new("ShaderNodeOutputMaterial")
nt.links.new(attr.outputs["Color"], em.inputs["Color"])
nt.links.new(em.outputs["Emission"], outn.inputs["Surface"])
for o in k.coll.objects:
    if o.type == "MESH":
        o.data.materials.clear()
        o.data.materials.append(flat)
sc.view_settings.view_transform = "Standard"
sc.render.resolution_x = sc.render.resolution_y = res
try:
    sc.eevee.use_gtao = False
except Exception:
    pass
cam = sc.camera
files = []
for v in views:
    loc, tgt = pk.camera_for(k, v)
    pk.aim(cam, loc, tgt)
    p = os.path.join(k.dir, "renders", "flat_%s.png" % v)
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    files.append(p)
print("HEADLESS_RESULT " + json.dumps({"portrait": os.path.join(k.dir, name + "_portrait_raw.png"), "flat": files}))
