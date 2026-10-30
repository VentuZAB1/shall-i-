import json, time, io
D = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\CinderOverlord"
S = D + r"\_scratch"


def hr(path):
    s = open(path, encoding="utf-8", errors="replace").read()
    return json.loads(s.split("HEADLESS_RESULT", 1)[1].strip().splitlines()[0])


ex = hr(S + r"\export_r7.txt")
gold = json.load(open(S + r"\gold_r7.json"))
g = json.load(open(S + r"\gate_f85.json"))
g.update({
    "written": time.strftime("%Y-%m-%d %H:%M"),
    "round": "final 8.5 round 7 (_review/CinderOverlord_final85_r7.md + coordinator); the ONLY gate file",
    "export": {"fbx": r"C:\cdimp\CinderOverlord.fbx", "run": "_scratch/export_r7.txt",
               "meta_stride_BU_per_48f": round(ex["export"]["meta"]["stride"], 4)},
    "step1": {"collision_free": ex["collision_free"], "ground_min_z": ex["ground_min_z"], "audit": ex["audit"],
              "tris": ex["tris_body"], "lua_bytes": ex["lua_bytes"], "events": ex["events"]},
    "icons_64_128": {k: {sz: {kk: v[sz][kk] for kk in ("kit_29-58", "wide_29-60", "lemon_59-61", "fill_h", "fill_w",
                                                       "area")} for sz in ("64", "128")} for k, v in gold.items()},
    "game_icon_head_share": {"head_crown_of_icon_h": 0.244, "head_crown_of_figure_h": 0.283,
                             "method": "_scratch/head_share.py (Head / Jaw / Mouth / Crown_* verts on the kit game camera)"},
    "kit_counter_64": {"portrait": 108, "game": 45}})
json.dump(g, open(S + r"\gate_f85.json", "w"), indent=1)


def row(lab, k):
    a, b = gold[k]["64"], gold[k]["128"]
    return "  | %s | %d | %d | %.3f | %.2f | %d | %d | %.3f |" % (
        lab, a["kit_29-58"], a["wide_29-60"], a["area"], a["fill_h"], b["kit_29-58"], b["wide_29-60"], b["area"])


