# Volt Rhino - FINAL 8.5 GATE (2026-10-28) - FIX

**Model: 7.5/10. Clips: 7.5/10. Verdict: FIX.** Both are under the 8.5 floor (owner, 2026-10-28). Higher is better, so the TO 9+ list is below the MUST list.

The motion is sound: collision-free, ground-clean, audit clean, every pose limit inside its bound, end at rest, event times in the fraction convention, and the brace and lateral walk read correctly. The model is a credible armoured rhino with a strong lime-horn hero. What holds it back is visible in the renders: the back still has tank-like seams, the chin reads as a white slab, the eye slits are too small at icon size, the legs stack as boxes, and the idle has no animationreference.org reference (an owner-rule breach) and no renders from the final rig.

**Caveat on the model score:** the model sheets, close-ups, flat palette renders and icon strips are from 10-27 14:39 to 17:31. `pets/VoltRhino.py` was last changed 10-27 23:59 and the export is 10-28 00:00 to 00:02. I scored the mesh from the pre-final sheets plus the final beat renders (head and horn unchanged visually). Item M1 must be re-rendered before this score is final.

## What I looked at
- Plan `_review/VoltRhino_plan.md` (v2, section 10 now filled); reviews 1 to 4; `GLACIER_REVIEWER_BRIEF.md`; `GLACIER_CONCEPTS.md` owner decisions; Obsidian `Model Review Checklist.md`; `FIERCE_GUIDE.md`.
- `VoltRhino/MODEL_NOTES.md`, `CLIP_NOTES.md`, `ANIM_REFS.md`; `_scratch/export_result.txt` (headless step 1 + export, 10-28 00:02).
- `pets/VoltRhino.py` (code line refs below).
- Renders: `renders/_model_sheet`, `_close_sheet`, `_icons_strip_64`, `_icons_strip_128`, `model_game`, `flat_game`, `under.png` (old), `beat_rw_side_idle_038` and `beat_rw_tq_idle_046` (old); `renders/_beats_act_final_1028_0000_side` and `_tq`; `_beats_rw_final_1028_0000_side` and `_tq`; `renders/final/pclose_side_roar_28`, `pclose_side_act_horntap_42`, `pclose_below_*`; `renders/_final_jaw_throat`; `VoltRhino_icon.png`.
- Comparison: `Raiju/renders/_model_sheet.png`, `_ALL_FIERCE_progress.png`.
- No `pose_tq_*` sheets exist for this pet; the `_beats_*` sheets are the pose sheets.

---------------------------------------------------------------------------------------------------------------------
## 1. Model score: 7.5/10

**Good:** the species reads at 64 and 128 px next to ThunderBull, Raiju, Thunderbird, Thunder Rex and StormWyvern. The horn is the hero and it reads at icon size. The back is the darkest mass and the belly is a real pale band. The face has narrow lime slits under brows (no googly eyes). Ears are dark flaps. Stud skin is off the horn, inlays, toenails and eyes. Export tris_body 12,328 (under 15k). No glow. Silhouette is distinct in the Thunder egg.

**Costs:** three ring seams across the back (game camera reads tank hoops); a white chin slab under the snout; eye slits too small to read at 64 px; legs and feet stack as boxes; the pale flanks read close to grey plastic in the close-ups.

## 2. Clip score: 7.5/10

**Good:** pose data is clean (collision_free true, ground_min_z -0.002, neck max 6.0, chest vs spine 3.8 at the brace, pitch-up 16.0, end at rest 0.0, feet z ≈ 0 at taps). Walk is a true lateral sequence (BL f0, FL f10, BR f20, FR f30, duty 0.70). Roar head lift reads with the snout forward. Act brace reads as a charge, not a bow. Snap from face-down to horn-to-sky in 6 frames reads. Event convention matches ThunderRex and CreatureAnimator.

**Costs:** idle has no animationreference.org reference and no renders from the final rig; the act's three strikes are identical dips with no impact, so at phone size they read as pecking; the roar pulses are small at 5 studs.

---------------------------------------------------------------------------------------------------------------------
## 3. MUST (to reach 8.5+)

### Model

**M1. Re-render the model gate from the final file, and regenerate the portrait (required before any PASS).**
- Re-render from `VoltRhino_rigged.blend` (00:02): `_model_sheet`, `_close_sheet`, `flat_side` / `flat_tq` / `flat_game` (new value shares; IRON_D must stay at or above 25 % of the side view), `_icons_strip_64` and `_icons_strip_128` (Volt first, then ThunderBull, Raiju, Thunderbird, ThunderRex, StormWyvern), `model_game` (600 px) and `under.png`.
- Regenerate `VoltRhino_icon.png` (dated 10-27 17:22) from the final `VoltRhino_portrait_raw.png` (10-28 00:02).
- Put the render time in each sheet title, as the owner asked for the clips.

