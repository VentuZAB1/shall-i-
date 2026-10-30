import json, time, io
D = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\CinderOverlord"
S = D + r"\_scratch"


def hr(path):
    s = open(path, encoding="utf-8", errors="replace").read()
    return json.loads(s.split("HEADLESS_RESULT", 1)[1].strip().splitlines()[0])


ex = hr(S + r"\export_r5.txt")
gold = json.load(open(S + r"\gold_r5.json"))
g = json.load(open(S + r"\gate_f85.json"))
g.update({
    "written": time.strftime("%Y-%m-%d %H:%M"),
    "round": "final 8.5 round 5 (_review/CinderOverlord_final85_r5.md + coordinator); the ONLY gate file",
    "export": {"fbx": r"C:\cdimp\CinderOverlord.fbx", "run": "_scratch/export_r5.txt",
               "meta_stride_BU_per_48f": round(ex["export"]["meta"]["stride"], 4) if "export" in ex else 5.0089},
    "step1": {"collision_free": ex["collision_free"], "ground_min_z": ex["ground_min_z"], "audit": ex["audit"],
              "tris": ex["tris_body"], "lua_bytes": ex["lua_bytes"], "events": ex["events"]},
    "gold_px_64": {k: {kk: v[kk] for kk in ("kit_29-58", "wide_29-60", "lemon_59-61", "hist", "fill_h", "fill_w",
                                             "area")} for k, v in gold.items()},
    "gold_method": "_scratch/gold_hist.py: icon3 recipe -> 64 px; s > .5, v > .45; kit window = game_icon.py hue "
                   "0.08-0.16 (H 28.8-57.6); wide = H 29-60; lemon = H 59-61. Kit counter (game_icon.py): portrait 81, "
                   "game 25 (identical)."})
json.dump(g, open(S + r"\gate_f85.json", "w"), indent=1)


def row(lab, k):
    v = gold[k]
    return "  | %s | %d | %d | %d | %.2f | %.3f |" % (lab, v["kit_29-58"], v["wide_29-60"], v["lemon_59-61"],
                                                     v["fill_h"], v["area"])


TXT = """## FINAL 8.5 ROUND 5 (2026-10-28, after `_review/CinderOverlord_final85_r5.md`: model 8.4, clips 8.5 PASS) - EXPORTED 06:09
Backups:
- the round-4 export: `_scratch/CinderOverlord_exported_r4.py`
- this export: `_scratch/CinderOverlord_exported_r5.py`

The 9+ patch is `_scratch/fix_r5.py`; the nose / chin caps were added after it (see 9+ below).
- **MUST 1, gold to amber:** crest-only `GOLD` (255, 196, 50) -> **(250, 160, 35)**.
  - Chosen from a 4-colour sweep on the kit portrait (`_scratch/gold_sweep_crest.png`, `gs_c0..c3`):

    | colour | kit H 29-58 | lemon H 59-61 | look |
    |---|---|---|---|
    | c0 (255, 196, 50), the old gold | 36 | 24 | lemon |
    | c1 (255, 172, 40) | 64 | 8 | still yellow-leaning |
    | **c2 (250, 160, 35)** | **80** | **1** | amber gold |
    | c3 (240, 150, 30) | 77 | 0 | turning orange |
  - c0 measured with my tool = 36, the same as the kit counter's round-4 number, so the tool matches the kit.
  - Why the hue moved: the lit faces had clipped G to 255 (lemon). With c2 they land at H 42-52.
    The shaded faces sit at H 30-38, which is still gold, not orange (`renders/close_front.png`).
  - GOLD_D is unused (no change).
- **Gold at 64 px** (`_scratch/gold_hist.py`, s > .5, v > .45; data `_scratch/gold_r5.json`):

  | icon | kit window H 29-58 | widened H 29-60 | lemon H 59-61 | fill height | opaque area |
  |---|---|---|---|---|---|
%s
%s
%s
%s
%s
  - Kit counter (`_tools/game_icon.py`): portrait **81**, game **25** - the same as above.
  - The game icon is AT the 25 floor (it was 28). Hue is not what limits it:
    - c2, (252, 168, 40) and (255, 176, 44) all give 25 there (`_scratch/g2_*`).
    - From behind only ~25 px of the crest frames show.
- **MUST 2, icon presence (lead ruling: pose + framing, not the model):**
  - `CinderOverlord_portrait_alt.png` (06:10) is the kit portrait camera (tq, transparent 512) at the **molt peak
    f40**: crest fanned 90 deg, neck arched, head level-high. The icon crops to the bounding box (icon3 recipe).
  - Icon: `CinderOverlord_icon_alt.png`.
  - Strips: `renders/_icons_alt_strip_64.png` / `_128.png`, laid out as [alt, kit idle f0, Thunder Rex, Cosmic Leviathan].
  - Numbers:
    - Height fill **0.89** (pass >= 0.70); gold 91 / 91, lemon 0.
    - Thunder Rex: fill 0.91, area 0.372. Cosmic Leviathan: fill 0.56, area 0.208.
  - Note: the current kit icon already measured fill 0.906 and area 0.383. The 'about 50 %%' in the review matches the
    Cosmic Leviathan (0.56), not the Cinder.
  - Closer / lower cameras were tried (`_scratch/pp_m4-m9`, `pp_r1-r3`). They cut the body at the frame edge or gave a
    narrower, weaker silhouette, so the kit distance was kept.
- **9+ (cheap):**
  - T-a eyes: socket and slit outer ends come in 0.02; the inner ends stay.
  - T-b snout: the "pig snout" was the skull's studs showing on the flat snout front. Now:
    - a smaller stud-free cap ring 0.012 ahead of the snout tip;
    - the jaw tip a touch flatter (rh 0.034 -> 0.030), with a stud-free chin cover and the same kind of cap.
    - From the front: a smooth nose and chin, the two nostril pits on top (`renders/close_front.png`, `_close_sheet.png`).
- **Step 1** (`_scratch/export_r5.txt`):
  - collision_free **true**; ground -0.006 everywhere; linear 0; loops 0 / 0.
  - Tris **10,468** (+240 for the caps / chin cover); stride **5.0089 BU / 48 f**.
  - FBX `C:\\cdimp\\CinderOverlord.fbx` 06:09.
- **Renders** (title bar 06:12, "final 8.5 round 5"):
  - `close_front`, `_close_sheet`, `gamelook_game` / `_tq`, `_model_sheet`, `flat_game_stamped`.
  - The two `_icons_strip` and two `_icons2_strip` sizes, plus `_icons_alt_strip_64` / `_128` (06:10).

""" % (row("kit portrait (idle f0)", "kit_portrait"), row("game camera", "game"),
       row("**portrait_alt (molt f40)**", "portrait_alt"), row("ThunderRex", "ThunderRex"),
       row("CosmicLeviathan", "CosmicLeviathan"))
p = D + r"\MODEL_NOTES.md"
s = io.open(p, encoding="utf-8").read()
i = s.index("## FINAL 8.5 ROUND 4")
io.open(p, "w", encoding="utf-8").write(s[:i] + TXT + s[i:])
c = io.open(D + r"\CLIP_NOTES.md", encoding="utf-8").read()
c = c.replace("Gate run (current): `_scratch/clipgate_r4.txt` + the export run `_scratch/export_r4.txt` (round 4: see MODEL_NOTES)",
              "Gate run (current): `_scratch/clipgate_r5.txt` + the export run `_scratch/export_r5.txt` (round 5: see MODEL_NOTES; clips unchanged)")
io.open(D + r"\CLIP_NOTES.md", "w", encoding="utf-8").write(c)
print("ok")
