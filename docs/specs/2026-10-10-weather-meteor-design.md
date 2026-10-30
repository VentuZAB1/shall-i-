# Weather #2: METEOR SHOWER — design (2026-10-10)

**Owner's brief:** "Another weather event called Meteor shower. Same rules as the UFO Invasion, make the models in blender, and
for the ICON if there's no one available, just make a picture from the model. Cutscene, animations, sfx and vfx are the key
part: almost the same thing as the aliens, but hitting the eggs / players with meteors, giving the eggs a mutation or
knocking you down (add a fall animation, since we do not have it). Don't ask questions, do your best, as recommended."

Every open choice below was decided by me (Claude) on the owner's instruction; each one says why.

## Same rules as UFO Invasion (no change to the framework)
- **Scheduling:** WeatherServer picks it like any weather: ONE weather per hour per server since 2026-10-11 (a coin flip
  between the two), 5:00 long. NO_REPEAT is 15 min per type. It moves area to area, staying 30–90 s each time.
- **Arrival cutscene (8 s):** it plays only for players on the hub or runway, not those on the slingshot, in the tutorial
  or in a hatch cinematic. Waves are frozen during it and for 2 s after.
- **HUD pill:** shows the meteor icon and "METEOR: m:ss". The announcement bar gives the start, each move and the stop.
- **Admin:** the WEATHER row gets a METEOR SHOWER chip next to UFO INVASION.
- **Sky tint:** in the active area the tint is orange.
- **Never hit:**
  - a player in a trench (safe box);
  - a player on the slingshot;
  - a player in the tutorial;
  - a player outside the weather's area;
  - a player on cooldown.
- **Never targeted:** an egg that already has the mutation.

## What the meteors do
- **Targeted strikes:** one every 4–7 s in the weather's area.
  - Player chance is 0.4 if both an eligible player and an eligible egg exist; otherwise it targets whatever is eligible.
  - At most 2 targeted strikes are in flight at once.
- **Warning ring (2.2 s, orange):**
  - The ring follows the target, then **locks 0.7 s before impact**.
  - Ring and meteor share the same ring + countdown language as the UFO ring, but in fire colours. You can read it, and
    you can RUN OUT of it to dodge.
  - *Why:* the UFO already has "hide in the trench". Dodging adds the meteor's own skill moment.
- **Player hit:** anyone still within 9 studs of the locked spot at impact, unless safe, goes through this sequence:
  1. Drops a carried egg.
  2. Is **knocked down**: blown 10–16 studs away from the impact along an arc.
  3. Lands on their back and lies dazed with stars over the head.
  4. Gets back up (2.8 s total). Then 40 s hit cooldown.
  - Untargeted bystanders in the blast are knocked down too; it's a meteor.
- **Egg hit:** the egg gets the **"Meteor" mutation**: x1.5 income and sell value, stacking with UFO (UFO + Meteor = x2.25).
  - The egg hops from the impact, then shows a fire-ember aura and "+METEOR".
  - Its countdown gets +30 s.
  - *Why x1.5:* "same rules as the UFO". Equal value keeps both weathers equally exciting.
- **Ambient meteors:** about one per 1.5 s, small, landing in the area but never within 14 studs of a player. They do
  nothing but look and sound great.
- **Distant streaks:** on every client, meteors streak across the high sky while the weather runs. Pure decoration.

## The fall animation
- **Keyframed and procedural:** poses on the R15 joints are set locally on every client after the Animator each frame,
  the same technique as the UFO "abducted" pose.
  - *Why:* no animation asset has to be uploaded or owned by the group, it runs identically on every client, and it
    works for every avatar scale.
- **Server:** moves the anchored root along the knock-back arc and holds it on the ground. Player attributes:
  `MeteorDownAt` (server time) and `MeteorDownDir`.
- **Beats** come from animationreference.org reference clips (see the plan):
  1. impact whiplash;
  2. airborne flail;
  3. back slam + bounce;
  4. dazed lie;
  5. sit up;
  6. push up to a crouch;
  7. stand.

## The storm cloud (owner 2026-10-11)
The owner asked for a black dark cloud hovering over the area, with thunder around it, and the meteors falling from there.
- **Model:** `WeatherAssets.Meteor.StormCloud`, a 207 x 93 x 405-stud cumulonimbus bank: three levels of billows
  down to cauliflower puffs, a flat storm base with mammatus lobes, a charcoal ramp. It is a Model of 4 MeshParts
  (19k tris each) with baked SurfaceAppearance maps (Blender `Weather/Meteor/HQ/build_storm_hq.py`; the HQ remake of
  2026-10-11, owner: "they are low polygon, we need high quality").
- **Placement:** it hangs 85 studs over the area's floor and casts a shadow.
- **Effects** (VFX Studio textures): soft billows, ragged scud and falling embers (`WeatherFX.MeteorCloud`), plus a storm
  rumble loop.
