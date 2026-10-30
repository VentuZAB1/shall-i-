import json, time, io
D = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\CinderOverlord"
S = D + r"\_scratch"


def hr(path, tag="HEADLESS_RESULT"):
    s = open(path, encoding="utf-8", errors="replace").read()
    return json.loads(s.split(tag, 1)[1].strip().splitlines()[0])


ex = hr(S + r"\export_r11.txt")
cp = hr(S + r"\coll_probe_r11.txt", "COLLPROBE")
paw = hr(S + r"\pawpx_r11.txt", "PAWPX")
st = hr(S + r"\stance_r11.txt", "STANCE")
st10 = hr(S + r"\stance_r10.txt", "STANCE")
gold = json.load(open(S + r"\gold_r11.json"))
hs = json.loads(open(S + r"\headshare_r11.txt").read().split(" ", 1)[1])
B = cp["B_min_clearance"]
g = json.load(open(S + r"\gate_f85.json"))
g.update({
    "written": time.strftime("%Y-%m-%d %H:%M"),
    "round": "final 8.5 round 11 (_review/CinderOverlord_final85_r11.md + coordinator: RAISED COBRA STANCE); the ONLY gate file",
    "export": {"fbx": r"C:\cdimp\CinderOverlord.fbx", "run": "_scratch/export_r11.txt",
               "meta_stride_BU_per_48f": round(ex["export"]["meta"]["stride"], 4), "HEIGHT_studs": 11.72,
               "H_model_BU": 2.829},
    "step1": {"collision_free": ex["collision_free"], "pairs": cp["A_pairs"], "ground_min_z": ex["ground_min_z"],
              "audit": ex["audit"], "tris": ex["tris_body"], "lua_bytes": ex["lua_bytes"], "events": ex["events"]},
    "collision_proof_r10": None,
    "collision_proof_r11": {
        "probe": "_scratch/coll_probe.py -> coll_probe_r11.txt; per-frame depths _scratch/coll_depths_r11.json",
        "kit_gate": {"what": "blockkit.overlap_report with the pet's joints() (JOINT-AWARE: crossings inside a hinge "
                             "proxy are ignored)", "pairs": cp["A_pairs"], "collision_free": cp["A_collision_free"]},
        "strict_run_A2": {"what": "the same 83 pairs, each with ONLY its own parent-hinge proxy",
                          "collision_free": cp["A2_collision_free"],
                          "NOT collision-free as an A2 count": True,
                          "only_entries": cp["A2_collisions"],
                          "listed_seats": {"Arm_L|Neck1": "left shoulder ball seated on the neck side (root)",
                                           "Arm_R|Neck1": "right shoulder ball seated on the neck side (root)"}},
        "seat_depth_BU": {"rest": cp["D_depth_rest"], "max_over_all_clips": cp["D_depth_max"], "limit": 0.035},
        "min_surface_clearance_all_frames": B,
        "sensitivity": cp["C_sensitivity"]},
    "stance_r11": {"probe": "_scratch/stance_probe.py -> stance_r11.txt (r10: stance_r10.txt)", "per_clip": st},
    "paws_past_body_outline_game_cam_BU": {"L": paw["L"]["out_left_bu"], "R": paw["R"]["out_right_bu"]},
    "icons_64_128": {k: {sz: {kk: v[sz][kk] for kk in ("kit_29-58", "wide_29-60", "lemon_59-61", "fill_h", "fill_w",
                                                       "area")} for sz in ("64", "128")} for k, v in gold.items()},
    "game_icon_head_share": {"head_crown_of_icon_h": hs["head_of_icon_h"], "head_crown_of_figure_h": hs["head_of_figure_h"]},
    "kit_counter_64": {"portrait": 114, "game": 52}})
g.pop("collision_proof_r10", None)
json.dump(g, open(S + r"\gate_f85.json", "w"), indent=1)


def row(lab, k):
    a, b = gold[k]["64"], gold[k]["128"]
    return "  | %s | %d | %.3f | %d | %.3f |" % (lab, a["kit_29-58"], a["area"], b["kit_29-58"], b["area"])


def cl(key):
    v = B[key]
    return "%.3f (%s f%d)" % (v[0], v[1], v[2])


