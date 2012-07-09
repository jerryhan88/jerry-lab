'''
Created on 2012. 7. 6.

@author: JerryHan
'''

from itertools import permutations

def partitions(L, k):
    '''
    partition list L into k (possibly empty) subsets
      e.g., if n = 3 and k = 3, enumerating M as follows:
        [0,0,0], [1,0,0], [2,0,0], [0,1,0], ..., [2,2,2]
    number of all possible partitions is k**|L|
    '''
    n, M = len(L), [0] * len(L)  # M[i]: membership of L[i]
    while True:
        # make and report a partition regarding K
        P = [[] for _ in xrange(k)]
        for i in xrange(n):
            P[M[i]].append(L[i])
        yield P
        # move to next membership
        for i in xrange(n):
            M[i] += 1
            if M[i] == k:
                M[i] = 0
            else:
                break
        else:
            break

def all_parallel_machine_schedules(num_jobs, num_machine):
    def _sequencing(P, S=None):
        if not S:
            S = []
        if len(S) == len(P):
            yield S
        else:
            k = len(S)
            S.append(None)
            for Sk in permutations(P[k]):
                S[k] = Sk
                for S in _sequencing(P, S):
                    yield S
            S.pop()
    L, n = range(num_jobs), num_machine
    for P in partitions(L, n):
        for S in _sequencing(P):
#            print S
            yield S
            
if __name__ == '__main__':
    all_parallel_machine_schedules(4, 3)
