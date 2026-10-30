#!/usr/bin/env bash
# Renders the style mockups with headless Edge.  usage: bash render.sh [A|B|all] [qa]
# Output: <name>_pc.png (1920x1080) and <name>_phone.png (844x390) next to this script; qa = print the containment report.
cd "$(dirname "$0")"
EDGE="/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
W=$(cygpath -w "$PWD"); M=$(cygpath -m "$PWD")
shot() { # html dev state out w h
  "$EDGE" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 --run-all-compositor-stages-before-draw \
    --virtual-time-budget=3000 --screenshot="$W\\$4" --window-size=$5,$6 "file:///$M/$1?dev=$2&state=$3" >/dev/null 2>&1
  echo "rendered $4"
}
qa() { # html dev state
  "$EDGE" --headless=new --disable-gpu --virtual-time-budget=3000 --window-size=$4,$5 --dump-dom "file:///$M/$1?dev=$2&state=$3&qa=1" 2>/dev/null \
    | python -c "import sys,re,html; d=sys.stdin.read(); m=re.search(r\"<pre id=.qa.[^>]*>(.*?)</pre>\",d,re.S); print(html.unescape(m.group(1)) if m else \"no qa\")"
}
run() { # html name
  shot "$1" pc mid "$2_pc.png" 1920 1080
  shot "$1" phone next "$2_phone.png" 844 390
  shot "$1" "pc&view=sheet" mid "$2_sheet.png" 1500 1025
  if [ "$QA" = "qa" ]; then
    echo "--- QA $2 pc/mid";   qa "$1" pc mid 1920 1080
    echo "--- QA $2 phone/next"; qa "$1" phone next 844 390
  fi
}
QA=$2
case "${1:-all}" in
  A) run dirA_studbox.html A_studbox ;;
  B) run dirB_hatchnight.html B_hatchnight ;;
  all) run dirA_studbox.html A_studbox; run dirB_hatchnight.html B_hatchnight ;;
esac
