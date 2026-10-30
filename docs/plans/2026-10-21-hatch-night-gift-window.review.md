# Review: HATCH NIGHT Gift window plan (2026-10-21)

Plan: `docs/plans/2026-10-21-hatch-night-gift-window.md`. Reviewer: plan reviewer (read-only).

**Inputs I read:**
- the plan, all 1234 lines;
- spec `docs/specs/2026-10-21-slingshot-ui-style.md`;
- `dirB_hatchnight.html`, `common.js`, and the three B mockup PNGs;
- the owner's evidence PNG;
- the Check-UI skill;
- the memory notes on layout rules and the login streak.

**Code I read in Studio:** MenuController, BrickUI, StreakClient, PlaytimeClient, PotionHud, ShopClient (side tabs), StarterPackClient, StreakConfig, PlaytimeConfig, CreatureConfig and StreakTests.

**Studio access:** another agent kept Studio in Play for most of the review. I ran `execute_luau` only in Edit, only to read values, during two short Edit windows. I wrote nothing and never touched Play.

## Verdict: **APPROVE WITH CHANGES**

The plan is unusually precise, and most of its numbers check out (details below). It fixes all six root causes behind the owner's complaint. Five changes are required before building:
- One real overlap at rest that the planned test cannot see.
- One overlap on hover.
- One anchor bug.
- One gap in the hero card's state table.
- One factual error about StreakTests.

---

## Verified (no change needed)

| Claim in the plan | Result |
|---|---|
| Window / Face / Body AnchorPoint (0.5, 0.5) | yes: Window (0.5,0.5) at (0.5,0.5); Face (1, 0.9773) at (0.5, 0.4886); Body (0.9226, 0.7116) at (0.5, 0.5977). So 8.2 check 5's 0.9226 is right. |
| `Window.BaseSize` has no Offset, so the new `mul()` changes nothing for Check-UI pages | yes: BaseSize = {0.3229,0},{0.4074,0} |
| Window children's ZIndex | Depth 1, Face 1, so HatchFront Z2 is strictly above Face. The UIAspectRatioConstraint is DominantAxis Height; harmless because the Offset size has the exact ratio. |
| Face holds nothing else that would show over the night shell | yes. In Edit it has UICorner, UIStroke, Studs, Gloss, Icon, Title, Close and Body. At runtime `restyle` destroys Studs and Gloss, `B.header` adds Header, and Close becomes CloseOld (hidden) plus the new Close. |
| Body has no constraint that would block Size (1,1) | yes: UICorner, UIStroke, Studs (destroyed at runtime) and Message only. ClipsDescendants is false. |
| HUD edge formulas (section 3) | yes. Menu: AnchorPoint (0, 0.5), X 0.0094, Size (0.1292, 0.2426), AR 0.9466; the 1.3 phone UIScale grows to the right. Holder: AnchorPoint (0, 1), X 0.0094, Size (0.2135, 0.2093), AR 1.814. |
| Fit rows of section 3 | Re-derived by hand: 1.18 / 873.2x554.6 / cx 960; 1.0982 / cx 635.65; 0.7106 / cx 407.24; 0.6787 / cx 389.03. All exact. At 1050x620 the spec formula alone gives s 1.170 with the window's left edge at x 92, which would cover the tiles (139) and the pills (223), so D5 is needed. |
| HUD draw order | MainMenu DO 3, SpeedUI DO 0, AreaTitle DO 0. The PotionHud timer row (`Holder.Potions`, X 1.03..1.98 of the Holder, outside its box) draws under the window. On phones about 2 px of the first potion icon peeks out at the window's left edge; at 1050x620 it is fully hidden. Acceptable. |
| `UIStroke.BorderStrokePosition` exists | yes (default Outer). `AbsoluteRotation` exists. A new ScreenGui defaults to CoreUISafeInsets and IgnoreGuiInset false, so StreakFly matches MainMenu. |
| `workspace.HalloweenDecor` | a Folder |
| Glow 121438949090215 is a soft disc, and Rays 76624006953375 fade radially | yes. RebirthClient_v2 names `make_rays2.py` as the source. glow2 is solid to 50 % of the radius, then `(1-smoothstep)^1.6`. rays2 fades out by r = 1.0 (the inscribed circle), so `HatchRadial` (checking the unrotated box) is valid. |
| Longest secret pet name | THORNBLADE MANTIS (Cosmic Leviathan @16 = 150 px). Fits the 214 px box. |
| Skip product | `PlaytimeSkipProduct` = 3716713236 (set), Studio price 48, so "SOON" never shows live |
| `PlaytimeConfig.PET_KG` | 1000 ("1K KG") |

