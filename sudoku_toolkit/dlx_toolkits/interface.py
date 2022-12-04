import numpy as np
from .dlx_core import DLX

class Interface:
    def solve(self, sudokuArr):
        solver = DLX()
        solver.create_matrix(sudokuArr)
        dlx_solution, found = solver.search()
        return (dlx_solution, found)

    def return_sol(self, solved):
        solution = [0] * 81
        for i in solved:
            solution[(i.row - 1) // 9] = i.row % 9 if i.row % 9 != 0 else 9
        sol_list = [[solution[i] for i in range(j, j + 9)] for j in range(0, 81, 9)]
        return sol_list

    def return_sol_num(self, sudokuArr):
        solver = DLX()
        solver.create_matrix(sudokuArr)
        dlx_solution, found, sol_num = solver.search_sol_num()
        return sol_num

    def return_if_multi_sol(self, sudokuArr):
        solver = DLX()
        solver.create_matrix(sudokuArr)
        dlx_solution, found, sol_num = solver.search_if_multi_sol()
        if found == 2:
            return True
        elif found == 0:
            return False

    def return_average_alter_nums_flow(self, sudokuArr):
        solver = DLX()
        solver.create_matrix(sudokuArr)
        return solver.alter_nums_flow()

    def return_average_alter_nums(self, sudokuArr):
        alter_nums_flow = self.return_average_alter_nums_flow(sudokuArr)
        return np.average(np.array(alter_nums_flow[0]), axis=0)[1]


