# VOLT RHINO - concept plan v2 (Thunder Egg, HIGH 6 %, area 3 Thunder / Storm)

Planner: pet planner (concept only). The lead builds `pets/VoltRhino.py` on the ThunderBull kit. Binding. Not built.

## v2 changes (from GLACIER_PLAN_REVIEW.md)
APPROVED WITH CHANGES, 7/10. Applied:
- Body (MUST 1): IRON (176,180,186) is a plain grey plate. IRON_D (104,110,120) now covers the back, the shoulder shield and the
  skin folds: at least 25 % of the side view. IRON stays on the flanks and legs. The PALE belly stays.
- Roar (MUST 2): the horn-to-the-sky roar keeps the horn up, but the head pitch-up is 16 degrees or less (was 22). The snout stays
  forward during the bellow. Raiju's howl is chin-to-sky; the rhino must not read as that.
- HEIGHT (NICE): 9.0 becomes 8.5 (the Thunderbird is 8.5 and rarer than the rhino's 6 %).
- Kept: the VOLT lime (210,255,80) accent, accepted (review ruling 9).
- Builder gates from review section 6 apply.

## 0. Facts
| | |
|---|---|
| Tier | High |
| Odds | 6 % (money x2.10) |
| Egg / area | Storm (Thunder) Egg, area 3 |
| Rig | quad (heavy, columnar legs) |
| Closest kit file | `pets/ThunderBull.py` (heavy quad, horn kit, charge pattern) |
| HEIGHT | 8.5 studs (top of the lightning horn at rest) |
| Tris | 8-11k |

## 1. Read in one line
"A charging armoured rhino in iron-grey studded hide with dark plate folds, and one huge ivory horn crackling with volt-lime lightning."
At 64 px: a dark-backed grey barrel with a long pale horn pointing forward and a small brow horn. It must NOT read as:
- ThunderBull (navy-violet bison, cape, big horns, charge act). The rhino is iron-grey with one lightning horn and no cape.
- Raiju (storm wolf, blue). The rhino is a heavy quad with no tail fan.
- Thunderbird or StormWyvern (birds and wyverns). The rhino is a four-legged mammal.

## 2. Rarity ladder
- High (6 %). It must beat Wyvern (14 %), Bull (25 %) and Raiju (50 %) on look.
- Must be beaten by Thunderbird (4 %) and Thunder Rex (1 %).
- The High tier needs a clear signature: the lightning horn.

## 3. Silhouette and anatomy (x H, H = 8.5 studs)
- Barrel body. Chest 0.38H deep, body length 1.25H, withers 0.55H. Belly tapered, not a box.
- Head low and forward, 0.32H long. Head top 0.55H.
- Main horn: from the nose, 0.32H long, pointing forward and slightly up, with a lightning inlay line down it.
- Brow nub: a small horn behind the eyes (0.12H), IVORY.
- Shoulder shield: a heavy plate fold over the shoulder (IRON_D).
- Skin folds: 3 folds (shoulder, behind the shoulder, the flank), each a dark studded band over the back and flank.
- Legs: 4 pillars. Ground to shoulder 0.36H, leg width 0.22H. Feet 3-toe pads (DARK toenails).
- Tail: short whip, 0.25H, with a dark tuft.

## 4. Palette (Blender RGB; body brightest channel 186 >= 170)
| Name | RGB | Hex | Where | Share (side) |
|---|---|---|---|---|
| IRON_D | 104,110,120 | #686E78 | back, shoulder shield, skin folds, brow, leg plates (at least 25 % of the side view) | 26 % |
| IRON | 176,180,186 | #B0B4BA | flanks and legs (studded) | 40 % |
| PALE | 222,224,228 | #DEE0E4 | belly strip (follows the slope), inside the legs | 10 % |
| HORN_IVORY | 240,236,222 | #F0ECDE | horn body and brow nub (smooth) | 6 % |
| VOLT | 210,255,80 | #D2FF50 | THE accent: lightning inlay on the horn and shoulder bolts, eye slits | 4 % |
| BLACK | 14,14,22 | #0E0E16 | toenails, nostrils, eye sockets | 4 % |
| MOUTH | 86,18,30 | #56121E | mouth | 1 % |

- In game about (112,116,121) for the flanks: a dark iron grey. The back is darker still.
- Accent family: VOLT LIME. Nearest: Thunderbird BOLT (21 degrees, a sibling), Mossback EYE_HOT (Grass, d 1, cross-egg). Accepted (review ruling 9).
- Gold: none.

## 5. Part list (x H)
- Torso: chest block 0.38H deep, body block 1.0H, belly taper, `rnd 0.30`.
- Back and shoulder shield: IRON_D blocks over the spine and shoulder, 0.22H long, 0.06H proud.
- Skin folds: 3 bands (IRON_D), flush inlays, 0.02H thick, across the back and flank.
- Head: wedge skull 0.32H long, a brow ridge (IRON_D), nostrils BLACK.
- MAIN HORN (the hero of the High tier): IVORY base block 0.05H wide, tapering to a tip; 0.32H long; a VOLT lightning inlay in 3 zigzag segments down the upper face (flush, 0.012H). Keep the zigzag gentle (no Thunderbird kink).
- Brow nub: HORN_IVORY, 0.12H, behind the eyes.
- Legs (x4): 2 blocks (upper 0.18H, lower 0.18H), feet 3 DARK toes.
- Tail: 3 segments, 0.25H, DARK tuft.
- Shoulder bolts: 2 VOLT flush inlays on the shoulder shield (small zigzags).
- Hero piece: the lightning horn. No gold.
- Stud skin on the body, head, legs. Not on the horn, the inlays, the toenails.

## 6. Face spec
- Eyes: small, fierce. VOLT slit (0.05H x 0.015H) in a BLACK socket, tilted 15 degrees, inner corner low, under an IRON_D brow ridge.
- Nostrils: two BLACK slits on the front of the snout.
- Mouth: closed, MOUTH line.
- No glint, no round eyes.

## 7. Clips (30 fps)
- **idle (120 f loop): "horn tilt".** The weight shifts, one foreleg lifts 0.02H and sets down. The horn tilts side to side slowly (yaw +/-6 degrees, the head bone). The lightning inlay flickers (VFX). The tail flicks once at f90 (not a fly swat). Settles.
- **walk (40 f loop, quad walk):** heavy, slow, steady. Body rocks 0.02H per step. Walk slide ~0.
- **roar (60 f): "horn-to-the-sky bellow" (review 2.9 MUST 2).** f0-14 the head lifts 16 degrees (the pitch-up limit, not 22). The snout stays forward (no chin-to-sky). f14-40 the mouth opens and the bellow pulses three times (events `bellow1` f20, `bellow2` f28, `bellow3` f36 on `Mouth`, a VFX ring). The legs stay planted. f40-60 the head lowers and the mouth closes.
- **act_horntap (100 f, in place): "lightning taps".** Beats:
  1. f0-22: the head lowers and the horn comes down to the ground (pitch down 25 degrees).
  2. f22-56: the horn taps the ground three times, each tap at f30, f42, f54 (events `tap1`, `tap2`, `tap3`; a small bolt VFX runs along the ground from `Horn_Tip`).
  3. f56-70: the head flicks up and the horn snaps to the sky (fast, 6 frames).
  4. f70-86: the horn holds up and the lightning inlays flash in turn (VFX, event `charge`).
  5. f86-100: the head returns to rest. Exact rest pose.
  Limits: the legs stay planted in every frame; ground_min_z >= -0.02; the horn tip is the only ground contact.

## 8. VFX anchor bones (named after the effect; parent bone in brackets)
- `FX_BoltTrail` [Horn_Tip]: small spark puff on each tap and a bolt trail along the ground.
- `FX_ChargeGlow` [Horn_Base]: a glow on the charge event.
- `FX_BoltSpark_L` [Shoulder_L], `FX_BoltSpark_R` [Shoulder_R]: small sparks on the bolt inlays.
- `FX_DustTap` [Foot_FL]: dust puff on the taps' stance.
- `FX_BellowRing` [Mouth]: a bellow ring on each pulse.

## 9. Distinctness
- ThunderBull (Thunder, navy-violet bison, cape, horns): the rhino is iron-grey, has one lightning horn, no cape, and the horn-tap act.
- Raiju (Thunder, storm wolf): a wolf with bolts and a chin-to-sky howl. The rhino has a horn, a snout forward, and a 16-degree bellow.
- StormWyvern (Thunder, violet wyvern): membrane wings, red accent. The rhino is a quad with a grey body.
- Thunder Rex (Thunder, secret): storm-blue shells and cyan crystals. The rhino is grey, with volt lime.

## 10. Animation references
Final list, 2026-10-28. The full notes are in `VoltRhino/ANIM_REFS.md` ("Per-animation references").

| clip | ref (tag / source) | frames | taken |
|---|---|---|---|
| walk | **animationreference.org `/tags/elephants`**, "Video by projectarcheology" (stepped from the tag page's preview, 10.0-11.4 s at 0.2 s; no clip open) | the adult's fore swings ~0.4 s, one every ~0.6 s → duty ≈ 0.67; low foot clearance; the body leans onto the planted fore; the head dips on each fore landing | 40 f cycle, duty 0.70, lift 0.08, roll to the planted side |
| walk | Sakugabooru #144564, *The Jungle Book*, Colonel Hathi's march (`walk_cycle`, `animals`; `/tags/walk-cycle` searched) | stride ≈ 30 f at 24 fps = 37.5 f at 30; duty ≈ 0.70-0.75 | 40 f cycle, duty 0.70 |
| walk | Muybridge "Walking bison" (Wikimedia) | hind swings photos 1-2 / 7-8 / 13-14 / 19-20; fore swings 3-5 / 9-11 / 15-17 / 21-23 | lateral BL, FL, BR, FR; low head; tucked fore swing |
| idle | animationreference.org `/tags/elephants` (1 clip): "Video by projectarcheology" (tags animals, body-mechanics; real footage, 13.4 s; stepped from the tag page's own preview video, no clip open used) + the bison plate | adult elephant 10.6-13.2 s: ears held out, trunk swings slowly toward the calf (10.6-12.0 s); body leans before the near foreleg moves (12.0-12.3 s); low foreleg lift and plant 12.3-12.6 s (~0.3 s = 9 f at 30 fps) | the weight shifts OFF the lifting foreleg (shift peak on the far side at f38, mid-lift); the lift was 0.032, then 0.060 (r2), and is now 0.120 with the sole kept near flat (3 deg toe) so it reads at phone scale (final85 r3 MUST 3; the elephant's lift is low, but the game camera needs about 10 px); the head and ears keep moving while the body is still; the snort is a 6 deg head toss f71-73 that settles at f76. No-fit note: `/tags/animals` (533) and `/tags/creature-animation` (2,415) were cross-checked by thumbnail md5 against Sakugabooru's western heavy-animal posts (Ice Age, Snow Bear, Mickey's Elephant, Ferdinand): none of those is on the site |
| roar | W0 Sakugabooru #174333, *Wolf's Rain* #30 (`/tags/wolfs-rain`) + 1014 top #3 Sea Beasts | onset 16 f at 24 fps = 20 f at 30; hold ≥ 30 f | the jaw lags the head, then stays open through the pulses |
| act_horntap | Muybridge Plate 700 "Buffalo galloping" (Wikimedia; `/tags/kaiju-no-8` searched: 6 clips, none fits) + 1014 Mantis #5 / #6 + Leviathan #9 | photos 9-16 | the braced strike; the cocked tell + 2-3 f strike; the fast snap up; the slow return |

## 11. Reviewer gates
1. 64 px: the dark-backed grey barrel and the long pale horn read. The lime lightning reads on the horn.
2. Game camera: the back and shoulder shield are darkest; the horn is the brightest part.
3. The act is a horn tap with bolts on the ground. It is not a charge, a hoof scrape or a stomp.
4. The roar lifts the horn with a head pitch-up of 16 degrees or less, and the snout stays forward. Compare with Raiju's howl at 64 px.
5. Builder gates (review section 6): step-1 tris, collision_free, ground_min_z >= -0.02, linear 0, loops closed; icon strip at 64 and 128 px next to ThunderBull and Raiju; value shares (IRON_D >= 25 % of the side view); pose sheet of the horn tap.
