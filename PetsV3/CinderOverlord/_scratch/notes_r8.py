import json, time, io
D = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\CinderOverlord"
S = D + r"\_scratch"


def hr(path):
    s = open(path, encoding="utf-8", errors="replace").read()
    return json.loads(s.split("HEADLESS_RESULT", 1)[1].strip().splitlines()[0])


ex = hr(S + r"\export_r8.txt")
gold = json.load(open(S + r"\gold_r8.json"))
hs = json.loads(open(S + r"\headshare_r8.txt").read().split(" ", 1)[1])
g = json.load(open(S + r"\gate_f85.json"))
g.update({
    "written": time.strftime("%Y-%m-%d %H:%M"),
    "round": "final 8.5 round 8 (_review/CinderOverlord_final85_r8.md + coordinator); the ONLY gate file",
    "export": {"fbx": r"C:\cdimp\CinderOverlord.fbx", "run": "_scratch/export_r8.txt",
               "meta_stride_BU_per_48f": round(ex["export"]["meta"]["stride"], 4)},
    "step1": {"collision_free": ex["collision_free"], "ground_min_z": ex["ground_min_z"], "audit": ex["audit"],
              "tris": ex["tris_body"], "lua_bytes": ex["lua_bytes"], "events": ex["events"]},
    "icons_64_128": {k: {sz: {kk: v[sz][kk] for kk in ("kit_29-58", "wide_29-60", "lemon_59-61", "fill_h", "fill_w",
                                                       "area")} for sz in ("64", "128")} for k, v in gold.items()},
    "game_icon_head_share": {"head_crown_of_icon_h": hs["head_of_icon_h"], "head_crown_of_figure_h": hs["head_of_figure_h"],
                             "method": "_scratch/head_share.py (Head / Jaw / Mouth / Crown_* verts on the kit game camera)"},
    "kit_counter_64": {"portrait": 114, "game": 47}})
json.dump(g, open(S + r"\gate_f85.json", "w"), indent=1)


def row(lab, k):
    a, b = gold[k]["64"], gold[k]["128"]
    return "  | %s | %d | %.3f | %.2f | %d | %.3f |" % (lab, a["kit_29-58"], a["area"], a["fill_h"], b["kit_29-58"],
                                                      b["area"])


