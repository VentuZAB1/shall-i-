# rewrites CinderOverlord/_scratch/gate_f85.json for final-8.5 round 2 (still the ONLY gate file), both gold windows,
# then adds the round-2 sections to the notes
import json, os, time, io
D = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\CinderOverlord"
S = D + r"\_scratch"


def hr(path):
    s = open(path, encoding="utf-8", errors="replace").read()
    return json.loads(s.split("HEADLESS_RESULT", 1)[1].strip().splitlines()[0])


ex = hr(S + r"\export_r2.txt")
gw = json.loads(open(S + r"\gold_windows_r2.txt").read().split(" ", 1)[1])
fan = json.loads(open(S + r"\fan_r2.txt").read().split("FAN_RESULT", 1)[1])
ang = json.loads(open(S + r"\ang_r2.txt").read().split("ANG", 1)[1])
sh = json.load(open(S + r"\shares_all_r2.json"))
g = {
    "written": time.strftime("%Y-%m-%d %H:%M"),
    "round": "final 8.5 round 2 (_review/CinderOverlord_final85_r2.md + coordinator); the ONLY gate file",
    "export": {"fbx": r"C:\cdimp\CinderOverlord.fbx", "run": "_scratch/export_r2.txt"},
    "step1": {"collision_free": ex["collision_free"], "ground_min_z": ex["ground_min_z"], "audit": ex["audit"],
              "tris": ex["tris_body"], "lua_bytes": ex["lua_bytes"], "stride": round(ex["stride"], 3),
              "clips": ex["clips"], "events": ex["events"]},
    "gold_px_64": {
        "kit_counter": {"method": "_tools/game_icon.py: HSV H 29-58, s > 0.5, v > 0.45, LANCZOS 64 px",
                        "portrait": gw["portrait"]["kit_29-58_s.5_v.45"][0], "game": gw["game"]["kit_29-58_s.5_v.45"][0]},
        "rendered_window": {"method": "same 64 px icons, H 40-62, s >= 0.6, v >= 0.55 (_scratch/gold_cmp.py)",
                            "portrait": gw["portrait"]["rendered_40-62_s.6_v.55"][0],
                            "game": gw["game"]["rendered_40-62_s.6_v.55"][0]}},
    "shares_method": "flat palette ID renders renders/flat_<view>.png (idle f0), every figure pixel -> nearest palette colour",
    "shares_pct": sh,
    "molt_front_fan_spread_1_5_deg": {f: fan[f]["fan_spread_1_5"] for f in fan},
    "molt_blade_speed_deg_per_f": ang,
}
json.dump(g, open(S + r"\gate_f85.json", "w"), indent=1)
kp, kg = g["gold_px_64"]["kit_counter"]["portrait"], g["gold_px_64"]["kit_counter"]["game"]
rp, rg = g["gold_px_64"]["rendered_window"]["portrait"], g["gold_px_64"]["rendered_window"]["game"]


def ins(path, marker, text):
    s = io.open(path, encoding="utf-8").read()
    i = s.index(marker)
    io.open(path, "w", encoding="utf-8").write(s[:i] + text + s[i:])


def row(v):
    x = sh[v]
    return "  | %s | %.1f | %.1f | %.1f | %.1f | %.1f |" % (v, x["PLUM_OBS"], x["OBS_D"], x["PALE_S"], x["CROWN_IN"],
                                                         x["GOLD"] + x["GOLD_D"])


