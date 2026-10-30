# Frostfang Lynx - animation references (owner rule), 2026-10-27

animationreference.org had 6/25 clip opens left today, and its tags have no cat, crouch or claw entries. So I studied the
**source clips on Sakugabooru** (the free source host). For each one I built a canvas contact sheet of the post's mp4 in
the browser and stepped through it at 0.125-0.2 s. Clips are 24 fps; ours are 30 fps (frames = s x 30). Study only.

**Clip review 3 follow-up, 2026-10-27: a site clip is added (L0).** I searched the site's tag index for cat, lynx,
crouch, claw and stalk (see the Wraith ANIM_REFS for the full list). `/tags/the-cat-returns` gave the clip below. It
was opened in the site player (the counter went 4 → 3), and its frames were stepped on the same source file.

| # | Clip | Used for | Key poses and timing |
|---|---|---|---|
| **L0** | **animationreference.org, `/tags/the-cat-returns`: "Animals: Character Acting & Creature Animation (BD - Crowd)"** (Shinji Otsuka; source Sakugabooru #256671, tags walk_cycle, running) | **walk**, act crouch | **16.92-17.5 s:** a side-view cat walk. The head and back stay level while the legs cycle (a steady head), the tail is carried up, and the cycle is ~0.8-1.0 s (24-30 f). **16.5-16.83 s:** the cat comes out of a low crouch-walk with the front end low. |
| L1 | **Pinocchio** (1940), Figaro at the window, Sakugabooru #132474 (Eric Larson), 1.8-4.8 s | idle look-around | After a yawn he looks around. Each **head turn takes ~0.6 s (18 f)** and is followed by a **0.3-0.4 s hold** (10-12 f). The head leads and the body stays still. Small ear changes follow the head by ~3-4 f. |
| L2 | **Pinocchio**, Figaro chasing the ball, #132272, 0.5-1.4 s | act beat 1 (crouch stare) | He drops from standing to a **flat crouch in ~0.25 s (8 f)**: the front goes down first, the paws stay forward, the head is locked on the target, the ears forward. He **holds the stare ~0.6 s**. The rump stays slightly higher than the shoulders. |
| L3 | **Pinocchio**, Figaro at the fishbowl, #132391 (Eric Larson), 0.0-0.9 s | act_clawflex (the claw flex) | Crouched and staring at the bowl, he raises one forepaw a little and the **toes spread over ~0.4 s (12 f)**. A short hold, then the paw sets down. The other paw stays planted, and the head never leaves the target. |
| L4 | `_review/ANIM_REFERENCES_1014.md` #6, **Monsters University** (crouch, then explode into the spread pose in 5-7 f, hold) | roar "ruff-flare threat" | The threat display: compress first, then the flare happens fast (6-8 f) and is held. |
| L5 | Sakugabooru #143881, **Pluto and the Gopher**, 50.0-52.75 s (also in the badger refs) | roar (shoulders drop) | The shoulders sink first and the head pushes forward low; the rise is slower than the drop. |

## Mapping
- **idle (120 f loop)** (L1):
  - The head turns to +14 deg over f8-26 (18 f), holds to f40, turns to -8 over f44-60, holds, and is back to 0 by
    f80. The neck takes at most 6 deg of the yaw and the head the rest (review: neck yaw 8 deg or less).
  - The ears follow 4 f late and twitch 3 deg at f70; the tail tip flicks 10 deg at f90.
- **walk (30 f loop, r6; was 24 f)** (L0: a ~24-30 f cycle with a steady head): a lateral-sequence cat walk (BL / FL / BR / FR, duty 0.56) with soft feet (zero-speed lift-off and touchdown, lift 0.030; the front paws curl under in the swing and reach flat for the touchdown).
  - Springy body: two small dips per cycle, lowest at the front touchdowns. The head nods 1 f after each front contact.
  - The bobtail is lifted and swings against the hips (12 deg yaw + 6 deg roll).
- **roar (60 f)** (L4 + L5):
  - f0-14: shoulders drop and the ruffs and tufts flare out 20 deg (the flare is fast, 6-8 f, then held).
  - f20-45: the head drops 8 deg and pushes forward twice (pulses at f26 and f38).
  - f25-50: the jaw opens to the frost fangs, peaking at f30 (event `hiss` f30).
  - f50-60: settle.
- **act_clawflex (96 f)** (L2 + L3):
  - f0-20: crouch stare. The body lowers 0.05H in ~8-10 f (L2) with the front lower than the rump. The head turns
    14 deg toward the viewer and holds to f40; the tufts flatten 8 deg.
  - f20-40: the tufts rise 12 deg and hold.
  - f40-72: the forepaws flex one after the other: the left claws open f40-48 (`claw1` f48), the right claws f52-60
    (`claw2` f60), a **12 f lag** so the sparks land on the plan's event frames. Each paw's claw-fan parent opens 35 deg
    (claws up and out, over ~8 f; L3: 12 f at 24 fps); the four claws fan from it - centre two +6 deg more (41 total),
    outer two 8 deg less (27 total), yaw +-6 / +-18 deg - and knead 4 deg while open. The flexing paw rolls its toes up
    12 deg on the heel. The paws stay on the ground.
  - f72-84: claws retracted; the tail tip flicks 10 deg once.
  - f84-96: exact rest. The hind feet are planted in every frame.
