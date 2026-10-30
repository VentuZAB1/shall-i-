cd "/c/Users/ventu/OneDrive/Desktop/SLINGSHOT Creatures/PetsV3"
BL="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
"$BL" -b --factory-startup --python _tools/headless_pack.py -- InfernoPhoenix views=side,tq,game,front > /c/Users/ventu/AppData/Local/Temp/phx_pack.log 2>&1
grep -i "Traceback" -A8 /c/Users/ventu/AppData/Local/Temp/phx_pack.log | head
python _tools/pack_post.py InfernoPhoenix MoltenBoar,LavaGolem,Cerberus,Ivonrath,Thunderbird,Griffin,SolarLion views=side,tq,game,front > InfernoPhoenix/renders/_shares_raw.json
python -c "
import json
sh=json.load(open('InfernoPhoenix/renders/_shares_raw.json'))['shares_pct']
fam={'BASALT+D':('BASALT','BASALT_D'),'EMBER':('EMBER',),'PALE':('PALE',),'FIRE':('LAVA','FLAME','HOT'),'GOLD':('GOLD','GOLD_D'),'BLK+MOUTH':('BLACK','MOUTH')}
for v,row in sh.items():
  print(v, {f: round(sum(row.get(c,0) for c in cs),1) for f,cs in fam.items()}, 'BASALT', round(row.get('BASALT',0),1))
"
cd InfernoPhoenix/renders && python -c "
from PIL import Image
ims=[Image.open(f'flat_{v}.png').convert('RGB') for v in ('front','side','game','tq')]
w,h=ims[0].size
S=Image.new('RGB',(w*4,h))
for i,im in enumerate(ims): S.paste(im,(i*w,0))
S.save('_flat_v1.png')
"
