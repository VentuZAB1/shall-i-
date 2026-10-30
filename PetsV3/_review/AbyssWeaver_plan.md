# ABYSS WEAVER — build plan v1 (Void egg, 1.5 % SECRET, x3.2 income)

Builder: me, in the PetsV3 kit (`pets/AbyssWeaver.py`, headless Blender). House pipeline:
plan → plan review → build → visual reviews → clips → clip review → export.

This plan is for the plan reviewer. Decide or adjust everything marked **[DECIDE]**.

## 1. Role and the one-line read
"The queen of the void: a giant armoured spider of obsidian and violet, with a gold-crowned head of eight burning eyes,
huge fangs, crystal-bristled legs arched high above its body, and a swollen abdomen that carries a gold-rimmed VOID
RIFT, the portal it weaves its webs from."

At 64 px it must read as **a black-violet spider queen with a gold ring (the rift) on its back and a gold crown**.

It must NOT read as:
- **Thornblade Mantis** (Grass 2 %): an upright green insect with raptorial scythe arms. The Weaver is low and wide, with
  8 walking legs and fangs, not scythes.
- **Kraken** (Water): a red squid with curling tentacles. Spider legs are jointed straight segments, never curls.
- **Shade Panther**: violet crystal CLUSTERS on the shoulders. The Weaver's crystals are thin single bristle-spines on
  the leg joints, not clusters.
- **the Halloween hub's decorative spiders** (24 low-poly props): a premium creature, armoured, crowned, far richer.

## 2. Silhouette and proportions (side; −Y forward, Z up; rest = idle f0)
- **Cephalothorax** (Spine): an armoured oval carapace about 0.62 long × 0.52 wide, top at z ≈ 0.62, with a raised
  ocular turret at the front.
- **Pedicel → abdomen** (Abd1, Abd2 bones): a big ovoid, about 0.95 long × 0.78 wide × 0.62 tall, raised 10° behind.
  Its top is the model top at z ≈ 1.05 [DECIDE: the crown tip or the abdomen top is H_MODEL]. Spinnerets at the rear.
- **8 legs**, each coxa → femur (up and out) → patella/tibia (down) → metatarsus/tarsus (to the ground):
  - The knees arch HIGH (z ≈ 0.95–1.1, above the carapace), the classic spider silhouette, with the feet planted wide.
  - Leg span about 2.4 at rest.
  - Pair 1 is longest, reaching forward. Pair 4 reaches back. Pairs 2–3 go sideways.
- **Head front:**
  - 2 big chelicerae with curved fangs (BONE → black tips), on a Jaw-like bone pair for the threat spread
  - 2 short pedipalps
- **Size:** HEIGHT 8.5 studs to H_MODEL [DECIDE]. In game that is about as wide as the Black Dragon is long.

## 3. Colour blocking (3-band, flat palette-ID shares measured)
| role | colour (Blender) | where |
|---|---|---|
| OBSIDIAN | (30, 26, 42) | leg segments, carapace edge, chelicerae |
| CARAPACE | (62, 50, 96) dark violet | carapace plates, abdomen armour plates (segmented, with gaps) |
| VELVET | (96, 44, 150) deep violet "hair" | the abdomen's underlying hide between the plates, leg joint bands |
| VOID ×3 | deep (70, 30, 160) → violet (150, 80, 255) → hot (236, 214, 255) | eyes, bristle-spine tips, rift vortex rings |
| MAGENTA | (236, 56, 196) | the 2 main eyes' irises, the underside hourglass mark [DECIDE] |
| GOLD + GOLD_D | (255, 200, 60) / (212, 142, 30) | the CROWN (3 spikes over the eye turret), the RIFT rim, the fang bases |
| BONE | (232, 222, 200) | fangs |

Share targets (game cam):
- OBSIDIAN + CARAPACE 40–50 %
- VELVET 12–20 %
- the VOID family 10–16 %
- GOLD 5–9 % (the rift rim faces the game camera)
- No role above 45 %.

## 4. Head and eyes (the fierce zone)
- **Eyes:** an 8-eye cluster on the ocular turret.
  - 2 big front eyes (MAGENTA iris, a black vertical slit, a VOID-hot spot, no glint).
  - 2 medium side eyes and 4 small rear eyes (VOID).
  - A heavy CARAPACE brow ledge overlaps the top of the big eyes (the V-lid lesson from the Mantis and the Leviathan).
- **Crown:** 3 swept-back gold spikes rising from the turret, plus a small gold circlet band. It is the 64 px gold
  anchor along with the rift.
- **Chelicerae:**
  - big, dark, with gold base rings and curved BONE fangs pointing down and in
  - a slight open gape at rest (2°) so the fangs read
  - in roar and act they spread apart (Fang_L / Fang_R yaw)

## 5. HERO: the VOID RIFT on the abdomen back [DECIDE]
- **R1, recommended:** a gold-rimmed portal disc set into the abdomen's upper back, facing up and back toward the game
  camera.
  - A thick GOLD ring, 0.30 across and 0.04 thick (smooth, nostud).
  - Inside it, 3 stepped concentric discs, DEEP → VIOLET → HOT, with a black pupil-slit centre (the "void eye" read).
  - 4 short gold clasps pin the ring to the abdomen plates.
