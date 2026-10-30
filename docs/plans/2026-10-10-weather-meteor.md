# Meteor Shower — implementation plan + ledger (2026-10-10)

**Spec:** `docs/specs/2026-10-10-weather-meteor-design.md`.
**Executor:** Claude, inline, while the owner is away. The owner said "don't ask, do your best, as recommended", so every
fork is a ruling in the ledger below.

## Animation reference: the knockdown (owner rule: references before any character animation)
| Clip (animationreference.org) | Frames (24 fps) | What I took from it |
|---|---|---|
| **Lego**, tag `tripping` (a Lego minifig hit by a flying lantern) | f23–37 | Brief recoil before contact, head turned toward the threat |
| | f40–49 | **Hit:** the body folds forward around the impact (arms and legs swing forward) and is carried backward; the feet leave the ground |
| | f52–60 | **Airborne:** almost horizontal, limbs trailing, travels about 1.5 body lengths |
| | f63 | **Slam:** lands on the back and side, limbs splayed; a little bounce |
| | f63–84 | **Slide** that decelerates, then lies still |
| | f99–106 | **Sits up, dazed**, propped on the arms |
| **Kung Fu Panda**, tag `tripping` (Po face-down, gets up) | f230–300 | The head rises first and the hands plant |
| | f300–346 | The back arches and the weight shifts forward over the hands |
| | f357–403 | The hips come up into a crouch, then stand. Compressed hard for gameplay. |

**Keyed timing at 30 fps (2.8 s):**

| Time | Beat |
|---|---|
| 0 | Impact fold |
| 0–0.70 s | Airborne back-flip toward horizontal |
| 0.70 s | Back slam |
| 0.70–1.0 s | Bounce and settle |
| 1.0–1.6 s | Dazed lie (head lolls, stars) |
| 1.6–2.0 s | Sit up on the arms |
| 2.0–2.4 s | Push forward into a crouch |
| 2.4–2.8 s | Stand |

Lego's hit-to-land takes about 23 frames at 24 fps, roughly 0.96 s. For gameplay I compressed it to 0.7 s.

## Tasks
1. Assets. Done 2026-10-10.
   - **Blender:** `Weather/Meteor/build_meteor.py`. Meteor (844 tris), MeteorBig (2,740), MeteorChunk (20). Imported as ZAB Studio into `RS.WeatherAssets.Meteor`.
   - **Icon:** `rbxassetid://84492648795778`.
   - **VFX templates:** MeteorTrail / MeteorImpact / MeteorScorch / MeteorRing / MeteorAura in WeatherFX.
   - **Sounds:** 8 SFX.LIB entries, all PSE.
2. **Config.** `WeatherConfig.TYPES.Meteor` and `Mutations.TYPES.Meteor`. Done.
3. **WeatherLogic.** Add `inBlast(pos, at, radius)`, `knockDir(rootPos, at, fallbackLook)` and `skyDir(rng)`, with Edit tests in WeatherTests. Done.
4. **EggSpawner.** Add `ServerStorage.EggStrike:Invoke(egg, mutation) -> true`. It hops the egg, applies the mutation and adds +bonus time. Done.
5. **Server module `Weathers.Meteor`.** Done.
   - Strikes and rings, the knockdown, egg hits, ambient meteors.
   - start / moveTo / stop.
   - Studio-only `MeteorDebug`.
6. **Client.** Done.
   - `RS.Knockdown` (the fall animation).
   - `Weathers.MeteorClient`: the strikes, rings, sky streaks, cutscene and "+METEOR" pop-up.
7. **WeatherServerTests Meteor section.** Done 2026-10-11. Regression with TestFreshSave = true, all green:
   WeatherTests 73/73, WeatherServerTests 128/128 (clean Play session), AdminTests 98/98, AdminServerTests 35/35.
8. **Visual checks.** Done 2026-10-11 (single-player screenshots of every beat, then a 2-player Server & Clients run).
9. **Docs and memory**, then the report to the owner. Done 2026-10-11 (`Weather/Meteor/README.md`, `docs/weather-live-checklist.md`).

## Ledger
- Ruling: knockdown = procedural keyframes on joint Transforms (client), not an uploaded animation asset. It needs no
  group-owned upload, runs the same on every client and fits every avatar scale. *Cost if wrong:* an animator would
  re-author it as an asset.
- Ruling: Meteor mutation = x1.5 ("same rules as the UFO"). *Cost if wrong:* one number in Mutations.
- Ruling: dodging. The ring locks 0.7 s before impact and anyone still inside the blast is knocked down, bystanders
  included. *Cost if wrong:* `lockBefore` / `blastRadius` in WeatherConfig.
- Ruling: icon = Blender render of the meteor and flame trail, outlined like the saucer icon. Like the saucer icon, it's
  uploaded under the owner's user account; it works in the group game the same way the saucer icon does.
