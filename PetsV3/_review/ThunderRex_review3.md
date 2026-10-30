# Thunder Rex - art director review 3 (2026-10-14) - MODEL APPROVED, SIGNATURE ACT REVISE

**Model: APPROVE, 8.5/10 for a 1% SECRET** (v1 3/10, v2 7/10). All 10 round-1 checklist items now pass, and every
review-2 fix landed. The mesh is locked: don't touch it unless the owner asks.

**Animation: REVISE one clip.** `act_tailspin` must be replaced. It is the third airborne 360 in our roster, the
Storm egg's own Raiju already does the same beat structure, and it reads light, not heavy. Idle, walk and roar are
approved, with three small should-fix tweaks. No new model review is needed: send only the new act's pose sheet.

What I looked at:
- v3 `pets/ThunderRex.py`
- `_model_sheet` (tq at 600), `_close_sheet`, and model_side / model_game / model_tq at full size
- `_icons_strip_64/128` plus `ThunderRex_icon.png`
- `_pose_tq_sheet` and the 8 single pose frames
- the act docstrings of all 21 other pets

How I measured: the same pixel classifier as round 2 (background removed, ±3%).

| view | ARMOR | HIDE | BELLY | crystal | GOLD | v2 → v3 notes |
|---|---|---|---|---|---|---|
| side | **35.7%** | **36.6%** | **7.2%** | 19.2% | 1.2% | HIDE 47→37, ARMOR 29→36, BELLY 4→7 |
| game cam | 32.7% | 34.8% | 6.6% | 23.4% | **2.5%** | GOLD 0.2→2.5 |
| back 3/4 | 26.7% | 36.5% | 12.3% | 22.9% | 1.6% | |
| tq | 23.8% | 49.8% | 7.3% | 17.4% | **1.7%** | |

---------------------------------------------------------------------------------------------------------------------
## 1. Round-1 checklist - final pass

1. **Lineup - PASS.** On the real icon strip it is now the most complex and best-accented Storm pet: dark armour,
   a cyan/white ridge and a gold crown. It clearly outclasses Raiju, ThunderBull, StormWyvern and CelestialDragon, and
   it holds its own next to SolarLion. It is not a remix.
2. **64 px test - PASS (narrow).** T-rex: yes. Glowing ridge: yes, it pops on the slate. Crown: about 13 gold pixels,
   up from 1-2, and it reads as a gold crest on the head; at 128 px the prongs read clearly. (Optional, for the icon
   only: raise the icon camera ~8°, so the crown sits on the top edge of the silhouette instead of in front of the
   horns.)
3. **Value blocking - PASS.** The side view shows three bands: ARMOR 36 / HIDE 37 / BELLY 7, with no colour over
   45%. From the side the tail now reads dark shell / blue hide / silver stripe. Saturation median 0.52. ARMOR in the
   game view is 32.7%, just under the 35% target. I accept it.
4. **Accent - PASS.** Crystals are 19-23% of the side, back and game views. Each shard steps DEEP→CYAN→HOT. There
   are no stickers.
5. **Silhouette - PASS.** The horn tips are the highest point and the centre crown prong sits just under them. The
   ridge peak is 0.42. L:H is 1.66 in the side render, unchanged. Chest hw 0.29. From the game camera the W fan now
   runs into Tail1-2, and the tail ends in a 3-prong burst.
6. **Face - PASS.**
   - The V brow and the eyes sit above the snout.
   - The narrowed nasal plate (hw 0.045) no longer reads as a "tie".
   - The fangs now hang outside the lower lip.
   - The gold circlet reads as a crown band from the side and from the back.
7. **Legs - PASS.** No change from v2.
8. **Hard rules - PASS.**
   - 8,684 tris.
   - `collision_free: true` with Tail1-vs-legs added; audits clean; ground_min_z ≥ -0.006.
   - Nothing floats.
9. **Family fit - PASS.** No change from v2.
10. **Deliverables - PASS.** Everything is present: model sheet, close sheet, game render, the real icon pipeline
    strip, a 600 px tq and the pose sheet.

### Review-2 fixes - all landed
- 1 crown: lands
- 2 dark top: lands
- 3 tail: lands
- 4 silver underside: lands
- A neck shard: lands
- B jaw-hinge horns: lands
- C mouth interior: lands
- D VFX anchors: lands
- E teeth: lands
- Walk safety: lands
- **5 core: partly lands.** The core moved down, but the throat strip still covers its upper half. In the tq and the
  icon it reads as a gold/cyan chevron emblem over a silver bib rather than a full diamond. That reads fine as a chest
  badge, so it is **not blocking**. If you want the full diamond (optional): start the throat strip (L223) at
  `NECK0.lerp(NECK1, 0.45)` instead of 0.3, or set the core's `off` to 0.06.

I re-checked the pose limits against the roar peak (Neck -8, Head -16):
- The skull's back corner and the crown back plate stop at y ≈ -0.48, ~0.09 clear of shard 2 (now on Chest).
- The horn tips stay ~0.24 above the side-shard tips.
- The Q tips stay at x 0.37, clear of the side rows.

