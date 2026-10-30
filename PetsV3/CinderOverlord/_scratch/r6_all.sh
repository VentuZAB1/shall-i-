#!/bin/bash
# Cinder r6: export + every render the round asks for (run from anywhere)
cd "/c/Users/ventu/OneDrive/Desktop/SLINGSHOT Creatures/PetsV3"
BL="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
CV=PermafrostTitan/_scratch/clip_views.py
S=CinderOverlord/_scratch
cp pets/CinderOverlord.py $S/CinderOverlord_exported_r6b.py
PICKS=$(grep -o "pose_tq_[a-z_]*_[0-9]*\.png" $S/export_r5.txt | sort -u | sed 's/pose_tq_//; s/\.png//' | sed -E 's/_([0-9]+)$/:\1/' | sed -E 's/:0*([0-9])/:\1/' | tr '\n' ',' | sed 's/,$//')
"$BL" -b --factory-startup --python _tools/headless_full.py -- CinderOverlord "$PICKS" 1 export > $S/export_r6.txt 2>&1
python sheet3.py CinderOverlord pose_tq_ 6 > /dev/null 2>&1
bash $S/rend.sh CinderOverlord 0,-0.95,1.78 2.1 > /dev/null
"$BL" -b --factory-startup --python PermafrostTitan/_scratch/gamelook.py -- CinderOverlord views=tq,game > /dev/null 2>&1
bash $S/goldrun.sh
"$BL" -b --factory-startup --python $S/portrait_pose.py -- CinderOverlord jobs "act_molt:40:1,-1.36,0.62:CinderOverlord_portrait_alt.png" > /dev/null 2>&1
rm -f CinderOverlord/renders/cv_game_walk_*.png CinderOverlord/renders/cv_side_walk_*.png CinderOverlord/renders/mr6_*.png
"$BL" -b --factory-startup --python $CV -- CinderOverlord "walk:0,walk:8,walk:16,walk:24,walk:32,walk:40" views=game,side res=400 prefix=cv > /dev/null 2>&1
"$BL" -b --factory-startup --python $CV -- CinderOverlord "act_molt:0,act_molt:22,act_molt:34,act_molt:40,act_molt:56,act_molt:84,act_molt:100" views=front,tq res=300 prefix=mr6 > /dev/null 2>&1
W="walk:0,walk:8,walk:16,walk:24,walk:32,walk:40"
M="act_molt:0,act_molt:22,act_molt:34,act_molt:40,act_molt:56,act_molt:84,act_molt:100"
python PermafrostTitan/_scratch/cv_sheet.py CinderOverlord game $W _cv_walk_game.png 6 cv > /dev/null
python PermafrostTitan/_scratch/cv_sheet.py CinderOverlord side $W _cv_walk_side.png 6 cv > /dev/null
python PermafrostTitan/_scratch/cv_sheet.py CinderOverlord front $M _molt_r6_front.png 7 mr6 > /dev/null
python PermafrostTitan/_scratch/cv_sheet.py CinderOverlord tq $M _molt_r6_tq.png 7 mr6 > /dev/null
python -c "
import json
s=open(r'$S/export_r6.txt',encoding='utf-8',errors='replace').read()
r=json.loads(s.split('HEADLESS_RESULT',1)[1].strip().splitlines()[0])
print({k:r[k] for k in ('collision_free','ground_min_z','audit','tris_body','lua_bytes','collisions') if k in r}, 'stride', r.get('export',{}).get('meta',{}).get('stride'))"
ls -la --time-style=+%H:%M /c/cdimp/CinderOverlord.fbx CinderOverlord/*.png | awk '{print $6, $7}'
