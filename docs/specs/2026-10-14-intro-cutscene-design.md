# New-player intro cutscene (2026-10-14)

Owner request (verbatim summary): a fully cinematic intro that plays instantly when a NEW player joins, before the
tutorial: slingshot launch -> egg pickup while a swinging wave comes -> run through the hole -> jump wave -> safe,
exhausted "WHEW!" (Minecraft-style expressive) -> smooth hand-over to the tutorial. "Do as recommended, don't ask."

## Decisions (made autonomously, owner away)
- **Who sees it:** saved field `IntroSeen` (PlayerData). Brand-new saves = false, every existing save = true, so it
  plays ONCE. Finished or skipped -> `ReplicatedStorage.Tutorial.IntroSeen` remote -> saved true.
  Studio: workspace attribute `TestIntro = true` replays it every join (use with `TestTutorial = true` to also get the
  tutorial afterwards; TestFreshSave alone skips both).
- **Length + SKIP:** ~30 s with a SKIP button after 1 s. The design playbook warns that first-minute bounce hurts
  discovery, so the intro must stay short, skippable and teach the real loop (slingshot -> egg -> waves -> safety).
- **Puppet, not the real character:** a local clone of the player's avatar (their real look) plays the scene; the real
  character waits safe in the hub, hidden, controls off. At the end the real character is moved to the puppet's final
  spot/facing and the camera eases back, so the hand-over is seamless. Nothing in the scene touches the server
  (no real egg, no real waves, no deaths).
- **Animation:** procedural keyed poses on the R15 joints (Motor6D or AnimationConstraint -> converted to Motor6D on
  the puppet), the same no-upload approach as `ReplicatedStorage.Knockdown`. Root motion along scripted paths.
  Non-R15 avatars get root motion only.
- **Waves:** local copies of the real `WaveModels.Swing` (two halves + glowing hole posts, like WaveClient) and the
  JUMP WAVE (taller than in game so the jump reads as a big moment). Real wave visuals are hidden locally while it plays.
- **VFX:** clones of existing library emitters (WeatherFX MeteorImpact Dust/Ring, TractorBeam Sparkles, CloudBurst
  Puff) recoloured; WaveClient-style spray on the wave lips; emoji sweat drops; no new hand-made particle textures.
- **UI (Check-UI):** cinematic letterbox bars, SKIP = canonical iconless button, "WHEW!" in GothamBlack + black stroke
  with a gold gradient, popping on its centre.
- **Sound:** existing ids only (Slingshot Stretch/Release/Whoosh/Land, SFX Pickup/WaveRoar/Splash/Bank/HatchWin...).

## Shot list (cutscene seconds; slow-mo stretches real time)
| t | shot |
|---|---|
| 0-1.2 | fade in; low camera behind the avatar, the giant slingshot ahead; sprinter crouch |
| 1.2-2.6 | sprint to the launch pad, side tracking dolly |
| 2.6-3.1 | hop up into the pouch, low hero angle under the fork |
| 3.1-4.4 | pull back (bands stretch, FOV narrows), over-the-shoulder view down the runway |
| 4.4-7.2 | RELEASE: FOV punch + shake, superman flight over the gate, chase camera, wind trails |
| 7.2-8.2 | superhero landing (three-point), dust ring |
| 8.2-10 | run to the egg, lift it overhead; the ground starts to rumble |
| 10-11.6 | low reveal: a massive SWINGING WAVE with its glowing hole; the avatar turns and bolts |
| 11.6-15 | chase toward the hub, look-back over the shoulder, cut diagonally into the hole; SLOW-MO as the walls pass |
| 15-19 | JUMP WAVE races in; tuck jump, bullet-time orbit at the apex, land and keep running |
| 19-20.5 | through the gate: the egg banks (sparkles + "+1 EGG") |
| 20.5-23.5 | stumble to a stop, hands on knees, panting, sweat drops |
| 23.5-26.5 | stand, wipe the forehead, big exhale: "WHEW!" |
| 26.5-28 | bars retract, camera eases behind the real character, tutorial step 1 starts |

## Animation references (owner rule: 1-3 animationreference.org clips before animating)
- **Spider-Verse (#jumping, 3.4 s, 24 fps):** f37 mid-air roll, f51 three-point landing (one hand down, other arm
  back, head up), f64-f78 leap: knees tucked high, arms flung out for balance, body arched; dutch low camera.
  -> superhero landing pose + jump-wave tuck + bullet-time camera.
- **Tangled (#running-locomotion, Flynn chased, 4.9 s):** sprint toward camera, big arm pumps, strong forward lean,
  looks back over the shoulder mid-stride (f63-f83) without breaking the run; ~10 frames per step.
  -> chase run cycle + look-back beat in front of the swinging wave.
- No exhausted/relief clip found by tag search; the WHEW is acted from the principles (anticipation: the big inhale
  lifts the shoulders, the exhale drops them with overlap in the head and arms) in the Minecraft-style "whole body
  bobs with the head" look the owner asked for.

## Files
- `ServerScriptService.PlayerData` (IntroSeen), `ServerScriptService.TutorialServer` (IntroSeen remote, TestIntro)
- `StarterPlayerScripts.TutorialClient` (waits for the intro, max 90 s)
- `ReplicatedStorage.Intro` (Poses module, Assets: EggShell / EggNest)
- `StarterPlayerScripts.IntroCutscene` (the scene)
- Backup: `ServerStorage._Backup_IntroCutscene.Before`
