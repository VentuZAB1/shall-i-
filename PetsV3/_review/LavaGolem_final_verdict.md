APPROVE 8/10 - a real pass: it went from a grey Minecraft iron golem (5.5) to a volcano silverback. You get the knuckle stance,
silver rock back over black limbs, molten joint bands and seams, a sagittal crest, fangs and boulder fists. The tq / portrait view is
strong and the three acts are the most physical in the roster. (Final gate, phase 2: model + all clips.)

Earlier must-fixes (fierce_verdict):
1. Upright side silhouette: FIXED. The upper body leans 18 deg more about the waist, there is a rump block, the fists are planted, and the
   back now slopes down from the hump (~50 deg, steeper than the 35-40 asked, but it reads as a hunched gorilla).
2. Pillar arms: MOSTLY FIXED. The upper arm narrows into the elbow, the forearm tapers to a visible wrist and the fist reads as its own boulder.
   The guard plank is replaced by 2 shards. From the front the ")(" bow is still slight (see polish 2).
3. Bland grey: FIXED. Basalt is warmed, forearms/fists/shins/feet are DARK, the hump and back plates are silver, and there are magma
   bands at the elbow, wrist and knee, deltoid/thigh seams and magma gaps under the back plates. Orange measures 2-8.5 % by view.
4. Head size / nostrils: FIXED. The head is scaled 1.18 and raised, the face clears the pauldrons, the brow overhangs and the nostrils are on the muzzle.
5. Emet glyph: FIXED. There are 3 full bars on the brow's front face.

Animation (checked front/side/tq renders of the exported blend; ground_min -0.016 in walk, 0.0 elsewhere):
- idle KNUCKLE REST: the right fist lifts and turns for inspection, then cracks 3x into the left palm and plants back. Unique.
- roar CHEST BEAT: rises tall, 6 alternating beats, then a hoot with the arms flung wide and the head back. Unmistakable gorilla.
- act_pound: R smash, L smash, overhead clasp, jump (+0.15 clear of the ground), double-fist smash, impact crouch. Big arcs, reads at 30 studs.
- walk: the knuckle-walk with planted knuckles (builder's note) is right for this creature.

Optional polish (not blocking):
1. The brow shelf is DARK, smooth (role "detail", no studs) and 0.147 wide, so from the front and side it reads as a black visor /
   headband more than a rock brow. Make it BASALT or TOPS with studs (nostud off) and keep the 3 MAGMA bars on it.
2. To get a clearer ")(" from the front, move E x 0.58 -> 0.62 and keep W at 0.45, then re-check the Fore/Leg pairs.
3. From the front, the 4 chest seams around the heart read as an "X" bow-tie/buckle. Run the upper pair up toward the armpits
   (end at z +0.06 instead of -0.02) so they flow into the deltoid seams.
