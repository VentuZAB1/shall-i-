import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import creature_kit as K

K.new_scene("_test")
K.palette({"fur": "#c98a4b", "white": "#ffffff"})
body = K.box("Body", (1.0, 1.6, 0.8), (0, 0, 0.8), "fur")
head = K.ellipsoid("Head", (0.5, 0.5, 0.45), (0, -1.0, 1.3), "fur")
eye = K.ellipsoid("EyeL", (0.12, 0.08, 0.12), (0.2, -1.4, 1.4), "white")
head = K.join_as("Head", [head, eye])
K.pivot(head, (0, -0.8, 1.1))
tris = K.tri_count()
assert 0 < tris < 3000, tris
assert {o.name for o in K.meshes()} == {"Body", "Head"}, [o.name for o in K.meshes()]
out = os.path.join(K.EXPORT, "_test.fbx")
K.export_fbx(out)
assert os.path.getsize(out) > 0
print("KIT_TEST_OK", tris)
