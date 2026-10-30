# round 2b value pass (review 1 MUST 4 targets: icon mean lum down, dark share up, the 3-band read): the review's
# colours kept for STEEL_BLUE / DEEP_STEEL; DEEP_STEEL now also on the wing arms, the shins + feet, lower saddle
# shells and a wider neck saddle; MEMBRANE pushed one step further (116,146,206 -> 100,130,196); wider DARK trim
import runpy, sys
V = runpy.run_path("FrostcrownDragon/_scratch/val_var.py".replace("val_var.py", "_noop.py")) if False else None
p = "pets/FrostcrownDragon.py"
s = open(p, encoding="utf-8").read()
src = open("FrostcrownDragon/_scratch/val_var.py", encoding="utf-8").read()
i0, i1 = src.index("R = {"), src.index("VARS = json")
ns = {"json": None}
exec(src[i0:i1], ns)
for key in ("arms", "shells", "memb", "trim", "legs"):
    for a, b in ns["R"][key]:
        assert s.count(a) == 1, a
        s = s.replace(a, b)
s = s.replace("MEMBRANE = (100, 130, 196)    # wing membranes (smooth), frost blue (review 1 MUST 4)",
              "MEMBRANE = (100, 130, 196)    # wing membranes (smooth), frost blue (review 1 MUST 4, one step darker: round 2)")
s = s.replace('''    """bat wing on 4 fingers: STEEL_BLUE arm + wrist knuckle + an ice thumb claw, STEEL_BLUE fingers, pale MEMBRANE''',
              '''    """bat wing on 4 fingers: DEEP_STEEL arm + wrist knuckle + an ice thumb claw, DARK fingers, MEMBRANE''')
open(p, "w", encoding="utf-8").write(s)
print("ok")
