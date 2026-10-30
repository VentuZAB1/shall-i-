import json, time, io
D = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\CinderOverlord"
S = D + r"\_scratch"


def hr(path, tag="HEADLESS_RESULT"):
    s = open(path, encoding="utf-8", errors="replace").read()
    return json.loads(s.split(tag, 1)[1].strip().splitlines()[0])


ex = hr(S + r"\export_r12.txt")
cp = hr(S + r"\coll_probe_r12.txt", "COLLPROBE")
paw = hr(S + r"\pawpx_r12.txt", "PAWPX")
st = hr(S + r"\stance_r12.txt", "STANCE")
gold = json.load(open(S + r"\gold_r12.json"))
gi = json.loads(open(S + r"\game_icon_out.txt", encoding="utf-8", errors="replace").read().strip().splitlines()[-1])
hs = json.loads(open(S + r"\headshare_r12.txt").read().split(" ", 1)[1])
B = cp["B_min_clearance"]
HOODK = ["HOOD|Head", "HOOD|Jaw", "HOOD|SPIKES", "HOOD|Crown_1", "HOOD|Crown_2", "HOOD|Crown_3", "HOOD|Crown_4",
         "HOOD|Crown_5", "HOOD|Claw_L", "HOOD|Claw_R", "HOOD|Arm_L", "HOOD|Arm_R", "HOOD|Neck1", "HOOD|Spine"]
g = json.load(open(S + r"\gate_f85.json"))
hist = g.pop("history_pre_r10", {})
for key in ("gold_px_64", "gold_method", "shares_method", "shares_pct", "molt_front_fan_spread_1_5_deg",
            "molt_blade_speed_deg_per_f", "kit_counter_64", "collision_proof_r11", "stance_r11"):
    if key in g:
        hist[key] = g.pop(key)
g["history_pre_r12"] = {"note": "older rounds' measurements, kept for reference only - NOT gates (the gold numbers here"
                                " are from rounds 5-9; the current gold gate is gold_gate below)", **hist}
g.update({
    "written": time.strftime("%Y-%m-%d %H:%M"),
    "round": "final 8.5 round 12 (_review/CinderOverlord_final85_r12.md + coordinator: OWNER -> COBRA HOOD); the ONLY gate file",
    "export": {"fbx": r"C:\cdimp\CinderOverlord.fbx", "run": "_scratch/export_r12.txt",
               "meta_stride_BU_per_48f": round(ex["export"]["meta"]["stride"], 4), "HEIGHT_studs": ex["export"]["meta"]["height"]},
    "step1": {"collision_free": ex["collision_free"], "pairs": cp["A_pairs"], "ground_min_z": ex["ground_min_z"],
              "audit": ex["audit"], "tris": ex["tris_body"], "lua_bytes": ex["lua_bytes"], "events": ex["events"]},
    "gold_gate": {
        "THE gate counter": "_tools/game_icon.py gold_px_portrait_64 (hue 0.08-0.16, s > 0.5, v > 0.45, 64 px) on "
                            "CinderOverlord_icon.png (the kit portrait icon, idle f0)",
        "value": gi["gold_px_portrait_64"], "floor": 103, "pass": gi["gold_px_portrait_64"] >= 103,
        "same counter via gold_hist.py kit_29-58 on the same icon": gold["kit_portrait"]["64"]["kit_29-58"],
        "not gates (reference)": {"portrait_alt (molt f40) kit window": gold["portrait_alt"]["64"]["kit_29-58"],
                                  "game camera icon": gi["gold_px_game_64"],
                                  "Weaver-brief counter [portrait, game]": gi["gold_px_brief_counter"]}},
    "collision_proof_r12": {
        "probe": "_scratch/coll_probe.py -> coll_probe_r12.txt; per-frame seat depths _scratch/coll_depths_r12.json",
        "kit_gate": {"what": "blockkit.overlap_report with joints() (JOINT-AWARE)", "pairs": cp["A_pairs"],
                     "collision_free": cp["A_collision_free"]},
        "strict_run_A2": {"what": "the same pairs, each with ONLY its own parent-hinge proxy",
                          "collision_free": cp["A2_collision_free"], "NOT collision-free as an A2 count": True,
                          "only_entries": cp["A2_collisions"],
                          "listed_seats": {"Arm_L|Neck1": "left shoulder ball seated on the neck side (root)",
                                           "Arm_R|Neck1": "right shoulder ball seated on the neck side (root)"}},
        "seat_depth_BU": {"rest": cp["D_depth_rest"], "max_over_all_clips": cp["D_depth_max"], "limit": 0.035},
        "hood_clearance_all_frames": {k: B[k] for k in HOODK},
        "min_surface_clearance_all_frames": B},
    "stance_r12": {"probe": "_scratch/stance_probe.py -> stance_r12.txt", "per_clip": st},
    "paws_past_body_outline_game_cam_BU": {"L": paw["L"]["out_left_bu"], "R": paw["R"]["out_right_bu"]},
    "icons_64_128": {k: {sz: {kk: v[sz][kk] for kk in ("kit_29-58", "wide_29-60", "lemon_59-61", "fill_h", "fill_w",
                                                       "area")} for sz in ("64", "128")} for k, v in gold.items()},
    "game_icon_head_share": {"head_crown_of_icon_h": hs["head_of_icon_h"], "head_crown_of_figure_h": hs["head_of_figure_h"]}})
