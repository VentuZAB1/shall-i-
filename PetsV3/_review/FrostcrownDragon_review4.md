# Frostcrown Dragon - model re-check + CLIP GATE review 4 (2026-10-27) - REVISE

**Model short check: APPROVED, 8/10.** **Clip gate: REVISE, 7/10.** Overall: **REVISE, 7/10** (ship at 8+).

The model did what I asked. All five front crown points show, the back-to-flank contrast reads, and the darker palette is
under the luminance target without going navy-black. The clips are clean on the physics: collision-free, loops closed,
pose limits met, readable beats. Three things stop the gate: (1) takeoff, land and walk have no animationreference.org
reference, which breaks the owner's rule; (2) the signature act has no wing peak, so it is not yet mythic-worthy; (3) the
end-of-clip rest frames are not in the sheets, so "ends at rest" is not verified. A small ice-white miss is also open.

## Part 1 - Model short check (round 4 palette and crown)
| Check | Result | Evidence |
|---|---|---|
| All five crown points visible from the front | PASS | `crown_front.png`: centre tall, inner pair and outer pair all read between the horns |
| Horns sweep back, no ears | PASS | Roots at x 0.21 / 0.24 sit clear of the band; horns read as horns |
| Dark top separate from flanks in `model_game` | PASS | Back and neck read as a darker navy band over the mid-blue flank (builder gap 26.3; my sample on the spine: median lum ~79) |
| Luminance <= 110 | PASS | 128 px strip: **107** (my count), 105 (builder); 64 px: 100 (mine), 105 (builder); alpha icon 109 (builder) |
| Dark share >= 28 % | PASS on my count, borderline on the builder's | 128 px: **29 %** (mine), 24 % (builder); 64 px: 36 % (mine), 26 % (builder) |
| Ice-white >= 9 % | **FAIL (small)** | 128 px: **7.8 %** (mine); the ICE_BELLY darkening pulled some pale pixels under the threshold. See MUST 4 |
| Gold hero at 64 px | PASS | Portrait 64 px: 44 px (mine) vs Rex 4 and Leviathan 11; builder 76 / 114. Game camera 28 / 31 (lead ruling >= 25) |
| Reads ICE-dragon, not navy-black, at 64 px | PASS, with a watch item | At 64 px the body is a deep blue with the white fin row, frost core and gold crown carrying the ice and gold read. The game-camera icon is darker (lum ~79-86 on my count), so the ice read leans on the fins |
| Distinct from the secrets | PASS | Rex: cyan spines and seams on a navy body. Leviathan: magenta and plum. Frostcrown: deep steel-blue with white fins and gold crown. On my count Frostcrown is at or below both in luminance and has the most dark mass |
| Distinct from Celestial / Black / Ivonrath | PASS | Celestial (lum ~77) is more violet-indigo with a white crest; Black Dragon (~78) and Ivonrath (~68) are darker and warmer. The gold crown and white fins keep Frostcrown apart |
| Tris | PASS (builder) | 8,440 builder-reported, gate 13k |

Note on the numbers: my 128 px strip split was wrong at first (the strip is 810 px, six icons). The figures above use the
correct six-cell split. The builder's counts differ from mine by a few points on the same strips, so treat luminance as +/- 3.

## Part 2 - Clip gate

### Step 1 (from `_scratch/full_step1.txt` and `CLIP_NOTES.md`)
| Check | Value | Rule | Result |
|---|---|---|---|
| collision_free | true | true | PASS |
| Audit linear | 0 on every clip | 0 | PASS |
| Loops closed (idle, walk, fly) | loop_pos 0.0, loop_rot 0.0 | closed | PASS |
| Walk slide | 0.0; foot_z_var 0.0 | ~0 | PASS |
| ground_min_z (idle, walk, takeoff, land, roar, act) | -0.005 / -0.005 / -0.008 / -0.005 / -0.005 / -0.005 | >= -0.02 | PASS |
| Fly ground | +0.098 | airborne | PASS |
| Largest per-frame bone step | 42.4 deg, WingTip_L, takeoff f12 (launch) | < ~60 | PASS (see NICE 2) |
| Neck max | 8.0 (Neck2 8.0), in the act press | <= 8 | PASS, zero margin (NICE 1) |
| Chest vs Spine | 3.0 | <= 5 | PASS |
| Head + neck pitch-up | 15 (roar) | <= 30 | PASS |
| Head shake / airborne spin | none found in the clip list | none | PASS |
| Events | frostpuff 0.667 x120 = f80; launch 0.393 x28 = f11; touch 0.571 x28 = f16; roar 0.364 x66 = f24; click 0.145 x110 = f16; frost 0.455 x110 = f50 | match the clip table | PASS (JSON stores event times as fractions of the clip) |

