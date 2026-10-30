# HubGrime - 2D check sheets (system Python, numpy + PIL).
#   python gen\make_sheets.py
# sheets\overview_floor.png / overview_wall.png : every decal at the same stud scale (24 px/stud) over green, blue,
#                                                 cream and orange studded swatches (linear-light compositing)
# sheets\swatch_<name>.png                      : 1:1 pixels over the four colours (2x2)
# sheets\thumbs.png                             : 1/8-size thumbnails (the shape-read test)
# sheets\fringe_floor.png / fringe_wall.png     : naive straight-alpha mips (as a GPU builds them) over black /
#                                                 white / magenta + a 2x2 WRAPPED tile (Roblox Texture/Decal wrap)
# sheets\mossbase_seams.png (+ _crops)          : EndL|A|A|B|B|A|B|EndR chain on a blue studded wall, seam ticks
# checks.json["mossbase_seams"]                 : numeric seam test for every pairing
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grime_lib import HERE, DECALS, lin, to_srgb  # noqa: E402
from make_decals import ALL, SPECS  # noqa: E402
from quickview import BG, stud_surface  # noqa: E402

OUT = os.path.join(HERE, "sheets")
FLOOR = [n for n in ALL if n.startswith("G_")]
WALL = [n for n in ALL if n.startswith("W_")]


def load(name):
    im = np.asarray(Image.open(os.path.join(DECALS, name + ".png"))).astype(np.float32) / 255.0
    return im


def resize(im, w, h):
    """Straight-alpha aware resize (premultiply -> resize -> unpremultiply) for display only."""
    a = im[..., 3:4]
    pm = np.concatenate([im[..., :3] * a, a], -1)
    out = np.asarray(Image.fromarray((pm * 255).astype(np.uint8), "RGBA").resize((w, h), Image.LANCZOS)) / 255.0
    a2 = out[..., 3:4]
    rgb = np.where(a2 > 1e-4, out[..., :3] / np.maximum(a2, 1e-4), 0)
    return np.concatenate([np.clip(rgb, 0, 1), a2], -1).astype(np.float32)


def over_lin(dst, im, x, y):
    h, w = im.shape[:2]
    H, W = dst.shape[:2]
    y0, x0, y1, x1 = max(0, y), max(0, x), min(H, y + h), min(W, x + w)
    if y1 <= y0 or x1 <= x0:
        return
    src = im[y0 - y:y1 - y, x0 - x:x1 - x]
    rgb = lin(src[..., :3] * 255.0)
    a = src[..., 3:4]
    dst[y0:y1, x0:x1] = rgb * a + dst[y0:y1, x0:x1] * (1 - a)


