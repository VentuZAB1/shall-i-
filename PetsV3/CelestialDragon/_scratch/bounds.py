# prints the rest bounds of a pet model without rendering (read-only for other pets)
import sys, runpy
argv = sys.argv[sys.argv.index("--") + 1:]
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
m = R3["spec"](argv[0])
k = R3["new_pet"](m, argv[0])
info = m.model(k)
mn, mx = k.bounds()
print("HEADLESS_RESULT", [round(v, 3) for v in mn], [round(v, 3) for v in mx], info)
