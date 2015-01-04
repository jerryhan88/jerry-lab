from __future__ import division

from heapq import heappush, heappop

class _node(object):
    def __init__(self, nid):
        self.nid, self.nexts = nid, []
    def __repr__(self):
        return 'n' + str(self.nid)
    def set_next(self, n1, w):
        self.nexts.append([n1, w])

class Net(object):
    def __init__(self, n, E, W):
        self.N = [_node(nid) for nid in xrange(n)]
        for (src, dst), w in zip(E, W):
            self.N[src].set_next(self.N[dst], w)
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
            n._closed = True
            for n1, d_n_n1 in n.nexts:
                if not n1._closed and d + d_n_n1 < n1._distance:
                    n1._distance, n1._parent = d + d_n_n1, n
                    heappush(S, (n1._distance, n1))
        else:
            return None
