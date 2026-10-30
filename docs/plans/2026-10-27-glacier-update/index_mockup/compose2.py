"""v6+ compose: paste portraits into the card slots, then restore the label rows (name + pill) from the raw capture,
because in game the labels draw above the portrait. Usage: python compose2.py raw.jpg out.png "<rects>" "<stage>" <InspectPet>"""
import sys, ast
import compose
from PIL import Image

def run(raw_path, out_path, rects, stage, inspect_name, sel_index=None):
    raw = Image.open(raw_path).convert("RGBA")
    base = raw.copy()
    for n, r in zip(compose.NAMES, rects):
        compose.paste_fit(base, compose.portrait(n), r, 1.0)
    for (x, y, w, h) in rects:
        W, H = w / 0.8, h / 0.68
        x0, y0 = x - 0.1 * W, y - 0.22 * H
        for (fx, fy, fw, fh) in ((0.20, 0.82, 0.60, 0.16), (0.04, 0.10, 0.92, 0.12)):
            box = (int(x0 + fx * W), int(y0 + fy * H), int(x0 + (fx + fw) * W), int(y0 + (fy + fh) * H))
            base.paste(raw.crop(box), box[:2])
    compose.paste_fit(base, compose.portrait(inspect_name), stage, 0.92)
    base.convert("RGB").save(out_path)
    return base

if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2], ast.literal_eval(sys.argv[3]), ast.literal_eval(sys.argv[4]), sys.argv[5])
