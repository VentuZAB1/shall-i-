# REVIEW: Tier 7 `Tier7_x12` (x12, EMERALD), Phase C (2026-10-12)

Reviewer: the independent visual reviewer. This review was read-only: I didn't edit the template or the lab, and I didn't
call `T.refresh` or `T.reset`.

**What I checked:**
- The brief, `PLAN_REVIEW.md` (x12 = APPROVED, notes N1-N4, rules R1-R3), PLAN.md and BUILD_NOTES.md.
- All 68 parts of the template, read back in belt space (sizes, positions, rotations, colours, variants, flags, lights).
- `TreadmillClient`'s rune, sparkle and pulse code, and its screen detector.
- `T.validate(7)`.
- A coplanar-face scan of every axis-aligned part.
- 15 captures taken under `T.lock("Rev7")`, one at a time, then `T.unlock("Rev7")`.

## VERDICT: **FIX** (1 MUST, a one-property recolour; 2 NICE)
The build is clean and on the agreed ladder. The only thing standing between it and "on point" is the silver screen
bracket in the middle of the emerald slab, the hero shape that the plaza sees.

---

## Items

### 1. MUST: recolour the chassis screen bracket from PLATINUM to EMERALD DEEP
**The part:**
- The chassis Part 2.162 × 2.853 × 0.985 at belt (0, 5.577, −8.927), tilted 20°.
- It is now (192, 202, 208) Plastic/Universal.

**What's wrong:**
- In the screen frame's local space it covers x ±1.08 and y −1.73..+0.26.
- On the plaza side it stands **0.29 proud** of the slab's back face. That is a 2.16 × 1.99 silver plate (about 19 % of
  the slab) whose top edge stops mid-slab for no visible reason.
- In every front view it is the brightest shape on the model. The emerald slab reads as "a green box with a white
  window" instead of one big cut jewel. This is worst at hub distance.
- Evidence:
  - `Rev7_eye` and `Rev7_close`: a sticker in the centre of the slab.
  - `Rev7_hub34` and `Rev7_spawn`.
  - `Rev7_hubPlus45` and `Rev7_hubMinus45`.
  - `Rev7_far55` and `Rev7_lineup`: at 55-60 studs it's the first thing you see.

**The family rule supports the change.** In tiers 1-6 the bracket always takes the screen-face colour:
| Tier | Bracket | Face |
|---|---|---|
| T4 | green | green |
| T5 | red | red |
| T6 | gold | gold |

That's why T6's gold plate reads as part of the screen (`Rev7_bay6vs7`). Platinum on T7 matches neither the face nor
the slab.

**Fix:**
- Set it to Color **(0, 100, 60)**, MaterialVariant **Studs**. That's EMERALD DEEP, the tone next to the label face
  (0, 78, 50), and Studs like the T5/T6 brackets.
- Change the colour only. Size, CFrame and collision stay as they are.
- Results:
  - From the plaza: a tonal mount, so the slab stays one jewel.
  - From the runner: a green stem under the label, like T6's gold stem. Today it's a white block under the screen
    (`Rev7_runner`).
- Fallback: if the deep green looks like a hole in `eye`/`far`, use ONYX (16, 38, 30) Studs instead.
- After the change:
  - Re-run `T.validate(7)`. The screen detector works on size, not colour, so the label stays on the face.
  - Recapture `eye`, `hub34`, `spawn` and a far front view at 50-55 studs.
- The platinum count drops from 21 to 20 parts. That's fine.

### 2. NICE: crest gem material, only if it still reads washed out after item 1
- `screen_gem` is Glass, T 0.15.
  - Up close it's a lovely translucent faceted emerald (`Rev7_close`).
  - From the −45° plaza angle it goes pale mint/white with sky reflection (`Rev7_hubMinus45`), weaker than the vivid
    Plastic rail crystals.
- If it still looks whitish in the post-fix `hub34` / ±45° captures, switch it to Plastic/Weld GEM (60, 230, 140),
  T 0-0.15 (same size and CFrame, keep `CrestLight` inside).
- That would leave 0 accent-material parts. If it reads green, keep the Glass.

### 3. NICE: no action on the builder's other two open points (approved as built)
- **Crystal overhang on the cups: KEEP.**
  - The rail crystals' upper girdle vertices sit at r 0.57 (0.63 at 110 %) against the collar's 0.5 half-width. So they
    overhang 0.07 (0.13).
  - The lower girdle corners poke at most 0.07 out of the collar sides at y ≈ 2.9.
  - In `Rev7_railCupClose` it reads as a gem a little wider than its setting, which is natural jewellery. At 55 % the
    crystal sinks fully into its cup, so the twinkle "breathes" well.
