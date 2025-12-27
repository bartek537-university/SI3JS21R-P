from solver import Board, is_puzzle_valid, solve

if __name__ == "__main__":
    unsolved_puzzle = "210800000904000000083001000006040003000082640040000000700008200000503098698027305"
    print("Solving", unsolved_puzzle)

    unsolved_board = Board.of_string(unsolved_puzzle)
    solved_boards = solve(unsolved_board)

    for i, solved_board in enumerate(solved_boards):
        print(f"#{i}", "Valid" if is_puzzle_valid(str(solved_board)) else "Invalid", str(solved_board))
