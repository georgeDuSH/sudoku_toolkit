import pandas as pd

class TestCases():
    def __init__(self, case_amount):
        self.case_amount = case_amount
        self.test_puzzle_cases = []
        self.test_solution_cases = []

    def return_sudoku(self, sudoku_list):
        sudoku_row = []
        sudoku = [[] for r in range(9)]
        for i in range(9):
            for j in range(9):
                sudoku_row.append(sudoku_list[i * 9 + j])
            sudoku[i] = sudoku_row
            sudoku_row = []
        return sudoku

    def read_csv(self, file_name):
        df = pd.read_csv(file_name, nrows=self.case_amount)
        temp_puzzle = []
        temp_solution = []
        for i in range(self.case_amount):
            puzzle = df.iat[i, 0]
            solution = df.iat[i, 1]
            for number in puzzle:
                temp_puzzle.append(int(number))
            for number in solution:
                temp_solution.append(int(number))
            self.test_puzzle_cases.append(temp_puzzle)
            self.test_solution_cases.append(temp_solution)
            temp_puzzle = []
            temp_solution = []

    def return_test_puzzle_cases(self):
        temp_puzzles = []
        for i in range(self.case_amount):
            temp_puzzles.append(self.return_sudoku(self.test_puzzle_cases[i]))
        return temp_puzzles

    def return_test_solution_cases(self):
        temp_solutions = []
        for i in range(self.case_amount):
            temp_solutions.append(self.return_sudoku(self.test_solution_cases[i]))
        return temp_solutions

# test = TestCases()
# test.read_csv(10) # case_amount = 10
# test.return_test_puzzle_cases()
# test.return_test_solution_cases()

test_case0 = [
    [0,8,5,0,0,0,2,1,0],
    [0,9,4,0,1,2,0,0,3],
    [0,0,0,3,0,0,7,0,4],
    [5,0,3,4,0,9,0,0,0],
    [0,4,0,2,0,6,0,3,0],
    [0,0,0,1,0,3,9,0,7],
    [6,0,8,0,0,5,0,0,0],
    [1,0,0,8,4,0,3,6,0],
    [0,2,7,0,0,0,8,9,0]
]

test_case0_multi = [
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,1,0,0,0,0],
    [0,0,0,3,0,0,7,0,4],
    [5,0,3,4,0,9,0,0,0],
    [0,4,0,2,0,6,0,3,0],
    [0,0,0,1,0,3,9,0,7],
    [6,0,8,0,0,5,0,0,0],
    [1,0,0,8,4,0,3,6,0],
    [0,2,7,0,0,0,8,9,0]
]

test_case1 = [
    [9,0,0,0,0,8,1,7,3],
    [0,0,0,0,0,6,8,0,5],
    [0,0,0,5,1,0,4,2,0],
    [0,0,0,0,6,0,7,0,0],
    [0,4,0,0,0,0,0,5,0],
    [0,0,3,0,2,0,0,0,0],
    [0,6,2,0,5,1,0,0,0],
    [1,0,4,6,0,0,0,0,0],
    [5,3,9,4,0,0,0,0,7]
]

test_case2 = [
    [0,0,1,5,0,8,7,0,3],
    [2,0,0,0,0,0,0,0,0],
    [0,0,4,1,0,0,0,9,0],
    [3,0,2,8,0,0,0,0,0],
    [7,0,0,0,4,0,0,0,1],
    [0,0,0,0,0,6,2,0,5],
    [0,2,0,0,0,1,6,0,0],
    [0,0,0,0,0,0,0,0,9],
    [6,0,8,2,0,5,1,0,0]
]

lmq_sample = [
    [9,0,0,8,0,0,0,0,0],
    [0,0,0,0,0,0,5,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,2,0,0,1,0,0,0,3],
    [0,1,0,0,0,0,0,6,0],
    [0,0,0,4,0,0,0,7,0],
    [7,0,8,6,0,0,0,0,0],
    [0,0,0,0,3,0,1,0,0],
    [4,0,0,0,0,0,2,0,0],
]

lc_case = [
    [5,3,0,0,7,0,0,0,0],
    [6,0,0,1,9,5,0,0,0],
    [0,9,8,0,0,0,0,6,0],
    [8,0,0,0,6,0,0,0,3],
    [4,0,0,8,0,3,0,0,1],
    [7,0,0,0,2,0,0,0,6],
    [0,6,0,0,0,0,2,8,0],
    [0,0,0,4,1,9,0,0,5],
    [0,0,0,0,8,0,0,7,9]
]
