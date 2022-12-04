from ..utils import SUDOKU
from ..dlx_toolkits import DLXInterface
import numpy as np

class SudokuGenerator(SUDOKU):
    """ Generate sudoku
    """
    def __init__(self, matrix_seed=None, rows='ABCDEFGHI', cols='123456789', stage=3):
        # zero seed
        if matrix_seed is None:
            matrix_seed = [[0 for _ in range(stage**2)] for _ in range(stage**2)]
        super().__init__(matrix_seed, rows, cols, stage)
        self.completed_matrix = None # randomly generated complete matrix
        self.generated_matrix = None # randomly generated sudoku with clues

    def random_init(self, method='dfs') -> None:
        """ Init with random DFS, support generate sudoku with seed

            Example 1: Generate complete sudoku without seed:
            >>> sg1 = SudokuGenerator()
            >>> sg1.random_init()
            >>> print(SUDOKU(sg1.completed_matrix))

                3 6 7 	 1 9 2 	 5 8 4
                1 8 4 	 7 5 3 	 9 6 2
                2 9 5 	 6 4 8 	 3 1 7

                6 2 3 	 4 8 1 	 7 5 9
                9 4 1 	 3 7 5 	 6 2 8
                7 5 8 	 2 6 9 	 1 4 3

                5 1 2 	 8 3 7 	 4 9 6
                8 3 6 	 9 1 4 	 2 7 5
                4 7 9 	 5 2 6 	 8 3 1

            Example 2: Generate complete sudoku seed:
            >>> bugseed = [[0,0,0,0,0,0,0,0,0],
                           [0,0,2,0,0,0,1,0,0],
                           [0,1,0,0,0,0,0,2,0],
                           [0,0,0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0,0,0],
                           [0,2,0,0,0,0,0,1,0],
                           [0,0,1,0,0,0,2,0,0],
                           [0,0,0,0,0,0,0,0,0]]
            >>> sg1 = SudokuGenerator(matrix_seed=bugseed)
            >>> sg1.random_init()
            >>> print(SUDOKU(sg1.completed_matrix))

                8 9 5 	 2 3 1 	 7 4 6
                3 4 2 	 5 6 7 	 1 9 8
                6 1 7 	 9 4 8 	 5 2 3

                5 3 9 	 4 8 2 	 6 7 1
                2 6 8 	 7 1 3 	 9 5 4
                1 7 4 	 6 9 5 	 8 3 2

                4 2 6 	 8 5 9 	 3 1 7
                9 8 1 	 3 7 4 	 2 6 5
                7 5 3 	 1 2 6 	 4 8 9
        """
        from copy import deepcopy
        from random import shuffle

        sudoku = deepcopy(self.sudoku_matrix)
        digits = list(range(1,10,1))

        def random_dfs_generator(sudoku):
            def candidates(row, col):
                row_elem = sudoku[row]
                col_elem = [r[col] for r in sudoku]
                # upper-left elem in target block
                colstart, rowstart = (col//3)*3, (row//3)*3
                block_elem = [sudoku[i][j]
                              for i in range(rowstart, rowstart + 3)
                              for j in range(colstart, colstart + 3)]
                return set(digits) - set(row_elem + col_elem + block_elem) - set([0])

            def solve(ix=0):
                if ix == 81:
                    return True
                row, col = ix//9, ix%9
                # if current hover on missing cube
                if sudoku[row][col] == 0:
                    cands = list(candidates(row, col))
                    # random shuffle
                    shuffle(cands)
                    for val in cands:
                        sudoku[row][col] = val
                        if solve(ix+1):
                            return True
                        sudoku[row][col] = 0
                # if current hover on clue
                else:
                    if solve(ix+1):
                        return True
                return False

            solve()
            return sudoku

        def random_dlx_generator():
            while True:
                sudoku_rand_11 = [[0 for i in range(9)] for j in range(9)]
                index_list = np.random.randint(0, 81, size=11)
                value_list = np.random.randint(1, 10, size=11)
                for i in range(11):
                    sudoku_rand_11[int(index_list[i]) // 9][int(index_list[i]) % 9] = value_list[i]
                s = DLXInterface()
                sol, found = s.solve(sudoku_rand_11)
                if found:
                    sol_list = s.return_sol(sol)
                    return sol_list

        completed_matrix = None
        if method == 'dfs':
            completed_matrix = random_dfs_generator(sudoku)
        elif method == 'dlx':
            completed_matrix = random_dlx_generator()
        else:
            print(f'Invalid method {method}')

        self.completed_matrix = SUDOKU(completed_matrix)

    def generate_puzzle(self, spaces):
        """ Abstract method place holder for later generators """
        pass

if __name__ == "__main__":
    test = SudokuGenerator()
    test.random_init()
    print(SUDOKU(test.completed_matrix))