ang = st["act_molt"]["max_angle"]
TXT = """## FINAL 8.5 ROUND 11 (2026-10-28, after `_review/CinderOverlord_final85_r11.md`: model 8.3, clips 8.5) - RAISED COBRA STANCE - EXPORTED 13:51
Owner decision (binding, via the lead): **raised cobra stance**.

Backups:
- the round-10 export: `_scratch/CinderOverlord_exported_r10.py`
- this export: `_scratch/CinderOverlord_exported_r11.py`

The patches are `_scratch/fix_r11.py` (stance, nose, crown x), `fix_r11c.py` (idle) and `fix_r11d.py` (seats), plus the
constants named below.
- **MUST 1, raised cobra stance:**
  - `FRONT[4]` z 1.16 -> **1.28**, `FRONT[5]` z 1.42 -> **1.60** (`HEAD_LIFT` 0.18). The neck's top half is 0.12-0.18
    taller; Neck2 / Neck3 are longer.
  - The head group rides up 0.18 through the `HEAD_XF` offset (-0.08 -> **+0.10**). Its pivot stays the build-space
    throat (`THROAT` 1.50, where the head is modelled), so the Head joint lands on the raised FRONT[5].
    - This gives the same world result as the review's "pivot 1.68 + jaw pivot / Jaw joint +0.18", with no head, jaw
      or crown coordinate re-typed.
  - **Deviation:** `HEAD_XF` scale 1.45 -> **1.60** (review: about 1.54). At 1.54 the taller figure made the kit-portrait
    gold **102** (< 103); at 1.60 it is 114, and head + crown is **%.3f** of the figure height on the game camera.
  - **Lead decision needed: `HEIGHT` 10.5 -> 11.72 studs** (= 10.5 x 2.829 / 2.534 BU). Only the head is taller.
    Studs per BU stay as approved, so the body size, the stud pitch (0.0541) and the stride in studs are unchanged. With
    10.5 kept, the whole pet, body and slither stride included, would shrink 10 %% in game. One-line revert.
  - **Game camera, idle f0:** the gap between the head group's lowest pixel and the body's highest pixel is **%.1f px**
    (r10 **%.1f**), out of about 440 px of figure. The head and crown stand clear above the coil, with the neck as a
    stem between them.
  - **Hood trial (rejected):** I tried a cobra hood (the neck's side radius x2.1 under the head). From behind it read as a
    bulging barrel neck, not a hood, so it is not in the file (`_scratch/r11_hood_trial_rejected.png`).
- **Clips for the stance** (details in CLIP_NOTES round 11):
  - **Idle redone** as a COBRA SWAY. The r10 idle leaned the neck back 13.5 deg per breath, which dropped the head toward
    the game camera. The neck now stands upright and sways side to side; the head is held level.
  - **Walk keys unchanged.** The raised neck carries the head through the cycle at full height (gap %.1f-%.1f px, head
    pitch +/-0.6 deg), so there was nothing to redo.
  - Roar and act_molt re-checked.
- **MUST 2, flat nose cap:**
  - The skull's nose station 1.0 goes from half-height 0.032 to **0.022** (width 0.044 kept).
  - The cap ring's height factor goes from 0.80 to **0.60** (its width stays 0.80).
  - The nostril pits sit on the flatter top (`surf_hit` re-seats them).
  - From the front, the tip is now a low flat wedge with the narrow chin under it (`renders/close_front.png`, re-aimed
    0,-1.05,2.10 / 2.9 for the raised, larger head).
- **MUST 3a, crown gaps:** Crown_2 / Crown_4 x 0.150 -> **0.168**, Crown_1 / Crown_5 0.300 -> **0.310** (`CR_X1`,
  `CR_X2`). Neighbours, minimum over all four clips:
  - 1|2 %s;
  - 2|3 %s;
  - 3|4 %s;
  - 4|5 %s.
  - All are **>= 0.02**.
- **MUST 3b, seats changed (not only documented):**
  - **Shoulder:** the ball moves out onto the neck side, (+/-0.17, -0.71) -> (+/-**0.251**, **-0.765**), z 0.77.
    - Seat depth in Neck1: **%.4f** at rest, **%.4f** max over all clips (%s). The limit is 0.035; r10 was about 0.10.
  - **Chest / Neck2 caps:** the chest's end cap and Neck2's start cap (inside Neck1) go from 0.5 x r to **0.30 x r**.
    Neck2|Spine: no crossing, depth 0.
  - **Body2 / Body4 caps:** Body2's end cap and Body4's start cap (inside the Body3 bend) go from 0.45 / 0.55 x r to
    **0.30 / 0.35 x r**. Body4|Body2: no crossing in any clip, depth 0.
  - Arm|Neck2 is now %s, and Arm|Spine has depth 0.
  - **Strict run (A2): not collision-free as a count.** Its only entries are the two shoulder seats (Arm_L|Neck1 and
    Arm_R|Neck1, 4-8 triangle pairs re-shuffling around the root ring). `gate_f85.json` says this.
  - **Kit gate (A, joint-aware): collision_free true**, 83 pairs, every frame of all four clips.
- **NICE 1 / 2:**
  - The claw fan is wider (`PAW_GX` 0.042 -> 0.050).
  - The frill is longer (0.22 / 0.17 -> 0.26 / 0.21). It clears the crown by %s.
- **Paws past the body outline** on the game camera: near **%.3f**, far **%.3f** BU.
- **Clearances (proxy-free, every frame of all four clips):**
  - paws: Neck1 %s, Spine %s, Jaw %s;
  - skull: Neck2 %s;
  - jaw: Neck2 %s.
- **Numbers (kit window H 29-58):**

  | icon | gold 64 | area 64 | gold 128 | area 128 |
  |---|---|---|---|---|
%s
%s
%s
%s
%s
  - Kit counter: portrait 114, game 52. Gold >= 103: PASS (portrait_alt **%d**, kit portrait **%d**).
  - Game area **%.3f** (>= 0.18).
- **Step 1** (`_scratch/export_r11.txt`):
  - collision_free **true**; ground **-0.006**; linear 0; loops 0 / 0.
  - Tris **%d**. Stride **%.4f**: the rear body and the walk keys are unchanged, and `walk()` returns the stride from
    the segment lengths.
  - FBX `C:\\cdimp\\CinderOverlord.fbx` 13:51.
- **Renders** (title bars 13:47-13:55, "final 8.5 round 11"):
  - Game camera: `gamelook_game` / `_tq`, `_icon_game_64_128`, `_icons2_strip_64` / `_128`, and the NEW
    `_cv_idle_game` / `_cv_idle_front` (the cobra sway).
  - Portrait: `CinderOverlord_portrait_alt.png` + `_icon_alt`; `_icons_alt_strip_64` / `_128`.
  - Sheets: `close_front`, `_close_sheet`, `_model_sheet`, `_pose_tq_sheet`, `_molt_r11_front` / `_tq`,
    `_cv_roar_front` / `_side`, `_cv_walk_game` / `_side`.
  - The `mr10_*` / `_molt_r10_*` files moved to `_scratch/stale_r11_renders/`.
- **Honest read:** from behind and above, the game icon is now a crowned, maned head held clearly above the coil on a
  taller neck. It is still a vertical figure, though (the body runs away from the camera), so "dragon, not worm" at
  64 px stays the reviewer's call.

""" % (hs["head_of_figure_h"], st["idle"]["screen_f0"]["gap"], st10["idle"]["screen_f0"]["gap"],
       st["walk"]["screen"]["gap"][0], st["walk"]["screen"]["gap"][1],
       cl("Crown_1|Crown_2"), cl("Crown_2|Crown_3"), cl("Crown_3|Crown_4"), cl("Crown_4|Crown_5"),
       cp["D_depth_rest"]["Arm_L|Neck1"], cp["D_depth_max"]["Arm_L|Neck1"][1], cp["D_depth_max"]["Arm_L|Neck1"][0],
       cl("Arm_L|Neck2"), cl("SPIKES|Crown_1"),
       paw["L"]["out_left_bu"], paw["R"]["out_right_bu"],
       cl("Claw_L|Neck1"), cl("Claw_L|Spine"), cl("Claw_L|Jaw"), cl("Head|Neck2"), cl("Jaw|Neck2"),
       row("**Cinder portrait_alt**", "portrait_alt"), row("Cinder kit portrait", "kit_portrait"),
       row("Cinder game camera", "game"), row("InfernoPhoenix", "InfernoPhoenix"), row("Ivonrath", "Ivonrath"),
       gold["portrait_alt"]["64"]["kit_29-58"], gold["kit_portrait"]["64"]["kit_29-58"], gold["game"]["64"]["area"],
       ex["tris_body"], ex["export"]["meta"]["stride"])
