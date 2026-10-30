# ECLIPSE SERAPH - concept plan v2 (Celestial Egg, MYTHIC 0.1 %, area 6 Celestial)

Planner: pet planner (concept only). The lead builds `pets/EclipseSeraph.py`. Binding. Not built.
It must beat Cosmic Leviathan (1 %), Celestial Dragon (13 %), Griffin (27 %) and Solar Lion (54.9 %) on look.

## v2 changes (from GLACIER_PLAN_REVIEW.md)
APPROVED WITH CHANGES, 7/10. Applied:
- HEIGHT (MUST 1): 11.0 becomes 11.5. Tied with the Frostcrown Dragon (also 11.5), above ForestStag (11.0).
- Halo (MUST 2): the open annulus is replaced by a SOLID OBSID disc (the centre is filled). A GOLD rim band of 0.02H. A BLOOD ring just
  inside the rim, on the disc face. The open ring read as Cvetibara's brass ring from above.
- Body (MUST 3): MOON_IVORY (226,222,236) becomes lilac ivory (232,208,240), #E8D0F0 (H 285, S 0.13). IVORY_D shading stays.
- Six-wing gate (MUST 4): kept. Step-1 build of the three pairs. Report the tris count and a 64 px read. Target 13k, ceiling 15k.
  The fallback rule is written in section 0 (owner decision).
- NICE: the lower pair (0.6H) is small, and it is tucked at the flank. The read is two big pairs plus a tuck.
- Builder gates from review section 6 apply.

## 0. Facts and the six-wing RULE
| | |
|---|---|
| Tier | MYTHIC (eclipse halo, gold rim as the hero) |
| Odds | 0.1 % (money x8.80) |
| Egg / area | Celestial Egg, area 6 |
| Rig | wing-quad flyer: a quad lion body (SolarLion kit) with THREE wing pairs (the Griffin / CelestialDragon wing chain) |
| Closest kit files | `pets/SolarLion.py` (lion quad, mane, sunburst pattern). `pets/CelestialDragon.py` (wingquad, halo/crown anchors). `pets/Griffin.py` (wingquad) |
| HEIGHT | 11.5 studs (top of the halo rim) |
| Wingspan | 2.6 x H, tip to tip (all six wings) |
| Tris | 13k target, 15k ceiling |

**SIX-WING RULE (review section 1 gate, written here as the build rule):**
1. The step-1 build has three wing pairs. Report the tris count and a 64 px read before the full build.
2. If the step-1 tris are over 15k, OR the 64 px read is a blob (the three pairs merge into one silhouette, and the six wings cannot be counted), the fallback is FOUR wings: the upper and middle pairs only, with the lower pair removed.
3. The four-wing fallback needs the owner's OK before it is built. The owner decides (GLACIER_CONCEPTS.md, owner decisions).
4. Until the owner decides, the build stays six-wing.

## 1. Read in one line
"A six-winged lion-angel: a lilac-ivory lion with an obsidian mane and wing tips, three pairs of feather wings stacked like a seraph, and a solid black eclipse halo with a gold rim and a blood-red corona above its head."
At 64 px: a pale lion with a dark mane ring and six wings fanned out, with a dark disc above the head that has a bright gold rim. It must NOT read as:
- Solar Lion (tawny lion, gold sun-ray mane, sunburst act). The Seraph is pale lilac-ivory, with an obsidian mane, six wings and a dark disc, not a sun.
- Cvetibara (capybara with a brass halo ring, bloom act). The Seraph's halo is a solid black disc, not a brass ring.
- Celestial Dragon (indigo wingquad with a moon crescent). The Seraph is a lion, with six wings and a red corona.
- Griffin (brown eagle-lion). The Seraph is pale, and its wings are feather-angel wings, not eagle wings.

## 2. Rarity ladder
- Mythic (0.1 %). It beats every Celestial pet: Solar Lion (54.9 %), Griffin (27 %), Celestial Dragon (13 %), Cvetibara (4 %) and Cosmic Leviathan (1 %).
- Must look at least as strong as the Frostcrown Dragon (the other mythic).
- Nothing in the Celestial egg is rarer or above it.

## 3. Silhouette and anatomy (x H, H = 11.5 studs)
- Lion body: withers 0.58H, chest 0.38H deep, body length (chest to rump) 1.25H. A tucked waist; no box belly.
- Head: lion head 0.26H wide, muzzle 0.12H. The halo floats above the head. The mane frames the face in three rings (obsidian).
- Mane: 3 rings of stacked OBSID blocks, outer ring 0.18H deep, around the head and shoulders.
- Wings: SIX, in three pairs fanned from the shoulders and the back.
  - Upper pair: the main wings, span 1.3H each side, feather rows (3 rows).
  - Middle pair: 0.9H span each side, 2 rows.
  - Lower pair: 0.6H span each side, 2 rows, tucked at the flank (not fanned out).
  - The upper and middle pairs overlap by 25 % and fan back. The lower pair tucks in at the flank. The read is two big pairs plus a tuck.
