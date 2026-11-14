#!/usr/bin/env bash
# Install the fonts the PDF renderer needs (Nanum Myeongjo/Gothic + a CJK fallback for Hanja).
# 1) apt with retries; 2) if the Ubuntu mirrors are unreachable, the same OFL fonts from github.com/google/fonts.
set -uo pipefail
NANUM=/usr/share/fonts/truetype/nanum
FALLBACK=/usr/share/fonts/truetype/arc-fallback
USER_NANUM="${HOME:-/tmp}/.local/share/fonts/nanum"
USER_FALLBACK="${HOME:-/tmp}/.local/share/fonts/arc-fallback"
SUDO=""
if [ "$(id -u)" -ne 0 ]; then
  if sudo -n true >/dev/null 2>&1; then SUDO="sudo -n"
  else NANUM="$USER_NANUM"; FALLBACK="$USER_FALLBACK"; fi
fi
have_nanum() {
  for d in /usr/share/fonts/truetype/nanum "$USER_NANUM"; do
    ok=1
    for f in NanumMyeongjo NanumMyeongjoBold NanumGothic NanumGothicBold; do [ -s "$d/$f.ttf" ] || { ok=0; break; }; done
    [ "$ok" -eq 1 ] && return 0
  done
  return 1
}
have_cjk() { [ -s /usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc ] || [ -s /usr/share/fonts/truetype/wqy/wqy-zenhei.ttc ] || [ -s "/usr/share/fonts/truetype/arc-fallback/NotoSerifKR.ttf" ] || [ -s "$USER_FALLBACK/NotoSerifKR.ttf" ]; }

if [ -n "$SUDO" ] || [ "$(id -u)" -eq 0 ]; then
  for attempt in 1 2 3; do
    have_nanum && have_cjk && break
    $SUDO apt-get update -q -o Acquire::Retries=3 >/dev/null 2>&1
    $SUDO apt-get install -y -q -o Acquire::Retries=3 -o DPkg::Lock::Timeout=60 fonts-nanum fonts-wqy-zenhei fonts-noto-cjk >/dev/null 2>&1 && break
    echo "apt attempt $attempt failed"; sleep $((attempt * 10))
  done
fi

BASE=https://raw.githubusercontent.com/google/fonts/main/ofl
fetch() { $SUDO curl -fsSL --retry 4 --retry-delay 3 -o "$2" "$1" && [ -s "$2" ]; }
if ! have_nanum; then
  echo "apt unavailable: fetching Nanum fonts from google/fonts into $NANUM"
  $SUDO mkdir -p "$NANUM"
  fetch "$BASE/nanummyeongjo/NanumMyeongjo-Regular.ttf" "$NANUM/NanumMyeongjo.ttf"
  fetch "$BASE/nanummyeongjo/NanumMyeongjo-Bold.ttf" "$NANUM/NanumMyeongjoBold.ttf"
  fetch "$BASE/nanumgothic/NanumGothic-Regular.ttf" "$NANUM/NanumGothic.ttf"
  fetch "$BASE/nanumgothic/NanumGothic-Bold.ttf" "$NANUM/NanumGothicBold.ttf"
fi
if ! have_cjk; then
  echo "apt unavailable: fetching CJK fallback from google/fonts into $FALLBACK"
  $SUDO mkdir -p "$FALLBACK"
  fetch "$BASE/notoserifkr/NotoSerifKR%5Bwght%5D.ttf" "$FALLBACK/NotoSerifKR.ttf"
fi
have_nanum && have_cjk && { echo "fonts ready"; exit 0; }
echo "FONT INSTALL FAILED"; exit 1
