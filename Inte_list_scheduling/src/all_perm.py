from __future__ import division

from problem import gnode, validate_problem

def enum(pb):
    '''
    enumerate all feasible schedules
    '''
    J, QS, YA, nt = pb  # problem
    validate_problem(pb)
    # prepare
    YA = [list(ya) for ya in YA]  # NOTE YA will change during iterations
    gnode.specify_qc_job_seqence_to_graph(QS)
    # enumeration of yc job sequences
    YS = [[] for _ in YA]
    for _ in feasible_ys_job_seqs(J, YA, YS):
        # enumeration of truck assignment
        for TA in partitions(J, nt):
            # enumeration of truck job sequences
            TS = [[] for _ in TA]
            for _ in feasible_truck_job_seqs(J, TA, TS):
                yield QS, YS, TS

def feasible_ys_job_seqs(J, YA, YS, k=0):
    # ASSUME ya is not empty for every ya in YA
    #        node's next_by_res is cleared
    for i in xrange(len(YA[k])):
        # now, sequencing new job YA[k][i] after YS[k][-1] (i.e., YS[k][-1] --> YA[k][i])
        # check new sequencing gives rise to cycle
        # TODO if next job YA[k][i] is discharge, maybe don't need to check??
        #      (already tried but does not reduce cpu time much.. --)
        if YS[k] and gnode.check_reachable(J, [YA[k][i].ysn], YS[k][-1].yen):
            # there will be cycle, skip!
            continue
        # add job to sequence and specify arc if more than one job are planned
        YS[k].append(YA[k].pop(i))
        if len(YS[k]) > 1:
            YS[k][-2].yen.next_by_res = YS[k][-1].ysn
        # populate next jobs and next yc's job sequence
        if YA[k]:
            for _ in feasible_ys_job_seqs(J, YA, YS, k):
                yield
        elif k < len(YA) - 1:
            for _ in feasible_ys_job_seqs(J, YA, YS, k + 1):
                yield
        else:
            yield
        # get job back from sequence and remove arc
        YA[k].insert(i, YS[k].pop())
        if YS[k]:
            YS[k][-1].yen.next_by_res = None

def feasible_truck_job_seqs(J, TA, TS, k=0):
    if TA[k]:
        for i in xrange(len(TA[k])):
            # now, sequencing new job TA[k][i] after TS[k][-1] (i.e., TS[k][-1] --> TA[k][i])
            # check new sequencing gives rise to cycle
            if TS[k] and gnode.check_reachable(J, [TA[k][i].tsn], TS[k][-1].ten):
                # there will be cycle, skip!
                continue
            # add job to sequence and specify arc if more than one job are planned
            TS[k].append(TA[k].pop(i))
            if len(TS[k]) > 1:
                TS[k][-2].ten.next_by_res = TS[k][-1].tsn
            # populate next jobs and next truck's job sequence
            if TA[k]:
                for _ in feasible_truck_job_seqs(J, TA, TS, k):
                    yield
            elif k < len(TA) - 1:
                for _ in feasible_truck_job_seqs(J, TA, TS, k + 1):
                    yield
            else:
                yield
            # get job back from sequence and remove arc
            TA[k].insert(i, TS[k].pop())
            if TS[k]:
                TS[k][-1].ten.next_by_res = None
    else:
        if k < len(TA) - 1:
            for _ in feasible_truck_job_seqs(J, TA, TS, k + 1):
                yield
        else:
            yield

def enum_all(pb):
    '''
    enumerate all feasible and infeasible schedules
    '''
    J, QS, YA, nt = pb  # problem
    validate_problem(pb)
    # prepare
    YA = [list(ya) for ya in YA]  # NOTE YA will change during iterations
    gnode.specify_qc_job_seqence_to_graph(QS)
    # enumeration of yc job sequences
    YS = [[] for _ in YA]
    for _ in all_ys_job_seqs(J, YA, YS):
        # enumeration of truck assignment
        for TA in partitions(J, nt):
            # enumeration of truck job sequences
            TS = [[] for _ in TA]
            for _ in all_truck_job_seqs(J, TA, TS):
                yield QS, YS, TS

def all_ys_job_seqs(J, YA, YS, k=0):
    # ASSUME ya is not empty for every ya in YA
    for i in xrange(len(YA[k])):
        # now, sequencing new job YA[k][i] after YS[k][-1] (i.e., YS[k][-1] --> YA[k][i])
        YS[k].append(YA[k].pop(i))
        # populate next jobs and next yc's job sequence
        if YA[k]:
            for _ in all_ys_job_seqs(J, YA, YS, k):
                yield
        elif k < len(YA) - 1:
            for _ in all_ys_job_seqs(J, YA, YS, k + 1):
                yield
        else:
            yield
        # get job back from sequence
        YA[k].insert(i, YS[k].pop())