- Halo: a SOLID black eclipse disc, 0.50H across, 0.04H thick, tilted 20 degrees, floating 0.20H above the head on a Halo bone. A GOLD rim band of 0.02H on the outer edge. A thin BLOOD corona ring just inside the rim, on the disc face.
- Legs: four lion legs, 2-bone, 0.30H upper, 0.30H lower, paws with 4 claws.
- Tail: long, 0.85H, with an OBSID tuft.

## 4. Palette (Blender RGB; body brightest channel 236 >= 170)
| Name | RGB | Hex | Where | Share (side) |
|---|---|---|---|---|
| MOON_IVORY | 232,208,240 | #E8D0F0 | body, legs, head (studded; lilac ivory) | 40 % |
| IVORY_D | 190,184,206 | #BEB8CE | shading, belly lines, the inner wing bars | 10 % |
| OBSID | 60,60,84 | #3C3C54 | mane rings, wing tips, the solid halo disc, tail tuft | 14 % |
| WING_IN | 238,236,250 | #EEECFA | inner wing feathers (smooth) | 8 % |
| BLOOD | 255,84,88 | #FF5458 | THE accent: eye slits, the corona ring on the halo disc | 4 % |
| GOLD | 255,196,50 | #FFC432 | THE hero: the gold rim of the halo (house gold, crown only) | 2 % |
| BLACK | 14,14,22 | #0E0E16 | claws, pupils, nose | 3 % |
| IVORY | 238,234,220 | #EEEADC | fangs | 1 % |
| MOUTH | 96,26,30 | #601A1E | mouth | 1 % |

- In game about (139,125,144) for the body: a mid lilac-grey lion. The OBSID mane and halo are the darkest parts.
- Three bands: OBSID (dark mane, halo, wing tips) / MOON_IVORY (body) / GOLD + BLOOD (halo rim and eyes).
- Accent families: BLOOD corona (red-rose) and the gold halo rim. Nearest: Ivonrath FLAME/RED (Fire, d 2, cross-egg), Cerberus RED (Fire, d 4, cross-egg). Accepted (review ruling 9).
- Gold: house gold on the halo rim only (2 %). Solar Lion's gold is a mane tip, not a rim.
- No brass halo (Cvetibara), no moon crescent (Celestial Dragon), no sun rays (Solar Lion), no azure stars (Leviathan).

## 5. Part list (x H)
- Torso: chest block 0.38H deep, body block 1.25H long, waist tuck, `rnd 0.30`.
- Head: lion skull 0.26H wide, muzzle block 0.12H, cheek blocks (MOON_IVORY), nose BLACK.
- Mane: 3 rings of OBSID blocks (outer 0.18H, middle 0.12H, inner 0.06H), studded, stacked.
- Wings (x6): wing3 kit for the upper pair (coverts MOON_IVORY, secondaries IVORY_D, primaries OBSID tips). Middle and lower pairs: 2 rows each (WING_IN inner, OBSID tips). Feather blocks with a saw edge, smooth.
- HERO halo:
  - Disc: a SOLID OBSID disc, 0.50H across, 0.04H thick (filled, not an annulus).
  - Gold rim: GOLD band on the outer edge, 0.02H wide.
  - Corona: a thin BLOOD ring on the disc face, just inside the rim, 0.015H wide.
  - Mounted on a Halo bone 0.20H above the head.
- Legs: 4 x 2 blocks, paws with 4 BLACK claws.
- Tail: 4 segments, 0.85H, OBSID tuft at the end.
- Hero piece: the solid eclipse halo with its gold rim. The six wings are the second big read.
- Stud skin on the body, head, legs, mane (rows), and the wing bases. Not on the halo, the corona, the feathers, the claws.

## 6. Face spec
- Eyes: fierce slits, BLOOD (0.08H x 0.02H), BLACK slit pupils, under an OBSID brow ridge (20 degrees inner-down). No glint, no round eyes.
- Nose: BLACK, flat.
- Mouth: closed or open, MOUTH cavity, two IVORY fangs (0.08H upper), no smile.
- The OBSID mane frames the face.

