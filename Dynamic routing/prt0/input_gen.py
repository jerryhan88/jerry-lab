from __future__ import division
from random import randrange, random, uniform

R = 100
N = 11

RT = 300

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

def run0():
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
#     run()
    run0()
