import json, time, io
D = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\CinderOverlord"
S = D + r"\_scratch"


def hr(path, tag="HEADLESS_RESULT"):
    s = open(path, encoding="utf-8", errors="replace").read()
    return json.loads(s.split(tag, 1)[1].strip().splitlines()[0])


ex = hr(S + r"\export_r10.txt")
cp = hr(S + r"\coll_probe_r10.txt", "COLLPROBE")
paw = hr(S + r"\pawpx_r10.txt", "PAWPX")
gold = json.load(open(S + r"\gold_r10.json"))
hs = json.loads(open(S + r"\headshare_r10.txt").read().split(" ", 1)[1])
g = json.load(open(S + r"\gate_f85.json"))
g.update({
    "written": time.strftime("%Y-%m-%d %H:%M"),
    "round": "final 8.5 round 10 (_review/CinderOverlord_final85_r10.md + coordinator); the ONLY gate file",
    "export": {"fbx": r"C:\cdimp\CinderOverlord.fbx", "run": "_scratch/export_r10.txt",
               "meta_stride_BU_per_48f": round(ex["export"]["meta"]["stride"], 4)},
    "step1": {"collision_free": ex["collision_free"], "pairs": cp["A_pairs"], "ground_min_z": ex["ground_min_z"],
              "audit": ex["audit"], "tris": ex["tris_body"], "lua_bytes": ex["lua_bytes"], "events": ex["events"]},
    "collision_proof_r10": {"probe": "_scratch/coll_probe.py -> coll_probe_r10.txt",
                            "kit_gate_83_pairs_collision_free": cp["A_collision_free"],
                            "min_surface_clearance_all_frames": cp["B_min_clearance"],
                            "rest_clearance": cp["B_rest"],
                            "own_hinge_only_run": cp["A2_collisions"],
                            "sensitivity": cp["C_sensitivity"]},
    "paws_past_body_outline_game_cam_BU": {"L": paw["L"]["out_left_bu"], "R": paw["R"]["out_right_bu"]},
    "icons_64_128": {k: {sz: {kk: v[sz][kk] for kk in ("kit_29-58", "wide_29-60", "lemon_59-61", "fill_h", "fill_w",
                                                       "area")} for sz in ("64", "128")} for k, v in gold.items()},
    "game_icon_head_share": {"head_crown_of_icon_h": hs["head_of_icon_h"], "head_crown_of_figure_h": hs["head_of_figure_h"]},
    "kit_counter_64": {"portrait": 104, "game": 45}})
json.dump(g, open(S + r"\gate_f85.json", "w"), indent=1)


def row(lab, k):
    a, b = gold[k]["64"], gold[k]["128"]
    return "  | %s | %d | %.3f | %d | %.3f |" % (lab, a["kit_29-58"], a["area"], b["kit_29-58"], b["area"])


B = cp["B_min_clearance"]


def cl(key):
    v = B[key]
    return "%.3f (%s f%d)" % (v[0], v[1], v[2])


