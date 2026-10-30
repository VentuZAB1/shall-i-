# builder E pose helper (background Blender):
#   blender -b --factory-startup --python Cvetibara/_poses.py -- <Name> <view> act:frame,act:frame,...
# Builds model + rig + clips (no save) and renders pose shots from one view (tq|side|front|back) into
# <Name>/renders/pose_<view>_<act>_<f>.png
import sys, runpy
argv = sys.argv[sys.argv.index("--") + 1:]
name, view = argv[0], argv[1]
picks = [(t.split(":")[0], int(t.split(":")[1])) for t in argv[2].split(",")]
R3 = runpy.run_path(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\run3.py")
R3["full"](name, save=False)
k = R3["STATE"]["k"]
files = R3["pk"].pose_renders(k, picks, view=view, res=300)
print("POSES", files)
