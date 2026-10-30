# UI appeal review: OLD Check-UI, window by window and HUD (2026-10-22)

Reviewer: read-only UI reviewer. Only this file was written. Roblox Studio was not opened.

**Owner decision (2026-10-22):** "okay just return the old ui." The HATCH NIGHT look is dropped. This review covers
the OLD bright Check-UI look only. Target: make it better for kids WITHOUT changing its identity.

**Identity to keep (do not change):** solid slate canvas `#3B5866`, loud gradient headers with the checkerboard
and divider, glossy bevelled buttons, colourful cards, big outlined GothamBlack titles, the red [X], and the
big header icon.

**Evidence limits:**
- Colours are the Check-UI palette from the skill spec (`check-ui-clean-roblox/SKILL.md` section 2 and
  `DESIGN_SYSTEM.md`), not pixel-sampled.
- Pixel sizes come from the 1519 x 753 captures. Phone sizes assume the phone frame is 844 wide, scaled 1.8x.
  The builder must re-measure with `AbsoluteSize` on the emulator.
- Contrast ratios are my WCAG 2.x calculations.
- Process note: the brief asked for research first. I did a first pass over the screenshots before the searches.

---

## 0. Top items for the owner (read first)

1. **Clipped and outside-the-box faults on the old windows:** the Shop's VIP and x2 SPEED copy is cut off, the Shop's
   side tabs hang outside the panel, and the big header icons and SECRET ribbons poke past their boxes.
2. **Too-small text on phones and in cards:** body copy is 9-11 px in the captures (floor is 16 px base).
3. **White text on lime and cyan fails contrast** (about 1.2:1 and 1.9:1). Use ink labels there.
4. **Welcome Back puts the paid "CLAIM x5 (39 R$)" rainbow above the free CLAIM.** That is a pressure pattern for
   kids. The free claim must be the loudest.
5. **Starter Pack HUD and popup:** the timer sits on the egg art, the red last-hour escalation must go, and the
   countdown must be verified as set once per player (Roblox rule).

Counts: **MUST 10, SHOULD 12, NICE 5.**

---

## 1. Research (Part 1)

### 1.1 Roblox's own rules (official pages, fetched)

| Topic | Rule (as fetched) | Source |
|---|---|---|
| Paid random items: odds | Show the numerical odds of every outcome before purchase. Percentages total 100%. A labelled info pop-up is allowed; a bare (i) icon is not. | https://create.roblox.com/docs/production/monetization/paid-random-items |
| Paid random items: eligibility | Check `PolicyService:GetPolicyInfoForPlayerAsync()`. If `ArePaidRandomItemsRestricted` is true, that player cannot use the paid random generator. | same page |
| Countdowns | "Don't use a countdown timer that isn't accurate or automatically restarts for the same item." A "24 hours" deal that reappears at every login is a false sense of urgency. | https://create.roblox.com/docs/production/monetization |
| Urgency with minors | "Avoid using pushy or urgent messages when interacting with minors." Replace "LAST CHANCE, ACT NOW" with "See Price". | same page |
| Limited time | Limited-time content is allowed. The timer must be true. | same page |

### 1.2 Roblox developer forum (community view, not policy)

- Rewarding individual likes is commonly seen as probably against Roblox's giveaway and promotion rules. The API
  cannot read likes. Group-join rewards look acceptable to most posters. Sources:
  https://devforum.roblox.com/t/is-rewarding-players-for-liking-favoriting-a-game-allowed/2926286 and
  https://devforum.roblox.com/t/clarifying-requirements-for-paid-random-items/4654622 (odds announcement).
- Owner should confirm the like step with Roblox before publishing (M8).

### 1.3 Accessibility and phone

- **Text contrast:** WCAG 2.2 SC 1.4.3 needs 4.5:1 for normal text and 3:1 for large text. SC 1.4.11 needs 3:1 for
  UI controls. https://www.w3.org/TR/WCAG22/
