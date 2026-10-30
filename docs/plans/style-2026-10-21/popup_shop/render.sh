#!/usr/bin/env bash
# Renders the HATCH NIGHT Starter Pack popup + Shop mockups with headless Edge (same recipe as ../render.sh).
# usage: bash render.sh [qa]      -> PNGs next to this script; qa = also print each view's containment report
cd "$(dirname "$0")"
EDGE="/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
W=$(cygpath -w "$PWD"); M=$(cygpath -m "$PWD")
shot() { # view dev out w h
  "$EDGE" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 --run-all-compositor-stages-before-draw \
    --virtual-time-budget=4000 --screenshot="$W\\$3" --window-size=$4,$5 "file:///$M/popup_shop.html?view=$1&dev=$2" >/dev/null 2>&1
  echo "rendered $3"
}
qa() { # view dev w h
  "$EDGE" --headless=new --disable-gpu --virtual-time-budget=4000 --window-size=$3,$4 --dump-dom "file:///$M/popup_shop.html?view=$1&dev=$2&qa=1" 2>/dev/null \
    | python -c "import sys,re,html; d=sys.stdin.read(); m=re.search(r\"<pre id=.qa.[^>]*>(.*?)</pre>\",d,re.S); print(html.unescape(m.group(1)) if m else \"no qa\")"
}
VIEWS_PC="popup popup_restricted popup_thanks popup_error popup_urgent shop_top shop_speed shop_potions shop_bottom shop_gift"
VIEWS_PHONE="popup popup_restricted shop_top shop_potions shop_gift"
for v in $VIEWS_PC; do shot $v pc "${v}_pc.png" 1920 1080; done
for v in $VIEWS_PHONE; do shot $v phone "${v}_phone.png" 844 390; done
shot shop_long pc shop_long.png 1180 1700
shot sheet pc sheet.png 1500 700
if [ "$1" = "qa" ]; then
  for v in $VIEWS_PC; do echo "--- QA $v pc"; qa $v pc 1920 1080; done
  for v in $VIEWS_PHONE; do echo "--- QA $v phone"; qa $v phone 844 390; done
  echo "--- QA shop_long"; qa shop_long pc 1180 1700
  echo "--- QA sheet"; qa sheet pc 1500 700
fi
