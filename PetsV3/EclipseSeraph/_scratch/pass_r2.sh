#!/bin/bash
# builder D round-2 render pass for one pet: pack + shares, game icon, idle views, close-ups, model views LAST
cd "/c/Users/ventu/OneDrive/Desktop/SLINGSHOT Creatures/PetsV3"
BL="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
N=$1; CMP=$2; GCMP=$3; CLOSE=$4; MODELV=$5
LOG=$N/_scratch/pass_r2.log; : > $LOG
"$BL" -b --factory-startup --python _tools/headless_pack.py -- $N 2>&1 | grep -E "Error|Traceback|RESULT" >> $LOG
python _tools/pack_post.py $N $CMP > $N/_scratch/pack.json 2>>$LOG
"$BL" -b --factory-startup --python _tools/game_raw.py -- $N 2>&1 | grep -E "Error|Traceback" >> $LOG
python _tools/game_icon.py $N $GCMP > $N/_scratch/gold.json 2>>$LOG
"$BL" -b --factory-startup --python EclipseSeraph/_scratch/idle_views.py -- $N tq,front,side,back,game 600 2>&1 | grep -E "Error|Traceback|IDLE|tris|top" >> $LOG
IFS='|' read -ra CL <<< "$CLOSE"
for c in "${CL[@]}"; do
  eval "set -- $c"
  "$BL" -b --factory-startup --python _tools/headless_closeup.py -- $N "$@" 2>&1 | grep -E "Error|Traceback" >> $LOG
done
"$BL" -b --factory-startup --python _tools/headless_model.py -- $N "$MODELV" 520 2>&1 | grep -E "Error|Traceback|HEADLESS_RESULT" >> $LOG
python FrostcrownDragon/_scratch/iconstats.py $N >> $LOG
echo DONE >> $LOG
