import json, time, io
D = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\CinderOverlord"
S = D + r"\_scratch"


def hr(path, tag="HEADLESS_RESULT"):
    s = open(path, encoding="utf-8", errors="replace").read()
    return json.loads(s.split(tag, 1)[1].strip().splitlines()[0])


ex = hr(S + r"\export_r13.txt")
cp = hr(S + r"\coll_probe_r13.txt", "COLLPROBE")
paw = hr(S + r"\pawpx_r13.txt", "PAWPX")
st = hr(S + r"\stance_r13.txt", "STANCE")
st12 = hr(S + r"\stance_r12.txt", "STANCE")
gold = json.load(open(S + r"\gold_r13.json"))
gold12 = json.load(open(S + r"\gold_r12.json"))
gi = json.loads(open(S + r"\game_icon_out.txt", encoding="utf-8", errors="replace").read().strip().splitlines()[-1])
hs = json.loads(open(S + r"\headshare_r13.txt").read().split(" ", 1)[1])
B = cp["B_min_clearance"]
HOODK = ["HOOD|Head", "HOOD|Jaw", "HOOD|SPIKES", "HOOD|Crown_1", "HOOD|Crown_2", "HOOD|Crown_3", "HOOD|Crown_4",
         "HOOD|Crown_5", "HOOD|Claw_L", "HOOD|Claw_R", "HOOD|Arm_L", "HOOD|Arm_R", "HOOD|Neck1", "HOOD|Spine"]
CROWNK = ["Crown_1|Crown_2", "Crown_2|Crown_3", "Crown_3|Crown_4", "Crown_4|Crown_5"]
g = json.load(open(S + r"\gate_f85.json"))
# MUST 5: no other gold figure anywhere in the gate file - only gold_gate gates
h = g.pop("history_pre_r12", {})
for key in ("gold_px_64", "gold_method", "kit_counter_64"):
    h.pop(key, None)
h["note"] = ("older rounds' non-gold measurements, reference only (NOT gates). Gold: superseded by gold_gate "
             "(round 12); the old per-round gold fields are deleted.")
g["history_pre_r12"] = h
g.pop("collision_proof_r12", None)
g.pop("stance_r12", None)
g.update({
    "written": time.strftime("%Y-%m-%d %H:%M"),
    "round": "final 8.5 round 13 (_review/CinderOverlord_final85_r13.md + coordinator: the reviewer's 5 fixes); the ONLY gate file",
    "export": {"fbx": r"C:\cdimp\CinderOverlord.fbx", "run": "_scratch/export_r13.txt",
               "meta_stride_BU_per_48f": round(ex["export"]["meta"]["stride"], 4), "HEIGHT_studs": ex["export"]["meta"]["height"]},
    "step1": {"collision_free": ex["collision_free"], "pairs": cp["A_pairs"], "ground_min_z": ex["ground_min_z"],
              "audit": ex["audit"], "tris": ex["tris_body"], "lua_bytes": ex["lua_bytes"], "events": ex["events"]},
    "gold_gate": {
        "THE gate counter": "_tools/game_icon.py gold_px_portrait_64 (hue 0.08-0.16, s > 0.5, v > 0.45, 64 px) on "
                            "CinderOverlord_icon.png (the kit portrait icon, idle f0)",
        "value": gi["gold_px_portrait_64"], "floor": 103, "pass": gi["gold_px_portrait_64"] >= 103},
    "area_gate": {"what": "kit portrait icon (icon-3 recipe, 64 px) opaque share; outclass Thunder Rex 0.372",
                  "value": gold["kit_portrait"]["64"]["area"], "ThunderRex": gold["ThunderRex"]["64"]["area"],
                  "pass": gold["kit_portrait"]["64"]["area"] >= 0.372},
    "collision_proof_r13": {
        "probe": "_scratch/coll_probe.py -> coll_probe_r13.txt; per-frame seat depths _scratch/coll_depths_r13.json",
        "kit_gate": {"what": "blockkit.overlap_report with joints() (JOINT-AWARE)", "pairs": cp["A_pairs"],
                     "collision_free": cp["A_collision_free"]},
        "strict_run_A2": {"what": "the same pairs, each with ONLY its own parent-hinge proxy",
                          "collision_free": cp["A2_collision_free"], "NOT collision-free as an A2 count": True,
                          "only_entries": cp["A2_collisions"],
                          "listed_seats": {"Arm_L|Neck1": "left shoulder ball seated on the neck side (root)",
                                           "Arm_R|Neck1": "right shoulder ball seated on the neck side (root)"}},
        "seat_depth_BU": {"rest": cp["D_depth_rest"], "max_over_all_clips": cp["D_depth_max"], "limit": 0.035},
        "hood_clearance_all_frames": {k: B[k] for k in HOODK},
        "crown_neighbours_all_frames": {k: B[k] for k in CROWNK},
        "min_surface_clearance_all_frames": B},
    "stance_r13": {"probe": "_scratch/stance_probe.py -> stance_r13.txt", "per_clip": st},
    "paws_past_body_outline_game_cam_BU": {"L": paw["L"]["out_left_bu"], "R": paw["R"]["out_right_bu"]},
    "icons_64_128": {k: {sz: {kk: v[sz][kk] for kk in ("kit_29-58", "wide_29-60", "lemon_59-61", "fill_h", "fill_w",
                                                       "area")} for sz in ("64", "128")} for k, v in gold.items()},
    "game_icon_head_share": {"head_crown_of_icon_h": hs["head_of_icon_h"], "head_crown_of_figure_h": hs["head_of_figure_h"]}})