### Clip-by-clip judgement (pose sheets `renders/_pose_tq_<clip>_sheet.png`)
| Clip | Beats read? | Notes |
|---|---|---|
| idle (120) | PASS | Wings fold / half-open / fold; calm head; no shake |
| walk (40) | PASS on the motion | Quad stride reads; the body holds level. Reference gap, see MUST 1 |
| fly (28) | PASS | Stroke reads f0 high, f7 mid, f14 low, f21 mid. Body level, legs trail, tail streams |
| takeoff (28) | PASS | f0 crouch, f10 wings up, f13 downstroke + hind push, f17-22 airborne. Launch at f11 reads |
| land (28) | PASS on the beats, sheet ends at f21 | Touch f16; the feet reach. The last frames are missing (MUST 3) |
| roar (66) | PASS | f14 head lifts and wings spread, f26 jaw open (lags the head), f40 hold, f58 closing. Sheet ends at f58 (MUST 3) |
| act_stillfreeze (110) | **Beats read, the act does not peak** | f16 inhale and fins up, f34-50 head press with the jaw open and the body dipped, f70 head lifts, f88 wings settle. **The wings never move f0-f80** (the code keys them only at f0, f80, f88, f98, f110), so the biggest silhouette change is missing. The fins at 25 deg are hard to read as they rise against the white sky. See MUST 2 |

The act's body dip and head press are correct. My frame diff confirms the moving region is the head, neck and body, and the
wings only move at f80-98 (the settle). That is consistent with the code, so there is no stray wing key.

### ANIM_REFS rule (owner rule: 1-3 clips from animationreference.org, frames read, cited)
| Clip | Cited reference | From animationreference.org? | Verdict |
|---|---|---|---|
| fly | ANIM_REFERENCES_1014 #8, banshee flight (site); D2 legs from Sakugabooru | stroke: yes; legs: no | PASS for the stroke |
| roar | 1014 #3, Sea Beasts heavy-head roar (site); W0 Wolf's Rain roar hold (site tag `wolfs-rain`) | yes | PASS |
| takeoff | D1: *Kobayashi-san Chi no Maid Dragon* #09, Sakugabooru #31258 | **no** (builder: "No site credits were used") | **FAIL** |
| land | D2: Maid Dragon #01, Sakugabooru #29750 | **no** | **FAIL** |
| walk | W0 cited for the head hold only. W0 is a diagonal-pair walk, the rig is lateral-sequence | W0 yes, but it does not match the gait | **FAIL** (no gait reference) |
| act_stillfreeze | W0 for the jaw hold | yes (jaw only) | PARTIAL (the head press and the fin rise cite nothing) |
| idle | W0 for the head level | yes | PARTIAL (the frost hum has no reference) |

The lead's 1027 pick said the flyers should spend the site opens on HTTYD clips ("3 site opens are left, spend them on 1-2
HTTYD clips"). The builder opened one HTTYD clip, which froze the tab, and did not spend the second. That leaves the takeoff
and land on Sakugabooru. The Sakugabooru fallback is only allowed when no site tag fits or the day's opens are used up.
Neither applies here.

## MUST (round 5, in priority order)

