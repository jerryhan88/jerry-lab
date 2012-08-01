from __future__ import division

from itertools import izip, chain
import pickle

class Job(object):
    '''
    isD (isL): true, if j is discharge (loading) job; false, otherwise
    qsn, tsn, ysn: nodes of specifying start of qc op, truck op, yc op
    qen, ten, yen: nodes of specifying end of qc op, truck op, yc op
    n0, nX: first and last node
    '''
    def __init__(self, id, type):
        assert type in ['D', 'L']
        self.id, self.isD, self.isL = id, type == 'D', type == 'L'
        # prepare nodes
        j = self
        j.qsn, j.tsn, j.ysn, j.nX = gnode(j, 'Q'), gnode(j, 'T'), gnode(j, 'Y'), gnode(j, 'F')
        if self.isD:
            j.n0, j.qen, j.ten, j.yen = j.qsn, j.tsn, j.ysn, j.nX
            j.qsn.next_by_job, j.tsn.next_by_job, j.ysn.next_by_job = j.tsn, j.ysn, j.nX
        else:
            j.n0, j.yen, j.ten, j.qen = j.ysn, j.tsn, j.qsn, j.nX
            j.ysn.next_by_job, j.tsn.next_by_job, j.qsn.next_by_job = j.tsn, j.qsn, j.nX
        j.nX.next_by_job = None
    def __repr__(self):
        return str(self.id) + (':D' if self.isD else ':L')
    def __cmp__(self, other):
        return self.id - other.id
    def __hash__(self):
        return self.id
    @staticmethod
    def create_jobs(pb_spec):
        '''
        create_jobs('0D-1L,2D-3L | 0+1+2,3 | 2 | gen_time0') is same as:
          J = j0, j1, j2, j3 = Job(0, 'D'), Job(1, 'L'), Job(2, 'D'), Job(3, 'L')
          QS = [[j0, j1], [j2, j3]]
          YA = [[j0, j1, j2], [j3]]
          nt = 2
          gen.gen_time0(J, QS, YA, nt)
        '''
        import gen
        QS, YA, nt, tfunc = (pb_spec.split(' | ') + ['gen_time0'])[:4]
        QS = [[Job(int(js[:-1]), js[-1]) for js in qs.split('-')] for qs in QS.split(',')]
        J = list(chain(*QS))
        YA = [[J[int(j)] for j in qs.split('+')] for qs in YA.split(',')]
        nt = int(nt)
        assert range(len(J)) == sorted(j.id for j in J) == sorted(j.id for j in chain(*YA)), (J, QS, YA)
        return getattr(gen, tfunc)(J, QS, YA, nt)
    @staticmethod
    def get_processing_and_setup_time(J):
        pQ, pY, pT = zip(*[(j.qsn.p, j.ysn.p, j.tsn.p) for j in J])
        uQ, uY, uT = zip(*[(j.qen.u, j.yen.u, j.ten.u) for j in J])
        return (pQ, pY, pT), (uQ, uY, uT)