- **R2:** a gold widow hourglass on the abdomen back. Iconic, but it remixes real black widows, and gold on a flat
  hourglass reads less "secret".
- **R3:** a web-sigil: gold web lines radiating over the abdomen. Thin lines risk the "no detail under 0.02" rule and
  read as cracks at 64 px.

## 6. Legs and crystals
- **Construction:** tapered B.seg per segment. A dark OBSIDIAN femur and tibia with VELVET joint bands and a gold
  CLAW tip on each tarsus [DECIDE: gold claws, or black].
- **Bristle-spines:** single VOID crystal spines (DEEP → VIOLET → HOT stepped spikes) on the TOP of every knee (patella),
  pointing up and back. That is 8 spines total, like a crown of points around the body at 64 px. NOT clusters
  (Shade Panther).
- **Underside:** a MAGENTA hourglass mark on the abdomen's belly [DECIDE], seen in the roar rear-up.

## 7. Rig ("spider" rig; motion "Walk")
- **Bones:**
  - Root, Spine (cephalothorax), Head (ocular turret + chelicera base; small range), Fang_L/R, Palp_L/R
  - Abd1, Abd2 (abdomen pitch/bounce)
  - per leg i = 1..4, side L/R: Leg_iS (femur) → Shin_iS (tibia) → Foot_iS (tarsus), with 2-bone IK via `add_leg2`
    (knee direction up and out)
- **VFX anchors:**
  - Rift (the abdomen portal centre)
  - Crown
  - Spinneret (abdomen rear)
  - EyeGlow (front eyes)
  - FangTip_L/R (venom)
- **Pairs:**
  - neighbour legs (1-2, 2-3, 3-4 per side) on femur, shin and foot
  - Leg4 vs the abdomen
  - Fang vs Palp, Palp vs Leg1
  - Abd vs Spine
- **Joint capsules:** the coxa ring (all 8 coxae meet the carapace underside), the pedicel, the fang bases.

## 8. Clips (references pulled from animationreference.org and cited BEFORE animating, owner rule)
| clip | frames | idea |
|---|---|---|
| idle | 120 loop | Still-hunter: long pauses, then twitchy single-leg taps (one leg at a time, 4–6 f), palps groom the fangs, the abdomen slowly "breathes" (Abd pitch ±2), one predator head-tilt (no shake). The rift pulses (event) |
| walk | 32 loop | Alternating TETRAPOD gait (L1 R2 L3 R4 / R1 L2 R3 L4), duty 0.55, fast low scuttle; the body level (z ±0.006) and the abdomen lagging 2 f; feet planted (slide 0) |
| roar | about 80 | THREAT DISPLAY (tarantula): rears up on legs 3–4, legs 1–2 raised high and spread, fangs spread with venom drip (event), the abdomen tilts down, a hiss-shiver hold, then down |
| act_riftweave | about 120 | **RIFT WEAVE** (signature) |

RIFT WEAVE beats:
1. Plants and lowers.
2. The abdomen lifts and the spinnerets fire silk (event `silk`).
3. The front legs WEAVE: alternating crossing strokes in front of the face, 3 strokes (event per stroke).
4. The rift opens: the abdomen pumps and the rift flares (event `rift`).
5. SLAM: both front legs stab down together (impact; event `slam`).
6. Settle.

Rules:
- no head shakes, no spins, no jumps
- 0 collisions at step 1, ground ≥ −0.02 every frame, slide 0, no linear keys
- in-betweens on any swing over 60° in one frame (Mantis F1 lesson)

## 9. Budget and deliverables
- Body ≤ 12 k tris (cap 15 k). 8 legs × 3 segments plus spines is the tri risk, so keep the segments simple.
- Model gate:
  - a 600 px model sheet (tq / front / back / side / game) + a separate tq
  - a face close sheet (8 eyes, fangs, crown)
  - the 64/128 strip with ShadePanther, NightmareStallion, BlackDragon, PharaohAsparuh, ThornbladeMantis and Kraken
  - an A/B pair (Weaver next to the Mantis, then next to the Kraken)
  - flat shares, tris
  - limit poses (the roar rear-up, the walk extremes, the weave cross, the slam)

## 10. Questions for the plan reviewer
1. Rift R1 (gold portal disc) vs R2 (gold hourglass) vs R3 (web-sigil)? Crown spikes needed as well?
2. Leg proportions and knee height for a fierce, not creepy-cute, read. Bristle-spines OK, or too close to Shade
   Panther's crystals?
3. Palette: is it distinct enough from the Black Dragon's indigo and Shade Panther's violet within the Void family?
4. The tetrapod walk at 32 f: too fast for the kit's foot planting? Any rule for 8 IK legs?
5. Is the act unique enough (the weave strokes versus the Mantis X-cross)? Better ideas?
6. Any remix or jackpot issue for a 1.5 % secret?