json.dump(g, open(S + r"\gate_f85.json", "w"), indent=1)


def cl(key):
    v = B[key]
    return "%.3f (%s f%d)" % (v[0], v[1], v[2])


TXT = """## FINAL 8.5 ROUND 13 (2026-10-28, after `_review/CinderOverlord_final85_r13.md`: model 8.3, clips 8.3 (act_molt)) - the reviewer's 5 fixes only - EXPORTED 14:41
Owner decision: one more SMALL round, the reviewer's 5 fixes and nothing else.

Backups:
- the round-12 export: `_scratch/CinderOverlord_exported_r12.py`
- this export: `_scratch/CinderOverlord_exported_r13.py`

The patch is `_scratch/fix_r13.py`, plus the crown and molt constants below.
1. **Hood colour:** the hood back plate goes from OBS_D to **PLUM_OBS** (ember) and the ribs to **PALE_S**. The obsidian
   rim and the sulfur-blue eye spots stay.
   - From the game camera the hood is now a red fan with a dark edge and pale ribs, separate from the dark frill and
     crown (`renders/gamelook_game.png`, `_icon_game_64_128.png`, `_hood_back_2x_idle_f0_f20.png`). Geometry is
     unchanged.
2. **Nose lump:** the hide test (`_scratch/nose_hide_r13.png`) shows two parts.
   - Under the nostrils: the muzzle's blunt oval front. That is the skull tip station plus the snout pad tube and its
     cap ring, seen end-on.
   - Under the mouth line: the jaw's round chin cap.
   - Fix (before / after in `_scratch/nose_r13_before_after.png`):
     - the muzzle tapers to a point: tip 0.044 x 0.022 -> **0.026 x 0.018**; 0.96 station width 0.060 -> **0.046**;
     - the muzzle slopes down to the tip (dz -0.026 / -0.034 / -0.036 -> **-0.040 / -0.062 / -0.068**);
     - the snout cap ring x0.80 / x0.60 -> **x0.55**;
     - the nostrils move to x 0.034 on the narrower tip;
     - the chin: jaw 0.85 station 0.078 / 0.032 -> **0.070 / 0.026**, tip 0.034 / 0.016 -> **0.024 / 0.012**, cap
       x0.80 -> **x0.60 / x0.55**.
   - Visible half-height under the nostril line: the tip is 0.018 (<= 0.03).
   - From the front the snout is now a wedge to a pointed nose (`renders/close_front.png`). The fangs and the roar
     mouth are unchanged (`_cv_roar_side.png`).
3. **Crown / area - deviation, measured:** the centre blade 0.40 -> 0.44 made the figure TALLER. The icon is
   bbox-normalised, so the kit area FELL to **0.354** (0.44 / 0.23 / 0.18) and 0.360 (0.44 / 0.27 / 0.22).
   - Trials, kit portrait at 64 px:

     | centre / middle / outer | gold | area |
     |---|---|---|
     | 0.40 / 0.23 / 0.18 (r12) | 113 | 0.365 |
     | 0.44 / 0.23 / 0.18 (review) | 110 | 0.354 |
     | 0.44 / 0.27 / 0.22 | 122 | 0.360 |
     | 0.40 / 0.27 / 0.22 | 118 | 0.370 |
     | **0.40 / 0.30 / 0.25** | **117** | **0.378** |
     | 0.42 / 0.30 / 0.26 | 124 | 0.371 |
   - Chosen: the centre stays **0.40**, the four side blades grow **0.23 / 0.18 -> 0.30 / 0.25**. They fill the top
     corners without adding height: kit area **%.3f** (Thunder Rex %.3f), gold **%d**.
   - Crown neighbours >= **%.4f** in all four clips: 1|2 %s, 2|3 %s, 3|4 %s, 4|5 %s.
4. **Molt hold - deviation, measured:** the review's head 20.5 -> 14 alone made the game-camera gap WORSE, **31.8 px**
   (r12 34.8). Nose-up tips the back of the head down toward the camera behind.
   - So I also used the review's fallback and lowered the neck arch. `MOLT_ARCH` -22.5 -> **-9** (3 deg per neck bone)
     and `MOLT_HEAD` 20.5 -> **9**, so the head stays level.
   - Game-camera head gap at every molt beat: **%.1f-%.1f px** (>= 50; r12 %.1f-%.1f).
   - NEW `renders/_molt_game.png` (game camera, f0 / 22 / 34 / 40 / 56 / 84 / 100): the blades lift and fan above a
     clear head.
5. **Gate file:** every old gold field (`gold_px_64`, the old `gold_method` text with the 91, `kit_counter_64`) is
   deleted from `gate_f85.json`. `gold_gate` is the only gold number (**%d**, floor 103), and `area_gate` is new
   (**%.3f** >= 0.372).
- **Kept:**
  - kit gate **collision_free true** (%d pairs); strict run only the two shoulder seats (<= %.4f);
  - hood clearance >= %.3f;
  - ground -0.006; loops 0 / 0; stride **%.4f**; HEIGHT 11.72; tris **%d**;
  - head + crown %.3f; game area **%.3f**; paws past the outline %.3f / %.3f;
  - game gap idle %.1f-%.1f, walk %.1f-%.1f, roar %.1f-%.1f px.
- **Renders** (title bars 14:41-14:43, "final 8.5 round 13"): the round-12 list plus `_molt_game.png`.
  - `_molt_r12_*` and `mr12_*` moved to `_scratch/stale_r13_renders/`.

""" % (gold["kit_portrait"]["64"]["area"], gold["ThunderRex"]["64"]["area"], gi["gold_px_portrait_64"],
       min(B[k][0] for k in CROWNK), cl(CROWNK[0]), cl(CROWNK[1]), cl(CROWNK[2]), cl(CROWNK[3]),
       st["act_molt"]["screen"]["gap"][0], st["act_molt"]["screen"]["gap"][1],
       st12["act_molt"]["screen"]["gap"][0], st12["act_molt"]["screen"]["gap"][1],
       gi["gold_px_portrait_64"], gold["kit_portrait"]["64"]["area"],
       cp["A_pairs"], cp["D_depth_max"]["Arm_L|Neck1"][1], min(B[k][0] for k in HOODK),
       ex["export"]["meta"]["stride"], ex["tris_body"], hs["head_of_figure_h"], gold["game"]["64"]["area"],
       paw["L"]["out_left_bu"], paw["R"]["out_right_bu"],
       st["idle"]["screen"]["gap"][0], st["idle"]["screen"]["gap"][1], st["walk"]["screen"]["gap"][0],
       st["walk"]["screen"]["gap"][1], st["roar"]["screen"]["gap"][0], st["roar"]["screen"]["gap"][1])
