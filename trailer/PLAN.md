# Trailer production plan + state

**Owner, 2026-10-15:** "animate it in Roblox Studio and add it into the admin panel. When I click it I run it, make it
black screen for 2 s so I can turn on OBS, and I will record it ingame full reso". Also: make the pets face the camera,
and make the pumpkin look straight during the cinematic.
How to record / finish / upload: README.md.

## Built (Studio, 2026-10-15, not published)

- `ServerStorage.AdminUI.Trailer` (ModuleScript, about 1,500 lines, local copy `studio/Trailer.lua`) + `Trailer.Assets`.
- AdminClient: SERVER tab gets a TRAILER section with PLAY TRAILER.
- HalloweenClient: pumpkin target = straight ahead while `player.TrailerPlaying` exists.
- Bug fix: `Map.Hub.Floor` was Anchored = false, so in every Play/live server it fell and was destroyed, and the hub showed the cloud sea.
- Backups: `ServerStorage._Backup_Trailer.Before`.

## Timeline

Content seconds; music "Race To Finish" from 142.4 s. The drop at 144.4 s = release; the last hit at 172.2 s = title.

| t (s) | Shot | Caption |
|---|---|---|
| 0 | HOOK: through the fork, the avatar in the pouch, the giant pumpkin behind; release on the drop | — |
| 2.45 | Chase cam flight over the runway | LAUNCH |
| 4.9 | Superhero landing (x 18 lane, no decor), egg lift | GRAB AN EGG |
| 7.2 | Sprint at the camera, tsunami behind | OUTRUN THE TSUNAMI |
| 9.0 | Crane: dive into the Grass trench, the wave rolls over (slow-mo) | — |
| 11.2 | Hub gate: burst through, egg banks, wave crashes behind | — |
| 12.4 | Storm egg wobbles x3 + cracks; burst into Thunder Rex (faces camera, roar) | HATCH FIERCE PETS / THUNDER REX - SECRET |
| 16.2 | Pet cuts: Inferno Phoenix (Fire), Abyss Weaver (Thunder), Cosmic Leviathan (Water) | — |
| 18.4 | x20 Diamond Rainbow treadmill, "+2M" popups | TRAIN YOUR SPEED |
| 20.6 | Storm cloud, meteor strike | METEOR SHOWERS |
| 22.6 | UFO saucer beams an egg up | UFO INVASIONS |
| 24.4 | Halloween hub drone at golden hour (pumpkin looks straight) | HALLOWEEN HUB |
| 27.4 | 1,000,000 KG Celestial egg + "$1.25T" counter | — |
| 29.8 | Title: game icon + SLINGSHOT / FOR EGGS over a wide hero shot | — |
| 32.5-33.4 | Fade to black (+1.5 s black), then everything is restored | — |

## Lessons

- `Model:ScaleTo` on a CreatureModels pet breaks CreatureAnimator (the bones blow up to 400 studs). Use real size.
- CreatureModels face -Z like any model. Check facing by measuring the head bone vs the pivot distance to the camera, not by eye.
- A BillboardGui parented inside a ScreenGui never draws. Parent it to the PlayerGui.
- Shadow / Celestial (z < -1700) don't stream in from the hub, even with RequestStreamAroundAsync. Water / Thunder / Fire do.
- The Roblox menu button can't be hidden (TopbarEnabled false still shows it). Crop it in post (`finish_video.py`).
- Studio audio was silent because of Studio's own Mute (View > Mute in the new UI), not Windows.
- Recording Studio itself with OBS (the first approach) worked for video, but the Studio window had to be enlarged past the screen.
  The owner chose in-game recording instead.

## Status

- [x] Rules checked; shot list; music picked by loudness scan
- [x] Built + Play-reviewed every shot (frozen frames + real-time runs), no errors in the log
- [x] Pets face the camera; pumpkin straight; floor fix
- [ ] OWNER: save + publish, record with OBS, run finish_video.py, upload (README.md)
