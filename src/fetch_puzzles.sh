#!/usr/bin/env bash

readonly API_URL='xxx'

readonly DIFFICULTY_LEVELS=('xxx')
readonly PUZZLE_PER_DIFFICULTY_COUNT=3

if [ -z "$1" ]; then
  printf "Output directory path not specified.\n" >&2
  exit 1
fi
if [ ! -d "$1" ]; then
  printf "The specified path does not exist or is not a directory.\n" >&2
  exit 1
fi

get_puzzle() {
  local difficulty="${1:-easy}"

  if ! response=$(curl -sS -X POST "$API_URL" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    -d "{\"difficulty\":\"$difficulty\"}"); then
    printf "Failed to fetch puzzle." >&2
    return 1
  fi

  printf "%s" "$response"
}

puzzle_index=0

for difficulty in "${DIFFICULTY_LEVELS[@]}"; do
  for _ in $(seq "$PUZZLE_PER_DIFFICULTY_COUNT"); do
    printf -v file_name "%02d_%s.txt" $puzzle_index "$difficulty"
    get_puzzle "$difficulty" | jq -r ".puzzle" > "$1"/"$file_name"

    ((puzzle_index++))
  done
done