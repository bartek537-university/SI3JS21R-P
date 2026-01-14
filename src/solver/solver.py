import copy

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


def _find_hidden_single(board: Board, positions: list[Position]) \
        -> list[tuple[int, Position]]:
    counts = [0] * 10
    history: list[Position | None] = [None] * 10

    for position in positions:
        if board.get_value(position) != 0:
            continue
        for candidate in board.get_candidates(position):
            counts[candidate] += 1
            history[candidate] = position

    hidden_singles: list[tuple[int, Position]] = []

    for value in range(1, 10):
        if counts[value] != 1:
            continue
        position = history[value]
        hidden_singles.append((value, position))

    return hidden_singles


def _find_hidden_singles(board: Board) -> list[tuple[int, Position]]:
    hidden_singles: set[tuple[int, Position]] = set()

    for y in range(9):
        row_positions = [(x, y) for x in range(9)]
        hidden_singles.update(_find_hidden_single(board, row_positions))

    for x in range(9):
        column_positions = [(x, y) for y in range(9)]
        hidden_singles.update(_find_hidden_single(board, column_positions))

    for bx in range(0, 9, 3):
        for by in range(0, 9, 3):
            block_positons = [(bx + i, by + j) for i in range(3) for j in range(3)]
            hidden_singles.update(_find_hidden_single(board, block_positons))

    return list(hidden_singles)


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
    while True:
        naked_singles = _find_naked_singles(board)

        for value, position in naked_singles:
            if value not in board.get_candidates(position):
                return []
            board.place(value, position)

        hidden_singles = _find_hidden_singles(board)

        for value, position in hidden_singles:
            if value not in board.get_candidates(position):
                return []
            board.place(value, position)

        if len(naked_singles) == 0 and len(hidden_singles) == 0:
            break

    if board.is_solved():
        return [board]

    solutions = []
    pivot_position = _find_pivot_position(board)

    for candidate in board.get_candidates(pivot_position):
        assumed_board = copy.deepcopy(board)
        assumed_board.place(candidate, pivot_position)
        solutions.extend(__internal_solve(assumed_board))

    return solutions


def solve(unsolved: Board) -> list[Board]:
    return list(set(__internal_solve(unsolved.copy())))
