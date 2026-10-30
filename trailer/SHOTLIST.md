# SLINGSHOT FOR EGGS — trailer shot list (v1, 2026-10-15)

Target: **30 s**, 1920x1080, 16:9, H.264 MP4, 60 fps, under 100 MB, one video + one audio stream.

## Roblox rules it must meet (checked 2026-10-15)

Live Creator Hub > Places > Videos page:
- .mp4 / .mov, max 100 MB, ~15 Mbps recommended, max **60 s**
- 640x360 to 1920x1080, 16:9
- 1 video slot, **3 uploads per month**; a failed or rejected upload still uses one

Creator Docs "Thumbnails" (video guidelines):
- Allowed: real gameplay, camera work, minor post-processing, a logo/branding overlay, highlight-reel cuts, Roblox-catalog music.
- Not allowed:
  - voice-over, or music with lyrics
  - mechanics or UI the game doesn't have
  - graphics better than what players really see
  - real-life footage
  - advertising, promotions, or subjective claims ("BEST", "#1", "FREE")

DevForum (2026): the file must have **exactly one video stream**; an embedded cover image fails the upload.

## Shots

| # | Time | What we see | Camera | Text |
|---|------|-------------|--------|------|
| 1 | 0:00-0:02 | **HOOK**: avatar in the pouch, bands stretched; release, and the player rockets over the lens | Low, under the slingshot, looking up; brief slow-mo, then a speed ramp | (band snap + whoosh) |
| 2 | 0:02-0:04.5 | Flight over the long studded runway, areas to the horizon | Chase cam behind and above | LAUNCH |
| 3 | 0:04.5-0:06.5 | Landing, run to an egg, hold bar fills, egg pops overhead | Low side dolly | GRAB AN EGG |
| 4 | 0:06.5-0:10 | Tsunami rolls at camera; player sprints with the egg, drops into a trench, wave rolls over | Low wide, in front of the runner | OUTRUN THE TSUNAMI |
| 5 | 0:10-0:11 | Through the gate into the hub, "+1 egg" | Quick cut | — |
| 6 | 0:11-0:14.5 | Egg on the base wobbles, cracks, bursts; a SECRET pet (Thunder Rex) roars | Slow push-in, cut on the burst | HATCH FIERCE PETS |
| 7 | 0:14.5-0:16.5 | 3 fast pet cuts: Inferno Phoenix, Abyss Weaver, Cosmic Leviathan | Short orbits | — |
| 8 | 0:16.5-0:18.5 | Top-tier treadmill, "+X / step" speed popups | Side tracking | TRAIN YOUR SPEED |
| 9 | 0:18.5-0:22 | Meteor shower storm cloud, a meteor strike; a UFO saucer beams an egg | Wide, then close | METEOR SHOWERS · UFO INVASIONS |
| 10 | 0:22-0:25 | Halloween hub: giant jack-o'-lantern eyes follow the camera, bats, pumpkin lamps | Drone fly-through | HALLOWEEN HUB |
| 11 | 0:25-0:27 | Big numbers: money counter in the trillions, a 1,000,000 KG egg | UI / egg-label close-ups | (the numbers) |
| 12 | 0:27-0:30 | Hero shot of the hub + slingshot, then the title card | Slow pull-back | **SLINGSHOT FOR EGGS** + game icon |

## Look and sound

- **Text:** short ALL-CAPS words in Luckiest Guy (free OFL font that ships with Roblox), white with a thick dark outline, punched in on the beat.
- **HUD:** hidden during cinematic shots; the real UI shows only in shot 11.
- **Music:** one Roblox-catalog APM instrumental, recorded from Studio's own audio output (no outside download).
- **Sound effects:** the game's real sounds, recorded live with each take (slingshot, wave roar, egg crack, hatch fanfare, meteor thunder).
- **Footage:** real Play-mode gameplay in Studio, filmed by scripted cameras. Only the test save is used (TestFreshSave = true); it gets late-game money/speed for shot 11.
- **Edit:** ffmpeg (bundled with Python) for cuts, speed ramps, text, mix, and export.
