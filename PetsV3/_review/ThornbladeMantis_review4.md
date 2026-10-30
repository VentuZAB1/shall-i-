# Thornblade Mantis - art director review 4 (2026-10-14) - CLIPS ROUND 2: APPROVED, export after F1

**Verdict:** all four clips are approved. One small timing fix (F1, the two 1-frame snaps) must go in before export.
After F1, re-run the gate and **export without another review round**. Attach the F1 renders to the export report.
The model stays approved at 8.5/10. **The Thornblade Mantis is signed off as a 2% secret once F1 is in.**

What I looked at:
- `act_thornstrike` in `pets/ThornbladeMantis.py`
- `_act_r3`, `_groom_roar_r3`, `_roar30_eye` and the f50-57 un-cross renders
- my own 520 px poses (rig + anim built without `write_clips`), in `C:\Users\ventu\AppData\Local\Temp\mantis_rev\c2\`
  (`S_strike.png`, `S_misc.png`):
  - thornstrike f20/25/27/35/44 in game, tq and side
  - idle f84, act f52/54/68 and roar f30 in front, tq and game

Your gate numbers: collision_free, linear 0, loops closed, slide 0, ground = feet only, Blade min z 0.27 (was -0.014).
All good.

---------------------------------------------------------------------------------------------------------------------
## 1. Per clip
| clip | verdict | notes |
|---|---|---|
| idle | **APPROVED** | The groom now reads: the left blade swings in across the jaws, and the head turns down to it (front f84) |
| walk | **APPROVED** | No change |
| roar | **APPROVED** | C3 landed. The eye-spots now read as eyes (pale rim, ruby, black slit) in tq, and as visible marks on the dark fans from the game camera |
| act_thornstrike | **APPROVED, with F1** | The re-stage works. See below |

**act_thornstrike re-stage:**
- **The cock reads from behind.** At f20-24, the two raised scythes stand beside the crown in the game view. That is
  the tell the round-1 version lacked.
- **The reach (f25) is a real mantis strike.** The forelegs shoot forward nearly straight at chest height. In side and
  tq the gold tibiae point at the target, and from the game camera a gold blade shows past the head.
- **The X and the hold read** in front and tq. From the game camera they are mostly hidden under the head. That is
  acceptable, because the cock and reach carry the act from that view.
- **Nothing touches the ground.**

## 2. Rulings on your deviations
1. **Cock up 70 / fore -30 / Chest -8 (not up 30 / fore +15 / Chest -10): APPROVED.** The target was the knee
   spines above the eye tops (z 1.29 vs 1.12), not the literal numbers. The look is right.
2. **Reach with Spine y -0.05 and the coxa swung back -40: APPROVED.** The tips are 0.55 in front of HC, inside the 0.6
   limit, and the knee angle is 168° with no hyperextension.
3. **X-hold with the tibiae open ~76-92° (clutch = a 7° close): APPROVED.** A tibia-on-tibia X is the readable one.
   Elbows meeting at the midline would look broken.
4. **Un-cross in reverse arrival order (R drops to up -50 at f51-53, then L leaves): APPROVED.** In front f52 it
   reads as one blade lowering, then the other. That is a natural unclasp, and it is collision-free.
5. **Groom variant** (out -15, fore -10, head -6 / yaw 8; the tibia about 0.1 in front of the mandibles instead of
   0.02-0.04): **APPROVED.** It is the closest collision-free pose, and in front and tq the gold tibia clearly crosses
   in front of the jaws with the head turned to it.
6. **C3 eye-spots exactly as specified: APPROVED.**
7. **`_tools/mantis_fk.py` and `pose_try pts=`:** good tooling. Keep them for the next secrets.

---------------------------------------------------------------------------------------------------------------------
## 3. F1 - make both snaps 2 frames, with an in-between (must, small)
Two moves happen in ONE frame:
- **f24 → f25 (strike 1):** coxa +70 → -40 (110°) and tibia -9 → 130 (139°).
- **f33 → f34/35 (strike 2):** about 40° coxa + 40° yaw + 80° tibia, per arm.

**Why it matters:**
- The Lua clip is sampled per frame, and Roblox interpolates between samples. A 110° swing between two adjacent
  samples plays as a pop or teleport, not a lash.
- The sub-frame halfway pose is never collision-checked: the raised blade swings forward past the eye dome in that
  gap.
- Your own reference ("Attack": smear f15, full reach f16) is a 2-frame snap.

**Fix:** add one in-between key at about 60% of each move. It then becomes a checked frame, and the eye reads it as
the smear.

| f | L | R | notes |
|---|---|---|---|
| 25 | in-between: about 60% from the f24 tell to the reach (≈ up -2, out 14, fore -10, blade 75) | same | `strike1` event stays at f25 |
| 26 | REACH (-40, 6, 8, 130) | same | Body y -0.05 moves from f25 to f26 |
| 28 | SNAP shut (-25, 6, 25, 10) | same | Shift the recoil by +1 (f30 / 32-34) |
| 35 | in-between toward the X (60%) | half-cock | `strike2` event moves to f35 |
| 36 | X pose | in-between | |
| 37 | X | X pose | `finish` moves to f37. The hold runs f37-50 unchanged |

Use `pose_try` / `mantis_fk` to make sure the two in-between poses are clean (Fore/Blade vs Head and Jaw). If an
in-between clips the eye, give it a bit more `out` (+4) rather than less raise.

**After F1:** run headless_clips (collision_free, ground_min_z, audit, events), then
`headless_full.py -- ThornbladeMantis - 1 export`. In the export report, include:
- the tq + game renders of f25 and f26
- the updated event table

---------------------------------------------------------------------------------------------------------------------
## 4. Owner to-do (after export)
- Studio import of the FBX as creator **ZAB Studio**.
- VFX Studio effects:
  - **Crown:** a secret sparkle aura
  - **EyeSpot_L/R:** a flash on roar `display` f24
  - **BladeTip_L/R:** slash trails on `strike1` / `strike2`
  - optional: a small hit spark on the snap frame
- Wire the Grass-egg odds (2%), the Index portrait (`ThornbladeMantis_icon.png`) and the roar/act events in
  CreatureClips.
- Save + Publish.
