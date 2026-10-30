#!/usr/bin/env bash
# Renders the HATCH NIGHT Rebirth / Index / Settings mockups with headless Edge (same recipe as ../popup_shop/render.sh).
# usage: bash render.sh [qa]      -> PNGs next to this script; qa = also print each view's containment report
cd "$(dirname "$0")"
EDGE="/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
W=$(cygpath -w "$PWD"); M=$(cygpath -m "$PWD")
shot() { # view dev out w h
  "$EDGE" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 --run-all-compositor-stages-before-draw \
    --virtual-time-budget=4000 --screenshot="$W\\$3" --window-size=$4,$5 "file:///$M/ris.html?view=$1&dev=$2" >/dev/null 2>&1
  echo "rendered $3"
}
qa() { # view dev w h
  "$EDGE" --headless=new --disable-gpu --virtual-time-budget=4000 --window-size=$3,$4 --dump-dom "file:///$M/ris.html?view=$1&dev=$2&qa=1" 2>/dev/null \
    | python -c "import sys,re,html; d=sys.stdin.read(); m=re.search(r\"<pre id=.qa.[^>]*>(.*?)</pre>\",d,re.S); print(html.unescape(m.group(1)) if m else \"no qa\")"
}
VIEWS_PC="settings settings_off index index_claim rebirth rebirth_ready rebirth_need rebirth_confirm rebirth_max"
VIEWS_PHONE="settings index rebirth_need"
VIEWS_1050="settings index rebirth_need"
for v in $VIEWS_PC; do shot $v pc "${v}_pc.png" 1920 1080; done
for v in $VIEWS_PHONE; do shot $v phone "${v}_phone.png" 844 390; done
for v in $VIEWS_1050; do shot $v pc1050 "${v}_1050.png" 1050 620; done
if [ "$1" = "qa" ]; then
  for v in $VIEWS_PC; do echo "--- QA $v pc"; qa $v pc 1920 1080; done
  for v in $VIEWS_PHONE; do echo "--- QA $v phone"; qa $v phone 844 390; done
  for v in $VIEWS_1050; do echo "--- QA $v 1050"; qa $v pc1050 1050 620; done
fi
