# Abyssal Orca - art director review 3 (2026-10-14) - MODEL APPROVED (8.5/10)

**Model: APPROVE, 8.5/10 for a 1.5% SECRET** (v1 2.5, v2 7). This is the DEEP SOVEREIGN as briefed, and it now sits
level with Thunder Rex as a secret.
- A smooth, blunt-headed orca torpedo, with the melon dome now in.
- A flush black/white/saddle pattern that reads at 64 px.
- A fierce face, the stepped blade dorsal with jade veins, and round lantern beads.
- The best hero piece in the Tide egg: a gold-clawed jade teardrop on a gold-ringed rod, with a gold coronet.

**The mesh is locked.** Don't touch it unless the owner asks, apart from the optional polish in section 3. The rig is
unchanged apart from the +0.035 Lure root lift, which is harmless, so carry on with the clips. The next gate is the
clip round (section 4).

What I looked at:
- `pets/AbyssalOrca.py` v3 (760 lines), and the v2 → v3 rig and `check_pairs` diff
- `blockkit.py` against `_tools/blockkit_pre_tube_20261014.py`
- `_model_sheet` (600 px), `_close_sheet`, `_orb_sheet` and all single renders at full size
- the 3 flat ID renders and `_icons_strip_64/128` (zoomed)
- 2-3x crops of the saddle, lobes, fluke notch and front face

Temp files are outside the project; nothing but this verdict was written.

---------------------------------------------------------------------------------------------------------------------
## 1. The Tube deviation from my FIX 3 - ACCEPTED, and better than my recipe
Your diagnosis is right on all three points:
- The end-face rounding recedes ~0.08-0.12, so a 0.05 burial can't hide it.
- `_resolve` caps `_off` at `0.45 × mn`, which silently clips my matched-rnd formula on thin shells.
- `seg ext` shifts the whole taper.

A lofted superellipse tube with rings exactly at the stations makes `hull()` the truth by construction. Making the
bands the same section (outer skin + inner skin + crisp edge walls) is the clean answer for flush patterns.

I checked the kit change:
- It is **purely additive.** `part_bm()` dispatches Tube → `_tube_bm` and keeps Poly → `_poly_bm` and Block → `_box_bm` unchanged.
- The StudMask branch for Block/Poly is the old expression, unchanged.
- `_apply_head_xf` only gains a Tube branch.
- No other pet's build changes.
- The tubes carry the stud skin (studs show on the hull, the bands and the saddle).

The n 2.6 section keeps the family's soft-box read, so it still looks like one of ours, not a vinyl toy.

---------------------------------------------------------------------------------------------------------------------
## 2. Review-2 fixes and checklist

| fix | result |
|---|---|
| 1 saddle | **lands.** A flush grey chevron with a curved front edge. From the game camera it reads as a real orca saddle, with no lip, step or "box in a box". zlo +0.40 instead of my -0.10 was the right call for a fully visible band. |
| 2 flank lobes | **lands.** A stepped white staircase rising toward the back: flush, studded, split at Tail1. No shards anywhere (side, back and game crops at 2x). It is the angular f_63 look done in our kit. |
| 3 hull | **lands (via Tube).** No creases at any joint in the side or back views. The head is blunt with a domed melon, and the coronet and rod root sit on the skin. |
| 4 eye lens | **lands.** The big lens shows from the side, the tq and the front; at 64 px it is ~5x2.5 px (gate ≥ 3x2). |
| 5 fluke notch | **lands.** A clean V and no knob. |
| 6 orb | **lands.** A smooth teardrop that is clearly a lure drop, with the HOT drip visible. The pepper/pumpkin read is gone. |
| 7 beads | **lands.** Octagonal lanterns; the tile/porthole read is gone. |
| 8 polish | chin dash fixed; brow tabs not done (optional, section 3) |