class gnode:
    '''
    graph node
      next_by_res: next node regarding job seq. of resource (qc, yc, truck)
      next_by_job: next node regarding operation seq. of job
      num_incomings: number of incoming arcs
    '''
    def __init__(self, job, type):
        self.jid, self.type = job.id, type
        self.next_by_res = None
    def __repr__(self):
        return str(self.jid) + '-' + self.type
    @staticmethod
    def specify_qc_job_seqence_to_graph(QS):
        for qs in QS:
            for i in xrange(len(qs) - 1):
                qs[i].qen.next_by_res = qs[i + 1].qsn
    @staticmethod
    def clear_node_considered_flag(J):
        for j in J:
            j.qsn.considered = j.tsn.considered = j.ysn.considered = j.nX.considered = False
    @staticmethod
    def check_reachable(J, src_nodes, dst_node):
        gnode.clear_node_considered_flag(J)
        # traverse
        todo = src_nodes
        for n in todo:
            n.considered = True
        while todo:
            n = todo.pop()
            if n == dst_node:
                # there is path from src_nodes to dst_node
                return True
            if n.next_by_job and not n.next_by_job.considered:
                todo.append(n.next_by_job)
                n.next_by_job.considered = True
            if n.next_by_res and not n.next_by_res.considered:
                todo.append(n.next_by_res)
                n.next_by_res.considered = True
        # no path
        return False
    @staticmethod
    def is_cycle_free(J, QS, YS, TS):
        '''
        ASSUME QS do not change and are already specified in graph
        '''
        # reset arcs and number of incoming arcs
        for j in J:
            j.yen.next_by_res = j.ten.next_by_res = None
            j.qsn.num_incomings = j.ysn.num_incomings = j.tsn.num_incomings = j.nX.num_incomings = 1
            j.n0.num_incomings = 0
        # draw arcs and count incoming arcs by job sequences
        for qs in QS:
            for i in xrange(1, len(qs)):
                qs[i].qsn.num_incomings += 1
        for ys in YS:
            for i in xrange(1, len(ys)):
                ys[i - 1].yen.next_by_res = ys[i].ysn
                ys[i].ysn.num_incomings += 1
        for ts in TS:
            for i in xrange(1, len(ts)):
                ts[i - 1].ten.next_by_res = ts[i].tsn
                ts[i].tsn.num_incomings = 2
        # get nodes without incoming arcs
        todo, remains = [j.n0 for j in J if j.n0.num_incomings == 0], 4 * len(J)
        # peel out nodes from graph
        while todo:
            n = todo.pop()
            remains -= 1
            if n.next_by_job:
                n.next_by_job.num_incomings -= 1
                if n.next_by_job.num_incomings == 0:
                    todo.append(n.next_by_job)
            if n.next_by_res:
                n.next_by_res.num_incomings -= 1
                if n.next_by_res.num_incomings == 0:
                    todo.append(n.next_by_res)
        return remains == 0
    @staticmethod
    def makespan(J, QS, YS, TS):
        '''
        ASSUME QS do not change and are already specified in graph
        '''
        # reset arcs, number of incoming arcs, ET (earliest-possible start time)
        for j in J:
            j.yen.next_by_res = j.ten.next_by_res = None
            j.qsn.num_incomings = j.ysn.num_incomings = j.tsn.num_incomings = j.nX.num_incomings = 1
            j.n0.num_incomings = 0
            j.qsn.ET = j.ysn.ET = j.tsn.ET = j.nX.ET = 0
        # draw arcs and count incoming arcs by job sequences
        for qs in QS:
            for i in xrange(1, len(qs)):
                qs[i].qsn.num_incomings += 1
        for ys in YS:
            for i in xrange(1, len(ys)):
                ys[i - 1].yen.next_by_res = ys[i].ysn
                ys[i].ysn.num_incomings += 1
        for ts in TS:
            for i in xrange(1, len(ts)):
                ts[i - 1].ten.next_by_res = ts[i].tsn
                ts[i].tsn.num_incomings = 2
        # get nodes without incoming arcs
        todo, remains = [j.n0 for j in J if j.n0.num_incomings == 0], 4 * len(J)
        # peel out nodes from graph by updating ET
        while todo:
            n = todo.pop()
            remains -= 1
            n1j, n1r = n.next_by_job, n.next_by_res
            if n1j:
                ET1 = n.ET + n.p
                if ET1 > n1j.ET:
                    n1j.ET = ET1
                n1j.num_incomings -= 1
                if n1j.num_incomings == 0:
                    todo.append(n1j)
            if n1r:
                ET1 = n.ET + n.u[n1r.jid]
                if ET1 > n1r.ET:
                    n1r.ET = ET1
                n1r.num_incomings -= 1
                if n1r.num_incomings == 0:
                    todo.append(n1r)
        # check cycle-freeness and return makespan
        if remains == 0:
            return max(j.qen.ET for j in J)


def validate_problem(pb):
    J, QS, YA, _ = pb
    # check id vailidity
    for jid, j in enumerate(J):
        assert jid == j.id
    # not empty qc sequence and yc assignment
    for x in chain(QS, YA):
        assert x
    # same jobs specified in qc sequence and yc assignment
    assert set(J) == set(chain(*QS)) == set(chain(*YA))
    # consecutive id in qc sequence
    for qs in QS:
        for i in xrange(1, len(qs)):
            assert qs[i - 1].id < qs[i].id
    # NOTE setup time of qc and yc should be strictly greater than zero,
    #      because in math. model setup time is used to detect and prevent
    #      cycle. E.g., CQ[i] + uQ[i][j] <= CT[j] and CT[j] + uT[j][i] <= CQ[i]
    #      can be evaluated as feasible only when uQ[i][j] or uT[j][i] is
    #      greater than zero, because uT[j][i] can be zero.
    EPSILON = 0.01
    for j in J:
        assert all(u == 'x' or u > EPSILON for u in j.qen.u), (j, j.qen.u)
        assert all(u == 'x' or u > EPSILON for u in j.yen.u), (j, j.yen.u)

def to_tuple_with_id(QS, YS, TS):
    QS = tuple(tuple(j.id for j in qs) for qs in QS)
    YS = tuple(tuple(j.id for j in ys) for ys in YS)
    TS = tuple(tuple(j.id for j in ts) for ts in TS)
    return (QS, YS, TS)

def is_partial_schedule(SS1, SS2):
    for i in (1, 2):
        S1, S2 = SS1[i], SS2[i]
        for s1, s2 in izip(S1, S2):
            if s1 != s2[:len(s1)]:
                return False
    return True


def read_all_schedules(fname):
    # load
    f = open(fname, 'rb')
    J, QS, YA, nt, S = pickle.load(f)
    f.close()
    # transform back
    J = [Job(*j) for j in J]
    QS = [[J[j] for j in qs] for qs in QS]
    YA = [[J[j] for j in ya] for ya in YA]
    # NOTE problem without time information
    return (J, QS, YA, nt), S

