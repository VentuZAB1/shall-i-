#!/bin/bash
# Cinder r7: export + every render the round asks for
cd "/c/Users/ventu/OneDrive/Desktop/SLINGSHOT Creatures/PetsV3"
BL="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
CV=PermafrostTitan/_scratch/clip_views.py
S=CinderOverlord/_scratch
cp pets/CinderOverlord.py $S/CinderOverlord_exported_r8.py
PICKS=$(grep -o "pose_tq_[a-z_]*_[0-9]*\.png" $S/export_r7.txt | sort -u | sed 's/pose_tq_//; s/\.png//' | sed -E 's/_([0-9]+)$/:\1/' | sed -E 's/:0*([0-9])/:\1/' | tr '\n' ',' | sed 's/,$//')
"$BL" -b --factory-startup --python _tools/headless_full.py -- CinderOverlord "$PICKS" 1 export > $S/export_r8.txt 2>&1
python sheet3.py CinderOverlord pose_tq_ 6 > /dev/null 2>&1
bash $S/rend.sh CinderOverlord 0,-1.0,1.86 2.6 > /dev/null
"$BL" -b --factory-startup --python PermafrostTitan/_scratch/gamelook.py -- CinderOverlord views=tq,game > /dev/null 2>&1
bash $S/goldrun.sh
"$BL" -b --factory-startup --python $S/portrait_pose.py -- CinderOverlord jobs "act_molt:40:1,-1.36,0.80:CinderOverlord_portrait_alt.png" > /dev/null 2>&1
rm -f CinderOverlord/renders/cv_game_walk_*.png CinderOverlord/renders/cv_side_walk_*.png CinderOverlord/renders/cv_front_roar_*.png CinderOverlord/renders/cv_side_roar_*.png
mkdir -p $S/stale_r8_renders
mv CinderOverlord/renders/mr7_* CinderOverlord/renders/crown_* $S/stale_r8_renders/ 2>/dev/null
mv CinderOverlord/renders/_molt_r7_front.png CinderOverlord/renders/_molt_r7_tq.png $S/stale_r8_renders/ 2>/dev/null
W="walk:0,walk:8,walk:16,walk:24,walk:32,walk:40"
M="act_molt:0,act_molt:22,act_molt:34,act_molt:40,act_molt:56,act_molt:84,act_molt:100"
R="roar:0,roar:14,roar:22,roar:30,roar:44,roar:58"
"$BL" -b --factory-startup --python $CV -- CinderOverlord "$W" views=game,side res=400 prefix=cv > /dev/null 2>&1
"$BL" -b --factory-startup --python $CV -- CinderOverlord "$R" views=front,side res=300 prefix=cv > /dev/null 2>&1
"$BL" -b --factory-startup --python $CV -- CinderOverlord "$M" views=front,tq res=300 prefix=mr8 > /dev/null 2>&1
python PermafrostTitan/_scratch/cv_sheet.py CinderOverlord game $W _cv_walk_game.png 6 cv > /dev/null
python PermafrostTitan/_scratch/cv_sheet.py CinderOverlord side $W _cv_walk_side.png 6 cv > /dev/null
python PermafrostTitan/_scratch/cv_sheet.py CinderOverlord front $R _cv_roar_front.png 6 cv > /dev/null
python PermafrostTitan/_scratch/cv_sheet.py CinderOverlord side $R _cv_roar_side.png 6 cv > /dev/null
python PermafrostTitan/_scratch/cv_sheet.py CinderOverlord front $M _molt_r8_front.png 7 mr8 > /dev/null
python PermafrostTitan/_scratch/cv_sheet.py CinderOverlord tq $M _molt_r8_tq.png 7 mr8 > /dev/null
python -c "
import json
s=open(r'$S/export_r8.txt',encoding='utf-8',errors='replace').read()
r=json.loads(s.split('HEADLESS_RESULT',1)[1].strip().splitlines()[0])
print({k:r[k] for k in ('collision_free','ground_min_z','audit','tris_body','lua_bytes','collisions') if k in r}, 'stride', r.get('export',{}).get('meta',{}).get('stride'))"
ls -la --time-style=+%H:%M /c/cdimp/CinderOverlord.fbx CinderOverlord/*.png | awk '{print $6, $7}'
