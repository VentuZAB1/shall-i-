import json, time, io
D = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\CinderOverlord"
S = D + r"\_scratch"


def hr(path):
    s = open(path, encoding="utf-8", errors="replace").read()
    return json.loads(s.split("HEADLESS_RESULT", 1)[1].strip().splitlines()[0])


ex = hr(S + r"\export_r6.txt")
gold = json.load(open(S + r"\gold_r6.json"))
g = json.load(open(S + r"\gate_f85.json"))
g.update({
    "written": time.strftime("%Y-%m-%d %H:%M"),
    "round": "final 8.5 round 6 (_review/CinderOverlord_final85_r6.md + coordinator); the ONLY gate file",
    "export": {"fbx": r"C:\cdimp\CinderOverlord.fbx", "run": "_scratch/export_r6.txt",
               "meta_stride_BU_per_48f": round(ex["export"]["meta"]["stride"], 4)},
    "step1": {"collision_free": ex["collision_free"], "ground_min_z": ex["ground_min_z"], "audit": ex["audit"],
              "tris": ex["tris_body"], "lua_bytes": ex["lua_bytes"], "events": ex["events"]},
    "icons_64_128": {k: {sz: {kk: v[sz][kk] for kk in ("kit_29-58", "wide_29-60", "lemon_59-61", "fill_h", "fill_w",
                                                       "area")} for sz in ("64", "128")} for k, v in gold.items()},
    "gold_method": "_scratch/gold_hist.py: icon3 recipe -> 64 / 128 px; s > .5, v > .45; kit window = game_icon.py "
                   "hue 0.08-0.16 (H 28.8-57.6); wide = H 29-60; lemon = H 59-61. Kit counter (game_icon.py) at 64: "
                   "portrait 91, game 35."})
json.dump(g, open(S + r"\gate_f85.json", "w"), indent=1)


def row(lab, k):
    a, b = gold[k]["64"], gold[k]["128"]
    return "  | %s | %d | %d | %.3f | %.2f | %.2f | %d | %d | %.3f |" % (
        lab, a["kit_29-58"], a["wide_29-60"], a["area"], a["fill_h"], a["fill_w"], b["kit_29-58"], b["wide_29-60"],
        b["area"])


