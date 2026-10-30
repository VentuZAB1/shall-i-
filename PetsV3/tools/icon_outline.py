import sys
from PIL import Image, ImageFilter, ImageChops
src, dst, size = sys.argv[1], sys.argv[2], int(sys.argv[3])
im = Image.open(src).convert("RGBA")
a = im.getchannel("A")
bbox = a.point(lambda v: 255 if v > 8 else 0).getbbox()
im = im.crop(bbox)
w, h = im.size
side = int(max(w, h) * 1.14)  # room for the outline
canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
canvas.paste(im, ((side - w) // 2, (side - h) // 2), im)
alpha = canvas.getchannel("A").point(lambda v: 255 if v > 40 else 0)
r = max(3, side // 55)
grown = alpha.filter(ImageFilter.MaxFilter(r * 2 + 1)).filter(ImageFilter.GaussianBlur(1.2))
outline = Image.new("RGBA", canvas.size, (20, 26, 32, 255))
outline.putalpha(grown)
out = Image.alpha_composite(outline, canvas)
out = out.resize((size, size), Image.LANCZOS)
out.save(dst)
print("saved", dst, out.size, "outline px", r)
