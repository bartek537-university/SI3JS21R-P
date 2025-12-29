import argparse
import datetime
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Final

from jinja2 import Environment, FileSystemLoader

TEMPLATE_DIRECTORY: Final[Path] = Path(__file__).parent / "../templates"
TEMPLATE_NAME: Final[str] = "report_template.j2"


class SolverResult:
    def __init__(self, file_name: str, measured_time: timedelta, unsolved_puzzle: str, solved_puzzles: list[str]):
        self.file_name = file_name
        self.measured_time = measured_time
        self.unsolved_puzzle = unsolved_puzzle
        self.solved_puzzles = solved_puzzles

    @staticmethod
    def of_file(output_file_path: str) -> SolverResult:
        with open(output_file_path) as output_file_contents:
            unsolved_puzzle, solution_count, measured_time_seconds = output_file_contents.readline().split(",")
            solved_puzzles = [output_file_contents.readline().strip() for _ in range(int(solution_count))]

        return SolverResult(
            file_name=os.path.basename(output_file_path),
            measured_time=timedelta(seconds=float(measured_time_seconds)),
            unsolved_puzzle=unsolved_puzzle,
            solved_puzzles=solved_puzzles
        )


def _is_result_file(absolute_path: str) -> bool:
    return os.path.isfile(absolute_path) and absolute_path.endswith(".txt")


def _get_output_file_paths(output_folder: Path) -> list[str]:
    paths = list[str]()

    for element_relative_path in os.listdir(output_folder):
        element_absolute_path = os.path.abspath(output_folder / element_relative_path)

        if _is_result_file(element_absolute_path):
            paths.append(element_absolute_path)

    return paths


def _render_report(environment: Environment, solver_results: list[SolverResult]) -> str:
    template = environment.get_template(TEMPLATE_NAME)

    current_datetime = datetime.now()

    datasource: object = {
        "generated_at": current_datetime.strftime("%Y-%m-%d %H:%M:%S"),
        "results": solver_results,
    }

    return template.render(datasource)


def _try_read_solver_result(output_file_path: str) -> SolverResult | None:
    try:
        return SolverResult.of_file(output_file_path)
    except Exception as exception:
        print(f"Failed to read file {output_file_path}: {type(exception).__name__}: {str(exception)}")
    return None


def _run_report_pipeline(output_folder: Path, report_path: Path) -> None:
    output_file_paths = _get_output_file_paths(output_folder)

    solver_results = [
        solver_result for output_file_path in output_file_paths
        if (solver_result := _try_read_solver_result(output_file_path)) is not None
    ]

    solver_results.sort(key=lambda solver_result: solver_result.file_name)

    environment = Environment(loader=FileSystemLoader(TEMPLATE_DIRECTORY))
    report = _render_report(environment, solver_results)

    with open(report_path, "w+") as output_file:
        output_file.write(report)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("output_folder", type=Path, help="Folder path with the solver results.")
    parser.add_argument("report_path", type=Path, help="Output file path for the generated result.")

    args = parser.parse_args()

    _run_report_pipeline(args.output_folder, args.report_path)