- **Touch targets:** Roblox gives no number. Third-party guidance uses 44 x 44 px. Source:
  https://www.smashingmagazine.com/2023/04/accessible-tap-target-sizes-rage-taps-clicks/
- **Roblox phone advice:** test on physical phones; notches and Roblox overlays can cover controls. Sources:
  https://create.roblox.com/docs/performance-optimization/test-on-hardware and
  https://create.roblox.com/docs/production/publishing/adaptive-design

### 1.4 What top simulators look like (community and parental reviews)

- **Pet Simulator 99:** bright colours, cute animals, image-based buttons; the hook is rarity, not UI. One parental
  review puts the sweet spot at about ages 8-13. Sources: https://enjoy9game.com/blog/games/roblox--pet-simulator-99
  and https://screenwiseapp.com/media/pet-simulator-99-game (I did not confirm which carried the age line).
- **Grow a Garden and Steal a Brainrot:** no design breakdown found. A PC Gamer quote calls Steal a Brainrot's
  events "sensory overload" (URL not captured), which supports keeping HUD clutter low.

### 1.5 Colour and children

- Young children prefer bright, saturated colour. Older children move toward softer tones. The closest age study
  (ages 3-15) is about room furniture, not interfaces; preference rises with brightness and older children prefer
  lower saturation. Source: https://pubmed.ncbi.nlm.nih.gov/40130501/
- Toy-colour eye-tracking (brightness vs saturation): no results in the snippet. Source:
  https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10771309/
- **Takeaway:** keep neon for headers, buttons and rewards; keep the slate canvas for the body. No study I found tests
  game UI for ages 9-14 directly. This is an inference.

### 1.6 Dark patterns to avoid

- Early childhood apps: periodic rewards that look like gambling; paywalls. Source:
  https://www.researchgate.net/publication/374502995_The_Dark_Side_of_Fun_Understanding_Dark_Patterns_and_Literacy_Needs_in_Early_Childhood_Mobile_Gaming
- Casual mobile games: pay-to-skip, forced grinding, play locked to set times. Source:
  https://www.researchgate.net/publication/365827727_Finding_Dark_Patterns_in_Casual_Mobile_Games_Using_Heuristic_Evaluation
- Countdowns exploit fear of missing out in children. Advocacy filing to the FTC, not peer-reviewed. Source:
  https://fairplayforkids.org/wp-content/uploads/2021/05/darkpatterns.pdf

---

## 2. Strict review of the OLD UI (Part 2)

Kid appeal (1-10) is my judgement from the before shots. The criteria are the owner's list: appeal, clarity, tap
size, text size, icons, colour hierarchy, juice, consistency, clutter, anything that overlaps text or pokes out.

