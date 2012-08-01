from __future__ import division
from random import choice, randrange
from problem import Job

def gen_jobs0(nj, nq, ny, nt):
    J = [Job(i, choice(['D', 'L'])) for i in xrange(nj)]
    QS = random_partition(J, nq)
    i0 = 0
    for k in xrange(nq):
        QS[k] = J[i0:i0 + len(QS[k])]
        i0 += len(QS[k])
    YA = random_partition(J, ny)
    return J, QS, YA, nt

def random_partition(J, k):
    # partition J into k non-empty subset
    while True:
        PP = [[] for _ in xrange(k)]
        for j in J:
            PP[randrange(k)].append(j)
        if all(P for P in PP):
            return PP


def gen_time0(J, QS, YA, nt):
    '''
    processing and setup time specification in Lee & Ha, 2008
    '''
    # tj: type of each job, qc & yc: qc & yc index of each job
    #   E.g., '0D-1L,2D-3L | 0+1+2,3' -- tj, qc, yc = [0, 1, 0, 1], [0, 0, 1, 1], [0, 0, 0, 1]
    (tj, qc, yc), _J = prepare_gen_time(J, QS, YA), range(len(J))
    # travel time of truck by qc and yc index
    tT_by_QQ = lambda j1, j2: abs(qc[j1] - qc[j2])
    tT_by_QY = lambda j1, j2: abs(qc[j1] - yc[j2]) + 2
    tT_by_YQ = lambda j1, j2: abs(yc[j1] - qc[j2]) + 2
    tT_by_YY = lambda j1, j2: abs(yc[j1] - yc[j2])
    # processing time
    #   QC: D(2), L(2)
    #   YC: D(2), L(2)
    pQ_by_type, pY_by_type, pT_by_type = [2, 2], [2, 2], [tT_by_QY, tT_by_YQ]
    pQ = [pQ_by_type[tj[j]] for j in _J]
    pY = [pY_by_type[tj[j]] for j in _J]
    pT = [pT_by_type[tj[j]](j, j) for j in _J]
    # setup time
    #   QC: D-D(2), D-L(1), L-D(1), L-L(2)
    #   YC: D-D(2), D-L(2), L-D(1), L-L(2)
    uQ_by_type = [[2, 1], [1, 2]]
    uY_by_type = [[2, 2], [1, 2]]
    uT_by_type = [[tT_by_YQ, tT_by_YY], [tT_by_QQ, tT_by_QY]]
    uQ = [['x'] * len(J) for j1 in _J]
    for qs in QS:
        for i in xrange(len(qs) - 1):
            j1, j2 = qs[i].id, qs[i + 1].id
            uQ[j1][j2] = uQ_by_type[tj[j1]][tj[j2]]
    uY = [[(uY_by_type[tj[j1]][tj[j2]] if yc[j1] == yc[j2] else 'x') for j2 in _J] for j1 in _J]
    uT = [[uT_by_type[tj[j1]][tj[j2]](j1, j2) for j2 in _J] for j1 in _J]
    for j in _J:
        uQ[j][j] = uY[j][j] = uT[j][j] = 'x'
    return specify_time_in_job(J, (pQ, pY, pT), (uQ, uY, uT)), QS, YA, nt

def prepare_gen_time(J, QS, YA):
    # validate
    for i, j in enumerate(J):
        assert i == j.id
    # type of job: D(0), L(1)
    tj = [(0 if j.isD else 1) for j in J]
    # index of qc and yc assigned to job
    qc, yc = [None] * len(J), [None] * len(J)
    for q, qs in enumerate(QS):
        for j in qs:
            qc[j.id] = q
    for y, ya in enumerate(YA):
        for j in ya:
            yc[j.id] = y
    assert all(q != None for q in qc) and all(y != None for y in yc)
    return tj, qc, yc

def specify_time_in_job(J, (pQ, pY, pT), (uQ, uY, uT)):
    for j in J:
        j.qsn.p, j.ysn.p, j.tsn.p = pQ[j.id], pY[j.id], pT[j.id]
        j.qen.u, j.yen.u, j.ten.u = uQ[j.id], uY[j.id], uT[j.id]
    return J


def test():
    import problem
    pb = gen_time0(*gen_jobs0(5, 3, 3, 4))
    problem.display_problem(pb)

if __name__ == '__main__':
    test()