**M2. Back: three ring seams down to two, and no full ring.** The seams are the shield edge plus two fold wedges (fold loop, lines 193-196), with the saddle and rump edges (ARMOUR, lines 83-85) on top.
- Line 194: remove `(0.405, "Spine")` from the fold loop, keeping `(-0.065, "Chest")`.
- Line 105 (`fold_wedge`, default `thick`): `0.030` to `0.014`.
- Target: `model_game` and `model_side` show the shield edge and one fold on the back, no hoop.

**M3. Chin: the white slab reads as a separate plank.** Line 217, the pale jaw `B.seg(... 0.14, 0.055, PALE, "Jaw", ...)`: radii `0.14, 0.055` to `0.10, 0.040`. In `renders/final/pclose_side_roar_28.png` and `_final_jaw_throat.png` the pale block sits under the head as a white bar. After the change it should read as the belly strip running into the chin. Keep the MOUTH interior (line 221) inside the snout when closed.

**M4. Eyes: the lime slit must read at 64 px.** Line 237 (eye loop): VOLT half `(0.008, 0.018, 0.080)` to `(0.009, 0.026, 0.092)`; BLACK socket `(0.010, 0.034, 0.094)` to `(0.011, 0.040, 0.100)`. The slit stays narrow (height / length ≈ 0.28), so it is still fierce, not round.

**M5. Legs: no stacked boxes.** In `under.png` (old) and `beat_rw_side_idle_038` (17:33) each back leg stacks thigh, shin, hock and box foot as separate tiers.
- Line 294 (back-leg hock seg, `# hock`): radii `0.115, 0.115` to `0.13, 0.105`, so the hock flows from the shin's 0.13 with no ledge at A.
- Line 301 (foot pad `(0.160, 0.165, 0.075)`, `IRON_D`): height `0.075` to `0.055`, `rnd=0.40` to `0.60`.
- Mesh only, no bone change. Re-run step 1 and confirm collision_free stays true.

### Clips

**C1. Idle has no animationreference.org reference (owner rule breach).** The rule is per animation. `ANIM_REFS.md` and plan section 10 say idle = "the bison plate ... no site clip searched for the idle".
- Search animationreference.org for one heavy animal's idle, weight shift or foreleg stamp (try `/tags/animals` or `/tags/elephants`). Cite 1 to 3 clips with frames at 24 to 30 fps in `ANIM_REFS.md` and plan section 10.
- If nothing fits, write the no-fit line (how many candidates, why) and let the owner decide a waiver. The builder and the reviewer cannot grant one.

**C2. Idle renders are stale (17:33; the final rig is 00:02).** The idle is the first clip a player sees.
- Re-render side and tq from `VoltRhino_rigged.blend` at f0, f30, f46 (stamp), f60, f90 (flick), f120.
- Check the left-fore stamp is visible at f46 and that the three other feet stay planted.

**C3. Act strike reads as pecking, not striking.** The three strikes (f30, f42, f54) are the same dip with no impact or weight release (see `TAP_P`, the act keyframe table, roughly lines 505-511).
- (a) Hold: the horn tip stays on the snow for 2 frames at each strike (f30-31, f42-43, f54-55). Horn_Tip z at or below 0.010. ground_min_z at or above -0.02.
- (b) Rebound: 3 frames after each strike (f33, f45, f57) the head pitches 4 deg up from the strike pose, and the chest eases back toward 2.0 (the brace releases). This gives the strike weight.
- (c) Vary the taps: tap 3 (f54) goes 2-3 deg deeper in head pitch than tap 1 (f30). Tap 2 (f42) stays shallower with the lateral drag (review 3 NICE 2).
- Re-check: feet z ≈ 0 at each tap, neck max at or below 8, head + neck pitch-up at or below 30.

---------------------------------------------------------------------------------------------------------------------
## 4. NICE (do these too)

- **N1 (model, richer back):** IRON_D `(92, 100, 116)` to `(76, 84, 102)` on line 16 (back, shield, folds). The game back goes to about (46, 50, 61). The darkest-back read gets stronger and the body is a richer dark. Keep IRON_D at or above 25 % side.
- **N2 (model, tame the stud highlights):** IRON `(156, 164, 178)` to `(146, 154, 168)` on line 17. The stud highlights on the light flanks read as bubble-wrap in `_close_sheet` panels 1 and 3. Luminance is about 153 (above the 95 rule); the brightest channel drops to 168, which is under the 170 line, so this is a NICE only.
- **N3 (clip, roar pulses):** at bellow1/2/3 (f20, f28, f36) add a neck pump of +2 deg with the head -2 deg (3-frame ease: f19-22, f27-30, f35-38). Head + neck pitch-up stays at 16, the neck max goes 3.5 to 5.5 (under 8), and the snout stays forward.

