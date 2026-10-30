# Thunderbird - art director review 3 (2026-10-14) - APPROVED (model + clips), with one 1-line fix before export

**Score: 8/10 for a 5% pet** (v1 4/10, v2 6.5/10). It now clearly beats the three Storm-egg commons and sits just below
Thunder Rex (8.5, secret):
- a real bald-eagle silhouette from every camera
- a dark storm cloak from behind, with the bolt-edged wings and white fan carrying the read
- its own teal identity in the egg
- an eagle-only signature (the stoop)

All review-2 fixes landed, and the clip set is complete and clean. **Ship it after the walk ground fix (fix 1).**
Everything else below is optional polish.

What I looked at:
- `pets/Thunderbird.py` v3 (model, rig, joints, all 7 clips)
- `_r3_pose_tq/side/game_sheet`, plus the single game and side frames of fly (0/7/14/21) and the stoop
  (20/28/31/32/33/34/46)
- `_model_sheet`, `_close_sheet`, `_knee_strip` and the pclose_* frames
- `_icons_strip_64/128`

My independent checks: a headless rebuild of your spec with outputs only in
`C:\Users\ventu\AppData\Local\Temp\tb_review3\`; no project file touched.
- Full clip build, audit and overlap at step 1 with three knee-capsule variants.
- **ground_min_z sampled on every frame.** `headless_clips` samples every 2nd frame.
- Worst-frame knee renders (`knees.png`), a face close-up and the fold views (`face_fold.png`).

---------------------------------------------------------------------------------------------------------------------
## 1. Model: review-2 fixes, all landed
| # | fix | result |
|---|---|---|
| 1 | shoulder blocks removed, WDX 0.07, FOLD (86,10,-80,0) | landed. Game cam: the wings hug, the hands no longer flare. |
| 2 | STORM dorsal saddle | landed. The shark teeth are gone; the mantle is tonal texture. |
| 3 | arm bar teal → storm split | landed. The rails are gone; short teal shoulder patches remain. |
| 4 | eye (lid-heavy, no pupil), brow back 0.014, hook 0.09, crest 16-22°/x3 | landed. Fierce narrow eye; the crest is a swept tuft from the front, no longer a crown. |
| 5 | withers fin | landed. The top mantle row is now a single centre shingle at z 0.18; no fin in the side view. |
| 6 | trousers | landed. Narrower, top flare removed, 7-feather mirrored cuff that never splays inward. |
| 7 | tail cup | landed, at +0.05 and spread 34 (I asked for +0.10 / 38). The front-view bar is gone, so I accept it. |
| 8 | deliverables | 600 px model sheet and both icon strips present. |
| 9 | env constants | landed. No `os.environ` reads remain. |

**Your round-3 model changes, all accepted:**
- **Flank blades** (one STORM row hung at x 0.225, outside the trouser swing band).
- **Belly keel** (bottom taper 0.22). From the front, the legs come out of the body feathers.
- **Trouser top and cuff.**

  These hide the knee in every pose I rendered. The blades read a little like flat cards in an extreme side close-up,
  but they are invisible at game distance.

**Ruling on the knee capsule: accepted as a hinge region, and please tighten it** (fix 2). I rebuilt every clip
three ways:

| knee capsule | collisions (all 7 clips, step 1) |
|---|---|
| yours: K-0.10d → K+0.20d, r 0.13 | 0 |
| **tighter: K-0.08d → K+0.15d, r 0.11** | **0** |
| none | Shin vs Spine only, 37-107 tri-pairs: idle f21/41, walk f9/24, takeoff f10, land f13, roar f6/7, stoop f32 |

I rendered every one of the "none" worst frames from side, front and back (`knees.png`). In each case the crossing is
the trouser top passing **inside** the belly, which is the designed "leg out of the body feathers" region. Nothing
pokes out through the flank, the blades or the keel. So it is a legitimate hinge mask. The tighter version is just as
clean, though, and it keeps the lower half of the trouser and the cuff fully checked against the blades, the tail and
the other leg.

**Palette** (your flat game-cam shares match my test build):
- STORM+PRI 44.6 / TEAL+COV 14.4 / WHITE 22.2 / BOLT+HOT 15.3 / GOLD 1.1
- Largest single colour: STORM 30.3
- PASS. The teal lives on the breast, front and shoulders (tq icon), and the back reads dark storm with lightning
  edges.

**64 / 128 px strip:** PASS. It is the teal eagle of the egg: white head, gold beak, heavy-lidded eye, dark wing,
yellow bolts. Clearly distinct from Rex, Wyvern, Griffin and Raiju. Keep idle f0 as the portrait pose.

---------------------------------------------------------------------------------------------------------------------
## 2. Clips (30 fps): all approved
My rebuild agrees with your pass:
- `collision_free` with 0 pairs in all 7 clips
- audit linear 0
- idle/walk/fly loops closed
- walk slide 0, foot_z_var 0
- 10,500 tris

| clip | verdict | notes |
|---|---|---|
| **idle** 132 | APPROVED | The look-around is fixed: ≤ 28° in 4 f, holds L/R, no whip. The hunting stare (f58-78, dead still) is the best beat. Wing breath goes through LIFT1 → BREATH → LIFT1 → FOLD. Talon re-grips at f18-24 and f38-44. The downward tail pump is the right call against the folded wingtips. |
| **walk** 28 | APPROVED (fix 1) | Rolling strut, gyro head (75% cancel), asymmetric contact dip, the passing foot swings wide of the keel, wing ripple toward LIFT1 on contacts. **ground_min_z -0.0203 at f26** (every-frame sample), 0.0003 past the -0.02 rule. |
| **fly** 28 | APPROVED | The body is horizontal at FPITCH 40 on the 46-52° rest body, the head is level and the beak forward. The body rises on the downstroke and the tail steers. From behind, the feet hang open under the fan, which reads as real raptor flight (optional tuck, fix 5). |
| **takeoff** 30 | APPROVED | FOLD → LIFT1 (f3) → LIFT2 (f6) → LIFT3 (f8) → LIFT4 (f9) → stroke top f10, LAUNCH f11. Crouch -0.12. Push, then tuck. |
| **land** 32 | APPROVED | Brake with the wings swept forward, open talons thrown forward (f10-15), TOUCH f17, absorb holding the raised V (f17-22), then fold LIFT4 → LIFT1 → FOLD. Matches the brief. |
| **roar** 70 | APPROVED | SKY SCREECH: gather → rear → raised V at f14, two thunder beats with body lift at f23/f35, a jaw buzz that keeps the head still, fold via LIFT3-1. From the game camera the V plus the lightning edges is the money shot. |
| **act_stoop** 84 | APPROVED | Matches the table: lock-on crouch, launch f14, hover with one beat (f18-21), STOOP (f24-30, the wings snap LIFT4 → FOLD one key per frame, 25° nose-down teardrop), throw and flare (f31-34 FOLD → LIFT1-3 → V), STRIKE f33, chest shudder (not the head), scream f46-58, talon release f57-60, two hop-steps back. Unique in the roster. |

Events are all present and on the right frames:
- takeoff `launch`
- land `touch`
- roar `screech` / `beat1` / `beat2`
- act_stoop `launch` / `strike` / `scream`

**Naming:** the act is now `act_stoop`, not `act_talonstrike`. Make sure the Studio side (CreatureClips / pet config /
VFX hooks) uses `act_stoop`.

---------------------------------------------------------------------------------------------------------------------
## 3. Fixes
**Before export (required, one line):**
1. **Walk ground.** ground_min_z is -0.0203 at walk f26 (Foot_L talon). Raise the walk's planted target by 0.001,
   either with `FOOT_LIFT = 0.013` or with `+0.001` in `strut()`, so every clip is ≥ -0.02 on every frame. Re-run the
   step-1 pass.

**Recommended (do now if cheap; not blocking):**

2. **Tighten the knee capsule** in `joints()` to `(K - d*0.08) → (K + d*0.15), r 0.11`. Verified 0 hits on all 7
   clips (table above).
3. **Brow, side view.** It still juts out as a pale WHITE_D block above the eye (`face_fold.png`, side). Taper its
   front, `top=(0.8, 0.85)`, or move it back another 0.01. From the front and in tq it already reads right.
4. **Stoop drama from the game camera.** The hover peak is 0.30 (about 1.4 studs at x1). Raising it to **0.40**
   (f18/21 keys, then let `lift_air_frames` and the stoop keys follow) makes the dive read better from behind. Re-check
   collisions and ground afterwards.

**Optional polish:**

5. **Fly:** THI 70 → ~76, so the open feet sit closer under the fan from the game camera.
6. **Idle:** add a 6-frame hold at centre between the left and right looks (f32-38, then shift the R keys +6). The
   L → R swing is currently one continuous 56° move over 10 frames. It isn't a whip, but a hold reads more "bird".
7. **Housekeeping:** stale comments.
   - The header (L3) and `model()` (L197) still mention "flight-muscle shoulders".
   - The FOLD comment says "wing root x 0.35, tail fan ±38". It is now 0.27 / ±34.

---------------------------------------------------------------------------------------------------------------------
## 4. Summary for the coordinator
- **APPROVED: model + all 7 clips, 8/10 for a 5% pet.** Apply fix 1 (one line), re-run the step-1 pass, then export
  (`headless_full … - 1 export` → `C:\cdimp\Thunderbird.fbx`). Fixes 2-4 are recommended but not required; 5-7 are
  optional.
- **Owner to-do** (as for all pets):
  - Studio import as creator **ZAB Studio**.
  - Index icon from idle f0 (`icon3.py`).
  - **VFX Studio** effects on the anchors **WingBolt_L/R, TailBolt, Crest, Beak, Strike**, driven by the events:
    sparks along the wing edges, a lightning flash on roar `beat1` / `beat2`, a bolt plus ground scorch on stoop
    `strike`, a small crest crackle. No aura (the secrets' language).
  - Add it to the Storm egg as the 5% normal.
  - Save + Publish.
- Colours render ~0.6x darker in Roblox. STORM will go near-black in shadow, so the bolt tips and the white head/tail
  carry the in-game read. That is intended; the VFX on WingBolt / TailBolt make it pop.
