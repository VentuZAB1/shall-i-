# GLACIER CONCEPTS v2 - 12 new pets (2026-10-27)

v2 applies every MUST and NICE item of `_review/GLACIER_PLAN_REVIEW.md` (11 pets APPROVED WITH CHANGES, Permafrost Titan REVISE).
Each pet has its own file: `_review/<Name>_plan.md` (v2 changes listed at the top of each). Nothing is built.
Money bonus from the odds: `max(1, (50 / odds%)^0.35)`.

## OWNER DECISIONS (2026-10-27, binding)
- Names are TWO words ("Lord Vienna", not "Lorda Vienna The First I"):
  - Absolute Zero Dragon -> **Frostcrown Dragon**
  - Coral Crusher Crab -> **Coral Crusher**
  - Cinder Wyrm Overlord -> **Cinder Overlord**
  - The other nine stay.
- "The details ... I cannot visualize it, so do it as you wish": the concepts are approved; the builder decides the details, and the reviewers gate the quality.
- **Permafrost Titan hero = option A, the GOLD CHEST BEZEL.** The owner left it to the lead ("we'd add more areas + new pets in future"), so head crowns stay free for future pets.
- **Eclipse Seraph:** six wings; it falls back to four only if the step-1 gate fails.
- Glacier has NO new wave type.

## 1. What changed in v2 (one line per pet)

