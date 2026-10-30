REVISE - 6.5/10 vs the references (round 1). It reads as a cat from the front and tq. The side and back are one indigo
slab, the tail is a thin pipe whose crystal pokes up between the ears, and the crystals are too small to sell tier 5.

MUST FIX (most important first):
1. The light zone is missing where players look. The bib hides behind the front legs and neck, and the belly is on the
   underside, so the side and back views are about 90 % indigo (bible item 6 wants 15-25 %; "Avoid: monotone navy").
   - Add a flush LIGHT belly band on each chest flank between the legs: B.bar along flank(chest, s, y, -0.17) for local
     y 0.02..0.30, width 0.13, 0.010 proud, normal from flank(), off the leg tops. Skip the hips: the chest and hind leg hide them.
   - Raise the lowest rosette on each block to local z >= 0.0 so it clears the band.
   - Add a LIGHT throat, B.add((0, -0.66, 0.82), (0.292, 0.12, 0.075), LIGHT, "Neck", studs=[]), so the chin tone runs down the neck.
2. The tail's crystal and dark collar sit above the head between the ears in the front view (LESSONS 6). The tail sags,
   then kinks up as 4 straight thin pipes. TAILP -> [(0, 0.50, 0.86), (0, 0.74, 0.78), (0, 0.98, 0.76), (0, 1.18, 0.82),
   (0, 1.30, 0.92)], tip cluster dir (0, 0.7, 0.7), top <= z 1.10 (head top 1.27 minus ~0.15 of front-camera lift). Seg
   widths (0.085, 0.072, 0.06, 0.05) -> (0.10, 0.085, 0.07, 0.06). Tail4 seg LIGHT (lilac tip); tip collar (155) DARK -> MID.
3. At 64 px the Void crystals are pink specks, and their DARK collars read as black lumps. Shoulder clusters (line 105):
   L 0.26 -> 0.34, w 0.052 -> 0.064, base x ±0.17 -> ±0.20. Collar (line 70): w*1.6 -> w*1.3, DARK -> MID. Tail-tip cluster L 0.24 -> 0.28.
4. From the side the head is a long box with a protruding muzzle (dog-like; the bible says "Avoid: a dog head"), and the
   whiskers and cheek blades bristle like a broom. Muzzle (line 110): half y 0.145 -> 0.11, centre y -1.16 -> -1.125.
   Shift the nose, sheen, mouth, fang and whisker roots +0.07 in y and the jaw (lines 126-127) +0.05. Whiskers: length 0.22 -> 0.15,
   CRYS_L -> LIGHT. Move the cheek-blade roots back from y -0.98 to -0.80 so they grow from the jaw hinge.
5. The rosettes close into square frames, so they read as washers or bolt heads. In rosette(): bar long half a*1.45 -> a*1.15
   (opens the corners), rotate R ±25° about the normal on alternate rosettes, drop one bar on every second rosette (C-shape).
6. Pounce pin (frames 66-75): spine 10° + Neck 14° + Head 16-18° drive the face into the ground (pose_tq_act_pounce_70:
   face hidden, ears pointing forward like horns). Cap Neck at 6 and Head at 8 there.

KEEP:
- The cat read: tall CRYS-lined ears, fierce eyes with a light rim and slit pupils, the dark nose with sheen, the fang.
- Proportions: head 0.95 TW, legs 0.39 TW with flush lilac socks and pale claw nubs, the clean chest/hips step; the
  rosette idea (dark ring around a mid-tone centre) and the shoulder plus tail-tip crystal placement.
