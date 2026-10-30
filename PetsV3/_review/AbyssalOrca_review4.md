# Abyssal Orca - art director review 4 (2026-10-14) - CLIPS APPROVED, with ONE required sign fix in act_lure

**Verdict:**
- **Polish: ACCEPTED.** The mesh stays at 8.5/10, locked, 10.17k tris.
- **swim, idle and roar: APPROVED.** The roar has 2 optional polish notes.
- **act_lure: APPROVED once one sign error is fixed.** Its tail keys were never converted to kit convention, so the
  strike folds the body into a ∩ instead of whipping head-in / tail-out.

The fix is a sign flip on 7 tail triplets. After it, send a 4-frame strip and a collision re-run (section 4). No full
re-review is needed; then **the Abyssal Orca is signed off.**

What I looked at:
- the clip code in `pets/AbyssalOrca.py`: `ground_lift`, `phase45`, swim, idle, roar, lure_act, `joints()`
- petkit `key()` / `Rq()`, to confirm the axes: rot = (pitch about +X with + = nose down, yaw about +Z, roll about +Y); on tail bones + pitch lifts
- the three pose sheets (tq / side / game), `_act_side.png`, and the single frames assembled into a strike strip (f50 / 57 / 60 / 62, side + game)
- your checks and the Esca clearance table

Temp files are outside the project.

---------------------------------------------------------------------------------------------------------------------
## 1. Checks - PASS