- Ruling (2026-10-11): sounds are 8 PSE clips. The spec's "MeteorFire" crackle loop became MeteorWhoosh + MeteorRoar on
  the big cutscene meteor, plus MeteorFar for distant impacts. *Cost if wrong:* one more SFX.LIB entry.
- Ruling (2026-10-11): cutscene opening. The visual check showed the planned "pull back" lerping the player's camera
  toward the area, which flew it 1000+ studs down the runway when the player stood on the hub (most players). Now the
  shock beat (0-1 s) happens where the player stands: the camera pulls back and tilts up. Then it flash-cuts to the
  area for the crane. *Cost if wrong:* a few camera lines in `MeteorClient.cutscene`.
  The UFO cutscene has the same fly-through and was left as the owner approved it; the fix is offered as a follow-up.
- Ruling (2026-10-11): dazed stars made bigger (4.6 x 2 stud billboard) with a dark rim under each star. On the yellow
  Thunder sand the plain yellow flare stars disappeared. Same VFX Studio flare texture. *Cost if wrong:* sizes in
  `makeStars`.
- Fix (2026-10-11): `UFOClient.resetPose` reset only Motor6D joints. This game's avatars use AnimationConstraint joints,
  so the reset after an abduction did nothing (the Animator usually overwrote it a frame later). Now it resets both.
- Test fix (2026-10-11): the WST egg strike could hit the egg the player had just dropped. The player was then knocked
  down as a bystander (correct behaviour) and was still down when the STOP test started. The test now stands next to
  the egg on purpose, checks "a bystander in the egg's blast is knocked down", and waits until the player is up.

## Ledger: v2, 2026-10-11
The owner asked for four things:
1. Fix the UFO cutscene.
2. Meteor sounds that aren't the UFO's.
3. A black storm cloud with thunder that the meteors fall from.
4. A cutscene that makes sense, instead of "one meteor splits into 8".

- **Done: UFO cutscene.** The same omen-then-flash-cut opening as the Meteor's. Checked from the hub.
- **Finding: shared sounds.** Two were shared: the Meteor start was the UFO's siren asset (9118781307) pitched down, and
  both cutscenes ended on the bat whack.
  - Replaced with PSE thunder: `MeteorStart` (Lion Roar Searing Blast 1), `MeteorTitle` (Searing Blast 7),
    `MeteorThunder1-3` (Thunder Lightning 3/5/7), `MeteorThunderFar` (Distant Boom), `MeteorStorm` (Distant Rumble 2,
    a 136 s loop).
  - PSE ids are alphabetical: the thunder sits at 9120011395-9120030275.
  - Test added: no Meteor banner sound shares an asset with the UFO, and the client plays no UFO or bat sound.
- **Ruling: the cloud is client-side,** drawn by every client from the server's folder attributes. The server only owns
  where meteors come from (`From`). *Cost if wrong:* nothing; it's decoration.
- **Ruling: base height 85 studs** (first 105). From the runway at 105, players saw it only far ahead. *Cost if wrong:*
  `cloudBase`.
- **Ruling: no meteors while the cloud glides between areas** (6 s), so meteors never come from empty sky. *Cost if
  wrong:* `cloudMove`.
- **Ruling: lightning is decoration.** It never hits anyone; bolts land at least 24 studs from you. *Cost if wrong:* a
  gameplay hit would need server records like meteors.
- **Ruling: the belly glows for 0.5 s before each meteor,** a readable tell. *Cost if wrong:* `GLOW_LEAD` in
  MeteorClient.
- **Look fixes after seeing it in Play:**
  - The first billow texture (Smoke #3) had ink outlines, which looked like bubbles; it's now the soft #4.
  - The first cool gradient read navy; it's now charcoal and re-imported.
- **Test infrastructure:**
  - `ServerStorage.WeatherMove` (Studio only) moves the running weather like a scheduled move. Tests run in Studio's
    command context, where `require` of a weather module gives a separate copy that isn't running, so calling its
    `moveTo` did nothing.
  - `workspace.WeatherTestStay` (Studio only) keeps a weather in its first area, for looking at it.
  - The "No Waves still clears" check now waits up to 2 s (0.3 s flat was flaky).
- **Tests:** WeatherTests 84/84, WeatherServerTests 134/134 (clean Play session), AdminTests 98/98,
  AdminServerTests 35/35.
- **Not re-done:** the 2-player check after the cloud was added (single-player visual checks only).

## Ledger: v3, 2026-10-11 (HQ models)
The owner: "The idea is cool, but i guess we gotta change the models, sorry but they are low polygon, we need high
quality, it looks like trash." Then: "also the storm models fix."
- **Done: all four meteor-shower models rebuilt** (`Weather/Meteor/HQ/`, README "HQ models"):
  - Meteor (7k tris), MeteorBig (19.5k) and MeteorChunk (1.5k) are baked from 0.08-1.3M-tri sculpts;
  - the StormCloud is 4 pieces x 19k tris from a 2.1M-tri SDF sculpt;
  - every part has a SurfaceAppearance (colour x AO, normal, roughness) and Precise fidelity.
- **Ruling: SurfaceAppearance via the 3D importer.** The importer turns an FBX's Principled material (base colour,
  normal map, roughness textures) into a SurfaceAppearance uploaded as ZAB Studio, with no separate image uploads.
  *Cost if wrong:* nothing, it was verified in Studio.