### MUST 1 - animationreference.org references for takeoff, land and walk (owner rule)
- Spend the remaining site opens: one HTTYD clip for takeoff and one for land (`/tags/how-to-train-your-dragon`, e.g. "Flying
  With The Dragon Rider (HTTYD2)" or "Hiccup & Toothless Fly Together"). Use the free study-page preview if the player freezes
  again; record the attempt.
- One site walk clip for the gait: `/tags/walk-cycle` or `/tags/running-locomotion`, lateral-sequence if the site has one.
- One site clip for the act's head press (`/tags/creature-animation`, or W0 with the jaw-hold frames cited for the press).
- Step the frames on the same source (the site's Sakugabooru post), note the frames, and cite them in `ANIM_REFS.md` with
  the takeoff, land and walk keys mapped to frames. Sakugabooru clips stay as supporting refs only.

### MUST 2 - The act needs a mythic climax: open the wings at the frost burst
- Current: the wings are FOLD f0-80, so the act's peak is a head press with a mist cone. The silhouette never changes.
- Fix in `stillfreeze()` (`wings` keys at L731-732): add a SPREAD key at f44, hold SPREAD f44-58 (the same pose the roar
  uses), then settle to HALF f70 and FOLD f80, as now. The mist fires at f50 inside the hold. The fins stay at 25 and the head
  stays at Neck 8 / Neck2 8 / Head 9.
- Fin legibility: raise the rise from 25 to 30 deg, or keep 25 and rely on the wing flare. Either way the fins must read
  against the white sky in `_pose_tq_act_stillfreeze_sheet.png`.
- Target: in the sheet, f50 shows the wings open, the fins up and the head pressed, all at once. That is the mythic frame.

### MUST 3 - Verify the end-of-clip rest frames
- The sheets stop before the ends: roar at f58 (clip 66), act at f88 (clip 110), land at f21 (clip 28), takeoff at f22
  (clip 28).
- Add the final frames to the sheets: roar f66, act f110, land f27, takeoff f27. Print the maximum bone delta against the
  rest / FOLD pose at the final frame. It must be <= 2 deg for roar and act. Takeoff and land end in the flight cycle or
  FOLD, so state which.
- Without this, "ends exactly at rest" is not verified.

### MUST 4 - Ice-white back above 9 % (ICE_BELLY darkened too far)
- Round 4 darkened ICE_BELLY (210,226,246) -> (196,214,240). That pulls the pale pixels under the ice-white threshold: 7.8 %
  on my 128 px count (target 9 %).
- Fix: keep (196,214,240) on the belly strip and the chest plate, and restore (210,226,246) on the throat plate and the core
  facet only. Re-measure. Target >= 9 % on the 128 px strip, luminance still <= 110.

## NICE
- **N1 Neck margin.** Neck 8.0 and Neck2 8.0 sit exactly on the limit. Use Neck 7 / Neck2 7 / Head 11 in the press (total still
  25). Gives 1 deg of margin.
- **N2 Takeoff snap.** Split the launch frame (f11-13) with one in-between to bring the 42.4 deg WingTip_L step under 30 deg.
- **N3 Front horn roots.** Round 4's roots read as wide gold blocks at the skull sides in the front view. Taper the root
  (keep the x 0.21 / 0.24 positions).
- **N4 Walk gait match.** If the site walk clip is lateral-sequence, keep it. If the only fit is a diagonal-pair walk, say so.

## Pass / fail checklist
| # | Item | Result | Note |
|---|---|---|---|
| 1 | Five crown points visible from the front | PASS | |
| 2 | Dark top separate from flanks, `model_game` | PASS | |
| 3 | Luminance <= 110 (128 / 64 / alpha) | PASS | 107 / 100 / 109 (mine and builder within 3) |
| 4 | Dark share >= 28 % | PASS (mine) | Borderline on the builder count |
| 5 | Ice-white >= 9 % | FAIL | 7.8 % (MUST 4) |
| 6 | Gold hero readable at 64 px | PASS | 44 px portrait; game 28 (ruling) |
| 7 | Reads ICE-dragon, not navy-black | PASS | Watch the game icon |
| 8 | Step 1: collision_free, loops, linear 0 | PASS | |
| 9 | Step 1: ground_min_z >= -0.02 | PASS | -0.008 worst (takeoff) |
| 10 | Neck <= 8 | PASS | At the limit (NICE 1) |
| 11 | Chest vs Spine <= 5 | PASS | 3.0 |
| 12 | Head + neck pitch-up <= 30 | PASS | 15 |
| 13 | Largest step < 60 | PASS | 42.4 (NICE 2) |
| 14 | No head shake, no airborne spin | PASS | |
| 15 | Beats readable (takeoff, fly, land, roar) | PASS | |
| 16 | Act readable beats | PASS | Head press and mist read |
| 17 | Act is mythic-worthy | FAIL | No wing peak; fins small on white (MUST 2) |
| 18 | Ends at rest (roar, act, land, takeoff) | NOT VERIFIED | Final frames missing (MUST 3) |
| 19 | ANIM_REFS: roar | PASS | |
| 20 | ANIM_REFS: fly | PASS (stroke) | Legs cite Sakugabooru |
| 21 | ANIM_REFS: takeoff | FAIL | Sakugabooru only (MUST 1) |
| 22 | ANIM_REFS: land | FAIL | Sakugabooru only (MUST 1) |
| 23 | ANIM_REFS: walk | FAIL | No gait reference (MUST 1) |
| 24 | ANIM_REFS: act | PARTIAL | Jaw only; press and fins uncited (MUST 1) |
| 25 | Events match clip table | PASS | Fraction-stored times reconcile |
| 26 | Name is two words, no glow, studs | PASS | |

## Next round
Send: `ANIM_REFS.md` with the site frames for takeoff, land, walk and the act press (MUST 1); the act pose sheet with the
wing flare at f44-58 (MUST 2); the final-frame sheets and the rest-delta numbers (MUST 3); the re-measured 128 px strip for
ice-white (MUST 4). The model itself is approved once MUST 4 is re-measured.

Verdict: **REVISE, 7/10 overall.** The model is 8/10 and approved on the short check. The clips need MUST 1-3 (the rule,
the act peak and the rest verification) before the clip gate can pass.
