from ..utils import SUDOKU
from ._solver import SudokuSolver
import sys

class BrutalSolver(SudokuSolver):
    def __init__(self, matrix, rows='ABCDEFGHI', cols='123456789', stage=3):
        super().__init__(matrix, rows, cols, stage)
        self.peers_ix = self.get_peer_ixs()

    def solve(self, ) -> None:
        from itertools import product

        targets = [self.map_rc2ix[elem] for elem in self.cubes if self.value_dict[elem] == 0]  # targets to fill in

        target_cands = dict(zip(targets, [list(self.get_candidate_value_s(ix)) for ix in targets]))
        # keys = list(target_cands.keys())
        vals = list(target_cands.values())
        for ix, guess in enumerate(product(*vals)):
            if ix % 1000000000000 == 0:
                print(ix)
            if self.evaluation(guess) == 0:
                self.solution = SUDOKU(self.fill_guess(guess))
                return

        print('SUDOKU not solvable')

    def evaluation(self, sol) -> int:
        sol_dict = dict(zip(self.targets, sol))
        score = 0
        for elem in sol_dict:
            peer_vals = [self.value_1d[peer] if self.value_1d[peer] != 0 else sol_dict[peer] for peer in
                         list(self.peers_ix[elem])]

            for val in peer_vals:
                if val == sol_dict[elem]:
                    score += 1
        # double-scoring
        return int(score / 2)


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
                test = BrutalSolver(s)
                test.solve()
                print(test.solution)
                #
            else:
                print("Please Provide a .txt file...")

