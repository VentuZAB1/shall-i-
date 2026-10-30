# SLINGSHOT thumbnails, 2026-10-22: notes

Status: **DONE**.
- Deliverables: `thumb_1_launch.png`, `thumb_2_secret.png`, `thumb_3_tsunami.png` (1920x1080) and `sheet.png` (full size plus 400 px previews).
- The stage now lives in `ServerStorage._ThumbStage_2026_10_22`, with 0 tags and 0 scripts. Nothing new is left in workspace.
- ShowDevelopmentGui is back to true, Lighting was never changed, and Studio is in Edit. The StarterGui ScreenGuis were never touched: ShowDevelopmentGui = false alone hid the whole HUD in Edit captures.

## Final picks (what each thumbnail shows)

| File | Capture | Camera -> look-at (FOV 70) | Shows | Headline |
|---|---|---|---|---|
| `thumb_1_launch.png` | `work/caps/S1_6.jpg` | (-3, 32, -66) -> (3, 36, -46) | The grinning avatar flies big out of the real hub slingshot, speed streaks leading back to the pouch. The giant jack-o'-lantern sits behind; the hub plaza, pads and walls are below. | LAUNCH / FOR EGGS! (yellow-orange) |
| `thumb_2_secret.png` | `work/caps/S2_8.jpg` | (45, 4.5, 112) -> (38, 10, 100) | Thunder Rex (Storm egg 1% SECRET) roaring out of a cracked Storm egg, low hero angle, cyan light rays, gold and cyan sparkles, shell chunks. | 1% SECRET / PET! (gold) |
| `thumb_3_tsunami.png` | `work/caps/S3_5.jpg` | (-8, 2.5, -1311) -> (8, 9, -1328) | Shocked avatar sprints at the camera holding a big Magma egg overhead; the tsunami wall with its foam crest diagonal behind, splash chunks, Fire runway and VIP hideout wall. | RUN FROM THE / TSUNAMI! (yellow-red) |

### What changed in Phase B, and why
- **Launch:**
  - The camera moved in closer (S1-1 had the avatar too small).
  - The 3 streaks that crossed the pumpkin's face were trimmed and 6 removed (`S1_5` -> `S1_6`).
  - Body streaks shortened (`torsoTrail` 9, wind lines 4-9 studs).
- **Secret:** the first pick (S2-1, `S2_1.jpg`) was rejected at 400 px. Rex's face was turned away, he was dark on dark, and the pumpkin covered a third of the frame. The fix was a rebuild with these opts:
  - `{eggScale = 1.6, facing = Vector3.new(-0.45, 0, 1), camPos = Vector3.new(31, 5, 113), feet = -0.75}`
  - shot from the plaza side in profile, with the jaws open towards the left and the text in clear sky on the right
  - the 4 shell chunks that sat in the text area were lowered by hand after the build (not in the builder)
- **Tsunami:**
  - S3-1 had the runner small and the wave crest cut. The pick is a tighter 3/4 (`S3_5`).
  - The crop is `crop_h = 700`, so the egg and the feet both stay inside the frame.
- **No in-world text besides the headline:**
  - The VIP sign in thumb 3 is painted out with clean wall from the same capture.
  - The SELL stall sign in thumb 2 is blurred.

### Other captures kept (`work/caps/`)
| Capture | What it is |
|---|---|
| `S1_1` | first wide pick |
| `S1_4` | closer, text space only top-right |
| `S1_5` | before the streak trim |
| `S2_1` | original 3/4 pick |
| `S2_2` | wide with nest |
| `S2_6` | reverse angle |
| `S2_7` | before the chunk fix |
| `S3_1` | wide 3/4 |
| `S3_4` | very tight, the egg crowds the top |

`S3_5` is the final tsunami pick. The plate with no runner (wave + wall only, for mattes) was captured but not used.

## Composite (`work/compose.py`)
`python work/compose.py` rebuilds all 3 plus `sheet.png` from `work/caps/`. To rebuild just one, pass its file name.

Per thumbnail:
1. **Patches** on the raw capture: copy or blur, used for sign text.
2. **Crop and scale:** crop to 16:9 and Lanczos-upscale to 1920x1080.
3. **Grade:** saturation x1.12-1.18, contrast x1.08.
4. **Focus:** radial soft focus away from the subject (Gaussian 3-5 px), then an unsharp mask on the subject.
5. **Vignette.**
6. **Headline:**
   - Luckiest Guy, found automatically in `%LOCALAPPDATA%\Roblox\Versions\*\content\fonts`
   - gradient fill with a glossy top band
   - 16 px navy outline, 10 px extrude, soft drop shadow
   - tilted ±4-5°, inside the centre 80 % safe area