p = D + r"\MODEL_NOTES.md"
s = io.open(p, encoding="utf-8").read()
assert "## FINAL 8.5 ROUND 13" not in s
i = s.index("## FINAL 8.5 ROUND 12")
io.open(p, "w", encoding="utf-8").write(s[:i] + TXT + s[i:])
c = io.open(D + r"\CLIP_NOTES.md", encoding="utf-8").read()
old = c[c.index("Gate run (current):"):c.index("\n\n## ")]
new = ("Gate run (current): the export run `_scratch/export_r13.txt` (round 13, 14:41, see MODEL_NOTES; act_molt hold changed,\n"
       "the other clip keys unchanged); single gate file `_scratch/gate_f85.json`.\n"
       "Current sheets (2026-10-28 14:41-14:43, from the round-13 file): `renders/_pose_tq_sheet.png` (26 beats),\n"
       "`_cv_idle_game.png` / `_cv_idle_front.png`, `_hood_back_2x_idle_f0_f20.png`, `_cv_walk_side.png` /\n"
       "`_cv_walk_game.png`, `_cv_roar_front.png` / `_cv_roar_side.png`, `_molt_r13_front.png` / `_molt_r13_tq.png`,\n"
       "`_molt_game.png` (NEW, game camera). Older sheets and frames are in `_scratch/stale_r6_renders/` ...\n"
       "`stale_r13_renders/`.")
