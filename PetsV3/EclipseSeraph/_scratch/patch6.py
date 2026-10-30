# round 2b value pass (review 1 MUST 1 / MUST 2 targets measured on the portrait: near-white, saturation, dark):
# deeper lilac body + wing lilac (same hue), the upper pair's coverts / hand coverts / secondaries lilac (its WING_IN
# primaries stay the one pale highlight), the middle + lower pairs' coverts BODY_MID, OBSID one step darker
import os
p = "pets/EclipseSeraph.py"
s = open(p, encoding="utf-8").read()
src = open("EclipseSeraph/_scratch/val_var.py", encoding="utf-8").read()
ns = {}
exec(src[src.index("COV = "):src.index("VARS = json")], ns)
for key in ("cov_bc", "sec_a", "deep", "a_lilac", "obs"):
    for a, b in ns["R"][key]:
        assert s.count(a) == 1, a
        s = s.replace(a, b)
rep = [
    ("BODY_MID = (184, 128, 214)    # mid lilac: chest, tuck, waist, hips, legs, paws, tail (review 1 MUST 1)",
     "BODY_MID = (184, 128, 214)    # rich lilac (H 278): chest, tuck, waist, hips, legs, paws, tail, coverts of B + C"),
    ("WING_LILAC = (190, 150, 226)  # flight feathers of the middle + lower wing pairs (review 1 MUST 1)",
     "WING_LILAC = (190, 150, 226)  # flight feathers of B + C, the upper pair's coverts + secondaries"),
    ("OBSID = (46, 46, 70)          # mane rings, flight-feather tips, the solid halo disc, brows, tail tuft",
     "OBSID = (46, 46, 70)          # mane, flight-feather tips, the solid halo disc, brows, tail tuft (one step darker)"),
    ('''    """dense feather wing: MOON_IVORY arm bar (studded) + wrist + hand bar; a covert row (MOON_IVORY studded on the
    upper pair, WING_IN on the others); secondaries hanging back to the hinge line (IVORY_D on the upper pair, WING_IN
    on the others); primaries fanned densely from the wrist on the hand bone; every flight feather tipped OBSID"""''',
     '''    """dense feather wing: MOON_IVORY arm bar (studded) + wrist + hand bar; a covert row (WING_LILAC studded on the
    upper pair, BODY_MID on the others); WING_LILAC secondaries hanging back to the hinge line; primaries fanned densely
    from the wrist on the hand bone (WING_IN on the upper pair = the one pale highlight, WING_LILAC on the others);
    every flight feather tipped OBSID"""'''),
]
for a, b in rep:
    assert s.count(a) == 1, a[:80]
    s = s.replace(a, b)
open(p, "w", encoding="utf-8").write(s)
print("ok")
