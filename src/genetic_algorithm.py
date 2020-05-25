import random
import sys
import time

import matplotlib.pyplot as plt
import numpy as np

import util
from amnesiac import blurry_memory

"""
It’s on the tip of my tongue! (Genetic Algorithm)
"""

class PasswordCracker:
    # seed
    stuId = 190038751
    # target password length
    pass_len = 10

    def __init__(self, p_sz, m_rt):
        # hyper_parameters
        # population size
        self.p_sz = p_sz
        # mutation rate
        self.m_rt = m_rt
        # parents number
        self.select_num = 10
        # elites (do not evolve)
        self.elite_num = 1

    def selection(self, heuristics):
        """
        select portion of the individuals from the population
        using the 'confidence' as fitness
        """
        # sorted_p = {k:v for k, v in p.items() if v > 0.5}
        sorted_h = sorted(heuristics.items(), key=lambda item: item[1], reverse=True)
        residue = [k[0] for k in sorted_h[self.select_num:]]
        parents = [k[0] for k in sorted_h[:self.select_num]]
        # select_p = random.randrange(0, len(p))
        # selected = sorted_p[len(sorted_p)//2:]

        return parents, residue

    def crossover(self, parent1, parent2):
        """
        one point cross over
        between two strings
        """
        cross_p = random.randrange(0, len(parent1))
        child1 = parent1[:cross_p] + parent2[cross_p:]
        child2 = parent2[:cross_p] + parent1[cross_p:]
        return child1, child2

    def mutation(self, individual):
        """
        random mutation of each individual
        """
        # for i in individual:
        #     # for every gene
        if random.uniform(0, 1) < self.m_rt:
            return individual.replace(random.choice(individual), util.random_pass(1))
        else:
            return individual

    def evolve(self, ps):
        """
        use crossover and mutation to
        evolve the selected parents
        """
        offs = []

        # elitism
        for i in range(0, self.elite_num):
            offs.append(ps[i])

        # crossover
        # while len(offs) < len(ps) - self.elite_num:
        for i in range(0, self.p_sz):
            p1 = random.choice(ps)
            p2 = random.choice(ps)

            cs = self.crossover(p1, p2)
            offs += cs

        # mutation
        for i in range(self.elite_num, len(offs)):
            offs[i] = self.mutation(offs[i])
        # pdb.set_trace()
        return offs

    def crack(self, argv, showPlt=True):
        # init population
        population = []
        for i in range(self.p_sz):
            population.append(util.random_pass(self.pass_len))
        residue = population
        # maxIter = 5000
        curIter = 0
        t0 = time.time()

        # plot data
        stats = []
        while True:
            # filling the population to its original size
            # in case duplication happen
            # while len(population) < self.p_sz:
            #     population.append(util.random_pass(self.pass_len))
            heuristics = blurry_memory(population, self.stuId, int(argv))
            # pdb.set_trace()
            best = util.best_item_by_value(heuristics)
            stats.append(best[1])
            if best[1] == 1.0:
                # result
                break
            # selection (parents for evolving)
            parents, residue = self.selection(heuristics)
            # crossover & mutation (evolve)
            offsprings = self.evolve(parents)
            # pdb.set_trace()
            population = offsprings #+ residue
            # print(len(population))
            curIter += 1

        finish = time.time() - t0
        print("Cracked in {} iteration, and {} seconds! \nIt is = {}".format(curIter, finish, best[0]))

        # # plot all iterations
        if showPlt:
            fig, ax = plt.subplots()
            plt.plot(stats)
            fig.suptitle('Total time used: {}'.format(finish), fontsize=14)
            ax.set_xlabel('Generation')
            ax.set_ylabel('Fitness Score')
            plt.show()

            # save plot
            fig.savefig('../plot/amnesiac{}.png'.format(p_idx))

        return curIter, finish

    def crack_multi(self, argv=0, rs=2):
        iters = []
        ts = 0
        for r in range(rs):
            it, t = cracker.crack(argv, (True if (rs == 1) else False))
            iters.append(it)
            ts += t

        print('Average iteration is: {}, time is {}, variance is {}'.format(sum(iters) / rs,
                                                                            round(ts / rs, 3),
                                                                            np.var(iters)))
        fig, ax = plt.subplots()
        plt.plot(iters)
        # fig.suptitle('Average iteration and time is: {}, {}'.format(sum(iters)/runs, ts/runs), fontsize=14)
        ax.set_xlabel('Run')
        ax.set_ylabel('Iterations')
        plt.show()

        # save plot
        fig.savefig('../plot/amnesiacs{}.png'.format(rs))


if __name__ == '__main__':
    cracker = PasswordCracker(100, 0.3)
    """
    run argument with password index and total number of runs
    for example: python ex2 0 100
    """
    p_idx = 0
    # get which password to crack
    try:
        p_idx = int(sys.argv[1])
    except IndexError:
        pass

    # get how many simulations
    try:
        runs = int(sys.argv[2])
        if runs == 1:
            cracker.crack(p_idx)
        else:
            cracker.crack_multi(p_idx, runs)
    except IndexError:
        cracker.crack(p_idx)