| check | result |
|---|---|
| collision_free | TRUE in all 4 clips |
| linear / loops | 0; idle and swim close exactly (all phase terms are whole cycles over n) |
| ground_min_z | idle 0.072, swim 0.159, roar 0.020, act 0.020 (≥ -0.02) |
| Esca clearance | ≥ 0.058 at the worst frame (f37, twitch extreme), above the 0.04 gate; dorsal clearance 0.60-0.84 at lure-up |
| pectoral hinge in `joints()` | accepted: the root chord block turning inside the hull at its own pivot is a joint, not a clip |
| head shakes | none: claps are on Jaw, twitches on Esca/Lure2, lashes on the tail, savour on a Spine roll |
| owner animation-reference rule | met (Petrov #17124, Children of the Sea #111777, Sea Beasts), cited in the code and in `_review/ANIM_REFERENCES_1014.md` |

**DANGLE 24 / 30 instead of my 16 / 20: right call.** With the bigger orb, f28 now hangs the lantern at mouth height
just ahead of the snout. That is the bait read, and it still clears the head by 0.15.

---------------------------------------------------------------------------------------------------------------------
## 2. Clip by clip

### swim (36 f): APPROVED
- The vertical wave travels front → back (lag 0.08 per bone).
- `phase45` puts the power downstroke at 45%, and the heave peaks at the end of the downstroke (+0.035).
- The front stays almost still (head counters, net pitch ≈ ±0.8°), as in the Petrov reference.
- The lantern follows through on the rod, and the pendulum on the Esca lags 7 f.
- From the game camera the flukes visibly beat. This is the orca's own motion: the Hammerjaw must keep the lateral sweep.

### idle (120 f): APPROVED (one optional softening)
- The patrol heave, lazy beats, alternating sculls and lagging lantern all read.
- The spyhop is one slow look each way with holds, so it is not a shake. The blow (event f76) and the 14° roll with the low-side fin raised also read.
- **Optional:** the return to level at f66 → 72 drops 8° of pitch and 14° of yaw in 6 frames, which is quick for the heaviest pet in the egg. Move the f72 level key to f76, and shift the blow to f76-86 (event f80) and the roll to f88-116. The loop still closes.

### roar (64 f): APPROVED (two optional notes)
- The gather → nose-down snap → 3 claps → 2 lashes → overshoot release follows the brief.
- The tail signs ARE kit-correct here: cocked down = -4 / -8 / -12, and the lashes go up then hard down.
- It reads from every camera, and it is not the Kraken's rear-up.
- **Optional, event sync:** the lash keys put the down-lash EXTREME at c+2 (f26 / f38), but `lash1/2` fire at f24 / f36, mid-swing. Shift the lash keys 2 frames earlier (c-5 up, c down, c+5 zero) so the splash fires on the hit.
- **Optional, your own Sea Beasts note:** "the jaw opens a beat AFTER the head commits". Right now the jaw rises 10 → 30 → 44 in lockstep with the snap (f12 → 16 → 20). Hold it at ~12 until f17 and open to 44 by f20. The snap then lands first and the gape follows, which makes it heavier.

### act_lure (120 f): APPROVED after REQUIRED FIX A
All the beats and timing match the brief:
- the dim at f6
- the bait twitches at f21/29/37, on the +12 peaks
- the draw-back with the rod compensating so the bait stays put
- the lure-up at f58, BEFORE the jaw opens
- the 1-frame gape and the hard shut at f62
- 0.22 of lunge (~1.2 studs at x1)
- the savour roll, and the relight and ripple chain at f92 / 96 / 100 / 104
- it ends at rest

**REQUIRED FIX A: flip the tail signs in the act's K table.**
- The roar converted my "+ = tail down" values to kit; the act copied them verbatim. In kit, `(8, 12, 16)` at
  f56-58 cocks the flukes **UP**, and `(-14, -22, -30)` at f59 kicks them **DOWN**.
- Combined with Head +6 / Spine +6 at the strike, both ends of the body drop at f60. The orca folds into a ∩, which
  reads as a hunch or cower (side f60), not an explosive strike.
- It also contradicts the reference you cite (Petrov: "the strike drives the head INTO the target while the tail
  snaps the other way") and the brief (cock DOWN to load, kick UP on the strike).

**Change the tail column of K as follows:**

| frame | now | flip to |
|---|---|---|
| f56 | (8, 12, 16) | **(-8, -12, -16)** |
| f58 | (8, 12, 16) | **(-8, -12, -16)** |
| f59 | (-14, -22, -30) | **(14, 22, 30)** |
| f60 | (-10, -16, -22) | **(10, 16, 22)** |
| f61 | (-6, -10, -14) | **(6, 10, 14)** |
| f62 | (-2, -4, -6) | **(2, 4, 6)** |
| f77 | (2, 3, 4) | **(-2, -3, -4)** (the tail droops lazily in the roll) |

Leave the 2 symmetric resume strokes (f106 / f114) as they are.

- **Result:** a bow on the draw-back (head up, flukes low), then a see-saw whip on the gulp (head down into the bait, flukes flicked UP). From the game camera the fluke flick then rises INTO view behind the body, instead of dropping away below it.
- **Limits:** Tail1 at +14 is inside the ±16 limit, and the dorsal's trailing root is 0.12 ahead of the Tail1 pivot. Re-run (Tail1, Dorsal) and (Tail2, Dorsal) at f59-60 anyway.

---------------------------------------------------------------------------------------------------------------------
## 3. Polish - ACCEPTED
- The brow is now seated flush (`up2 * 0.040 * sc`, no `n * 0.006`) and turned 8° toward the face.
- The throat tube starts at -0.99, which closes the jaw seam.
- The glint sticker is removed (L393 note); the Bulb VFX supplies the highlight.
- Tris are 10.17k.
- The model/close renders (08:20-08:21) predate the polish. With the final pass, include one refreshed `close_front` so the brow fix is on record.

---------------------------------------------------------------------------------------------------------------------
## 4. Sign-off pass (after FIX A; no full re-review)
1. A 4-frame strip at **f57, f59, f60, f62** in side + game views. At f57 the flukes are low; at f60 the flukes are UP with the head down, a straight-ish diagonal body, not a ∩.
2. `collision_free: true` and `ground_min_z` ≥ -0.02 for act_lure. Report (Tail1/Tail2, Dorsal) at f59-60.
3. A refreshed `close_front` (the brow polish).
4. Optional items: idle f72 → f76, roar lash shift and jaw lag. Any of them is fine to ship without.

**Then: Abyssal Orca SIGNED OFF** (model 8.5/10 + clip set).

---------------------------------------------------------------------------------------------------------------------
## 5. Addendum (review 4b, 2026-10-14) - SIGNED OFF

**Abyssal Orca: SIGNED OFF. Model 8.5/10 + clip set approved. Ready to export.**

**FIX A: lands.**
- In the code, the K tail column is exactly the flip table (f56 / f58 / f59-62 / f77).
- In `_fixA_side` / `_fixA_game`:
  - f57: the flukes are cocked low under a lifted head (the bow).
  - f59-60: head down into the bait with the jaw wide, the flukes flicked UP. A diagonal see-saw, no more ∩.
  - f62: the jaw is shut.
- From the game camera the fluke flick now rises into view behind the body: the strongest beat of the act from the
  player's camera.
- (Tail1, Dorsal) clears by 0.043-0.044 at f59-60 and (Tail2, Dorsal) by 0.21. That is tight but clean, and
  `collision_free` is true.

**Optional items: all land** (verified in the code).
- idle: the level key is at f76, the blow at f76-86 with the event at f80 (0.667), the roll at f88-116. The loop closes.
- roar: the lash keys are at c-5 / c / c+5, so the down-lash hits ON lash1 f24 / lash2 f36.
- roar: the jaw holds at 12 through f16-17 and opens to 44 by f20. The snap lands first, the gape follows.

**Checks: pass.**
- `collision_free` true in all 4 clips.
- ground_min_z: act 0.020, roar 0.020, idle 0.088, swim 0.159.
- Linear 0, and the loops close.

**Face (`_face_sheet`): accepted.** Seated flush and turned in, the brows still show a small ledge beyond the rostrum
in the front view. That ledge is the family's fierce_eye overhang (Rex review 1 asked for a 0.02-0.03 overhang), and it
reads as a scowl in side and tq. It is invisible at game distance and at 64 px. No further change.

**Owner to-do:**
- Studio import of `C:\cdimp\AbyssalOrca.fbx` as creator ZAB Studio.
- VFX Studio effects on Bulb, Glow1-3, DorsalTip, FlukeL/R, Blow, Maw and the eyes, driven by these events:
  - idle `blow`
  - roar `roar` / `clap1-3` / `lash1-2`
  - act_lure `dim` / `twitch1-3` / `gulp` / `relight` / `ripple` / `glow1-3`
- Save + Publish.
