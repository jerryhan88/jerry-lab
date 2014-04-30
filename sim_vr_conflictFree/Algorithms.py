from __future__ import division

M = 1e40

def findN(nID):
    for n in Network[0]:
        if n.id == nID:
            return n
    else:
        False

def findE(eID):
    for e in Network[1]:
        if e.id == eID:
            return e
    else:
        False

def conflictFree_routing(sn, en, VsSchedules, Network):
    N = [n.id for n in Network[0]]
    A = [(e._from.id, e._to.id)for e in Network[1]]
    t_i = [4 for _ in range(len(N))]
    
    snID, enID = sn.id, en.id
    
    R = {n:[] for n in N}
    vF = {n:[[-M, M]] for n in N}
    
    for schedules in VsSchedules:
        for WT, n, e in schedules:
            R[n.id].append(WT)
    
    for k, v in R.items():
        for TW in sorted(v):
            c, d = TW
            Oa, Ob = vF[k].pop()
            if Oa < c: 
                vF[k].append([Oa, c])
                vF[k].append([d, Ob])
            else: vF[k].append([Oa, Ob])
        R[k] = sorted(v)
    
    F = set([])
    
    for k, v in vF.items():
        for x in range(len(v)):
            F = F.union(set([(k, x)]))
    
    mainProcedure(snID, enID, N, A, R, F, vF, t_i)

def mainProcedure(snID, enID, N, A, R, F, vF, t_i):
    # Initialization
    L = {}
    P = {}
    Q = {}
    tNOW = 0
    for k, v in vF.items():
        for x in range(len(v)):
            L.setdefault((k, x), M)
            P.setdefault((k, x), 0)
            Q.setdefault((k, x), 0)
            
    L[(snID, 0)] = tNOW
    T = set([(snID, 0)])
    U = set([])
    
    Labelling(F, T, vF, A, L)

def Labelling(F, T, vF, A, L, t_i):    
    for f_jq in F.difference(T):
        for f_ip in T:
            checkReachability(f_ip, f_jq, A, L, t_i)
    
def checkReachability(f_ip, f_jq, A, L, t_i):
    _tau, _lambda = None, None 

    fromID, fOrder = f_ip
    toID, tOrder = f_jq
    
    print L
    print f_ip
    assert False
    # space-feasiblity
    if fromID != toID:
        if (fromID, toID) not in A:
            _tau, _lambda = M, 0
            return _tau, _lambda
        _alpha = L[f_ip] + t_i[]
        
    else:
        assert fromID == toID
        
        
if __name__ == '__main__':
    from data import Network1
    PRT_SPEED = 1200  # unit (cm/s)
    S2J_SPEED = 600
    J2D_SPEED = 900
    SETTING_TIME = (45.0, 60.0)  # unit (sec)
    global Network
    Network = Network1(PRT_SPEED, S2J_SPEED, J2D_SPEED)
            
    v1_sche = [
                ([9, 13], findN('5S'), findE('11')),
                ([20, 24], findN('5'), findE('8')),
                ([40, 44], findN('4'), findE('4')),
                ([60, 64], findN('1'), findE('1')),
                ([71, 75], findN('1N'), findE('1')),
                ]
    
    v2_sche = [
                ([-3, 1], findN('3W'), findE('5')),
                ([8, 12], findN('3'), findE('6')),
                ([28, 32], findN('4'), findE('7')),
                ([39, 43], findN('4E'), findE('7')),
                ]
    
    vehicleLength = 6
    safetyAllowance = 0
    checkZoneLength = vehicleLength + 2 * safetyAllowance
    vehicleSpeed = 3
    responseTime = 2

    VsSchedules = [v1_sche, v2_sche]
    
    conflictFree_routing(findN('2'), findN('6'), VsSchedules, Network)