**Extra GothamBlack widths I measured** (TextService; all fit, so add them to the section 0 table):

| Text @ size | px | Box (room after stroke) |
|---|---|---|
| x5 / x2 / x1 @16 | 18 / 17 / 15 | 26 (21) |
| IN 6 DAYS @18 | 84 | 168 (163) |
| 23:59:59 @17 | 64 | 94 (89) |
| 1:59:59 @16 | 50 | 97 (92) |
| TOMORROW! @18 | 112 | 142 (137) |
| EGGS FULL! @18 | 96 | 142 (137) |
| PETS FULL! @16 (slot) | 83 | 97 (92) |
| 90 MIN @16 | 52 | 80 (76) |
| LOST! @16 | 42 | 76 (72) |
| $7.25Qa @20 | 73 | 105 (100) |
| +$7.25Qa SPEED @28 (fly) | 208 | 400 |
| celebration Name @22 | 325 | 600 |
| LEAVING RESETS PROGRESS! @16 | 214 | (owner's call below) |

---

## MUST changes

### 1. Draw the CLAIM rings UNDER the card content

**What's wrong today.** As planned, they overlap the CLAIM button even at rest, and the containment test can't see it.

- **Small cards.** `Badges.Ring` (3,3,152,155) plus its 3 px stroke is a band at y 158..161; RingGlow is a band at y 155..158.
  - The CLAIM button's depth slab plus its 2.5 outline reaches y 159.5, and x 5.5..152.5.
  - Badges (Z7) draws after Face (Z3), so the lime ring cuts across the bottom of the CLAIM button: 1.5 px into the ring, 3 px into the glow.
  - At pulse 1.05 it is 2.3 px into the ring, and the ends cross the side bands.
  - The lime DayPill's outline (y 4..28) also crosses the RingGlow band (3..6).
- **Slots.** Same numbers: Ring (3,3,107,155) against the button's bottom at 159.5.
- **Hero.** `Ring` (7,7,208,321) is a band at y 328..331 and x 4..7 / 215..218.
  - The hero button's outline reaches y 331.5: a 3 px overlap at rest, touching the PrismRim band (331..335).
  - The Tag's outline (y 5..31) overlaps the ring by 2 px; the DayPill's (y 6..30) by 1 px.

**Required layout.**
- Small cards and slots: `Ring` and `RingGlow` become children of `Card.Face` at ZIndex 1, created after `Glow`.
- Hero: put `Ring` in `Card7.Face` at ZIndex 3, created after `Halo`. Or drop the hero ring; the mockup has none on the hero. That choice is the owner's (owner's call 5).
- `Badges` keeps only Check and Lock.
- Face ClipsDescendants is fine: the ring's outer box is exactly the face (0..158 x 0..161, outer corner 11 + 3 = 14 = the face corner).

**Required test.** Add 8.3 check 6 ("draw order"). For every card and slot, `Ring` and `RingGlow` must be descendants of that card's `Face`, with ZIndex lower than DayPill, Tag, the chips and Button.

### 2. No hover scale on the tab Pill or the SKIP ALL button, and add a hover-peak pass

Both sit 3 px inside a 38-tall recess.

