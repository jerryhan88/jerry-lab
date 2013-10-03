from __future__ import division
from random import randrange, random

R = 10
N = 8

RT = 30 

def run():
    requests = []
    for _ in range(R):
        t = round(random() * 30, 1)
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
    run()
