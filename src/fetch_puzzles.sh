#!/usr/bin/env bash

readonly API_URL='xxx'

readonly DIFFICULTY_LEVELS=('xxx')
readonly PUZZLE_PER_DIFFICULTY_COUNT=3

get_puzzle() {
  local difficulty="${1:-easy}"

  if ! response=$(curl -sS -X POST "$API_URL" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    -d "{\"difficulty\":\"$difficulty\"}"); then
    echo "Failed to fetch puzzle." >&2
    return 1
  fi

  echo "$response" >&1
}

for difficulty in "${DIFFICULTY_LEVELS[@]}"; do
  for i in $(seq -f "%02g" 1 $PUZZLE_PER_DIFFICULTY_COUNT); do
    puzzle=$(get_puzzle "$difficulty" | jq -r '.puzzle')
    echo "$puzzle" > "${difficulty}_${i}.txt"
  done
done