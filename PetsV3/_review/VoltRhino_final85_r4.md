# Volt Rhino - FINAL 8.5 GATE, ROUND 4 (2026-10-28) - PASS

**Model: 8.5/10 - PASS. Clips: 8.6/10 - PASS.**

Both are at or above the 8.5 floor. The round-3 blockers are closed: the chin plank is gone, the eye shows at 64 px as a lime mark (not a slit yet), the idle stamp reads at phone scale, and the feet are re-logged on the final save. The model sits exactly on the floor. The TO 9+ list is where the extra points are.

## What I looked at
- Brief; round-3 verdict; `MODEL_NOTES.md` and `CLIP_NOTES.md` ("Final gate round 3" sections); `_scratch/feet_taps_f85r3.txt` (probe 05:11:31 on the 05:09:54 save); `_scratch/verify.json` (05:11); `_scratch/export_result_f85r3.txt` (05:11: tris_body 14,532, height 8.69, ground_min_z, collision_free true); `pets/VoltRhino.py` (read only: lines 25-29, 312-344, 383, 532-543, 612-617, 639-653); the approved plan `_review/VoltRhino_plan.md` (palette, eye spec, tier).
- Renders, newest set (05:10-05:12): `under.png`, `closeb_cbelow.png`, `closeb_cside2.png`, `pclose_below_roar_28.png`, `pclose_side_roar_28.png`, `close_side.png`, `close_tq.png`, `close_front.png`, `_chin_sheet.png`, `_close_sheet.png`, `_model_sheet.png`, `_icons_strip_64.png`, `_icons_strip_128.png`, `_icons_sheet.png`, `VoltRhino_icon.png`, `_idle_stamp.png`, `beat_f85r3_idle_side_idle_030/038/046.png`, `_beats_f85r3_idle_side.png`, `_beats_f85r3_idle_tq.png`.
- NOT from the newest set: the act and walk/roar beat sheets (`_beats_act_final_1028_0000_*`, `_beats_rw_final_1028_0000_*`, both 00:00). They predate the 05:09 save. I used them for motion only (see the ship check).
- Read-only pixel checks (nothing written to the project): lime connected components in both icon strips; near-white and brightness in the chin close-ups and `under.png`; the lowest dark row of the near front foot in the 360 px idle frames. The visual reads come from the displayed images; the numbers are measured from the PNGs.
- Number check: the brief's "tris 14,352" is the 05:05 step-1 log. The 05:11 export and MODEL_NOTES both say 14,532. Both are under the 15k cap.

---------------------------------------------------------------------------------------------------------------------
## 1. Model score: 8.5/10 - PASS
What works:
- The silhouette reads at 128 px and at 64 px: a dark-backed rhino, an ivory horn with a lime zig, the studded hide and the pale belly. The palette follows the plan. Builder's flat shares: IRON_D 43.4 % side (gate 25 %), VOLT 4.6 %, PALE 8.3 % (plan 10 %).
- The chin is fixed (MUST 1). The face no longer has a light plank.
- The eye is a lime mark at 64 px (MUST 2 acceptance met, see section 3).

What keeps it at 8.5 and not higher:
- The eye at 64 px is a 6 px lime dash on a mid-grey face. The black socket does not resolve, so it reads as a speck, not a fierce slit (TO 9+ T1).
- The open jaw in the roar is a hard-edged maroon wedge with a flat floor and a squared front corner (T4).
- At 64 px the Volt is the greyest Thunder icon in the row, and its lime signature is thin (T2, owner call).
- The head is a round tube capped by a flat dark nose plate. In side view it reads a little like a sausage (T3).

---------------------------------------------------------------------------------------------------------------------
## 2. Clip score: 8.6/10 - PASS
What works:
- MUST 3 is met: the idle stamp reads at phone scale (numbers in section 3).
- Feet at the taps: soles at 0.000 at f30, f42 and f54 on all four feet. Horn_Tip 0.008 / 0.008 / 0.004.
- Every limit is inside the gate: neck max idle 2.06 / walk 2.48 / roar 6.5 / act 6.0 (limit 8); chest vs spine 0.72 / 2.09 / 1.0 / 3.8 (limit 5); head + neck pitch-up roar 16.0, act 16.0 (limit 30); one-shots end at rest 0.0; ground_min_z idle 0.000, walk -0.002, roar 0.000, act -0.008; loops closed; walk slide 0; idle foot drift 0; collision_free true.