| Window | Score | Shot file | What works | Defects (ranked) |
|---|:-:|---|---|---|
| Daily Rewards (Gift) | 7 | `hatch_gift_before.jpg` | Lime checker header, bright day cards, rainbow Day 7, lime CLAIM | Day copy ("+1 Hatch & Speed Potion", "+2.33M Speed", "Wood Egg 30K KG") is 9-11 px. The SECRET! ribbon pokes out of the Day 7 corner. Grey LOCKED buttons read weakly. |
| Free Gift | 7 | `compare_freegift_build.jpg` (left) | Blue checker header, big "3 POTIONS!", bright potion art | "~ ONE-TIME GIFT! ~" and "x2 MONEY / HATCH / SPEED" are tiny. Step 1 says "Like the game!" as a requirement, but the claim checks only the group (M8). White CLAIM on lime (1.2:1). |
| Upgrades | 6 | `compare_upgrades_build.jpg` (left) | Bright rocket, bolt and heart icons; checker header | Header icon overlaps the top-left corner and sticks above the header. "Range 370 > 447 studs" and "Survive 0 hits" are about 9 px. Locked REBIRTH buttons are grey with low contrast. |
| Welcome Back | 7 | `compare_welcome_build.jpg` (left) | Gold header, big "$547K" | The "39" Robux chip sits outside the top-left corner of CLAIM x5. The rainbow CLAIM x5 is the loudest button, above the free CLAIM (pressure, M9). |
| Shop | 8 | `shop_before_after.jpg` (left), `popup_shop/shop_before.jpg` | Magenta checker header, a different bright colour per pass card, icon tabs | The store icon pokes above the window top. VIP and x2 SPEED copy is cut off at the card bottom. The side tab rail hangs outside the right edge. Not big on PC (about 60% of width). |
| Starter Pack popup | 7 | `popup_before_after.jpg` (left) | Magenta header, five-outcome egg odds summing to 100% (keep this) | "NO THANKS" is small and grey. White BUY on lime (contrast). The last-hour timer goes red in the current build (`popup_urgent.jpg`); check the legacy code for the same rule. |
| Creature Index | 8 | `index_before_after.jpg` (left) | Blue checker header, area-coloured tab rail, bright cards | The book icon pokes above the header. "DISCOVERED 13 / 30" text sits on the moving fill. The SECRET tag pokes past the card corner on the "?" cards. The "!" and star badges crowd the tab corners. |
| Rebirth | 8 | `rebirth_before_after.jpg` (left) | Purple checker header, orange, pink, green and blue reward chips | The coin icon pokes above the header. "+1 PET SLOT 3 > 4" and the Money+Speed line are about 9-11 px. Disabled "REBIRTH!" sits on the checkerboard (text over pattern). The gold/purple SKIP is clear. |
| Settings | 6 | `settings_before_after.jpg` (left) | White-silver checker header, big "Settings", pink / lime / orange toggles | The "-" and "+" buttons are about 22 px (too small). Row subtitles are about 10 px, low contrast. The title sits on the checker (keep the stroke). |
| Playtime | 6 | `hatch_playtime_old_vs_restored.jpg` (left) | Lime checker header, silver CLAIMED, orange Venom Basilisk tile, red "LEAVING RESETS PROGRESS!" warning (keep: it is honest) | The gift icon pokes above the header. Tile values and timers are about 11 px. White "Skip All" label on lime (contrast). |
| HUD (every shot) | 7 | `hatch_pc_mid.jpg`, `fix_01_top.jpg`, `starter_hud_v2_live_magma_1519.jpg`, `starter_hud_v2_compact_emulated.jpg` | Chunky Check-UI tiles (Shop, Claim!, Rebirth, Index, ADMIN), pink speed bar and green cash bar, right tiles | Left and right tiles are about 69-70 px in the phone capture (about 38-39 pt if the frame is 844 wide). Starter timer "23:59:37" sits on the egg art. The lime "49" sits on the green potion. The egg is clipped at the right screen edge on phone. Hotbar labels ("10K KG") are tiny. |

**Average kid appeal (windows):** 7.0 out of 10. The HUD is 7.

---

## 3. Builder instructions (Part 3)

**Rules for every item:** GothamBlack with a black UIStroke; device scale from the 1050 x 620 base, clamped 0.52..1.18;
ScaleType Fit; centre-anchored UIScale; text fills at most 83% of its box; nothing over text; corners inside their
box; nothing runs per frame while a window is closed.

**Base size is 1050 x 620 px.** Keep each window's current base size, except the Shop (M10).

### 3.1 Palette (Check-UI; use these RGB values)

- Canvas: `59, 88, 102` (`#3B5866`), UICorner 4, outer UIStroke 3.5 px `24, 30, 34` (`#181E22`), Border mode. Opaque.
- Recess / card: `26, 44, 52` (`#1A2C34`). Card highlight `75, 125, 145`, 1.2 px, transparency 0.4.
- Headers (top -> bottom; highlight; checker; divider):