def all_truck_job_seqs(J, TA, TS, k=0):
    if TA[k]:
        for i in xrange(len(TA[k])):
            # now, sequencing new job TA[k][i] after TS[k][-1] (i.e., TS[k][-1] --> TA[k][i])
            TS[k].append(TA[k].pop(i))
            # populate next jobs and next truck's job sequence
            if TA[k]:
                for _ in all_truck_job_seqs(J, TA, TS, k):
                    yield
            elif k < len(TA) - 1:
                for _ in all_truck_job_seqs(J, TA, TS, k + 1):
                    yield
            else:
                yield
            # get job back from sequence
            TA[k].insert(i, TS[k].pop())
    else:
        if k < len(TA) - 1:
            for _ in all_truck_job_seqs(J, TA, TS, k + 1):
                yield
        else:
            yield

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

def check_agreeability():
    import sys
    x = 0
    for n in xrange(50):
        for _ in xrange(100):
            sys.stdout.write('.')
            seed(x)
            #J, QS, _, _ = pb = problem.generate_random_problem0(5, 2, 2, 3)
            J, QS, _, _ = pb = problem.generate_random_problem0(4, 2, 2, 2)
            #problem.display_problem(pb)
            # test: cycle-free schdule --> agreeability
            # test: agreeability --> cycle-free schdule
            for QS, YS, TS in enum_all(pb):
                # cycle-free schdule
                cfree = gnode.is_cycle_free(J, QS, YS, TS)
                # agreeability
                qs_ts = is_agreeable(QS, TS)
                ys_ts = is_agreeable(YS, TS)
                qs_ys = is_LD_agreeable(QS, YS)
                #
                if cfree != (qs_ts and ys_ts and qs_ys):
                    print '----------------------------', x, (cfree, (qs_ts, ys_ts, qs_ys))
                    problem.display_problem(pb)
                    print '----------------------------'
                    problem.display_schedule(QS, YS, TS)
                    return
            x += 1
        print ' ', n + 1

def is_agreeable(S1, S2):
    for s1 in S1:
        for s2 in S2:
            p = 0  # 
            for j1 in s1:
                try:
                    p1 = s2.index(j1)
                    if p1 < p:
                        return False
                    p = p1
                except:
                    pass
    return True

def is_LD_agreeable(QS, YS):
    for qs in QS:
        for ys in YS:
            for iq in xrange(len(qs)):
                jq = qs[iq]
                if jq.type == 'L':
                    try:
                        iy = ys.index(jq)  # index of loading job jq, in yc job seq.
                        for iq1 in xrange(iq + 1, len(qs)):
                            try:
                                if qs[iq1].type == 'D' and ys.index(qs[iq1]) < iy:
                                    return False
                            except:
                                pass
                    except:
                        pass
    return True


def test():
    from time import clock
    seed(0)
    pb = problem.ex2()
    #pb = gen.gen_time0(*gen.gen_jobs0(6, 3, 3, 3))
    # all enumeration of only feasibles
    S0, t0, ys0 = set(), clock(), None
    for i, (QS, YS, TS) in enumerate(enum(pb)):
        if ys0 != YS[0]:
            print i, [j.id for j in YS[0]]
            ys0 = list(YS[0])
        S0.add(problem.to_tuple_with_id(QS, YS, TS))
    assert len(S0) == i + 1
    print clock() - t0
    # all enumeration including infeasibles
    S1, t0, J = set(), clock(), pb[0]
    for QS, YS, TS in enum_all(pb):
        # check cycle-free schdule
        if gnode.is_cycle_free(J, QS, YS, TS):
            S1.add(problem.to_tuple_with_id(QS, YS, TS))
    print clock() - t0
    # check
    assert S0 == S1

def test_profile():
    import cProfile, pstats
    seed(0)
    pb = gen.gen_time0(*gen.gen_jobs0(6, 3, 3, 3))
    cProfile.runctx('for QS, YS, TS in enum(pb): pass', globals(), locals(), 'profile')
    s = pstats.Stats('profile')
    s.strip_dirs().sort_stats('cumulative', 'time').print_stats()

def test_compare():
    from time import clock
    pb, sS = problem.read_all_schedules('all_j6_2_2_3(1).pkl')
    # generate
    t0 = clock()
    S0 = [problem.to_tuple_with_id(*s) for s in enum(pb)]
    print clock() - t0
    # check
    assert len(S0) == len(sS)
    assert set(S0) == sS

def test_validity():
    import sys
    x = 0
    for n in xrange(50):
        for _ in xrange(100):
            sys.stdout.write('.')
            seed(x)
            J, _, _, _ = pb = gen.gen_time0(*gen.gen_jobs0(5, 2, 2, 3))
            # new
            S0 = set()
            for i, (QS, YS, TS) in enumerate(enum(pb)):
                S0.add(problem.to_tuple_with_id(QS, YS, TS))
            assert len(S0) == i + 1
            # all enumeration of only feasibles
            S0 = set(problem.to_tuple_with_id(*s) for s in enum(pb))
            # all enumeration including infeasibles
            S1 = set()
            for QS, YS, TS in enum_all(pb):
                # check cycle-free schdule
                if gnode.is_cycle_free(J, QS, YS, TS):
                    S1.add(problem.to_tuple_with_id(QS, YS, TS))
            # check
            assert S0 == S1
            # to next
            x += 1
        print ' ', n

if __name__ == '__main__':
#    import psyco; psyco.full()  # import Psyco, to speed up!
    from random import seed
    import problem, gen
    #test()
    #test_profile()
    #test_compare()
    #test_validity()
    #check_agreeability()