- **The Pill.** At rest the left cap fits by 0.38 px: cap centre (17.5, 17.5), radius 14.5 + 2 = 16.5, against the recess cap at (19, 19), r 19.
  - At hover 1.04 the cap moves to (15.12, 17.44) with an outer radius of 17.16. That is 4.18 + 17.16 = 21.3 > 19.
  - So it pokes 2.3 px through the track's outline.
- **SKIP ALL.** At 1.04 it pokes 3.5 px out of the PlayBar's right end.
- **The limit.** By spec 2.1.4, a button with pad p, outline o and width w may scale to at most `1 + 2(p - o)/w`. For the Pill that is about 1.006.

**Rule.**
- `glossButton` gets `opts.hoverScale` (default 1.04). The Pill and SkipAll pass `hoverScale = 1`.
- Their hover feedback becomes the face's Gloss transparency, 0.58 -> 0.45 (Quad Out, 0.08 s).
- Press (0.95) stays as planned.
- Every other button keeps 1.04: Close, cards, slots and hero all have enough margin.

**Test.**
- New Studio switch: GiftPage attribute `HatchTestHover = true` makes every glossButton rest at its hover scale.
- Run 8.3 checks 1 and 3 with it in run A (native and 0.7106) and in run F.

### 3. `H.sticker` must be centre-anchored

**The conflict.** Section 4.0 says rotated stickers are centre-anchored. But the "write exactly" code builds them through `H.image`, so they get AnchorPoint (0,0).

**Why it matters.** The Check stamp's `Stamp` UIScale (1.8 -> 1, spec 2.5) would grow from the top-left corner instead of the centre. That breaks the Check-UI centre-anchor rule.

**Fix.**
- The image gets AnchorPoint (0.5, 0.5) at `Position = (x + size/2, y + size/2)`.
- The shadow gets the same AnchorPoint at `(x + size/2, y + size/2 + 3)`.
- The tables keep their top-left (x, y, size) inputs; the helper converts them.
- Rotation is centre-based either way, so the "rotated box" numbers in 4.5 don't change.

### 4. Complete the Day 7 hero state table (4.7 / 5.1)

**Missing values.** The plan gives the hero's button for each state, but not its Dim, icon tint or badges for TOMORROW and week-done.

**Use these values:**

| Hero state | Dim (brightness) | Pet / chip tint | Badges | Motion |
|---|---|---|---|---|
| CLAIM | 1.0 | 255 | Ring (per MUST 1) | pulse, rays, prism, shine |
| TOMORROW (`through == 6`, not claimable) | 0.95 | 255 | none | rays, prism, shine |
| week done (`through >= 7`, not claimable) | 0.6 | 153 | Check (82, 100, 58), -8 deg | rays, prism, shine keep running |
| LOCKED | 0.95 | 255 | none (no Lock sticker) | rays, prism, shine |

**Remove the impossible row.** Delete the "CLAIMED (week not done)" row. `StreakConfig.view` returns `claimedThrough = nxt - 1 = 0` as soon as a new week is claimable, so `through >= 7` always means not claimable.

### 5. StreakTests has no `CLIENT_SRC`

I checked in Edit: no `CLIENT_SRC` in 9015 chars. The plan says "only CLIENT_SRC changes", and its own ledger rule would make the builder stop on this conflict.

Reword sections 1 and 7/9 as: "add `T.CLIENT_SRC` = the text of `streak_client.lua` v2 (a long string); `T.fresh`, `T.pure` and `T.live` stay byte-identical."

---

## SHOULD changes

### Robustness

1. **Guard against a failed Hatch module.**
   - If `B.Hatch` fails, PlaytimeClient errors before its RenderStepped loop. That kills the Gift tile's "Claim!" label and badge, not only the page.
   - StreakClient also hangs on `WaitForChild("GiftPage")`, so the auto-open never runs.
   - Fix: in PlaytimeClient, `if not B.Hatch then warn(...)`, skip the page and keep the tile loop. In StreakClient, use `WaitForChild("GiftPage", 30)` and return with a warning on nil.
   - Also correct risk 14, which says only the page fails.
