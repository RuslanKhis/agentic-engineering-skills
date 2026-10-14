#!/bin/zsh
# usage: run.sh <root> <condition> <scenario>
R="$1"; cond="$2"; j="$3"
prompt="$(grep "^$j	" "$R/prompts.tsv" | cut -f2-)

$(cat "$R/rules-headless.txt")"
W="$R/$cond/$j"; rm -rf "$W"; mkdir -p "$W/.claude"
cp -R "$R/skills-$cond" "$W/.claude/skills"
(cd "$W" && git init -q && git add -A && git -c user.email=t@t -c user.name=t commit -qm fixture)
cd "$W" || exit 1
start=$(date +%s)
timeout 3600 claude -p "$prompt" --model opus --setting-sources project --max-turns 150 \
  --output-format json --dangerously-skip-permissions > "$R/$cond-$j.json" 2> "$R/$cond-$j.err"
echo "$cond $j turn1 exit=$? secs=$(( $(date +%s) - start ))" >> "$R/status.log"
if [[ $j == K1 ]]; then
  sid=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['session_id'])" "$R/$cond-$j.json")
  update="Update from the user: we just learned that asset rights also depend on territory, flight dates and whether the creative may be modified. Revise the design and plan for this, and append what changed to REPORT.md. The same session rules apply."
  timeout 3600 claude -p "$update" --resume "$sid" --model opus --setting-sources project --max-turns 100 \
    --output-format json --dangerously-skip-permissions > "$R/$cond-$j-turn2.json" 2> "$R/$cond-$j-turn2.err"
  echo "$cond $j turn2 exit=$? secs=$(( $(date +%s) - start ))" >> "$R/status.log"
fi
