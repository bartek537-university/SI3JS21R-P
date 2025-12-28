#!/usr/bin/env bash

readonly input_dir='./data/input'
readonly output_dir='./data/output'
readonly report_dir='./data/reports'
readonly backup_dir='./data/backups'

readonly solver_prog=(python3 './src/solve_puzzle.py')

create_backup() {
  printf "Creating backup...\n"
}

solve_puzzles() {
  printf "Starting Sudoku solver...\n"

  input_files=("$input_dir"/*.txt)
  input_file_count="${#input_files[@]}"

  files_processed=0

  for input_file in "${input_files[@]}"; do
    printf "Solving %d/%d...\r" $((files_processed+1)) "$input_file_count"

    file_name=$(basename "$input_file")
    output_file="$output_dir/$file_name"

    "${solver_prog[@]}" "$input_file" "$output_file"

    ((files_processed++))
  done
}

create_report() {
  printf "Creating report...\n"
}

open_report() {
  printf "Opening report in the default browser...\n"
}

create_backup
solve_puzzles
create_report
open_report