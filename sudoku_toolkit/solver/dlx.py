import numpy as np
from ..utils import SUDOKU
from ._solver import SudokuSolver
from ..dlx_toolkits import DLXInterface
import sys

class DLXSolver(SudokuSolver):
    def __init__(self, matrix, rows='ABCDEFGHI', cols='123456789', stage=3):
        super().__init__(matrix, rows, cols, stage)
        self.sudoku = matrix

    def solve(self):
        sudoku = np.array(self.sudoku)
        s = DLXInterface()
        sol, found = s.solve(sudoku.astype(int))
        if not found:
            print('Unsolvable SUDOKU')
        else:
            sol_list = s.return_sol(sol)
            self.solution = SUDOKU(sol_list)


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
                test = DLXSolver(s)
                test.solve()
                print(test.solution)
                #
            else:
                print("Please Provide a .txt file...")