p = D + r"\MODEL_NOTES.md"
s = io.open(p, encoding="utf-8").read()
assert "## FINAL 8.5 ROUND 11" not in s
i = s.index("## FINAL 8.5 ROUND 10")
io.open(p, "w", encoding="utf-8").write(s[:i] + TXT + s[i:])

c = io.open(D + r"\CLIP_NOTES.md", encoding="utf-8").read()
old = c[c.index("Gate run (current):"):c.index("\n\n## ")]
new = ("Gate run (current): the export run `_scratch/export_r11.txt` (round 11, 13:51: RAISED COBRA STANCE, see MODEL_NOTES;\n"
       "idle redone as a cobra sway, walk / roar / act_molt keys unchanged); single gate file `_scratch/gate_f85.json`.\n"
       "Current sheets (2026-10-28 13:47-13:55, from the round-11 file): `renders/_pose_tq_sheet.png` (26 beats),\n"
       "`_cv_idle_game.png` / `_cv_idle_front.png`, `_cv_walk_side.png` / `_cv_walk_game.png`, `_cv_roar_front.png` /\n"
       "`_cv_roar_side.png`, `_molt_r11_front.png` / `_molt_r11_tq.png`. Older sheets and frames are in\n"
       "`_scratch/stale_r6_renders/` ... `stale_r11_renders/`.")