def save_all_schedules(pb, S, fname):
    # NOTE time information will not be stored
    J, QS, YA, nt = pb
    # transform
    J = [[j.id, 'D' if j.isD else 'L'] for j in J]
    QS = [[j.id for j in qs] for qs in QS]
    YA = [[j.id for j in ya] for ya in YA]
    # pickle
    f = open(fname, 'wb')
    pickle.dump((J, QS, YA, nt, S), f)
    f.close()


def display_problem(pb, show_time=True):
    J, QS, YA, nt = pb
    (pQ, pY, pT), (uQ, uY, uT) = Job.get_processing_and_setup_time(J)
    q_spec = ','.join('-'.join(str(j.id) + ('D' if j.isD else 'L') for j in qs) for qs in QS)
    y_spec = ','.join('+'.join(str(j.id) for j in ya) for ya in YA)
    print "## '" + ' | '.join([q_spec, y_spec, str(nt)]) + "'"
    print '# of jobs = %d' % len(J)
    print '# of qcs, ycs, yts = %d, %d, %d' % (len(QS), len(YA), nt)
    print 'J = %s' % str(J)
    print '\n'.join("qc%d's seq. = %s" % (i, qs) for i, qs in enumerate(QS))
    print '\n'.join("yc%d's asn. = %s" % (i, ya) for i, ya in enumerate(YA))
    if show_time:
        print 'pQ =', pQ
        print 'pY =', pY
        print 'pT =', pT
        u_to_str = lambda u: '|' + '|\n     |'.join(', '.join(str(y) for y in x) for x in u) + '|'
        print 'uQ =', u_to_str(uQ)
        print 'uY =', u_to_str(uY)
        print 'uT =', u_to_str(uT)

def display_schedule(QS, YS, TS):
    for i, qs in enumerate(QS):
        print 'QC' + str(i) + '=' + str(qs), ' ',
    print
    for i, ys in enumerate(YS):
        print 'YC' + str(i) + '=' + str(ys), ' ',
    print
    for i, ts in enumerate(TS):
        print 'YT' + str(i) + '=' + str(ts), ' ',
    print


def ex1():
    return Job.create_jobs('0D-1L,2D-3L | 0+1+2,3 | 4')

def ex2():
    return Job.create_jobs('0D-1L,2D-3L-4L | 0+1+2,3+4 | 3')

def ex3():
    # number of all schedules: 16176
    return Job.create_jobs('0L-1L-2L,3D-4L-5D | 0+2+4+5,1+3 | 3')

def ex4():
    # 10 jobs, 3 qcs, 3 ycs, 6 trucks
    QS = '0D-1L-2L-3L,4D-5D-6L,7D-8L-9L'
    YS = '0+2+3,1+7+8,4+5+6+9'
    return Job.create_jobs('%s | %s | 8' % (QS, YS))

def ex5():
    # 10 jobs, 3 qcs, 5 ycs, 10 trucks
    QS = '0D-1D-2L-3L-4D-5L-6L,7D-8D-9D-10L-11L-12D,13D-14L-15L-16L-17D-18L-19D'
    YS = '6+7+10+15+17,1+3+12,4+5+8+11+16,9+13+18,0+2+14+19'
    return Job.create_jobs('%s | %s | 10' % (QS, YS))

def ex6():
    # 4 jobs, 2 qcs, 2 ycs, 4 trucks
    QS = '0D-1L-2D,3D'
    YS = '1+3,0+2'
    return Job.create_jobs('%s | %s | 4' % (QS, YS))

def ex7():
    # 4 jobs, 1 qcs, 1 ycs, 2 trucks
    QS = '0L-1D-2L-3L'
    YS = '0+1+2+3'
    return Job.create_jobs('%s | %s | 2' % (QS, YS))

def test():
    pb = ex2()
    display_problem(pb)

def test_pickle():
    from time import clock
    import all_perm
    pb = ex3()
    display_problem(pb, False)
    S0, t0, ys0 = set(), clock(), None
    for i, (QS, YS, TS) in enumerate(all_perm.enum(pb)):
        if ys0 != YS[0]:
            print i, '%.0f sec.' % (clock() - t0), [j.id for j in YS[0]]
            ys0 = list(YS[0])
        #S0.add(problem.to_tuple_with_id(QS, YS, TS))
    print i
    return
    S = set(to_tuple_with_id(*s) for s in all_perm.enum(pb))
    save_all_schedules(pb, S, 'all_j6_2_2_3(1).pkl')
    pb1, S1 = read_all_schedules('all_j6_2_2_3(1).pkl')
    assert pb == pb1 and S == S1
    print 'ok'


if __name__ == '__main__':
#    import psyco; psyco.full()  # import Psyco, to speed up!
    test()
    #test_pickle()
