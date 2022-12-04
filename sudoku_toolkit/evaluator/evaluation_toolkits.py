from ..dlx_toolkits import DLXInterface
from ..utils import SUDOKU
import sys


def parse_sudoku(sudoku) -> list:
    from copy import deepcopy
    """ parse sudoku into list
        : param sudoku: list of list, or SUDOKU
        : return sudoku_value: list
    """
    sm = sudoku.sudoku_matrix if isinstance(sudoku, SUDOKU) else sudoku
    return deepcopy(sm)


def is_valid(sudoku) -> bool:
    from math import sqrt
    """ Validate if a sudoku is valid. Assume all inputs are number.
        1. square
        2. sqrt(size) is integer
        3. numbers within range [0, size]
        ---
        : param sudoku: list of list or SUDOKU
        : return: bool
            validate if a sudoku is valid
    """
    sudoku_m = parse_sudoku(sudoku)

    size = len(sudoku_m)
    # invalid shape:
    sq_size = sqrt(size)
    if sq_size!=int(sq_size):
        return False
    max_num = 0
    min_num = 0
    for row in sudoku_m:
        # inconsistent shape
        if len(row)!=size:
            return False
        # update max
        if max_num < max(row):
            max_num = max(row)
        # update min
        if min_num < min(row):
            min_num = min(row)

    # exceed bound
    if max_num > size or min_num < 0:
        return False

    return True


def is_solvable(sudoku) -> bool:
    """ Validate if a sudoku is solvable
    """
    sudoku_m = parse_sudoku(sudoku)
    if not is_valid(sudoku_m):
        return False
    digits = list(range(1,10,1))

    def is_solvable_detector(board):
        def candidates(row, col):
            row_elem = board[row]
            col_elem = [r[col] for r in board]
            # upper-left elem in target block
            colstart, rowstart = (col//3)*3, (row//3)*3
            block_elem = [board[i][j]
                          for i in range(rowstart, rowstart + 3)
                          for j in range(colstart, colstart + 3)]
            return set(digits) - set(row_elem + col_elem + block_elem) - set([0])

        def solve(ix=0):
            """ Solve the sudoku recursively.
                Assume all other indecies<ix is solvable.
                If we move ix=81, the mat is solved, otherwise, we iterate all elems.
                If current cube has no clue, we iterate on all candidate values.
                    If unsolvable, we reset that value to zero, and mark as unsolvable.
                    If solvable, we move on to next ix.
                Otherwise, he current cube has clue, we move to next ix.
                Otherwise, the quiz do not have solution, we mark it as unsolvable.
            """
            if ix == 81:
                return True
            row, col = ix//9, ix % 9
            # if current hover on missing cube
            if board[row][col] == 0:
                # print(candidates(row, col))
                for val in candidates(row, col):
                    board[row][col] = val
                    if solve(ix+1):
                        return True
                    board[row][col] = 0
            # if current hover on clue
            else:
                if solve(ix+1):
                    return True
            return False

        if solve():
            # print(board)
            return True
        else:
            return False
        # return solve()

    return is_solvable_detector(sudoku_m)


def is_multi_sol(sudoku) -> bool:
    s = DLXInterface()
    return s.return_if_multi_sol(sudoku)


def solution_num(sudoku) -> int:
    s = DLXInterface()
    return s.return_sol_num(sudoku)


def print_solution_report(sudoku) -> None:
    """ Validate if a sudoku is solvable, and if it has unique solution if solvable.
        : param sudoku: SUDOKU | list
    """
    sudoku_m = parse_sudoku(sudoku)
    # valid sudoku examinne
    if not is_valid(sudoku_m):
        print('Sudoku under examinination is not valid...')
    else:
        print('Sudoku is valid...')
        if not is_solvable(sudoku_m):
            print('Sudoku under examination is not solvable...')
        else:
            print('Sudoku is solvable...')
            if not is_multi_sol(sudoku_m):
                print('Sudoku has one unique solution')
            else:
                print(f'Sudoku has multiple solutions, to be specific, {solution_num(sudoku_m)} in all.')


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) < 1:
        print("Please provide a sudoku as a file or plain text...")
    else:
        for arg in args:
            if arg[-4:] == ".txt":
                s = []
                with open(arg, "r") as f:
                    for line in f.readlines():
                        s.append([int(d) for d in [c for c in line] if d.isdigit()])
                #
                print(is_multi_sol(s))
                #
            else:
                print("Please Provide a .txt file...")
