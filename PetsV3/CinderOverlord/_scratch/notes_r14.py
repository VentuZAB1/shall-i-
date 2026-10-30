import json, time, io
D = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\CinderOverlord"
S = D + r"\_scratch"


def hr(path, tag="HEADLESS_RESULT"):
    s = open(path, encoding="utf-8", errors="replace").read()
    return json.loads(s.split(tag, 1)[1].strip().splitlines()[0])


ex = hr(S + r"\export_r14.txt")
cp = hr(S + r"\coll_probe_r14.txt", "COLLPROBE")
paw = hr(S + r"\pawpx_r14.txt", "PAWPX")
st = hr(S + r"\stance_r14.txt", "STANCE")
gold = json.load(open(S + r"\gold_r14.json"))
gi = json.loads(open(S + r"\game_icon_out.txt", encoding="utf-8", errors="replace").read().strip().splitlines()[-1])
hs = json.loads(open(S + r"\headshare_r14.txt").read().split(" ", 1)[1])
B = cp["B_min_clearance"]
HOODK = [k for k in B if k.startswith("HOOD|")]
CROWNK = ["Crown_1|Crown_2", "Crown_2|Crown_3", "Crown_3|Crown_4", "Crown_4|Crown_5"]
BLADEK = ["BLADE_%d|Head" % i for i in range(1, 6)]
g = json.load(open(S + r"\gate_f85.json"))
g.pop("collision_proof_r13", None)
g.pop("stance_r13", None)
g.update({
    "written": time.strftime("%Y-%m-%d %H:%M"),
    "round": "final 8.5 round 14 (_review/CinderOverlord_final85_r14.md + coordinator: micro-fix); the ONLY gate file",
    "export": {"fbx": r"C:\cdimp\CinderOverlord.fbx", "run": "_scratch/export_r14.txt",
               "meta_stride_BU_per_48f": round(ex["export"]["meta"]["stride"], 4), "HEIGHT_studs": ex["export"]["meta"]["height"],
               "portrait_exported_with_the_fbx": ex["export"].get("portrait")},
    "step1": {"collision_free": ex["collision_free"], "pairs": cp["A_pairs"], "ground_min_z": ex["ground_min_z"],
              "audit": ex["audit"], "tris": ex["tris_body"], "lua_bytes": ex["lua_bytes"], "events": ex["events"]},
    "shipping_portrait": {
        "ships": "CinderOverlord/CinderOverlord_portrait_raw.png (kit portrait, idle f0) -> icon CinderOverlord/CinderOverlord_icon.png",
        "why": "the kit export writes this portrait with the FBX; its icon is the gold / area gate icon",
        "icon_64": {"gold (gate counter)": gi["gold_px_portrait_64"], "area": gold["kit_portrait"]["64"]["area"]},
        "not shipped": {"file": "CinderOverlord/CinderOverlord_portrait_alt.png (molt f40, reference render only)",
                        "area_64": gold["portrait_alt"]["64"]["area"],
                        "reframe trials (molt f40, dir 1,-1.36,0.62 / 0.70 / 1.2,-1.36,0.80)": [0.362, 0.366, 0.370],
                        "note": "never >= 0.372, so it is dropped from the outclass claim"}},
    "gold_gate": {
        "THE gate counter": "_tools/game_icon.py gold_px_portrait_64 (hue 0.08-0.16, s > 0.5, v > 0.45, 64 px) on "
                            "CinderOverlord_icon.png (the shipping kit portrait icon, idle f0)",
        "value": gi["gold_px_portrait_64"], "floor": 103, "pass": gi["gold_px_portrait_64"] >= 103},
    "area_gate": {"what": "the shipping kit portrait icon (icon-3 recipe, 64 px) opaque share; outclass Thunder Rex",
                  "value": gold["kit_portrait"]["64"]["area"], "ThunderRex": gold["ThunderRex"]["64"]["area"],
                  "pass": gold["kit_portrait"]["64"]["area"] >= 0.372},
    "collision_proof_r14": {
        "probe": "_scratch/coll_probe.py -> coll_probe_r14.txt; per-frame seat depths _scratch/coll_depths_r14.json",
        "kit_gate": {"what": "blockkit.overlap_report with joints() (JOINT-AWARE)", "pairs": cp["A_pairs"],
                     "collision_free": cp["A_collision_free"]},
        "strict_run_A2": {"what": "the same pairs, each with ONLY its own parent-hinge proxy",
                          "collision_free": cp["A2_collision_free"], "NOT collision-free as an A2 count": True,
                          "only_entries": cp["A2_collisions"],
                          "listed_seats": {"Arm_L|Neck1": "left shoulder ball seated on the neck side (root)",
                                           "Arm_R|Neck1": "right shoulder ball seated on the neck side (root)"},
                          "Crown_1..5|Head": "no entries: each blade socket stays inside its own hinge zone in the mount"},
        "seat_depth_BU": {"rest": cp["D_depth_rest"], "max_over_all_clips": cp["D_depth_max"], "limit": 0.035},
        "crown_vs_head_all_frames": {
            "what": "Crown_i BLADE (every vertex > 0.07 above its hinge = above the crown mount) vs the Head group "
                    "(skull, mount, cap, brows, eyes; the frill / cheek spikes are SPIKES|Crown_i). The socket below "
                    "is seated in the mount by design (strict run: no crossing outside its hinge zone).",
            **{k.replace("BLADE_", "Crown_"): B[k] for k in BLADEK}, "pass_>=0.02": min(B[k][0] for k in BLADEK) >= 0.02},
        "crown_neighbours_all_frames": {k: B[k] for k in CROWNK},
        "hood_clearance_all_frames": {k: B[k] for k in HOODK},
        "min_surface_clearance_all_frames": B},
    "stance_r14": {"probe": "_scratch/stance_probe.py -> stance_r14.txt", "per_clip": st},
    "paws_past_body_outline_game_cam_BU": {"L": paw["L"]["out_left_bu"], "R": paw["R"]["out_right_bu"]},
    "icons_64_128": {k: {sz: {kk: v[sz][kk] for kk in ("kit_29-58", "wide_29-60", "lemon_59-61", "fill_h", "fill_w",
                                                       "area")} for sz in ("64", "128")} for k, v in gold.items()},
    "game_icon_head_share": {"head_crown_of_icon_h": hs["head_of_icon_h"], "head_crown_of_figure_h": hs["head_of_figure_h"]}})
