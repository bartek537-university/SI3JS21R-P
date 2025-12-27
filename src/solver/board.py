import copy

import numpy as np

Position = tuple[int, int]


def _align_start(value: int, grid_size: int) -> int:
    return (value // grid_size) * grid_size


class Board:
    def __init__(self):
        self._values = np.zeros(shape=(9, 9), dtype=int)
        self._candidates = np.vectorize(lambda _: {*range(1, 10)})(np.empty(shape=(9, 9), dtype=object))

    @staticmethod
    def _is_puzzle_valid(puzzle: str) -> bool:
        if len(puzzle) != 81:
            return False
        if any(not char.isdigit() for char in puzzle):
            return False
        return True

    @staticmethod
    def of_string(puzzle: str) -> Board:
        if not Board._is_puzzle_valid(puzzle):
            raise ValueError("Invalid board format.")

        board = Board()

        for i, value in enumerate(puzzle):
            if value == "0":
                continue
            board.place(int(value), position=(i % 9, i // 9))

        return board

    def get_value(self, position: Position) -> int:
        x, y = position

        assert 0 <= x < 9 and 0 <= y < 9, "The position is out of range."

        return self._values[y, x]

    def get_candidates(self, position: Position) -> set[int]:
        x, y = position

        assert 0 <= x < 9 and 0 <= y < 9, "The position is out of range."

        return self._candidates[y, x]

    @staticmethod
    def _get_peers(position: Position) -> set[Position]:
        x, y = position
        peers = set[Position]()

        for i in range(9):
            peers.add((x, i))
            peers.add((i, y))

        bx, by = _align_start(x, 3), _align_start(y, 3)

        for i in range(3):
            for j in range(3):
                peers.add((bx + i, by + j))

        peers.remove((x, y))

        return peers

    def place(self, value: int, position: Position) -> None:
        x, y = position

        assert 0 <= x < 9 and 0 <= y < 9, "The position is out of range."
        assert self._values[y, x] == 0, "The tile is occupied."
        assert 1 <= value <= 9, "The value is out of range."

        assert value in self._candidates[y, x], "The value appears multiple times in the same region."

        self._values[y, x] = value
        self._candidates[y, x].clear()

        for px, py in self._get_peers(position):
            if value not in self._candidates[py, px]:
                continue
            self._candidates[py, px].remove(value)

    def is_solved(self) -> bool:
        return np.all(self._values != 0)

    def copy(self) -> Board:
        return copy.deepcopy(self)

    def __hash__(self):
        return hash(tuple(self._values.reshape((81,))))

    def __str__(self) -> str:
        return "".join(str(value) for value in self._values.reshape((81,)))
