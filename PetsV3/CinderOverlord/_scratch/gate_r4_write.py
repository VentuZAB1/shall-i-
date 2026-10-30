import json, time, io
D = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\CinderOverlord"
S = D + r"\_scratch"


def hr(path):
    s = open(path, encoding="utf-8", errors="replace").read()
    return json.loads(s.split("HEADLESS_RESULT", 1)[1].strip().splitlines()[0])


ex = hr(S + r"\export_r4.txt")
gw = json.loads(open(S + r"\gold_windows_r4.txt").read().split(" ", 1)[1])
sh = json.load(open(S + r"\shares_all_r4.json"))
ang = json.loads(open(S + r"\ang_r4.txt").read().split("ANG", 1)[1])
g = json.load(open(S + r"\gate_f85.json"))
g.update({
    "written": time.strftime("%Y-%m-%d %H:%M"),
    "round": "final 8.5 round 4 (_review/CinderOverlord_final85_r4.md + coordinator); the ONLY gate file",
    "export": {"fbx": r"C:\cdimp\CinderOverlord.fbx", "run": "_scratch/export_r4.txt",
               "meta_stride_BU_per_48f": round(ex["export"]["meta"]["stride"], 4), "H_model_BU": 2.276},
    "step1": {"collision_free": ex["collision_free"], "ground_min_z": ex["ground_min_z"], "audit": ex["audit"],
              "tris": ex["tris_body"], "lua_bytes": ex["lua_bytes"], "clips": ex["clips"], "events": ex["events"]},
    "gold_px_64": {"kit_counter": {"portrait": 36, "game": 28, "method": "_tools/game_icon.py"},
                   "gold_cmp_kit_window": {"portrait": gw["portrait"]["kit_29-58_s.5_v.45"][0], "game": gw["game"]["kit_29-58_s.5_v.45"][0]},
                   "rendered_window": {"portrait": gw["portrait"]["rendered_40-62_s.6_v.55"][0],
                                       "game": gw["game"]["rendered_40-62_s.6_v.55"][0],
                                       "method": "H 40-62, s >= 0.6, v >= 0.55 (_scratch/gold_cmp.py)"}},
    "shares_pct": sh, "molt_blade_speed_deg_per_f": ang})
json.dump(g, open(S + r"\gate_f85.json", "w"), indent=1)


def row(v):
    x = sh[v]
    return "  | %s | %.1f | %.1f | %.1f | %.1f | %.1f |" % (v, x["PLUM_OBS"], x["OBS_D"], x["PALE_S"], x["CROWN_IN"],
                                                         x["GOLD"] + x["GOLD_D"])


TXT = """## FINAL 8.5 ROUND 4 (2026-10-28, after `_review/CinderOverlord_final85_r4.md` + coordinator) - EXPORTED 05:00
Backup of the round-3 export: `_scratch/CinderOverlord_exported_r3.py`.
- **1, vents:**
  - The vent core bar is now ROSE (the deep blue), not LAVA. The white cores read as ladder rungs.
  - In the walk from the game camera the blue slits still read as legs, so per T-e I dropped one slit of each pair. The
    pairs sit side by side along the body, not upper / lower, so each segment side keeps ONE slit at the pair centre
    (where the `Vent_*` anchor already is).
  - Now 6 slits per side instead of 12; no colour added. `renders/_cv_walk_game.png`.
- **2, neck:** the Neck3 ring is dropped and Neck2 is a thin band (0.70-0.80). From above: one full band (Neck1) and one
  thin band (Neck2); the Neck3 dorsal spike reads as a spike, not a band, so it stays. `renders/gamelook_game.png`.
- **3, walk renders:** `_cv_walk_game.png` / `_cv_walk_side.png` are re-made from the current file (05:00).
- **T-a, eyes:** the eye point moves to y -0.86 (was -0.83, originally -0.80); the brows follow.
- **T-b, snout:** the skull's tip stations are 10 %% flatter (rh 0.048 -> 0.043 and 0.040 -> 0.036); the smooth cover and
  the nostrils follow.
- **T-c, molt:** the outer blades lift **50 deg** (was 45). Still collision-free.
  - Front fan spread: f0 48.0, f22 69.4, f34 / f40 **90.0** deg (was 85.0).
  - Rise vs fall peak (deg/f): outer 8.29 vs 6.62, middle 7.88 vs 6.35, centre 5.18 vs 3.17 - every fall stays slower.
- **Gold at 64 px:**

  | tool | portrait | game |
  |---|---|---|
  | kit counter (`game_icon.py`) | **36** | **28** |
  | `gold_cmp` kit window | 38 | 29 |
  | rendered window (H 40-62) | **35** | 9 |
- **Shares (all figure pixels, %%):**

  | view | body | obsidian | pale | blue | gold |
  |---|---|---|---|---|---|
%s
%s
%s
%s
- **Step 1** (`_scratch/export_r4.txt`):
  - collision_free **true**; ground_min_z -0.006 everywhere; linear 0; loops 0 / 0.
  - Tris **10,228**. Export stride **5.0089 BU / 48 f**.
- **Renders (title bar = 2026-10-28 05:00):** `close_front`, `_close_sheet`, `gamelook_game`, `flat_game_stamped` (plain
  `flat_game` kept for the sampler), the four icon strips, `_model_sheet`, `_molt_r4_front` / `_side`,
  `_cv_walk_game` / `_side`, `_pose_tq_sheet`.

""" % (row("game"), row("side"), row("tq"), row("back"))
p = D + r"\MODEL_NOTES.md"
s = io.open(p, encoding="utf-8").read()
i = s.index("## FINAL 8.5 ROUND 3")
io.open(p, "w", encoding="utf-8").write(s[:i] + TXT + s[i:])
c = io.open(D + r"\CLIP_NOTES.md", encoding="utf-8").read()
c = c.replace("Gate run (current): `_scratch/clipgate_r3.txt` + the export run `_scratch/export_r3.txt` (round 3: see MODEL_NOTES)",
              "Gate run (current): `_scratch/clipgate_r4.txt` + the export run `_scratch/export_r4.txt` (round 4: see MODEL_NOTES)")
io.open(D + r"\CLIP_NOTES.md", "w", encoding="utf-8").write(c)
print("ok")
