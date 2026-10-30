# Ice Dragon v5 -> v6: the reviewer's [editor] fixes (2026-10-29).
#  1. sky only: calmer slate blue (less saturation, a bit brighter) so the navy dragon stands out
#  2. a soft contact shadow under the egg's snow base
#  3. sharpen the soft far-right ice cliffs
#  4. remove the loose ice cube lying on the snow near the dragon's foot
# Run: py polish_v6.py  (reads 1_ice_dragon_v5.png, writes 1_ice_dragon_v6.png + 250 px tile + before/after)
import numpy as np
from PIL import Image, ImageFilter, ImageDraw

SRC, DST = "1_ice_dragon_v5.png", "1_ice_dragon_v6.png"
im = Image.open(SRC).convert("RGB")
W, H = im.size
a = np.asarray(im).astype(np.float32) / 255.0


def rgb_to_hsv(x):
    r, g, b = x[..., 0], x[..., 1], x[..., 2]
    mx, mn = x.max(-1), x.min(-1)
    d = mx - mn
    h = np.zeros_like(mx)
    m = d > 1e-6
    rr = m & (mx == r)
    gg = m & (mx == g) & ~rr
    bb = m & ~rr & ~gg
    h[rr] = ((g - b)[rr] / d[rr]) % 6
    h[gg] = (b - r)[gg] / d[gg] + 2
    h[bb] = (r - g)[bb] / d[bb] + 4
    h = h * 60.0
    s = np.where(mx > 1e-6, d / np.maximum(mx, 1e-6), 0)
    return h, s, mx


def hsv_to_rgb(h, s, v):
    c = v * s
    hp = (h % 360) / 60.0
    x = c * (1 - np.abs(hp % 2 - 1))
    z = np.zeros_like(h)
    conds = [(hp < 1), (hp < 2), (hp < 3), (hp < 4), (hp < 5), (hp >= 5)]
    vals = [(c, x, z), (x, c, z), (z, c, x), (z, x, c), (x, z, c), (c, z, x)]
    r = np.select(conds, [v_[0] for v_ in vals])
    g = np.select(conds, [v_[1] for v_ in vals])
    b = np.select(conds, [v_[2] for v_ in vals])
    m = v - c
    return np.stack([r + m, g + m, b + m], -1)


def box_mean(x, k):
    # mean over a k x k window (edge padded), via cumulative sums
    p = k // 2
    xp = np.pad(x, ((p + 1, p), (p + 1, p)), mode="edge")
    c = xp.cumsum(0).cumsum(1)
    return (c[k:, k:] - c[:-k, k:] - c[k:, :-k] + c[:-k, :-k]) / (k * k)


# ---------------------------------------------------------------- 1. sky mask + grade
h, s, v = rgb_to_hsv(a)
lum = a.mean(-1)
std = np.sqrt(np.maximum(box_mean(lum * lum, 7) - box_mean(lum, 7) ** 2, 0))
yy = np.arange(H)[:, None] * np.ones((1, W))
cand = (h > 198) & (h < 215.5) & (s > 0.25) & (s < 0.75) & (v > 0.45) & (std < 0.035) & (yy < 620)  # sky is hue 211-213, the wing blues 217-224
# grow from the top rows through smooth sky only (downscaled x2 for speed), so ice crystals / wings stay out
small = cand[::2, ::2]
mask = np.zeros_like(small)
mask[:4, :] = small[:4, :]
for _ in range(2000):
    grown = mask.copy()
    grown[1:, :] |= mask[:-1, :]
    grown[:-1, :] |= mask[1:, :]
    grown[:, 1:] |= mask[:, :-1]
    grown[:, :-1] |= mask[:, 1:]
    grown &= small
    if (grown == mask).all():
        break
    mask = grown
sky = Image.fromarray((mask * 255).astype(np.uint8)).resize((W, H), Image.NEAREST)
# close tiny holes (cloud wisps)
sky = sky.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.MinFilter(5))
# the original has a glowing bright-blue rim around the spikes and wing edges: take in bright, saturated blue pixels
# up to 3 px outside the sky too (the navy body is darker, v < 0.6, so it stays out), then feather 1.5 px
near = np.asarray(sky.filter(ImageFilter.MaxFilter(7))) > 127
rim = near & (h > 195) & (h < 216) & (s > 0.3) & (s < 0.8) & (v > 0.6)
skym = (np.asarray(sky) > 127) | rim
sky = Image.fromarray((skym * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.5))
skyw = np.asarray(sky).astype(np.float32)[..., None] / 255.0

# graded sky: 38 % less saturation, 10 % brighter, hue nudged toward slate (208 deg)
h2 = h + (208 - h) * 0.5
s2 = s * 0.62
v2 = np.minimum(v * 1.10 + 0.02, 1.0)
graded = hsv_to_rgb(h2, s2, v2)
out = a * (1 - skyw) + graded * skyw

# ---------------------------------------------------------------- 2. soft contact shadow under the egg base
shadow = Image.new("L", (W, H), 0)
ImageDraw.Draw(shadow).ellipse((520, 800, 1050, 852), fill=255)
shadow = shadow.filter(ImageFilter.GaussianBlur(16))
sw = np.asarray(shadow).astype(np.float32)[..., None] / 255.0 * 0.42
tint = np.array([0.18, 0.26, 0.42], np.float32)  # cool blue-grey, not black
out = out * (1 - sw) + (out * tint) * sw

# ---------------------------------------------------------------- 4. the loose cube on the snow (x 1070-1140, y 785-845)
o8 = Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8))
patch = o8.crop((1150, 785, 1220, 845))  # plain snow just right of it
o8.paste(patch, (1072, 785))
mfeather = Image.new("L", (W, H), 0)
ImageDraw.Draw(mfeather).rectangle((1066, 780, 1148, 850), fill=255)
mfeather = mfeather.filter(ImageFilter.GaussianBlur(4))
blend = o8.filter(ImageFilter.GaussianBlur(1.2))
o8 = Image.composite(blend, o8, mfeather.point(lambda p: int(p * 0.5)))

# ---------------------------------------------------------------- 3. sharpen the far-right cliffs
box = (1470, 420, W, 800)
reg = o8.crop(box).filter(ImageFilter.UnsharpMask(radius=1.6, percent=90, threshold=2))
o8.paste(reg, box[:2])

o8.save(DST)
t = o8.copy()
t.thumbnail((250, 250))
t.save("1_ice_dragon_v6_phone_tile_250px.png")
# before / after for a quick look
ba = Image.new("RGB", (W, H * 2 + 10), (255, 0, 255))
ba.paste(im, (0, 0))
ba.paste(o8, (0, H + 10))
ba.thumbnail((1100, 1300))
ba.save("_v5_vs_v6.png")
Image.fromarray((mask * 255).astype(np.uint8)).save("_sky_mask_small.png")
print("sky pixels %.1f%%" % (skyw.mean() * 100), "saved", DST)
