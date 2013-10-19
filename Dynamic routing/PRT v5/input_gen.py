from __future__ import division
from random import randrange, random, uniform
from numpy.random import poisson
from Dynamics import Node, Edge

def run():
    requests = []
    for _ in range(R):
        t = round(random() * RT, 1)
        sn = randrange(N)
        dn = randrange(N)
        while sn == dn:
            dn = randrange(N)
        requests.append((t, sn, dn))
    requests.sort()
    
    create_input_txt(requests)    

def run_poi(Nnodes, Nrequest, TTime):
    mu_assi = 10000
    assumed_rambda = TTime/Nrequest
    mu = assumed_rambda * mu_assi
    pd = poisson(mu, Nrequest)
    
    request_at = []
    for i, t in enumerate(pd):
        
        if i == 0:
            request_at.append(t)
            continue
        request_at.append(request_at[-1] + t)
        
    requests = []
    for t in request_at:
        sn = randrange(N)
        dn = randrange(N)
        while sn == dn:
            dn = randrange(N)
        requests.append((t/mu_assi, sn, dn))
    create_input_txt(requests)

def run_uni(Nnodes, Nrequest, TTime):
    requests = []
    for _ in range(R):
#         t = round(random() * RT, 1)
        t = uniform(0, RT)
        
        sn = randrange(N)
        dn = randrange(N)
        while sn == dn:
            dn = randrange(N)
        requests.append((t, sn, dn))
    requests.sort()
    create_input_txt(requests)
    
def create_input_txt(requests):
    i_txt = open('Input', 'w')
    for i, r in enumerate(requests):
        t, sn, dn = r
        i_txt.write('C%d,%f,%d-%d\n' % (i, t, sn, dn))
    i_txt.close()
    
def network0():
    sx, sy = 800, 600
    ns_pos = [(sx * 0.2, sy * 0.3),(sx * 0.6, sy * 0.2),(sx * 0.1, sy * 0.5),(sx * 0.4, sy * 0.6),
     (sx * 0.6, sy * 0.45),(sx * 0.85, sy * 0.35),(sx * 0.3, sy * 0.85),(sx * 0.8, sy * 0.65)]
    Nodes = [Node(px, py) for px, py in ns_pos]
    
    ns_connection = [(0,3),(1,4),(2,3),(3,4),(3,6),(4,5),(4,7),(0,2),(0,4),(1,5),(5,7),(6,7)]
    Edges = [Edge(Nodes[pn], Nodes[nn]) for pn,nn in ns_connection]
    
    for e in Edges[:]:
        Edges.append(Edge(e._to, e._from))
    
    return Nodes, Edges 

def network1():
    sx, sy = 800, 800
        
    ns_pos = [(sx * 0.1, sy * 0.1),(sx * 0.4, sy * 0.1),(sx * 0.75, sy * 0.1),
              (sx * 0.1, sy * 0.3),(sx * 0.4, sy * 0.3),(sx * 0.75, sy * 0.3),
              (sx * 1.0, sy * 0.3),(sx * 0.1, sy * 0.62),(sx * 0.4, sy * 0.62),
              (sx * 0.75, sy * 0.62),(sx * 1.0, sy * 0.62)]
    Nodes = [Node(px, py) for px, py in ns_pos]
    
    ns_connection = [(1, 0), (1, 2), (3, 4), (5, 4), (5, 6), (8, 7), (8, 9), (10, 9), (0, 3), (4, 1), (2, 5), (7, 3), (4, 8), (9, 5), (6, 10)]
    Edges = [Edge(Nodes[pn], Nodes[nn]) for pn,nn in ns_connection]
    
    return Nodes, Edges 
    
if __name__ == '__main__':
    R = 100
    N = 11
    RT = 300
    run_poi(N, R, RT)
