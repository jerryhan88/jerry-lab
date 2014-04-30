from __future__ import division
import RoutingSystem

def run():
    # parameter setting
    NUM_PRT = 50
    NUM_CUSTOMER = 2000
    ArrivalRate = 0.3
    
    PRT_SPEED = 1200  # unit (cm/s)
    S2J_SPEED = 600
    J2D_SPEED = 900
    SETTING_TIME = (45.0, 60.0)  # unit (sec)
    
    Network = Network1(PRT_SPEED, S2J_SPEED, J2D_SPEED)
    
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
    
    v3_sche = [
               ([0,4], findN('2'), findE('3')),
               ([10,14], findN('1'), findE('4')),
               ([32,36], findN('4'), findE('6')),
               ([44,48], findN('4'), findE('8')),
               ([64,68], findN('8'), findE('10')),
               ([74,78], findN('6'), findE('3')),
               ]
    
    
    vehicleLength = 6
    safetyAllowance = 0
    checkZoneLength = vehicleLength + 2 * safetyAllowance
    vehicleSpeed = 3
    responseTime = 2
    
    
    
    from RoutingSystem import PRT
    PRTs = [
            PRT('1', v1_sche[0][1], v1_sche),
            PRT('2', v2_sche[0][1], v2_sche),
            PRT('3', v3_sche[0][1], v3_sche),
            ] 
    
    RoutingSystem.run(SETTING_TIME, PRT_SPEED, Network, PRTs)
    
def Network1(PRT_SPEED, S2J_SPEED, J2D_SPEED):
    from RoutingSystem import Node, Edge, TRANSFER, STATION, JUNCTION, DOT
    
    C_len = [250, 200, 120]
    C = [sum(C_len[:i + 1]) for i in range(len(C_len))]
    
    R_len = [250, 160, 160]
    R = [sum(R_len[:i + 1]) for i in range(len(R_len))]
    
    numOfBerth_station = 4
    btw = 150
    Nodes = [
             Node('1N', C[1], R[0] - btw, JUNCTION, numOfBerth_station),
             Node('1', C[1], R[0], STATION, numOfBerth_station),
             
             Node('2', C[2], R[0], STATION, numOfBerth_station),
             
             Node('3W', C[0] - btw, R[1], JUNCTION, numOfBerth_station),
             Node('3', C[0], R[1], STATION, numOfBerth_station),
             
             Node('4E', C[1] + btw, R[1], JUNCTION, numOfBerth_station),
             Node('4', C[1], R[1], STATION, numOfBerth_station),
             
             Node('5S', C[1], R[2] + btw, JUNCTION, numOfBerth_station),
             Node('5', C[1], R[2], STATION, numOfBerth_station),
             
             Node('6', C[2], R[2], STATION, numOfBerth_station),
             ]
    
    def findN(nID):
        for n in Nodes:
            if n.id == nID:
                return n
        else:
            False
    
    Edges = [
             
             Edge('1', findN('1'), findN('1N'), 11),
             Edge('2', findN('1'), findN('3'), 40),
             Edge('3', findN('1'), findN('2'), 10),
             Edge('4', findN('1'), findN('4'), 20),
             Edge('5', findN('3W'), findN('3'), 11),
             Edge('6', findN('3'), findN('4'), 20),
             Edge('7', findN('4'), findN('4E'), 11),
             Edge('8', findN('4'), findN('5'), 20),
             Edge('9', findN('3'), findN('5'), 40),
             Edge('10', findN('5'), findN('6'), 10),
             Edge('11', findN('5'), findN('5S'), 11),
             
             ]
    
    return Nodes, Edges

if __name__ == '__main__':
    run()