c = c.replace(old, new)


def a(clip, b):
    v = st[clip]["max_angle"].get(b)
    return "%.2f" % v[0] if v else "0"


CT = """## FINAL 8.5 ROUND 11 (2026-10-28) - RAISED COBRA STANCE: idle redone, walk / roar / act_molt re-checked
- **Idle = COBRA SWAY** (`idle()`; refs S2 reared king cobra, C1 / C2):
  - The neck stands upright and sways side to side: roll **2.2 deg per neck bone**, one sway per 120-frame loop, plus a
    0.4 deg yaw.
  - The head follows about 5 frames later. It counter-rolls 4.4 deg, so it stays near level, and turns 3 deg into the
    sway.
  - Two breaths stay small: neck pitch 1 deg per bone, head +0.8, jaw 2.25, crown lift 2.25, paws 3.
  - The tail flick at f80 is unchanged. Events are unchanged (smoke1 0.25, flick 0.667, smoke2 0.75).
  - Why: the r10 idle leaned the neck back 13.5 deg on each breath, which brought the head toward the game camera.
    Game-camera head-to-body gap over the loop: r10 idle **%.1f-%.1f px**, r11 idle **%.1f-%.1f px**.
  - Sheets: `renders/_cv_idle_game.png`, `_cv_idle_front.png`; idle beats in `_pose_tq_sheet.png`.
- **Walk keys unchanged:** the head holds full height through the cycle (gap %.1f-%.1f px; head pitch +/-0.6 deg;
  neck bones 1.12 deg). The raised stance comes from the rest pose.
- **Pose limits, re-measured on this file** (`_scratch/stance_probe.py`, max rotation vs rest):

  | clip | neck bones (each) | head | Spine | neck pitch sum | head pitch-up (world) |
  |---|---|---|---|---|---|
  | idle | %s | %s | %s | %s | %s |
  | walk | %s | %s | %s | %s | %s |
  | roar | %s | %s | %s | %s | %s |
  | act_molt | %s | %s | %s | %s | %s |

  - Neck <= 8 per bone, chest (Spine) <= 5, head + neck pitch-up <= 30: **PASS** in all four clips.
- **Collision:**
  - Kit gate (joint-aware) **true**: 83 pairs, every frame.
  - Strict run (own hinge only): the only entries are the two shoulder seats, seat depth <= **%.4f** (limit 0.035).
  - Per-frame depths of every seated pair are in `_scratch/coll_depths_r11.json`. Neck2|Spine and Body4|Body2 have
    no crossing in any frame.
  - Crown neighbours >= 0.0307. Jaw to neck %s.
- Loops 0 / 0; stride %.4f; ground -0.006.

""" % (st10["idle"]["screen"]["gap"][0], st10["idle"]["screen"]["gap"][1], st["idle"]["screen"]["gap"][0],
       st["idle"]["screen"]["gap"][1], st["walk"]["screen"]["gap"][0], st["walk"]["screen"]["gap"][1],
       a("idle", "Neck1"), a("idle", "Head"), a("idle", "Spine"), "%.2f" % st["idle"]["max_angle"]["neck_pitch_sum"][0],
       "%.2f" % st["idle"]["max_angle"]["head_pitch_up"][1],
       a("walk", "Neck1"), a("walk", "Head"), a("walk", "Spine"), "%.2f" % st["walk"]["max_angle"]["neck_pitch_sum"][0],
       "%.2f" % st["walk"]["max_angle"]["head_pitch_up"][1],
       a("roar", "Neck1"), a("roar", "Head"), a("roar", "Spine"), "%.2f" % st["roar"]["max_angle"]["neck_pitch_sum"][0],
       "%.2f" % st["roar"]["max_angle"]["head_pitch_up"][1],
       a("act_molt", "Neck1"), a("act_molt", "Head"), a("act_molt", "Spine"),
       "%.2f" % st["act_molt"]["max_angle"]["neck_pitch_sum"][0], "%.2f" % st["act_molt"]["max_angle"]["head_pitch_up"][1],
       cp["D_depth_max"]["Arm_L|Neck1"][1], cl("Jaw|Neck2"), ex["export"]["meta"]["stride"])
assert "## FINAL 8.5 ROUND 11" not in c
j = c.index("## FINAL 8.5 ROUND 10")
c = c[:j] + CT + c[j:]
io.open(D + r"\CLIP_NOTES.md", "w", encoding="utf-8").write(c)
print("ok")
