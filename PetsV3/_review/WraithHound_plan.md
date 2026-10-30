# WRAITH HOUND - concept plan v2 (Shadow Egg, MEDIUM-HIGH 10 %, area 5 Shadow / Void)

Planner: pet planner (concept only). The lead builds `pets/WraithHound.py` on the ShadePanther kit. Binding. Not built.

## v2 changes (from GLACIER_PLAN_REVIEW.md)
APPROVED WITH CHANGES, 6/10. Applied:
- Body (MUST 1): ASH (176,176,190) becomes lavender-ash (170,160,206), #AAA0CE (H 253, S 0.22). The ghost stays pale, with no plain grey.
- Saddle (MUST 2): SOOT (92,92,116) runs as a solid saddle along the spine, at least 18 % of the side view, not only the mane tips.
- Accent (MUST 3): INDIGO (120,84,240) becomes (100,120,240), #6478F0 (H 231). INDIGO_L (176,150,255) becomes (160,176,255),
  #A0B0FF (H 230). That is 40 degrees from ShadePanther VIOLET and 33 degrees from BlackDragon MANE (both in the Void egg).
- Known near match (added by the planner, for the step-1 check): INDIGO H 231 is 9 degrees from BlackDragon's INK body (dark
  indigo, same egg). The eyes are small and saturated, so check at 64 px.
- NICE: the mane stays SOOT blocks only; the ears stay as planned.
- Builder gates from review section 6 apply.

## 0. Facts
| | |
|---|---|
| Tier | Medium-high |
| Odds | 10 % (money x1.76) |
| Egg / area | Void (Shadow) Egg, area 5 |
| Rig | quad (lean hound, long legs) |
| Closest kit files | `pets/ShadePanther.py` (quad cat kit, Void egg). `pets/NightmareStallion.py` (long mane blocks, lag chains) |
| HEIGHT | 8.0 studs (top of the smoke mane) |
| Tris | 6-9k |

## 1. Read in one line
"A ghost hound: a lean lavender-ash hide, a soot saddle and a soot mane of stacked blocks that streams back like smoke, and purple-indigo eyes."
At 64 px: a lean hound with a dark saddle and a streaming mane, a long head and two indigo eye slits. It must NOT read as:
- ShadePanther (indigo-black big cat with violet crystals, pounce act). The Wraith is a hound with a lavender-ash hide and no crystals.
- NightmareStallion (charcoal horse, magenta flame mane, rear act). The Wraith is a hound, its mane is soot-grey and not pink.
- a cute dog. The head is a long wedge with a slant brow, and the mane is fierce.

## 2. Rarity ladder
- Medium-high (10 %). It must look bigger and stranger than Stallion (25 %) and Panther (50 %).
- Must be beaten by Black Dragon (9.5 %), Asparuh (4 %) and Weaver (1.5 %).
- Its mane, saddle and eyes carry it. No hero piece is needed.

## 3. Silhouette and anatomy (x H, H = 8.0 studs)
- Lean hound. Withers 0.56H. Body length 1.20H. Chest deep 0.34H. A waist tuck.
- Legs long: ground to elbow 0.42H. Feet narrow (1.0 x leg width). Four claws (BLACK).
- Head: a long wedge, 0.30H long, flat skull. Head top 0.64H with the ears.
- Ears: tall and pointed, 0.12H, pinned slightly back.
- Saddle: a solid SOOT band along the spine from the withers to the hips (at least 18 % of the side view).
- Mane: 3 rows of tapered SOOT blocks from the neck top to 1.0H, streaming back 0.30H. Blocks only, no strand fringe.
- Tail: long and low, 0.70H, with three SOOT blocks stepping down to the tip. A smoke tip (VFX).
- No box belly: the belly line rises from the chest to the flanks.

## 4. Palette (Blender RGB; body brightest channel 206 >= 170)
| Name | RGB | Hex | Where | Share (side) |
|---|---|---|---|---|
| ASH_LAV | 170,160,206 | #AAA0CE | body, legs, head (studded), lavender-ash | 40 % |
| MIST | 226,226,236 | #E2E2EC | underside, muzzle, chest, inside legs | 12 % |
| SOOT | 92,92,116 | #5C5C74 | spine saddle (at least 18 % of the side view), mane blocks, ears, tail | 26 % |
| INDIGO | 100,120,240 | #6478F0 | THE accent: eye slits, mane tip accents (smooth) | 6 % |
| INDIGO_L | 160,176,255 | #A0B0FF | eye rims, brow highlights | 2 % |
| BLACK | 14,14,22 | #0E0E16 | nose, claws, eye pupils | 4 % |
| IVORY | 238,234,220 | #EEEADC | two small fangs | 1 % |
| MOUTH | 56,28,70 | #381C46 | mouth cavity | 1 % |

- In game about (102,96,124) for the body: a dusky lavender ghost. The soot saddle and mane are the dark parts.
- Accent family: WRAITH INDIGO (a blue-violet, S 0.61). Nearest in the Void egg: ShadePanther VIOLET (40 degrees), BlackDragon MANE (33 degrees), BlackDragon INK (9 degrees, dark body; check at 64 px).
- Gold: none.