def save_lin(img, path, labels=()):
    im = Image.fromarray(np.round(to_srgb(img) * 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    for (x, y, t) in labels:
        d.text((x + 1, y + 1), t, fill=(0, 0, 0))
        d.text((x, y), t, fill=(255, 255, 255))
    im.save(path)
    return path


def overview(names, path, pps=24, bgs=("green", "blue", "cream", "orange")):
    pad = 16
    sizes = [(int(round(SPECS[n]["studs"][0] * pps)), int(round(SPECS[n]["studs"][1] * pps))) for n in names]
    W = sum(w for w, h in sizes) + pad * (len(names) + 1)
    rowh = max(h for w, h in sizes) + pad * 2 + 12
    img = np.zeros((rowh * len(bgs), W, 3), np.float32)
    labels = []
    for r, b in enumerate(bgs):
        img[r * rowh:(r + 1) * rowh] = stud_surface(W, rowh, pps, BG[b])
        x = pad
        for n, (w, h) in zip(names, sizes):
            over_lin(img, resize(load(n), w, h), x, r * rowh + pad + 12)
            if r == 0:
                labels.append((x, 2, n))
            x += w + pad
        labels.append((W - 60, r * rowh + 2, b))
    return save_lin(img, path, labels)


def swatch_1to1(name):
    im = load(name)
    h, w = im.shape[:2]
    pad = 12
    pps = SPECS[name]["px"][0] / SPECS[name]["studs"][0]
    img = np.zeros((2 * (h + 2 * pad), 2 * (w + 2 * pad), 3), np.float32)
    for k, b in enumerate(("green", "blue", "cream", "orange")):
        r, c = divmod(k, 2)
        y, x = r * (h + 2 * pad), c * (w + 2 * pad)
        img[y:y + h + 2 * pad, x:x + w + 2 * pad] = stud_surface(w + 2 * pad, h + 2 * pad, pps, BG[b])
        over_lin(img, im, x + pad, y + pad)
    return save_lin(img, os.path.join(OUT, f"swatch_{name}.png"), [(4, 2, name + " 1:1")])


def thumbs(path):
    pad = 10
    ims = [load(n) for n in ALL]
    th = [resize(im, max(1, im.shape[1] // 8), max(1, im.shape[0] // 8)) for im in ims]
    W = sum(t.shape[1] for t in th) + pad * (len(th) + 1)
    H = max(t.shape[0] for t in th) + 2 * pad
    img = np.zeros((2 * H, W, 3), np.float32)
    for r, b in enumerate(("green", "blue")):
        img[r * H:(r + 1) * H] = stud_surface(W, H, 9.1, BG[b])
        x = pad
        for t in th:
            over_lin(img, t, x, r * H + pad)
            x += t.shape[1] + pad
    return save_lin(img, path)


def crack_gate(path):
    """REVIEW MUST 1 gate: W_Crack_C next to W_Crack_A at 1/8 and 1/4 size over the blue and cream walls."""
    pad = 14
    rows = []
    for k in (8, 4):
        th = [resize(load(n), max(1, load(n).shape[1] // k), max(1, load(n).shape[0] // k))
              for n in ("W_Crack_A", "W_Crack_C")]
        rows.append(th)
    W = max(sum(t.shape[1] for t in th) + pad * 3 for th in rows)
    hs = [max(t.shape[0] for t in th) + 2 * pad for th in rows]
    img = np.zeros((2 * sum(hs), W * 1, 3), np.float32)
    y = 0
    for b in ("blue", "cream"):
        for th, h in zip(rows, hs):
            img[y:y + h] = stud_surface(W, h, 9.1 * (1 if h == hs[0] else 2), BG[b])
            x = pad
            for t in th:
                over_lin(img, t, x, y + pad)
                x += t.shape[1] + pad
            y += h
    return save_lin(img, path)


def naive_mip(im, k):
    f = 2 ** k
    H, W = im.shape[:2]
    Hc, Wc = (H // f) * f, (W // f) * f
    return im[:Hc, :Wc].reshape(Hc // f, f, Wc // f, f, 4).mean((1, 3))


def comp_flat(im, col):
    b = np.array(col, np.float32) / 255.0
    return im[..., :3] * im[..., 3:4] + b * (1 - im[..., 3:4])


def fringe(names, path, cell_h=150):
    rows = []
    for n in names:
        im = load(n)
        tiles = []
        # 2x2 wrapped tile at mip 1 over magenta: any content touching an edge shows as a line across the middle
        t2 = np.tile(im, (2, 2, 1))
        tiles.append(comp_flat(naive_mip(t2, 1), (255, 0, 255)))
        for col in ((0, 0, 0), (255, 255, 255), (255, 0, 255)):
            for k in (1, 2, 3):
                tiles.append(comp_flat(naive_mip(im, k), col))
        out = []
        for t in tiles:
            h, w = t.shape[:2]
            s = cell_h / h
            pil = Image.fromarray(np.round(np.clip(t, 0, 1) * 255).astype(np.uint8)).resize(
                (max(1, int(w * s)), cell_h), Image.NEAREST)
            out.append(np.asarray(pil))
            out.append(np.full((cell_h, 6, 3), 40, np.uint8))
        row = np.concatenate(out, 1)
        lab = np.full((16, row.shape[1], 3), 30, np.uint8)
        rows.append(np.concatenate([lab, row], 0))
    W = max(r.shape[1] for r in rows)
    rows = [np.pad(r, ((0, 6), (0, W - r.shape[1]), (0, 0)), constant_values=30) for r in rows]
    sheet = Image.fromarray(np.concatenate(rows, 0))
    d = ImageDraw.Draw(sheet)
    y = 0
    for n, r in zip(names, rows):
        d.text((4, y + 2), n + "   [2x2 WRAP tile, mip1, magenta] | black mip1-3 | white mip1-3 | magenta mip1-3",
               fill=(255, 255, 255))
        y += r.shape[0]
    sheet.save(path)
    return path


def seam_metrics():
    """Premultiplied RGBA. (1) band identity: the outer 48 px (1.1 studs) must be identical in A, B and the caps (up to
    dither). (2) the difference across each seam vs the difference between neighbouring columns inside the strips."""
    def pm(n):
        im = load(n)
        return np.concatenate([im[..., :3] * im[..., 3:4], im[..., 3:4]], -1)
    A, B, L, R = pm("W_MossBase_A"), pm("W_MossBase_B"), pm("W_MossBase_EndL"), pm("W_MossBase_EndR")
    k = 48
    res = {"band_px": k}
    res["band_identity_max_255"] = {
        "A_vs_B_left": round(float(np.abs(A[:, :k] - B[:, :k]).max() * 255), 2),
        "A_vs_B_right": round(float(np.abs(A[:, -k:] - B[:, -k:]).max() * 255), 2),
        "EndL_vs_A_right": round(float(np.abs(L[:, -k:] - A[:, -k:]).max() * 255), 2),
        "EndR_vs_A_left": round(float(np.abs(R[:, :k] - A[:, :k]).max() * 255), 2)}
    inner = np.concatenate([np.abs(x[:, 1:] - x[:, :-1]).max(2) for x in (A, B)], 1)
    res["inner_neighbour"] = {"mean": round(float(inner.mean()), 4), "p99": round(float(np.percentile(inner, 99)), 4),
                              "p999": round(float(np.percentile(inner, 99.9)), 4)}
    pairs = {"A|A": (A, A), "A|B": (A, B), "B|A": (B, A), "B|B": (B, B), "EndL|A": (L, A), "EndL|B": (L, B),
             "A|EndR": (A, R), "B|EndR": (B, R)}
    ok = max(res["band_identity_max_255"].values()) <= 3.0
    for name, (l, r) in pairs.items():
        d = np.abs(l[:, -1] - r[:, 0]).max(axis=1)
        res[name] = {"mean": round(float(d.mean()), 4), "max": round(float(d.max()), 4)}
        ok = ok and d.mean() <= 2 * inner.mean() and d.max() <= res["inner_neighbour"]["p999"]
    res["seamless_ok"] = bool(ok)
    return res


def seam_chain():
    order = ["W_MossBase_EndL", "W_MossBase_A", "W_MossBase_A", "W_MossBase_B", "W_MossBase_B", "W_MossBase_A",
             "W_MossBase_B", "W_MossBase_EndR"]
    ims = [load(n) for n in order]
    pps = 1024 / 24.0
    pad = 30
    W = sum(i.shape[1] for i in ims) + 2 * pad
    H = ims[0].shape[0] + 2 * pad + 20
    img = stud_surface(W, H, pps, BG["blue"])
    # floor below the contact line (the hidden band sinks into it)
    yc = pad + int(round(6.0 * pps))
    img[yc:] = stud_surface(W, H - yc, pps, BG["green"])
    x = pad
    seams = []
    for i, im in enumerate(ims):
        over_lin(img, im, x, pad)
        x += im.shape[1]
        if i < len(ims) - 1:
            seams.append(x)
    # re-draw the floor over the hidden band (it is inside the floor part in game)
    img[yc:] = stud_surface(W, H - yc, pps, BG["green"])
    labels = []
    for sx in seams:
        img[pad - 14:pad - 4, sx - 1:sx + 1] = lin(np.array([255, 230, 0], np.float32))
    full = save_lin(img, os.path.join(OUT, "mossbase_seams_full.png"))
    pil = Image.open(full)
    pil.resize((pil.width // 2, pil.height // 2), Image.LANCZOS).save(os.path.join(OUT, "mossbase_seams.png"))
    crops = []
    for sx in seams:
        crops.append(np.asarray(pil.crop((sx - 128, 0, sx + 128, pil.height))))
        crops.append(np.full((pil.height, 8, 3), 30, np.uint8))
    Image.fromarray(np.concatenate(crops, 1)).save(os.path.join(OUT, "mossbase_seams_crops_1to1.png"))
    os.remove(full)
    return seams


def hidden_bands():
    """Contact edges: content must run past the contact line into the hidden band, then a >= 4 px alpha-0 margin."""
    from make_specs import SPECS
    out = {}
    for n, sp in SPECS.items():
        if "contact" not in sp:
            continue
        a = load(n)[..., 3]
        H = a.shape[0]
        pps = sp["px"][0] / sp["studs"][0]
        edge, band = sp["contact"]
        k = int(round(band * pps))           # rows from the edge to the contact line
        if edge == "bottom":
            contact_row, band_rows, margin = a[H - k], a[H - k:H - 4], a[H - 4:]
        else:
            contact_row, band_rows, margin = a[k - 1], a[4:k], a[:4]
        cols = contact_row > 0.05
        # where content touches the contact line it must continue at full strength for >= 0.25 stud past it
        n25 = int(np.ceil(0.25 * pps))
        rows25 = band_rows[-n25:] if edge == "bottom" else band_rows[:n25]
        rows25 = a[H - k:H - k + n25] if edge == "bottom" else a[k - n25:k]
        cont = rows25[:, cols].min(axis=0) if cols.any() else np.array([1.0])
        out[n] = {"edge": edge, "hidden_band_studs": band, "band_px": int(k - 4), "margin_px": 4,
                  "margin_alpha_max": round(float(margin.max()), 4),
                  "content_cols_at_contact": int(cols.sum()),
                  "band_continuation_p10_alpha_ratio": round(float(np.percentile(cont / np.maximum(contact_row[cols], 1e-3), 10)) if cols.any() else 1.0, 3)}
        out[n]["full_strength_studs_checked"] = round(n25 / pps, 3)
        out[n]["ok"] = bool(out[n]["margin_alpha_max"] == 0 and out[n]["band_continuation_p10_alpha_ratio"] > 0.8)
    return out


def _dilate(m, r):
    """Approximate disc dilation by r px (alternating 4- and 8-neighbour steps = octagon)."""
    m = m.copy()
    for i in range(int(r)):
        n = m.copy()
        n[1:, :] |= m[:-1, :]
        n[:-1, :] |= m[1:, :]
        n[:, 1:] |= m[:, :-1]
        n[:, :-1] |= m[:, 1:]
        if i % 2:
            n[1:, 1:] |= m[:-1, :-1]
            n[1:, :-1] |= m[:-1, 1:]
            n[:-1, 1:] |= m[1:, :-1]
            n[:-1, :-1] |= m[1:, 1:]
        m = n
    return m


def floating_moss():
    """REVIEW MUST 3 metric: opaque moss blobs on the WALL decals that are not within 0.5 stud of an anchor.
    moss = alpha > 0.75 and green-lit (G >= 44); anchors = the moss mass touching the contact line (MossBase, W_Crack_C,
    drips) + the dark crack core (alpha > 0.75, G < 40). A blob of >= 3 px whose gap to every anchor is > 0.5 stud is
    'floating' (must be 0); attached satellites (separate blob, gap <= 0.5 stud) are reported for information."""
    from grime_lib import components
    from make_specs import SPECS
    out = {}
    for n in WALL:
        sp = SPECS[n]
        im = load(n)
        A, G = im[..., 3], im[..., 1] * 255
        pps = sp["px"][0] / sp["studs"][0]
        H = A.shape[0]
        moss = (A > 0.75) & (G >= 44)
        if not moss.any():
            out[n] = {"moss_blobs": 0, "floating": 0, "attached_satellites": 0, "ok": True}
            continue
        lab = components(moss)
        ids, counts = np.unique(lab[lab >= 0], return_counts=True)
        anchor = (A > 0.75) & (G < 40)
        if "contact" in sp:
            edge, band = sp["contact"]
            k = int(round((band + 0.1) * pps))
            rows = slice(H - k, H) if edge == "bottom" else slice(0, k)
            touching = np.unique(lab[rows][lab[rows] >= 0])
            anchor |= np.isin(lab, touching)
        reach = _dilate(anchor, round(0.5 * pps))
        floating, sats, worst = [], 0, 0.0
        anchored = set(np.unique(lab[anchor & (lab >= 0)]).tolist())
        for i, c in zip(ids.tolist(), counts.tolist()):
            if c < 3 or i in anchored:
                continue
            blob = lab == i
            if (blob & reach).any():
                sats += 1
            else:
                ys, xs = np.nonzero(blob)
                floating.append({"x_studs": round(float(xs.mean()) / pps, 2), "y_studs": round(float(ys.mean()) / pps, 2),
                                 "px": c})
        out[n] = {"moss_blobs": int(len(ids)), "anchored": len(anchored), "attached_satellites": sats,
                  "floating": len(floating), "floating_list": floating[:10], "ok": len(floating) == 0}
    return out


def order_pairs(path):
    """Every overlap pair rendered in BOTH draw orders (Roblox sorts transparent parts per part), side by side."""
    R = os.path.join(HERE, "renders")
    pairs = [("order_floor_moss_over_stain", "order_floor_stain_over_moss"),
             ("order_floor_crack_over_stain", "order_floor_stain_over_crack"),
             ("order_wall_moss_over_crack", "order_wall_crack_over_moss"),
             ("order_wallfoot_moss_over_stain", "order_wallfoot_stain_over_moss")]
    w, h = 900, 506
    sheet = Image.new("RGB", (2 * w + 30, len(pairs) * (h + 34) + 10), (28, 28, 28))
    d = ImageDraw.Draw(sheet)
    for r, pair in enumerate(pairs):
        for c, n in enumerate(pair):
            f = os.path.join(R, n + ".png")
            if not os.path.exists(f):
                continue
            x, y = 10 + c * (w + 10), 10 + r * (h + 34)
            sheet.paste(Image.open(f).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + 22))
            d.text((x, y + 4), n, fill=(240, 240, 240))
    sheet.save(path)


def ingame_compare(path):
    """Round 4: the owner's LIVE-GAME screenshots of the round-3 test patch next to the re-calibrated mock - first with
    the very same round-3 decals (does the mock now match the game?), then with the round-4 decals."""
    G = os.path.join(HERE, "ingame_round3")
    R = os.path.join(HERE, "renders")
    rows = [("day, third person", "tp_after_day_MossBaseA.jpg", "calibcheck_r3_game_tp_day.png", "game_tp_day.png"),
            ("day, close", "close_after_day_MossBaseA.jpg", "calibcheck_r3_game_close_day.png", "game_close_day.png"),
            ("Moonlit night", "tp_after_night_MossBaseB.jpg", "calibcheck_r3_game_tp_night.png", "game_tp_night.png"),
            ("day, before (no grime)", "tp_before_day.jpg", None, "game_tp_day_before.png")]
    heads = ("LIVE GAME (round-3 patch)", "MOCK, re-calibrated, SAME round-3 decals", "MOCK, CURRENT decals (round 5 + polish)")
    w, h = 640, 317
    sheet = Image.new("RGB", (3 * w + 40, 40 + len(rows) * (h + 26)), (24, 24, 24))
    d = ImageDraw.Draw(sheet)
    for c, t in enumerate(heads):
        d.text((10 + c * (w + 10), 12), t, fill=(240, 240, 240))
    for r, (label, g, m3, m4) in enumerate(rows):
        y = 40 + r * (h + 26)
        d.text((10, y), label, fill=(200, 200, 200))
        for c, (folder, f) in enumerate(((G, g), (R, m3), (R, m4))):
            if f and os.path.exists(os.path.join(folder, f)):
                sheet.paste(Image.open(os.path.join(folder, f)).convert("RGB").resize((w, h), Image.LANCZOS),
                            (10 + c * (w + 10), y + 16))
    sheet.save(path)


def moss_chroma():
    """Round 5 gate (REVIEW round 4, MUST 2): median HSV saturation of the wall moss in the live-game framing
    (game_tp_day / game_tp_night), measured on the green pixels of the wall-foot band (rows of the wall from the floor
    line up to 5 studs, where the shaded wall is blue, so every green pixel there is moss), next to the slime drip
    (W_Drip_B, top-left of the same frame). Gate: moss <= 0.68 day / <= 0.75 night, slime the most saturated green."""
    R = os.path.join(HERE, "renders")
    out = {}
    for tag in ("day", "night"):
        f = os.path.join(R, f"game_tp_{tag}.png")
        if not os.path.exists(f):
            continue
        im = np.asarray(Image.open(f).convert("RGB")).astype(np.float32) / 255.0
        mx, mn = im.max(-1), im.min(-1)
        sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
        r, g, b = im[..., 0], im[..., 1], im[..., 2]
        hue = (np.degrees(np.arctan2(np.sqrt(3) * (g - b), 2 * r - g - b)) + 360) % 360
        green = (hue > 60) & (hue < 160) & (sat > 0.2) & (mx > 0.15)
        H = im.shape[0]
        band = np.zeros_like(green)
        band[int(H * 332 / 752):int(H * 424 / 752), :] = True     # wall rows 0-5 studs above the floor (camera maths)
        moss = green & band
        top = np.zeros_like(green)
        top[:int(H * 0.3), :int(im.shape[1] * 0.25)] = True       # the slime drip (side section, top-left)
        slime = green & top & (sat > 0.45)
        out[tag] = {"moss_px": int(moss.sum()), "moss_median_sat": round(float(np.median(sat[moss])), 3),
                    "moss_mean_rgb": [int(v) for v in (im[moss].mean(0) * 255)],
                    "moss_median_value": round(float(np.median(mx[moss])), 3),
                    "slime_px": int(slime.sum()),
                    "slime_median_sat": round(float(np.median(sat[slime])), 3) if slime.any() else None}
        lim = 0.68 if tag == "day" else 0.75
        out[tag]["ok"] = bool(out[tag]["moss_median_sat"] <= lim and
                              (out[tag]["slime_median_sat"] or 0) > out[tag]["moss_median_sat"])
    return out


def moss_gate():
    """Review item 4: our moss (6-stud close-ups + 25-stud crops) next to the Graveyard moss reference."""
    R = os.path.join(HERE, "renders")
    ref = Image.open(os.path.join(os.path.dirname(HERE), "Graveyard", "review_close_Grave_A.png")).convert("RGB")
    tiles = [("Graveyard moss (reference, close)", ref.crop((500, 300, 1050, 620))),
             ("Graveyard moss at the grave base", ref.crop((420, 800, 1160, 1000)))]
    for title, f, box in (("G_Moss_A, 6 studs (eye height 5)", "moss_close6_floor.png", (360, 300, 1560, 900)),
                          ("W_MossBase_A, 6 studs", "moss_close6_wall.png", (200, 380, 1720, 1000)),
                          ("floor moss, 25 studs (true pixels)", "floor_eye25_day.png", (400, 470, 1150, 620)),
                          ("wall moss, 25 studs (true pixels)", "wall_eye25_day.png", (330, 600, 1100, 770))):
        p = os.path.join(R, f)
        if os.path.exists(p):
            tiles.append((title, Image.open(p).convert("RGB").crop(box)))
    W, h = 900, 420
    sheet = Image.new("RGB", (2 * W + 30, ((len(tiles) + 1) // 2) * (h + 40) + 10), (28, 28, 28))
    d = ImageDraw.Draw(sheet)
    for i, (title, im) in enumerate(tiles):
        r, c = divmod(i, 2)
        s = min(W / im.width, h / im.height)
        im2 = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
        x, y = 10 + c * (W + 10), 10 + r * (h + 40)
        sheet.paste(im2, (x, y + 22))
        d.text((x, y + 4), title, fill=(240, 240, 240))
    sheet.save(os.path.join(OUT, "moss_gate.png"))


def main():
    os.makedirs(OUT, exist_ok=True)
    overview(FLOOR, os.path.join(OUT, "overview_floor.png"))
    overview(WALL, os.path.join(OUT, "overview_wall.png"))
    for n in ALL:
        swatch_1to1(n)
    thumbs(os.path.join(OUT, "thumbs.png"))
    crack_gate(os.path.join(OUT, "gate_W_Crack_C_vs_A.png"))
    fringe(FLOOR, os.path.join(OUT, "fringe_floor.png"))
    fringe(WALL, os.path.join(OUT, "fringe_wall.png"))
    seam_chain()
    cpath = os.path.join(HERE, "checks.json")
    checks = json.load(open(cpath)) if os.path.exists(cpath) else {}
    checks["mossbase_seams"] = seam_metrics()
    checks["hidden_bands"] = hidden_bands()
    checks["floating_moss"] = floating_moss()
    checks["moss_chroma"] = moss_chroma()
    moss_gate()
    order_pairs(os.path.join(OUT, "order_pairs.png"))
    ingame_compare(os.path.join(OUT, "ingame_vs_mock.png"))
    json.dump(checks, open(cpath, "w"), indent=1)
    print(json.dumps(checks["mossbase_seams"], indent=1))
    print(json.dumps({k: (v["floating"], v["attached_satellites"]) for k, v in checks["floating_moss"].items()}))


if __name__ == "__main__":
    main()
