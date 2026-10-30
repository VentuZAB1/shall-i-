# samples plain-surface colours in the calibration renders (system Python)
import sys
import numpy as np
from PIL import Image
base = sys.argv[1] if len(sys.argv) > 1 else "renders"
for f in ("calib_floor_day", "calib_floor_night", "calib_wall_day", "calib_wall_night"):
    try:
        im = np.asarray(Image.open(f"{base}/{f}.png").convert("RGB")).astype(int)
    except Exception as e:
        print(f, e)
        continue
    H, W = im.shape[:2]
    def s(x, y):
        return tuple(int(v) for v in im[int(y * H) - 4:int(y * H) + 4, int(x * W) - 4:int(x * W) + 4].reshape(-1, 3).mean(0))
    if "floor" in f:
        print(f, "green near", s(0.3, 0.9), "cream near", s(0.86, 0.78), "green far", s(0.3, 0.6), "sky", s(0.5, 0.1))
    else:
        print(f, "wall", s(0.3, 0.5), "wall low", s(0.3, 0.7), "floor", s(0.3, 0.95), "trim", s(0.5, 0.07))
