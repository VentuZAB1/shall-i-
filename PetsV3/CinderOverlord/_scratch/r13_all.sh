#!/bin/bash
# Cinder r13: export + every render the round asks for
cd "/c/Users/ventu/OneDrive/Desktop/SLINGSHOT Creatures/PetsV3"
BL="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
CV=PermafrostTitan/_scratch/clip_views.py
S=CinderOverlord/_scratch
cp pets/CinderOverlord.py $S/CinderOverlord_exported_r13.py
PICKS=$(grep -o "pose_tq_[a-z_]*_[0-9]*\.png" $S/export_r9.txt | sort -u | sed 's/pose_tq_//; s/\.png//' | sed -E 's/_([0-9]+)$/:\1/' | sed -E 's/:0*([0-9])/:\1/' | tr '\n' ',' | sed 's/,$//')
"$BL" -b --factory-startup --python _tools/headless_full.py -- CinderOverlord "$PICKS" 1 export > $S/export_r13.txt 2>&1
python sheet3.py CinderOverlord pose_tq_ 6 > /dev/null 2>&1
bash $S/rend.sh CinderOverlord 0,-1.05,2.10 2.9 > /dev/null
"$BL" -b --factory-startup --python PermafrostTitan/_scratch/gamelook.py -- CinderOverlord views=tq,game > /dev/null 2>&1
bash $S/goldrun.sh
"$BL" -b --factory-startup --python $S/portrait_pose.py -- CinderOverlord jobs "act_molt:40:1,-1.36,0.80:CinderOverlord_portrait_alt.png" > /dev/null 2>&1
rm -f CinderOverlord/renders/cv_game_walk_*.png CinderOverlord/renders/cv_side_walk_*.png CinderOverlord/renders/cv_front_roar_*.png CinderOverlord/renders/cv_side_roar_*.png
mkdir -p $S/stale_r13_renders
mv CinderOverlord/renders/mr12_* CinderOverlord/renders/hx12_* $S/stale_r13_renders/ 2>/dev/null
mv CinderOverlord/renders/_molt_r12_front.png CinderOverlord/renders/_molt_r12_tq.png $S/stale_r13_renders/ 2>/dev/null
W="walk:0,walk:8,walk:16,walk:24,walk:32,walk:40"
M="act_molt:0,act_molt:22,act_molt:34,act_molt:40,act_molt:56,act_molt:84,act_molt:100"
R="roar:0,roar:14,roar:22,roar:30,roar:44,roar:58"
"$BL" -b --factory-startup --python $CV -- CinderOverlord "$W" views=game,side res=400 prefix=cv > /dev/null 2>&1
"$BL" -b --factory-startup --python $CV -- CinderOverlord "$R" views=front,side res=300 prefix=cv > /dev/null 2>&1
"$BL" -b --factory-startup --python $CV -- CinderOverlord "$M" views=front,tq res=300 prefix=mr13 > /dev/null 2>&1
python PermafrostTitan/_scratch/cv_sheet.py CinderOverlord game $W _cv_walk_game.png 6 cv > /dev/null
python PermafrostTitan/_scratch/cv_sheet.py CinderOverlord side $W _cv_walk_side.png 6 cv > /dev/null
python PermafrostTitan/_scratch/cv_sheet.py CinderOverlord front $R _cv_roar_front.png 6 cv > /dev/null
python PermafrostTitan/_scratch/cv_sheet.py CinderOverlord side $R _cv_roar_side.png 6 cv > /dev/null
python PermafrostTitan/_scratch/cv_sheet.py CinderOverlord front $M _molt_r13_front.png 7 mr13 > /dev/null
python PermafrostTitan/_scratch/cv_sheet.py CinderOverlord tq $M _molt_r13_tq.png 7 mr13 > /dev/null
"$BL" -b --factory-startup --python $S/head_share.py -- CinderOverlord view=game clip=idle f=0 2>&1 | grep HEADSHARE > $S/headshare_r13.txt
"$BL" -b --factory-startup --python $S/paw_px.py -- CinderOverlord idle:0 2>&1 | grep PAWPX > $S/pawpx_r13.txt
"$BL" -b --factory-startup --python $S/coll_probe.py -- CinderOverlord step=1 dstep=2 "depth_out=C:/Users/ventu/OneDrive/Desktop/SLINGSHOT Creatures/PetsV3/CinderOverlord/_scratch/coll_depths_r13.json" > $S/coll_probe_r13.txt 2>&1
"$BL" -b --factory-startup --python $S/stance_probe.py -- CinderOverlord step=2 2>&1 | grep STANCE > $S/stance_r13.txt
"$BL" -b --factory-startup --python $S/face_id.py -- CinderOverlord res=160 out=face_id_r13 2>&1 | grep FACEID > $S/face_id_r13.txt
python $S/gold_r13.py
sed -i 's/(final 8.5 round 12)/(final 8.5 round 13)/' $S/alt_strip.py
python $S/alt_strip.py
python $S/icon_game_64_128.py
python $S/stamp.py CinderOverlord "final 8.5 round 13" gamelook_game.png gamelook_tq.png close_front.png _model_sheet.png _close_sheet.png _pose_tq_sheet.png _cv_walk_game.png _cv_walk_side.png _cv_roar_front.png _cv_roar_side.png _molt_r13_front.png _molt_r13_tq.png _icons2_strip_64.png _icons2_strip_128.png _icons_strip_64.png _icons_strip_128.png
python -c "
import json
s=open(r'$S/export_r13.txt',encoding='utf-8',errors='replace').read()
r=json.loads(s.split('HEADLESS_RESULT',1)[1].strip().splitlines()[0])
print({k:r[k] for k in ('collision_free','ground_min_z','audit','tris_body','lua_bytes','collisions') if k in r}, 'stride', r.get('export',{}).get('meta',{}).get('stride'))"
cat $S/headshare_r13.txt $S/pawpx_r13.txt | cut -c1-300
ls -la --time-style=+%H:%M /c/cdimp/CinderOverlord.fbx CinderOverlord/*.png | awk '{print $6, $7}'
I="idle:0,idle:15,idle:30,idle:45,idle:60,idle:75,idle:90,idle:105"; "$BL" -b --factory-startup --python $CV -- CinderOverlord "$I" views=game,front res=300 prefix=cv > /dev/null 2>&1; python PermafrostTitan/_scratch/cv_sheet.py CinderOverlord game $I _cv_idle_game.png 8 cv > /dev/null; python PermafrostTitan/_scratch/cv_sheet.py CinderOverlord front $I _cv_idle_front.png 8 cv > /dev/null
"$BL" -b --factory-startup --python $S/hood_close.py -- CinderOverlord frames=0,20 res=800 > /dev/null 2>&1
python $S/hood_sheet.py
python $S/stamp.py CinderOverlord "final 8.5 round 13" _cv_idle_game.png _cv_idle_front.png
rm -f CinderOverlord/renders/cv_game_idle_*.png CinderOverlord/renders/cv_front_idle_*.png
"$BL" -b --factory-startup --python $CV -- CinderOverlord "$M" views=game res=300 prefix=mg13 > /dev/null 2>&1
python PermafrostTitan/_scratch/cv_sheet.py CinderOverlord game $M _molt_game.png 7 mg13 > /dev/null
rm -f CinderOverlord/renders/mg13_*.png
python $S/stamp.py CinderOverlord "final 8.5 round 13" _molt_game.png