What keeps it at 8.6:
- The idle snort (6 deg) is faint on a 360 px frame (T5).
- The roar's 3 deg neck pump reads small on screen (T6).
- The act head snap (f56-62) peaks at 26.7 deg per frame on the horn-tip bone. It reads as a snap, not a shake, but it is the sharpest move in the set (T7).
- Verification gap: the act and roar frames were not re-rendered after the 05:09 model save. The chin, nose cap and eye changed after 00:00. The motion numbers and the feet probe were re-run on the final save, so the visual risk is low (see the ship check).

---------------------------------------------------------------------------------------------------------------------
## 3. Round-3 items

**MUST 1, chin plank and white snout tip: PASS.**
- The Jaw chin seg is gone (old line 286). The MOUTH interior on the Jaw stays (lines 312-316). In `pclose_below_roar_28` the open jaw shows a dark maroon mouth, not a pale plank.
- `under.png`: the brightest pixel in the head-underside box (x 110-270, y 190-280) is the sky colour (201,215,235). No light plane sits under the head.
- `closeb_cbelow`: the throat spindle (x 255-335, y 320-380) is grey-blue, peak (181,197,218), with soft tapered ends and no straight hard edge.
- `closeb_cside2`: the solid white line is gone. The front edge of the dark nose cap peaks at (244,255,255) at x 89-90, y 200-219, then sits at 229-240 down to y 280. That is a 1-2 px sheen on a dark cap, not a white line (T3 tidies it).

**MUST 2, eye slit visible at 64 px: PASS on the stated acceptance. Legibility is PARTIAL.**
- The values are as specified (line 344: BLACK (0.011, 0.048, 0.118), VOLT (0.009, 0.036, 0.110)). `close_side` and `close_tq` show a long lime slit with a black lower edge.
- `_icons_strip_64` at 1:1 (Volt first): a lime line of 6 px (diagonal, x 30-32, y 37-40) on the head side. That is the eye: by scale it matches the eye wedge in `VoltRhino_icon.png`. The builder reported 8 px; I count 6. Round 3 was about 1 px, so this is a clear gain.
- The black socket does not resolve around it at 64 px. The neighbouring pixels are mid-grey (about 5e7353 to 8c98b5). BLACK sits only 0.004 proud (line 344), which is below one icon pixel.
- At 128 px the slit is clear (about 4 px thick, 8 px long).

**MUST 3, idle foot stamp readable: PASS.**
- Lift 0.120 over the f30-46 window (stamp event f46 kept). At 360 px the near front sole's lowest dark row is 271 at f30, 260 at f38 (11 px higher) and 271 at f46. The builder reported 11-12 px. This meets the brief's "at least 10 px".
- `_idle_stamp.png` and `_beats_f85r3_idle_side.png`: the front foot is clearly up at f34-38 and back down by f46.
- The other feet stay planted (idle_foot_drift 0).

**MUST 4, process (feet re-log, icon from the final portrait): PASS.**
- `feet_taps_f85r3.txt` is the probe at 05:11:31 on the 05:09:54 save: soles 0.000 at f30/42/54; Horn_Tip 0.008 / 0.008 / 0.004.
- `VoltRhino_icon.png` and both strips are 05:11, newer than the 05:09 save; the portrait is 05:11.

**Round-3 9+ items (T1-T4 from r3):**
- T1 snort: PARTIAL. Numbers are right (6 deg up at f71-72, settles past rest at f76; SNORT line 532, head line 543). The head lift is still faint on the 360 px idle beat (see T5).
- T2 roar pump: PARTIAL. The 3 deg pump is present (lines 612-617) but reads small (T6).
- T3 pale throat collar as a bib: PASS. The throat in `pclose_below_roar_28` is a soft grey spindle, not a white ring.
- T4 act taps 1 and 3 look alike: NOT ADDRESSED. No tap-1 yaw was added in the round-4 notes (T8).

---------------------------------------------------------------------------------------------------------------------
## 4. New MUSTs (blocking 8.5)
None. Nothing in the round-4 evidence drops below 8.5 on either score.

**Ship check (not a score item, do before the owner sees it):**
- Re-render the act (f30, f42, f54) and roar (f28, side and below) frames from the 05:11 save. The current act/roar beat sheets are from 00:00. Check the snout tip and nose cap against the brisket at f54. The raw collision counts (Head|Chest 80 frames, Jaw|Chest 28 frames in `verify.json`) are hidden by the 0.26 throat hinge. The 00:00 check (`_final_jaw_throat.png`) showed no poke-through, so this is confirmation only.

