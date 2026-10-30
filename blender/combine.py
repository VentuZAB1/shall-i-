"""Merge every creature source .blend into one FBX for a single Studio import.
Objects are renamed '<Creature>__<Part>' and spread along X (8 units apart).
blender -b -P combine.py"""
import bpy, os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import creature_kit as K

NAMES = ["MossbackTortoise", "ForestFawn", "TreantSprout", "VineSerpent",
         "SeaTurtlePup", "Kappa", "Hippocampus", "KrakenHatchling",
         "SparkFox", "Raiju", "CloudRam", "ThunderBull", "Thunderbird", "StormWyvern"]

bpy.ops.wm.read_factory_settings(use_empty=True)
joints = {}
for i, name in enumerate(NAMES):
    path = os.path.join(K.SOURCE, name + ".blend")
    with bpy.data.libraries.load(path) as (src, dst):
        dst.objects = [n for n in src.objects if not n.startswith("Cam")]
    off = i * 8.0
    joints[name] = {"offsetX": off, "parts": {}}
    for ob in dst.objects:
        if ob is None or ob.type != "MESH":
            continue
        bpy.context.scene.collection.objects.link(ob)
        part = ob.name.split(".")[0]
        ob.location.x += off
        ob.name = "%s__%s" % (name, part)
        joints[name]["parts"][part] = list(ob.location)

bpy.ops.object.select_all(action="DESELECT")
for ob in bpy.context.scene.objects:
    ob.select_set(True)
out = os.path.join(K.EXPORT, "AllCreatures.fbx")
bpy.ops.export_scene.fbx(filepath=out, use_selection=True, path_mode="COPY", embed_textures=True,
                         apply_unit_scale=True, object_types={"MESH"}, add_leaf_bones=False)
with open(os.path.join(K.EXPORT, "AllCreatures_joints.json"), "w") as f:
    json.dump(joints, f, indent=1)
print("COMBINED", len(bpy.context.scene.objects), "objects ->", out)
