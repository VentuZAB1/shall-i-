# blender -b --factory-startup --python MossbackTortoise/_bounds.py -- Name1,Name2,...  -> prints model heights (no files)
import sys, runpy
argv = sys.argv[sys.argv.index("--") + 1:]
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
import bpy
for name in argv[0].split(","):
    m = R3["spec"](name)
    k = R3["new_pet"](m, name)
    m.model(k)
    mn, mx = k.bounds()
    h = mx.z - mn.z
    print("BOUNDS %s height %.3f HEIGHT %.1f U %.4f pitch_now %.4f" % (name, h, m.HEIGHT, h / m.HEIGHT,
                                                                       getattr(m, "PITCH", 0)))
