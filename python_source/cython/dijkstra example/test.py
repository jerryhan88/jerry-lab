from __future__ import division

# network
import net
#N, D = net.ND(*net.gr())
N, D = net.ND(*net.berlin())
E, W = zip(*[([s, d], D[s][d]) for s in N for d in N if s != d])

# graph
import  igraph, dijkstra, dijkstra1, dijkstra2
g = igraph.Graph(len(N), list(E), True, edge_attrs={'weight': W})
net = dijkstra.Net(len(N), E, W)
net1 = dijkstra1.Net(len(N), E, W)
net2 = dijkstra2.Net(len(N), E, W)

# source and destination pairs
from random import sample
num_findings = 10000
SD = [sample(N, 2) for _ in xrange(num_findings)]

def test():
    # validity
    for _ in xrange(100):
        src, dst = sample(N, 2)
        d0 = g.shortest_paths(*[src, dst], weights='weight')[0][0]
        d1 = net.get_shortest_path(src, dst)
        d2 = net1.get_shortest_path(src, dst)
        d3 = net2.get_shortest_path(src, dst)
        assert d0 == d1 == d2 == d3, (d0, d1, d2, d3)
    # time it.
    from timeit import timeit
    print timeit("for s, d in SD: g.shortest_paths(s, d, 'weight')",
                 'from test import g, SD', number=1)
    print timeit('for s, d in SD: net.get_shortest_path(s, d)',
                 'from test import net, SD', number=1)
    print timeit('for s, d in SD: net1.get_shortest_path(s, d)',
                 'from test import net1, SD', number=1)
    print timeit('for s, d in SD: net2.get_shortest_path(s, d)',
                 'from test import net2, SD', number=1)


if __name__ == '__main__':
    test()
