import argparse
import os
import shutil
import sys
from pathlib import Path


def _is_report_file(absolute_path: str) -> bool:
    return os.path.isfile(absolute_path) and absolute_path.endswith(".html")


def _get_reports_to_back_up(report_folder: Path, backup_folder: Path) -> list[tuple[str, str]]:
    paths = list[tuple[str, str]]()

    for report_file_name in os.listdir(report_folder):
        report_file_path = os.path.abspath(report_folder / report_file_name)

        if not _is_report_file(report_file_path):
            continue

        backup_file_path = os.path.abspath(backup_folder / report_file_name)

        if os.path.exists(backup_file_path):
            continue

        paths.append((report_file_path, backup_file_path))

    return paths


def _run_backup_pipeline(report_folder: Path, backup_folder: Path) -> None:
    try:
        files_to_backup = _get_reports_to_back_up(report_folder, backup_folder)

        for i, (source_path, destination_path) in enumerate(files_to_backup):
            print(f"Backing up {i + 1}/{len(files_to_backup)}...\r", end="")
            shutil.copy2(source_path, destination_path)

    except Exception as exception:
        print(exception)
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("report_folder", type=Path, help="Folder path with the solver results.")
    parser.add_argument("backup_folder", type=Path, help="Output file path for the generated result.")

    args = parser.parse_args()

    _run_backup_pipeline(args.report_folder, args.backup_folder)
