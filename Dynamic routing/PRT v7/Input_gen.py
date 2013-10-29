from __future__ import division
from numpy.random import poisson
from random import randrange, seed

def network0():
    sx, sy = 800, 800
        
    ns_pos = [(sx * 0.1, sy * 0.1, True), (sx * 0.4, sy * 0.1, True), (sx * 0.75, sy * 0.1, True),
              (sx * 0.1, sy * 0.3, True), (sx * 0.4, sy * 0.3, True), (sx * 0.75, sy * 0.3, True), (sx * 1.0, sy * 0.3, True), 
              (sx * 0.1, sy * 0.62, True), (sx * 0.4, sy * 0.62, True),(sx * 0.75, sy * 0.62, True), (sx * 1.0, sy * 0.62, True)
              , (sx * 0.82, sy * 0.105, False), (sx * 0.88, sy * 0.118, False), (sx * 0.90, sy * 0.13, False)
              , (sx * 0.93, sy * 0.148, False), (sx * 0.9425, sy * 0.1622, False), (sx * 0.97, sy * 0.182, False)
              , (sx * 0.99, sy * 0.22, False)]
    
    ns_connection = [(1, 0), (1, 2), (3, 4), (5, 4), (5, 6),
                     (8, 7), (8, 9), (10, 9), (0, 3), (4, 1),
                     (2, 5), (7, 3), (4, 8), (9, 5), (6, 10)
                     , (11, 2), (12, 11), (13, 12), (14, 13), (15, 14), (16, 15), (17, 16), (6, 17)]
    
    return ns_pos, ns_connection  

def gen_customer_arrival_poisson(num_request, Last_arriving_time, ns_pos):
#     seed(5)
    seed(300)
    
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
        sn, dn = 0, 0
        while sn == dn or not ns_pos[sn][2] or not ns_pos[dn][2]:
            sn = randrange(len(ns_pos))
            dn = randrange(len(ns_pos))
        Requests.append((t / mu_assi, sn, dn))
    return Requests

def PRT_pos_ex0():
    return [6, 0, 8, 7,
            1, 0, 9, 7,
            2, 0, 8, 9,
            3, 0, 9, 7,
            4, 0, 8, 9,
            6, 0, 9, 9,
            7, 0, 8, 7,
            8, 10, 8, 9,
            ]

def make_txt_ofCustomerArrival(Requests):
    i_txt = open('Info. Arrivals of customers.txt', 'w')
    for t, sn, dn in Requests:
        i_txt.write('%f,%d-%d\n' % (t, sn, dn))
    i_txt.close()

if __name__ == '__main__':
    ns_pos, ns_connection = network0()
    num_request, Last_arriving_time = 1000, 300.0
    make_txt_ofCustomerArrival(gen_customer_arrival_poisson(num_request, Last_arriving_time, ns_pos))
    print 'customer arrivals are generated'
