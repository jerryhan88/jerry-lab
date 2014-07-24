from igraph import Graph
E = [(0,1), (0,2), (1,3), (2,3), (3,4), (3,5), (4,5)]
W = [ 4 , 2 , 3 , 2 , 3 , 1 , 4 ]

g = Graph(6, E, True, edge_attrs={'weight': W})
print g.topological_sorting()