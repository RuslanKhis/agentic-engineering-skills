#!/bin/sh
# Mint an ID token for the Toolbox service once at start-up, then serve the agent.
set -e
TOOLBOX_TOKEN="$(curl -s -H 'Metadata-Flavor: Google' \
  "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/identity?audience=https://analytics-toolbox-6p2kq3vt4a-nw.a.run.app")"
export TOOLBOX_TOKEN
exec adk api_server --host 0.0.0.0 --port "${PORT:-8080}" .
