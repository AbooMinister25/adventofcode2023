import functools

from more_itertools import substrings_indexes
from aoc_lube import fetch, submit


def part_1(inp: str) -> int:
    lines = inp.splitlines()
    digits = ["".join(i for i in line if i.isdigit()) for line in lines]
    return sum((int(d[0] + d[-1]) for d in digits))


def part_2(inp: str) -> int:
    lines = inp.splitlines()
    numbers = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }

    ret = 0

    for line in lines:
        substrings = (
            "".join(i[0])
            for i in sorted(substrings_indexes(line), key=lambda t: t[1])
            if len(i) <= 5
        )
        digits = [i for i in substrings if i.isdigit() or i in numbers]

        first = digits[0] if len(digits[0]) < 2 else numbers[digits[0]]
        last = digits[-1] if len(digits[-1]) < 2 else numbers[digits[-1]]

        ret += int(first + last)

    return ret


if __name__ == "__main__":
    raw_input = fetch(2023, 1)
    part_2(raw_input)
    submit(2023, 1, 1, functools.partial(part_1, raw_input))
    submit(2023, 1, 2, functools.partial(part_2, raw_input))
