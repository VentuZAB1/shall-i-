#!/bin/bash
# builder D: Roc clip pass -> summary (audit / ground / collisions) + pose renders of the picks
cd "/c/Users/ventu/OneDrive/Desktop/SLINGSHOT Creatures/PetsV3"
BL="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
N=${1:-BlizzardRoc}; PICKS=${2:-idle:24}; VIEWS=${3:-tq}
rm -f $N/renders/pose_*
"$BL" -b --factory-startup --python _tools/headless_clips.py -- $N $PICKS views=$VIEWS res=300 2>&1 | grep -E "HEADLESS_RESULT|Error|Traceback" > $N/_scratch/clips_last.txt
python - "$N" <<'PY'
import sys, json
for line in open(sys.argv[1] + "/_scratch/clips_last.txt"):
    if line.startswith("HEADLESS_RESULT"):
        d = json.loads(line[len("HEADLESS_RESULT "):])
        for kk in ("audit", "clips", "events", "tris_body", "ground_min_z", "collisions", "collision_free", "stride"):
            print(kk, json.dumps(d.get(kk))[:1200])
    else:
        print(line[:600])
PY