TXT = """## FINAL 8.5 ROUND 8 (2026-10-28, after `_review/CinderOverlord_final85_r8.md`: model 8.4, clips 8.5 PASS) - EXPORTED 09:32
Backups:
- the round-7 export: `_scratch/CinderOverlord_exported_r7.py`
- this export: `_scratch/CinderOverlord_exported_r8.py`

The patch is `_scratch/fix_r8.py`, plus the vent snap / crack edits.
- **1, head + crown:**
  - `HEAD_XF` 1.38 -> **1.45** (the lead's cap) and the centre blade 0.36 -> **0.40**.
  - Head + crown on the game camera (`_scratch/head_share.py`, idle f0): **0.302 of the figure height, 0.260 of the
    icon height**.
  - The icon frame is 1.16 x the larger side, so the whole figure tops out at 0.86 of the icon. The 0.30-of-icon target
    is NOT reached at 1.45 + 0.40; per the lead I did not go bigger.
  - Molt and roar are collision-free with the bigger head.
- **2, bands:** the Body4 ring is dropped (skip set 2-7). The rear rings are now on the Spine base, Body1 and Tail4;
  from behind the back shows two bands.
- **3, vents:** the six slits (Spine, Body1, Body2 x 2 sides) are **30 %% shorter** and **flush**.
  - New `vent_flush()`: each slit is 5 short overlapping bars that follow the curved flank.
  - Their points are ray-cast onto the REAL skin, because the loft is a superellipse and `surf_pt`'s ellipse sat ~0.01
    inside it: the first flush try was buried.
  - The top sits 0.001 proud of the skin, with a 0.002 core line.
  - Width x0.65, so they read as jagged glowing cracks, not plates or limbs; nothing sticks past the outline from the
    game camera (`renders/gamelook_game.png`).
- **4, dorsal spikes +25 %%** (body Spine..Tail1 and neck Neck1..3, length and base width). Collision-free with the crest
  in the molt and the roar.
- **5, hygiene:**
  - MODEL_NOTES line 3 now says MYTHIC.
  - `crown_*.png` and the `mr7_*` / `_molt_r7_*` frames moved to `_scratch/stale_r8_renders/`.
  - 9+ chin: the jaw tip goes 0.063 x 0.026 -> 0.056 x 0.022, the 0.85 station rh 0.044 -> 0.040, and the cap ring
    sits at 1.006 (was 1.012).
- **Portrait_alt camera:** a little higher, dir (1, -1.36, **0.80**) (kit 0.62).
  - Reason: the taller crest pushed the molt portrait area down to 0.348, under the round-7 >= 0.36 bar. At 0.80 it is
    0.373; still the molt peak f40, still three-quarter front.
- **Numbers (same counter, icon3 recipe, kit window H 29-58):**

  | icon | gold 64 | area 64 | fill h | gold 128 | area 128 |
  |---|---|---|---|---|---|
%s
%s
%s
%s
%s
  - Kit counter (`game_icon.py`): portrait 114, game 47.
  - **Gold >= 103: PASS** - portrait_alt **136** (Phoenix 93; at 128 px 537 vs 357, and vs 436 on its widened window).
  - **Area:** portrait_alt **0.373** (>= 0.36); game camera **0.188** (>= 0.18).
- **Step 1** (`_scratch/export_r8.txt`):
  - collision_free **true** in all four clips; ground -0.006; linear 0; loops 0 / 0.
  - Tris **11,384** (the curved vents); stride **5.0089** (unchanged).
  - FBX `C:\\cdimp\\CinderOverlord.fbx` 09:32.
- **Renders** (title bars 09:33-09:35, "final 8.5 round 8"):
  - Portrait: `CinderOverlord_portrait_alt.png` + `_icon_alt`.
  - Strips: `_icons_alt_strip_64` / `_128` (with Phoenix and Ivonrath), the two `_icons_strip` and two `_icons2_strip` sizes.
  - Sheets: `gamelook_game` / `_tq`, `close_front`, `_close_sheet`, `_model_sheet`, `_molt_r8_front` / `_tq`,
    `_cv_roar_front` / `_side`, `_cv_walk_game` / `_side`, `_pose_tq_sheet`.

""" % (row("**Cinder portrait_alt (molt f40, z 0.80)**", "portrait_alt"), row("Cinder kit portrait", "kit_portrait"),
       row("Cinder game camera", "game"), row("InfernoPhoenix", "InfernoPhoenix"), row("Ivonrath", "Ivonrath"))
p = D + r"\MODEL_NOTES.md"
s = io.open(p, encoding="utf-8").read()
s = s.replace("Magma / Fire egg, ULTRA-RARE 0.5 % (must beat Phoenix, Ivonrath AND the 1 % secrets Thunder Rex + Cosmic Leviathan).",
              "Magma / Fire egg, **MYTHIC** (secret + mythic in the economy plan, 0.5 %; must beat Phoenix, Ivonrath AND the 1 % secrets\n"
              "Thunder Rex + Cosmic Leviathan).")
i = s.index("## FINAL 8.5 ROUND 7")
io.open(p, "w", encoding="utf-8").write(s[:i] + TXT + s[i:])
c = io.open(D + r"\CLIP_NOTES.md", encoding="utf-8").read()
old = c[c.index("Gate run (current):"):c.index("\n\n## ")]
new = ("Gate run (current): the export run `_scratch/export_r8.txt` (round 8, 09:32: see MODEL_NOTES; the clip keys are\n"
       "unchanged; head group x1.45, centre blade 0.40, flush vents, +25 % dorsal spikes); single gate file\n"
       "`_scratch/gate_f85.json`. Current sheets (2026-10-28 09:33-09:35, from the round-8 file): `renders/_pose_tq_sheet.png`\n"
       "(26 beats), `_cv_walk_side.png` / `_cv_walk_game.png`, `_cv_roar_front.png` / `_cv_roar_side.png`, `_molt_r8_front.png` /\n"
       "`_molt_r8_tq.png`. Older sheets and frames are in `_scratch/stale_r6_renders/`, `stale_r6b_renders/`, `stale_r7_renders/`\n"
       "and `stale_r8_renders/`.")
c = c.replace(old, new)
io.open(D + r"\CLIP_NOTES.md", "w", encoding="utf-8").write(c)
print("ok")
