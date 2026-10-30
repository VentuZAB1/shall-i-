import bpy, numpy as np, os
OUT = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween\vfx\_work"
img = bpy.data.images.new("t", 4, 2, alpha=True)
print("float?", img.is_float, "cs", img.colorspace_settings.name, "alpha_mode", img.alpha_mode)
a = np.zeros((2, 4, 4), np.float32)
a[..., 0] = 0.5; a[..., 1] = 0.25; a[..., 2] = 0.1; a[..., 3] = 0.3
a[1, 0] = (1.0, 0.5, 0.0, 0.0)   # top-left pixel in PIL terms (row 1 = top in blender)
img.pixels.foreach_set(a.ravel())
img.filepath_raw = os.path.join(OUT, "png_test.png"); img.file_format = "PNG"; img.save()
