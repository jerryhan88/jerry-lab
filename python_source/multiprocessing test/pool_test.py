from multiprocessing import Pool
import time

def aFunction(x):
    return [[len(z), z] for z in x]

if __name__ == '__main__':
    # create a pool that has 8 workers
    pool = Pool(processes = 4)
    f = open('stopWord.txt', 'r')
    l = f.readlines()
    f.close()
    # remove new line character
    d = [w.strip() for w in l]
    st = time.time()
    result = pool.apply_async(aFunction, [d])
    # print out the result
    print result.get()
    print time.time() - st
#     for x in d:
#         print x