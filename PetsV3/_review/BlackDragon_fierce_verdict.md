REVISE 7/10 - it reads as an eastern lung at 64 px (S-body, gold antlers, whisker arcs) and the face is properly fierce. Three things hold it back:
the body tube is fatter than the head, so it reads as a long sausage-dog; in the tq and side views the whiskers cross the mouth like gold rods; and the pearl
reads as a sugar cube. (Phase 1 = model only; the clips were not judged. Colours are fine per the Studio calibration: INK lands as near-black indigo.)

LENGTH (the coordinator's question): do NOT make it longer in world size. At ~3.9 BU it is already ~2.3x its own height (~20 studs long at x1, ~45 studs at
x2.2 behind a 5-stud player). What sells a lung is the length/diameter ratio, so thin the tube instead (item 1): D 0.34 -> 0.28 gives ~12.7 D
at the same 3.9 BU, close to the plan's 14-16 D.

Must fix:
1. Sausage body: today the tube (D 0.34) is taller than the snout (0.20) and the cranium (0.28), so the head looks small. Set D 0.34 -> 0.28
   (RAD and the scutes / back ridge / mane follow it) and the neck rings 0.155 -> 0.135. Deepen the S so it flows: CP[3] z 1.02 -> 1.08,
   CP[5] z 0.64 -> 0.58, CP[9] z 1.01 -> 1.08. Move the hind-leg hip x 0.095 -> 0.075 so it stays inside the thinner Body5. The head becomes 1.43 D wide
   (the plan says 1.4).
2. The whiskers cross the face (model_tq, close_tq, model_side): a gold rod lies across the open jaw, then drops down in front of the neck. Re-route each
   whisker back along the jaw line, then let it droop beside the neck: w = HC + (s*0.14,-0.52,-0.05), (s*0.24,-0.40,-0.12), (s*0.38,-0.20,-0.20),
   (s*0.50,0.02,-0.34), (s*0.58,0.20,-0.52). The front view keeps its two arcs; the tq and side views show barbels trailing back under the cheek
   (this path clears the jaw, cheek frills, neck and pearl).
3. The pearl reads as a white sugar cube with a pink sticker (model_tq, close_tq). It is the prop of the idle and the signature, so it must read at 30 studs.
   Half 0.08 -> 0.11; add a 2nd PEARL block of the same size rotated (45,0,45) for a faceted, round silhouette; replace the PEARL_C diamond
   with a GOLD equator band (0.025 tall, 0.01 proud) that ties it to the accent. The flames stay VFX.

Keep:
- the face: heavy dark brows over gold eyes with slit pupils, the nostril knobs, the open jaw with 4 fangs, the tongue and the flame beard
- the gold 3-segment antlers with 2 tines, the chimu, the ox ears and the cheek frills
- the clam-belly scutes, the dark back ridge under the violet flame crest, and the 3-blade tail fan