c = c.replace(old, new)
CT = """## FINAL 8.5 ROUND 13 (2026-10-28) - act_molt hold for the game camera
- **act_molt:** the arch hold goes -22.5 -> **-9** (3 deg per neck bone) and the head hold 20.5 -> **9** (`MOLT_ARCH`,
  `MOLT_HEAD`), so the head stays level.
  - Keys, timing, blade lifts / fans / reseat, ripple and events are unchanged (lift1 0.2, lift2 0.436, shed 0.509).
  - Why both: the review's head 20.5 -> 14 alone gave a 31.8 px gap (worse), because nose-up tips the back of the head
    toward the game camera.
  - Game-camera head gap at every beat: **%.1f-%.1f px** (r12 %.1f-%.1f; target >= 50). See NEW
    `renders/_molt_game.png`.
  - Pose limits: neck %.1f per bone (<= 8), head %.1f, chest %.1f (<= 5), head + neck pitch-up %.1f (<= 30).
- **Idle, walk and roar keys unchanged.** Gaps: idle %.1f-%.1f, walk %.1f-%.1f, roar %.1f-%.1f px.
- **Crown neighbours** with the taller side blades (lift + fan in the molt and roar) >= **%.4f** in all clips.
- **Collision:** kit gate **true**; strict run only the two shoulder seats (<= %.4f). Loops 0 / 0; stride %.4f;
  ground -0.006.

""" % (st["act_molt"]["screen"]["gap"][0], st["act_molt"]["screen"]["gap"][1], st12["act_molt"]["screen"]["gap"][0],
       st12["act_molt"]["screen"]["gap"][1], st["act_molt"]["max_angle"]["Neck1"][0], st["act_molt"]["max_angle"]["Head"][0],
       st["act_molt"]["max_angle"]["Spine"][0], st["act_molt"]["max_angle"]["head_pitch_up"][1],
       st["idle"]["screen"]["gap"][0], st["idle"]["screen"]["gap"][1], st["walk"]["screen"]["gap"][0],
       st["walk"]["screen"]["gap"][1], st["roar"]["screen"]["gap"][0], st["roar"]["screen"]["gap"][1],
       min(B[k][0] for k in CROWNK), cp["D_depth_max"]["Arm_L|Neck1"][1], ex["export"]["meta"]["stride"])
assert "## FINAL 8.5 ROUND 13" not in c
j = c.index("## FINAL 8.5 ROUND 12")
c = c[:j] + CT + c[j:]
io.open(D + r"\CLIP_NOTES.md", "w", encoding="utf-8").write(c)
print("ok")
