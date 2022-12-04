from copy import deepcopy
from ..utils import SUDOKU
from ._solver import SudokuSolver
import sys

class DFSSolver(SudokuSolver):
    """ Solve SUDOKU based on recursively DFS search.

        Example:
        >>> r = DFSSolver(
                [[0,8,5,0,0,0,2,1,0],
                [0,9,4,0,1,2,0,0,3],
                [0,0,0,3,0,0,7,0,4],
                [5,0,3,4,0,9,0,0,0],
                [0,4,0,2,0,6,0,3,0],
                [0,0,0,1,0,3,9,0,7],
                [6,0,8,0,0,5,0,0,0],
                [1,0,0,8,4,0,3,6,0],
                [0,2,7,0,0,0,8,9,0]])
        >>> r.solve()
        >>> print(r.solution)

            3 8 5 	 7 6 4 	 2 1 9
            7 9 4 	 5 1 2 	 6 8 3
            2 1 6 	 3 9 8 	 7 5 4

            5 7 3 	 4 8 9 	 1 2 6
            9 4 1 	 2 7 6 	 5 3 8
            8 6 2 	 1 5 3 	 9 4 7

            6 3 8 	 9 2 5 	 4 7 1
            1 5 9 	 8 4 7 	 3 6 2
            4 2 7 	 6 3 1 	 8 9 5
    """
    def __init__(self, matrix, rows='ABCDEFGHI', cols='123456789', stage=3):
        super().__init__(matrix, rows, cols, stage)

    def solve(self, ) -> None:
        # local vars
        sol = deepcopy(self.sudoku_matrix)
        value_1d = self.value_1d
        ix2rcix = self.ix2rcix
        get_candidate_value = self.get_candidate_value_d

        # solver core
        def solver(ix=0) -> bool:
            """ Solve the sudoku recursively.
                Assume all other indecies<ix is solvable.
                If we move ix=81, the mat is solved, otherwise, we iterate all elems.
                If current cube has no clue, we iterate on all candidate values.
                    If unsolvable, we reset that value to zero, and mark as unsolvable.
                    If solvable, we move on to next ix.
                Otherwise, he current cube has clue, we move to next ix.
                Otherwise, the quiz do not have solution, we mark it as unsolvable.
            """
            if ix==len(value_1d):
                return True
            row, col = ix2rcix(ix)
            # current holds blank number
            if sol[row][col]==0:
                for cand in get_candidate_value(sol, ix):
                    sol[row][col] = cand
                    if solver(ix+1):
                        return True
                    sol[row][col] = 0
            # current holds clue or guess
            else:
                if solver(ix+1):
                    return True
            return False

        if solver():
            self.solution = SUDOKU(sol)
        else:
            print('Unsolvable SUDOKU')


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
                test = DFSSolver(s)
                test.solve()
                print(test.solution)
                #
            else:
                print("Please Provide a .txt file...")


