# Inferno Phoenix - CLIP review (review 2, 2026-10-14)

## Verdict: APPROVED WITH ONE FIX (fly plumes, K1). Score 8.5 / 10.

**What works:**
- Idle, walk, takeoff, land, roar and act_rebirth are approved as built.
- The act is the strongest part: the bow into the pyre, the dead-still ember sleep, two heartbeats, the head waking first, two beats into a heraldic screech, then landing and folding.
- The roar's head-thrust with the 3-frame jaw lag is good.

**What needs fixing:**
- The **fly wake** is the one real problem. Every frame with its colour, view and size: [table](#fly-wake-view-table).
  - **Cause:** the chain's own rest curl (+48.6°, seg1 → vane) is still applied in flight.
  - **Effect:** on average the vanes sit **+37° above horizontal**, swinging between +16° and +58°.
  - **Result:** for half of every stroke the three plumes stand up behind the bird. In tq they look like vertical antennae; from the game camera they look like J-hooks. The brief forbids hooks, so this is the Celestial Dragon crescent risk.
  - **Fix:** K1 below, tested.

**Gate:** I reproduced it myself on a temp copy (`phx_rev2\clip_try.py`, step 1, every frame, all `check_pairs` + `joints`):
- 0 hits on all 7 clips, 0 linear keys
- ground min −0.0118 to −0.0152, always at the talon tips
- my numbers are identical to yours

**How I worked:** nothing in the project was written except this file. All tests and renders are in `C:\Users\ventu\AppData\Local\Temp\phx_rev2\`.

## Model pack: F1-F5 confirmed
- **F1-F3 and F5:** the spec diff against my tested `PhxF2` (F1-F3) and `PhxB` (F4) is the exact fix text, plus `H_MODEL = 2.034` and the belly shingles you removed.
- **F1:** the side view shows the long trailing plumes, and the icon shows a plume bottom-right.
- **F2:** the feet are separated in the front view.
- **F3:** the collar points are visible from the game camera.
- **F4:** `close_side.png` shows a continuous culmen. I compared it against v1 and against my `PhxB` render.
- **Removing the belly shingles: approved.** It costs front PALE 12.0 → 11.5 (0.5 under the 12 floor); accepted as a tolerance.
- **One polish item, M1 (optional, tested):** the outer collar shingles (x ±0.11) stand out of the neck side as a small red stub, visible in `close_side` / `close_tq` (the Index inspect view). Narrow that row:
  ```python
  neck_cape(B, n1a, n1b, 0.15, [(0.90, (-0.085, -0.03, 0.03, 0.085), True)],
  ```
  The stub disappears from the side and the LAVA collar points still show from the game camera (`phx_rev2\collar_cmp.png`).

## Per-clip verdicts

| clip | verdict | notes |
|---|---|---|
| idle | **APPROVED** | Breath with the head level, the L / C / R licks, a 44° look-back over the left shoulder held 18 f (the left fire-eye faces the follow camera), crest flare + glare, heat lift, re-grip. The look-back turns 44° in 8 f, as the brief's table specifies. That is above the brief's own "≤ 30° per 6 f" rule, but it is a single turn-and-hold, not a shake. Accepted. |
| walk | **APPROVED** | Rolling strut, gyro head, crest follow-through, plumes on X1 4 ± 2 with travelling yaw. Slide 0, foot_z_var 0. |
| fly | **FIX K1** | Body, wings, FPITCH 45, rise on the downstroke and the D9 tuck are all good. The plumes are not (above). |
| takeoff | **APPROVED** | The shallow crouch (−0.05) reads through the pitch-forward and the cloak opening. The plumes drag and then swing into the trail with the +6 overshoot. Re-verified with K1 in place: 0 hits; with K1 the swing lands in a straight wake by f23. |
| land | **APPROVED** | The brake flare of the plumes (+20 / +10 / +6) reads as an air-brake. Touch on LIFT4 and the brake path are as tested. Re-verified with K1: 0 hits. |
| roar | **APPROVED** | LIFT1 cloak hold, the train at +56 / +24 / −14 with a 2-f chain lag, crest +14, 4° chin-up thrust, jaw 3 f behind the head, buzz with the head still. From the game camera the train reads as three flame tongues low behind the bird (moderate, not a money shot; the `screech` / StreamerEnd VFX will carry it). I tested three alternatives (below); none improved it. |
| act_rebirth | **APPROVED** | All the story beats read in tq, side and game. Heights are right: feet at 0.39 and plumes at ≥ 0.134 at the rising peak. f58 tq shows the far wing edge-on as a thin rod; that is a 2-frame transient on the downbeat. Accepted. |

## Deviations C1-C7

**C1-C5 and C7: approved**
- **C1** walk lift 0.08 + 0.06 wide swing. The buried knee is the design limit, and the wide pass reads as part of the strut swagger. Front-view check: no waddle.
- **C2** re-grip 0.045 / 6°.
- **C3** all planted crouches at −0.05, land absorb −0.04 (my rule 1).
- **C4** streamer floors and biases.
- **C5** roar cloak on LIFT1, brief train keys. I tested three alternatives and kept yours:
  - fan L −8 / R +8: clean, but no visible gain
  - fan ±12: 30-38 wing hits (`WingTip|StreamerL3/R3`)
  - steeper root +68 / +12: clean, but no gain
- **C7** act legs: FK (24, −10, 40) → (50, −30, 66, spread 15) → reach; plant and air ranges as in the brief.

**C6: body and legs approved; the plume keys are overruled.** Replace them with K1.

### K1 - fly plumes (MUST). Replace `fly_stream` with:
```python
def fly_stream(ph, c):
    """the BURNING WAKE: X2 / X3 baselines cancel the chain's rest curl (seg1 -34.6 -> seg2 -20 -> vane +14 deg), so in
    flight the plumes stream nearly straight behind (ref #8), seg1 ~12 deg under the flight line, vanes ~+8 deg, with a
    travelling S on top (X1 peaking 0.15 after the downstroke start, lag 0.10 per segment); forked fan L -8 / R +8"""
    q = ph - 0.03 * LAG[c]
    fan = {"L": -8.0, "C": 0.0, "R": 8.0}[c]
    w = lambda d: math.cos(2 * math.pi * (q - d))
    return dict(x1=-22 + 4 * w(0.15), x2=-11 + 7 * w(0.25), x3=-18 + 7 * w(0.35), y1=fan, y3=3 * w(0.60))
```
**Verified on the temp copy:**
- **fly:** 0 hits at step 1; ground min 0.437 (unchanged); loop closed (the function is periodic in `ph`)
- **takeoff and land:** both read `fly_stream` at their boundaries; 0 hits; ground min −0.0118 (unchanged)
- **ranges:** X3 stays within −25…−11 (inside the §5.4 limit ±25) and X2 within −18…−4
- **renders:** `phx_rev2\fly_cmp.png` (rows: v1 / K1 / a milder variant), `tl1.png`

<a id="fly-wake-view-table"></a>**The fly wake, view by view** (`fly_cmp.png`, frames 0 / 8 / 16 / 24):

| view | v1 keys | K1 |
|---|---|---|
| side | The plumes rise to 30-40° above the flight line from f8 to f20. | One straight fire wake trailing just under the flight line. |
| tq | Three vertical sticks stand up behind the back. | The plumes trail behind the wing; nothing stands up. |
| game | Three J-hooks. | Three straight fire streaks fanning back. |

- **Milder variant: rejected.** It used X1 −20 + 4w / X2 −7 + 7w / X3 −12 + 9w, and the plumes still stood up in tq.
- **After K1:** re-render the fly pose sheet (0 / 8 / 16 / 24) plus takeoff 23 and land 0 / 6. Nothing else needs re-review.

## Events and references
- **Events: approved.** The kit stores one time per name, so the numbered names are correct.
- **Studio registration list:**
  - **act:** `act_rebirth`, `ignite`, `pyre`, `ash`, `heartbeat1`, `heartbeat2`, `rebirth`, `reborn`, `touch`
  - **roar:** `screech`, `rattle`
  - **takeoff / land:** `launch`, `touch`
  - **idle:** `lick1`-`lick3`, `ember1`-`ember2`, `flare`
  - When the owner wires the VFX, match the idle events by prefix (`lick*`, `ember*`).
- **References: accepted.** #3 / #4 / #5 / #6 / #7 / #8 / #9 are cited. The three "if available" ones do not exist on the site; that is logged, and no credits were spent.

## Summary
- **Verdict:** APPROVED WITH ONE FIX, 8.5/10.
- **Clips approved as built:** idle, walk, takeoff, land, roar, act_rebirth.
- **Fly:** must take K1, the new `fly_stream`. It removes the stand-up / hook plumes and was tested at 0 hits on fly, takeoff and land.
- **Deviations:** C1-C5 and C7 approved; C6 is approved except the plume keys.
- **Model pack:** confirms F1-F5.
- **Optional polish:** M1, a narrower collar row.
- After K1 (and M1 if taken), re-render the fly sheet and the takeoff / land boundary frames, then hand it to the owner. Nothing is to be published or imported by the pipeline.
