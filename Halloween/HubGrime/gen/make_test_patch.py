# HubGrime - writes test_patch.json: the owner TEST PATCH (one back-wall bay + the floor in front of it, plus an
# optional plaza-rim spot) as exact carrier parts (size + CFrame), in Roblox world coordinates.
#   python gen\make_test_patch.py
# Round 2 (REVIEW MUST 6 + NICE 6): the patch moved OFF Base2 into the back-wall bay between the pillars at x 39.8
# and 66.4 (Studio facts from the lead, 2026-10-14):
#   back wall inner face z = 104.00 (BackWall centre z 107, 6 thick), floor top y = 0, top trim bottom y = 22.9,
#   pillars 2.5 wide (x) x 1.6 deep (z), centred z 103.1 (they stand proud of the wall: z 104 -> 102.3),
#   pillar faces x 41.05 / 65.15 -> clear width 24.1, centre 53.1.
#   Base2 slot x -38..26 and Base3 slot x 76..140 (+4 margin each) -> this bay (x 41..65) clears both.
# Every placement is derived from the PNG alpha (content extents), and the script REFUSES to write the JSON if a wall
# pair is closer than 2 studs or the floor moss is more than 0.5 stud from the wall foot.
import json
import os
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_specs import SPECS  # noqa: E402

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DECALS = os.path.join(HERE, "decals")
WALL_Z = 104.0              # inner face of the back wall (faces -Z, toward the hub)
FLOOR_Y = 0.0
TRIM_BOTTOM_Y = 22.9
PILLAR_X = (39.8, 66.4)     # pillar centres of the bay
PILLAR_W, PILLAR_D, PILLAR_ZC = 2.5, 1.6, 103.1
FACE_R = PILLAR_X[0] + PILLAR_W / 2     # 41.05 = the RIGHT face as seen from the hub (+X is the viewer's LEFT)
FACE_L = PILLAR_X[1] - PILLAR_W / 2     # 65.15 = the LEFT face as seen from the hub
BAY_X = (FACE_L + FACE_R) / 2           # 53.1
BAY_W = FACE_L - FACE_R                 # 24.1
BASES = {"Base2": (-38.0, 26.0), "Base3": (76.0, 140.0)}
BASE_MARGIN = 4.0
T = 0.05                    # carrier thickness
MIN_WALL_GAP = 2.0          # studs between the visible content of two wall decals
MAX_FOOT_GAP = 0.5          # floor moss content must reach within this of the wall foot
A_VIS = 0.1                 # "visible content" alpha threshold

COMMON = {"Anchored": True, "CanCollide": False, "CanTouch": False, "CanQuery": False, "CastShadow": False,
          "Transparency": 1, "Material": "SmoothPlastic"}


def alpha(tex):
    return np.asarray(Image.open(os.path.join(DECALS, tex + ".png")))[..., 3].astype(np.float32) / 255.0


def margins(tex, thr=0.3):
    """Content margins (studs) from each carrier edge: left/right = image columns, top/bottom = image rows."""
    a = alpha(tex) > thr
    H, W = a.shape
    w, h = SPECS[tex]["studs"]
    cols, rows = np.nonzero(a.any(0))[0], np.nonzero(a.any(1))[0]
    return {"left": cols[0] / W * w, "right": w - (cols[-1] + 1) / W * w,
            "top": rows[0] / H * h, "bottom": h - (rows[-1] + 1) / H * h}


def wall_part(name, tex, x, y_bottom, layer, kind="Decal", extra=None, width=None):
    w, h = SPECS[tex]["studs"]
    w = width or w
    zc = WALL_Z - layer + T / 2          # the Front (decal) face sits `layer` studs in front of the wall face
    d = {"name": name, "texture": tex, "kind": kind, "face": "Front", "size": [round(w, 4), round(h, 4), T],
         "position": [round(x, 4), round(y_bottom + h / 2, 4), round(zc, 4)], "rotation_y_deg": 0,
         "layer_studs": layer, "part": COMMON}
    if extra:
        d.update(extra)
    return d