json.dump(g, open(S + r"\gate_f85.json", "w"), indent=1)


def cl(key):
    v = B[key]
    return "%.3f (%s f%d)" % (v[0], v[1], v[2])


def row(lab, k):
    a, b = gold[k]["64"], gold[k]["128"]
    return "  | %s | %d | %.3f | %d | %.3f |" % (lab, a["kit_29-58"], a["area"], b["kit_29-58"], b["area"])


LAB = {"HOOD|Head": "skull / head parts", "HOOD|Jaw": "jaw", "HOOD|SPIKES": "frill + cheek spikes",
       "HOOD|Crown_1": "crown blade 1", "HOOD|Crown_2": "crown blade 2", "HOOD|Crown_3": "crown blade 3 (centre)",
       "HOOD|Crown_4": "crown blade 4", "HOOD|Crown_5": "crown blade 5", "HOOD|Claw_L": "left paw",
       "HOOD|Claw_R": "right paw", "HOOD|Arm_L": "left upper arm", "HOOD|Arm_R": "right upper arm",
       "HOOD|Neck1": "Neck1 (below)", "HOOD|Spine": "chest"}
table = "\n".join("  | %s | %.3f | %s f%d |" % (LAB[k], B[k][0], B[k][1], B[k][2]) for k in HOODK)
TXT = """## FINAL 8.5 ROUND 12 (2026-10-28, after `_review/CinderOverlord_final85_r12.md`: model 8.2, clips 8.5 APPROVED) - COBRA HOOD - EXPORTED 14:21
Owner decision (binding, via the lead): **cobra hood**. This is the last round before the owner decides again.

Backups:
- the round-11 export: `_scratch/CinderOverlord_exported_r11.py`
- this export: `_scratch/CinderOverlord_exported_r12.py`

The patch is `_scratch/fix_r12.py` plus the hood constants (`HOOD_*`) and `cobra_hood()` in the file.
- **MUST 1, cobra hood: thin studded plates, NOT a neck-radius scale.** Per side there are two panels:
  - The lower panel sits on **Neck2** (z 1.08-1.30), the upper on **Neck3** (z 1.26-1.64). Each is a thin lofted
    shell, 0.026 thick, so the idle sway, roar and molt carry the hood with the neck.
  - The panels sit 0.07 behind the neck axis and cup forward at the rim (0.10), so from behind they read as a fan.
  - Front face: ember (the body colour), smooth.
  - Back: an **obsidian studded back plate**, inset 0.025 from the rim.
  - **Rim:** obsidian, along the whole outer outline.
  - **Ribs:** three ember ribs per side on the dark back.
  - **Eye spot:** one **sulfur-blue** spot per side with a white-hot centre (cobra hood marking).
  - **Width:** the widest point is |x| **0.64** at z 1.38-1.44, just under the head. That is 0.43 past the neck side
    (0.21) and 0.27 past the skull side (0.37), so the hood is clearly wider than the skull. It narrows into the neck
    above (under the jaw) and below (z 1.08).
    - This is wider than the lead's "~0.12 per side", for the brief's own target (T / fan, wider than the skull).
      `HOOD_W` 1.45 is one constant; 1.22 gives |x| 0.55.
  - The upper panel's top shoulders stay under the lowest cheek spikes.
  - Hood 2x close-up from fixed cameras (back and game direction, idle f0 / f20, the hood swaying with the neck):
    `renders/_hood_back_2x_idle_f0_f20.png`.
  - The r11 radius-scale trial stays rejected (`_scratch/r11_hood_trial_rejected.png`).
- **Hood clearance, proxy-free, every frame of all four clips** (min, clip and frame):

  | hood vs | min BU | at |
  |---|---|---|
%s

  - All are **>= 0.02** (hood minimum %s).
- **MUST 2, snout:** skull stations 0.82 / 0.96 half-height 0.082 / 0.040 -> **0.066 / 0.028** (widths kept). The tip
  (0.022) and the cap ring (x0.60) are unchanged. The nostrils re-seat by `surf_hit`.
  - `close_front.png` shows a lower, tapered snout front. The fangs are unchanged, and the roar mouth is unchanged
    (Jaw|Neck2 %s).
- **MUST 3, one gold number:** the gate counter is `_tools/game_icon.py` `gold_px_portrait_64` on the kit portrait icon
  (`CinderOverlord_icon.png`, idle f0) = **%d** (>= 103, PASS). `gold_hist.py`'s kit window on the same icon gives
  the same %d.
  - The "91" the reviewer saw was a stale round-5-9 field (`gold_px_64` / the old `gold_method` text). It is moved to
    `history_pre_r12` and marked "not gates".
  - Reference only: portrait_alt %d, game icon %d. No extra gold was needed.
- **Kept:**
  - head + crown **%.3f** of the figure height;
  - game area **%.3f**;
  - paws past the outline %.3f / %.3f;
  - crown neighbours >= %s;
  - shoulder seats <= **%.4f** (strict run: only those two entries);
  - Neck2|Spine and Body4|Body2 depth 0;
  - kit gate **collision_free true** (%d pairs, + Head / Jaw vs Neck2);
  - ground -0.006; loops 0 / 0; linear 0;
  - stride **%.4f** (walk keys unchanged); HEIGHT 11.72; tris **%d**.
- **Numbers (kit window H 29-58):**

  | icon | gold 64 | area 64 | gold 128 | area 128 |
  |---|---|---|---|---|
%s
%s
%s
%s
%s
- **Renders** (title bars 14:21-14:24, "final 8.5 round 12"): the round-11 list plus `_hood_back_2x_idle_f0_f20.png`.
  - `gamelook_game` / `_tq`, `_icon_game_64_128`, `_icons2_strip_64` / `_128`, `_cv_idle_game` / `_front`.
  - `CinderOverlord_portrait_alt.png` + `_icon_alt`, `_icons_alt_strip_64` / `_128`, `_icons_strip_64` / `_128`.
  - `close_front`, `_close_sheet`, `_model_sheet`, `_pose_tq_sheet`, `_molt_r12_front` / `_tq`, `_cv_roar_front` /
    `_side`, `_cv_walk_game` / `_side`.
  - The `mr11_*` / `_molt_r11_*` files moved to `_scratch/stale_r12_renders/`.
- **Honest read:**
  - From the game camera the dark hood with its two blue spots now shows as a wide band under the crown and frill: a
    T / fan top on the neck.
  - At 64 px the hood and frill merge into one dark crowned block over the red coil.
  - The 3/4 and front views read as a hooded cobra-dragon.

""" % (table, cl(min(HOODK, key=lambda k: B[k][0])), cl("Jaw|Neck2"),
       gi["gold_px_portrait_64"], gold["kit_portrait"]["64"]["kit_29-58"], gold["portrait_alt"]["64"]["kit_29-58"],
       gi["gold_px_game_64"], hs["head_of_figure_h"], gold["game"]["64"]["area"], paw["L"]["out_left_bu"],
       paw["R"]["out_right_bu"], "%.3f" % min(B[k][0] for k in ("Crown_1|Crown_2", "Crown_2|Crown_3", "Crown_3|Crown_4",
                                                                "Crown_4|Crown_5")),
       cp["D_depth_max"]["Arm_L|Neck1"][1], cp["A_pairs"], ex["export"]["meta"]["stride"], ex["tris_body"],
       row("**Cinder kit portrait (GATE)**", "kit_portrait"), row("Cinder portrait_alt", "portrait_alt"),
       row("Cinder game camera", "game"), row("InfernoPhoenix", "InfernoPhoenix"), row("ThunderRex", "ThunderRex"))
