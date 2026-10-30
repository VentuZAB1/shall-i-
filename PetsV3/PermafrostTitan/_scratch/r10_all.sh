#!/bin/bash
# Titan r10 (toes tucked 40, lead ruling 10-28): export + the act evidence pack
cd "/c/Users/ventu/OneDrive/Desktop/SLINGSHOT Creatures/PetsV3"
BL="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
CV=PermafrostTitan/_scratch/clip_views.py
S=PermafrostTitan/_scratch
R=PermafrostTitan/renders
mkdir -p $S/r8_export_files && cp -n /c/cdimp/PermafrostTitan.fbx $S/r8_export_files/PermafrostTitan_r8_0953.fbx
cp pets/PermafrostTitan.py $S/PermafrostTitan_exported_r10.py
"$BL" -b --factory-startup --python _tools/headless_full.py -- PermafrostTitan "idle:0,idle:30,idle:60,idle:90,walk:0,walk:5,walk:12,walk:24,walk:29,walk:36,roar:10,roar:22,roar:27,roar:34,roar:50,roar:66,act_kneelrise:5,act_kneelrise:9,act_kneelrise:18,act_kneelrise:20,act_kneelrise:40,act_kneelrise:50,act_kneelrise:58,act_kneelrise:70" 1 export > $S/export_r10.txt 2>&1
python sheet3.py PermafrostTitan pose_tq_ 6 > /dev/null 2>&1
rm -f $R/hx_*.png $R/b2_tq_act_*.png $R/kv_*.png $R/gs_*.png
"$BL" -b --factory-startup --python $CV -- PermafrostTitan act_kneelrise:30,act_kneelrise:40,act_kneelrise:50 views=tq,game res=700 prefix=hx > /dev/null 2>&1
"$BL" -b --factory-startup --python $CV -- PermafrostTitan "act_kneelrise:00,act_kneelrise:09,act_kneelrise:18,act_kneelrise:20,act_kneelrise:40,act_kneelrise:50,act_kneelrise:58,act_kneelrise:70,act_kneelrise:84" views=tq res=560 prefix=b2 > /dev/null 2>&1
"$BL" -b --factory-startup --python $CV -- PermafrostTitan "act_kneelrise:18,act_kneelrise:40,act_kneelrise:58" views=front,tq,back,game res=420 prefix=kv > /dev/null 2>&1
GS=$(python -c "print(','.join('act_kneelrise:%d' % f for f in range(0, 65, 4)))")
"$BL" -b --factory-startup --python $CV -- PermafrostTitan "$GS" views=game res=360 prefix=gs > /dev/null 2>&1
"$BL" -b --factory-startup --python $S/kneel_cam.py -- r10b 30,40,50 views=game2x,tq2x > /dev/null 2>&1
python $S/r10_pack.py
python -c "
import json
s=open(r'$S/export_r10.txt',encoding='utf-8',errors='replace').read()
r=json.loads(s.split('HEADLESS_RESULT',1)[1].strip().splitlines()[0])
print({k:r[k] for k in ('collision_free','ground_min_z','audit','tris_body','lua_bytes','collisions','events') if k in r})"
ls -la --time-style=+%Y-%m-%d_%H:%M:%S /c/cdimp/PermafrostTitan.fbx PermafrostTitan/PermafrostTitan.lua PermafrostTitan/PermafrostTitan_meta.json PermafrostTitan/PermafrostTitan_bu.json PermafrostTitan/PermafrostTitan_portrait_raw.png | awk '{print $6, $7}'