2. **Restore the saved Visible flags.** `applySkin` should restore the Visible values it saved (header, closeHolder, Icon, Title, Depth), not `not on`. It is the same result today, but safe if a page ever hides one.
3. **Fly-text fallback.** If `SpeedUI` is disabled or `Holder.MoneyRow` / `Holder.SpeedRow` is missing, use "start minus (0, 120 s)".
4. **Slot claim failure.** Show the 5.1 flash mapping on that slot's `State` label for 1.5 s (for example "PETS FULL!" on the pet slot). Today the failure is silent.

### Layout and motion

5. **Bigger tap targets on phones.**
   - `CloseHit` = (684, 0, 56, 56): 39.8 pt at 0.71, still above the tabs' hits (y 62).
   - Add `SkipHit`, a TextButton (186, -4, 214, 46) in PlayBar, `HatchHit`, Activated -> skip. SKIP ALL's face is only 20.6 pt tall at 0.71. It doesn't overlap HitPlaytime: the canvas x ranges are 516..730 and 164..318.
6. **Clip the stamp slam.** Set `Badges.ClipsDescendants = true`. At 1.8 and -20 deg the Check's rotated box (about 133 px) pokes about 11 px above row-1 cards for roughly 0.1 s. Clipping works here because only the child is rotated.
7. **Centre the timer group.** In TOMORROW / dusk buttons, measure the text width `tw`.
   - Clock x = `(W - (18 + 6 + tw)) / 2`; the label goes at clock x + 24, left aligned (W = 142 for small cards, 202 for the hero).
   - As planned the group sits 7.5 px (small cards) and 8.5 px (hero) left of centre.
8. **Snap the Pill on open.** In `onShown`, set the Pill to its slot without the 0.15 s slide. Today it slides across while the window pops open.
9. **No overshoot on Hatch pages.** Open them with Quad Out 0.32 s instead of Back. The window now hugs the left HUD at 1050 px and below, and Back's roughly 10 % overshoot covers the pills for about 0.1 s.
10. **Softer glows.** glow2 is a flat plateau to half its radius, so ImageTransparency 0.45 gives a flat 55 % disc. The mockup has 53 % at the centre falling to 13 % at 60 % of the radius. Start the card and slot glows at 0.6; the visual review tunes it.
11. **Header teeth edges.** At 1.18, check the 74 rotated tooth squares in `hatch_pc_mid.png` (zoomed). If the edges look stair-stepped, try a 1 px UICorner on each Ink/Tooth frame and re-shoot.
12. **Centre-anchored hits.** Make the hit buttons (card `Hit`, `HitDaily`, `HitPlaytime`, `CloseHit`) AnchorPoint (0.5, 0.5) with converted positions. This satisfies the Check-UI checklist's "all interactive elements centre-anchored", even though hits never scale.

### Tests

13. **Add these checks to 8.3:**
   - **HUD clearance**, native scale, no HatchTestScale, runs A and F at 1920x1080:
     - window outer edge (AbsolutePosition minus 3.5 s) is at least `max(Menu right, Holder right) + 6 - TOL`;
     - top >= 6, bottom <= guiH - 6, right <= guiW - 8.
   - **Nothing over the window:** sample `PlayerGui:GetGuiObjectsAtPosition` every 24 logical px inside the stroked window box. The first visible GuiObject must belong to `MainMenu` (or StreakFly). Record the DisplayOrder of every enabled ScreenGui in the ledger.
     - Coordinates: MainMenu has IgnoreGuiInset false, so pass AbsolutePosition coordinates as they are, with no inset adjustment. Write this in the test so a top-bar offset can't cause a false fail.
   - **Hover-peak pass** (MUST 2) and **draw-order check** (MUST 1).
   - **Rounded corners:** for children within r of a rounded parent's corner (Lock, Close, the buttons, Tag), the stroked corner must stay inside the parent's corner arc. Today they pass by my numbers; for example the slot button at pulse is 13.3 inside a radius of 14. The check guards future edits.
   - **Tile boxes:** for holders with no stroke of their own, the "stroked box" is the union of their descendants' Border-stroked boxes.
