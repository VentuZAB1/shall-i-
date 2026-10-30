# Glacier update: animation references (lead, 2026-10-27)

The owner's rule: before any animation, pull 1-3 clips from **animationreference.org**, note the key poses and frames, and cite them.

## How to do it (the method that works, found by Builder A)
1. Search the site's TAG pages (free). Search only matches titles, so use tag URLs: `/tags/<tag>`.
   - Useful tags found today: `animals`, `creature-animation`, `walk-cycle`, `running-locomotion`, `flying`, `wolfs-rain`, `wolf-children`, `the-cat-returns`, `elephants`, `kaiju-no-8`, `sea-beasts`, `how-to-train-your-dragon`, `dragon`, `creature`, `beastars`, `muybridge`, `locomotion`, `body-mechanics`.
   - No such tags (404 / none): quadruped, birds, idle, dig, crab, snake, golem, kneel.
2. Open the chosen clip in the site player. It costs 1 of the **25 opens/day** (the counter is in the top bar).
3. The overlay HANGS while the Browser pane is hidden, so step the frames on the **same source file**: the clip's "Cut #id" / source = the Sakugabooru post `sakugabooru.com/post/show/<id>`, the same mp4 the player streams.
   - Build a canvas contact sheet or step `currentTime` to read the key poses.
   - Anime runs at 24 fps; our clips run at 30 fps (frames × 1.25).
4. When no site tag fits (crab, snake...) or the day's opens are used up, the fallback is other frame-by-frame sources:
   - Sakugabooru posts;
   - Muybridge *Animal Locomotion* plates. The site curates Muybridge in its locomotion set and has a `muybridge` tag; the Wikimedia scans are the same plates;
   - real footage on Wikimedia Commons.
   Cite the tags you tried, so the reviewer can see the site was searched first.

## Site clips opened today (counter now 3/25)
| id | site path | source | used by |
|---|---|---|---|
| W0 | `/tags/wolfs-rain`, "Animals: Character Acting & Creature Animation (#30 - Wolfs Rain)", Yutaka Nakamura | Sakugabooru #174333 | **Wraith Hound** walk + snarl. Diagonal-pair walk, cycle ~0.9-1.0 s (27-30 f); the mouth opens over ~15 f, then holds; head level. **Also fits the Frostcrown roar and any canid/beast snarl.** |
| L0 | `/tags/the-cat-returns`, "Animals: Character Acting & Creature Animation (BD - Crowd)", Shinji Otsuka | Sakugabooru #256671 | **Frostfang Lynx** walk + crouch. Level head and back, tail carried up, cycle ~0.8-1.0 s (24-30 f). |
| (elephants) | `/tags/elephants`, "Video by projectarcheology" (the only elephant clip) | real elephant footage | Opened by the lead; the player froze (hidden pane), so no frames were read. **Mammoth / Rhino:** use Muybridge Plate 733 (elephant walking) + "Walking bison" as the step-by-step source. |

## Per pet: what to cite (builders fill in the frames in their own ANIM_REFS.md)
- **Bramble Badger:** site walk ref D + Sakugabooru #258150 (Pointer), #143881 (Pluto and the Gopher), #282941 (Once Upon a Forest). Done.
- **Frostfang Lynx:** L0 (site) + Figaro #132474 / #132272 / #132391, #143881. Done.
- **Wraith Hound:** W0 (site) + #143877, #258150. Done.
- **Ice Mammoth:**
  - the site's `elephants` tag (the clip above, cite it as found on the site) + Muybridge Plate 733 (walk);
  - for the trumpet / trunk reach: real elephant footage (Wikimedia) if found;
  - W0's ~15 f mouth-open timing for the roar onset.
- **Volt Rhino:**
  - Muybridge "Walking bison" (walk);
  - W0 for the bellow onset;
  - the horn-tap brace: bull charge/graze footage (Wikimedia) or the `kaiju-no-8` / `creature` tag cuts that show a head-down charge.
- **Glacier Yeti:**
  - Muybridge Plate 747 (baboon on all fours), ANIM_REFERENCES_1014 #4 (Dragon Walk Cycle);
  - the `kaiju-no-8` tag (e.g. Sakugabooru #257646, Yuya Takahashi, heavy creature acting) for the roar weight.
- **Permafrost Titan:**
  - Muybridge Plates 27 / 356 (the heavy walk, carrying weight; Plate 27 is in the site's curated locomotion set);
  - the `kaiju-no-8` cuts (#257646, #254909) for the heavy roar / rise.
- **Coral Crusher:** no site tag. Wikimedia crab-walk + fiddler-crab-wave footage (cite the tags tried).
- **Cinder Overlord:** no site tag. Wikimedia snake / cobra footage; `/tags/dragon` and the serpent dragons in `/tags/creature` for the crown flare / roar if one fits.
- **Blizzard Roc, Frostcrown Dragon, Eclipse Seraph (flyers):**
  - `/tags/how-to-train-your-dragon` (10 film clips: "Flying With The Dragon Rider (HTTYD2)", "Hiccup & Toothless Fly Together") for the wingbeat, takeoff, landing and dragon roar;
  - `/tags/flying` for the bird wingbeat;
  - ANIM_REFERENCES_1014 #8 (banshee flight: ~0.85 s stroke, the tail streams) and the Bird Flight flapping diagram.
  - 3 site opens are left today: Builder D should spend them on 1-2 HTTYD clips.