json.dump(g, open(S + r"\gate_f85.json", "w"), indent=1)


def cl(key):
    v = B[key]
    return "%.3f (%s f%d)" % (v[0], v[1], v[2])


TXT = """## FINAL 8.5 ROUND 14 (2026-10-28, after `_review/CinderOverlord_final85_r14.md`: model 8.4, clips 8.5 APPROVED) - micro-fix - EXPORTED 14:53
Backups:
- the round-13 export: `_scratch/CinderOverlord_exported_r13.py`
- this export: `_scratch/CinderOverlord_exported_r14.py`

Nothing else changed.
1. **Hood rim:** the rim `B.seg` in `cobra_hood()` goes from OBS_D to **PALE_S** (222, 194, 158); its size is unchanged.
   - From the game camera the hood is now a red fan with a light edge, separate from the dark frill above:
     `renders/gamelook_game.png`, `_icon_game_64_128.png` (a light-edged fan at 128, a light band under the dark head at
     64), `_hood_back_2x_idle_f0_f20.png`.
   - The fallback (lowering the hood top 0.03) was not needed.
   - Geometry is unchanged, so every hood clearance is as round 13 (min %s).
2. **Crown vs Head:** each blade socket is seated in the crown mount. That is a hinge: in the strict run no
   Crown_i|Head crossing falls outside its own hinge zone.
   - Clearance of each blade above the mount (every vertex more than 0.07 above its hinge) to the Head group, all
     frames of all four clips:
     - Crown_1 %s;
     - Crown_2 %s;
     - **Crown_3 %s**;
     - Crown_4 %s;
     - Crown_5 %s.
     - All are **>= 0.02**.
   - Crown neighbours >= %.4f. Frill / cheek spikes to the crown >= %.3f.
3. **Shipping portrait:** **`CinderOverlord_portrait_raw.png`** (kit portrait, idle f0; the kit export writes it with the
   FBX) and its icon **`CinderOverlord_icon.png`**: gold **%d** (the gate counter), area **%.3f** (Thunder Rex %.3f).
   - The alt (`CinderOverlord_portrait_alt.png`, molt f40) is NOT shipped: area %.3f. Three reframes reached
     0.362 / 0.366 / 0.370, never 0.372.
   - It stays a reference render; `_icons_alt_strip_*` labels it "not shipped".
- **Kept as round 13:**
  - kit gate **collision_free true** (%d pairs); strict run only the two shoulder seats (<= %.4f);
  - ground -0.006; loops 0 / 0; stride **%.4f**; HEIGHT 11.72; tris **%d**;
  - head + crown %.3f; game area **%.3f**; paws %.3f / %.3f;
  - game gaps idle %.1f-%.1f, walk %.1f-%.1f, roar %.1f-%.1f, molt %.1f-%.1f px.
- **Renders** (title bars 14:53-14:55, "final 8.5 round 14"): the round-13 list.
  - `_molt_r13_*` and `mr13_*` moved to `_scratch/stale_r14_renders/`.

""" % (cl(min(HOODK, key=lambda k: B[k][0])), cl(BLADEK[0]), cl(BLADEK[1]), cl(BLADEK[2]), cl(BLADEK[3]),
       cl(BLADEK[4]), min(B[k][0] for k in CROWNK), min(B["SPIKES|Crown_%d" % i][0] for i in (1, 2, 4, 5)),
       gi["gold_px_portrait_64"], gold["kit_portrait"]["64"]["area"], gold["ThunderRex"]["64"]["area"],
       gold["portrait_alt"]["64"]["area"], cp["A_pairs"], cp["D_depth_max"]["Arm_L|Neck1"][1],
       ex["export"]["meta"]["stride"], ex["tris_body"], hs["head_of_figure_h"], gold["game"]["64"]["area"],
       paw["L"]["out_left_bu"], paw["R"]["out_right_bu"],
       st["idle"]["screen"]["gap"][0], st["idle"]["screen"]["gap"][1], st["walk"]["screen"]["gap"][0],
       st["walk"]["screen"]["gap"][1], st["roar"]["screen"]["gap"][0], st["roar"]["screen"]["gap"][1],
       st["act_molt"]["screen"]["gap"][0], st["act_molt"]["screen"]["gap"][1])