14. **Add these cases to the run matrix:**
   - **G** `set p, 6, today`: Day 7 TOMORROW, hero dusk timer.
   - **H** `set p, 4, today-3`: LOST label plus pip shake (pips at x 102..328, clear of Count at 340). Run containment within the 4 s window.
   - **I** run D plus `failNext "pet"` plus TestPress 7: "PETS FULL!" on the hero. Also run C plus `failNext "egg"` on Day 4.
   - **J** PLAYTIME: all slots claimed (SkipAll hidden) and the skip error flash ("TRY AGAIN").
   - **K** run D at `HatchTestScale 0.6787`, so the hero pulse is also checked at the smallest scale.
15. **Rapid page switching** (8.6 extension):
   - (a) `OpenPage("Gift")`, wait 0.05 s, `OpenPage("Shop")`, wait 0.7 s, dump: must equal BEFORE.
   - (b) Shop, wait 0.05 s, Gift: HatchBack visible, `Face.Header` / `Face.Close` hidden, AR 740/470.
   - (c) Gift, `CloseWindow` at 0.1 s, then reopen Gift: window visible and fitted.
   - My reading is that all three are safe: a new Size tween cancels the old one in the same frame, and `fitScale` resets Position. The tests make it proven.
16. **8.2 check 1:** also assert that `Face.Close` and `Face.Icon` are hidden on Gift.
17. **Respawn check** (separate session): with Gift open, kill the character. `StreakFly` and `StreakCelebrate` must still exist and the window must work after respawn.

### Plan text

18. **Risk 7 is misstated.** ClipsDescendants is ignored only when the clipping frame or one of its ancestors is rotated; rotated children are clipped. The conclusion (rays rely on radial art) still stands.

---

## Checklist answers

### 1. Fidelity to the mockups

With MUSTs 1-3 the build would match `B_hatchnight_pc.png` and `B_hatchnight_phone.png`. I verified element by element:
- shell, band, gloss, teeth, sticker and title with its ink copy;
- tabs and dots;
- streak pips and links (positions match `streak()`);
- every card's icon positions, which match `buildCard()`'s formula after the stated "nudge up so bottom <= 89.5";
- the hero layers;
- the shell crack (teeth recomputed from `crackEdge(.., 18, 88, 17, .., 2, 12)`, exact).

