import numpy as np

from .board import Board

Position = tuple[int, int]


def _find_naked_singles(board: Board) -> list[tuple[int, Position]]:
    naked_singles: list[tuple[int, Position]] = []

    for position in np.ndindex((9, 9)):
        candidates = board.get_candidates(position)

        if len(candidates) == 1:
            naked_singles.append((list(candidates)[0], position))

    return naked_singles


def _find_pivot_position(board: Board) -> Position:
    pivot_position: Position = (0, 0)

    for current_position in np.ndindex((9, 9)):
        pivot_cell_candidates = board.get_candidates(pivot_position)
        current_cell_candidates = board.get_candidates(current_position)

        if len(current_cell_candidates) == 0:
            continue

        if len(pivot_cell_candidates) == 0 or len(pivot_cell_candidates) > len(current_cell_candidates):
            pivot_position = current_position

    return pivot_position


def __internal_solve(board: Board) -> list[Board]:
    while naked_singles := _find_naked_singles(board):
        for value, position in naked_singles:
            # Prevent filling cells with the only candidate removed during the current iteration.
            if len(board.get_candidates(position)) < 1:
                return []

            board.place(value, position)

    if board.is_solved():
        return [board]

    solutions = []
    pivot_position = _find_pivot_position(board)

    for candidate in board.get_candidates(pivot_position):
        (assumed_board := board.copy()).place(candidate, pivot_position)
        solutions.extend(__internal_solve(assumed_board))

    return solutions


def solve(unsolved: Board) -> list[Board]:
    return list(set(__internal_solve(unsolved.copy())))