- **Frostfang Lynx:** body warmer (#BEAC96); rosette flanks; the wall act is replaced by `act_clawflex`.
- **Ice Mammoth:** idle is a trunk swing (no sniff); mint moved to #96ECD2; trunk prototype gate.
- **Glacier Yeti:** height 9.0; idle is a plate settle (no rake); eyes are plate-grey, aurora on the seams only.
- **Blizzard Roc:** no white fan; erect crest; CHAR eye mask; grey back #B0B2BA; bow with zero net travel; no hop.
- **Permafrost Titan:** REDESIGN. No crown, no cyan core, no slabs, no crown flower. Mauve body; gold hero in two options; kneel act; core bellow.
- **Frostcrown Dragon:** height 11.5 (tied tallest with the Seraph); body #7CA0D8; five frost fins; the stillfreeze act rises all together.
- **Bramble Badger:** dark mantle band; short thorns (0.08-0.10H); the dig has forepaw scoops that lift at most 0.05H.
- **Coral Crusher:** eyestalks 0.07H, eyes in the brow plate; six-leg walk prototype gate.
- **Volt Rhino:** height 8.5; dark back and shoulder shield (IRON_D at least 25 %); horn-up roar capped at 16 degrees.
- **Cinder Overlord:** body #B684AC; the rim must show 25 gold px; it beats the 1 % secrets too; the crown tilt is 15 degrees.
- **Wraith Hound:** lavender-ash body #AAA0CE; soot saddle (at least 18 %); indigo #6478F0 and #A0B0FF.
- **Eclipse Seraph:** height 11.5; solid obsidian halo with a gold rim; body #E8D0F0; six-wing rule written in section 0.

## 2. One row per pet

| Pet | Tier | Odds (money) | Height | Look | Main colours (hex) | Hero | Signature act |
|---|---|---|---|---|---|---|---|
| Frostfang Lynx | Starter | 50 % (x1.00) | 7.0 | Sand-silver ice cat, rosette flanks, snow ear tufts | body #BEAC96, rosettes #7E746E, snow #F0F4FA, accent ICE #96ECFF | none | `act_clawflex`: forepaws flex, claws flash |
| Ice Mammoth | Medium | 26 % (x1.26) | 9.0 | Woolly teal-grey mammoth, cracked ice tusks, trunk | body #96B8BC, wool #60767C, accent MINT #96ECD2 | none (tusks and trunk) | `act_dustover`: trunk flings dust over the back |
| Glacier Yeti | Big | 14 % (x1.56) | 9.0 | Hunched navy snow beast, ice-plated arms, plate-grey eyes | body #7880C8, plates #CEE2F0, snow #E8F0F8, seams AURORA #78F0A0 | none (ice-plate arms) | `act_skid`: arms sweep, chest slides, shards brake |
| Blizzard Roc | High (flies) | 7.4 % (x1.95) | 9.0 | Snowy raptor, storm-grey back, erect frost crest | snow #EEF2FA, back #B0B2BA, CHAR #3A4050, accent FROST_V #B08CFF | none (erect crest) | `act_bow`: vertical bobs, crest flares, wings snap |
| Permafrost Titan | Secret | 2.5 % (x2.85) | 10.0 | Mauve ice giant, rounded pauldrons, ice-white chest core | body #B896C8, ice #E2F0FA, joints #343C54, gold #FFC432 | gold bezel (A) or gold arch (B) | `act_kneelrise`: kneels, core pulses, rises |
| Frostcrown Dragon | Mythic | 0.1 % (x8.80) | 11.5 | Steel-blue ice dragon, five white fins, gold horn crown | body #7CA0D8, belly #D2E2F6, ice #ECF6FC, gold #FFC432 | gold horn crown | `act_stillfreeze`: fins rise together, head presses ice |
| Bramble Badger | Starter | 40 % (x1.08) | 7.0 | Grumpy grey badger, amber thorn crest, dark belly | back #B0ACB4, mantle #6E6874, belly #483A36, accent AMBER #EC963C | none | `act_burrow`: forepaws scoop, hind legs kick |
| Coral Crusher | Medium | 15 % (x1.52) | 7.5 | Bronze armoured crab, rose-spiked claws, brow-plate eyes | shell #C49668, seams #846042, accent ROSE #FF7896 | none (rose-spiked claws) | `act_semaphore`: big claw waves in semaphore arcs |
| Volt Rhino | High | 6 % (x2.10) | 8.5 | Iron-grey rhino, dark plate folds, one lightning horn | back #686E78, flank #B0B4BA, belly #DEE0E4, accent VOLT #D2FF50 | lightning horn | `act_horntap`: horn taps the ground, bolts run out |
| Cinder Overlord | MYTHIC (secret + mythic flag, Fire tab mythic card; updated 10-28) | 0.5 % (x5.01) | 10.5 | Ember-red serpent, sulfur-blue vents, obsidian crown (palette as built, 10-28) | body #B04836, plates #3E3240, belly ash #DEC29E, vents SULFUR BLUE #145CFA, white-hot cores #E2F0FF, gold #FAA023 | obsidian crown, gold frames | `act_molt`: crown plates lift, shed embers, reseat |
| Wraith Hound | Medium-high | 10 % (x1.76) | 8.0 | Lavender-ash ghost hound, soot saddle, streaming mane | body #AAA0CE, soot #5C5C74, mist #E2E2EC, accent INDIGO #6478F0 | none (streaming mane) | `act_smokecloak`: crouches, mane fans into a cloak |
| Eclipse Seraph | Mythic | 0.1 % (x8.80) | 11.5 | Six-winged lilac-ivory lion-angel, obsidian mane, dark halo | body #E8D0F0, obsidian #3C3C54, corona BLOOD #FF5458, gold #FFC432 | solid eclipse halo, gold rim | `act_wingcascade`: six wings ripple tip to root |

## 3. Lineup logic per area

Odds below are the full tables, each summing to 100.

**Area 1, Grass / Wood egg.** Tortoise 30, Stag 16, Treant 8.5, Basilisk 3.5, Mantis 2, Bramble Badger 40.
- The badger is the new commonest pet, so it sits at the bottom of the ladder: simple, bright, with a dark mantle and an amber crest.
- Grass accents so far are lime, green, violet and ruby. The badger's amber is the only amber in the egg.

**Area 2, Tide / Water egg.** Kappa 45, Turtle 25, Coral Crusher 15, Kraken 9, Hammerjaw 4.5, Orca 1.5.
- The crab sits between the Turtle and the Kraken. It must look more armoured than the Turtle and less exotic than the Kraken.
- The rose is 7 degrees from the Wyrm's rose (cross-egg). Watch both in the lineup.

**Area 3, Storm / Thunder egg.** Raiju 50, Bull 25, Wyvern 14, Volt Rhino 6, Thunderbird 4, Thunder Rex 1.
- The rhino sits between the Wyvern and the Thunderbird. It is 8.5 tall, the same as the Thunderbird, and the Thunderbird is rarer.
- Its signature is the one ivory lightning horn with volt-lime inlays.

**Area 4, Magma / Fire egg.** Boar 53.5, Golem 27, Cerberus 13, Ivonrath 4, Phoenix 2, Cinder Overlord 0.5.
- The Wyrm is the top of the egg. It must outclass Phoenix and Ivonrath, and it must also beat the 1 % secrets (Rex, Leviathan).
- The Fire egg is all orange and red. The Wyrm uses a rose accent and a gold rim, so it is the one new family in the egg.

**Area 5, Shadow / Void egg.** Panther 50, Stallion 25, Wraith Hound 10, Black Dragon 9.5, Asparuh 4, Weaver 1.5.
- The Wraith sits between the Stallion and the Black Dragon.
- Its lavender-ash body and soot saddle keep it apart from the Panther. Its indigo is 40 degrees from the Panther's violet.

**Area 6, Celestial egg.** Solar Lion 54.9, Griffin 27, Celestial Dragon 13, Cvetibara 4, Cosmic Leviathan 1, Eclipse Seraph 0.1.
- The Seraph is the top of the egg, and it is the tallest of the 12 (tied at 11.5 with the Frostcrown Dragon).
- The Celestial egg has gold, brown, indigo, brass and azure. The Seraph is lilac-ivory with an obsidian mane and a solid halo.

**Area 7, Frostfall Glacier egg (new).** Frostfang Lynx 50, Ice Mammoth 26, Glacier Yeti 14, Blizzard Roc 7.4, Permafrost Titan 2.5, Frostcrown Dragon 0.1.
- Six silhouettes: cat, elephant, hunched ape, bird, upright giant, dragon.
- Body families after v2: warm sand-silver (Lynx), charcoal-teal (Mammoth), navy (Yeti), storm-grey with white (Roc), mauve (Titan), steel-blue (Absolute Zero). The four blue-violet bodies from v1 are gone.
- Accent families after v2: ICE cyan (Lynx), MINT (Mammoth), AURORA on the Yeti seams, FROST violet (Roc), gold (Titan hero, Absolute Zero horns). Non-gold accents are at least 22 degrees apart.
- The Titan (2.5 %) must outclass the Roc (7.4 %) and the Yeti (14 %). The Frostcrown Dragon (0.1 %) must beat the 1 % secrets (Rex, Leviathan) and the Titan.

## 4. Owner decisions (still open)

1. **Permafrost Titan hero: option A or option B.**
   - A: a gold chest bezel (a 0.22H ring around the chest core, tilted 10 degrees up).
   - B: a gold arch headdress over the skull (no spikes).
   - Both are fully specified in `_review/PermafrostTitan_plan.md` section 5, marked OWNER PICKS. The build waits for this choice.
2. **Eclipse Seraph: six wings, or the four-wing fallback.**
   - The plan builds six wings. The step-1 gate fails if the tris are over 15k or the 64 px read is a blob. Then the fallback is four wings (the lower pair removed).
   - The four-wing fallback needs the owner's OK before it is built (`_review/EclipseSeraph_plan.md` section 0).

## 5. Assumptions and build notes

- Odds names "Badger", "Crab", "Wyrm", "Wraith", "Seraph" in the spec are the new pets. Existing pets are the 30 files in `PetsV3/pets/`.
- There is no old IceMammoth file in PetsV3. The Mammoth is built from scratch.
- There is no crab kit. The crab uses the AbyssWeaver multi-leg chain. A six-leg walk prototype is a build gate.
- The Mammoth trunk has no kit tube. A trunk prototype is a build gate.
- Builder gates for every pet are in review section 6: step-1 tris (target 13k, cap 15k), `collision_free`, `ground_min_z >= -0.02`, linear 0, loops closed, the 64 and 128 px icon strips next to the nearest pets, value shares, and pose sheets of the act beats.
- The Frostcrown Dragon act has six beats, as the review wrote it. The Wyrm and Seraph acts keep five beats.

## 6. Machine-readable list

```json
[
  {"name": "Frostfang Lynx", "file": "_review/FrostfangLynx_plan.md", "tier": "starter", "odds": 50, "egg": "Glacier", "height": 7.0, "look": "Sand-silver ice cat, rosette flanks, snow ear tufts, cyan slits.", "hero": "", "act": "act_clawflex: forepaws flex, icy claws flash out", "swatches": [["body", "#BEAC96"], ["rosettes", "#7E746E"], ["underside", "#F0F4FA"], ["accent", "#96ECFF"]]},
  {"name": "Ice Mammoth", "file": "_review/IceMammoth_plan.md", "tier": "medium", "odds": 26, "egg": "Glacier", "height": 9.0, "look": "Woolly teal-grey mammoth, cracked ice tusks, trunk, dome hump.", "hero": "", "act": "act_dustover: trunk scoops snow and flings it over its back", "swatches": [["body", "#96B8BC"], ["wool", "#60767C"], ["belly", "#CED6D8"], ["accent", "#96ECD2"]]},
  {"name": "Glacier Yeti", "file": "_review/GlacierYeti_plan.md", "tier": "big", "odds": 14, "egg": "Glacier", "height": 9.0, "look": "Hunched navy snow beast, ice-plated arms, plate-grey eyes.", "hero": "", "act": "act_skid: arms sweep, chest slides, ice shards brake", "swatches": [["body", "#7880C8"], ["plates", "#CEE2F0"], ["muzzle", "#E8F0F8"], ["seams", "#78F0A0"]]},
  {"name": "Blizzard Roc", "file": "_review/BlizzardRoc_plan.md", "tier": "high", "odds": 7.4, "egg": "Glacier", "height": 9.0, "look": "Snowy raptor, storm-grey back, erect frost crest, frost-violet trim.", "hero": "", "act": "act_bow: vertical bobs, crest flares, wings snap shut", "swatches": [["breast", "#EEF2FA"], ["back", "#B0B2BA"], ["primaries", "#3A4050"], ["accent", "#B08CFF"]]},
  {"name": "Permafrost Titan", "file": "_review/PermafrostTitan_plan.md", "tier": "secret", "odds": 2.5, "egg": "Glacier", "height": 10.0, "look": "Mauve ice giant, rounded pauldrons, ice-white chest core.", "hero": "Gold bezel or gold arch: owner picks", "act": "act_kneelrise: kneels, core pulses, rises again", "swatches": [["body", "#B896C8"], ["ice", "#E2F0FA"], ["joints", "#343C54"], ["gold", "#FFC432"]]},
  {"name": "Frostcrown Dragon", "file": "_review/FrostcrownDragon_plan.md", "tier": "mythic", "odds": 0.1, "egg": "Glacier", "height": 11.5, "look": "Steel-blue ice dragon, five white fins, gold horn crown, frost mist.", "hero": "Gold horn crown", "act": "act_stillfreeze: fins rise together, head presses the ice", "swatches": [["body", "#7CA0D8"], ["belly", "#D2E2F6"], ["ice", "#ECF6FC"], ["gold", "#FFC432"]]},
  {"name": "Bramble Badger", "file": "_review/BrambleBadger_plan.md", "tier": "starter", "odds": 40, "egg": "Wood", "height": 7.0, "look": "Grumpy grey badger, amber thorn crest, dark belly, white face stripes.", "hero": "", "act": "act_burrow: forepaws scoop dirt, hind legs kick back", "swatches": [["back", "#B0ACB4"], ["belly", "#483A36"], ["face", "#F0ECE2"], ["accent", "#EC963C"]]},
  {"name": "Coral Crusher", "file": "_review/CoralCrusher_plan.md", "tier": "medium", "odds": 15, "egg": "Tide", "height": 7.5, "look": "Bronze armoured crab, rose-spiked claws, brow-plate rose eyes.", "hero": "", "act": "act_semaphore: big claw waves in slow semaphore arcs", "swatches": [["carapace", "#C49668"], ["seams", "#846042"], ["rose", "#FF7896"], ["belly", "#F0E2C8"]]},
  {"name": "Volt Rhino", "file": "_review/VoltRhino_plan.md", "tier": "high", "odds": 6, "egg": "Storm", "height": 8.5, "look": "Iron-grey rhino, dark plate folds, one lightning horn.", "hero": "Lightning horn with volt-lime inlays", "act": "act_horntap: horn taps the ground, bolts run out", "swatches": [["flank", "#B0B4BA"], ["back plate", "#686E78"], ["belly", "#DEE0E4"], ["volt", "#D2FF50"]]},
  {"name": "Cinder Overlord", "file": "_review/CinderOverlord_plan.md", "tier": "mythic", "odds": 0.5, "egg": "Magma", "height": 10.5, "look": "Ember-red serpent, sulfur-blue vents, obsidian crown (palette as built, 10-28).", "hero": "Obsidian crown with gold frames", "act": "act_molt: crown plates lift, shed embers, reseat", "swatches": [["body", "#B04836"], ["plates", "#3E3240"], ["belly", "#DEC29E"], ["vents", "#145CFA"], ["cores", "#E2F0FF"], ["gold frames", "#FAA023"]]},
  {"name": "Wraith Hound", "file": "_review/WraithHound_plan.md", "tier": "medium-high", "odds": 10, "egg": "Void", "height": 8.0, "look": "Lavender-ash ghost hound, soot saddle, streaming mane, indigo eyes.", "hero": "", "act": "act_smokecloak: crouches, mane fans into a smoky cloak", "swatches": [["ash", "#AAA0CE"], ["soot", "#5C5C74"], ["mist", "#E2E2EC"], ["indigo", "#6478F0"]]},
  {"name": "Eclipse Seraph", "file": "_review/EclipseSeraph_plan.md", "tier": "mythic", "odds": 0.1, "egg": "Celestial", "height": 11.5, "look": "Six-winged lilac-ivory lion-angel, obsidian mane, dark halo.", "hero": "Solid eclipse halo, gold rim", "act": "act_wingcascade: six wings ripple tip to root, then fold", "swatches": [["body", "#E8D0F0"], ["mane/halo", "#3C3C54"], ["corona", "#FF5458"], ["gold rim", "#FFC432"]]}
]
```