- **Platinum (192, 202, 208): APPROVED.**
  - It reads as light silver.
  - Side by side it is clearly greyer than x14's snow white (238, 247, 255): see `Rev7_far55` and `Rev7_lineup`.
  - It is still bright enough in shade (`Rev7_rear34`).
  - Don't go lighter again.

---

## What is good (keep all of it)
- **Theme:**
  - Emerald (0, 172, 100) has hue ≈ 155° at full saturation, and the gems (60, 230, 140) are ≈ 148°.
  - T4's grass greens are ≈ 108° at about 50 % saturation. So there's no confusion with T4, and no gold anywhere, so it
    isn't "T6 recoloured" in palette.
  - The green-black ONYX (16, 38, 30) still reads as the family's dark frame, not navy.
- **Craft:**
  - Every decor joint is exact:
    - stanchion top = grip bottom 3.163;
    - rail ends butt the stanchion at z −5.275 and end flush with the frame at 7.955;
    - posts run 0.871 → 2.2;
    - collars sit on the rail;
    - runes are evenly spaced, with 0.537 gaps.
  - The crest is built in the frame's local space. The base sits flush on the frame's top face (local y 1.729), the
    prongs sit on the base, and the gem's side tips meet the prongs (0.775 vs 0.778).
  - The emblem diamond is seated 0.05 into the plaque, and the plaque is flush on the console face (−9.338).
  - **The coplanar scan found no decor z-fighting.** The only hits are chassis undersides on the floor and faces hidden
    inside the console bar.
  - No floating bits. Symmetric about x = 0. The only asymmetry is in fixed T6 chassis parts: posts at −2.85 / +2.64
    and feet at −6.20 / +6.33.
- **Brick look:** every part is Plastic with a variant: Studs on onyx, Weld on the emerald and gems, Inlet on the belt
  and Universal on the platinum. That's the T1-T6 mix. The one Glass part is within the cap.
- **Runner view (`Rev7_runner`):**
  - "+600K / sec" is crisp yellow on the deep face (lum 0.23).
  - The rails frame the belt.
  - The console crystals flank the screen.
  - Nothing is over the head or in the corridor.
- **Lights:**
  - `CrestLight` sits about 0.5 BEHIND the face's runner-side plane, so it can't lift the label face.
  - The rail lights are about 12 studs from the face, with range 7.
  - R3 passes.
- **Ladder (PLAN_REVIEW §1), measured:**
  | Check | Built | Target |
  |---|---|---|
  | Solid top | 8.53 | ~8.5 |
  | Static peak | 9.98 | 10.0 |
  | Anim max | 9.98 | ≤ 10.1 (`screen_gem` only changes colour) |
  | Visible parts | 68 | 64-72 |
  | Animated parts | 22 | ~22: 12 runes, 8 sparkles, 2 pulses |

  - It is a clear step up from x10 in richness: a 5-role jewel palette, rails, crest, plaque, 3 lights and the first
    motion (`Rev7_bay6vs7`, `Rev7_rear34`).
  - It is still clearly quieter than x14's gate next door (`Rev7_lineup`, `Rev7_far55`), which leaves room for
    x14..x20.
  - The side rails read best from the hub's ±45° bases (`Rev7_hubPlus45`, `Rev7_hubMinus45`), which is where bases 1
    and 3 are seen from.
- **Clearances:**
  - Decor max |x| is 5.82 (the console crystals at 110 %). The sign keep-out (|x| > 6.4) and the lamp (x ≥ 7.7) are
    clear. Both upgrade signs are fully visible (`Rev7_rear34`).
  - R1 walkway: nothing at |x| ≤ 4.1 behind z 7.
  - Zone, head box and corridor are clear. `T.validate(7)` = **0 FAIL, 0 WARN**.
- **Motion (worked out from the `TreadmillClient` source):**
  - Runes sort by number. `rune_1..6` run up the left rail and `rune_7..12` run down the right: a 2 s clockwise loop.
  - While running, idle runes dim to about (33, 127, 77), still green on platinum.
  - Sparkles scale about their centre. At 110 % the rail crystals reach y 3.77 and the console crystals 5.87, all clear.
    At 55 % they sink into their cups and caps.
  - The `screen_gem` and `hood_emblem` pulses only change colour.

## Captures (all `Rev7_*`, lock `Rev7`)
| Group | Capture ids |
|---|---|
| Presets | `spawn`, `hub34`, `eye`, `side`, `sideHi`, `runner`, `rear34`, `close`, `lineup` |
| Extra | `hubPlus45`, `hubMinus45` (the hub's ±45° bases, ~30 studs), `far55` (front, ~53 studs), `railCupClose` (crystal / collar detail), `bay6vs7` (x10 vs x12 from the front) |
| Not used | `crestSide` (too close, distorted) |

- The mock "+600K" label rendered in every capture where the face is visible, so there's no label bug.
