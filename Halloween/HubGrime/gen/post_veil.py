# HubGrime - Roblox-like atmospheric veil (uniform, conservative: it lowers decal contrast) applied to the renders.
#   python gen\post_veil.py renders\*.png   (files whose name contains "_day" or "calib_floor_day"/"calib_wall_day" get
#   the day veil, "_night" the night veil; the ortho scale view and wip files are left alone)
import glob
import sys

import numpy as np
from PIL import Image

DAY = ((228, 234, 250), 0.06)   # round 4: lighter (the live game reads more saturated)
NIGHT = ((120, 130, 190), 0.06)
NIGHT_SAT = 1.35  # the Moonlit preset has ColorCorrection Saturation +0.25


def veil(path):
    if "ortho" in path:
        return
    v = DAY if "day" in path else NIGHT if ("night" in path or "lamp" in path) else None
    if v is None or "order_" in path and "day" not in path:
        v = DAY
    im = np.asarray(Image.open(path).convert("RGB")).astype(np.float32)
    if v is NIGHT:
        m = im.mean(-1, keepdims=True)
        im = np.clip(m + (im - m) * NIGHT_SAT, 0, 255)
    col, k = np.array(v[0], np.float32), v[1]
    out = im * (1 - k) + col * k
    Image.fromarray(np.clip(np.round(out), 0, 255).astype(np.uint8)).save(path)


if __name__ == "__main__":
    for pat in sys.argv[1:]:
        for f in glob.glob(pat):
            veil(f)
            print("veiled", f)
