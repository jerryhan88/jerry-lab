from __future__ import division #@UnresolvedImport
from feasible_search import build_graph, is_cycle
from clasese import Job

def ex1():
    j0, j1, j2, j3, j4, j5 = Job(0, 'L'), Job(1, 'D'), Job(2, 'L'), Job(3, 'D'), Job(4, 'L'), Job(5, 'D') 
    qs = [[j1, j2, j3, j5], [j0, j4]]
    ys = [[j5, j0, j3], [j1, j4, j2]]
    ts = [[j4, j1, j5], [j2, j0], [j3]]
    build_graph(qs, ys, ts, True)
    print is_cycle(qs, ys, ts)

def ex2():
    j0, j1, j2, j3, j4, j5 = Job(0, 'L'), Job(1, 'D'), Job(2, 'D'), Job(3, 'D'), Job(4, 'D'), Job(5, 'L')
    qs = [[j1, j4, j2], [j3, j0, j5 ]]
    ys = [[j4, j1], [j3, j2, j0, j5]]
    ts = [[j1, j3], [j2, j0], [j4, j5]]
    build_graph(qs, ys, ts, True)
    print is_cycle(qs, ys, ts)
if __name__ == '__main__':
#    ex1()
    ex2()
