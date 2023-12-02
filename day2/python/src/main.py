import functools
import math

import collections
from aoc_lube import fetch, submit


def parse(inp: str) -> dict[int, list[collections.Counter[str]]]:
    lines = (line.split(":") for line in inp.splitlines())
    games: dict[int, list[collections.Counter[str]]] = {}

    for line in lines:
        sets = (s.split(",") for s in line[1].split(";"))
        cubes: list[collections.Counter[str]] = []
        for s in sets:
            amounts: collections.Counter[str] = collections.Counter()
            for cube in s:
                amount, color = cube.strip().split()
                amounts[color] += int(amount)

            cubes.append(amounts)

        games[int(line[0].split()[1])] = cubes

    return games


def part_1(inp: str) -> int:
    games = parse(inp)
    num_cubes = collections.Counter(red=12, green=13, blue=14)

    return sum(
        game_id
        for game_id, cubes in games.items()
        if all(amounts <= num_cubes for amounts in cubes)
    )


def part_2(inp: str) -> int:
    games = parse(inp)

    return sum(
        math.prod(functools.reduce(lambda a, b: a | b, cubes).values()) for cubes in games.values()
    )


if __name__ == "__main__":
    raw_input = fetch(2023, 2)
    submit(2023, 2, 1, functools.partial(part_1, raw_input))
    submit(2023, 2, 2, functools.partial(part_2, raw_input))
