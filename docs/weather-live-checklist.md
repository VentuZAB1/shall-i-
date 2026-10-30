# Weather (UFO Invasion + Meteor Shower): live checklist (2026-10-10, Meteor added 2026-10-11)

## 1. Save, publish, then migrate the servers
The weather system lives in the open Studio place. Nothing is live until you **File > Save** and **Publish**.
Then, in the Creator Hub (Experience > ... > **Migrate to Latest Update**), restart the live servers.
**Why:** UFO and Meteor eggs are saved in a new format. A server still running the old code can't read them: the player would get no egg tools there, and Sell would error. No data is lost, but migrating avoids that.

## 2. Two-player check (5 min, before or right after publishing)
**Done by Claude on 2026-10-10 (Studio Server & Clients, 2 players): everything below passed on both clients.**
That covered the cutscene, the 4 saucers, the ring and beam on the other player, the floating pose, the egg beam, the "+UFO" pop-up, and the fly-out on STOP.
Repeat it in a live server if you like.
Use Studio **Test > Clients and Servers** with 2 players, or two accounts in a live server.
- [ ] Admin menu > ADMIN ABUSE > **WEATHER: UFO INVASION > START**. Both players on the hub or runway see the cutscene: the mothership comes down, its belly opens, the saucers drop out, then "UFO INVASION - AREA -".
- [ ] A player on the slingshot or in the tutorial gets **no** cutscene.
- [ ] Stand in the UFO area. A white-green **target ring** appears under you and shrinks. Then the green **tractor beam** lifts you ("ABDUCTED!") and throws you.
- [ ] A saucer beams an egg: the egg floats up, turns **"UFO ..."** and gets a green glow.
- [ ] Pick up that egg, bank it, place it at your base and hatch it. The pet tag shows a green **"UFO"** on top (no x1.5 since 2026-10-10; the $/s still includes it).
- [ ] The second player sees the same saucers, beams and rings.
- [ ] Start it once in **Celestial** (or let it move there): the cutscene shows the Celestial area, not empty sky.
- [ ] **STOP** ends it at once: the saucers fly up and out (about 2.5 s), and the waves run normally again.

## 2b. Meteor Shower two-player check
**Done by Claude on 2026-10-11 (Studio Server & Clients, 2 players), before the storm cloud: everything passed on both
clients.** Both clients played the full cutscene and got their camera back. Player 2 saw Player 1's ring, the knock-back
and the fall animation. Both saw the egg strike, "+METEOR", the ember aura and the orange METEOR label.
The storm cloud (added later on 2026-10-11) was checked single-player only. Every client draws it from the same server
attributes, but a second-player look is worth doing.
- [ ] Admin menu > ADMIN ABUSE > **WEATHER: METEOR SHOWER > START**. Players on the hub or runway see the cutscene:
  - where they stand, the light drains, far thunder rolls and the camera looks up;
  - a lightning cut to the area: a **black storm cloud billows into being** with lightning crawling through it;
  - its belly glows orange, and a giant burning meteor tears out of it onto the far end of the runway;
  - the storm unleashes the barrage;
  - "METEOR SHOWER - AREA -" slams in to a thunder roar.
- [ ] The **storm cloud** hangs over the meteor area: you see it from the runway ahead of you and from the hub.
  - Lightning flickers in it, sometimes down to the ground (harmless), with thunder.
  - The screen flashes when it strikes near you, and the area under it turns darker.
  - On a move it **glides** to the next area; no meteors fall while it travels.
  - On STOP it dissolves.
- [ ] **HQ models (remade 2026-10-11 after "low polygon ... looks like trash"):** the meteors are sculpted cracked
  rock with glowing-orange crack networks (not smooth blobs), and the cloud is a billowing cumulonimbus with cauliflower
  tops and hanging pouches under its base. Up close and from far away, nothing should look faceted. They use
  SurfaceAppearance maps, so check on a phone too (lower graphics levels drop the normal maps, but the colour stays).
- [ ] **Sounds:** the start is a thunder roar, not the UFO siren. The title slam is thunder too. Nothing is shared with
  the UFO.
- [ ] Stand in the meteor area. An orange **target ring** follows you; it **locks** (turns red) just before impact.
  **Run out of it** and you dodge. Stay in it and you're **blown back and knocked down** (you land on your back, dazed
  stars over your head, then you get up; about 3 s).
- [ ] Carrying an egg when hit drops it.
- [ ] Standing next to someone who gets hit knocks you down too (blast radius 9).
- [ ] A meteor hits an egg: it hops, gets an ember aura, "+METEOR" pops up, the label turns **"METEOR ..."** and its
  timer gets +30 s.
- [ ] Every meteor comes **out of the cloud**. Its belly glows orange where one is about to break out (a tell), then
  the meteor tears through the base and falls at a slant.