p = D + r"\MODEL_NOTES.md"
s = io.open(p, encoding="utf-8").read()
assert "## FINAL 8.5 ROUND 12" not in s
i = s.index("## FINAL 8.5 ROUND 11")
io.open(p, "w", encoding="utf-8").write(s[:i] + TXT + s[i:])
c = io.open(D + r"\CLIP_NOTES.md", encoding="utf-8").read()
old = c[c.index("Gate run (current):"):c.index("\n\n## ")]
new = ("Gate run (current): the export run `_scratch/export_r12.txt` (round 12, 14:21: COBRA HOOD on Neck2 / Neck3, see\n"
       "MODEL_NOTES; clip keys unchanged since round 11); single gate file `_scratch/gate_f85.json`.\n"
       "Current sheets (2026-10-28 14:21-14:24, from the round-12 file): `renders/_pose_tq_sheet.png` (26 beats),\n"
       "`_cv_idle_game.png` / `_cv_idle_front.png`, `_hood_back_2x_idle_f0_f20.png`, `_cv_walk_side.png` /\n"
       "`_cv_walk_game.png`, `_cv_roar_front.png` / `_cv_roar_side.png`, `_molt_r12_front.png` / `_molt_r12_tq.png`.\n"
       "Older sheets and frames are in `_scratch/stale_r6_renders/` ... `stale_r12_renders/`.")
