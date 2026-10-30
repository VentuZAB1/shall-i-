"""Fix round M1/M4: average render colour of named crops (1x1 LANCZOS, the VISUAL_REVIEW method).
Usage: python measure.py R08 <shot.jpg>  |  python measure.py R03 <shot.jpg>  |  python measure.py R06 <shot.jpg>"""
import colorsys
import sys

from PIL import Image

CROPS = {
    "R08": {"panel": (400, 500, 600, 650), "pillar": (200, 300, 300, 600), "coping": (400, 125, 1100, 165)},
    "R03": {"panel": (700, 330, 800, 400), "pillar": (815, 320, 830, 390)},
    "R06": {"slotbed": (100, 520, 500, 600)},
}

cam, path = sys.argv[1], sys.argv[2]
im = Image.open(path).convert("RGB")
for name, box in CROPS[cam].items():
    c = im.crop(box).resize((1, 1), Image.LANCZOS).getpixel((0, 0))
    h, l, s = colorsys.rgb_to_hls(*[x / 255 for x in c])
    print(f"{cam} {name:7s} {c}  H{h * 360:.0f} S{s:.2f} L{l:.2f}")
