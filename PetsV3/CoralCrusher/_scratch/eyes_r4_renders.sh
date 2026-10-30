#!/bin/bash
# Crab r4 eyes: before / after renders (face close-up + game camera at 1x = 390 px) for the eye-stalk change.
cd "/c/Users/ventu/OneDrive/Desktop/SLINGSHOT Creatures/PetsV3"
BL="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
CV=PermafrostTitan/_scratch/clip_views.py
P=pets/CoralCrusher.py
S=CoralCrusher/_scratch
cp $P $S/CoralCrusher_eyes_r4.py
for tag in B A; do
  if [ $tag = B ]; then cp $S/CoralCrusher_before_eyes.py $P; else cp $S/CoralCrusher_eyes_r4.py $P; fi
  "$BL" -b --factory-startup --python _tools/headless_closeup.py -- CoralCrusher 0,-0.56,0.46 1.9 600 \
      "front=0,-1,0.22;tq=0.35,-1,0.75" ey${tag}_ > /dev/null 2>&1
  [ -n "$SKIPGAME" ] || "$BL" -b --factory-startup --python $CV -- CoralCrusher \
      "act_semaphore:30,act_semaphore:41,act_semaphore:53,act_semaphore:62,act_semaphore:66" \
      views=game res=390 prefix=ey${tag} > /dev/null 2>&1
done
cp $S/CoralCrusher_eyes_r4.py $P
cmp -s $P $S/CoralCrusher_eyes_r4.py && echo "pet file = r4 eyes"
ls CoralCrusher/renders | grep -E "^ey[AB]" | tr '\n' ' '