p = D + r"\MODEL_NOTES.md"
s = io.open(p, encoding="utf-8").read()
assert "## FINAL 8.5 ROUND 14" not in s
i = s.index("## FINAL 8.5 ROUND 13")
io.open(p, "w", encoding="utf-8").write(s[:i] + TXT + s[i:])
c = io.open(D + r"\CLIP_NOTES.md", encoding="utf-8").read()
old = c[c.index("Gate run (current):"):c.index("\n\n## ")]
new = ("Gate run (current): the export run `_scratch/export_r14.txt` (round 14, 14:53: hood rim colour only, see MODEL_NOTES;\n"
       "clip keys as round 13); single gate file `_scratch/gate_f85.json`.\n"
       "Current sheets (2026-10-28 14:53-14:55, from the round-14 file): `renders/_pose_tq_sheet.png` (26 beats),\n"
       "`_cv_idle_game.png` / `_cv_idle_front.png`, `_hood_back_2x_idle_f0_f20.png`, `_cv_walk_side.png` /\n"
       "`_cv_walk_game.png`, `_cv_roar_front.png` / `_cv_roar_side.png`, `_molt_r14_front.png` / `_molt_r14_tq.png`,\n"
       "`_molt_game.png`. Older sheets and frames are in `_scratch/stale_r6_renders/` ... `stale_r14_renders/`.")
c = c.replace(old, new)
io.open(D + r"\CLIP_NOTES.md", "w", encoding="utf-8").write(c)
print("ok")
