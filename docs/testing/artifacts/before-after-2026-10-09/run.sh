#!/bin/zsh
R="$1"; cond="$2"; j="$3"
prompt="$(grep "^$j	" "$R/prompts.tsv" | cut -f2-)$(cat "$R/friction.txt")"
cd "$R/$cond/$j" || exit 1
start=$(date +%s)
timeout 3600 claude -p "$prompt" --model opus --setting-sources project --max-turns 150 \
  --output-format json --dangerously-skip-permissions > "$R/$cond-$j.json" 2> "$R/$cond-$j.err"
echo "$cond $j exit=$? secs=$(( $(date +%s) - start ))" >> "$R/status.log"
