from __future__ import division

from heapq import heappush, heappop

class _node(object):
    def __repr__(self):
        return 'n' + str(self.nid)

class Net(object):
    def __init__(self, n, E, W):
        self.N = []
        for nid in xrange(n):
            nobj = _node()
            nobj.nid = nid
            self.N.append(nobj)
        self.D = [[None] * n for _ in xrange(n)]
        for (src, dst), w in zip(E, W):
            self.D[src][dst] = w
    def get_shortest_path(self, src, dst):
        '''
        find shortest path using Dijkstra's algorithm
        '''
        n_from, n_to = self.N[src], self.N[dst]
        for n in self.N:
            n._closed, n._distance = False, 1e400
        S, n_from._parent, n_from._closed, n_from._distance = [(0, n_from)], None, False, 0
        while S:
            d, n = heappop(S)
            if n._closed:
                continue
            if n == n_to:
                return d
            n._closed, n._distance = True, d
            for n1 in self.N:
                if n1 != n and not n1._closed and d + self.D[n.nid][n1.nid] < n1._distance:
                    n1._distance, n1._parent = d + self.D[n.nid][n1.nid], n
                    heappush(S, (n1._distance, n1))
        else:
            return None
