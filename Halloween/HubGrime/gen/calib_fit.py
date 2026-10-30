# HubGrime round 4 - fit the mock lighting + wall/pillar albedo to the LIVE GAME screenshots (ingame_round3\).
#   python gen\calib_fit.py            -> writes gen\calib_round4.json (read by mock_preview.py) + logs\calib_fit.txt
# Targets = median colours sampled from the owner's screenshots of the round-3 test patch (no decals at the samples):
#   day  (tp_before_day.jpg): shaded back wall, shaded floor at the wall foot, sunlit floor, pillar front
#   night (tp_after_night_MossBaseB.jpg, Moonlit): the same three surfaces
# The game has the sun BEHIND the back wall, so the wall face and the floor at its foot only get sky light.
# Per channel, in linear light (veil and the night saturation boost inverted): sky colour <- floor shade, sun colour
# <- sunlit minus shaded floor, wall/pillar albedo <- their shade values. A few multiplicative iterations converge.
import json
import os
import subprocess
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import post_veil  # noqa: E402

BLENDER = r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
OUTJ = os.path.join(HERE, "gen", "calib_round4.json")
TRIAL = os.path.join(HERE, "logs", "calib_trial.json")
R = os.path.join(HERE, "renders")

TARGETS = {
    "day": {"wall": (55, 114, 181), "floor_shade": (61, 130, 108), "floor_sun": (186, 227, 168), "pillar": (26, 68, 143)},
    "night": {"wall": (28, 76, 178), "floor_shade": (55, 113, 72), "floor_sun": (100, 165, 99), "pillar": (10, 41, 134)},
}
START = {
    "day": {"sun": 4.5, "sun_col": [1.0, 0.95, 0.86], "sun_dir": [0.25, 0.42, 0.87], "sky": [0.3, 0.55, 1.0],
            "sky_str": 1.2, "sky_display": [0.45, 0.62, 0.85], "exposure": 0.0, "vt": "Khronos PBR Neutral"},
    "night": {"sun": 1.6, "sun_col": [0.7, 0.8, 1.0], "sun_dir": [0.25, 0.42, 0.87], "sky": [0.2, 0.4, 0.8],
              "sky_str": 0.9, "sky_display": [0.012, 0.02, 0.07], "stars": True, "exposure": 0.0,
              "vt": "Khronos PBR Neutral"},
    "albedo": {"green": [128, 170, 96], "blue": [96, 132, 170], "pillar": [69, 95, 132]},
}


def s2l(c):
    c = np.clip(np.asarray(c, float) / 255.0, 0, 1)
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def l2s(c):
    c = np.clip(np.asarray(c, float), 0, 1)
    return 255 * np.where(c <= 0.0031308, c * 12.92, 1.055 * c ** (1 / 2.4) - 0.055)


def unveil(rgb, night):
    col, k = post_veil.NIGHT if night else post_veil.DAY
    x = (np.asarray(rgb, float) - k * np.asarray(col, float)) / (1 - k)
    if night:                                   # undo the Moonlit saturation boost (mean is preserved)
        m = x.mean()
        x = m + (x - m) / post_veil.NIGHT_SAT
    return s2l(x)


def measure(name):
    im = np.asarray(Image.open(os.path.join(R, name + ".png")).convert("RGB")).astype(float)
    pix = json.load(open(os.path.join(R, name + "_samples.json")))
    out = {}
    for k, (x, y) in pix.items():
        x, y = int(round(x)), int(round(y))
        patch = im[max(0, y - 10):y + 11, max(0, x - 10):x + 11].reshape(-1, 3)
        out[k] = np.median(patch, 0)
    return {"wall": (out["wall"] + out["wall2"]) / 2, "floor_shade": (out["floor_shade"] + out["floor_shade2"]) / 2,
            "floor_sun": (out["floor_sun"] + out["floor_sun2"]) / 2, "pillar": out["pillar"]}


def band_moss(im):
    """Median RGB of the wall moss in the live-game framing: green pixels in the wall rows 0-5 studs above the floor
    (the shaded wall is blue there, so green = moss). Same mask as make_sheets.moss_chroma."""
    im = np.asarray(im, float) / 255.0
    mx, mn = im.max(-1), im.min(-1)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
    r, g, b = im[..., 0], im[..., 1], im[..., 2]
    hue = (np.degrees(np.arctan2(np.sqrt(3) * (g - b), 2 * r - g - b)) + 360) % 360
    H = im.shape[0]
    m = (hue > 60) & (hue < 160) & (sat > 0.2) & (mx > 0.15)
    m[:int(H * 332 / 752)] = False
    m[int(H * 424 / 752):] = False
    return np.median(im[m], 0) * 255


GAME = os.path.join(HERE, "ingame_round3")
TARGETS["day"]["moss"] = tuple(band_moss(Image.open(os.path.join(GAME, "tp_after_day_MossBaseA.jpg")).convert("RGB")
                                         .resize((1520, 752))))
TARGETS["night"]["moss"] = tuple(band_moss(Image.open(os.path.join(GAME, "tp_after_night_MossBaseB.jpg"))
                                           .convert("RGB").resize((1520, 752))))
R3 = os.path.join(HERE, "decals_round3")


