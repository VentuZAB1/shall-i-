#!/bin/bash
# builder D scratch: TOP A_L variant -> halo hidden (takeoff f2-10), far blade width (takeoff 6/10), collisions
cd "/c/Users/ventu/OneDrive/Desktop/SLINGSHOT Creatures/PetsV3"
BL="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; T=$1; V="$2"; S=EclipseSeraph/_scratch/r10
cp EclipseSeraph/_scratch/EclipseSeraph_r10a.py.txt pets/EclipseSeraph.py
python - "$V" <<'PY'
import sys
p="pets/EclipseSeraph.py"; s=open(p,encoding="utf-8").read()
a='       "A_L": (40.0, -4.0, 30.0, -10.0)}'
assert a in s; s=s.replace(a,'       "A_L": (%s)}' % sys.argv[1]); open(p,"w",encoding="utf-8").write(s)
PY
HP_DIR=r10/hp_$T "$BL" -b --factory-startup --python EclipseSeraph/_scratch/halo_px.py -- clip takeoff 2 10 2 >/dev/null 2>&1 &
A=$!
"$BL" -b --factory-startup --python EclipseSeraph/_scratch/rod_metric.py -- takeoff:6,takeoff:8,takeoff:10 2>&1 | grep "^ROD" > $S/rodtop_$T.txt &
B=$!
"$BL" -b --factory-startup --python _tools/headless_clips.py -- EclipseSeraph - views=game 2>&1 | grep HEADLESS_RESULT | python -c "
import sys,json
for l in sys.stdin: d=json.loads(l[16:]); print('$T collisions', d['collisions'])" &
C=$!
wait $A $B $C
python -c "
import json
d=json.loads(open('$S/rodtop_$T.txt').read()[4:])
print('$T width L', [v['L']['minor'] for v in d.values()])"
python EclipseSeraph/_scratch/halo_count.py $S/hp_$T 2>/dev/null
