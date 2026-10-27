#!/usr/bin/env bash
# Run the pinned MCP conformance suite against the exposed server for one spec revision.
#   ci/conformance.sh 2026-07-28            (CONFORMANCE_VERSION overrides ci/conformance.version)
# Exit 0: every failure is in the baseline. Exit 1: unexpected failure OR stale baseline entry.
# A baseline still carrying the "# UNSEEDED" marker runs in record mode (never fails, artifacts only).
set -euo pipefail

rev="${1:?usage: ci/conformance.sh <2025-11-25|2026-07-28>}"
here="$(cd "$(dirname "$0")" && pwd)"
version="${CONFORMANCE_VERSION:-$(tr -d '[:space:]' < "$here/conformance.version")}"
baseline="$here/conformance-baseline-$rev.yml"
port="${PORT:-8765}"
out="$here/out/$rev"
mkdir -p "$out"

PORT="$port" python -m tests.conformance_server > "$out/server.log" 2>&1 &
server_pid=$!
trap 'kill "$server_pid" 2>/dev/null || true' EXIT

python - "$port" <<'PY'
import socket, sys, time
for _ in range(60):
    try:
        socket.create_connection(("127.0.0.1", int(sys.argv[1])), 0.5).close(); sys.exit(0)
    except OSError:
        time.sleep(0.5)
sys.exit("server did not start; see server.log")
PY

echo "conformance @modelcontextprotocol/conformance@$version, requirements $rev"
cmd=(npx -y "@modelcontextprotocol/conformance@$version" server
     --url "http://127.0.0.1:$port/mcp" --requirements "$rev" -o "$out")

if grep -q '^# UNSEEDED' "$baseline"; then
  echo "::warning::$baseline is UNSEEDED: recording only, this run does not gate. Seed it from $out and remove the marker."
  "${cmd[@]}" || true
else
  "${cmd[@]}" --expected-failures "$baseline"
fi
