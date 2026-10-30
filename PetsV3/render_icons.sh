#!/usr/bin/env bash
# Render icons/*.svg to transparent 512px PNGs with headless Chrome, then build icons/_sheet.jpg.
cd "$(dirname "$0")"
CHROME="/c/Program Files/Google/Chrome/Application/chrome.exe"
D=$(cygpath -w "$PWD/icons")
for f in icons/*.svg; do
  n=$(basename "$f" .svg)
  "$CHROME" --headless=new --disable-gpu --default-background-color=00000000 --hide-scrollbars \
    --window-size=512,512 --screenshot="$D\\$n.png" "file:///${D//\\//}/$n.svg" > /dev/null 2>&1
done
python - <<'EOF'
from PIL import Image
import glob, os
fs = sorted(glob.glob('icons/*.png'))
sheet = Image.new('RGBA', (220 * len(fs), 220), (232, 232, 232, 255))
for i, f in enumerate(fs):
    sheet.alpha_composite(Image.open(f).convert('RGBA').resize((220, 220), Image.LANCZOS), (220 * i, 0))
sheet.convert('RGB').save('icons/_sheet.jpg')
print([os.path.basename(f) for f in fs])
EOF