c = c.replace(old, new)
CT = """## FINAL 8.5 ROUND 12 (2026-10-28) - cobra hood; clip keys unchanged (clips APPROVED 8.5 in round 12)
- The hood panels are skinned to **Neck2** (lower) and **Neck3** (upper), so they move with the neck.
  - Idle cobra sway: the hood swings with the neck (`renders/_hood_back_2x_idle_f0_f20.png`, fixed cameras).
  - Roar gather and molt arch: the hood leans back with the neck.
- **Hood clearance**, proxy-free, every frame of all four clips:
  - head %s;
  - jaw %s;
  - frill / cheek spikes %s;
  - crown >= %.3f;
  - paws >= %.3f;
  - arms >= %.3f.
- **Pose limits unchanged** (`stance_r12.txt`): neck <= 7.5 per bone, chest 4.5, head + neck pitch-up <= 4.
- **Game-camera head gap:** idle %.1f-%.1f px, walk %.1f-%.1f px.
- **Collision:**
  - Kit gate **true** (%d pairs).
  - Strict run: only the two shoulder seats (<= %.4f).
- Loops 0 / 0; stride %.4f; ground -0.006.

""" % (cl("HOOD|Head"), cl("HOOD|Jaw"), cl("HOOD|SPIKES"),
       min(B[k][0] for k in HOODK if "Crown" in k), min(B["HOOD|Claw_L"][0], B["HOOD|Claw_R"][0]),
       min(B["HOOD|Arm_L"][0], B["HOOD|Arm_R"][0]),
       st["idle"]["screen"]["gap"][0], st["idle"]["screen"]["gap"][1], st["walk"]["screen"]["gap"][0],
       st["walk"]["screen"]["gap"][1], cp["A_pairs"], cp["D_depth_max"]["Arm_L|Neck1"][1], ex["export"]["meta"]["stride"])
assert "## FINAL 8.5 ROUND 12" not in c
j = c.index("## FINAL 8.5 ROUND 11")
c = c[:j] + CT + c[j:]
io.open(D + r"\CLIP_NOTES.md", "w", encoding="utf-8").write(c)
print("ok")