TXT = """## FINAL 8.5 ROUND 6 (2026-10-28, after `_review/CinderOverlord_final85_r6.md`: model 8.4, clips 8.5 on every clip) - EXPORTED 08:41
Backups:
- the round-5 export: `_scratch/CinderOverlord_exported_r5.py`
- this export: `_scratch/CinderOverlord_exported_r6b.py`
- **MUST 1, the game-camera worm read:**
  - (a) Ring skip set `(3, 5, 7)` -> **`(2, 3, 5, 6, 7)`**. The rings stay on the Spine base, Body1, Body4 and Tail4,
    i.e. 3 dark bands on the rear 8 segments. The Neck1 ring and the dorsal saddle are kept.
  - (b) **RAD[1..4] +10 %%** (0.339 / 0.308 / 0.277 / 0.220). The Body4 -> Tail1 taper (0.220 -> 0.168) reads fine in
    `_model_sheet`.
  - Measured with (a) + (b) alone: game-camera area **0.166**, fill width **0.50** - NOT enough; thickness hardly moves it.
    Extra test: tail +30 %%, neck +15 %% -> area 0.175, width 0.50.
  - (c) So I added **COIL = 1.5**: each body segment's heading away from the mean is x1.5. The S coils sideways and
    reads as a coiled serpent rather than a straight worm.
    - Every segment keeps its round-5 3D length, so the slither **stride stays 5.0089** (a plain RAD +10 %% would have
      made it 5.0186).
    - Non-adjacent body points stay >= 0.08 apart; collision-free.
  - Result (game icon, 64 px): area **0.190** (pass >= 0.18). Fill width **0.53** (FAIL vs >= 0.60).
    - Why the width won't move: the game camera sits behind and 24 deg to the side, so the body's run toward the
      camera also adds width. Coiling swaps that run for sideways S, and the two nearly cancel (coil 1.4 / 1.6 gave
      0.53 / 0.55).
    - Getting >= 0.60 needs the rear body to trail at an angle to the travel line, and then the slither would look like
      it crabs sideways. **Lead decision needed.**
  - Game-camera gold went up to 35 (kit counter) from 25.
- **MUST 2, outclass (same counter, icon3 recipe):**

  | icon | gold 64 (H 29-58) | gold 64 (H 29-60) | area 64 | fill h | fill w | gold 128 (H 29-58) | gold 128 (H 29-60) | area 128 |
  |---|---|---|---|---|---|---|---|---|
%s
%s
%s
%s
%s
%s
%s
  - Before the fix, the Cinder's portrait_alt gold was 88 / 349 (64 / 128) vs the Phoenix's 93 / 357, so it failed on
    gold. The opaque area already beat both.
  - Fix, crest only: the gold frames widen **+25 %% INWARD**. The new `plate_crown(gin=)` moves the frame centre in
    and grows its half-width by the same amount, so the outer edge and the blade-to-blade clearance stay put.
    - A plain x1.25 width made Crown_2|3 and Crown_3|4 touch in the roar and the molt, so it was dropped.
    - +45 %% inward gave only +2 px more and covered the blue inner V, so it was dropped too.
  - Result:
    - The Cinder portrait_alt is >= Phoenix and Ivonrath on gold (94 vs 93 / 25 at 64; 390 vs 357 / 112 at 128) and
      on area (0.373 vs 0.267 / 0.295).
    - Fill height: Cinder 0.89, Phoenix 0.91, Ivonrath **0.67**. Ivonrath is below the 0.70 bar on its own icon; that is
      not the Cinder's.
    - Caveat: the 64 px gold margin over the Phoenix is 1 px on the kit window. On the widened window the Phoenix
      counts 109 / 436 because 14 / 68 of its px are lemon flame (H 59-61); the Cinder has 0 lemon.
- **Step 1** (`_scratch/export_r6.txt`):
  - collision_free **true** (all four clips, incl. the molt with the thicker body); ground -0.006; linear 0; loops 0 / 0.
  - Tris **10,268** (fewer rings); stride **5.0089**.
  - FBX `C:\\cdimp\\CinderOverlord.fbx` 08:41.
- **Re-made from the final file** (title bars 08:43 / 08:46, "final 8.5 round 6"):
  - The `CinderOverlord_portrait_alt.png` (molt f40) render is from 08:42; `CinderOverlord_icon_alt.png` was made from it.
  - Strips: `_icons_alt_strip_64` / `_128` = [alt, kit, Phoenix, Ivonrath, Rex, Leviathan], the two `_icons_strip` and
    two `_icons2_strip` sizes.
  - Sheets: `_pose_tq_sheet`, `_cv_walk_game` / `_side`, `_cv_roar_front` / `_side`, `_molt_r6_front` / `_tq`,
    `close_front`, `_close_sheet`, `gamelook_game` / `_tq`, `_model_sheet`, `flat_game_stamped`.
  - Stale sheets (`_molt_r4_*`, `_cv_molt_front`, `_clip_sheet_v1`) moved to `_scratch/stale_r6b_renders/`.

""" % (row("**Cinder portrait_alt (molt f40)**", "portrait_alt"), row("Cinder kit portrait (idle f0)", "kit_portrait"),
       row("Cinder game camera", "game"), row("InfernoPhoenix", "InfernoPhoenix"), row("Ivonrath", "Ivonrath"),
       row("ThunderRex", "ThunderRex"), row("CosmicLeviathan", "CosmicLeviathan"))
p = D + r"\MODEL_NOTES.md"
s = io.open(p, encoding="utf-8").read()
i = s.index("## FINAL 8.5 ROUND 5")
io.open(p, "w", encoding="utf-8").write(s[:i] + TXT + s[i:])
c = io.open(D + r"\CLIP_NOTES.md", encoding="utf-8").read()
old = c[c.index("Gate run (current):"):c.index("(older sheets are in `_scratch/stale_r6_renders/`).")]
new = ("Gate run (current): the export run `_scratch/export_r6.txt` (round 6, 08:41: see MODEL_NOTES; the clip keys are\n"
       "unchanged, the body path coils 1.5x and RAD[1..4] +10 %); single gate file `_scratch/gate_f85.json`. Current sheets\n"
       "(2026-10-28 08:43-08:46, from the round-6 file): `renders/_pose_tq_sheet.png` (26 beats), `_cv_walk_side.png` /\n"
       "`_cv_walk_game.png`, `_cv_roar_front.png` / `_cv_roar_side.png`, `_molt_r6_front.png` / `_molt_r6_tq.png` ")
c = c.replace(old, new).replace("(older sheets are in `_scratch/stale_r6_renders/`).",
                                "(older sheets are in `_scratch/stale_r6_renders/` and `_scratch/stale_r6b_renders/`).")
io.open(D + r"\CLIP_NOTES.md", "w", encoding="utf-8").write(c)
print("ok")