**Checklist:**
1. **Lineup - PASS.** It is the most distinctive pet in the Tide egg.
2. **64 px - PASS.** The official icon strip: you can name the orca, the gold-and-jade lantern and the black/white pattern (eye patch plus white belly line). At 128 px it is one of the cleanest icons we have.
3. **Value blocking - PASS** on the flat ID count (my own count matches yours exactly). See the gate ruling below.
4. **Accent - PASS.**
   - GLOW is 7.3-8.5% plus HOT 1.7-2.0% and DEEP ~1.5%, so ~10.5-12% of jade family.
   - GOLD + GOLD_D is 4.4% (side), 8.4% (tq) and 5.7% (game). That is above the 2-3% target; I accept it, because all of it is the hero lantern.
5. **Silhouette - PASS.** No change from v2, and the melon improves the head.
6. **Face - PASS.** Brow tabs are a polish item.
7. **Fins - PASS.**
8. **Hard rules - PASS.** Flush, studded patterns; nothing floating; 10.2k tris; no Neon.
9. **Rig - PASS.** Unchanged, and the saddle, lobes and belly band are split per bone.
10. **Deliverables - PASS.** 600 px views, close and orb sheets, icon strips, flat counts.

**Gate ruling on the white share.**
- **Flat ID counts are now the official method** (more accurate than my shaded classifier). They are recorded here as
  the orca baseline:

  | view | INK | WHITE | SADDLE | WHITE+SADDLE |
  |---|---|---|---|---|
  | side | 57.6 | 14.4 | 4.6 | |
  | tq | 59.0 | 7.7 | 3.7 | |
  | game | 60.0 | 3.3 | 10.9 | 14.2 |

- On my own shaded method, for continuity with review 2: side WHITE 22.7% passes; tq 12.7% does not.
- My "tq WHITE ≥ 18%" gate was only a proxy for the 64 px orca read, and that read now passes. **I waive it. Do NOT
  push the white higher.** From above, a real orca is black. More white on the upper flanks would turn it into a
  white-sided dolphin and dilute the saddle, which is the game camera's light read.
- Game WHITE+SADDLE 14.2% against the ≥ 15% gate is within measurement noise: accepted.

---------------------------------------------------------------------------------------------------------------------
## 3. Optional polish (not blocking; only if you have time)
1. **Brow tabs (review-2 FIX 8b):** in the front view the two INK_D brow blocks still stick out of the rostrum like small headphones. Seat them at `n * 0.0` and yaw them 8° toward the face.
2. **White jaw seams:** close_side shows two vertical panel edges in the white under the eye, where the boxed Jaw loft ends against the throat tube. Run the throat tube 0.02 further forward, under the jaw's back face. They are invisible at game distance.
3. **Orb glint:** the HOT glint is a flat square that reads as a sticker in close-ups. Make it smaller (0.018), or a 2-part curved glint, or drop it, since the Bulb VFX will supply the highlight.
4. **Specular streak** on the smooth hull: confirm in the Studio zoo test. If a hard highlight line shows along the back in game, flat-shade the top 2 ring rows; otherwise leave it.

---------------------------------------------------------------------------------------------------------------------
## 4. Next gate: the clips
The rig is approved, and I see the clip code is already in. The review-1 section 4 tables and the review-2 section 3 notes apply.

**Return:**
- **Pose sheets:**
  - swim: 4 phases
  - idle: f40, f66 blow, f95 roll
  - roar: f12, f20, f26, f36 lash, f50
  - act_lure: f6, f28, f50, f57, f60, f62, f78, f96
- **The builder pass:** `collision_free: true`, `ground_min_z` ≥ -0.02 in all 4 clips, linear 0, loops closed, and the Esca clearance numbers for the dangle and the lure-up frames.

The owner to-do is the same as for all pets: Studio import as creator ZAB Studio, VFX Studio effects on Bulb / Glow1-3 / DorsalTip / FlukeL/R / Blow / Maw / eyes, driven by the clip events, then Save + Publish.
