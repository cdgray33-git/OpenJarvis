#!/usr/bin/env bash
set -euo pipefail

# ── OpenJarvis Quickstart ─────────────────────────────────────────────
# One-command setup: installs deps, checks remote Ollama-compatible host,
# launches the backend API server and frontend, then opens the browser.
#
# Usage:
#   git clone https://github.com/open-jarvis/OpenJarvis.git
#   cd OpenJarvis
#   ./scripts/quickstart.sh
# ──────────────────────────────────────────────────────────────────────

BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'
BOLD='\033[1m'

info()  { echo -e "${BLUE}[info]${NC}  $*"; }
ok()    { echo -e "${GREEN}[ok]${NC}    $*"; }
warn()  { echo -e "${YELLOW}[warn]${NC}  $*"; }
fail()  { echo -e "${RED}[fail]${NC}  $*"; exit 1; }

CLEANUP_PIDS=()
cleanup() {
  echo ""
  info "Shutting down..."
  for pid in "${CLEANUP_PIDS[@]}"; do
    kill "$pid" 2>/dev/null || true
  done
  wait 2>/dev/null || true
  ok "Done."
}
trap cleanup EXIT INT TERM

# ── Navigate to repo root ────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

echo -e "${BOLD}"
echo "  ┌──────────────────────────────────┐"
echo "  │       OpenJarvis Quickstart      │"
echo "  └──────────────────────────────────┘"
echo -e "${NC}"

# ── 1. Check Python ──────────────────────────────────────────────────
info "Checking Python..."
if command -v python3 &>/dev/null; then
  PY_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
  PY_MAJOR=$(echo "$PY_VERSION" | cut -d. -f1)
  PY_MINOR=$(echo "$PY_VERSION" | cut -d. -f2)
  if [ "$PY_MAJOR" -ge 3 ] && [ "$PY_MINOR" -ge 10 ]; then
    ok "Python $PY_VERSION"
  else
    fail "Python 3.10+ required (found $PY_VERSION)"
  fi
else
  fail "Python 3 not found. Install from https://python.org"
fi

# ── 2. Check / install uv ───────────────────────────────────────────
info "Checking uv..."
if command -v uv &>/dev/null; then
  ok "uv $(uv --version 2>/dev/null | head -1)"
else
  warn "uv not found — installing..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
  ok "uv installed"
fi

# ── 3. Check Node.js ────────────────────────────────────────────────
info "Checking Node.js..."
if command -v node &>/dev/null; then
  NODE_VERSION=$(node --version)
  NODE_MAJOR=$(echo "$NODE_VERSION" | sed 's/v//' | cut -d. -f1)
  if [ "$NODE_MAJOR" -ge 18 ]; then
    ok "Node.js $NODE_VERSION"
  else
    fail "Node.js 18+ required (found $NODE_VERSION). Install from https://nodejs.org"
  fi
else
  fail "Node.js not found. Install from https://nodejs.org"
fi

# ── 4. Check remote Ollama-compatible host ───────────────────────────
OLLAMA_HOST="${OLLAMA_HOST:-http://172.16.33.200:11434}"
MODEL="${OPENJARVIS_MODEL:-qwen3.5:9b}"

info "Checking remote LLM host at $OLLAMA_HOST ..."
if curl -sf "$OLLAMA_HOST/api/tags" &>/dev/null; then
  ok "Remote Ollama-compatible host is reachable"
else
  fail "Could not reach remote LLM host at $OLLAMA_HOST"
fi

info "Using remote model setting: $MODEL"

# ── 5. Install Python dependencies ──────────────────────────────────
info "Installing Python dependencies..."
uv sync --extra server --quiet 2>/dev/null || uv sync --extra server
ok "Python dependencies installed"

# ── 6. Build Rust extension ─────────────────────────────────────────
info "Building Rust extension..."
uv run maturin develop -m rust/crates/openjarvis-python/Cargo.toml --quiet 2>/dev/null \
  || uv run maturin develop -m rust/crates/openjarvis-python/Cargo.toml
ok "Rust extension built"

# ── 7. Install frontend dependencies ────────────────────────────────
info "Installing frontend dependencies..."
(cd frontend && npm install --silent 2>/dev/null || npm install)
ok "Frontend dependencies installed"

# ── 8. Export runtime env for remote Ollama host ────────────────────
export OLLAMA_HOST="$OLLAMA_HOST"
export OPENJARVIS_MODEL="$MODEL"

# ── 9. Start backend ────────────────────────────────────────────────
info "Starting backend API server on port 8000..."
uv run jarvis serve --port 8000 &>/dev/null &
CLEANUP_PIDS+=($!)
sleep 3

if curl -sf http://localhost:8000/health &>/dev/null; then
  ok "Backend running at http://localhost:8000"
else
  warn "Backend may still be starting..."
fi

# ── 10. Start frontend ──────────────────────────────────────────────
info "Starting frontend dev server on port 5173..."
(cd frontend && npm run dev) &>/dev/null &
CLEANUP_PIDS+=($!)
sleep 3
ok "Frontend running at http://localhost:5173"

# ── 11. Open browser ────────────────────────────────────────────────
URL="http://localhost:5173"
info "Opening $URL ..."
case "$(uname -s)" in
  Darwin) open "$URL" ;;
  Linux)  xdg-open "$URL" 2>/dev/null || true ;;
  *)      true ;;
esac

echo ""
echo -e "${GREEN}${BOLD}  OpenJarvis is running!${NC}"
echo ""
echo "  Chat UI:  http://localhost:5173"
echo "  API:      http://localhost:8000"
echo "  Model:    $MODEL"
echo "  Host:     $OLLAMA_HOST"
echo ""
echo "  Press Ctrl+C to stop all services."
echo ""

wait