**Missing or different:**
- The bats (D7, owner's call).
- The window is shifted right on phones; the mockup is centred (D5, needed).
- The Sheen sits at (0,46) as a disc instead of a glow coming from the top-left corner. It is nearly invisible behind the cards, so that is fine.
- The PLAYTIME tab has no mockup at all.

**Deviations, judged:**

| Deviation | Verdict |
|---|---|
| D8 header teeth spread evenly | Good. It matches the spec's text (16 px from both edges); the mockup loop's gap was an artefact. Extents 1.3..735.3, lowest point y 61.8. |
| D9 chips 74 + 120 | Justified. 98 + 98 gives a 6 px gap. Equal 97 + 97 leaves a 56 px value box, and `$7.25Qa` needs 59 + 5. |
| D12 PLAYTIME footer in row 2 | Good structure (row 2 = context bar on both tabs). The copy change is the owner's call. |
| D6 status line removed | Matches spec 2.4. Trade-off: "Streak lost" becomes "LOST!" once per session for 4 s ("STREAK LOST!" is 105 px and can't fit the 76 px label). |
| Fly-text instead of the toast | Matches spec 2.5.7, and is better: Day 2 goes to the speed pill, Days 4 and 5 float up. Needs the fallback in SHOULD 3. |

### 2. The owner's complaint

- **What the plan gets right.**
  - The containment test grows boxes by the Border stroke times the product of UIScales.
  - It uses AbsoluteRotation for rotated boxes and handles radial art separately.
  - It checks the pulse peak and text widths.
- **What it misses:**
  - The ring-over-button overlap (MUST 1). Its checks only compare parent-child pairs and the declared tile groups, so cousins (Badges vs Face.Button) are never compared.
  - The hover peak (MUST 2).
  - The stamp transient (SHOULD 6).
  - Rounded corners (SHOULD 13).
- **8 px padding:** cards 10 from the canvas edges, 8 apart, 11 at the bottom. Button bottoms are 4 px from the face by design (spec grid, `HatchPadBottom 3`).
- **Bevels inside:** each holder includes its own Side.

### 3. Other windows unchanged

**The hook is sound.**
- `saved` is captured after `restyle` and `header`; all restore targets exist; `mul` with offsets is a no-op for Scale-only BaseSize.
- The Hatch path returns before the title and header LAYOUT code, and the next Check-UI open re-sets it. `fitScale` resets `Position = basePos`.
- **WindowOpened listeners** (OfflineClient, UpgradeClient, SellClient, InventoryClient, PetsEggsUI, FreeGiftClient, TutorialClient, AdminClient) only close their own panels, and they fire before `applySkin`. None touch the window chrome.
- **Other scripts that touch the window:** ShopTabs (a Window child at Z5) is hidden outside the Shop. AdminBannerClient only reads the window's Absolute rect.
- **Name clashes:** recursive `FindFirstChild(.., true)` lookups never search for Title, Icon or Close.
- **BrickUI.Hatch with pcall:** sound. The weak point is the unguarded consumers (SHOULD 1).

### 4. Behaviour preserved

Preserved:
- `stateOf`, `press` with its busy lock, the 4 states, pips and Count derivation (all checked against `StreakConfig.view`), LOST once per session;
- the unchanged auto-open;
- the dots (a new PLAYTIME dot is a plus);
- the tile badge (PlaytimeReady is computed outside the visibility gate);
- TestPress on `DailyView.Card<d>`;
- PLAYTIME claim and skip-all logic;
- the celebration with its token auto-close and the CanvasGroup fallback;
- the TOMORROW countdown;
- the whole card as a hit everywhere.

Gaps: slot failure feedback (SHOULD 4) and the pet slot losing the pet's name (owner's call 4).

### 2b. Phone scale

**The fit numbers are exact** (re-derived above):
- 1.18 at 1080p;
- 1.0982 at 1050x620;
- 0.7106 at 844x390 (left edge 144.3, after the tiles at 110.2 and the pills at 138.3);
- 0.6787 at 667x375 (left edge 137.9).

**What "minimum 16" means.** It is 16 logical px, so the on-screen minimum is 16 x s:

| Screen | On-screen minimum |
|---|---|
| PC 1080p | 18.9 px |
| 1050x620 | 17.6 px |
| 844x390 | 11.4 pt |
| 667x375 | 10.9 pt |

So yes, at 0.68 the 16 px design text is 10.9 px (pt) on screen. The test (`TextSize*k >= HatchMin*ws`) checks exactly that, not 16 px on screen.

**Readability.**
- 11 pt is Apple's smallest recommended size. Uppercase GothamBlack with an ink stroke reads larger than regular 11 pt.
- The CTA text (CLAIM! / button labels, 18) is 12.2 pt or more. The 10.9 pt texts are the subs, day pills and chips.
- Acceptable on a 4.7" phone, but the owner should see it (owner's call 3).
- The plan's text sometimes mixes px and pt; say "logical 16 = 10.9 pt on a 667x375 phone".

### 5. Assets

- Every id is listed, and there are no uploads.
- The clock fallback is specified: hide it and centre the timer.
- Glow and rays art profiles are verified (see the Verified table).
- The Robux icon 132185731364109 matches the newest windows (StarterPack, Offline). The Shop's `ShopConfig.ROBUX_ICON` is the white hexagon 109535585247625. Either is fine; just be consistent.

### 6. Tests

Missing cases are listed in MUSTs 1-2 and SHOULDs 13-17. 8.1 and 8.2 are otherwise complete; with v2 check 3 using TestPress, the real `press()` path is now covered.

### 7. Vague spots (the builder would have to guess)

1. Hero Dim, tint and badges per state: fixed by MUST 4.
2. Fit variants for each live text. "Fit with variants" names none for the values. Use:
   - Day 2 Value and Day 6 Sub: `{"+X SPEED", "+X"}`;
   - hero Name: `{DISPLAY, last word}`;
   - slot buttons: `{"CLAIMED", "DONE"}`;
   - hero LOCKED: `{"IN n DAYS", "n DAYS"}`;
   - celebration Name: `{"NAME  X KG", "NAME"}`;
   - everything else: a single variant.

   Every measured worst case fits at full size, so these are only a safety net.
3. `glossButton` `opts.input` per instance:
   - Close: input = CloseHit.
   - Pill: listens to both tab hits but sinks only for the active slot's hit.
   - All others: no input (Face is an ImageButton, Activated -> press / claim / skip).
4. Slot claim failure feedback (SHOULD 4).
5. Fly-text target fallback (SHOULD 3).
6. The "stroked box" of a tile holder that has no stroke (SHOULD 13).
7. Day 4 glow key: `StreakArea` 1..6 maps to Grass, Water, Thunder, Fire, Shadow, Celestial.
8. Whether rays, prism and shine run in week-done: yes (MUST 4).
9. The new test switch `HatchTestHover` (MUST 2): Studio only, cleared after the run, like `HatchTestPulse`.

---

## What's good

- **D1 and D2 are the right calls.** A third STYLE value would have flipped 6 live scripts; the pcall child module keeps BrickUI byte-identical.
- **One logical canvas per layer.** UIScale makes strokes, corners and text scale together, so the window is the same at every size.
- **D5 is a real catch.** The spec's own fit would cover the HUD at 1050x620 and on phones. The pure function and its test table are exact.
- **Containment, tiles, hits and text are all automated.** Plus a chrome snapshot that diffs BEFORE vs AFTER, both fresh and after Gift.
- **In-engine text measurement** with fixed TextSize and `H.fit`: no silent TextScaled shrink.
- **Careful geometry.** Pip cracks derived from the SVG path, a TopHL inset that respects the corner radius, shell teeth recomputed from the mockup, icons nudged off the value line, and chip widths justified by measurement.
- **The CanvasGroup choice for the flying egg half is correct.** A rotated ClipsDescendants frame would stop clipping. The fallback is defined.
- **Strong test hygiene:** TestFreshSave, no Play takeover, no Studio UI driving, Edit require via `:Clone()`, backups with tags stripped.

## Owner's calls

1. **Bats on the Halloween band:** a one-time upload (168 x 84, group ZAB Studio), or a clean band without them.
2. **PLAYTIME warning copy.** The owner's reference said "Leaving Resets Progress!"; the plan shortens it to "LEAVING RESETS!".
   - The full text is 214 px. It fits only if SKIP ALL shrinks to about 149 px: warning box (14, 11, 226, 16); SkipAll at (248, 3, 149, 32); label (8, 5, 74, 16); Robux (84, 4.5, 20, 20); price (107, 5, 38, 16).
3. **Phone layout.**
   - The window sits about 41 px right of centre so it clears the tiles and pills.
   - Minimum text is 11.4 pt on iPhone 12-15 and 10.9 pt on iPhone SE/8.
   - Judge it on the emulator screenshot.
4. **PLAYTIME's 2-hour pet slot** shows "1K KG / PET" plus the portrait. The old slot showed the pet's name.
5. **Day 7 lime ring:** keep it (drawn under the content, per MUST 1) or drop it, as in the mockup, where the prism rim already frames the hero.