def floor_part(name, tex, x, z, yaw, layer, transparency=0.0, extra=None):
    w, h = SPECS[tex]["studs"]
    d = {"name": name, "texture": tex, "kind": "Decal", "face": "Top", "size": [w, T, h],
         "position": [round(x, 4), round(FLOOR_Y + layer - T / 2, 4), round(z, 4)], "rotation_y_deg": yaw,
         "layer_studs": layer, "decal": {"Transparency": transparency}, "part": COMMON}
    if extra:
        d.update(extra)
    return d


# ------------------------------------------------------------------ wall content in world space (for the gap check)
def wall_points(e, step=0.05):
    """World (x, y) of the VISIBLE content of a wall carrier, sampled on a step grid. Front face, identity rotation:
    u = 0 (image left) is at the viewer's LEFT = +X. Texture carriers tile with StudsPerTileU/V. Content below the
    floor (y < 0) or behind the trim (y > 22.9) is hidden and ignored."""
    a = alpha(e["texture"])
    H, W = a.shape
    w, h, _ = e["size"]
    cx, cy, _ = e["position"]
    tw, th = SPECS[e["texture"]]["studs"]
    tp = e.get("texture_props")
    us = np.arange(step / 2, w, step)                  # studs from the carrier's left edge (viewer's left)
    vs = np.arange(step / 2, h, step)                  # studs from the carrier's top edge
    U, V = np.meshgrid(us, vs)
    if tp:
        su, sv = tp["StudsPerTileU"], tp["StudsPerTileV"]
        iu = np.mod(U + tp.get("OffsetStudsU", 0), su) / su * W
        iv = np.mod(V + tp.get("OffsetStudsV", 0), sv) / sv * H
    else:
        iu, iv = U / w * W, V / h * H
    av = a[np.clip(iv.astype(int), 0, H - 1), np.clip(iu.astype(int), 0, W - 1)]
    X = cx + w / 2 - U
    Y = cy + h / 2 - V
    m = (av > A_VIS) & (Y > FLOOR_Y) & (Y < TRIM_BOTTOM_Y)
    return np.stack([X[m], Y[m]], 1)