| Page | Top | Bottom | Highlight | Checker | Divider |
|---|---|---|---|---|---|
| Shop, Starter Pack popup | 255, 20, 150 | 225, 0, 25 | 255, 200, 225 | 150, 0, 20 | 125, 0, 18 |
| Index, Free Gift, Upgrades | 0, 205, 255 | 0, 130, 245 | 180, 240, 255 | 0, 75, 150 | 0, 50, 110 |
| Rebirth | 160, 0, 255 | 96, 0, 200 | 224, 160, 255 | 96, 0, 144 | 80, 0, 120 |
| Settings | 255, 255, 255 | 215, 222, 232 | 255, 255, 255 | 110, 120, 135 | 90, 100, 112 |
| Daily Rewards, Playtime | 152, 255, 0 | 80, 208, 0 | 224, 255, 176 | 53, 128, 0 | 37, 96, 0 |
| Welcome Back | 255, 208, 0 | 255, 140, 0 | 255, 240, 160 | 176, 96, 0 | 153, 76, 0 |

  Welcome Back's row is approximate from the shot. Confirm its theme constant in the legacy OfflineClient.

- Buttons (top -> bottom gradient; 3 px bottom bevel; highlight; checker overlay):

| State | Gradient | Bevel | Highlight | Overlay | Label |
|---|---|---|---|---|---|
| CLAIM / BUY (lime) | 180, 255, 25 -> 105, 225, 0 | 15, 120, 15 | 235, 255, 130 | 40, 160, 20 at 30% | ink `17, 23, 26` |
| CLAIMED / OFF (silver) | 216, 222, 228 -> 148, 160, 176 | 72, 82, 96 | 255, 255, 255 | 96, 104, 112 at 35% | ink |
| LOCKED (red) | 255, 32, 80 -> 208, 0, 32 | 112, 0, 16 | 255, 176, 200 | 144, 0, 24 at 35% | white, 3 px stroke |
| SKIP / Robux buy (gold) | 255, 208, 0 -> 255, 140, 0 | 153, 76, 0 | 255, 240, 160 | 176, 96, 0 at 35% | ink |
| Music / toggle (pink) | 255, 20, 128 -> 212, 0, 85 | 120, 10, 45 | 255, 176, 208 | 160, 0, 64 at 35% | white, 3 px stroke |

- Close [X]: 38 x 38, base `115, 0, 16`, face `255, 125, 175 -> 255, 20, 40`, highlight `255, 210, 235`, separator `70, 0, 10`.
- Day cards: Purple `176,32,255 -> 112,0,224`; Cyan `0,210,255 -> 0,120,255`; Lime `180,255,25 -> 105,225,0`;
  Magenta `208,0,224 -> 128,0,160`; Amber `255,170,0 -> 224,96,0`.
- Day 7 rainbow: 0.00 `255,30,80`; 0.18 `255,140,0`; 0.35 `255,230,0`; 0.52 `40,230,50`; 0.70 `0,210,255`;
  0.85 `90,60,255`; 1.00 `220,0,230`.
- Checker overlay: `rbxassetid://385956923`, black, tile 19 x 19, transparency 0.85-0.9 on headers only.

**Label colour (my WCAG calculation):**
- White on lime `180,255,25`: 1.2:1. Ink `17,23,26` on it: about 14.9:1.
- White on lime header `152,255,0`: 1.3:1. Ink title.
- White on cyan `0,205,255`: 1.9:1. Ink title.
- White on magenta `255,20,150`: 3.6:1. White with 3 px stroke is fine for large text.
- White on purple `160,0,255`: 5.3:1. White. White on blue `0,130,245`: 3.8:1. White.
- Rule: titles need 3:1 or better; body and labels need 4.5:1. Otherwise use ink.

### 3.2 MUST (10)

**M1. Nothing pokes outside its box.** Applies to every window.
- Header icons (Gift, Free Gift, Upgrades, Welcome, Shop, Index, Rebirth, Playtime): keep the big icon, but its
  box must sit at least 8 px inside the window canvas on all sides. It may overlap the header's bottom edge by up to 16 px.
  It must not rise above the window top or past the left edge.
- Badges, ribbons and tags (SECRET! on Gift Day 7; SECRET tag on Index; star and "!" on Index tabs): fully inside
  their card or tab, inset 6 px. A rotated ribbon may be at most 8 degrees, and its rotated bounds must stay inside.
