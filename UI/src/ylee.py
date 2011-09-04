from __future__ import division

from random import seed, randrange, random, sample, shuffle
from sys import stdout
from problem import *

'''
TI: total mis-overlay index
x, y: index of stack, index of height
R: number of stacks
K: stack

m = (x0, x1): movement of top container at stack x0 to x1
S = [m1, m2, ...]: sequence of movement m1, m2, ...
'''

# probabilities at Major 1
P_ADD, P_DELETE, P_CHANGE = 0.3, 0.5, 0.3
W_LEN_SEQ, COOLING_RATE = 0.2, 0.999

# parameters for Minor 3
NUM_MAX_HEIGHT_FOR_CONSIDER, MAX_INDEX_FOR_CONSIDER = 2, 2

def neighborhood_search(H, L0, S):
    '''
    Major 1
    '''
    R = len(L0)
    # STEP 1
    Sxx = Sx = S = S[:]
    zxx = zx = W_LEN_SEQ * len(S) + 1.0 * total_mis_overlay_index(apply_sequence(DUP(L0), S))
    T = max(0.1 * zx, 1.2)
    P1, P12 = P_ADD, P_ADD + P_DELETE
    KI = range(R)  # indices of stack
    c = 0
    while T >= 1.0:
        c += 1
        # STEP 2
        p = random()
        if not S or p < P1:
            S.insert(randrange(len(S) + 1), sample(KI, 2))
        elif len(S) == 1 or p < P12:
            S.pop(randrange(len(S)))
        else:
            m = S.pop(randrange(len(S)))
            S.insert(randrange(len(S) + 1), m)
        # STEP 3
        HK = [len(K) for K in L0]  # height of each stack
        i = 0  # current movement index
        while i < len(S):
            x0, x1 = S[i]
            if HK[x0] == 0 or HK[x1] == H:
                S.pop(i)
            else:
                HK[x0] -= 1
                HK[x1] += 1
                i += 1
        # STEP 4
        L1 = apply_sequence(DUP(L0), S)
        z = W_LEN_SEQ * len(S) + 1.0 * total_mis_overlay_index(L1)
        if z < zx + T:
            Sx, zx = S[:], z
            if zx < zxx:
                Sxx, zxx = Sx, zx
        else:
            T *= COOLING_RATE
            # do Minor 3
            S += mis_overlay_index_reducing(H, L1)
    return Sxx, c

def stack_emptying(H, L0):
    '''
    Minor 1
    '''
    S, R, x0 = [], len(L0), randrange(len(L0))
    HK = [len(K) for K in L0]  # height of each stack
    for _ in L0[x0]:
        while True:
            x1 = randrange(R)
            if x1 != x0 and HK[x1] < H:
                break
        S.append((x0, x1))
        HK[x1] += 1
    return S

def sequence_reducing(L, S):
    '''
    Minor 2
    '''
    # construct IL0 (layout of container index)
    IL0, n = [], 0
    for K in L:
        IL0.append([n + j for j in xrange(len(K))])
        n += len(K)
    # reduce
    reduced = True
    while reduced:
        reduced = False
        # P: a set of path (movement sequence of a container)
        #   [[[(1,2), 3], [(2,4), 7], ...], ...]: container 0 is moved from stack 1 to 2
        #      by the 3rd movement in squence, is moved from stack 2 to 4 by 7th one 
        # mi: movement index
        # ci: container index
        P, mi, IL = [[] for _ in xrange(n)], 0, [I[:] for I in IL0]
        while mi < len(S):
            x0, x1 = S[mi]
            ci = IL[x0].pop()
            IL[x1].append(ci)
            if P[ci]:
                # two consecutive movements are (_x0, _x1) and (x0, x1)
                (_x0, _x1), m0i = P[ci][-1]  # m0i: index of previous movement in sequence
                assert _x1 == x0
                for mj in xrange(m0i + 1, mi):
                    if S[mj][0] == x1 or S[mj][1] == x1:
                        break
                else:
                    # change the previous movement and remove current
                    S[m0i] = P[ci][-1][0] = (_x0, x1)
                    del S[mi]
                    reduced = True
                    continue
                    # TODO repeat the above procedure again
            P[ci].append([(x0, x1), mi])
            mi += 1
        # remove (x0, x0) in S
        mi = 0
        while mi < len(S):
            if S[mi][0] == S[mi][1]:
                del S[mi]
            else:
                mi += 1