## How to rebuild a scene in Studio
1. Move `ServerStorage._ThumbStage_2026_10_22` back to workspace and rename it `_ThumbStage`. The builders look for `workspace._ThumbStage`.
2. `require(workspace._ThumbStage._Builders.S1_Launch:Clone())({})`, and the same for S2 / S3. Each opt can be overridden; the defaults are at the top of each builder.
3. Before each capture:
   - run `require(workspace._ThumbStage._Kit:Clone()).emitAll(workspace._ThumbStage.<scene>)`
   - keep only one scene folder in workspace
   - set `StarterGui.ShowDevelopmentGui = false`
4. Afterwards:
   - restore ShowDevelopmentGui from `_Originals`
   - strip tags, then move the stage back to ServerStorage
- The builders strip tags, attributes and scripts from every clone. Never keep a tagged copy (see the 10-21 Slingshot tag bug).

---
Phase A notes (staging + framing options) follow.

## What is staged (owner's Studio, Edit)

`workspace._ThumbStage` (nothing else was added to workspace; no map object was moved or edited):

| Child | What it is |
|---|---|
| `_Kit` (ModuleScript) | Helpers. `makeAvatar` builds the R15 avatar from a HumanoidDescription. `pose` bakes an `Intro.Poses`-style pose into anchored CFrames. Also `project` (world point -> 16:9 frame u,v), `streak` (speed-line beam), `foam` (static particles), `emitAll`, `strip`, `clearAttrs`. |
| `_Builders.S1_Launch / S2_Secret / S3_Tsunami` (ModuleScripts) | Each one rebuilds its scene folder from scratch. Use `require(workspace._ThumbStage._Builders.S2_Secret:Clone())({})`. The `:Clone()` avoids Studio's require cache. Opts can be overridden. |
| `_Originals` (Configuration) | The original value of every Lighting / DoF / Atmosphere / Bloom / SunRays / ColorCorrection property, plus `StarterGui.ShowDevelopmentGui` (= **true**) and the camera FOV (= **70**), saved as attributes. **Nothing is changed right now** (a DoF test was reverted; captures ignore DoF anyway). |
| `S1_Launch` | Avatar, body streaks and wind lines. The folder also holds 5 Wood eggs and a Normal wave on the Grass runway, which only the runway-chase framing uses. |
| `S2_Secret` | Cracked Storm egg on Base4's hatch floor; Thunder Rex in his roar pose; light rays, rim light, flying shell chunks, cyan and gold sparkles. |
| `S3_Tsunami` | Sprinting avatar holding a Magma egg overhead; a Normal wave right behind it; crest and base foam; splash chunks. |

Safety:
- Every clone is stripped: 0 CollectionService tags, 0 gameplay attributes (EggSpawner/pet attributes removed), 0 scripts.
- Every part is Anchored with CanCollide, CanTouch and CanQuery all off.
- The avatars' Humanoids have name and health display off.

### Real game content only
- **Slingshot, hub, giant pumpkin, runway:** the live map. Each shot is framed to use them as backgrounds.
- **Eggs:** `ServerStorage.Assets.Eggs` (Wood, Storm, Magma).
  - The Storm egg is at x1.9 (about 12 studs). `EggSize` says a 10K-50K KG egg is 10-14 studs, so that is honest.
  - The carried Magma egg is at x0.95, with the nest removed.
- **Wave:** `ReplicatedStorage.WaveModels.Normal`, built 120 x 35 x 75 exactly like WaveClient. Foam is static particles: crest at the lip (about 10 studs behind the front at the top, measured by raycast), plus base foam. WaveClient's own spray is particles too.
- **Pet:** `ReplicatedStorage.CreatureModels.ThunderRex` (Storm egg 1% SECRET). It stays at real size because ScaleTo blows the bone pose up (tested again today). It is posed with `CreatureAnimator` `roar` at its peak event.
- **Avatar:** built with `Players:CreateHumanoidModelFromDescription`. Not a real player's avatar.
  - Items: Roblox **Red Beanie & Blonde Hair** 221175236, **Blue and Black Motorcycle Shirt** 144076358, **Black Jeans with Sneakers** 382538503.
  - Classic head (SpecialMesh Head) with Roblox face images: "Know-It-All Grin" 26424652 (launch) and shocked face 147144198 (tsunami).
  - Poses come from `ReplicatedStorage.Intro.Poses`: `run` + `carry`, plus a flight pose in the S1 builder.