These numbers agree with the builder's collision pass.

---------------------------------------------------------------------------------------------------------------------
## 2. Animation review (30 fps)

### idle (120 f, 4 s): APPROVED, with one should-fix
- Good beats: breathing in the chest, a look left and right, a sniff with two short nose lifts, a double jaw clack,
  claw flexes, a heavy tail sway. It has plenty of variety for 4 s, and nothing loops visibly.
- **Should-fix, readability from the game camera:** the look-around is only ~12° in total (Neck yaw `ny*0.4` = 4°,
  Head `hy*0.6` = 8°). Seen from behind and above, that barely registers. Use `ny*0.8` and `hy*1.2`, for ~25° in
  total (inside the ±30° yaw limit). The nose lifts (Head 3↔7) can go to 2↔10.

### walk (32 f, 1.07 s, stride half 0.18, lift 0.13, duty 0.6): APPROVED, with one should-fix
- Good: the Spine yaw/roll is countered by the Chest, the neck bob and head counter-bob lag, the tail swings against
  the hips, and the toes peel 16°. Slide audit 0.
- **Should-fix, weight:** the body dip is a pure sine (`0.5-0.5cos`, 0.035), so contact and passing are equally soft,
  and that reads bouncy rather than heavy. Make it asymmetric: drop to **-0.05 within 3 frames after each contact**,
  then rise slowly over the remaining ~13 frames. The head picks up the lag automatically. The stomp should be felt
  on the frame the foot lands.

### roar (84 f, 2.8 s): APPROVED, with one should-fix
- This is the strongest clip. It follows the reference: a crouch with the head almost on the ground, a chest-led
  rise, the head arriving ~5 frames late, the jaw at 40, a jaw buzz and a tail-tip shiver through a 28-frame hold,
  then a 24-frame settle. The rise (f20→27, 0.23 s) is explosive but earned by the 20-frame crouch. All limits are
  respected (Head+Neck 24°, Chest 5°, Neck 8°).
- **Should-fix, silhouette in the crouch (f14-20):** the Spine pitches +16 nose-down, which already lifts the tail
  tip ~0.5. The tail pitch then adds another +10/+12 of curl upward, so the tail stands almost vertical and curls like
  a scorpion's (`pose_tq_roar_20`). A T-rex tail is a stiff counterweight. Set the crouch keys' tail pitch to
  **-4 / -6**, so the spine tilt alone raises it as a straight line ~20-25° up. This also stops the tail rising across
  the game camera.

### act_tailspin (76 f): MUST REPLACE
Three independent problems:
1. **Not unique, and it copies its own egg sibling.**
   - Raiju's `act_thunderflip`: "crouches low... EXPLODES upward into a full barrel roll with all four legs tucked,
     lands... holds a proud power pose (chest high, chin up, tail raised)".
   - The tailspin: crouch → hop → a 360 in the air with the legs tucked → land → a power pose with the chest up and
     chin high.
   - Only the rotation axis differs, and both pets are in the Storm egg. BlackDragon's `act_pearlchase` is also an
     airborne full corkscrew, and the stomp landing repeats LavaGolem's jump-smash.
   - The end pose (f44-60) also duplicates our own roar peak (compare `pose_tq_roar_32` with `tailspin_44`).
2. **No weight.** A 10-stud tyrant spins a full 360 in 12 frames (0.4 s, about 900°/s) and floats for ~0.47 s. That
   reads as a toy, and it undoes the heavy king the walk and roar build up.
3. **Footprint.** The yaw spins around the hips. The tail sweeps a circle of radius ~1.9 model units: ~9.4 studs at
   x1 and ~20 studs at x2.2. Pets stand right next to their owner, so this swats through the player's avatar and any
   neighbouring pet. Smaller issue: the yaw starts at f14 while the feet are still planted (the FK tuck keys begin at
   f18), so the feet twist on the ground on f15-17 before take-off.

**Replacement: `act_stormbreath`, "STORM BREATH" (the kaiju charge), ~100 f.**
No other pet in the roster has a breath act; I checked all 21 act docstrings. It stays planted and heavy, and the
ridge lights up from tail to crown, which is exactly what players see from behind. It also uses every VFX anchor this
model was built for (Bolt, Ridge1-3, Core, Crown, Breath). The feet stay planted for the whole clip: run
`plant_frames(k, range(0, n+1))`, no FK leg keys.