def render(cal):
    json.dump(cal, open(TRIAL, "w"), indent=1)
    for f in ("calib4_day", "calib4_night"):
        p = os.path.join(R, f + ".png")
        if os.path.exists(p):
            os.remove(p)
    log = os.path.join(HERE, "logs", "calib_fit_blender.txt")
    with open(log, "w") as fh:
        subprocess.run([BLENDER, "-b", "--factory-startup", "--python", os.path.join(HERE, "gen", "mock_preview.py"),
                        "--", "--shots", "calib4", "--cal", TRIAL, "--samples", "24", "--decals", R3], stdout=fh,
                       stderr=subprocess.STDOUT, timeout=900)
    for f in ("calib4_day", "calib4_night", "calib4m_day", "calib4m_night"):
        post_veil.veil(os.path.join(R, f + ".png"))
    md, mn = measure("calib4_day"), measure("calib4_night")
    md["moss"] = band_moss(Image.open(os.path.join(R, "calib4m_day.png")).convert("RGB"))
    mn["moss"] = band_moss(Image.open(os.path.join(R, "calib4m_night.png")).convert("RGB"))
    return md, mn


def rgb_of(cfg):
    return np.asarray(cfg["sun_col"], float) * cfg["sun"], np.asarray(cfg["sky"], float) * cfg["sky_str"]


def set_rgb(cfg, sun, sky):
    cfg["sun"] = float(max(sun.max(), 1e-3))
    cfg["sun_col"] = [round(float(v), 4) for v in sun / cfg["sun"]]
    cfg["sky_str"] = float(max(sky.max(), 1e-3))
    cfg["sky"] = [round(float(v), 4) for v in sky / cfg["sky_str"]]


def main():
    cal = json.loads(json.dumps(START))
    if os.path.exists(OUTJ) and "--fresh" not in sys.argv:
        cal = json.load(open(OUTJ))
    lines = []
    for it in range(int(sys.argv[sys.argv.index("--iters") + 1]) if "--iters" in sys.argv else 6):
        md, mn = render(cal)
        err = {}
        for tag, meas, night in (("day", md, False), ("night", mn, True)):
            T = {k: unveil(v, night) for k, v in TARGETS[tag].items()}
            M = {k: unveil(v, night) for k, v in meas.items()}
            err[tag] = {k: [int(round(a - b)) for a, b in zip(meas[k], TARGETS[tag][k])] for k in meas}
            sun, sky = rgb_of(cal[tag])
            if tag == "day":
                sky = sky * np.clip(T["floor_shade"] / np.maximum(M["floor_shade"], 1e-4), 0.4, 2.5) ** 0.85
            else:     # round 5: the night sky colour from THREE shaded materials (floor, wall, the known moss decal)
                lr = np.mean([np.log(np.clip(T[k] / np.maximum(M[k], 1e-4), 0.4, 2.5))
                              for k in ("floor_shade", "floor_shade", "wall", "moss")], axis=0)   # floor weighted x2
                sky = sky * np.exp(0.8 * lr)
            dT = np.maximum(T["floor_sun"] - T["floor_shade"], 1e-3)
            dM = np.maximum(M["floor_sun"] - M["floor_shade"], 1e-3)
            # the sun keeps a plausible warm-white (day) / cool (moon) colour: only its STRENGTH is fitted (green
            # channel); the floor albedo's red and blue absorb the rest (day only), so sunlit decals keep true hues
            if tag == "day":
                sun = sun * float(np.clip(dT[1] / dM[1], 0.4, 2.5)) ** 0.85
            else:                                             # Moonlit: the moon colour itself is graded -> free
                sun = sun * np.clip(dT / dM, 0.4, 2.5) ** 0.85
            set_rgb(cal[tag], sun, sky)
            if tag == "day":
                g = s2l(cal["albedo"]["green"])
                r = np.clip(T["floor_sun"] / np.maximum(M["floor_sun"], 1e-4), 0.5, 2.0) ** 0.6
                g[0] *= r[0]
                g[2] *= r[2]
                cal["albedo"]["green"] = [round(float(v), 1) for v in l2s(np.clip(g, 0.002, 0.92))]
            if tag == "day":                                  # albedo is fitted on the day frame only
                for key, alb in (("wall", "blue"), ("pillar", "pillar")):
                    a = s2l(cal["albedo"][alb]) * np.clip(T[key] / np.maximum(M[key], 1e-4), 0.4, 2.5) ** 0.5
                    cal["albedo"][alb] = [round(float(v), 1) for v in l2s(np.clip(a, 0.002, 0.92))]
        line = f"iter {it}: error (render - game, sRGB) {json.dumps(err)}"
        print(line, flush=True)
        lines.append(line)
    md, mn = render(cal)
    final = {tag: {k: [int(round(a - b)) for a, b in zip(meas[k], TARGETS[tag][k])] for k in meas}
             for tag, meas in (("day", md), ("night", mn))}
    cal["fit"] = {"targets": TARGETS, "final_error_render_minus_game": final,
                  "final_render_values": {"day": {k: [int(round(v)) for v in x] for k, x in md.items()},
                                          "night": {k: [int(round(v)) for v in x] for k, x in mn.items()}}}
    json.dump(cal, open(OUTJ, "w"), indent=1)
    lines.append("final " + json.dumps(final))
    open(os.path.join(HERE, "logs", "calib_fit.txt"), "w").write("\n".join(lines) + "\n")
    print("final", json.dumps(final))


if __name__ == "__main__":
    main()