## 5. Part list (x H)
- Torso: chest block 0.34H deep x 0.40H wide x 0.70H long, `rnd 0.30`, belly tuck, bottom taper (0.85, 0.90).
- Saddle: a SOOT band over the spine from the withers to the hips (0.18H tall, flush to the ASH_LAV flanks).
- Head: wedge skull (0.30H long, 0.14H wide), flat top, cheek blocks (ASH_LAV), MIST muzzle (0.10H).
- Ears (x2): 0.12H tall, SOOT backs, ASH_LAV fronts, pinned back 12 degrees.
- Mane: 3 rows of tapered SOOT blocks (each 0.14H to 0.22H long), from the nape to the tail base, tips point back and up. Row 1 at the neck, Row 2 at the withers, Row 3 at the back. Blocks overlap by 30 %.
- Legs (x4): 2 blocks each (upper 0.22H, lower 0.20H), feet 1.0 x leg, 4 BLACK claws (0.04H).
- Tail: 4 segments, 0.70H total, SOOT tuft at the tip.
- Eye accents: INDIGO slits with INDIGO_L rims (flush inlays).
- Hero piece: none. Signature shape = the streaming soot mane.
- Stud skin on the body, the head, the legs, the saddle. Not on the mane tips (smooth, `role detail`), the eyes, the claws, the fangs.

## 6. Face spec
- Eyes: INDIGO slit (0.08H x 0.02H), INDIGO_L rim, BLACK slit pupil, under a SOOT brow (heavy, 20 degrees inner-down). No glow mesh; the glow is VFX.
- Nose: BLACK, flat, 0.04H wide.
- Mouth: closed, MOUTH line, two IVORY fangs (0.05H).
- No glint, no round eyes.

## 7. Clips (30 fps)
- **idle (120 f loop): "scent drift".** The nose lowers and lifts (head pitch +/-10 degrees, within 30). The ears flick back and forward (f40, f80). The mane sways: each row lags 3 frames behind the one before (a slow drift, +/-4 degrees). Settles.
- **walk (30 f loop, lean trot-walk):** long steps. The mane lags 4 frames behind the body. Walk slide ~0.
- **roar (60 f): "mane flare".** f0-14: the mane rows lift outward 25 degrees (3 rows, lag 2 frames), the ears go back. f14-26: the chest pushes forward 0.05H; the head pitches down 10 degrees, the jaw opens 25 degrees, a silent snarl with the fangs out. f26-44: hold; the mane trembles 2 degrees. f44-60: the mane falls back, the jaw closes. No paw swipe (that is ShadePanther's roar).
- **act_smokecloak (100 f, in place): "the cloak spreads".** Beats:
  1. f0-18: the hound crouches flat (body lowers to 0.75H, legs bend 30 degrees).
  2. f18-40: the mane lifts and fans out wide (each row to 40 degrees, lag 3 frames). Event `cloak` f28 (smoke puff at each mane tip).
  3. f40-68: hold the fan, drifting slowly (mane sway +/-6 degrees, two cycles). Event `drift` f54.
  4. f68-86: the mane folds back in and the hound rises to standing (legs straighten, body rises back to 1.0 height).
  5. f86-100: the mane settles to rest. Exact rest pose.
  Limits: the feet stay planted in every frame; ground_min_z >= -0.02 at the crouch; no airborne movement.

## 8. VFX anchor bones (named after the effect; parent bone in brackets)
- `FX_SmokeWisp_1` to `FX_SmokeWisp_3` [Mane_Tip_1 to Mane_Tip_3]: smoke wisps on the tips, on the cloak.
- `FX_IndigoWisp_L` [Eye_L], `FX_IndigoWisp_R` [Eye_R]: a small INDIGO wisp (VFX, no glow mesh).
- `FX_SmokePuff_FL`, `FX_SmokePuff_FR` [Paw_FL, Paw_FR]: smoke puff on the crouch.
- `FX_SmokeTrail` [Tail_Tip]: smoke trail.
- `FX_Fog` [Chest]: faint fog on the roar.

## 9. Distinctness
- ShadePanther (Void, indigo-black panther): violet crystal clusters, pounce act. The Wraith is a lavender-ash hound with a soot saddle and mane, and its act is a cloak spread.
- NightmareStallion (Void, charcoal horse): magenta flame mane, rear act, buck. The Wraith is a hound with a soot mane and no pink.
- BlackDragon (Void, violet serpent): not a quad. Its gold antlers and pearl are not on the Wraith. Near match: INK body, see the v2 note.
- AbyssWeaver (Void, dark spider): not a quad.

## 10. Animation references
TBD by builder. Suggested tags: "wolf sniff", "dog ears back", "hound run".

## 11. Reviewer gates
1. 64 px: the long hound head, the soot saddle, the streaming mane and two indigo slits read.
2. Game camera: the lavender-ash body reads as a dusky ghost (not a plain grey); the soot saddle and mane are the dark parts.
3. The mane and saddle are blocks (no fringe, no flat cloth, no mesh wisps).
4. The act is a cloak spread; it is not a pounce, not a rear, not a stalk.
5. Builder gates (review section 6): step-1 tris, collision_free, ground_min_z >= -0.02, linear 0, loops closed; icon strip at 64 and 128 px next to ShadePanther and BlackDragon; value shares (SOOT saddle >= 18 %); pose sheet of the cloak beats.
