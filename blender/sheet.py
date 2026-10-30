"""Contact sheet of creature renders. blender -b -P sheet.py -- out.png Name1 Name2 ..."""
import bpy, os, sys
import numpy as np
ROOT = os.path.dirname(os.path.abspath(__file__))
args = sys.argv[sys.argv.index("--") + 1:]
out, names = args[0], args[1:]
cols = min(4, len(names))
rows = (len(names) + cols - 1) // cols
S = 512
sheet = np.zeros((rows * S, cols * S, 4), dtype=np.float32)
for i, n in enumerate(names):
    img = bpy.data.images.load(os.path.join(ROOT, "renders", n + ".png"))
    px = np.array(img.pixels[:], dtype=np.float32).reshape(img.size[1], img.size[0], 4)
    r, c = rows - 1 - i // cols, i % cols
    sheet[r * S:(r + 1) * S, c * S:(c + 1) * S] = px[:S, :S]
res = bpy.data.images.new("sheet", cols * S, rows * S)
res.pixels = sheet.ravel()
res.filepath_raw = os.path.join(ROOT, "renders", out)
res.file_format = "PNG"
res.save()
print("SHEET_OK", out)