---------------------------------------------------------------------------------------------------------------------
## 5. TO 9+ (ordered by impact; higher is better)

- **T1 (eye, 64 px):** make the black socket show. Widen BLACK on line 344 so about one 64-px pixel (about 0.03 units) of black sits past the lime on each long side. Starting point: BLACK half-size (0.036, 0.060, 0.130); VOLT stays (0.009, 0.036, 0.110). Accept when, at 1:1 in `_icons_strip_64`, dark pixels border the lime on both long sides and the lime stays at 6+ px. Then re-make the 64 and 128 strips and the icon.
- **T2 (High-tier read at 64 px, owner call):** the Volt is the lightest and least saturated icon in the Thunder row. The horn already carries about 20 lime px at 64, so the cleanest lever is the horn's lime zig thickness (line 383, 0.013 wide) to about 0.017, not a palette change. Judge it against the Wyvern and Bull in the strip.
- **T3 (nose cap, lines 319-330):** the domed cap reads edge-on as a flat vertical plate, and its front ring keeps a 1-2 px light sheen. Pull the front-most ring back by about 0.004, or make it IRON_D, so the front edge in `closeb_cside2` stays below (230,240,250).
- **T4 (open jaw, line 316):** the MOUTH interior reads as a flat maroon wedge with a squared front corner in `pclose_below_roar_28`. Taper its front end (current half-width 0.05) to about 0.025 so the open mouth reads as a mouth. Keep JAW_MAX 14.
- **T5 (snort, line 543):** 6 deg is still faint on a 360 px frame. Take the head toss from `6.0 * sn` to `8.0 * sn`, keeping the settle at f76. Idle head pitch-up stays well under 30 (currently 5.46).
- **T6 (roar pump, lines 612-617):** 3 deg reads small on screen. Try a 5 deg neck pump (pulse keys -6.5 to -8.5, in-between keys -3.5 to -5.5) with the head counter-tipping by the same amount, so head + neck stays 15 and pitch-up stays 16.
- **T7 (act snap, lines 645-653):** the head rise peaks at 26.7 deg per frame on FX_BoltTrail. Spread the snap over 8 frames (f54-62) so it reads as a power snap at phone scale, not a whip.
- **T8 (act taps 1 and 3, line 639):** still alike at phone scale. Add the 2-3 deg tap-1 yaw suggested in round 3 (tap1 keyframe) so the taps read as three different strikes.

---------------------------------------------------------------------------------------------------------------------
## 6. Pass / fail checklist (round 4)

| Item | Result | Evidence |
|---|---|---|
| MUST 1 chin: no plank, no white at snout | PASS | `under.png` (no light plane), `closeb_cbelow` (soft spindle), `closeb_cside2` (sheen only, peak 244,255,255 in a 1-2 px rim), `pclose_below_roar_28` (maroon mouth) |
| MUST 2 eye line at 64 px | PASS (acceptance); legibility PARTIAL | `_icons_strip_64` lime 6 px at x 30-32 y 37-40; `_icons_strip_128` clear slit; `close_side`, `close_tq` |
| MUST 3 idle stamp at phone scale | PASS | `beat_f85r3_idle_side_idle_038` sole row 260 vs 271 (11 px); `_idle_stamp.png` |
| MUST 3 other feet planted | PASS | idle_foot_drift 0.0 |
| MUST 4 feet re-logged on final save | PASS | `feet_taps_f85r3.txt` 05:11:31 on 05:09:54 save; soles 0.000 at f30/42/54 |
| MUST 4 icon and strips from final portrait | PASS | icon, strips 05:11; portrait 05:11 |
| 9+ snort 6 deg | PARTIAL | verify head_pitch_up 5.46; numbers right, faint at phone scale (T5) |
| R3 T2 roar pump | PARTIAL | neck pump 3 deg (lines 612-617); small on screen (T6) |
| R3 T3 throat collar | PASS | `pclose_below_roar_28` |
| R3 T4 act taps 1 and 3 | NOT ADDRESSED | no tap-1 yaw in round-4 notes (T8) |
| Limits (neck, chest, pitch-up, end at rest) | PASS | `verify.json` |
| Ground and collisions | PASS | ground min -0.008 (act); collision_free true (throat hinge 0.26 exemption, raw counts in verify.json) |
| Tris at or under 15k | PASS | 14,532 (05:11 export) |
| No glow | PASS | glow {} in export |
| Act and roar visuals on the final save | NOT RE-RENDERED | act and roar sheets are 00:00 (ship check) |
