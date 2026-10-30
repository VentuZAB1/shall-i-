
## Round 3 (clip review 3, 2026-10-27)
Every number below comes from `_scratch/verify.json`, one saved run of `_scratch/verify.py`. The step-1 JSON is in
`_scratch/full_step1.txt` and the measured footfalls are in `_scratch/footfalls.txt`.

### MUST 2: the brace
- At each strike (f30, f42, f54) the Spine drops 0.024 and pitches +1.5, and the Chest pitches 3.8 relative to the spine.
  The chest's lowest point goes 0.591 → 0.528. The neck holds the head (Neck loc +0.08 z), so the horn geometry is
  unchanged.
- The front knees fold **+29.8 deg** at the strikes and +6.7 deg on the approach (f22-27). This is the interior knee angle
  vs rest; Shin_FL and Shin_FR are the same.
- The 4-8 deg and 0.1 asks cannot both hold on this pillar leg. It stands at 98 % of its length at rest, so +8 deg of fold
  is only a 0.012 drop. I kept the chest drop, because that is what reads as a charge (see `_beats_act_side` f30 / f42 / f54).
- **Horn tip (Horn_Tip bone z):** tap1 f30 0.013, tap2 f42 0.024, tap3 f54 0.013. The horn mesh bottoms at -0.002 at
  tap1 / tap3 and 0.008 at tap2. The snout stays 0.043-0.045 above the snow.
- **ground_min_z** act -0.002; collision_free true (step 1).
- **NICE 2:** tap 2 lands a touch shallower, then drags the horn sideways (head yaw 6 deg, tip x 0 → 0.12, f42-46) while
  staying on the snow (0.008 → 0.030).

### MUST 3
- **(a) Beats:** `renders/_beats_act_side.png` and `_tq.png` now hold f16, 22, 27, 30, 39, 42, 46, 54, 58, 62, 86, 100.
- **(b) End at rest** (largest per-bone rotation): roar end vs start 0.0 and vs the bind pose 0.0; act 0.0 and 0.0.
- **(c) Chest vs spine:** this is the Chest bone's LOCAL rotation, and the Chest is parented to the Spine, so it is the
  chest-vs-spine angle. Rhino maxima: idle 0.68, walk 2.09, roar 1.0, act 3.8 (the brace).
  - The 4.4 in my gate message was the maximum across all three pets (the Yeti's act_skid), not the Rhino.
- **(d) Jaw:** the kit has no joint limits, so I defined one. `JAW_MAX = 14` is the opening the mouth covers.
  - A new MOUTH-coloured interior block rides the Jaw, hidden inside the snout when closed. With it, a 14 deg opening
    shows a dark mouth instead of the background. At 19 deg the old model showed see-through (`renders/_jaw_roar_sheet.png`).
  - The bellow pulses are now 14 deg (was 19), with 9 deg between pulses and an 11 deg hold. Jaw max: roar 14.0,
    act 8.0, idle 2.0, walk 1.5.

### MUST 4: the event convention
- Events are clip-length fractions, `round(f / n, 3)`. That is the same convention as approved, live pets: ThunderRex's
  exported Lua has `roar = {peak = 0.381, ...}`.
- The runtime (`ROBLOX PLAYBOOK/slingshot-code/ReplicatedStorage/CreatureAnimator.lua`, `_events`) fires at
  `t = frac * len` seconds. Loops use the phase, so it also covers the walk. The VFX fires on the keyed frame.

### Walk fix found while verifying
- `cm.quad_walk(gait="walk")` measured as touch-downs BL f0, FR f10, BR f20, FL f30. That is a DIAGONAL sequence, not the
  lateral one the bison / elephant plates show.
- The walk now sets its own offsets (BL 0, FL 0.75, BR 0.5, FR 0.25). Measured: BL f0, FL f10, BR f20, FR f30 = LH, LF,
  RH, RF.
- The body roll is re-phased toward the planted side, and the head dip now lands 2 f after each front touch-down.
  Slide 0.0; loop closed.

### NICE
- **1:** the idle tail flick is spread over 82-107. Its largest one-frame swing is now 15.1 deg (was 27.5).
- **3:** the bolt events fire on the tap frames (tap1-3).
- **4:** the jaw opens late (from f16) and the pale chin reads at the pulses.

### Raw collisions before the throat-hinge exemption
- The throat hinge has been in `joints()` since the model gate. Before the exemption, step 1:
  - idle: Head-Chest 25, Jaw-Chest 10, Jaw-Neck 26
  - walk: 15, 9, 8
  - roar: 35, 6, 27
  - act: 51, 62, 58
- With the hinge the count is 0, so every crossing lies within r 0.26 of the throat segment (inside the neck).

### References
- MUST 1 is pending. The central animationreference.org pull (`_review/ANIM_REFERENCES_1027.md`) has not landed yet, and
  per the lead I did not retry the browser.
