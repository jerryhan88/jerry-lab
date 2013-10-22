from __future__ import division
from random import randrange, random, uniform, seed
from numpy.random import poisson
from Dynamics import Node, Edge, PRT, Customer

seed(0)

def gen_network0():
    sx, sy = 800, 800
        
    ns_pos = [(sx * 0.1, sy * 0.1), (sx * 0.4, sy * 0.1), (sx * 0.75, sy * 0.1),
              (sx * 0.1, sy * 0.3), (sx * 0.4, sy * 0.3), (sx * 0.75, sy * 0.3),
              (sx * 1.0, sy * 0.3), (sx * 0.1, sy * 0.62), (sx * 0.4, sy * 0.62),
              (sx * 0.75, sy * 0.62), (sx * 1.0, sy * 0.62)]
    Nodes = [Node(px, py) for px, py in ns_pos]
    
    ns_connection = [(1, 0), (1, 2), (3, 4), (5, 4), (5, 6),
                     (8, 7), (8, 9), (10, 9), (0, 3), (4, 1),
                     (2, 5), (7, 3), (4, 8), (9, 5), (6, 10)]
    
    for pn, nn in ns_connection:
        Edge(Nodes[pn], Nodes[nn])
    
    return Nodes

def gen_PRT0(num_PRT, Nodes):
    return [PRT(Nodes[randrange(len(Nodes))]) for _ in range(num_PRT)]

def gen_customer0(Nodes, num_request, Last_arriving_time):
    mu_assi = 10000
    assumed_rambda = Last_arriving_time / num_request
    mu = assumed_rambda * mu_assi
    pd = poisson(mu, num_request)

    accu_pd = []
    for i, t in enumerate(pd):
        if i == 0:
            accu_pd.append(t)
            continue
        accu_pd.append(accu_pd[-1] + t)
    
    Customers = []
    for t in accu_pd:
        sn = randrange(len(Nodes))
        dn = randrange(len(Nodes))
        while sn == dn:
            dn = randrange(len(Nodes))
        Customers.append(Customer(t/mu_assi, Nodes[sn], Nodes[dn]))
        
    return Customers

def write_input_info(Customers, PRTs):
    
    txt = open('Info. Customers & PRTs.txt', 'w')
    txt.write('Customers Info.\n')
    for c in Customers:
        _id, arriving_time, sn, dn = c.id, c.arriving_time, c.sn.id, c.dn.id
        txt.write('C%d,%.1f,%d-%d\n' % (_id, arriving_time, sn, dn))
    txt.write('\n')
    txt.write('PRTs Info.\n')
    for prt in PRTs:
        _id, init_n = prt.id, prt.arrived_n.id
        txt.write('PRT%d, N%d\n' % (_id, init_n))
    txt.close()
            
if __name__ == '__main__':
    R = 100
    N = 11
    RT = 300
    run_poi(N, R, RT)
