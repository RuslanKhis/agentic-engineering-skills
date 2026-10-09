#!/bin/zsh
# usage: batch.sh <root> <condition> <scenarios...>; three at a time
R="$1"; cond="$2"; shift 2
for j in "$@"; do
  "$R/run.sh" "$R" "$cond" "$j" &
  while (( $(jobs -r | wc -l) >= 3 )); do sleep 5; done
done
wait
