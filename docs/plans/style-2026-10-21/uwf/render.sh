#!/usr/bin/env bash
# Renders the HATCH NIGHT Upgrades / Welcome Back / Free Gift mockups with headless Edge (same recipe as ../ris/render.sh).
# usage: bash render.sh [qa]      -> PNGs next to this script; qa = also write each view's containment report to qa_report.txt
cd "$(dirname "$0")"
EDGE="/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
W=$(cygpath -w "$PWD"); M=$(cygpath -m "$PWD")
shot() { # view dev out w h [page]
  "$EDGE" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 --run-all-compositor-stages-before-draw \
    --virtual-time-budget=4000 --screenshot="$W\\$3" --window-size=$4,$5 "file:///$M/${6:-uwf.html}?view=$1&dev=$2" >/dev/null 2>&1
  echo "rendered $3"
}
qa() { # view dev w h
  "$EDGE" --headless=new --disable-gpu --virtual-time-budget=4000 --window-size=$3,$4 --dump-dom "file:///$M/uwf.html?view=$1&dev=$2&qa=1" 2>/dev/null \
    | python -c "import sys,re,html; d=sys.stdin.read(); m=re.search(r\"<pre id=.qa.[^>]*>(.*?)</pre>\",d,re.S); print(html.unescape(m.group(1)) if m else \"no qa\")"
}
VIEWS_PC="freegift freegift_joined freegift_claimed freegift_refusal welcome welcome_big welcome_x5 welcome_refusal upgrades upgrades_free upgrades_step10 upgrades_max upgrades_refusal sheet"
VIEWS_PHONE="freegift_joined welcome upgrades upgrades_free"
VIEWS_1050="freegift welcome upgrades"
VIEWS_667="freegift welcome upgrades"
for v in $VIEWS_PC; do shot $v pc "${v}_pc.png" 1920 1080; done
for v in $VIEWS_PHONE; do shot $v phone "${v}_phone.png" 844 390; done
for v in $VIEWS_1050; do shot $v pc1050 "${v}_1050.png" 1050 620; done
for v in $VIEWS_667; do shot $v phone667 "${v}_667.png" 667 375; done
# the CURRENT Upgrades window (no capture exists: a reconstruction from UpgradeClient's numbers, Studio 1519 x 753)
"$EDGE" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 --run-all-compositor-stages-before-draw \
  --virtual-time-budget=4000 --screenshot="$W\\current_upgrades_1519.png" --window-size=1519,753 "file:///$M/current_upgrades.html" >/dev/null 2>&1
echo "rendered current_upgrades_1519.png"
if [ "$1" = "qa" ]; then
  {
    for v in $VIEWS_PC; do echo "--- QA $v pc"; qa $v pc 1920 1080; done
    for v in $VIEWS_PHONE; do echo "--- QA $v phone"; qa $v phone 844 390; done
    for v in $VIEWS_1050; do echo "--- QA $v 1050"; qa $v pc1050 1050 620; done
    for v in $VIEWS_667; do echo "--- QA $v 667"; qa $v phone667 667 375; done
  } > qa_report.txt
  cat qa_report.txt
fi
