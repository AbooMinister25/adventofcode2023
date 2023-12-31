from __future__ import annotations

import enum
import functools

from dataclasses import dataclass, field
import math
import typing

from aoc_lube import fetch, submit


class GridType(enum.Enum):
    NUMBER = enum.auto()
    SYMBOL = enum.auto()
    PERIOD = enum.auto()


@dataclass
class GridItem:
    value: str
    row: int
    span: tuple[int, int]
    touching: list[int] = field(default_factory=list)


def parse(inp: str) -> tuple[list[GridItem], list[list[str]]]:
    row = 0

    symbols = {"$", "%", "=", "*", "&", "+", "/", "@", "#", "-"}
    lines = inp.splitlines()
    ret: list[GridItem] = []

    for line in lines:
        col = 0
        while col < len(line):
            current = line[col]
            match current:
                case current if current.isdecimal():
                    acc = ""
                    start = col

                    while current.isdecimal():
                        acc += current
                        col += 1
                        if col >= len(line):
                            break
                        current = line[col]

                    ret.append(GridItem(acc, row, (start, col)))
                case c if c in symbols:
                    ret.append(GridItem(c, row, (col, col + 1)))
                    col += 1
                case c:
                    ret.append(GridItem(c, row, (col, col + 1)))
                    col += 1

        row += 1

    return ret, [list(line) for line in lines]


def find_neighbors(grid: list[list[str]], row: int, column: int) -> list[GridItem]:
    offsets = ((0, 1), (0, -1), (1, 0), (-1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1))
    neighbors: list[GridItem] = []

    for r, c in offsets:
        n_row = row + r
        n_col = column + c
        if n_row >= 0 and n_col >= 0 and n_row < len(grid) and n_col < len(grid[0]):
            neighbor = grid[n_row][n_col]
            n = GridItem(neighbor, n_row, (n_col, n_col + 1))
            neighbors.append(n)

    return neighbors


def touching_symbol(grid: list[list[str]], item: GridItem) -> tuple[bool, GridItem | None]:
    symbols = {"$", "%", "=", "*", "&", "+", "/", "@", "#", "-"}

    for i in range(*item.span):
        neighbors = find_neighbors(grid, item.row, i)
        touching = [n for n in neighbors if n.value in symbols]
        if touching:
            return True, touching[0]

    return False, None


def part_1(inp: str) -> int:
    items, grid = parse(inp)
    numbers: list[int] = []

    numbers = [
        int(item.value)
        for item in items
        if item.value.isdecimal() and touching_symbol(grid, item)[0]
    ]

    return sum(numbers)


def part_2(inp: str) -> int:
    items, grid = parse(inp)

    for item in items:
        if item.value.isdecimal():
            touching = touching_symbol(grid, item)

            if touching[0] and touching[1].value == "*":  # type: ignore
                sym = typing.cast(GridItem, touching[1])
                num = next(i for i in items if i.row == sym.row and i.span[0] == sym.span[0])
                num.touching.append(int(item.value))

    gears = [i.touching for i in items if len(i.touching) == 2]
    return sum(math.prod(i) for i in gears)


if __name__ == "__main__":
    raw_input = fetch(2023, 3)
    submit(2023, 3, 1, functools.partial(part_1, raw_input))
    submit(2023, 3, 2, functools.partial(part_2, raw_input))