---------------------------------------------------------------------------------------------------------------------
## 5. TO 9+ (higher is better; these are the highest-impact extras)

- **T1 (model silhouette):** an armour ridge of three short IRON_D spikes on the spine over the saddle (`B.spike`, `nostud`, about 0.11 tall, 0.05 wide, at Spine y -0.10, 0.12 and 0.30). It gives the 64 px silhouette a crest instead of a flat top, a Raiju-level read without copying Raiju's spines.
- **T2 (model accent in game):** one VOLT bolt on the saddle top at Spine y ≈ 0.10, the same `zig()` pattern as the rump bolts (line 209), width 0.068. The game camera (`model_game`) then sees the accent on the back and the horn, not only the rump.
- **T3 (clip idle character):** a 3-frame snort at f70-73: head -2 deg and jaw +2 deg, then back. One character beat besides the stamp. No head shake (one motion, not a repeat).

---------------------------------------------------------------------------------------------------------------------
## 6. Pass / fail checklist

| # | Check | Result | Notes |
|---|---|---|---|
| 1 | Tris at or under 15k | PASS | tris_body 12,328 (export) |
| 2 | 64 px and 128 px silhouette; species reads | PASS | Rhino plus horn; lightest body in the strip |
| 3 | Hero (lime horn) at 64 px | PASS | Lime zig on the horn reads at both sizes |
| 4 | Fierce, not cute | PARTIAL | Brows and slants good; eye slits too small (M4) |
| 5 | Not a grey plastic toy | PARTIAL | Back tank seams (M2); box legs (M5); white chin slab (M3) |
| 6 | Dark back + pale underside + ONE accent | PASS | Back darkest; belly pale band; lime is the one accent family |
| 7 | Palette shares (plan gate) | NOT RE-VERIFIED | Last values 10-27 17:22 (M1). Plan gate IRON_D ≥ 25 % was 45.8 % |
| 8 | Accent strong in game colours | PARTIAL | Horn and shoulder/rump bolts read; eye slits do not (M4); T2 |
| 9 | Distinct from siblings | PASS | Only neutral body in the egg; lime 26 deg from Thunderbird (accepted) |
| 10 | Stud skin off horn, inlays, toenails, eyes | PASS | nostud on horn, zigs, toenails, eye slits |
| 11 | No glow, no Neon | PASS | export glow [] |
| 12 | Floating, poking, intersecting parts | PARTIAL | Fold seams (M2); chin slab (M3); stacked leg tiers (M5) |
| 13 | Visible from below | PARTIAL | under.png is old; legs stacked (M5) |
| 14 | Model renders match the final export | FAIL | Sheets 14:39 to 17:31 vs export 10-28 00:02 (M1) |
| 15 | Clip: collision-free, ground, audit | PASS | collision_free true; ground_min_z -0.002; linear 0; loops closed; walk slide 0 |
| 16 | Clip: pose limits | PASS | neck max 6.0; chest vs spine 3.8; pitch-up 16.0; swing 23.2 (snap) |
| 17 | Clip: ends at rest; no shakes; no spins; acts in place | PASS | end vs rest 0.0; idle yaw one slow cycle |
| 18 | Clip: events in fraction convention | PASS | stamp 0.383, bellow1 0.333, tap1 0.3, snap 0.6, charge 0.7 |
| 19 | Clip: roar readable | PARTIAL | Head lift reads; pulses small at phone size (N3) |
| 20 | Clip: act readable (strike, snap, charge) | PARTIAL | Snap and charge read; strikes lack impact (C3) |
| 21 | Clip: idle renders current | FAIL | 17:33 renders; final rig 00:02 (C2) |
| 22 | Animation refs (owner rule, per animation) | PARTIAL | Walk (#144564 + Muybridge bison), roar (W0 #174333 with source frames), act (Plate 700; kaiju-no-8 "none fits" written) cited; idle missing (C1) |

---------------------------------------------------------------------------------------------------------------------
## 7. Next steps
1. Builder: apply M2 to M5 in `pets/VoltRhino.py` (all mesh-only except M5's hock line, which is still mesh-only). Re-run step 1 and export.
2. Builder: C1 (animationreference.org idle ref, or the no-fit line for the owner). C3 (act strike: hold, rebound, tap variety) and C2 (idle re-render).
3. Builder: M1 (full re-render of the model gate plus the regenerated portrait icon).
4. Send to the final reviewer, all at once: `_model_sheet`, `_close_sheet`, `_icons_strip_64/128`, `flat_side/tq/game`, `model_game`, `under.png`, the idle beats (side and tq), the act beats (f30, f42, f54 and the rebound frames), the roar beats, and the updated `ANIM_REFS.md` idle row.
5. Ship bar: model at or above 8.5 and clips at or above 8.5. TO 9+ if time allows.