MODEL = """## FINAL 8.5 ROUND 2 (2026-10-28, after `_review/CinderOverlord_final85_r2.md` + coordinator) - EXPORTED
Backup of the round-1 export: `_scratch/CinderOverlord_exported_f85.py`. Gate file: `_scratch/gate_f85.json` (still the only one).
- **Brightness (coordinator):** the body is **(176,72,54)** (was 166,66,50), the same ember hue (H 8.9 vs 8.3). In
  `renders/_icons_strip_128.png` it stays red-ember: no drift toward Ivonrath's purple or the Phoenix's orange.
- **R2-M1, neck:** rings stay on Neck1 and Neck3; Neck2 has a narrow band (0.62-0.80); the ring on the chest curve is
  dropped. From above the neck now shows three bands, one of them thin (was four). `renders/gamelook_game.png`.
- **R2-M2, brows:** half-length **0.070**, roll **10 deg** (as asked).
  - At those numbers the outer ends still reached the crown mount from the front. The brow plane faces outward and
    forward, so its outer end sits further back and rises on screen.
  - I also moved the brows 0.012 toward the nose (BROW_IN 0.030) and dropped them **0.016** (BROW_DZ 0.040, was 0.056).
  - `renders/close_front.png` (and `_scratch/brow_zoom.png`): short dark blocks over the eyes, with red skull between
    them and the crown mount. The forward points are unchanged.
- **R2-M3, vents:** the blue slits are **15 %% longer**. They sit 4 deg further up the flank (32 / 148) so the lower ends
  stay clear of the pale scutes.
- **R2-M4, gold, both windows at 64 px:**

  | window | portrait | game |
  |---|---|---|
  | kit counter (H 29-58, s > 0.5, v > 0.45) | **%d** | %d |
  | rendered (H 40-62, s >= 0.6, v >= 0.55) | **%d** | %d |

  Both portrait windows are >= 25, so no gold change was needed.
- **TO 9+:**
  - (a) A smooth stud-free cover over the snout tip (the skull loft f 0.74-1.0, +0.004); the nasal ridge and nostrils
    sit on it.
  - (b) Tail4 is 45 %% shorter (the tip pulled in, the curl 0.13), so the walk stride is now **5.01 BU** per 48 f (was 5.19).
- **Shares (all figure pixels, %%):**

  | view | body | obsidian | pale | blue | gold |
  |---|---|---|---|---|---|
%s
%s
%s
%s
- **Tris 10,688.**

""" % (kp, kg, rp, rg, row("game"), row("side"), row("tq"), row("back"))

CLIP = """## FINAL 8.5 ROUND 2 (2026-10-28) - EXPORTED to `C:\\cdimp\\CinderOverlord.fbx` (03:42)
- **Idle breath x1.5:**
  - Neck 13.5 deg in total = **4.5 per bone** (measured 4.55; limit 8), with the head counter-pitching 9, so it stays
    near level.
  - The jaw, the crown breath (2.25) and the forearm paddle (3) scale with it. The loop is closed.
- **Walk:** the stride is 5.01 BU per 48 f after the shorter Tail4 (the walk-speed check is the coordinator's).
- **Molt:** unchanged.
  - Front fan spread f0 / 22 / 34 / 40: %.1f / %.1f / %.1f / %.1f deg.
  - Rise vs fall peaks are unchanged (`_scratch/ang_r2.txt`).
- **Step 1** (`_scratch/export_r2.txt`): collision_free **true**; ground_min_z -0.006 in every clip; linear 0; idle and
  walk loops 0 / 0. Events are unchanged.
- **Renders re-made:** `_pose_tq_sheet.png` (26 beats), `_cv_walk_side/game.png`, `_cv_roar_front/side.png`,
  `_molt_r4_front/side/tq.png`, `_cv_molt_front.png`, `_model_sheet.png`, `_close_sheet.png`, the icon strips and
  `gamelook_*`. The round-1 renders are in `_scratch/stale_f85_renders/`.

""" % (fan["0"]["fan_spread_1_5"], fan["22"]["fan_spread_1_5"], fan["34"]["fan_spread_1_5"], fan["40"]["fan_spread_1_5"])

ins(D + r"\MODEL_NOTES.md", "## FINAL 8.5 (2026-10-28", MODEL)
ins(D + r"\CLIP_NOTES.md", "## FINAL 8.5 (2026-10-28", CLIP)
print("gate + notes ok", kp, kg, rp, rg)
