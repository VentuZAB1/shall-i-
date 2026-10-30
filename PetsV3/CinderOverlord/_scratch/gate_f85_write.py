# writes CinderOverlord/_scratch/gate_f85.json = THE single gate file of the final-8.5 round (one gold method)
import json, os, time
D = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\CinderOverlord\_scratch"


def hr(path):
    s = open(os.path.join(D, path), encoding="utf-8", errors="replace").read()
    return json.loads(s.split("HEADLESS_RESULT", 1)[1].strip().splitlines()[0])


ex = hr("export_f85.txt")
gi = json.loads(open(os.path.join(D, "game_icon_out.txt")).read().strip().splitlines()[-1])
fan = json.loads(open(os.path.join(D, "fan_f85.txt")).read().split("FAN_RESULT", 1)[1])
ang = json.loads(open(os.path.join(D, "ang_f85.txt")).read().split("ANG", 1)[1])
shares = json.load(open(os.path.join(D, "shares_all_f85.json")))
out = {
    "written": time.strftime("%Y-%m-%d %H:%M"),
    "round": "final 8.5 (_review/CinderOverlord_final85.md); the ONLY gate file - gate_r6.json and gold_windows_r6.txt are STALE",
    "export": {"fbx": r"C:\cdimp\CinderOverlord.fbx", "run": "_scratch/export_f85.txt"},
    "step1": {"collision_free": ex["collision_free"], "ground_min_z": ex["ground_min_z"], "audit": ex["audit"],
              "tris": ex["tris_body"], "lua_bytes": ex["lua_bytes"], "clips": ex["clips"], "events": ex["events"]},
    "gold_px_64": {"method": "kit counter _tools/game_icon.py (HSV H 29-58 deg, s > 0.5, v > 0.45, LANCZOS 64 px)",
                   "portrait": gi["gold_px_portrait_64"], "game": gi["gold_px_game_64"]},
    "shares_method": "flat palette ID renders renders/flat_<view>.png (idle f0), every figure pixel -> nearest palette colour",
    "shares_pct": shares,
    "molt_front_fan": {"method": "_scratch/fan_probe.py: Crown bone tilt from vertical in the front (x-z) plane",
                       "spread_1_5_deg": {f: fan[f]["fan_spread_1_5"] for f in fan},
                       "per_blade_change_vs_f0": {f: {b: fan[f][b]["d_front"] for b in fan[f] if b.startswith("Crown")}
                                                  for f in ("22", "34", "40")}},
    "molt_blade_speed": {"method": "_scratch/ang_probe.py (deg/frame vs rest)", "per_blade": ang},
}
json.dump(out, open(os.path.join(D, "gate_f85.json"), "w"), indent=1)
for f in ("gate_r6.json", "gold_windows_r6.txt"):
    p = os.path.join(D, f)
    if os.path.exists(p):
        os.replace(p, os.path.join(D, "STALE_f85_" + f))
print("gate_f85.json written; portrait", gi["gold_px_portrait_64"], "game", gi["gold_px_game_64"])
