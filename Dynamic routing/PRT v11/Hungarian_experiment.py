from __future__ import division
from random import random, seed, randrange
from munkres import Munkres
import dlib
def make_matrix_random(seed_num, size=10):
    seed(seed_num)
    munkres_M = [[random() * 100 for _ in range(size)] for _ in range(size)]
    for _ in range(20):
        munkres_M[randrange(size)][randrange(size)] = 100
    dlib_M = [[-y for y in x]for x in munkres_M]
    for i, x in enumerate(munkres_M):
        for j, v in enumerate(x):
            assert -v == dlib_M[i][j]
    hungarian_algo = Munkres()
    munkres_assignment = hungarian_algo.compute(munkres_M)
    cost = dlib.matrix(dlib_M)
    dlib_assignment = dlib.max_cost_assignment(cost)
    for i, j in munkres_assignment:
        assert dlib_assignment[i] == j
    assert abs(sum(munkres_M[i][j] for i, j in munkres_assignment) + dlib.assignment_cost(cost, dlib_assignment)) < 0.0001
    print 'success seed %d' % seed_num
    
if __name__ == '__main__':
    for i in range(100000):
        make_matrix_random(i)
