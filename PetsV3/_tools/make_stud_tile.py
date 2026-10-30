# Seamless Roblox-stud tile (2026-10-09, owner refs: Spideron / Bronto / Orca are fully covered in small studs).
# Grey multiplier map (Non-Color): 0.6667 = x1.0 (gain 1.5 in the shader). Stud: light top + top-left rim highlight,
# dark lower-right rim + a soft drop shadow, so every surface reads like Roblox plastic studs.
# python _tools/make_stud_tile.py  ->  PetsV3/_tools/stud_tile.png
import os
from PIL import Image, ImageFilter
import numpy as np

S = 256                      # supersampled, saved at 64
N = 64
c = S / 2
y, x = np.mgrid[0:S, 0:S].astype(np.float32) + 0.5
base = 0.5                   # x gain 2.0 = 1.0
R = 0.30 * S                 # stud radius
v = np.full((S, S), base, np.float32)
# soft drop shadow down-right
dx, dy = x - (c + 0.05 * S), y - (c + 0.06 * S)
d_sh = np.sqrt(dx * dx + dy * dy)
sh = np.clip((R * 1.10 - d_sh) / (0.08 * S), 0, 1)
v *= 1.0 - 0.34 * sh
# stud disk
d = np.sqrt((x - c) ** 2 + (y - c) ** 2)
inside = d < R
ang = np.arctan2(-(y - c), x - c)            # 0 = right, +90 = up (image y grows down)
lightdir = np.radians(135)                   # top-left
facing = np.cos(ang - lightdir)              # +1 top-left rim, -1 bottom-right rim
rim = np.clip((d - R * 0.72) / (R * 0.28), 0, 1)
top = base * 1.12
stud = top + rim * np.where(facing > 0, facing * 0.55 * base, facing * 0.42 * base)
edge = np.clip((d - R * 0.93) / (R * 0.07), 0, 1)            # thin dark outline at the very edge
stud = stud * (1 - 0.38 * edge)
v = np.where(inside, stud, v)
v = np.clip(v, 0, 1)
# G channel = ADDITIVE light (top-left rim + a soft cap): makes studs read on dark colours in Roblox's lighting
add = np.zeros((S, S), np.float32)
add = np.where(inside, 0.18 + rim * np.clip(facing, 0, 1) * 0.82, 0.0)
add *= 1 - edge
add = np.clip(add, 0, 1)
def small(a):
    return np.array(Image.fromarray((a * 255).astype(np.uint8), "L").filter(ImageFilter.GaussianBlur(1.2)).resize((N, N), Image.LANCZOS))
R, G = small(v), small(add)
im = Image.fromarray(np.stack([R, G, R], -1), "RGB")
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stud_tile.png")
im.save(out)
print(out, im.size, R.min(), R.max(), G.min(), G.max())
