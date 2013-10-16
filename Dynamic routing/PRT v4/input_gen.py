from __future__ import division
from random import randrange, random, uniform
from numpy.random import poisson

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
    
    i_txt = open('Input', 'w')
    for i, r in enumerate(requests):
        t, sn, dn = r
        i_txt.write('C%d,%f,%d-%d\n' % (i, t, sn, dn))
    i_txt.close()    

def run_poi(Nnodes, Nrequest, TTime):
    requests = []
    assumed_rambda = TTime/Nrequest
    rambda = assumed_rambda * 10000
    
    pd = poisson(rambda, Nrequest)
    
    request_at = []
    for i, t in enumerate(pd):
        if i == 0:
            request_at.append(t)
            continue
        request_at.append(request_at[-1] + t)
            
    return [t / 10000 for t in request_at]
    
#     for _ in range(R):
# #         t = round(random() * RT, 1)
# #         t = uniform(0, RT)
#          poisson()
#         
#         sn = randrange(N)
#         dn = randrange(N)
#         while sn == dn:
#             dn = randrange(N)
#         requests.append((t, sn, dn))
#     requests.sort()
#     
#     i_txt = open('Input', 'w')
#     for i, r in enumerate(requests):
#         t, sn, dn = r
#         i_txt.write('C%d,%f,%d-%d\n' % (i, t, sn, dn))
#     i_txt.close()

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
    
    i_txt = open('Input', 'w')
    for i, r in enumerate(requests):
        t, sn, dn = r
        i_txt.write('C%d,%f,%d-%d\n' % (i, t, sn, dn))
    i_txt.close()        
    
        
if __name__ == '__main__':
    R = 100
    N = 11
    RT = 300

    print run_poi(N, R, RT)
#     run()
#     run0()


