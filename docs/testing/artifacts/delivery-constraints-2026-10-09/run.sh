#!/bin/zsh
# usage: run.sh <root> <condition> <scenario>
R="$1"; cond="$2"; j="$3"
rules=rules-headless.txt; [[ $j == D5 ]] && rules=rules-firstturn.txt
prompt="$(grep "^$j	" "$R/prompts.tsv" | cut -f2-)$(cat "$R/$rules")"
W="$R/$cond/$j"; rm -rf "$W"; mkdir -p "$W/.claude"
if [[ $j == E1 ]]; then
  cp -R "$R/fixture/." "$W/"; cp "$R/T-201.md" "$W/tickets/"
fi
cp -R "$R/skills-$cond" "$W/.claude/skills"
(cd "$W" && git init -q && git add -A && git -c user.email=t@t -c user.name=t commit -qm fixture)
cd "$W" || exit 1
start=$(date +%s)
timeout 3600 claude -p "$prompt" --model opus --setting-sources project --max-turns 150 \
  --output-format json --dangerously-skip-permissions > "$R/$cond-$j.json" 2> "$R/$cond-$j.err"
echo "$cond $j exit=$? secs=$(( $(date +%s) - start ))" >> "$R/status.log"
