#!/usr/bin/env bash
# Start the research MCP server on loopback and run the pinned conformance suite per revision.
# Usage: scripts/conformance.sh [CONFORMANCE_PKG]   (default: the version in conformance/PINS.json)
# Env: REVISIONS="2026-07-28 2025-11-25"  BASELINES=1 (use baselines; set 0 to just report)
set -euo pipefail
cd "$(dirname "$0")/.."
PKG="${1:-$(python -c 'import json;print(json.load(open("conformance/PINS.json"))["conformance_package"])')}"
PORT="${PORT:-8765}"
OUT="${OUT:-conformance-out}"
mkdir -p "$OUT"
PORT=$PORT python -m research.mcp_server > "$OUT/server.log" 2>&1 &
SERVER=$!
trap 'kill $SERVER 2>/dev/null || true' EXIT
for _ in $(seq 1 60); do
  (exec 3<>/dev/tcp/127.0.0.1/$PORT) 2>/dev/null && break
  kill -0 $SERVER 2>/dev/null || { cat "$OUT/server.log"; echo "server died" >&2; exit 1; }
  sleep 0.5
done
status=0
for rev in ${REVISIONS:-2026-07-28 2025-11-25}; do
  args=(server --url "http://127.0.0.1:$PORT/mcp" --requirements "$rev" -o "$OUT/$rev")
  [ "${BASELINES:-1}" = 1 ] && args+=(--expected-failures "conformance/baseline-$rev.yml")
  echo "== conformance $PKG $rev"
  npx -y "$PKG" "${args[@]}" || status=1
done
exit $status
