import numpy as np
import numpy.typing as nt

def _is_sequence_valid(sequence: nt.NDArray[int]) -> bool:
    present_values = set[int]()

    for current_value in sequence.reshape((9,)):
        if current_value in present_values:
            return False
        present_values.add(current_value)

    return True


def is_puzzle_valid(puzzle: str) -> bool:
    if len(puzzle) != 81:
        return False
    if any(char not in "123456789" for char in puzzle):
        return False

    board = np.array([*map(int, puzzle)]).reshape((9, 9))

    for row in board:
        if not _is_sequence_valid(row):
            return False

    for column in board.T:
        if not _is_sequence_valid(column):
            return False

    for y, x in np.ndindex((3, 3)):
        bx, by = x * 3, y * 3
        box = board[by:by + 3, bx:bx + 3]

        if not _is_sequence_valid(box):
            return False

    return True