TXT = """## FINAL 8.5 ROUND 10 (2026-10-28, after `_review/CinderOverlord_final85_r10.md`: model 8.3, clips 8.5) - EXPORTED 13:14
Backups:
- the round-9 export: `_scratch/CinderOverlord_exported_r9.py`
- this export: `_scratch/CinderOverlord_exported_r10.py`

The patch is `_scratch/fix_r10.py`, plus the follow-ups below. Items 3 / 2 / 1 of the round, in the lead's order.
- **MUST 3, collision proof** (details in CLIP_NOTES round 10):
  - **The proxies are exclusion zones, not sensors.** In `blockkit.overlap_report`, a crossing whose points ALL lie
    within r of any `joints()` segment counts as a hinge sliver and is IGNORED. So the review's extra proxies (paw r
    0.07, skull side r 0.12) would hide crossings at the paws and the skull sides, not check them.
    - Injection test: the left paw pushed 0.16 / 0.22 BU into the neck gives 51 / 89 crossings with no proxies, and
      **0** with the pet's joints or with the review's extra proxies. The cause is the Neck1 hinge sphere (r 0.34),
      which covers that spot.
    - So no exclusion proxy was added at the paws or the skull.
  - **Instead, three checks:**
    - (a) The kit gate now runs **83 pairs** (was 64). New: paws and arms vs Spine / Body1 / Neck2; Head and Jaw vs
      Neck1; all five crown blades vs the Head group (skull, cheek spikes, frill). Result: **collision_free true** in
      all four clips, every frame.
    - (b) Proxy-free **minimum surface clearance**, every frame of all four clips:
      - paws: Neck1 %s, Spine %s, Neck2 %s, Jaw %s, Head %s;
      - skull: Neck1 %s, Neck2 %s, arms %s;
      - jaw: Neck2 %s (roar, jaw open);
      - frill + cheek spikes: crown blades %s, Neck2 / Neck3 %s.
      - All are **>= 0.02**.
    - (c) A run with only each pair's own hinge proxy. This found the centre crown blade's gold side frames grazing
      the neighbour sockets (molt f22). Fixed: the frames start 0.033 above the blade foot (inside the mount, not
      visible). Crown 2|3 is now %s.
      - What (c) still shows:
        - Seated contacts that exist at rest and stay in place (crossing box moves <= 0.035): the shoulder roots in
          Neck1 / Neck2 (their Neck2 / Spine crossings are 60-81 %% buried inside Neck1), and the Spine / Neck2
          junction at the neck base.
        - One motion-only contact: the overlap ends of Body2 and Body4 meet on the inner side of the Body3 bend
          (walk f19 / f26, molt f82; partly buried in Body3). It is unchanged since the round-6 coil, and the kit
          treats it as a joint sliver. `_scratch/b3_bend.png`: f19 / f26 look the same as f12, which has none.
      - None of these involve the paws, the skull, the jaw or the frill.
  - The kit's Crown_3 proxy is now a hinge segment along its 0.2-wide socket (was a point). That gate saw the
    seated socket as "new" crossings once Crown_3 vs Head was checked. Every Crown_3 x Head crossing, rest and all
    clips, lies inside the mount block (x +/-0.102, y -0.628..-0.536, z 1.809..1.871).
- **MUST 2, jaw taper:**
  - The jaw tip goes from 0.046 / 0.020 to **0.034 / 0.016** (under the nose tip's 0.044). The 0.85 station goes from
    0.098 to **0.078** (rh 0.032 kept).
  - The lower fangs move in from x 0.075 to 0.064, so they stay on the narrower rim.
  - Front ray-cast (`_scratch/face_id.py`, close_front camera): the jaw's visible width is now 0.267 BU at most (was
    0.284). Going down, the face outline only narrows (0.40 -> 0.38 -> 0.37 -> 0.25 -> 0.23).
  - Caveat: the round red snout cap with its two nostrils is unchanged (not in the list). If the reviewer still reads a
    nose bulb, the next lever is that cap.
- **MUST 1a, paws:**
  - Paw box (0.052, 0.046, 0.042) -> **(0.070, 0.062, 0.056)**. Claws 0.075 / 0.015 -> **0.110 / 0.020**, spaced 0.042.
  - The arm segments are a touch thicker. The hand moves to x +/-**0.39**, the elbow to +/-**0.42**.
  - On the `gamelook_game` camera (`_scratch/paw_px.py`), past the body outline:
    - near paw (L) **%.3f BU**;
    - far paw (R) **%.3f BU**.
    - Both are >= 0.10.
- **MUST 1b, skull frill:** one swept-back obsidian pair per side on the rear skull, above the cheek spikes.
  - Built with the same `B.spike(..., OBS_D, "Head", top=(0.12, 0.35))` call. At build scale (`FRILL` in the file):
    - base (0.150, -0.470, 1.790), dir (0.80, 0.56, 0.28), L 0.22, w 0.050;
    - base (0.165, -0.465, 1.715), dir (0.86, 0.50, 0.04), L 0.17, w 0.045.
    - That is about 35 deg swept back from the side.
  - In world units the tips reach |x| **0.538** against the skull side's 0.334, so **+0.20 BU** past the skull (top
    view).
  - They clear the crown blades by %s.
  - Read: a dark spiked mane around the head, in the portrait icons and from the game camera.
- **Keeps:**
  - HEAD_XF 1.45; head + crown **%.3f** of the figure height on the game camera; stride **%.4f**.
  - Gold >= 103: PASS (portrait_alt **%d**; kit counter portrait 104 / game 45). The frill and paws widen the figure,
    so the icon scales down a little (r9: 135 / 110 / 47).
- **Numbers (kit window H 29-58):**

  | icon | gold 64 | area 64 | gold 128 | area 128 |
  |---|---|---|---|---|
%s
%s
%s
%s
%s
  - Game-camera area **%.3f** (>= 0.18).
- **Step 1** (`_scratch/export_r10.txt`):
  - collision_free **true**; ground -0.006; linear 0; loops 0 / 0.
  - Tris **%d**; stride **%.4f**.
  - FBX `C:\\cdimp\\CinderOverlord.fbx` 13:14.
- **Renders** (title bars 13:15-13:19, "final 8.5 round 10"):
  - Game camera: `gamelook_game` / `_tq`, `_icon_game_64_128`, `_icons2_strip_64` / `_128`.
  - Portrait: `CinderOverlord_portrait_alt.png` + `_icon_alt`; `_icons_alt_strip_64` / `_128`.
  - Sheets: `close_front`, `_close_sheet`, `_model_sheet`, `_molt_r10_front` / `_tq`, `_cv_roar_front` / `_side`,
    `_cv_walk_game` / `_side`, `_pose_tq_sheet`.
  - The `mr9_*` / `_molt_r9_*` files moved to `_scratch/stale_r10_renders/`.
- **Not done (TO 9+):** the tail-tip crop in the walk tile, a standing Index pose, a flank accent, and
  `_review/GLACIER_CONCEPTS.md` lines 46 / 116. That last file is outside the files this builder may edit.

""" % (cl("Claw_L|Neck1"), cl("Claw_L|Spine"), cl("Claw_L|Neck2"), cl("Claw_L|Jaw"), cl("Claw_L|Head"),
       cl("Head|Neck1"), cl("Head|Neck2"), cl("Head|Arm_L"), cl("Jaw|Neck2"), cl("SPIKES|Crown_1"),
       cl("SPIKES|Neck3"), cl("Crown_2|Crown_3"),
       paw["L"]["out_left_bu"], paw["R"]["out_right_bu"], cl("SPIKES|Crown_1"),
       hs["head_of_figure_h"], ex["export"]["meta"]["stride"], gold["portrait_alt"]["64"]["kit_29-58"],
       row("**Cinder portrait_alt**", "portrait_alt"), row("Cinder kit portrait", "kit_portrait"),
       row("Cinder game camera", "game"), row("InfernoPhoenix", "InfernoPhoenix"), row("Ivonrath", "Ivonrath"),
       gold["game"]["64"]["area"], ex["tris_body"], ex["export"]["meta"]["stride"])
