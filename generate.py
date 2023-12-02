"""
Cookiecutter script for generating the solution structure for each day.
"""
import argparse
import pathlib
import subprocess


PYTHON_FILE_TEMPLATE = """import more_itertools
from aoc_lube import fetch, submit


def part_1() -> None:
    ...


def part_2() -> None:
    ...


if __name__ == "__main__":
    raw_input = fetch(2022, 3)
"""


parser = argparse.ArgumentParser(
    "generator", description="Generates the structure for a specific day's aoc solution."
)
parser.add_argument("day", type=int)


def generate(day: int) -> None:
    path = pathlib.Path(f"day{day}")
    path.mkdir(parents=True, exist_ok=True)

    rust_path = path / f"day{day}_rust"
    python_path = path / f"day{day}_python"

    rust_path.mkdir(parents=True, exist_ok=True)
    python_path.mkdir(parents=True, exist_ok=True)

    subprocess.run(["cargo", "init"], cwd=rust_path)

    python_src_path = python_path / "src"
    python_src_path.mkdir(parents=True, exist_ok=True)
    python_file_path = python_src_path / "main.py"

    with open(python_file_path, "w+") as f:
        f.write(PYTHON_FILE_TEMPLATE.format(day=day))

    print("Generated structure.")


if __name__ == "__main__":
    args = parser.parse_args()
    generate(args.day)