## 7. Clips (30 fps; no spin, no flip; six wings never pass through each other or the body)
- **idle (120 f loop): "halo drift".** The halo tilts 5 degrees side to side (Halo bone). The six wings breathe: upper pair lifts and falls (f10-60), middle and lower pairs lag by 4 frames. The head turns slowly (yaw +/-10 degrees, neck +/-8). A slight blood-corona pulse (VFX) at f80. Settles.
- **walk (40 f loop, quad walk):** the wings fold to half-open. The halo follows the head with a lag of 3 frames. Walk slide ~0.
- **fly (flap loop, six wings):** the upper pair flaps; the middle and lower pairs flap 4 frames behind. Legs pump. Takeoff event `launch`, land event `touch`. The wings never cross the body.
- **roar (66 f): "halo lift".** f0-14: the halo lifts 0.10H on its bone and tilts forward 25 degrees. The head rises 15 degrees (pitch up, within 30). f14-30: the jaw opens, the mane rings flare out 10 degrees. Event `roar` f24 (corona ring at `Mouth`). f30-50: hold; the wings open to half. f50-66: the halo settles back, the head returns, the jaw closes.
- **act_wingcascade (110 f, in place): "six-wing cascade".** A ripple runs through the wings, one pair after the other. Beats:
  1. f0-14: the head lowers 6 degrees and the halo sinks 0.05H (the Seraph bows its crown).
  2. f14-36: the upper pair lifts and ripples from the wing tip to the root (each feather row lags 2 frames). Event `ripple1` f22.
  3. f30-52: the middle pair follows, lag 4 frames. Event `ripple2` f40.
  4. f44-64: the lower pair follows, lag 4 frames. Event `ripple3` f54. The six wings hold a full fan for 6 frames at f62.
  5. f64-110: a reverse ripple (the lower pair folds first, then the middle, then the upper). The halo rises back to level, the head lifts, and the body settles to the exact rest pose.
  Limits: pitch-down <= 30; no spin; no flip; the wings never through each other; ground_min_z >= -0.02 at the bow; collision 0 at step 1.

## 8. VFX anchor bones (named after the effect; parent bone in brackets)
- `FX_CoronaSparkle` [Halo]: corona sparkle and a soft pulse on the roar and cascade events.
- `FX_FeatherSparkle_A_L`, `FX_FeatherSparkle_A_R` [Wing_A_L/R, upper pair]; `FX_FeatherSparkle_B_L`, `FX_FeatherSparkle_B_R` [Wing_B_L/R, middle pair]; `FX_FeatherSparkle_C_L`, `FX_FeatherSparkle_C_R` [Wing_C_L/R, lower pair]: feather-tip sparkle on each ripple.
- `FX_CoronaRing` [Mouth]: corona ring on the roar.
- `FX_HaloDust` [Mane_Top]: small dust on the halo lift.
- `FX_StarSparkle` [Tail_Tip]: star sparkle.
- The Celestial sparkles preset is allowed on the body; keep it small.

## 9. Distinctness
- SolarLion (Celestial, tawny lion, gold sun-ray mane, sunburst act): the Seraph is pale lilac-ivory, with dark mane rings, six wings, a solid dark halo, and the cascade act.
- Griffin (Celestial, brown eagle-lion, mantle act): the Seraph is a lion with angel wings, not an eagle.
- CelestialDragon (Celestial, indigo wingquad, moon crescent, eclipse act): the Seraph is a lion, has six wings, a dark halo and a red corona. Its act is not a tail arc.
- Cvetibara (Celestial, brass halo, bloom act): the Seraph's halo is a solid black disc with a gold rim, not a brass ring.
- CosmicLeviathan (Celestial, plum and azure fish, gold crown): the Seraph is a land lion with wings.
- Halo risk: Cvetibara's brass halo and the Seraph's halo are both above the head. The Seraph's is a DARK solid disc with a gold rim and a red corona. The reviewer must check at 64 px.

## 10. Animation references
TBD by builder. Suggested tags: "lion roar", "bird wing fan", "angel wings".

## 11. Reviewer gates (mythic, must outclass Leviathan)
1. Step 1: the six-wing build, tris count reported (target 13k, ceiling 15k), and the 64 px read. If the SIX-WING RULE (section 0) fails, stop and ask the owner before the four-wing fallback is built.
2. 64 px: the dark solid halo above a pale lion, six wings in a fan, and a gold rim visible. No brass ring (not Cvetibara), no sun rays (not Solar Lion). The gold rim is >= 20 gold px.
3. Game camera: the lilac-ivory body reads light; the obsidian mane and halo are the darkest parts. The six wings are readable as three pairs, not a blob.
4. The act is a six-wing cascade. It is not an eclipse, not a sunburst, not a tent, not a bloom.
5. A/B pairs at 64 px: Seraph next to Cosmic Leviathan, Celestial Dragon, Solar Lion and the Frostcrown Dragon. None reads as the same family. Collision 0 at step 1.
6. Builder gates (review section 6): icon strip at 64 and 128 px; value shares (OBSID dark share, IVORY body share, gold share); pose sheet of the cascade beats.