p = D + r"\MODEL_NOTES.md"
s = io.open(p, encoding="utf-8").read()
assert "## FINAL 8.5 ROUND 10" not in s
i = s.index("## FINAL 8.5 ROUND 9")
io.open(p, "w", encoding="utf-8").write(s[:i] + TXT + s[i:])
c = io.open(D + r"\CLIP_NOTES.md", encoding="utf-8").read()
old = c[c.index("Gate run (current):"):c.index("\n\n## ")]
new = ("Gate run (current): the export run `_scratch/export_r10.txt` (round 10, 13:14: see MODEL_NOTES; the clip keys are\n"
       "unchanged; bigger paws, a skull frill, a narrower chin); single gate file `_scratch/gate_f85.json`.\n"
       "Current sheets (2026-10-28 13:15-13:19, from the round-10 file): `renders/_pose_tq_sheet.png` (26 beats),\n"
       "`_cv_walk_side.png` / `_cv_walk_game.png`, `_cv_roar_front.png` / `_cv_roar_side.png`, `_molt_r10_front.png` /\n"
       "`_molt_r10_tq.png`. Older sheets and frames are in `_scratch/stale_r6_renders/` ... `stale_r10_renders/`.")
c = c.replace(old, new)
SC = cp["C_sensitivity"]
CT = """## FINAL 8.5 ROUND 10 (2026-10-28) - MUST 3 collision proof (`_scratch/coll_probe.py` -> `coll_probe_r10.txt`)
- **How the kit check works** (`blockkit.overlap_report`):
  - Mesh triangles of two bone groups are tested for crossings.
  - Contacts already present at rest are ignored.
  - A crossing whose points all lie within r of any `joints()` segment counts as a hinge sliver and is IGNORED.
  - So a proxy hides crossings; it does not add a check.
- **Injection test** (idle f0, pose set by hand):

  | test | no proxies | pet joints | + review's extra proxies |
  |---|---|---|---|
  | left paw 0.16 into Neck1 | %d | %d | %d |
  | left paw 0.22 into Neck1 | %d | %d | %d |
  | Crown_5 swung down 60 deg | %d | %d | %d |
  | Crown_5 swung down 100 deg | %d | %d | %d |

  - The paw spot is inside the Neck1 hinge sphere (r 0.34). That is why I prove the paws and the skull by surface
    clearance, not by more proxies.
- **Kit gate:** 83 pairs (+19: paws / arms vs Spine, Body1, Neck2; Head / Jaw vs Neck1; Crown_1..5 vs Head).
  collision_free **true**, every frame of idle, walk, roar and act_molt.
- **Proxy-free minimum surface clearance**, every frame of the four clips (BU):
  - Paws: %s.
  - Skull / jaw / frill: %s.
  - Crown neighbours: %s.
  - Every paw, skull, jaw and frill pair is >= 0.02.
- **Arm root vs Neck2 = 0.000:** the shoulder ball is rooted in the neck at rest (0.005 at rest). Its crossing box
  stays where it is at rest, inside Neck1.
- **Fixed this round:** the centre crown's side gold frames started 0.012 below the blade foot and grazed blades 2 / 4
  in the molt (proxy-free run). They now start 0.033 above it.
- **Clip keys:** unchanged; loops 0 / 0; stride 5.0089.

""" % (SC["paw_in_0.16"]["no_proxies"], SC["paw_in_0.16"]["pet_joints"], SC["paw_in_0.16"]["plus_paw_proxies"],
       SC["paw_in_0.22"]["no_proxies"], SC["paw_in_0.22"]["pet_joints"], SC["paw_in_0.22"]["plus_paw_proxies"],
       SC["crown5_down_60"]["no_proxies"], SC["crown5_down_60"]["pet_joints"], SC["crown5_down_60"]["plus_skull_proxies"],
       SC["crown5_down_100"]["no_proxies"], SC["crown5_down_100"]["pet_joints"], SC["crown5_down_100"]["plus_skull_proxies"],
       ", ".join("%s %s" % (k.split("|")[1], cl(k)) for k in ("Claw_L|Neck1", "Claw_L|Neck2", "Claw_L|Spine", "Claw_L|Body1",
                                                              "Claw_L|Jaw", "Claw_L|Head", "Claw_L|Claw_R")),
       ", ".join("%s %s" % (k, cl(k)) for k in ("Head|Neck1", "Head|Neck2", "Head|Arm_L", "Jaw|Neck2", "SPIKES|Crown_1",
                                                "SPIKES|Crown_2", "SPIKES|Neck2", "SPIKES|Neck3")),
       ", ".join("%s %s" % (k, cl(k)) for k in ("Crown_1|Crown_2", "Crown_2|Crown_3", "Crown_3|Crown_4", "Crown_4|Crown_5")))
assert "## FINAL 8.5 ROUND 10" not in c
j = c.index("## FINAL 8.5 ROUND 2")
c = c[:j] + CT + c[j:]
io.open(D + r"\CLIP_NOTES.md", "w", encoding="utf-8").write(c)
print("ok")