- **Ruling: RenderFidelity Precise on all of them.** On Automatic, Roblox swaps in a simplified mesh at range, and the
  cloud is always seen from range. *Cost if wrong:* a little GPU time, about 100k tris for one cloud per client.
- **Ruling: the cloud is a Model of 4 MeshParts** (the 20k-tris-per-MeshPart limit).
  - `MeteorClient.makeCloud` builds an invisible core Part from the Model's bounding box; the VFX attachments and the
    rumble hang on it, as before.
  - The pieces follow the core; their Size is only touched while the cloud forms or dissolves.
  - A plain MeshPart template still works (old code path).
  - *Cost if wrong:* a few lines in `makeCloud` / `updateCloud`.
- **Ruling: the cloud's darkest colour is warm charcoal sRGB (36, 32, 30), not near-black (10).** In Play, the belly
  read as a flat black ceiling with no lobes. AO darkens the crevices, so it still reads black. *Cost if wrong:* one
  ramp in `build_storm_hq.py`.
- **Ruling: no glow on the meshes (owner rule).** The magma cracks are albedo only, so in the cloud's shadow they are
  dim; the trail VFX carries the fire. *Cost if wrong:* the owner may want brighter cracks; they would come from VFX.
- `cloudSize` is now (207, 93, 405) and `POUCH` is 10 (the new mesh). The server's From-in-base bounds follow
  `cloudSize`.
- **Tests:**
  - WeatherTests has a new check: the HQ assets each have colour + normal maps and Precise fidelity, the cloud is a
    Model of pieces, and no part is Neon.
  - A guard check confirms the old low-poly set fails that HQ check. WeatherTests is now 86.
- **Backup:** the v1 models are in `ServerStorage._Backup_MeteorV1`.
- **Test fix: "No Waves still clears" failed once (2 waves left).** Admin boosts run in every server. A No Waves
  boost left on by my visual checks was still active when the fresh session started, so `boostStart` changed nothing
  and WaveServer's clear-on-change never fired.
  - The check now stops a running No Waves first, puts a wave on the runway, and checks the count was above 0 before
    the boost. Before, it could pass with no waves at all.
  - *Real-game effect:* an owner extending an active No Waves leaves their own admin-spawned waves running. That's
    harmless, so it was left as is.
- **Final regression** (TestFreshSave = true, set back to false afterwards): WeatherTests 86/86, WeatherServerTests
  134/134 (fresh Play session), AdminTests 98/98, AdminServerTests 35/35.

## Ledger: 2026-10-11, one weather per hour
The owner: "make in 1 hour there to be only 1 weather."
- **Done:** `WeatherConfig.EVERY = 3600`. Any start (scheduled, admin or late-joined) sets the next scheduled weather
  to an hour later; a stop no longer reschedules. `workspace.WeatherNextAt` publishes when the next one is due.
- **Ruling: the hour counts from the START, and admin starts count.** That way there is never more than one weather
  inside an hour on a server, even when the owner starts one by hand. *Cost if wrong:* if admin weathers shouldn't
  push the natural one back, remove one `setDue` line.
- **Ruling: a new server's first weather still comes after 10-20 min (GAP),** so players in a fresh server don't wait
  an hour to see one. *Cost if wrong:* one number.
- **Finding:** the old "they take turns" claim was wrong. NO_REPEAT (15 min) was always over by the next pick, so it
  was a coin flip every time. It still is: the owner didn't pick alternation (offered).
- **Tests:** WeatherTests 87 (EVERY = 3600 and every weather fits in it), WeatherServerTests: next due = start + 3600,
  and a stop doesn't change it.
- **Test fix:** "carried egg dropped at the catch spot" failed once. The test carried the area's *first* listed egg,
  which can be seconds from timing out (one had 18 s left, and the test takes about 15 s), so it could despawn
  mid-test. The test now picks the egg with the most time left and reports carrying / parent / distance on failure.
- **Final:** WeatherTests 87/87, AdminTests 110/110, WeatherServerTests 136/136 (fresh Play), AdminServerTests 46/46;
  TestFreshSave back to false.
