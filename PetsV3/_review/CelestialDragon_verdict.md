REVISE - 6.5/10 vs the references (round 1). The crown, neck trim and crescent tail are great, but the colours are split
per block (white front half, blue back half), so it reads as two animals glued at the hips. The eyes show a glyph and
the gold dots read as confetti.

MUST FIX (most important first):
1. Colour zones must follow anatomy, not blocks. PEARL chest + front legs against ROYAL hips + hind legs + tail shows a
   white front glued to a blue back, and pearl (S 9 %) cannot be the 60 % base (§1 item 6). V2 = blue body, pearl front.
   Chest ROYAL (line 125); front legs ROYAL (line 195); Tail3 SHADE -> ROYAL (line 204, no white stub before the
   crescent); delete the mantle plate (line 127); add a PEARL bib front_inlay(B, chest, 0, 0.58, 1.16, 0.52, 0.005,
   PEARL, "Spine") (0.52 stays in the flat area at the tapered bottom, lesson 2) with the BELLY bands on top; body
   dorsal blades all PEARL (line 141). Head + S-neck stay pearl: jaw -> neck -> bib -> belly, gold band as the collar.
2. Eye glyph (lines 170-171): hl_on_pupil with a 0.07 highlight on a 0.09 pupil gives a white square framed in black
   ("◘") in the 512 px crop. hl_size (0.07, 0.0) -> (0.035, 0.03): a small glint on the pupil corner + a lower-right one.
3. Constellations (lines 100-107, 128-129): lone gold squares on the panels and hips read as confetti or holes. Per
   outer panel, 1 constellation: 5 gold diamonds (half 0.03) in a "W" (Cassiopeia) zigzag about 0.12 apart + 1 bigger
   4-point star (2 crossed tapered bars, 0.10 x 0.025) at one end; nothing on the inner panel; the same "W" along the
   spine on the hips. Keep both wing faces.
4. Back of head and neck (the players' view): the head's +y plates sit in rows (3 + 2) like a vent grille and the S-neck
   is a plain white column. Drop "+y" from the head studs (line 159); add 2 ROYAL crest blades on the back faces of n1
   and n2 (sz 0.8 / 0.7, bone "Neck", laid back 62 deg as in line 141), so a crest runs from the head to the tail.
5. The orbit stars (lines 218-222, ring r 0.24 at z 1.62) sit between the wing roots and bunch into one gold clump on
   the shoulders (side/back views). Radius 0.36, ORBIT_C z 1.78, star r 0.12, normal (cos a, sin a, 0.9) normalised so
   they face up and out toward the follow camera; re-run collision_free for Orbit against the wings.
6. Legs show 0.78 TH (bible 0.65), so the front view looks leggy: LEG_TOP 0.58 -> 0.50, leg block centre z 0.32 -> 0.28,
   half z 0.28 -> 0.24, and lower everything above the paws by 0.08 (body, neck, head, wings, tail, orbit).

KEEP:
- The crown of 4 gold horns (2 big swept 3-segment horns + 2 small forward ones) and the gold brow plates.
- The gold-trimmed S-neck with rivets, the crescent-moon tail blade and the broad 2-tone scalloped wings.
