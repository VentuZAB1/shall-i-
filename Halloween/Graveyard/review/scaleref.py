import bpy
for n in ["Halloween_PumpkinEgg_Plain1", "Halloween_Grave_A"]:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.fbx(filepath=rf"C:\cdimp\{n}.fbx")
    for o in bpy.context.scene.objects:
        if o.type == "MESH":
            print("SCALEREF", n, o.name, tuple(round(s, 4) for s in o.scale), tuple(round(d / o.scale[0], 2) for d in o.dimensions))