TXT = """## FINAL 8.5 ROUND 7 (2026-10-28, after `_review/CinderOverlord_final85_r7.md`: model 8.3, clips 8.5 PASS) - EXPORTED 09:08
Backups:
- the round-6 export: `_scratch/CinderOverlord_exported_r6b.py`
- this export: `_scratch/CinderOverlord_exported_r7.py`

The patch is `_scratch/fix_r7.py` (+ the nostril line and the inward gold).
- **MUST 1a, vents:** the slits on Body3, Body4 and Tail1 are gone. The vents stay on the Spine, Body1 and Body2 (the
  front of the body near the head).
  - The `Vent_4..6` bones go with them; only `Vent_1..3` remain.
  - The plan's FX_VentSmoke_4..6 therefore have no anchor (VFX is not built yet).
- **MUST 1b, head:** the head group goes **x1.15** (`HEAD_XF` 1.20 -> 1.38, about the throat). The crown mount is
  0.04 wider each side (ends 0.22 -> 0.26).
  - Head + crown height on the game icon (`_scratch/head_share.py`): **0.244** of the icon height (0.283 of the figure).
    The review's target is >= 0.30 (not reached).
- **MUST 2, gold:**
  - The centre blade goes 0.34 -> **0.36**.
  - The centre and middle gold frames get **+0.004**. It went INWARD: outward, Crown_2|3 and Crown_3|4 touched even in
    the idle. The frames now sit at `gin` 0.25 x gw + 0.004.
- **Numbers (same counter, icon3 recipe):**

  | icon | gold 64 (H 29-58) | gold 64 (H 29-60) | area 64 | fill h | gold 128 (H 29-58) | gold 128 (H 29-60) | area 128 |
  |---|---|---|---|---|---|---|---|
%s
%s
%s
%s
%s
  - Kit counter (`game_icon.py`): portrait 108, game 45.
  - **Gold >= 103: PASS** - portrait_alt 113 at 64 px (+21 %% over the Phoenix's 93). At 128 px it is 466, which also
    beats the Phoenix's widened-window 436.
  - **Area:** portrait_alt 0.364 (>= 0.36); game camera **0.190** (>= 0.18).
  - **Head line:** in `renders/_icons_alt_strip_128.png` the Cinder's crown reaches the top of its tile, above the
    Phoenix's crest line.
- **9+:**
  - Eyes: the slit outer ends come in another 0.01 (socket 0.115 -> 0.110, slit 0.100 -> 0.095; the inner ends stay).
  - Chin: the jaw tip station is ~15 %% flatter / narrower (0.074 x 0.030 -> 0.063 x 0.026) and the cap ring sits
    closer (1.024 -> 1.012).
  - Nostrils: 0.012 x 0.018 -> **0.018 x 0.024**, which is 0.025 x 0.033 BU as shown (x1.38 head).
- **Step 1** (`_scratch/export_r7.txt`):
  - collision_free **true** in all four clips (the bigger head in the roar / molt included); ground -0.006; linear 0;
    loops 0 / 0.
  - Tris **10,188**; stride **5.0089** (unchanged).
  - FBX `C:\\cdimp\\CinderOverlord.fbx` 09:08.
- **Renders** (title bars 09:09-09:11, "final 8.5 round 7"):
  - Portrait: `CinderOverlord_portrait_alt.png` (molt f40) + `_icon_alt`.
  - Strips: `_icons_alt_strip_64` / `_128` (with Phoenix and Ivonrath), the two `_icons_strip` and two `_icons2_strip` sizes.
  - Close-ups (re-framed for the bigger head): `close_front`, `_close_sheet`.
  - Sheets: `gamelook_game` / `_tq`, `_model_sheet`, `_pose_tq_sheet`, `_cv_walk_game` / `_side`, `_cv_roar_front` /
    `_side`, `_molt_r7_front` / `_tq`.
  - The `mr4_*` / `mr6_*` frames and `_molt_r6_*` moved to `_scratch/stale_r7_renders/`.

""" % (row("**Cinder portrait_alt (molt f40)**", "portrait_alt"), row("Cinder kit portrait", "kit_portrait"),
       row("Cinder game camera", "game"), row("InfernoPhoenix", "InfernoPhoenix"), row("Ivonrath", "Ivonrath"))
p = D + r"\MODEL_NOTES.md"
s = io.open(p, encoding="utf-8").read()
i = s.index("## FINAL 8.5 ROUND 6")
io.open(p, "w", encoding="utf-8").write(s[:i] + TXT + s[i:])
c = io.open(D + r"\CLIP_NOTES.md", encoding="utf-8").read()
old = c[c.index("Gate run (current):"):c.index("\n\n## ")]
new = ("Gate run (current): the export run `_scratch/export_r7.txt` (round 7, 09:08: see MODEL_NOTES; the clip keys are\n"
       "unchanged; the head group is x1.15 bigger, the vents stay on the front three segments only); single gate file\n"
       "`_scratch/gate_f85.json`. Current sheets (2026-10-28 09:09-09:11, from the round-7 file): `renders/_pose_tq_sheet.png`\n"
       "(26 beats), `_cv_walk_side.png` / `_cv_walk_game.png`, `_cv_roar_front.png` / `_cv_roar_side.png`, `_molt_r7_front.png` /\n"
       "`_molt_r7_tq.png`. Older sheets and frames are in `_scratch/stale_r6_renders/`, `stale_r6b_renders/` and\n"
       "`stale_r7_renders/` (the `mr4_*` / `mr6_*` frames moved there in round 7).")
c = c.replace(old, new)
io.open(D + r"\CLIP_NOTES.md", "w", encoding="utf-8").write(c)
print("ok")
