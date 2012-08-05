from __future__ import division
from problem import validate_problem, gnode

class tnode(object):
    '''
    tree node
      C: list of jobs in cut
      JS: State of Job (which operation have to be performed)
      PJ: Primary job of each QC
      L: YT's job assign order
      num_LC: How many jobs are confirmed in L
      YS, TS: machine's schedule 
    '''
    next_id = 0
    def __init__(self, C, JS, PJ, L, num_LC, YS, TS, ptn):
        self.id, tnode.next_id, self.ptn = tnode.next_id, tnode.next_id + 1, ptn
        self.C, self.JS = C, JS
        self.PJ, self.L, self.num_LC = PJ, L, num_LC
        self.YS, self.TS = YS, TS

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

def find_available_yt(JS, TS): return [i for i, t in enumerate(TS) if not t or JS[t[-1].id] != 1]
        
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
        C0, JS0, PJ0, L0, num_LC0, YS0, TS0 = tn0.C, tn0.JS, tn0.PJ, tn0.L, tn0.num_LC, tn0.YS, tn0.TS
        _branched = False
        if num_LC0 < len(L0):
            for tr in find_available_yt(JS0, TS0):
                TS = list(TS0)
                TS[tr] = list(TS0[tr])
                TS[tr].append(L0[num_LC0])
                num_LC = num_LC0 + 1
                # branch only one child tree node
                PQ.append(tnode(C0, JS0, PJ0, L0, num_LC, YS0, TS, tn0))
                # mark as branched
                _branched = True
            continue
        elif not C0:
            # check complete schedule
            _nsolution += 1
            yield QS, YS0, TS0
            continue
        # For each op in cut, try branching
        for i in xrange(len(C0) - 1, -1, -1):
            j = C0[i]
            if JS0[j.id] == 0 or JS0[j.id] == 2 :  # YC Operation
                # check j.yc is available
                if YS0[j.yc] and JS0[YS0[j.yc][-1].id] == 1:
                    continue
                
                # plan yc
                YS= list(YS0)
                YS[j.yc] = list(YS0[j.yc])
                YS[j.yc].append(j)
                
                # update C, JS, PJ
                C, JS, PJ = list(C0), list(JS0), list(PJ0)
                if JS[j.id] == 0:
                    assert j.isL
                    JS[j.id] = 1
                else: # CP[j.id] == 2:
                    assert j.isD
                    C.pop(i)
                    JS[j.id] = 4
                    # update PJ
                    qc_id = j.qc
                    j1 = j.next_by_qc
                    # plan qc ops of all subsequent loading jobs
                    while j1 and j1.isL and JS[j1.id] == 4:
                        j1 = j1.next_by_qc
                    PJ[qc_id] = j1
                # branch only one child tree node
                PQ.append(tnode(C, JS, PJ, L0, num_LC0, YS, TS0, tn0))
                # mark as branched
                _branched = True
                
            elif JS0[j.id] == 1:  # YT operation
                C, JS, PJ, L = list(C0), list(JS0), list(PJ0), list(L0)
                if j.isD:  # discharge job
                    # NOTE qc op of job j is the first unplanned qc op regarding qc job sequence,
                    #      because qc op of discharge job can be planned when every preceding job
                    #      is planned
                    # specify truck op is planned
                    
                    # check YT's YC restraint
                    if YS0[j.yc] and JS0[YS0[j.yc][-1].id] == 2:
                        continue
                    JS[j.id] = 2
                    qc_is_released = True
                else:  # loading job
                    # check YT's QC restraint
                    yt_constraint_by_qc = False
                    if PJ[j.qc] != j:
                        j1 = PJ[j.qc].next_by_qc
                        while j1:
                            if JS[j1.id] == 2:
                                yt_constraint_by_qc = True
                                break
                            j1 = j1.next_by_qc
                    if yt_constraint_by_qc:
                        continue
                    # don't need to be cut any more, because ...
                    C.pop(i)
                    # determine truck is restricted
                    j0 = j.prev_by_qc
                    if j0 and JS0[j0.id] <= (1 if j0.isD else 3):
                        JS[j.id] = 2
                        qc_is_released = False
                    else:
                        JS[j.id] = 4
                        qc_is_released = True
                # update L
                L.append(j)
                         
                if qc_is_released:
                    qc_id = j.qc
                    j1 = j.next_by_qc
                    # plan qc ops of all subsequent loading jobs
                    while j1 and j1.isL and JS[j1.id] == 2:
                        # NOTE j has already been popped out from cut
                        JS[j1.id] = 4
                        j1 = j1.next_by_qc
                    # plan qc op of following discharge job
                    if j1 and j1.isD:
                        C.append(j1)
                        JS[j1.id] = 1
                        if j.isL:
                            PJ[qc_id] = j1
                    elif not j1:
                        PJ[qc_id] = 'end'
                # branch only one child tree node
                PQ.append(tnode(C, JS, PJ, L, num_LC0, YS0, TS0, tn0))
                # mark as branched
                _branched = True        
            else:
                print C0, JS0[j.id], j.id
                assert False
        if not _branched:
            problem.display_schedule(QS, YS0, TS0)
            assert False, (_ni, problem.to_tuple_with_id(QS, YS0, TS0))
    
    
def root_tree_node(J, QS, YA, nt):
    C0, JS0 = [], [-1] * len(J)
    PJ0, L0, num_LC0 = [], [], 0 
    for qs in QS:
        # always, include first job of each qc
        j = qs[0]
        C0.append(j)
        JS0[j.id] = (1 if j.isD else 0)  # if first job is discharge, plan qc op right away
        PJ0.append(j)
        # include all loading jobs in cut (yc operation)
        for j in qs[1:]:
            if j.isL:
                C0.append(j)
                JS0[j.id] = 0
    YS0, TS0 = [[] for _ in YA], [[] for _ in xrange(nt)]  # empty sequences of yc and truck
    
    return tnode(C0, JS0, PJ0, L0, num_LC0, YS0, TS0, None)

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
