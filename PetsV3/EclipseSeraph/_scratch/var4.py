# builder D scratch: Seraph round-4 chroma variants -> raw / icon / strip-cell stats (edits pets/EclipseSeraph.py,
# restores after). python EclipseSeraph/_scratch/var4.py '{"lab": ["key", ...], ...}'
NL = chr(10)
import subprocess, json, sys, os, colorsys
from PIL import Image
ROOT = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3"
P = os.path.join(ROOT, "pets", "EclipseSeraph.py")
SCR = os.path.join(ROOT, "EclipseSeraph", "_scratch")
BL = r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
orig = open(P, encoding="utf-8").read()
R = {
    "base": [],
    "obs1": [("OBSID = (34, 34, 56)", "OBSID = (28, 28, 60)")],
    "obs2": [("OBSID = (34, 34, 56)", "OBSID = (26, 26, 66)")],
    "ivo": [("MOON_IVORY = (232, 208, 240)", "MOON_IVORY = (230, 196, 244)")],
    "cor12": [("arc(cor_o - 0.10, lo)), (arc(cor_o, hi), arc(cor_o - 0.10, hi))",
               "arc(cor_o - 0.12, lo)), (arc(cor_o, hi), arc(cor_o - 0.12, hi))")],
    "wing": [("WING_LILAC = (206, 130, 240)", "WING_LILAC = (204, 120, 242)")],
}


def stats(im, mask):
    px = [p[:3] for p in im.getdata() if mask(p)]
    S = [colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)[1] for r, g, b in px]
    L = [0.299 * r + 0.587 * g + 0.114 * b for r, g, b in px]
    t = len(px)
    return "sat %.3f sh %.0f%% wh %.1f%% dk %.1f%%" % (sum(S) / t, 100.0 * sum(s > 0.35 for s in S) / t,
                                                     100.0 * sum(l > 200 for l in L) / t,
                                                     100.0 * sum(l < 90 for l in L) / t)


VARS = json.loads(sys.argv[1])
try:
    for lab, keys in VARS.items():
        s = orig
        for key in keys:
            for a, b in R[key]:
                assert s.count(a) == 1, a
                s = s.replace(a, b)
        open(P, "w", encoding="utf-8", newline=NL).write(s)
        subprocess.run([BL, "-b", "--factory-startup", "--python", os.path.join(ROOT, "_tools", "headless_pack.py"), "--",
                        "EclipseSeraph"], capture_output=True, cwd=ROOT)
        subprocess.run([sys.executable, os.path.join(ROOT, "_tools", "pack_post.py"), "EclipseSeraph",
                        "SolarLion,Griffin,CelestialDragon,Cvetibara,CosmicLeviathan"], capture_output=True, cwd=ROOT)
        raw = Image.open(os.path.join(ROOT, "EclipseSeraph", "EclipseSeraph_portrait_raw.png")).convert("RGBA")
        raw = raw.crop(raw.split()[3].point(lambda v: 255 if v > 8 else 0).getbbox())
        w, h = raw.size
        k = 64 / max(w, h)
        raw = raw.resize((max(1, int(w * k)), max(1, int(h * k))), Image.LANCZOS)
        ic = Image.open(os.path.join(ROOT, "EclipseSeraph", "EclipseSeraph_icon.png")).convert("RGBA").resize(
            (64, 64), Image.LANCZOS)
        st = Image.open(os.path.join(ROOT, "EclipseSeraph", "renders", "_icons_strip_64.png")).convert("RGB")
        cell = st.crop((6, 6, 70, 70))
        print(lab, "| raw", stats(raw, lambda p: p[3] > 200), "| icon", stats(ic, lambda p: p[3] > 200), "| cell",
              stats(cell, lambda p: abs(p[0] - 52) + abs(p[1] - 62) + abs(p[2] - 74) > 12), flush=True)
finally:
    open(P, "w", encoding="utf-8", newline=NL).write(orig)
