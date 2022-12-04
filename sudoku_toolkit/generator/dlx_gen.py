import time

import numpy as np
from ._generator import SudokuGenerator
from ..dlx_toolkits import DLXInterface
from ..evaluator import is_multi_sol
from ..utils import SUDOKU

class DLXGenerator(SudokuGenerator):
    def __init__(self, matrix_seed=None, rows='ABCDEFGHI', cols='123456789', stage=3):
        super().__init__(matrix_seed, rows, cols)
        pass

    def generate_puzzle(self, spaces, strategy = "optimized"):
        assert self.completed_matrix is not None, 'None completed matrx! Generate it first!'

        def make_holes(sol_list, strategy):
            unvisited_list = [i for i in range(81)]
            holes = 0
            while holes < spaces and len(unvisited_list) > 0:
                index = np.random.choice(unvisited_list)
                if strategy == "optimized":
                    value = sol_list[int(index) // 9][int(index) % 9]
                    sol_list[int(index) // 9][int(index) % 9] = 0
                    if is_multi_sol(sol_list):
                        sol_list[int(index) // 9][int(index) % 9] = value
                    else:
                        holes += 1
                elif strategy == "naive":
                    value = sol_list[int(index) // 9][int(index) % 9]
                    for i in range(1, 10):
                        if i != value:
                            sol_list[int(index) // 9][int(index) % 9] = i
                            DLX_solver = DLXInterface()
                            temp_sol, found = DLX_solver.solve(sol_list)
                            if found:
                                sol_list[int(index) // 9][int(index) % 9] = value
                                break
                    if not found:
                        sol_list[int(index) // 9][int(index) % 9] = 0
                        holes += 1
                unvisited_list.remove(index)
            if holes != spaces and len(unvisited_list) == 0:
                return False, sol_list
            elif holes == spaces:
                return True, sol_list

        def sudoku_puzzle_generator():
            loops = 0
            max_iter = 1000
            while True:
                loops += 1
                print(loops, "loops")
                if loops == max_iter:
                    print("Failed to get a puzzle with", spaces, f"holes in {max_iter} loops.")
                    break
                self.random_init()
                sol_list = self.completed_matrix.sudoku_matrix
                found, sol_list = make_holes(sol_list, strategy)
                if found:
                    return SUDOKU(sol_list)

        puzzle = sudoku_puzzle_generator()
        if isinstance(puzzle, SUDOKU):
            self.generated_matrix = puzzle



if __name__ == "__main__":
    # test = SudokuGeneratorDLX(59)
    # print(test.sudoku_puzzle_generator())
    start = time.time()
    g = DLXGenerator()
    g.random_init()
    g.generate_puzzle(50, strategy = "naive")
    end = time.time()
    print(g.generated_matrix, end - start)

