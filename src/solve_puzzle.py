import argparse
import pathlib
import sys
from datetime import datetime, timedelta
from typing import Callable

from solver import Board, is_puzzle_valid, solve


def _measure_time[T](f: Callable[[], T]) -> tuple[T, timedelta]:
    start = datetime.now()
    result = f()
    end = datetime.now()
    return result, end - start


def _run_solve_pipeline(input_path: pathlib.Path, output_path: pathlib.Path) -> None:
    try:
        with open(input_path) as input_file:
            unsolved_puzzle = input_file.read()

        unsolved_board = Board.of_string(unsolved_puzzle)
        solutions, measured_time = _measure_time(lambda: solve(unsolved_board))

        with open(output_path, "w+") as output_file:
            output_file.write(f"{len(solutions)},{measured_time.total_seconds()}\n")
            for solution in solutions:
                is_solution_valid = is_puzzle_valid(str(solution))
                output_file.write(f"{solution},{int(is_solution_valid)}\n")

    except FileNotFoundError as error:
        print(error)
        sys.exit(2)
    except Exception as exception:
        print(exception)
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("input_path", type=pathlib.Path, help="The input file path for an unsolved puzzle.")
    parser.add_argument("output_path", type=pathlib.Path, help="The output file path for the solved puzzle.")

    args = parser.parse_args()

    _run_solve_pipeline(args.input_path, args.output_path)
