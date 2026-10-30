import json, time, io
D = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\CinderOverlord"
S = D + r"\_scratch"


def hr(path):
    s = open(path, encoding="utf-8", errors="replace").read()
    return json.loads(s.split("HEADLESS_RESULT", 1)[1].strip().splitlines()[0])


ex = hr(S + r"\export_r9.txt")
gold = json.load(open(S + r"\gold_r9.json"))
hs = json.loads(open(S + r"\headshare_r9.txt").read().split(" ", 1)[1])
g = json.load(open(S + r"\gate_f85.json"))
g.update({
    "written": time.strftime("%Y-%m-%d %H:%M"),
    "round": "final 8.5 round 9 (_review/CinderOverlord_final85_r9.md + coordinator); the ONLY gate file",
    "export": {"fbx": r"C:\cdimp\CinderOverlord.fbx", "run": "_scratch/export_r9.txt",
               "meta_stride_BU_per_48f": round(ex["export"]["meta"]["stride"], 4)},
    "step1": {"collision_free": ex["collision_free"], "ground_min_z": ex["ground_min_z"], "audit": ex["audit"],
              "tris": ex["tris_body"], "lua_bytes": ex["lua_bytes"], "events": ex["events"]},
    "icons_64_128": {k: {sz: {kk: v[sz][kk] for kk in ("kit_29-58", "wide_29-60", "lemon_59-61", "fill_h", "fill_w",
                                                       "area")} for sz in ("64", "128")} for k, v in gold.items()},
    "game_icon_head_share": {"head_crown_of_icon_h": hs["head_of_icon_h"], "head_crown_of_figure_h": hs["head_of_figure_h"]},
    "kit_counter_64": {"portrait": 110, "game": 47}})
json.dump(g, open(S + r"\gate_f85.json", "w"), indent=1)


def row(lab, k):
    a, b = gold[k]["64"], gold[k]["128"]
    return "  | %s | %d | %.3f | %d | %.3f |" % (lab, a["kit_29-58"], a["area"], b["kit_29-58"], b["area"])


TXT = """## FINAL 8.5 ROUND 9 (2026-10-28, after `_review/CinderOverlord_final85_r9.md`: model 8.4, clips 8.5 PASS) - EXPORTED 10:00
Backups:
- the round-8 export: `_scratch/CinderOverlord_exported_r8.py`
- this export: `_scratch/CinderOverlord_exported_r9.py`

The patch is `_scratch/fix_r9.py`, plus the muzzle taper.
- **MUST 1a, forearms out:** the elbow goes to x +/-**0.40** and the hand to +/-**0.36** (same y, z), in the model, the rig
  fallback and the `joints()` list.
  - The forearm now stands ~0.12 outside the chest outline at z 0.65.
  - From the game camera the near-side (left) claw shows as a braced arm beside the neck, in the idle and through the
    walk (`renders/gamelook_game.png`, `_cv_walk_game.png`).
  - The far-side claw stays behind the neck from that camera.
  - The slither and the paddles are unchanged and collision-free.
- **MUST 1b, broader skull:** Head + Jaw + Mouth parts go **x1.15 in x only** about the throat line (x = 0); the
  Crown_1..5 blades are untouched, so the sockets keep their spacing.
  - blockkit's `HEAD_XF` is uniform only, so this is a pet-side `_xscale()` run just before `B.build()`. Boxes keep
    their rotation and each local half-size grows by its scaled axis length; tubes / polys map their points.
  - HEAD_XF stays 1.45. Head + crown on the game camera: **0.306 of the figure height** (0.264 of the icon).
- **MUST 1c:** the Tail4 ring is dropped - only the Spine-base and Body1 rings remain (two bands on the back).
- **MUST 2, front face:**
  - As asked: the jaw station at 0.85 goes rh 0.040 -> **0.032**, and the jaw's front sits **0.02 further back** (the
    loft end -0.48 -> -0.46).
  - That alone still left a round nose pad above the chin, so the muzzle also tapers to a narrower tip:
    - skull stations 0.82 / 0.96 / 1.0: 0.118 / 0.070 / 0.055 wide -> 0.112 / 0.060 / 0.044;
    - the jaw tip 0.056 x 0.022 -> 0.046 x 0.020;
    - both nose caps sit flatter (x0.80 rings).
  - The nostril pits on top are unchanged.
  - From the front the nose is now a narrow muzzle tip with the chin tucked behind it, not two stacked round bulbs
    (`renders/close_front.png`, `_close_sheet.png`).
- **Numbers (kit window H 29-58):**

  | icon | gold 64 | area 64 | gold 128 | area 128 |
  |---|---|---|---|---|
%s
%s
%s
%s
%s
  - Kit counter: portrait 110, game 47. Gold >= 103: PASS (portrait_alt **135**).
  - Game-camera area **0.192** (>= 0.18).
- **Step 1** (`_scratch/export_r9.txt`):
  - collision_free **true** in all four clips (forearms out, wider skull; molt and roar included).
  - Ground -0.006; linear 0; loops 0 / 0.
  - Tris **11,348**; stride **5.0089**.
  - FBX `C:\\cdimp\\CinderOverlord.fbx` 10:00.
- **Renders** (title bars 10:00-10:01, "final 8.5 round 9"):
  - Game camera: `gamelook_game` / `_tq`, a game icon at 64 and 128 (`renders/_icon_game_64_128.png`), and the two
    `_icons2_strip` sizes.
  - Portrait: `CinderOverlord_portrait_alt.png` + `_icon_alt`; `_icons_alt_strip_64` / `_128` (with Phoenix and Ivonrath).
  - Sheets: `close_front`, `_close_sheet`, `_model_sheet`, `_molt_r9_front` / `_tq`, `_cv_roar_front` / `_side`,
    `_cv_walk_game` / `_side`, `_pose_tq_sheet`.
  - The `mr8_*` / `_molt_r8_*` files moved to `_scratch/stale_r9_renders/`.

""" % (row("**Cinder portrait_alt**", "portrait_alt"), row("Cinder kit portrait", "kit_portrait"),
       row("Cinder game camera", "game"), row("InfernoPhoenix", "InfernoPhoenix"), row("Ivonrath", "Ivonrath"))
p = D + r"\MODEL_NOTES.md"
s = io.open(p, encoding="utf-8").read()
i = s.index("## FINAL 8.5 ROUND 8")
io.open(p, "w", encoding="utf-8").write(s[:i] + TXT + s[i:])
c = io.open(D + r"\CLIP_NOTES.md", encoding="utf-8").read()
old = c[c.index("Gate run (current):"):c.index("\n\n## ")]
new = ("Gate run (current): the export run `_scratch/export_r9.txt` (round 9, 10:00: see MODEL_NOTES; the clip keys are\n"
       "unchanged; the forearms sit further out, the skull is 1.15x wider); single gate file `_scratch/gate_f85.json`.\n"
       "Current sheets (2026-10-28 10:00-10:01, from the round-9 file): `renders/_pose_tq_sheet.png` (26 beats),\n"
       "`_cv_walk_side.png` / `_cv_walk_game.png`, `_cv_roar_front.png` / `_cv_roar_side.png`, `_molt_r9_front.png` /\n"
       "`_molt_r9_tq.png`. Older sheets and frames are in `_scratch/stale_r6_renders/` ... `stale_r9_renders/`.")
c = c.replace(old, new)
io.open(D + r"\CLIP_NOTES.md", "w", encoding="utf-8").write(c)
print("ok")
