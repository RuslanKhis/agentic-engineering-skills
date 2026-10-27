#!/bin/sh
# The agent authenticates to the managed BigQuery MCP server as its own service account (see
# analytics/agent.py); there is no token to mint here.
set -e
exec adk api_server --host 0.0.0.0 --port "${PORT:-8080}" .