def min_dist(p, q):
    if len(p) == 0 or len(q) == 0:
        return float("inf")
    # thin both clouds to their outlines (every 2nd point is plenty at 0.05-stud steps), then chunked brute force
    best = float("inf")
    q = q[:: max(1, len(q) // 20000)]
    for i in range(0, len(p), 2000):
        d = np.sqrt(((p[i:i + 2000, None, :] - q[None, :, :]) ** 2).sum(-1)).min()
        best = min(best, float(d))
    return best


def outline(pts, step=0.05):
    """Keep only boundary samples (a sample with a missing 4-neighbour) - same min distance, far fewer points."""
    if len(pts) == 0:
        return pts
    k = np.round(pts / step).astype(np.int64)
    s = set(map(tuple, k))
    keep = [i for i, (x, y) in enumerate(k) if not ((x + 1, y) in s and (x - 1, y) in s and (x, y + 1) in s
                                                     and (x, y - 1) in s)]
    return pts[keep]


def main():
    mg = {t: margins(t) for t in ("G_Moss_A", "G_Moss_B", "W_Crack_C", "W_Crack_B", "W_Drip_A")}
    # ---------------------------------------------------------------- wall
    crack_c_x = FACE_L - 8.5             # 8.5 studs right of the LEFT pillar face = centre of MossBase_A's low slot
    crack_b_x = FACE_R + 6.0             # 6 studs left of the RIGHT pillar face
    # drip by the LEFT pillar: its visible content starts 2 studs from the pillar face
    w_d = SPECS["W_Drip_A"]["studs"][0]
    drip_x = FACE_L - (2.0 + mg["W_Drip_A"]["left"]) - w_d / 2
    wall = [
        wall_part("MossBase_Bay", "W_MossBase_A", BAY_X, FLOOR_Y - 0.375, 0.05, kind="Texture", width=BAY_W,
                  extra={"texture_props": {"StudsPerTileU": 24, "StudsPerTileV": 6.375, "OffsetStudsU": 0,
                                           "OffsetStudsV": 0},
                         "note": "Texture: ONE carrier from pillar face to pillar face (24.1 wide; the last 0.1 stud "
                                 "repeats the seamless start of the tile). Bottom 0.375 below the floor top: the "
                                 "hidden band sinks into the floor. Both ends meet pillars, so no end caps here."}),
        wall_part("Crack_FloorUp", "W_Crack_C", crack_c_x, FLOOR_Y - 0.375, 0.04,
                  extra={"note": "LEFT pillar face - 8.5: the centre of MossBase_A's low-moss slot (6.7-10.3 studs "
                                 "from where the tile starts; u = 0 is the viewer's LEFT end). Its notch sits on the "
                                 "floor line. If the strip shows mirrored in Studio (a tall moss plume under the "
                                 "crack), mirror this x about the bay centre 53.1."}),
        wall_part("Crack_Diag", "W_Crack_B", crack_b_x, 4.0, 0.04,
                  extra={"note": "RIGHT pillar face + 6, lower half of the bay, clear of the garland swag. Round 4: "
                                 "raised just enough to keep 2 studs above the taller moss (see checks)"}),
        wall_part("Drip_Damp", "W_Drip_A", drip_x, TRIM_BOTTOM_Y + 0.35 - SPECS["W_Drip_A"]["studs"][1], 0.05,
                  extra={"note": "by the LEFT pillar: visible content starts 2 studs from the pillar face; top 0.35 "
                                 "hides behind the top trim (bottom y 22.9). If a garland pennant covers its top, "
                                 "slide it up to 0.5 stud toward the pillar (never onto the crack)."}),
    ]
    # round 4: the moss is taller -> lift W_Crack_B (in 0.25 steps from y 4) until its content clears the MossBase
    # by >= MIN_WALL_GAP; its top must stay below about y 16.5 (garland swag)
    mb_pts = outline(wall_points(wall[0]))
    for yb in np.arange(4.0, 6.51, 0.25):
        cand = wall_part("Crack_Diag", "W_Crack_B", crack_b_x, float(yb), 0.04, extra={"note": wall[2]["note"]})
        if min_dist(mb_pts, outline(wall_points(cand))) >= MIN_WALL_GAP:
            break
    wall[2] = cand
    # ---------------------------------------------------------------- floor
    # Decal on a Top face: image columns run along X and rows along Z (rotation 0). Whether the image TOP faces +Z
    # (the wall) or -Z is not verified, so each wall-foot carrier is pushed in until the LARGER of its top/bottom
    # content margins still reaches the foot: the moss then ends 0..MAX_FOOT_GAP short of the wall either way, and the
    # rest runs under the wall (hidden by the wall body).
    floor = []
    foot = []
    for name, tex, x in (("Moss_UnderCrack", "G_Moss_A", crack_c_x), ("Moss_WallFoot", "G_Moss_B", FACE_R + 5.6)):
        h = SPECS[tex]["studs"][1]
        m_hi = max(mg[tex]["top"], mg[tex]["bottom"])
        m_lo = min(mg[tex]["top"], mg[tex]["bottom"])
        zc = (WALL_Z - MAX_FOOT_GAP + 0.1) + m_hi - h / 2      # content edge 0.4 short of the wall in the worse case
        gaps = (WALL_Z - (zc + h / 2 - m_hi), WALL_Z - (zc + h / 2 - m_lo))
        foot.append({"part": name, "gap_to_wall_foot_studs": [round(g, 3) for g in gaps],
                     "orientations": ["image top toward the wall (+Z)" if mg[tex]["top"] >= mg[tex]["bottom"]
                                      else "image bottom toward the wall", "the other way round (negative = runs "
                                      "under the wall, hidden)"]})
        floor.append(floor_part(name, tex, x, zc, 0, 0.05, extra={
            "note": "wall-foot moss: reaches the wall foot so it joins the wall moss (rotation 0 on purpose: a yaw "
                    "would lift one corner off the foot)"}))
    floor.insert(0, floor_part("Stain_WallFoot", "G_Stain_A", BAY_X + 0.4, WALL_Z - 6.4, 20, 0.03, extra={
        "note": "damp watermark where the wall foot drains; its back edge runs under Moss_UnderCrack (layer 0.03 < "
                "0.05, both draw orders are fine)"}))
    floor.append(floor_part("Crack_Long", "G_Crack_A", BAY_X - 1.0, WALL_Z - 14.5, -25, 0.04, extra={
        "note": "away from the wall foot, crossing the walk line toward the bay"}))

    # ---------------------------------------------------------------- checks (refuse to write a bad patch)
    pts = {e["name"]: outline(wall_points(e)) for e in wall}
    clear = {}
    names = [e["name"] for e in wall]
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = names[i], names[j]
            if {a, b} == {"MossBase_Bay", "Crack_FloorUp"}:
                continue        # by design: the crack's notch sits IN the moss (its low slot)
            clear[f"{a} | {b}"] = round(min_dist(pts[a], pts[b]), 2)
    bad = {k: v for k, v in clear.items() if v < MIN_WALL_GAP}
    xs = []
    for e in wall + floor:
        w, _, d = e["size"]
        r = max(w, d) / 2 if e["face"] == "Top" else w / 2
        xs += [e["position"][0] - r, e["position"][0] + r]
    base_ok = all(not (lo - BASE_MARGIN < max(xs) and min(xs) < hi + BASE_MARGIN) for lo, hi in BASES.values())
    foot_ok = all(max(f["gap_to_wall_foot_studs"]) <= MAX_FOOT_GAP for f in foot)
    pillar_x = [(PILLAR_X[0] - PILLAR_W / 2, FACE_R), (FACE_L, PILLAR_X[1] + PILLAR_W / 2)]
    if bad or not base_ok or not foot_ok:
        raise SystemExit(f"test patch rejected: gaps<2 {bad}, base_ok {base_ok}, foot {foot}")

    patch = {
        "about": "HubGrime owner test patch (round 2). CFrame = CFrame.new(position) * CFrame.Angles(0, "
                 "math.rad(rotation_y_deg), 0). Parent: Workspace.HalloweenDecor.Grime.TestPatch. Every carrier: "
                 "Transparency 1, no collision/touch/query, CastShadow false. Wall carriers: identity rotation, so "
                 "the Front face looks at the hub (-Z). 'left'/'right' = as seen FROM THE HUB looking +Z (+X is on "
                 "the viewer's LEFT).",
        "assumptions": {
            "wall_inner_face_z": WALL_Z, "floor_top_y": FLOOR_Y, "trim_bottom_y": TRIM_BOTTOM_Y,
            "bay_pillar_centres_x": list(PILLAR_X), "pillar_size_x_z": [PILLAR_W, PILLAR_D],
            "pillar_centre_z": PILLAR_ZC, "pillar_front_z": round(PILLAR_ZC - PILLAR_D / 2, 3),
            "pillar_faces_x": {"left_seen_from_hub": FACE_L, "right_seen_from_hub": FACE_R},
            "bay_centre_x": round(BAY_X, 3), "bay_clear_width": round(BAY_W, 3),
            "stay_out_of": {k: {"x": list(v), "margin": BASE_MARGIN} for k, v in BASES.items()},
        },
        "verify": [
            "floor top y = 0 (stand a 1-stud test part on the floor in the bay and read its bottom)",
            "back wall inner face z = 104.00 (BackWall centre z 107, 6 thick)",
            "top trim bottom y = 22.9 (the drip's hidden 0.35 band must sit behind it)",
            "pillar depth: centres z 103.1, 1.6 deep -> they stand proud of the wall from z 104 to 102.3; the "
            "floor moss runs into the corner beside them",
            "pillar faces x 41.05 (right, seen from the hub) and 65.15 (left); the MossBase carrier spans exactly "
            "between them",
            "if the wall face or a pillar face is off, shift every wall part (z, or x) and the wall-foot floor parts "
            "(z) by the same delta",
        ],
        "checks": {
            "wall_content_clearance_studs (>= 2)": clear,
            "floor_moss_gap_to_wall_foot (<= 0.5; negative = tucked under the wall)": foot,
            "clear_of_Base2_Base3_with_margin": base_ok,
            "patch_x_range": [round(min(xs), 2), round(max(xs), 2)],
            "pillar_x_ranges": pillar_x,
        },
        "after_building": [
            "DELETE the GrimeTestPatch ModuleScript (it is only the JSON carrier for the command-bar snippet)",
            "show the owner TWO views: eye height (first person, about 25 studs back) AND the default THIRD-PERSON "
            "camera (character about 12 studs from the wall). From eye height the floor grime is faint and the "
            "stains vanish beyond about 25 studs - the third-person view is how players actually see the floor",
            "night check: switch to Moonlit and look again",
        ],
        "wall": wall,
        "floor": floor,
        "optional_plaza_rim": {
            "note": "a second small spot on the plaza rim (plaza centre (0,-33), r about 25), seen from spawn, outside "
                    "every base slot. Check that nothing stands there; the crack is on cream so it gets "
                    "Decal.Transparency 0.12.",
            "parts": [floor_part("Crack_Star_Rim", "G_Crack_B", 17.0, -46.0, 15, 0.04, transparency=0.12),
                      floor_part("Slime_Rim", "G_Slime_A", 21.5, -41.0, 0, 0.05)],
        },
        "luau_snippet": (
            "-- run in the Studio command bar after pasting the JSON into a ModuleScript 'GrimeTestPatch' "
            "(returns HttpService:JSONDecode(json)) and uploading the PNGs; fill IDS[texture] with the asset ids.\n"
            "local P = require(workspace.GrimeTestPatch); local IDS = {} -- IDS['W_MossBase_A'] = 'rbxassetid://...'\n"
            "local root = workspace.HalloweenDecor:FindFirstChild('Grime') or Instance.new('Folder', workspace.HalloweenDecor)"
            "; root.Name = 'Grime'\nlocal tp = Instance.new('Folder'); tp.Name = 'TestPatch'; tp.Parent = root\n"
            "local function make(e) local p = Instance.new('Part'); p.Name = e.name\n"
            "  for k, v in pairs(e.part) do if k == 'Material' then p.Material = Enum.Material[v] else p[k] = v end end\n"
            "  p.Size = Vector3.new(table.unpack(e.size))\n"
            "  p.CFrame = CFrame.new(table.unpack(e.position)) * CFrame.Angles(0, math.rad(e.rotation_y_deg), 0)\n"
            "  local d = Instance.new(e.kind == 'Texture' and 'Texture' or 'Decal'); d.Face = Enum.NormalId[e.face]\n"
            "  d.Texture = IDS[e.texture] or ''\n"
            "  for k, v in pairs(e.texture_props or {}) do d[k] = v end\n"
            "  for k, v in pairs(e.decal or {}) do d[k] = v end\n"
            "  d.Parent = p; p.Parent = tp end\n"
            "for _, e in ipairs(P.wall) do make(e) end; for _, e in ipairs(P.floor) do make(e) end\n"
            "workspace.GrimeTestPatch:Destroy() -- the ModuleScript is not needed once the parts exist"),
    }
    path = os.path.join(HERE, "test_patch.json")
    with open(path, "w") as f:
        json.dump(patch, f, indent=1)
    print("wrote", path)
    print(json.dumps(patch["checks"], indent=1))


if __name__ == "__main__":
    main()
