from multiprocessing import Pool
import re
 
def isprime(n):
    convert = ''.join('1' for i in range(n))
    return not re.match(r'^1?$|^(11+?)\1+$', convert)
 
if __name__ == "__main__":
    pool = Pool(processes=4)
    
    rs = [pool.apply_async(isprime, (x,)) for x in range(1000)]
    ps = [r.get() for r in rs]
    
    print [n for n, p in enumerate(ps) if p==True]