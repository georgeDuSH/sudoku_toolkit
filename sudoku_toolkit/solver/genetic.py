from ..utils import SUDOKU
from ._solver import SudokuSolver
import sys

class GeneticSolver(SudokuSolver):
    """ Solve SUDOKU with Genetic Algorithm

        Example:
        >>> pop_size = 1000 # population size
        >>> max_iter = 1000 # max iteration rounds
        >>> var_rate = 0.1  # variation rate

        >>> g = GeneticSolver(
                [[0,8,5,0,0,0,2,1,0],
                 [0,9,4,0,1,2,0,0,3],
                 [0,0,0,3,0,0,7,0,4],
                 [5,0,3,4,0,9,0,0,0],
                 [0,4,0,2,0,6,0,3,0],
                 [0,0,0,1,0,3,9,0,7],
                 [6,0,8,0,0,5,0,0,0],
                 [1,0,0,8,4,0,3,6,0],
                 [0,2,7,0,0,0,8,9,0]])
        >>> g.solve(population_size=pop_size, var_rate=var_rate, max_iter=max_iter)
        >>> print(g.solution)

            [Iter 0]: min score is 15.
            [Iter 34]: min score is 0.
            Find the optimal solution.
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
        # tagrgets for Genetic to fit
        self.targets = [self.map_rc2ix[elem] for elem in self.cubes if self.value_dict[elem]==0] # targets to fill in
        self.peers_ix = self.get_peer_ixs()
        # key elems for Genetic SOL
        self.population = []
        self.solution = None
        self.min_score = None

    def _random_init_individual(self, ) -> list:
        """ Randomly generate an individual sequence in 1d form.
            Not random from 1-9, but from feasible numbers via [self.get_candidate_nums(...)]

            : return individual: list
                a list of guessing for missing number in sudoku matrix
        """
        from random import choice

        individual = []
        for tix in self.targets:
            candidate_number = list(self.get_candidate_value_s(tix))
            individual.append(choice(candidate_number))

        return individual

    def _random_init_population(self, population_size) -> list:
        """ Randomly initialize a population with size [self.population_size]
            Calling [self._random_init_individual] to generate each individual.

            : return: [list, ...]
                A list with each inner list element as a random guessing of missing number
        """
        population = []
        for _ in range(population_size):
            population.append(self._random_init_individual())

        return population

    def evaluation(self, individual) -> int:
        """ evaluate the score of each individual

            : param individual: list
                Guessing of each individual

            : return: int
                Score of the individual
        """
        sol_dict = dict(zip(self.targets, individual))
        score = 0
        for elem in sol_dict:
            peer_vals = [self.value_1d[peer] if self.value_1d[peer] != 0 else sol_dict[peer] for peer in list(self.peers_ix[elem])]

            for val in peer_vals:
                if val==sol_dict[elem]:
                    score += 1
        # double-scoring
        return int(score/2)

    def solve(self, population_size=1000, var_rate=0.1, max_iter=1000, report=False) -> None:
        """ Main process of genetic algorithm
            1. Generate population
            2. Population cross & evaluation:
                [Result]
                1) If population reaches the minimal score as 0
                   , optimal solution found, we quit the loop
                2) Otherwise, keep loop until max_iter
                [Process]
                Survive involves cross of fathers to produce new individuals
                , variation is considered to produce more possibilities.
                The probability to cross and survive depends on score, with a
                lower score, the higher probability to do the above stuff.
                See more details in GeneticSolver.survive()

            : param population_size: int
                Total size of the population
            : param var_rate: double
                Variation rate, should between 0 to 1
            : param max_iter: int
                Maximum rounds of iteration
        """
        assert var_rate>=0 and var_rate<=1, f'Expected to get variation rate between 0 to 1, but got var_rate={var_rate}'

        population = self._random_init_population(population_size)
        self.population = population

        for iter in range(max_iter):
            (flag, population) = self._survive(population, var_rate)
            self.population = population
            if flag:
                sol2target = population[0]
                print(f'[Iter {iter}]: min score is {self.min_score}.')
                break
            if report and iter%50==0:
                print(f'[Iter {iter}]: min score is {self.min_score}.')

        if self.min_score!=0:
            print(f'Failed to get a solution in {max_iter} loops.')
        else:
            print(f'Find the optimal solution.')
            self.solution = SUDOKU(self.fill_guess(sol2target))

    def _survive(self, population, var_rate):
        """ Key procedure of corss, variation, and filtering.
            1. Evaluate each individual based on their scores. Individual with
               a lower score more likely to have prob to cross.
            2. Sample 2 parents at a time on score, make cross to produce
               offsprings, untill the total size is 2 times of the population
            3. Evaluate all parents' and offsprings' score again, see:
                1) If we got solution, return it along with stop flag
                2) Otherwise pick new population with pop_size based
                   on their score.
        """
        import numpy as np
        # effective weighted sampling technique
        from scipy.stats.sampling import DiscreteAliasUrn

        score = []
        opt_flag = False
        pop_size = len(population)

        for individual in population:
            score.append(self.evaluation(individual))

        prob = self.score2prob(score)
        # alias sampler, most effective weighted sampling, O(1) on average
        # print(prob)
        # print(sum(prob))
        alias_sampler = DiscreteAliasUrn(prob, random_state=np.random.default_rng())

        ng_count = 0 # stands for next generation
        while ng_count<pop_size//2:
            p1_ix, p2_ix = self._choose_parents(alias_sampler)
            p1, p2 = population[p1_ix], population[p2_ix]
            ngs = self._cross(p1, p2, var_rate)
            for ng in ngs:
                population.append(ng)
                score.append(self.evaluation(ng))
            ng_count+=1

        # filter population by score, survive if score is closer to 0
        prob = self.score2prob(score)
        pop_ix = np.arange(len(population))

        survive_ix = np.random.choice(pop_ix, size=pop_size, replace=False, p=prob)
        survived_population = [population[ix] for ix in survive_ix]

        self.min_score = min(score)

        if min(score)==0:
            opt_flag = True
            opt_individual = population[np.argmin(score)]
            return opt_flag, [opt_individual]

        else:
            return opt_flag, survived_population

    def _cross(self, parent0, parent1, var_rate):
        import random
        """ Cross of two parents, and variation of the cross part

            : param parent0, parent1: list
                parent individual randomly sampled from the population

            : return ng1, ng2: list
        """
        next_gen1, next_gen2 = parent0[:], parent1[:]

        plen = len(parent0)
        start = random.randint(0, plen-1)
        end = start + random.randint(0, plen-start-1)
        # cross
        for var_ix in range(start, end):
            next_gen1[var_ix], next_gen2[var_ix] = next_gen2[var_ix], next_gen1[var_ix]
        # variation
        next_gen1 = self._variation(next_gen1, start, end, var_rate)
        next_gen2 = self._variation(next_gen2, start, end, var_rate)

        return next_gen1, next_gen2

    def _variation(self, individual, start, end, var_rate):
        """ For a given individual, random replace digits with
            probability var_rate from start to end
        """
        import random

        gene = individual[:]
        for ix in range(start, end):
            if random.random()<var_rate:
                var_rc_elem = self.targets[ix]
                gene[ix] = random.choice(list(self.get_candidate_value_s(var_rc_elem)))

        return gene

    def fill_guess(self, solution):
        smat_val = self.value_1d[:]

        for ix, tix in enumerate(self.targets):
            smat_val[tix] = solution[ix]

        res = []
        for i in range(9):
            res.append(smat_val[9*i:9*(i+1)])

        return res

    @staticmethod
    def score2prob(score):
        """ Transform score to probability in genetic solver
            , such that individual with lower score will have
            a higher cross score.

            Take the reciprocal of the original score, and normalize all.

            : param score: list | numpy.ndarray
        """
        import numpy as np
        score = 1+score[:] if isinstance(score, np.ndarray) else 1+np.array(score)
        score = 1/score
        return score/score.sum()

    @staticmethod
    def _choose_parents(sampler):
        """ Choose two parent with different index with alias sampler

            : param sampler: scipy.stats.sampling.DiscreteAliasUrn
                sampler returned by scipy.stats.sampling.DiscreteAliasUrn
        """
        # from scipy.stats.sampling import DiscreteAliasUrn

        parent0 = sampler.rvs()
        while True:
            parent1 = sampler.rvs()
            if parent0 != parent1:
                break

        return parent0, parent1


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
                pop_size = 1000
                max_iter = 1000
                var_rate = 0.1

                g = GeneticSolver(s)
                g.solve(population_size=pop_size, var_rate=var_rate, max_iter=max_iter)
                print(g.solution)
                #
            else:
                print("Please Provide a .txt file...")