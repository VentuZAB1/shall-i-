"""Decode HubV2Kit.Render chunks (saved MCP tool outputs) into PNG files.

Usage:  python decode_render.py OUT_DIR file1.txt [file2.txt ...]
Each file holds one chunk: "HUBSHOT <name> <W> <H> <fromRow> <toRow>" + rows of RLE runs + "ENDSHOT".
A run = 3 chars colour (RGB555, base 32 over the B64 alphabet) + 1 char (run length - 1). Chunks of the same shot are
merged; a PNG is written once every row of a shot is present (name.png).
"""
import os
import sys
from PIL import Image

B64 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"
IDX = {c: i for i, c in enumerate(B64)}


def decode_row(s, w):
    px = []
    for i in range(0, len(s) - 3, 4):
        r, g, b, n = (IDX[s[i]], IDX[s[i + 1]], IDX[s[i + 2]], IDX[s[i + 3]] + 1)
        px.extend([(r * 255 // 31, g * 255 // 31, b * 255 // 31)] * n)
    if len(px) != w:
        raise ValueError(f"row has {len(px)} px, want {w}")
    return px


def main():
    out_dir = sys.argv[1]
    os.makedirs(out_dir, exist_ok=True)
    shots = {}
    for path in sys.argv[2:]:
        text = open(path, encoding="utf-8", errors="replace").read()
        pos = 0
        found = False
        while True:
            start = text.find("HUBSHOT ", pos)
            if start < 0:
                break
            found = True
            lines = text[start:].split("\n")
            _, name, w, h, a, b = lines[0].split()
            w, h, a, b = int(w), int(h), int(a), int(b)
            s = shots.setdefault(name, {"w": w, "h": h, "rows": {}})
            for k, y in enumerate(range(a, b + 1)):
                s["rows"][y] = decode_row(lines[1 + k], w)
            pos = start + 8
        if not found:
            print("no HUBSHOT in", path)
    for name, s in shots.items():
        if len(s["rows"]) != s["h"]:
            print(f"{name}: {len(s['rows'])}/{s['h']} rows - incomplete")
            continue
        img = Image.new("RGB", (s["w"], s["h"]))
        img.putdata([p for y in range(1, s["h"] + 1) for p in s["rows"][y]])
        p = os.path.join(out_dir, name + ".png")
        img.save(p)
        print("wrote", p)


if __name__ == "__main__":
    main()
