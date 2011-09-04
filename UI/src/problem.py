from __future__ import division

'''
H: maximum height
L: layout
K: stack
'''

def ex1():  # sample problem of YSLee
    H = 5
    L = [[5,3,3,3,1],
         [8,6,0],
         [1,5,6,7],
         [5,2],
         [8,8,5],
         [2,0,5,0],
         [8,5,7,6],
         [2],
         [1,6,9,6,4],
         [4,1,5,5]]
    return H, L

def ex2():  # TI = 1
    H = 4
    L = [[7, 3], [0, 3], [0, 0], [9, 0], [4], [8, 7, 4], [9, 5], [3], [9, 9]]
    return H, L

def ex3():  # TI = 4
    H = 4
    L = [[3, 3, 4, 6], [8], [], [4, 0], [9, 5], [1], [0], [], [5, 6, 2]]
    return H, L

def ex4():  # TI = 13
    H = 4
    L = [[4, 2, 0], [6, 7], [7, 8, 5, 4], [0, 1, 4], [6, 4, 1], [2, 5, 3, 5], [], [5, 6], [6, 9, 6, 1]]
    return H, L

def DUP(L):
    '''
    duplicate layout
    '''
    return [K[:] for K in L]

def display_layout(H, L):
    assert max(len(K) for K in L) <= H  # check feasibility
    for y in xrange(H - 1, -1, -1):
        for K in L:
            print K[y] if y < len(K) else ' ',
        print
    print '-' * (len(L) * 2 - 1)
    for x in xrange(len(L)):
        print x,
    print

if __name__ == '__main__':
    H, L = ex1()
    display_layout(H, L)
