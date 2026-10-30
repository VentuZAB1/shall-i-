# blender -b --factory-startup --python MossbackTortoise/_rigtest.py -- Name1,Name2  -> builds model + rig in memory
import sys, runpy, traceback
argv = sys.argv[sys.argv.index("--") + 1:]
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
for name in argv[0].split(","):
    try:
        for o in list(bpy.data.objects):
            bpy.data.objects.remove(o)
        m = R3["spec"](name)
        k = R3["new_pet"](m, name)
        m.model(k)
        m.rig(k)
        k.build_rig()
        bones = [b.name for b in k.arm.data.bones]
        print("RIGTEST %s ok %d bones: %s" % (name, len(bones), " ".join(bones)))
    except Exception:
        print("RIGTEST %s FAIL %s" % (name, traceback.format_exc()[-600:]))
