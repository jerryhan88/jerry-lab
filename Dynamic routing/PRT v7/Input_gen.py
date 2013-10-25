from __future__ import division
from numpy.random import poisson
from random import randrange, seed

def network0():
    sx, sy = 800, 800
        
    ns_pos = [(sx * 0.1, sy * 0.1), (sx * 0.4, sy * 0.1), (sx * 0.75, sy * 0.1),
              (sx * 0.1, sy * 0.3), (sx * 0.4, sy * 0.3), (sx * 0.75, sy * 0.3),
              (sx * 1.0, sy * 0.3), (sx * 0.1, sy * 0.62), (sx * 0.4, sy * 0.62),
              (sx * 0.75, sy * 0.62), (sx * 1.0, sy * 0.62)]
    
    ns_connection = [(1, 0), (1, 2), (3, 4), (5, 4), (5, 6),
                     (8, 7), (8, 9), (10, 9), (0, 3), (4, 1),
                     (2, 5), (7, 3), (4, 8), (9, 5), (6, 10)]
    
    return ns_pos, ns_connection  

def gen_customer_arrival_poisson(num_request, Last_arriving_time, NumOfNode):
    seed(0)
    
    accu_pd = []
    mu_assi = 10000
    assumed_rambda = Last_arriving_time / num_request
    mu = assumed_rambda * mu_assi
    pd = poisson(mu, num_request)
    for i, t in enumerate(pd):
        if i == 0:
            accu_pd.append(t)
            continue
        accu_pd.append(accu_pd[-1] + t)
    
    Requests = []
    for t in accu_pd:
        sn = randrange(NumOfNode)
        dn = randrange(NumOfNode)
        while sn == dn:
            dn = randrange(NumOfNode)
        Requests.append((t / mu_assi, sn, dn))
    return Requests

def PRT_pos_ex0():
    return [6, 0, 8]

def make_txt_ofCustomerArrival(Requests):
    i_txt = open('Info. Arrivals of customers.txt', 'w')
    for t, sn, dn in Requests:
        i_txt.write('%f,%d-%d\n' % (t, sn, dn))
    i_txt.close()

if __name__ == '__main__':
    ns_pos, ns_connection = network0()
    num_request, Last_arriving_time = 100, 300
    make_txt_ofCustomerArrival(gen_customer_arrival_poisson(num_request, Last_arriving_time, len(ns_pos)))
    print 'customer arrivals are generated'