- Welcome Back "39" Robux chip: inside the CLAIM x5 button, 8 px from its edge.

**M2. No clipped copy.** Shop VIP and x2 SPEED descriptions are cut at the card bottom. Fit the copy to the card at
16 px base with the 83% rule, or grow the card by the shortfall. Test: every TextLabel has `TextFits == true`.

**M3. Shop side tabs stay inside the panel.** The Featured, Speed, Potions, Treadmill and Eggs rail moves inside the
canvas with an 8 px gutter. Widen the canvas by the rail width (M10).

**M4. No text over a moving fill or over the checkerboard.**
- Index "DISCOVERED 13 / 30": the label sits beside the trough (right or below it, 8 px clear), not on the fill.
- Rebirth disabled "REBIRTH!": a solid silver button (CLAIMED style) with an ink label. No checker behind any label.
- Settings title on the checker is allowed only with a 3 px ink stroke. Test: no label's parent is a checker frame
  at a label's position.

**M5. Text floor 16 px base.** Day copy, Free Gift subtitles, the "x2" line, Upgrades "Range" and "Survive" lines,
Rebirth reward tiles, Settings subtitles, Playtime values and timers, Shop and phone copy.
- Body and labels 16 px base. Buttons 18-20 px. Values 20-22 px. Titles 26-29 px. Stroke 2.5-3 px.
- Check with `TextBounds` at 1050 x 620 and at the phone emulator scale. Never shrink below 16 base.
- Phone windows fit the safe area and keep a window scale floor of 0.7 (about 11 pt text).

**M6. Label contrast.** Ink `17,23,26` labels on lime, silver, gold and cyan (CLAIM, BUY, Skip All, Claim All, the
Daily and Free Gift cyan titles). White with a 3 px black stroke on magenta, purple and blue. This keeps the outlined look.

**M7. Phone tap size at least 44 pt.** Applies to the HUD tiles (Shop, Claim!, Rebirth, Index, Eggs, Pets, Potions),
window buttons, tabs and [X]. Settings "-" and "+" go from about 22 px to at least 44 pt. Convert with the device
scale (base = 44 pt / scale). Measure with `AbsoluteSize` on the emulator and log the numbers.

**M8. Free Gift like step: no required step the claim does not check.**
- Step 1 "Like the game!" is shown as required, but the claim checks only group membership.
- Owner decides: (a) remove the like card and keep "Join the group", or (b) show like as an optional hint with no tick.
- Roblox policy: rewarding likes is a community-believed risk (section 1.2). Owner confirms with Roblox before publishing.

**M9. Welcome Back: the free claim is the loudest button.** The rainbow CLAIM x5 (39 R$) outshines CLAIM. Make the
free CLAIM the largest, lime, primary button. CLAIM x5 becomes gold, same height, secondary, with the price in its
label. No rainbow on the paid button.

**M10. Shop: the biggest window on PC.** Base size 760 x 500 (was 600 x 415). That is about 920 x 590 px at 1080p
(about 48% of screen width). Keep MenuController's fit rule and the 1.18 clamp. The Starter Pack card stays at the top.

**Starter Pack timer and HUD (part of M7 and M1, listed here because the owner watches it):**
- Verify `StarterEndsAt` is set once per player and is not reset on rejoin, reopen or respawn. If it resets, stop and
  tell the owner (Roblox countdown rule).
- No red last-hour escalation: keep "ENDS IN" gold. Check the legacy code for any red rule and remove it.
- "OFFER ENDED" hides the timer while the refusal shows.
- HUD timer "23:59:37" moves below the egg art with a 6 px clear gap, stroke only, no background.
- HUD "49" price: gold `255,208,0 -> 255,140,0` with ink label, so it does not sit lime on the green potion.
- HUD block inset 8 px from the right safe edge on phone (the egg is clipped now).

### 3.3 SHOULD (12)

