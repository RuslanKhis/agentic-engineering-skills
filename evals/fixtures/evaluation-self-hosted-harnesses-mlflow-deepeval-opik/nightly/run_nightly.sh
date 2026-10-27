#!/usr/bin/env bash
# Nightly evaluation, run by Cloud Scheduler on a Cloud Run job in harbour-support-prod.
set -euo pipefail

adk eval app eval_cases/support.evalset.json --print_detailed_results > nightly/results.txt
echo "nightly eval finished with exit code $?"