| frames | beat | keys (rot in deg; + = nose-down; Spine loc in model units) |
|---|---|---|
| 0-14 | **plant & glare** | Spine z -0.06, pitch +6; Chest +3; Neck +6; Head +8; jaw 3 (shut); tail pitch -4 (drags low); arms curl 20 |
| 14-44 | **charge: 3 pumps** at f20/30/40 | each pump: Spine z -0.06→-0.085→-0.06, Chest +3→-2 (chest swells), head drops 2° more per pump; tail goes **stiff and lifts 4° per pump** (-4→0→+4→+8, each=(0.2,0.45,0.75,1.0)); events `charge1` f20 (Bolt + Ridge3), `charge2` f30 (Ridge2 + Core), `charge3` f40 (Ridge1 + Crown). The light runs tail → head. |
| 44-52 | **inhale** | Spine -6, z -0.02; Chest -4; Neck -8; Head -14 (Head+Neck 22 ≤ 30); jaw 26; arms spread 12 |
| 52-56 | **fire** | the head snaps forward and down: Spine +4, Chest +2, Neck +4, Head +6, jaw 40; **recoil:** Spine loc y +0.04 (back), z -0.05, with the planted legs absorbing it; event `breath` f54 |
| 56-80 | **beam** | jaw 40 with a ±2 buzz every 3 f; head sweeps across the beam: Head yaw -12→+12 and Neck yaw -5→+5 (total ≤ 17); tail held straight and stiff (+4) with a Tail4 shiver of ±5; recoil eases (y +0.04→+0.01); event `breath_end` f80 |
| 80-90 | **snap & shake** | jaw shut by f83 (smoke puff); Head yaw +8 (f84), -6 (f87), 0 (f90); Spine z -0.03 (exhale) |
| 90-100 | settle | back to rest |

- Ease into the pumps, and use hard stops on f54 (fire) and f83 (jaw snap).
- Rename the action, the `k.events` key and anything in CreatureClips or Studio that references `act_tailspin`.
- **Return:** a pose sheet at f20, f40, f50, f54, f68 and f84, plus the collision and audit pass.

---------------------------------------------------------------------------------------------------------------------
## 3. Summary for the coordinator
- **Mesh: approved, 8.5/10.** It is now a real 1% secret. In-game it will look better still once the VFX on the
  Ridge, Crown, Core and Bolt anchors goes in. Remember that colours render ~0.6x darker in Roblox, so the HOT tips
  will need the glow help there.
- **Must-fix before shipping:** replace `act_tailspin` with `act_stormbreath`, as specified above.
- **Should-fix (small):**
  - idle: double the look-around yaw
  - walk: an asymmetric contact dip of 0.05
  - roar: crouch tail pitch -4/-6
- **Optional:** expose the full core diamond (throat start 0.45, or core `off` 0.06); raise the icon camera 8° for
  the crown.

---------------------------------------------------------------------------------------------------------------------
## 4. Final sign-off on the animation set (round 3b) - APPROVE

**Animation set: APPROVED.** With the model at 8.5/10, **Thunder Rex is signed off and ready to ship.**

What I checked:
- the new clip code (`idle`, `walk`, `roar`, `stormbreath`) in `pets/ThunderRex.py`
- `_pose_tq_sheet.png`
- the stormbreath frames f50, f56 and f78 at full size

The builder's pass is clean: `collision_free: true`, linear 0, loops closed, slide 0, ground_min_z ≥ -0.006.

- **act_stormbreath - APPROVED.** It matches the key table. It is now the only breath act in the roster, it stays
  planted and in place (no sweeping footprint), and it uses every VFX anchor.
  - Every limit holds: Neck ≤ 8°, Chest ≤ 5°, Head+Neck pitch-up 22°, yaw ±17°.
  - The fire snap (f52→54, recoil y +0.04 / z -0.05) and the beam sweep read clearly in the stills: a dark mouth
    interior, the jaw wide open and the core emblem visible.
  - The events (charge1-3, breath, breath_end, smoke) are on the right frames.
  - **The head-shake deviation is accepted, and it was correct.** My table broke the owner's "no head shakes" rule.
    The jaw snap, snort lift and exhale that replace it are better anyway.
- **idle - APPROVED.** The look-around is now ~±25° (Neck ±8, Head ~±17), within the yaw limit, so it reads from the
  game camera.
- **walk - APPROVED.** The asymmetric dip lands on the contacts (gait contact t=0 → f0/f16, deepest at ~f3-4/19-20,
  slow rise). It now reads as a stomp.
- **roar - APPROVED.** The crouch tail at -4/-6 keeps the tail a straight counterweight; there is no more scorpion
  curl.
- **Core:** with the throat strip starting at 0.45, the chest emblem is visible in every front pose.

Optional polish for a later pass (not blocking):
1. **Stormbreath inhale.** The rear-up takes 4 frames (f44→48, 0.13 s) before a 4-frame hold, so on a 10-stud body it
   can read as a flinch rather than a breath in. Moving the f48 key to f50 (6-frame rear, 2-frame hold, fire still at
   f54, events unchanged) makes it read as a real intake.
2. **Stormbreath pumps.** The pumps (Spine z -0.06↔-0.085, Chest 3↔-2) are subtle without VFX. If the ridge VFX ends
   up soft in-game, deepen them to z -0.10 and Chest -4.
3. **Idle look.** The swing from one side to the other (f50→58) is ~40° in 8 frames, which is quick for a heavy king.
   Moving the f58 key to f60 softens it.

Owner to-do (as for all pets):
- Studio import of `C:\cdimp\ThunderRex.fbx` as creator ZAB Studio.
- VFX Studio effects on Crown / Core / Breath / Bolt / Ridge1-3, driven by the stormbreath and roar events.
- Save + Publish.