**S1. Claim juice (keep the Check-UI style).** On claim: button flash white 0.08 s; icon pops 1 -> 1.25 -> 1 (Back,
0.35 s) inside its clipped face; check stamp slams 1.8 -> 1.0 while rotating -20 -> -8 degrees (Back, 0.22 s);
card dims to CLAIMED over 0.3 s; 8-10 coloured star pieces burst from the icon, fade over 0.6 s and stay inside the
window canvas; the reward sound plays.

**S2. Count-up numbers.** Reward values count up over 0.6 s (Quad Out) and then settle with a 1.08 pop (0.2 s).

**S3. Clear button states.** CLAIM lime breathes 1.00 -> 1.05 (sine, 1.2 s). Locked: 0.45 dim with a lock glyph.
Claimed: silver with a check. Refusal: red for 1.3 s, then back.

**S4. Press and hover timings.** Hover: scale 1.04 (Quad Out, 0.08 s), centre-anchored. Press: scale 0.95 (0.05 s).
Release: Back, 0.18 s. Nothing runs while the window is closed.

**S5. Tabs.** Segmented pill, lime active (Check-UI lime), at least 148 x 38 base. The "!" dot sits inside the tab.

**S6. Index tab rail.** Area colours on the tabs (Grass lime, Water blue, Thunder amber, Fire orange, Shadow purple,
Celestial gold). Badges inside the tab corners (M1).

**S7. Headers and titles.** Titles 26-29 px with a 3 px ink stroke and the 2-tier divider. Keep each page's header
colour from 3.1.

**S8. Settings toggles.** Keep pink (Music), lime (Sounds) and orange (Time). Rows recessed `26,44,52` with the card highlight.

**S9. Playtime tile states.** CLAIM lime with ink label; CLAIMED silver; locked grey with a small lock; the special
tile (Venom Basilisk) orange. Timers sit on the tile, never in a bar.

**S10. Gift day cards.** Each day uses its area card gradient (3.1). Day 7 keeps the rainbow. Chips (x1, x2) sit 4 px
off the check icon, not touching it.

**S11. Starter popup "NO THANKS".** Silver button at least 40% of the BUY width. BUY stays gold with the Robux glyph.
The odds block stays as is (it is compliant).

**S12. Rebirth SKIP.** Keep the gold SKIP with its price, but show the requirement progress and the REBIRTH button
first when requirements are unmet, so the free path reads first.

### 3.4 NICE (5)

**N1.** Seasonal Halloween header option: the pumpkin band `255,180,60 -> 242,98,10` with a bat sticker, off-season
back to the page colour.
**N2.** Settings title outline 2 px heavier, to match the OLD title weight.
**N3.** Day 7 rainbow shine sweep every 3 s, and rays turning 12 degrees per second only while the window is open.
**N4.** HUD Friends pill text up to 16 px base.
**N5.** Hotbar item labels ("10K KG") to 16 px base, or dropped if they do not fit.

### 3.5 Test steps

1. Render every old window at 1050 x 620, 1920 x 1080 and the 844 x 390 phone emulator; compare with the before shots.
2. Run the containment harness and add: no child outside its parent (M1), no clipped text (M2), label contrast
   (M6), text floor (M5), tap size (M7).
3. Timer test: no background frame behind any timer label.
4. Starter test: `StarterEndsAt` unchanged after rejoin or Shop reopen (StarterDebug). OFFER ENDED hides the timer.
5. Free Gift test: claim works with the owner's chosen step rule (M8).
6. Set `TestFreshSave` to true before any Play test (memory rule).
7. Owner reviews before/after sheets before publish.

### 3.6 Owner decisions (not for the builder)

1. Free Gift like step: remove, make optional, or keep after the Roblox check (M8).
2. Starter countdown: confirm the per-player 24 h start (Starter section).
3. Welcome Back rainbow: keep it on the paid button? Recommended: no (M9).
4. Shop size: 760 x 500 base, or bigger (M10).

---

## Summary counts

- **MUST:** 10 (M1-M10, including the Starter timer and HUD items)
- **SHOULD:** 12 (S1-S12)
- **NICE:** 5 (N1-N5)
