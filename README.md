# Sudoku Toolkits

`sudoku_toolkit` is an end to end Sudoku generate, diagnose and solve package.  

You can easily play Sudoku puzzle by input your 9x9 matrix, use the case provided, or even launch a completely random one by our algorithm! Don't worry, these generated Sudokus are well-defined, i.e. they only has one unique solution. Moreover, you can ask for help by calling some solvers, to get more clues or check your solution.

The class structure of our project likes:

![image-20221204192340639](https://github.com/georgeDuSH/sudoku_toolkit/blob/main/Auxilaries/plots/cls_pic.png)

## Requirements

- Numpy 1.22.3
- Scipy 1.8.0 or above



## Usage

### Sudoku Loading

You can input your own sudoku to our specially designed class `sudoku_toolkit.utils.SUDOKU`. It will automatically prettify the out put of your puzzle.

```python
from sudoku_toolkit.utils import SUDOKU

my_puzzle = [[0,8,5,0,0,0,2,1,0],
             [0,9,4,0,1,2,0,0,3],
             [0,0,0,3,0,0,7,0,4],
             [5,0,3,4,0,9,0,0,0],
             [0,4,0,2,0,6,0,3,0],
             [0,0,0,1,0,3,9,0,7],
             [6,0,8,0,0,5,0,0,0],
             [1,0,0,8,4,0,3,6,0],
             [0,2,7,0,0,0,8,9,0]]

my_puzzle_sdk = SUDOKU(my_puzzle)
print(my_puzzle_sdk)

"""
0 8 5 	 0 0 0 	 2 1 0
0 9 4 	 0 1 2 	 0 0 3
0 0 0 	 3 0 0 	 7 0 4

5 0 3 	 4 0 9 	 0 0 0
0 4 0 	 2 0 6 	 0 3 0
0 0 0 	 1 0 3 	 9 0 7

6 0 8 	 0 0 5 	 0 0 0
1 0 0 	 8 4 0 	 3 6 0
0 2 7 	 0 0 0 	 8 9 0
"""
```

### Sudoku Diagnosing

Do you worry about whether your sudoku is solvable? And how many solutions it has in all? 

By calling `sudoku_toolkit.evaluator.print_solution_report`, our evaluating algorithm will automatically help you to check it out!

```python
from sudoku_toolkit.evaluator import print_solution_report

print_solution_report(my_puzzle)

"""
Sudoku is valid...
Sudoku is solvable...
Sudoku has one unique solution
"""
```

What if we input a bad case with **no solution**?

```python
bad_case_no_solution = [[0,8,5,0,0,0,2,5,0], # duplicated 5 at this row
                        [0,9,4,0,1,2,0,0,3],
                        [0,0,0,3,0,0,7,0,4],
                        [5,0,3,4,0,9,0,0,0],
                        [0,4,0,2,0,6,0,3,0],
                        [0,0,0,1,0,3,9,0,7],
                        [6,0,8,0,0,5,0,0,0],
                        [1,0,0,8,4,0,3,6,0],
                        [0,2,7,0,0,0,8,9,0]]

print_solution_report(bad_case_no_solution)

"""
Sudoku is valid...
Sudoku under examination is not solvable...
"""
```

What if we input a bad case with **multiple solutions**?

```python
# remove elements at the last col
bad_case_multi_solutions = [[0,8,5,0,0,0,2,0,0], 
                            [0,9,4,0,1,2,0,0,0],
                            [0,0,0,3,0,0,7,0,0],
                            [5,0,3,4,0,9,0,0,0],
                            [0,4,0,2,0,6,0,3,0],
                            [0,0,0,1,0,3,9,0,0],
                            [6,0,8,0,0,5,0,0,0],
                            [1,0,0,8,4,0,3,6,0],
                            [0,2,7,0,0,0,8,9,0]]

print_solution_report(bad_case_multi_solutions)

"""
Sudoku is valid...
Sudoku is solvable...
Sudoku has multiple solutions, to be specific, 3 in all.
"""
```

It's really a piece of wonder! The details lies in the detection logic is also interesting, go explore our algorithms!

### Sudoku Generation

Our package also supports generating a random Sudoku matrix.

To do so, we need to first create an object from `sudoku_toolkit.generator.DLXGenerator`.

Then call `random_init()` function to initialize our complete matrix.

Afterwards, try to use `generate_puzzle` with the expected spaces as parameter to generate your own real-time random puzzle!

Please feel free to generate puzzles, since they are all well-defined with only one unique solution.

```python
from sudoku_toolkit.generator import DLXGenerator
from sudoku_toolkit.evaluator import print_solution_report

print('----- Generating Puzzle without Seed -----')
dlx_gen = DLXGenerator()
dlx_gen.random_init()
dlx_gen.generate_puzzle(spaces=25)
print(dlx_gen.generated_matrix)
print_solution_report(dlx_gen.generated_matrix)


print('\n----- Generating Puzzle with Seed -----')
m_seed = [[0,0,0,0,0,0,0,0,0],
          [0,0,2,0,0,0,1,0,0],
          [0,1,0,0,0,0,0,2,0],
          [0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0],
          [0,2,0,0,0,0,0,1,0],
          [0,0,1,0,0,0,2,0,0],
          [0,0,0,0,0,0,0,0,0]]
dlx_gen_s = DLXGenerator(matrix_seed=m_seed)
dlx_gen_s.random_init()
dlx_gen_s.generate_puzzle(spaces=25)
print(dlx_gen_s.generated_matrix)
print_solution_report(dlx_gen_s.generated_matrix)


"""
----- Generating Puzzle without Seed -----
1 loops
3 6 0 	 4 0 1 	 8 0 7
0 0 0 	 6 5 8 	 1 2 3
0 0 0 	 0 0 2 	 4 6 9

8 1 0 	 9 4 6 	 0 3 2
0 0 9 	 1 7 0 	 6 8 0
6 4 5 	 2 8 3 	 7 9 1

1 5 8 	 3 2 7 	 9 4 0
4 0 6 	 0 1 0 	 0 7 5
9 0 3 	 5 6 4 	 2 0 0

Sudoku is valid...
Sudoku is solvable...
Sudoku has one unique solution

----- Generating Puzzle with Seed -----
1 loops
0 0 0 	 0 0 1 	 6 0 4
4 0 0 	 7 0 5 	 1 3 9
6 1 5 	 9 4 3 	 8 0 7

2 7 3 	 4 0 6 	 5 0 0
5 9 8 	 2 0 7 	 4 6 0
1 4 0 	 5 3 0 	 7 8 2

8 0 0 	 6 7 4 	 3 0 5
7 5 0 	 3 9 8 	 0 0 6
3 6 0 	 1 0 2 	 9 7 8

Sudoku is valid...
Sudoku is solvable...
Sudoku has one unique solution
"""
```

### Sudoku Solver

We also supports multiple solving algorithms to tackle the puzzles. Solvers includes:

- BrutalSolver
- DFSSolver
- BitcalSolver
- DLXSolver
- GeneticSolver

You can easily access them from `sudoku_toolkit.solver`, for example:

```python
from sudoku_toolkit.solver import DFSSolver

mat = dlx_gen.generated_matrix.sudoku_matrix

dfs = DFSSolver(mat)
dfs.solve()

print('----- Puzzle -----')
print(dfs)

print('----- Solution -----')
print(dfs.solution)


"""
----- Puzzle -----
3 6 0 	 4 0 1 	 8 0 7
0 0 0 	 6 5 8 	 1 2 3
0 0 0 	 0 0 2 	 4 6 9

8 1 0 	 9 4 6 	 0 3 2
0 0 9 	 1 7 0 	 6 8 0
6 4 5 	 2 8 3 	 7 9 1

1 5 8 	 3 2 7 	 9 4 0
4 0 6 	 0 1 0 	 0 7 5
9 0 3 	 5 6 4 	 2 0 0

----- Solution -----
3 6 2 	 4 9 1 	 8 5 7
7 9 4 	 6 5 8 	 1 2 3
5 8 1 	 7 3 2 	 4 6 9

8 1 7 	 9 4 6 	 5 3 2
2 3 9 	 1 7 5 	 6 8 4
6 4 5 	 2 8 3 	 7 9 1

1 5 8 	 3 2 7 	 9 4 6
4 2 6 	 8 1 9 	 3 7 5
9 7 3 	 5 6 4 	 2 1 8
"""
```

We support calling and solving puzzles with solver in the same way:

```python
from sudoku_toolkit.solver import DFSSolver, DLXSolver, BrutalSolver, GeneticSolver

solvers = [DFSSolver, DLXSolver, BrutalSolver, GeneticSolver]

for solver in solvers:
    model = solver(mat)
    model.solve()
    sol = model.solution
```

- By initializing with the puzzle; 
- By solving with with public function `.solve()`;
- By retrieving the result with public attribute `.solution`.

## Notes

For difficulty evaluation, and other details on our techniques, please kindly check our report.

Thanks for your time, and wish you happy while playing Sudoku.

