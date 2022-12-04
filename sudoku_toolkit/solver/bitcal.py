from ..utils import SUDOKU
from ._solver import SudokuSolver
from copy import deepcopy
import sys

class BitcalSolver(SudokuSolver):
    def __init__(self, matrix, rows='ABCDEFGHI', cols='123456789', stage=3):
        super().__init__(matrix, rows, cols, stage)

    def solve(self,) -> None:
        def flip(i: int, j: int, digit: int):
            line[i] ^= (1 << digit)
            column[j] ^= (1 << digit)
            block[i // 3][j // 3] ^= (1 << digit)

        def dfs(pos: int):
            nonlocal valid
            if pos == len(spaces):
                valid = True
                return

            i, j = spaces[pos]
            mask = ~(line[i] | column[j] | block[i // 3][j // 3]) & 0x1ff
            while mask:
                digitMask = mask & (-mask)
                digit = bin(digitMask).count("0") - 1
                flip(i, j, digit)
                board[i][j] = digit + 1
                dfs(pos + 1)
                flip(i, j, digit)
                mask &= (mask - 1)
                if valid:
                    return

        matrix = deepcopy(self.sudoku_matrix)
        board = matrix

        line = [0] * 9
        column = [0] * 9
        block = [[0] * 3 for _ in range(3)]
        valid = False
        spaces = list()

        for i in range(9):
            for j in range(9):
                if board[i][j] != 0:
                    digit = board[i][j] - 1
                    flip(i, j, digit)

        while True:
            modified = False
            for i in range(9):
                for j in range(9):
                    if board[i][j] == 0:
                        mask = ~(line[i] | column[j] | block[i // 3][j // 3]) & 0x1ff
                        if not (mask & (mask - 1)):
                            digit = bin(mask).count("0") - 1
                            flip(i, j, digit)
                            board[i][j] = digit + 1
                            modified = True
            if not modified:
                break

        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    spaces.append((i, j))

        self.solution = SUDOKU(board)
        dfs(0)


# test = BitcalSolver(s)
# test.solve()
# print(test.solution)


