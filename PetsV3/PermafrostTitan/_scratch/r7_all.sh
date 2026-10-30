#!/bin/bash
# Titan r6: export + every render the round asks for
cd "/c/Users/ventu/OneDrive/Desktop/SLINGSHOT Creatures/PetsV3"
BL="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
CV=PermafrostTitan/_scratch/clip_views.py
S=PermafrostTitan/_scratch
R=PermafrostTitan/renders
CMP=ThunderRex,LavaGolem,CosmicLeviathan,SeaTurtleWarrior,Treant
cp pets/PermafrostTitan.py $S/PermafrostTitan_exported_r7.py
"$BL" -b --factory-startup --python _tools/headless_full.py -- PermafrostTitan "idle:0,idle:30,idle:60,idle:90,walk:0,walk:5,walk:12,walk:24,walk:29,walk:36,roar:10,roar:22,roar:27,roar:34,roar:50,roar:66,act_kneelrise:5,act_kneelrise:9,act_kneelrise:18,act_kneelrise:20,act_kneelrise:40,act_kneelrise:50,act_kneelrise:58,act_kneelrise:70" 1 export > $S/export_r7.txt 2>&1
python sheet3.py PermafrostTitan pose_tq_ 6 > /dev/null 2>&1
sed -i 's/(final 8.5 round 6)" % (name, STAMP)/(final 8.5 round 7)" % (name, STAMP)/' $S/titan_sheets_r3.py
rm -f $R/pclose_*.png $R/hx_*.png $R/wk_*.png $R/b2_*.png $R/kv_*.png $R/rf_*.png
"$BL" -b --factory-startup --python _tools/headless_model.py -- PermafrostTitan tq,front,side,back 600 2>&1 | grep -E "Error|Traceback"
python sheet3.py PermafrostTitan model_ 2 > /dev/null
"$BL" -b --factory-startup --python $CV -- PermafrostTitan act_kneelrise:30,act_kneelrise:40,act_kneelrise:50 views=tq,game res=700 prefix=hx > /dev/null 2>&1
"$BL" -b --factory-startup --python $CV -- PermafrostTitan "roar:00,roar:10,roar:22,roar:27,roar:50,roar:66,act_kneelrise:00,act_kneelrise:09,act_kneelrise:18,act_kneelrise:20,act_kneelrise:40,act_kneelrise:50,act_kneelrise:58,act_kneelrise:70,act_kneelrise:84,idle:00,idle:30,idle:60,idle:90" views=tq res=560 prefix=b2 > /dev/null 2>&1
"$BL" -b --factory-startup --python $CV -- PermafrostTitan "walk:0,walk:6,walk:12,walk:18,walk:24,walk:30,walk:36,walk:42" views=tq,side,game res=360 prefix=wk > /dev/null 2>&1
"$BL" -b --factory-startup --python $CV -- PermafrostTitan "act_kneelrise:18,act_kneelrise:40,act_kneelrise:58" views=front,tq,back,game res=420 prefix=kv > /dev/null 2>&1
"$BL" -b --factory-startup --python $CV -- PermafrostTitan "roar:0,roar:22,roar:27,roar:50" views=front res=420 prefix=rf > /dev/null 2>&1
"$BL" -b --factory-startup --python _tools/headless_pose_close.py -- PermafrostTitan roar:0,roar:27 Head 1.3 views=front,tq res=500 > /dev/null 2>&1
python $S/titan_sheets_r3.py
python PermafrostTitan/_scratch/cv_sheet.py PermafrostTitan front "roar:0,roar:22,roar:27,roar:50" _roar_front_sheet.png 4 rf > /dev/null
"$BL" -b --factory-startup --python _tools/headless_closeup.py -- PermafrostTitan 0,-0.25,1.80 1.7 600 2>&1 | grep -E "Error|Traceback"
python sheet3.py PermafrostTitan close_ 3 > /dev/null
"$BL" -b --factory-startup --python _tools/headless_pack.py -- PermafrostTitan views=side,tq,game,back 2>&1 | grep -E "Error|Traceback"
python _tools/pack_post.py PermafrostTitan $CMP views=side,tq,game,back > $S/pack_post_r7.json 2>&1
"$BL" -b --factory-startup --python _tools/game_raw.py -- PermafrostTitan 2>&1 | grep -E "Error|Traceback"
python _tools/game_icon.py PermafrostTitan $CMP > $S/game_icon_r7.txt 2>&1
tail -1 $S/game_icon_r7.txt | cut -c1-120
python -c "
import json
s=open(r'$S/export_r7.txt',encoding='utf-8',errors='replace').read()
r=json.loads(s.split('HEADLESS_RESULT',1)[1].strip().splitlines()[0])
print({k:r[k] for k in ('collision_free','ground_min_z','audit','tris_body','lua_bytes','collisions') if k in r})"
ls -la --time-style=+%H:%M /c/cdimp/PermafrostTitan.fbx | awk '{print $6, $7}'
