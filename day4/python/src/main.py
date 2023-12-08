import collections
import functools
import math

from aoc_lube import fetch, submit


def parse(inp: str) -> list[set[str]]:
    ret: list[set[str]] = []
    lines = inp.splitlines()

    for line in lines:
        winners, yours = (set(i.strip().split()) for i in line.split(":")[1].split("|"))
        ret.append(winners.intersection(yours))

    return ret


def process_card(winners: list[set[str]], card: int) -> collections.Counter[int]:
    cards: collections.Counter[int] = collections.Counter()

    winner = winners[card]
    copies = (card + i + 1 for i in range(len(winner)))

    for copy in copies:
        cards[copy] += 1
        cards.update(process_card(winners, copy))

    return cards


def part_1(inp: str) -> int:
    winners = parse(inp)

    return sum(int(1 * math.pow(2, len(winner) - 1)) for winner in winners if winner)


def part_2(inp: str) -> int:
    winners = parse(inp)
    cards: collections.Counter[int] = collections.Counter()

    for card in range(len(winners)):
        cards[card] += 1
        cards.update(process_card(winners, card))

    return cards.total()


if __name__ == "__main__":
    raw_input = fetch(2023, 4)

    submit(2023, 4, 1, functools.partial(part_1, raw_input))
    submit(2023, 4, 2, functools.partial(part_2, raw_input))