## Framings (camera position -> look-at, FOV 70 for all)

Rule for every capture: frame for 16:9. The capture comes out about 2:1 (1519x753 today), so crop the sides, never the top or bottom. The `K.project` numbers below are for the 16:9 frame (u,v in 0..1).

### 1. LAUNCH ("LAUNCH FOR EGGS!")
| id | camera | look-at | notes |
|---|---|---|---|
| **S1-1 PICK** | (-6.5, 31.5, -67) | (6, 33.5, -46) | Builder default (`dist = 22`). The avatar has just left the pouch: grinning, flying up-left, streaks leading back to the pouch. Slingshot fork and pouch big at the bottom, giant pumpkin on the right. Text goes top-right over the sky (the beanie is at v≈0.25). |
| S1-2 | (-6.5, 36.5, -84) | (5.5, 43.5, -64) | Rebuild with `{dist = 38}`. More sky for text, avatar centre, pumpkin right. Only the fork tips show, so the slingshot reads weaker. |
| S1-3 | (9, 45, -67) | (-3, 30, -150) | Rebuild with `{dist = 38}`. Chase view from behind, down the runway with the eggs and the wave at the end. Weak: back of the head, green eggs on green grass, the wave tiny. |

### 2. SECRET PET ("1% SECRET PET!")
| id | camera | look-at | notes |
|---|---|---|---|
| **S2-1 PICK** | (31.5, 7, 89) | (39.5, 12.8, 99) | Close 3/4 low view. Rex roaring big out of the cracked egg rim, rays and sparkles behind, the giant pumpkin cut by the right edge. Text goes top-left over the sky (Rex's crown is at v≈0.32). |
| S2-2 | (27.5, 5.5, 85.5) | (38.5, 11, 100) | Wider: the whole egg, the nest, Rex smaller. |
| S2-3 | (47, 4, 80) | (37, 11, 102) | Front-low. Rex is seen head-on in the roar, so the face is hidden. Weakest. |

### 3. TSUNAMI ("RUN FROM THE TSUNAMI!")
| id | camera | look-at | notes |
|---|---|---|---|
| **S3-1 PICK** | (-10, 2.6, -1310) | (8, 9.5, -1328) | Builder default (`heading = (-0.55, 0, 0.83)`). 3/4 low view on the Fire runway: the wave is a diagonal crashing wall with a foam crest, the shocked avatar sprints at the camera with the big egg, splash chunks in the foreground. Text goes top-right over the sky and red wall. |
| S3-2 | (-2, 2.5, -1303.5) | (5, 10.5, -1335) | Rebuild with `{heading = Vector3.new(-0.08, 0, 1)}`. Straight-on: the wave is a flat wall behind, the runner centred. |
| S3-3 | (-17, 3.5, -1309) | (6, 10, -1326) | Same build as S3-1, wider side view: more wave, a smaller runner. |

## Phase B procedure (after "GO SCREENSHOTS")
1. Check the state: Edit mode, nobody playing.
2. `game.StarterGui.ShowDevelopmentGui = false` (original: true).
3. **Isolate:** parent the two scenes you are NOT shooting to nil (or ServerStorage). For example, S2's sparkles show up in S1's background.
4. **Particles:** they are not saved and they fade when the camera is far away. Run `require(workspace._ThumbStage._Kit:Clone()).emitAll(workspace._ThumbStage.<scene>)` right before EVERY capture. (S1 has no particles.)
5. `screen_capture` each framing above. Optional: a second capture with the subject hidden, to build a difference matte for a PIL background blur. DepthOfField does not render in Edit captures.
6. Composite in PIL to 1920x1080:
   - crop to 16:9 and upscale with Lanczos
   - sharpen, colour grade and vignette
   - headline in Luckiest Guy (`%LOCALAPPDATA%\Roblox\Versions\version-*\content\fonts\LuckiestGuy-Regular.ttf`) with a thick dark outline and a gradient fill
7. Cleanup:
   - Restore `ShowDevelopmentGui` and any Lighting value from `_Originals`.
   - Move `_ThumbStage` to `ServerStorage._ThumbStage_2026_10_22`.
   - Re-check: 0 tags, scripts disabled, nothing new left in workspace.
