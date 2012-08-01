from __future__ import division
from problem import validate_problem, gnode

class tnode(object):
    '''
    tree node
      C: list of jobs in cut
      CO = [o0, o1, ..., o_i, ...]: node of job i, which is in cut
      PC: Progress of cut
      PJ: Primary job among qc
      YS, TS: job sequence of yc and truck
      ptn: parent node
    '''
    next_id = 0
    def __init__(self, C, PC, PJ, YS, TS, ptn):
        self.id, tnode.next_id, self.ptn = tnode.next_id, tnode.next_id + 1, ptn
        self.C, self.PC, self.PJ, self.YS, self.TS = C, PC, PJ, YS, TS

def display_difference_from_all_feasible_schedules(S0, S1):
    print '|S0| =', len(S0)
    print '|S1| =', len(S1)
    SD1 = S1.difference(S0)
    SD2 = S0.difference(S1)
    print '|S1 - S0| = %d, |S0 - S1| = %d' % (len(SD1), len(SD2))
    # difference
    print '-------------- (S1 - S0)'
    for s in sorted(SD1):
        print s
    print '-------------- (S0 - S1)'
    for s in sorted(SD2):
        print s
        
def enum(pb):
    # preparation
    J, QS, YA, nt = pb  # problem and set of all trucks
    validate_problem(pb)
    
    initialize_jobs_and_nodes(QS, YA)
    # stack for depth first search with initial tnode in it
    PQ = [root_tree_node(J, QS, YA, nt)]
    # go!
    _ni, _nsolution, _ndeadlock = 0, 0, 0
    while PQ:
        _ni += 1
        tn0 = PQ.pop()
        C0, PC0, PJ0, YS0, TS0 = tn0.C, tn0.PC, tn0.PJ, tn0.YS, tn0.TS
        print C0
        
        # check complete schedule
        if not C0:
            _nsolution += 1
            yield QS, YS0, TS0
            continue
        _branched = False
        for i in xrange(len(C0) - 1, -1, -1):
            j = C0[i]
            
        assert False
    
    
def root_tree_node(J, QS, YA, nt):
    C0, PC0, PJ0 = [], [-1] * len(J), [] 
    for qs in QS:
        # always, include first job of each qc
        j = qs[0]
        C0.append(j)
        PC0[j.id] = (1 if j.isD else 0)  # if first job is discharge, plan qc op right away
        PJ0.append(j)
        # include all loading jobs in cut (yc operation)
        for j in qs[1:]:
            if j.isL:
                C0.append(j)
                PC0[j.id] = 0
    YS0, TS0 = [[] for _ in YA], [[] for _ in xrange(nt)]  # empty sequences of yc and truck
    return tnode(C0, PC0, PJ0, YS0, TS0, None)

def initialize_jobs_and_nodes(QS, YA):
    # connect jobs by qc schedule
    for q_id, qs in enumerate(QS):
        qs[0].prev_by_qc = None
        for i in xrange(len(qs) - 1):
            qs[i].next_by_qc = qs[i + 1]
            qs[i + 1].prev_by_qc = qs[i]
            qs[i].qc = q_id
        qs[-1].next_by_qc = None
        qs[-1].qc = q_id
    # specify yc assignment
    for i, ya in enumerate(YA):
        for j in ya:
            j.yc = i
    # specify qc's job sequence in graph
    gnode.specify_qc_job_seqence_to_graph(QS)


def test():
    from time import clock
    pb = problem.ex6()
    problem.display_problem(pb, False)
    print
    print 'Ref.:',
    t0 = clock()
    S0 = set(problem.to_tuple_with_id(*s) for s in all_perm.enum(pb))
    print '|S0| = %d, cpu time = %.1f' % (len(S0), clock() - t0)
    
    # all enum.
    print 'Enum:',
    t0 = clock()
    S1 = [problem.to_tuple_with_id(*s) for s in enum(pb)]
    print '|S1| = %d (%d), cpu time = %.1f' % (len(S1), len(set(S1)), clock() - t0)
    if S0 != set(S1):
        print
        display_difference_from_all_feasible_schedules(S0, set(S1))
    else:
        print 'ok'

if __name__ == '__main__':
    import problem, all_perm
    test()