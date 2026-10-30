import json, time, io
D = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\CinderOverlord"
S = D + r"\_scratch"


def hr(path):
    s = open(path, encoding="utf-8", errors="replace").read()
    return json.loads(s.split("HEADLESS_RESULT", 1)[1].strip().splitlines()[0])


ex = hr(S + r"\export_r3.txt")
gw = json.loads(open(S + r"\gold_windows_r3.txt").read().split(" ", 1)[1])
sh = json.load(open(S + r"\shares_all_r3.json"))
g = json.load(open(S + r"\gate_f85.json"))
g.update({
    "written": time.strftime("%Y-%m-%d %H:%M"),
    "round": "final 8.5 round 3 (_review/CinderOverlord_final85_r3.md + coordinator); the ONLY gate file",
    "export": {"fbx": r"C:\cdimp\CinderOverlord.fbx", "run": "_scratch/export_r3.txt",
               "meta_stride_BU_per_48f": round(ex["export"]["meta"]["stride"], 4), "H_model_BU": 2.276},
    "step1": {"collision_free": ex["collision_free"], "ground_min_z": ex["ground_min_z"], "audit": ex["audit"],
              "tris": ex["tris_body"], "lua_bytes": ex["lua_bytes"], "stride": round(ex["stride"], 4),
              "clips": ex["clips"], "events": ex["events"]},
    "gold_px_64": {
        "kit_counter": {"method": "_tools/game_icon.py: HSV H 29-58, s > 0.5, v > 0.45, LANCZOS 64 px",
                        "portrait": gw["portrait"]["kit_29-58_s.5_v.45"][0], "game": gw["game"]["kit_29-58_s.5_v.45"][0]},
        "rendered_window": {"method": "same 64 px icons, H 40-62, s >= 0.6, v >= 0.55 (_scratch/gold_cmp.py)",
                            "portrait": gw["portrait"]["rendered_40-62_s.6_v.55"][0],
                            "game": gw["game"]["rendered_40-62_s.6_v.55"][0]}},
    "shares_pct": sh})
json.dump(g, open(S + r"\gate_f85.json", "w"), indent=1)
k, r = g["gold_px_64"]["kit_counter"], g["gold_px_64"]["rendered_window"]


def row(v):
    x = sh[v]
    return "  | %s | %.1f | %.1f | %.1f | %.1f | %.1f |" % (v, x["PLUM_OBS"], x["OBS_D"], x["PALE_S"], x["CROWN_IN"],
                                                         x["GOLD"] + x["GOLD_D"])


TXT = """## FINAL 8.5 ROUND 3 (2026-10-28, after `_review/CinderOverlord_final85_r3.md` + coordinator) - EXPORTED 04:25
Backup of the round-2 export: `_scratch/CinderOverlord_exported_r2.py`.
- **MUST 1, forehead:** the obsidian skull cap ends at the eye line (stations 0.66 / 0.78 removed); the brows are
  unchanged. `renders/close_front.png` shows a red forehead band between the brows and the cap edge, with the nasal
  ridge down its middle.
- **MUST 2, neck:** only Neck1 keeps a full ring; Neck2 and Neck3 are narrow bands (0.62-0.80). From above there is one
  full band plus two thin ones (`renders/gamelook_game.png`).
- **MUST 3, nostrils:** pits are **0.006 x 0.004 x 0.009** at y -1.07 (the snout tip); they no longer read as a second
  pair of eyes.
- **T1, vents flush:** the slits are placed with `off=0.000` and the blue bar is **0.006** deep. The white-hot core
  line is 0.004 deep, 0.004 proud of the blue, so it does not stick out.
  - From the game camera the vents still read as blue-and-white bars - their colour carries the read - but nothing
    stands off the body any more.
- **T2, centre blade 0.32 -> 0.34:** the molt is still collision-free.
  - Front fan spread f0 / 22 / 34 / 40 is 48.0 / 66.9 / 85.0 / 85.0 deg, unchanged.
  - The model is now **2.276 BU** tall (was 2.254). HEIGHT stays 10.5 studs, so the in-game body is ~1 %% smaller; the
    stud pitch is 0.0486.
- **T3, eyes:** 0.03 toward the nose (the brows follow).
- **Gold at 64 px, both windows:**

  | window | portrait | game |
  |---|---|---|
  | kit counter | **%d** | **%d** |
  | rendered (H 40-62, s >= 0.6, v >= 0.55) | **%d** | %d |
- **Shares (all figure pixels, %%):**

  | view | body | obsidian | pale | blue | gold |
  |---|---|---|---|---|---|
%s
%s
%s
%s
- **Step 1** (`_scratch/export_r3.txt`): collision_free **true**; ground_min_z -0.006 in every clip; linear 0; loops 0 / 0.
  Tris **10,616**.
- **Walk stride (for the import check):** the export metadata carries **5.0089 BU per 48 f**.
- **Renders (title bar = render time, 2026-10-28 04:26):**
  - `close_front.png`, `_close_sheet.png`, `gamelook_game.png`, `_model_sheet.png`.
  - `_icons_strip_64/128.png`, `_icons2_strip_64/128.png`.
  - `_molt_r4_front.png`, `_pose_tq_sheet.png`.
  - `flat_game_stamped.png` - `flat_game.png` itself is left unstamped for the share sampler.

""" % (k["portrait"], k["game"], r["portrait"], r["game"], row("game"), row("side"), row("tq"), row("back"))
p = D + r"\MODEL_NOTES.md"
s = io.open(p, encoding="utf-8").read()
i = s.index("## FINAL 8.5 ROUND 2")
io.open(p, "w", encoding="utf-8").write(s[:i] + TXT + s[i:])
c = io.open(D + r"\CLIP_NOTES.md", encoding="utf-8").read()
c = c.replace("Gate run (current): `_scratch/clipgate_r2.txt` + the export run `_scratch/export_r2.txt`",
              "Gate run (current): `_scratch/clipgate_r3.txt` + the export run `_scratch/export_r3.txt` (round 3: see MODEL_NOTES)")
io.open(D + r"\CLIP_NOTES.md", "w", encoding="utf-8").write(c)
print("ok", k, r)