- **Forming:** it billows into being during the cutscene (1.0-3.2 s after the folder's `FormAt`).
- **Moving:** on a move it glides to the next area over 6 s. The server publishes `CloudFrom`, `CloudTo` and
  `CloudMoveAt`, and `WeatherLogic.cloudPos` computes the position. No meteors start while it glides.
- **Stopping:** it dissolves (3 s).
- **Meteors come out of it.** Each strike record carries `From`, a point in the cloud's base 20-55 studs to the side of
  the spot above its target (`WeatherLogic.cloudExit`), so the fall is slanted.
  - The belly glows orange there 0.5 s before (a tell).
  - The meteor tears out (`WeatherFX.MeteorCloudBurst`) and accelerates down onto the spot.
- **Lightning** every 3-7 s:
  - a spider flash in the base, about half the time with a bolt down to the ground (decoration, it hurts nobody);
  - the flash lights the underside and flashes the screen of anyone near;
  - thunder follows (sooner when you're close).
- **Storm shade:** standing in the area tints the world darker and greyer (`WeatherConfig.TYPES.Meteor.tint`).
- **Sounds:** none shared with the UFO. The start is a thunder roar, the title slam is a thunder blast, and the cloud
  has thunder cracks and a distant-rumble loop (all Pro Sound Effects).

## Cutscene (8 s, filmed at the area; redesigned 2026-10-11)
The owner on the first version: "1 big meteor splits mid-air in 6 or 8 small ones doesn't make sense". The storm is now
the source.
| Time | Beat |
|---|---|
| 0–1 s | **The omen**, where the player stands: the light drains to dusk, distant thunder, the camera pulls back and looks up. |
| 1–3 s | A lightning flash cuts to the area: **the black storm billows into being** overhead, with lightning crawling through it and a bolt to the ground. |
| 3–4.3 s | Under the belly: an **orange glow swells inside the cloud**, the rumble builds, the camera shakes. |
| 4.3–5.25 s | **The big one tears out** of the belly (smoke burst, flash, roar) and plunges onto the far end of the runway; the camera follows it down. |
| 5.25 s | Impact: white flash, shockwave, heavy shake. |
| 5.3–7 s | **The barrage**: meteor after meteor punches out of the base and rains on the runway; lightning to the ground. |
| 7–8 s | **"METEOR SHOWER"** slams in (orange) to a thunder roar, with "- AREA -" under it. |
| after 8 s | Glide back to the player's own camera. |

All cutscene meteors are client-local, so no server models are needed.

## Assets
- **Blender models**, HQ since 2026-10-11 (`Weather/Meteor/HQ/build_hq.py`): sculpted rocks with fracture faces,
  a molten crack network with heated rims, craters and melt-flow streaks, baked onto game meshes (Meteor 7k tris,
  MeteorBig 19.5k, MeteorChunk 1.5k) with SurfaceAppearance maps, RenderFidelity Precise. The first versions below
  (`Weather/Meteor/build_meteor.py`, 20-2,740 tris) are kept in `ServerStorage._Backup_MeteorV1`:
  - `Meteor` (about 7 studs): a chunky basalt rock with craters and orange/yellow magma cracks.
    - The cracks are geometry and palette colour only. **No neon or emissive** (owner rule); the glow comes from VFX.
  - `MeteorBig` (cutscene, about 60 studs).
  - `MeteorChunk` (debris, about 1.5 studs).
- **Icon:** no fitting icon exists, so it's a Blender render of the meteor with its flame trail, outlined like the saucer
  icon, uploaded under the game.
- **VFX:** only VFX Studio library textures (owner rule) in `ReplicatedStorage.WeatherFX`:
  - `MeteorTrail` (fire + smoke trail);
  - `MeteorImpact` (flash, shockwave ring, fire burst, smoke, sparks);
  - `MeteorScorch` (ground mark);
  - `MeteorRing` (warning ring);
  - `MeteorAura` (mutation embers).
- **Sounds:** licensed only, the same sources as UFO (Pro Sound Effects / Roblox's own). Entries go in `SFX.LIB`:
  - `MeteorSiren` (start);
  - `MeteorFall` (incoming whistle);
  - `MeteorImpact` (boom);
  - `MeteorRumble` (cutscene);
  - `MeteorWhoosh` + `MeteorRoar` (the big cutscene meteor) and `MeteorFar` (distant impacts), which replaced the
    planned `MeteorFire` crackle loop;
  - `KnockDown` (body slam).

## Code
| Where | What |
|---|---|
| `WeatherConfig.TYPES.Meteor` | numbers |
| `Mutations.TYPES.Meteor` | tag "METEOR", #FF7A1F, aura MeteorAura |
| `WeatherLogic` | pure functions: `inBlast`, `knockDir`, `skyDir` |
| `ServerScriptService.Weathers.Meteor` | strikes, knockdown, egg hits; `start` / `moveTo` / `stop` |
| `EggSpawner` | `ServerStorage.EggStrike:Invoke(egg, mutation)` |
| `ReplicatedStorage.Weathers.MeteorClient` | strikes, rings, ambient sky, cutscene, "+METEOR" pop-up |
| `ReplicatedStorage.Knockdown` | the fall animation, applied to every character with `MeteorDownAt` |
| `ServerStorage.MeteorDebug` (Studio only) | `("strike", player)` / `("egg")` / `("resetCooldown", player)` |

`WeatherTestNoActs` stops the automatic strikes.

## Tests
- **WeatherTests (Edit):** the new logic functions, the Meteor config sanity checks, and UFO+Meteor stacking x2.25.
- **WeatherServerTests (Play, TestFreshSave = true):**
  - start / moves / stop for Meteor;
  - a player knocked down and released;
  - the carried egg dropped;
  - cooldown;
  - never hit in a trench / tutorial / slingshot / another area;
  - dodging after the lock;
  - an egg mutated with +30 s;
  - STOP before impact = no effect;
  - STOP or reset while down = released.
- **Visual:** cutscene frames, impact, knockdown, the 2-player Server & Clients check.