def mis_overlay_index_reducing(H, L):
    '''
    Minor 3
    NOTE L will be changed!
    '''
    R, S = len(L), []
    # empty special stacks
    KI = range(R); shuffle(KI)
    for x0 in KI:
        if 0 < len(L[x0]) <= NUM_MAX_HEIGHT_FOR_CONSIDER and L[x0][-1] <= MAX_INDEX_FOR_CONSIDER:
            for _ in xrange(len(L[x0])):
                KI1 = range(R); shuffle(KI1)
                for x1 in KI1:
                    # TODO consider L[x1][-1] >= L[x0][-1]?? currently it is totally random
                    if x1 != x0 and 0 < len(L[x1]) < H:
                        L[x1].append(L[x0].pop())
                        S.append((x0, x1))
                        break
                else:
                    break
    # reduce mis-overlay index
    improved = True
    while improved:
        improved = False
        # TODO consider the stack with the greatest mis-overlay index
        #   or the container with the greatest type, first?
        KI = range(R); shuffle(KI)
        for x0 in KI:
            if mis_overlay_index_of_stack(L[x0]) > 0:
                KI1 = range(R); shuffle(KI1)
                for x1 in KI1:
                    if x1 == x0 or len(L[x1]) == H:
                        continue
                    if not L[x1] or (mis_overlay_index_of_stack(L[x1]) == 0 and L[x0][-1] <= L[x1][-1]):
                        L[x1].append(L[x0].pop())
                        S.append((x0, x1))
                        improved = True
                        break
    return S

def apply_sequence(L, S):
    for x0, x1 in S:
        L[x1].append(L[x0].pop())
    return L

def mis_overlay_index_of_stack(K):
    I = 0  # mis-overlay index of a stack
    for y in range(len(K) - 1):
        if K[y] < K[y + 1]:
            overlay_index = len(K) - (y + 1)
            if overlay_index > I:
                I = overlay_index
    return I

def total_mis_overlay_index(L):
    return sum(mis_overlay_index_of_stack(K) for K in L)

def display_layout_by_seq(H, L, S=()):
    # print sequence with container id
    print 'S(%d):' % len(S),
    CL = [['c%d%d' % (x, y) for y in xrange(len(L[x]))] for x in xrange(len(L))]
    for x0, x1 in S:
        print '%s:%d,%d' % (CL[x0][-1], x0, x1),
        CL[x1].append(CL[x0].pop())
    print
    # print layout and mis-overlay index
    L1 = apply_sequence(DUP(L), S)
    display_layout(H, L1)
    print 'TI = %d' % total_mis_overlay_index(L1)

def solve((H, L0), verbose=True):
    if verbose:
        display_layout_by_seq(H, L0)
    else:
        print total_mis_overlay_index(L0),
    zx = 1e400
    for counter in xrange(50):
        S = stack_emptying(H, L0)
        S, num_iters_NS = neighborhood_search(H, L0, S)
        for _ in xrange(3):
            S += mis_overlay_index_reducing(H, apply_sequence(DUP(L0), S))
            sequence_reducing(L0, S)
        TI = total_mis_overlay_index(apply_sequence(DUP(L0), S))
        z = W_LEN_SEQ * len(S) + TI
        if z < zx:
            Sx, zx, TIx = S, z, TI
        if verbose:
            print '%d(%d): %.1f %d(%d)' % (counter + 1, num_iters_NS, zx, TIx, len(Sx))
        else:
            stdout.write('.')
    print
    if verbose:
        display_layout_by_seq(H, L0, Sx)
    else:
        print 'z:%.1f TI:%d |S|:%d' % (zx, TIx, len(Sx))
    return Sx

def test():
    H, L0 = ex1()
    display_layout_by_seq(H, L0)
    print '\nm1:'
    S = stack_emptying(H, L0)
    display_layout_by_seq(H, L0, S)
    print '\nM1'
    S = neighborhood_search(H, L0, S)
    display_layout_by_seq(H, L0, S)
    print '\nm3'
    S += mis_overlay_index_reducing(H, apply_sequence(DUP(L0), S))
    display_layout_by_seq(H, L0, S)
    print '\nm2'
    sequence_reducing(L0, S)
    display_layout_by_seq(H, L0, S)

def test1():
    H, L0 = ex1()
    display_layout_by_seq(H, L0)
    sequence_reducing(L0, 1, 1)

def start_algoritms(layout, H=4):
    '''
    interface for UI
    '''
    L0 = [[int(c[3]) for c in K] for K in layout]
    print L0
    return solve((H, L0))

if __name__ == '__main__':
    # import Psyco if available, to speed up!
    try: import psyco; psyco.full()
    except ImportError: pass
    seed(0)
    #test()
    #test1()
    solve(ex1(), False)
    solve(ex2(), False)
    solve(ex3(), False)
    solve(ex4(), False)