- [ ] Small meteors keep landing around the area, never right next to a player.
- [ ] Hide in a trench, or be on the slingshot: you're never targeted.
- [ ] **STOP** ends it at once; anyone knocked down stands up on the spot.

## 2c. Several weathers at once (2026-10-12)
**Done by Claude on 2026-10-12 in Studio (solo Play, a late-joining client, the iPhone 17 Pro emulator).** The
two-server parts need live servers.
- [ ] Admin menu > ADMIN ABUSE > WEATHER: pick **METEOR SHOWER and UFO INVASION** (both turn blue) > **START**. Both
  start at once **with no cutscene**: just the bar announcements, the effects and two icons with timers. The waves keep running.
- [ ] **Weather icons**, bottom right (on a phone: left of the jump button; your reference design, 2026-10-12):
  - one picture per weather (the saucer, the meteor), side by side;
  - its time under it ("4:12", red under 1:00);
  - hover (PC) or tap (phone) one: its name and what it does.
  Running ADMIN ABUSE boosts are icons + timers in the SAME row (no label), and everything is in the order it
  started: the newest at the right end.
- [ ] Pick only UFO > **STOP**: just the UFO ends. Pick nothing: the button says **STOP ALL** and ends every weather.
- [ ] Start ONE weather while none runs: its cutscene plays as before. Start a second one while it runs: no cutscene.
- [ ] A pet from an egg that got both mutations shows **UFO** and **METEOR** on its tag, and earns x2.25 (x1.5 x
  x1.5) on top of the money boosts.
- [ ] **HOURLY WEATHER:** pick 1H / 6H / 24H > **PAUSE**. The row shows "PAUSED 0:59:59" and counts down, and no
  hourly weather starts in any server (admin weathers still work). It comes back by itself when the time is up;
  **RESUME** ends it early ("AUTO WEATHER: ON").
- [ ] Two servers: everything above happens in both, and a server that opens during an admin weather (or a pause)
  joins it.

## 3. How it runs on its own
- **One weather per hour** per server (owner 2026-10-11): the next one starts 60 min after the last one started
  (an admin START counts too; stopping one early doesn't bring the next closer). A new server gets its first one
  10-20 min after it opens. Each lasts **5:00**. Which one is a coin flip each hour (UFO Invasion or Meteor Shower),
  so the same one can come twice in a row. (Before 2026-10-11 this said "they take turns", which was wrong.)
  `workspace.WeatherNextAt` = server time the next one is due.
  The hourly one never starts while any weather runs, nor while the admin paused it (`workspace.WeatherAutoOffUntil`,
  os.time, 0 = on).
- Several can run at once (admin START; one of each type). Only a weather that starts alone gets a cutscene.
  Attributes: `workspace.Weather` = the running types ("Meteor,UFO"); per type `WeatherArea_<T>` (0 = off),
  `WeatherEnds_<T>`, `WeatherCutsceneAt_<T>`.
- Each moves between areas on its own, staying 30-90 s in each; two may share an area. The bar announces each move.
- The HUD shows one **icon + timer per weather** in the bottom-right corner (`StarterPlayerScripts.WeatherTilesClient`).
  The Admin Abuse boost icons sit in the same row (`AdminBannerClient` parents them into `PlayerGui.WeatherTiles.Row`),
  in the order they started (the row's `NextOrder` counter). The old "UFO: m:ss" pill in the boost column is gone.
- Two weathers in one area never grab the same player: someone a meteor knocked down can't be beamed, and someone a
  UFO holds can't be targeted.
- Meteor: a targeted strike every 4-7 s (max 2 in the air), 40 s cooldown per player after a knockdown.

## 4. Where things are
- Effects: `ReplicatedStorage.WeatherFX`. UFO: TractorBeam, TargetRing, UFOAura. Meteor: MeteorTrail, MeteorImpact,
  MeteorScorch, MeteorRing, MeteorAura, MeteorCloud, MeteorLightning, MeteorCloudBurst. Built only from **VFX Studio**
  library textures. Screenshots: `Weather/UFO/vfx_screens/`.
- Models: `ReplicatedStorage.WeatherAssets.UFO` (Mothership, Saucer) and `.Meteor` (Meteor, MeteorBig, MeteorChunk,
  StormCloud = a Model of 4 pieces); Blender sources in `Weather/UFO/` and `Weather/Meteor/HQ/` (README in
  `Weather/Meteor/`). The first low-poly meteor set is backed up in `ServerStorage._Backup_MeteorV1`.
- Fall animation: `ReplicatedStorage.Knockdown` (keyframed in code, no animation asset to upload).
- Settings: `ReplicatedStorage.WeatherConfig` (durations, chances, texts); mutation values in `ReplicatedStorage.Mutations`
  (Meteor x1.5, stacks with UFO to x2.25).
