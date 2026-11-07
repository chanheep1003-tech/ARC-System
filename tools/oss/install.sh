#!/usr/bin/env bash
# ARC-System 오픈소스 도구 설치기 (idempotent)
#   ./tools/oss/install.sh --quick   markitdown + rtk 만 (세션 시작 훅용, 수 초)
#   ./tools/oss/install.sh --full    + heretic, DeepTutor, Orkas 소스/의존성 (수 GB)
# 소스는 저장소에 커밋하지 않고 $ARC_OSS_HOME (기본 ~/.arc-oss) 에 둔다.
set -uo pipefail
MODE="${1:---quick}"
OSS_HOME="${ARC_OSS_HOME:-$HOME/.arc-oss}"
mkdir -p "$OSS_HOME" "$HOME/.local/bin"
export PATH="$HOME/.local/bin:$PATH"
log() { printf '[arc-oss] %s\n' "$*"; }

install_markitdown() {
  command -v markitdown >/dev/null && { log "markitdown ok"; return; }
  uv tool install 'markitdown[all]' >/dev/null 2>&1 || pip install -q 'markitdown[all]' && log "markitdown installed"
}
install_rtk() {
  command -v rtk >/dev/null && { log "rtk ok"; return; }
  # 릴리스 바이너리가 프록시/레이트리밋으로 막히면 Apache-2.0 에디션을 소스 빌드
  if RTK_EDITION=oss curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/refs/heads/master/install.sh | sh >/dev/null 2>&1; then
    log "rtk installed (release)"
  elif command -v cargo >/dev/null; then
    cargo install --quiet --locked --no-default-features --git https://github.com/rtk-ai/rtk --root "$HOME/.local" rtk 2>/dev/null \
      || cargo install --quiet --no-default-features --git https://github.com/rtk-ai/rtk --root "$HOME/.local" rtk
    command -v rtk >/dev/null && log "rtk installed (cargo, oss)" || log "rtk FAILED"
  else log "rtk FAILED (no cargo)"; fi
}
clone() { [ -d "$OSS_HOME/$2/.git" ] || git clone -q --depth 1 "https://github.com/$1" "$OSS_HOME/$2"; }
install_heretic() {
  command -v heretic >/dev/null && { log "heretic ok"; return; }
  uv tool install heretic-llm >/dev/null 2>&1 && log "heretic installed (GPU 없으면 실행 불가)" || log "heretic FAILED"
}
install_deeptutor() {
  clone HKUDS/DeepTutor DeepTutor || return
  cd "$OSS_HOME/DeepTutor" || return
  [ -x .venv/bin/deeptutor ] || { uv venv -q .venv && uv pip install -q --python .venv/bin/python -r requirements/full.txt && uv pip install -q --python .venv/bin/python -e . --no-deps; }
  [ -d web/node_modules ] || (cd web && npm ci --legacy-peer-deps >/dev/null 2>&1)
  log "DeepTutor ready: $OSS_HOME/DeepTutor (.venv/bin/deeptutor init && start)"
}
install_orkas() {
  clone Orkas-AI/Orkas Orkas || return
  cd "$OSS_HOME/Orkas" || return
  [ -d node_modules ] || npm ci >/dev/null 2>&1
  log "Orkas ready: $OSS_HOME/Orkas (./run.sh)"
}

install_markitdown; install_rtk
if [ "$MODE" = "--full" ]; then install_heretic; install_deeptutor; install_orkas; fi
log "done ($MODE)"
