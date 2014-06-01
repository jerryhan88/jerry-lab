from __future__ import division
from math import sqrt, pi, cos, sin
from random import randrange, seed, expovariate, sample
from itertools import chain
 
def ex1():
    seed(2)
    #---------------------------------------------------------------------
    # parameter setting
    NUM_PRT = 50
    NUM_CUSTOMER = 5000
    CUSTOMER_ARRIVAL_INTERVAL = 4.2
    
    PRT_SPEED = 12  # unit (m/s)
    S2J_SPEED = 6
    J2D_SPEED = 9
    SETTING_TIME = (45.0, 60.0)  # unit (sec)
    
    Network, Customers, PRTs = gen_instances(S2J_SPEED, J2D_SPEED, CUSTOMER_ARRIVAL_INTERVAL, NUM_CUSTOMER, NUM_PRT, PRT_SPEED)
    
    import Algorithms, Dynamics
    
    dispatcher = Algorithms.NNBA_I
#     dispatcher = Algorithms.NNBA_IA
#     dispatcher = Algorithms.NNBA_IAT
#     dispatcher = Algorithms.NNBA_IT
#     dispatcher = Algorithms.NNBA_IAP
#     dispatcher = Algorithms.NNBA_IATP
    
#     Dynamics.run(SETTING_TIME, PRT_SPEED, Network, PRTs, Customers, dispatcher)
    Dynamics.run(SETTING_TIME, PRT_SPEED, Network, PRTs, Customers, useVisualizer=True)

#---------------------------------------------------------------------
# Generate things such as Network, PRT, Customer

def gen_instances(S2J_SPEED, J2D_SPEED, CUSTOMER_ARRIVAL_INTERVAL, NUM_CUSTOMER, NUM_PRT, PRT_SPEED):
    Network = Network1(S2J_SPEED, J2D_SPEED)
    # Network
    #  Nodes, Edges = Network 
    Customers = gen_Customer(CUSTOMER_ARRIVAL_INTERVAL, NUM_CUSTOMER, Network[0])
    PRTs = gen_PRT(NUM_PRT, PRT_SPEED, Network[0])
    
    return Network, Customers, PRTs

def gen_Customer(average_arrival, num_customers, Nodes):
    from Dynamics import Customer, TRANSFER, STATION
    
    accu_pd = []
    pd = [expovariate(1.0 / average_arrival) for _ in range(num_customers)]
    for i, t in enumerate(pd):
        if i == 0:
            accu_pd.append(t)
            continue
        accu_pd.append(accu_pd[-1] + t)
    
    Stations = [ i for i, n in enumerate(Nodes) if n.nodeType == STATION or n.nodeType == TRANSFER]
    
    Customers = []
    for i, t in enumerate(accu_pd):
        sn, dn = sample(Stations, 2)
        Customers.append(Customer(i, t, Nodes[sn], Nodes[dn]))
    
    customerArrivals_txt = open('Info. Arrivals of customers.txt', 'w')
    for c in Customers:
        t, sn, dn = c.arriving_time, c.sn.id, c.dn.id 
        customerArrivals_txt.write('%f,%s-%s\n' % (t, sn, dn))
    customerArrivals_txt.close()
    
    return Customers

def gen_PRT(numOfPRT, _PRT_SPEED, Nodes):
    from Dynamics import PRT, STATION
    PRTs = []
    for _ in range(numOfPRT):
        target_n_id = randrange(len(Nodes)) 
        while Nodes[target_n_id].nodeType != STATION:
            target_n_id = randrange(len(Nodes)) 
        PRTs.append(PRT(Nodes[target_n_id]))
    return PRTs

def Network1(S2J_SPEED, J2D_SPEED):
    from Dynamics import Node, Edge, TRANSFER, STATION, JUNCTION, DOT
    
    C_len = [0, 210, 150, 200, 230, 180, 200]
    C = [sum(C_len[:i + 1]) for i in range(len(C_len))]
    
    R_len = [0, 150, 180, 160, 210]
    R = [sum(R_len[:i + 1]) for i in range(len(R_len))]
    
    btwSJ = 50
    
    numOfBerth_station = 4
    
    S_Nodes = [
             Node('0', C[1] - 50, R[0], STATION, numOfBerth_station), Node('1', C[3] + 30, R[0], STATION, numOfBerth_station), Node('2', C[5], R[0], STATION, numOfBerth_station),
             Node('3', C[0], R[1] + 25, TRANSFER, 5), Node('4', C[2], R[1], STATION, numOfBerth_station), Node('5', C[4], R[1] - 15, STATION, numOfBerth_station), Node('6', C[6], R[1] + 20, STATION, numOfBerth_station),
             Node('7', C[1], R[2], STATION, numOfBerth_station), Node('8', C[3] + 20, R[2], STATION, numOfBerth_station), Node('9', C[5], R[2] + 10, STATION, numOfBerth_station),
             Node('10', C[0], R[3] + 40, STATION, numOfBerth_station), Node('11', C[2], R[3], STATION, numOfBerth_station), Node('12', C[4], R[3] + 20, STATION, numOfBerth_station), Node('13', C[6], R[3] + 50, STATION, numOfBerth_station),
             Node('14', C[1] - 20, R[4], STATION, numOfBerth_station), Node('15', C[3] - 15, R[4], STATION, numOfBerth_station), Node('16', C[5] + 25, R[4], STATION, numOfBerth_station),
             ]
    
    J_Nodes = []
    
    for i in range(len(S_Nodes)):
        if (0 <= i <= 2) or (7 <= i <= 9) or (14 <= i <= 16):
            W_px, W_py = S_Nodes[i].px - btwSJ, S_Nodes[i].py
            E_px, E_py = S_Nodes[i].px + btwSJ, S_Nodes[i].py
            J_Nodes.append(Node(str(i) + 'W', W_px, W_py, JUNCTION))
            J_Nodes.append(Node(str(i) + 'E', E_px, E_py, JUNCTION))
        else:
            N_px, N_py = S_Nodes[i].px, S_Nodes[i].py - btwSJ
            S_px, S_py = S_Nodes[i].px, S_Nodes[i].py + btwSJ
            J_Nodes.append(Node(str(i) + 'N', N_px, N_py, JUNCTION))
            J_Nodes.append(Node(str(i) + 'S', S_px, S_py, JUNCTION))
    
    Nodes = S_Nodes + J_Nodes
    
    def findN(nID):
        for n in Nodes:
            if n.id == nID:
                return n
        else:
            False 
    JDJ_Nodes = []
    
    JDJ_pos_info1 = [
                    ('0W', '0E', 'Q41', 'CW'),
                    ('1W', '1E', 'Q32', 'CCW'),
                    ('2W', '2E', 'Q41', 'CW'),
                    ('7E', '7W', 'Q32', 'CW'),
                    ('8E', '8W', 'Q41', 'CCW'),
                    ('9E', '9W', 'Q32', 'CW'),
                    ('14E', '14W', 'Q41', 'CCW'),
                    ('15E', '15W', 'Q32', 'CW'),
                    ('16E', '16W', 'Q41', 'CCW'),
                    
                    ('3S', '3N', 'Q21', 'CCW'),
                    ('4N', '4S', 'Q43', 'CCW'),
                    ('5S', '5N', 'Q21', 'CCW'),
                    ('6N', '6S', 'Q43', 'CCW'),
                    ('10S', '10N', 'Q43', 'CW'),
                    ('11N', '11S', 'Q21', 'CW'),
                    ('12S', '12N', 'Q43', 'CW'),
                    ('13N', '13S', 'Q21', 'CW'),
                    ]
    
    def set_posD_OnCurve1(SN, EN, quadrant, direction):
        NS_OnCurve = []
        # SD: distance between a station and a driving link
        SD = 10
        # R: circles radius
        # # this one decide a degree of curve links 
        R = 24
        # L: length of a strait link
        L = 20
        # CLL: curved links length
        CLL = btwSJ - L
        assert R >= SD
        assert R >= CLL / 2
        
        if direction == 'CW':
            if quadrant == 'Q21':
                CC1_x, CC1_y = (SD - R), -CLL 
                CC2_x, CC2_y = (2 * sqrt(R ** 2 - (abs(-CLL / 2 - CC1_y)) ** 2) + SD - R), 0
                
                curveSx, curveSy = 0, -sqrt(R ** 2 - (CC2_x) ** 2)
# #                 
                curveCy = -CLL / 2
                curveCx = -sqrt(R ** 2 - (abs(curveCy - CC2_y)) ** 2) + CC2_x
                
                curve_pos = []
#                 curve_pos.append((CC1_x, CC1_y))
#                 curve_pos.append((curveSx, curveSy))
#                 curve_pos.append((curveCx, curveCy))
#                 curve_pos.append((CC2_x, CC2_y))
                
                for x in range(3):
                    p_y = curveSy + (x + 1) * (curveCy - curveSy) / 4
                    p_x = -sqrt(R ** 2 - (abs(p_y - CC2_y)) ** 2) + CC2_x
                    curve_pos.append((p_x, p_y))
                curve_pos.append((curveCx, curveCy))
                for x in range(4):
                    p_y = curveCy + (x + 1) * (CC1_y - curveCy) / 5
                    p_x = sqrt(R ** 2 - (abs(p_y - CC1_y)) ** 2) + CC1_x
                    curve_pos.append((p_x, p_y))
                curve_pos.append((SD, -(btwSJ - L)))
                curve_pos.append((SD, -(btwSJ)))
                curve_pos.append((SD, -(btwSJ + L)))
                CC1_x, CC1_y = (SD - R), -(btwSJ + L)
                CC2_x, CC2_y = (2 * sqrt(R ** 2 - (abs(-(btwSJ + L + CLL / 2) - CC1_y)) ** 2) + SD - R), -2 * btwSJ
                curveCy = CC2_y + CLL / 2  
                curveCx = -sqrt(R ** 2 - (abs(curveCy - CC2_y)) ** 2) + CC2_x
                curveEx, curveEy = 0, CC2_y + sqrt(R ** 2 - (CC2_x) ** 2)
                for x in range(4):
                    p_y = CC1_y + (x + 1) * (curveCy - CC1_y) / 5
                    p_x = sqrt(R ** 2 - (abs(p_y - CC1_y)) ** 2) + CC1_x
                    curve_pos.append((p_x, p_y))
                curve_pos.append((curveCx, curveCy))
                for x in range(3):
                    p_y = curveCy + (x + 1) * (curveEy - curveCy) / 4
                    p_x = -sqrt(R ** 2 - (abs(p_y - CC2_y)) ** 2) + CC2_x
                    curve_pos.append((p_x, p_y))
                for i, (px, py) in enumerate(curve_pos):
                    NS_OnCurve.append(Node(SN.id + '-' + str(i) + '-' + EN.id, SN.px + px, SN.py - py, DOT))
                    
            if quadrant == 'Q43':
                CC1_x, CC1_y = -(SD - R), CLL 
                CC2_x, CC2_y = -(2 * sqrt(R ** 2 - (abs(CLL / 2 - CC1_y)) ** 2) + SD - R), 0
                
                curveSx, curveSy = 0, sqrt(R ** 2 - (CC2_x) ** 2)
                curveCy = CLL / 2
                curveCx = sqrt(R ** 2 - (abs(curveCy - CC2_y)) ** 2) + CC2_x
                
                curve_pos = []

                for x in range(3):
                    p_y = curveSy + (x + 1) * (curveCy - curveSy) / 4
                    p_x = sqrt(R ** 2 - (abs(p_y - CC2_y)) ** 2) + CC2_x
                    curve_pos.append((p_x, p_y))
                curve_pos.append((curveCx, curveCy))
                for x in range(4):
                    p_y = curveCy + (x + 1) * (CC1_y - curveCy) / 5
                    p_x = -sqrt(R ** 2 - (abs(p_y - CC1_y)) ** 2) + CC1_x
                    curve_pos.append((p_x, p_y))
                curve_pos.append((-SD, (btwSJ - L)))
                curve_pos.append((-SD, (btwSJ)))
                curve_pos.append((-SD, (btwSJ + L)))
                CC1_x, CC1_y = -(SD - R), btwSJ + L
                CC2_x, CC2_y = -(2 * sqrt(R ** 2 - (abs(btwSJ + L + CLL / 2 - CC1_y)) ** 2) + SD - R), 2 * btwSJ
                 
                curveCy = CC2_y - CLL / 2  
                curveCx = sqrt(R ** 2 - (abs(curveCy - CC2_y)) ** 2) + CC2_x
                curveEx, curveEy = 0, CC2_y - sqrt(R ** 2 - (CC2_x) ** 2)
                for x in range(4):
                    p_y = CC1_y + (x + 1) * (curveCy - CC1_y) / 5
                    p_x = -sqrt(R ** 2 - (abs(p_y - CC1_y)) ** 2) + CC1_x
                    curve_pos.append((p_x, p_y))
                curve_pos.append((curveCx, curveCy))
                for x in range(3):
                    p_y = curveCy + (x + 1) * (curveEy - curveCy) / 4
                    p_x = sqrt(R ** 2 - (abs(p_y - CC2_y)) ** 2) + CC2_x
                    curve_pos.append((p_x, p_y))
                
                for i, (px, py) in enumerate(curve_pos):
                    NS_OnCurve.append(Node(SN.id + '-' + str(i) + '-' + EN.id, SN.px + px, SN.py - py, DOT))
            if quadrant == 'Q41':
                # circles center
                CC1_x, CC1_y = CLL, (SD - R)
                CC2_x, CC2_y = 0, (2 * sqrt(R ** 2 - (abs(CLL / 2 - CC1_x)) ** 2) + SD - R)
                
                curveSx, curveSy = sqrt(R ** 2 - (CC2_y) ** 2), 0
                
                curveCx = CLL / 2
                curveCy = -sqrt(R ** 2 - (abs(curveCx - CC2_x)) ** 2) + CC2_y
                
                curve_pos = []
                for x in range(3):
                    p_x = curveSx + (x + 1) * (curveCx - curveSx) / 4
                    p_y = -sqrt(R ** 2 - (abs(p_x - CC2_x)) ** 2) + CC2_y
                    curve_pos.append((p_x, p_y))
                
                curve_pos.append((curveCx, curveCy))
        
                for x in range(4):
                    p_x = curveCx + (x + 1) * (CC1_x - curveCx) / 5
                    p_y = sqrt(R ** 2 - (abs(p_x - CC1_x)) ** 2) + CC1_y
                    curve_pos.append((p_x, p_y))
                
                curve_pos.append((btwSJ - L, SD))
                curve_pos.append((btwSJ, SD))
                curve_pos.append((btwSJ + L, SD))
                
                CC1_x, CC1_y = btwSJ + L, (SD - R)
                CC2_x, CC2_y = 2 * btwSJ, (2 * sqrt(R ** 2 - (abs(btwSJ + L + CLL / 2 - CC1_x)) ** 2) + SD - R)
                
                curveCx = CC2_x - CLL / 2
                curveCy = -sqrt(R ** 2 - (abs(curveCx - CC2_x)) ** 2) + CC2_y
                
                curveEx, curveEy = CC2_x - sqrt(R ** 2 - (CC2_y) ** 2), 0
                
                for x in range(4):
                    p_x = CC1_x + (x + 1) * (curveCx - CC1_x) / 5
                    p_y = sqrt(R ** 2 - (abs(p_x - CC1_x)) ** 2) + CC1_y
                    curve_pos.append((p_x, p_y))
                curve_pos.append((curveCx, curveCy))
                for x in range(3):
                    p_x = curveCx + (x + 1) * (curveEx - curveCx) / 4
                    p_y = -sqrt(R ** 2 - (abs(p_x - CC2_x)) ** 2) + CC2_y
                    curve_pos.append((p_x, p_y))
                for i, (px, py) in enumerate(curve_pos):
                    NS_OnCurve.append(Node(SN.id + '-' + str(i) + '-' + EN.id, SN.px + px, SN.py - py, DOT))
            if quadrant == 'Q32':
                # circles center
                CC1_x, CC1_y = CLL, -(SD - R)
                CC2_x, CC2_y = 0, -(2 * sqrt(R ** 2 - (abs(CLL / 2 - CC1_x)) ** 2) + SD - R)
                
                curveSx, curveSy = sqrt(R ** 2 - (CC2_y) ** 2), 0
                
                curveCx = CLL / 2
                curveCy = sqrt(R ** 2 - (abs(curveCx - CC2_x)) ** 2) + CC2_y
                curve_pos = []
                for x in range(3):
                    p_x = curveSx + (x + 1) * (curveCx - curveSx) / 4
                    p_y = sqrt(R ** 2 - (abs(p_x - CC2_x)) ** 2) + CC2_y
                    curve_pos.append((p_x, p_y))
                
                curve_pos.append((curveCx, curveCy))
                
                for x in range(4):
                    p_x = curveCx + (x + 1) * (CC1_x - curveCx) / 5
                    p_y = -sqrt(R ** 2 - (abs(p_x - CC1_x)) ** 2) + CC1_y
                    curve_pos.append((p_x, p_y))
                
                curve_pos.append(((btwSJ - L), -SD))
                curve_pos.append(((btwSJ), -SD))
                curve_pos.append(((btwSJ + L), -SD))
                
                CC1_x, CC1_y = btwSJ + L, -(SD - R)
                CC2_x, CC2_y = 2 * btwSJ, -(2 * sqrt(R ** 2 - (abs(btwSJ + L + CLL / 2 - CC1_x)) ** 2) + SD - R)
                
                curveCx = CC2_x - CLL / 2
                curveCy = sqrt(R ** 2 - (abs(curveCx - CC2_x)) ** 2) + CC2_y
                
                curveEx, curveEy = CC2_x - sqrt(R ** 2 - (CC2_y) ** 2), 0
                
                for x in range(4):
                    p_x = CC1_x + (x + 1) * (curveCx - CC1_x) / 5
                    p_y = -sqrt(R ** 2 - (abs(p_x - CC1_x)) ** 2) + CC1_y
                    curve_pos.append((p_x, p_y))
                curve_pos.append((curveCx, curveCy))
                for x in range(3):
                    p_x = curveCx + (x + 1) * (curveEx - curveCx) / 4
                    p_y = sqrt(R ** 2 - (abs(p_x - CC2_x)) ** 2) + CC2_y
                    curve_pos.append((p_x, p_y))
                    
                
                for i, (px, py) in enumerate(curve_pos):
                    NS_OnCurve.append(Node(SN.id + '-' + str(i) + '-' + EN.id, SN.px - px, SN.py - py, DOT))
        else:
            assert direction == 'CCW'
            if quadrant == 'Q41':
                # circles center
                CC1_x, CC1_y = CLL, (SD - R)
                CC2_x, CC2_y = 0, (2 * sqrt(R ** 2 - (abs(CLL / 2 - CC1_x)) ** 2) + SD - R)
                
                curveSx, curveSy = sqrt(R ** 2 - (CC2_y) ** 2), 0
                
                curveCx = CLL / 2
                curveCy = -sqrt(R ** 2 - (abs(curveCx - CC2_x)) ** 2) + CC2_y
                curve_pos = []
                
                for x in range(3):
                    p_x = curveSx + (x + 1) * (curveCx - curveSx) / 4
                    p_y = -sqrt(R ** 2 - (abs(p_x - CC2_x)) ** 2) + CC2_y
                    curve_pos.append((p_x, p_y))
                curve_pos.append((curveCx, curveCy))
                 
                for x in range(4):
                    p_x = curveCx + (x + 1) * (CC1_x - curveCx) / 5
                    p_y = sqrt(R ** 2 - (abs(p_x - CC1_x)) ** 2) + CC1_y
                    curve_pos.append((p_x, p_y))
                curve_pos.append(((btwSJ - L), SD))
                curve_pos.append(((btwSJ), SD))
                curve_pos.append(((btwSJ + L), SD))
                CC1_x, CC1_y = btwSJ + L, (SD - R)
                CC2_x, CC2_y = 2 * btwSJ, (2 * sqrt(R ** 2 - (abs(btwSJ + L + CLL / 2 - CC1_x)) ** 2) + SD - R)
                 
                curveCx = CC2_x - CLL / 2
                curveCy = -sqrt(R ** 2 - (abs(curveCx - CC2_x)) ** 2) + CC2_y
                 
                curveEx, curveEy = CC2_x - sqrt(R ** 2 - (CC2_y) ** 2), 0
                 
                for x in range(4):
                    p_x = CC1_x + (x + 1) * (curveCx - CC1_x) / 5
                    p_y = sqrt(R ** 2 - (abs(p_x - CC1_x)) ** 2) + CC1_y
                    curve_pos.append((p_x, p_y))
                curve_pos.append((curveCx, curveCy))
                for x in range(3):
                    p_x = curveCx + (x + 1) * (curveEx - curveCx) / 4
                    p_y = -sqrt(R ** 2 - (abs(p_x - CC2_x)) ** 2) + CC2_y
                    curve_pos.append((p_x, p_y))
                    
                
                for i, (px, py) in enumerate(curve_pos):
                    NS_OnCurve.append(Node(SN.id + '-' + str(i) + '-' + EN.id, SN.px - px, SN.py - py, DOT))
            if quadrant == 'Q32':
                # circles center
                CC1_x, CC1_y = CLL, -(SD - R)
                CC2_x, CC2_y = 0, -(2 * sqrt(R ** 2 - (abs(CLL / 2 - CC1_x)) ** 2) + SD - R)
                
                curveSx, curveSy = sqrt(R ** 2 - (CC2_y) ** 2), 0
                
                curveCx = CLL / 2
                curveCy = sqrt(R ** 2 - (abs(curveCx - CC2_x)) ** 2) + CC2_y
                curve_pos = []
                
                for x in range(3):
                    p_x = curveSx + (x + 1) * (curveCx - curveSx) / 4
                    p_y = sqrt(R ** 2 - (abs(p_x - CC2_x)) ** 2) + CC2_y
                    curve_pos.append((p_x, p_y))
                curve_pos.append((curveCx, curveCy))
                for x in range(4):
                    p_x = curveCx + (x + 1) * (CC1_x - curveCx) / 5
                    p_y = -sqrt(R ** 2 - (abs(p_x - CC1_x)) ** 2) + CC1_y
                    curve_pos.append((p_x, p_y))
                curve_pos.append(((btwSJ - L), -SD))
                curve_pos.append(((btwSJ), -SD))
                curve_pos.append(((btwSJ + L), -SD))
                
                CC1_x, CC1_y = btwSJ + L, -(SD - R)
                CC2_x, CC2_y = 2 * btwSJ, -(2 * sqrt(R ** 2 - (abs(btwSJ + L + CLL / 2 - CC1_x)) ** 2) + SD - R)
                  
                curveCx = CC2_x - CLL / 2
                curveCy = sqrt(R ** 2 - (abs(curveCx - CC2_x)) ** 2) + CC2_y
                  
                curveEx, curveEy = CC2_x - sqrt(R ** 2 - (CC2_y) ** 2), 0
                  
                for x in range(4):
                    p_x = CC1_x + (x + 1) * (curveCx - CC1_x) / 5
                    p_y = -sqrt(R ** 2 - (abs(p_x - CC1_x)) ** 2) + CC1_y
                    curve_pos.append((p_x, p_y))
                curve_pos.append((curveCx, curveCy))
                for x in range(3):
                    p_x = curveCx + (x + 1) * (curveEx - curveCx) / 4
                    p_y = sqrt(R ** 2 - (abs(p_x - CC2_x)) ** 2) + CC2_y
                    curve_pos.append((p_x, p_y))
                for i, (px, py) in enumerate(curve_pos):
                    NS_OnCurve.append(Node(SN.id + '-' + str(i) + '-' + EN.id, SN.px + px, SN.py - py, DOT))
            if quadrant == 'Q21':
                CC1_x, CC1_y = -(SD - R), CLL 
                CC2_x, CC2_y = -(2 * sqrt(R ** 2 - (abs(CLL / 2 - CC1_y)) ** 2) + SD - R), 0
                
                curveSx, curveSy = 0, sqrt(R ** 2 - (CC2_x) ** 2)
                
                curveCy = CLL / 2
                curveCx = sqrt(R ** 2 - (abs(curveCy - CC2_y)) ** 2) + CC2_x
                
                curve_pos = []
                
                for x in range(3):
                    p_y = curveSy + (x + 1) * (curveCy - curveSy) / 4
                    p_x = sqrt(R ** 2 - (abs(p_y - CC2_y)) ** 2) + CC2_x
                    curve_pos.append((p_x, p_y))
                curve_pos.append((curveCx, curveCy))
                for x in range(4):
                    p_y = curveCy + (x + 1) * (CC1_y - curveCy) / 5
                    p_x = -sqrt(R ** 2 - (abs(p_y - CC1_y)) ** 2) + CC1_x
                    curve_pos.append((p_x, p_y))
                curve_pos.append((-SD, (btwSJ - L)))
                curve_pos.append((-SD, (btwSJ)))
                curve_pos.append((-SD, (btwSJ + L)))
                
                CC1_x, CC1_y = -(SD - R), btwSJ + L
                CC2_x, CC2_y = -(2 * sqrt(R ** 2 - (abs(btwSJ + L + CLL / 2 - CC1_y)) ** 2) + SD - R), 2 * btwSJ
                curveCy = CC2_y - CLL / 2  
                curveCx = sqrt(R ** 2 - (abs(curveCy - CC2_y)) ** 2) + CC2_x
                curveEx, curveEy = 0, CC2_y - sqrt(R ** 2 - (CC2_x) ** 2)
                for x in range(4):
                    p_y = CC1_y + (x + 1) * (curveCy - CC1_y) / 5
                    p_x = -sqrt(R ** 2 - (abs(p_y - CC1_y)) ** 2) + CC1_x
                    curve_pos.append((p_x, p_y))
                curve_pos.append((curveCx, curveCy))
                for x in range(3):
                    p_y = curveCy + (x + 1) * (curveEy - curveCy) / 4
                    p_x = sqrt(R ** 2 - (abs(p_y - CC2_y)) ** 2) + CC2_x
                    curve_pos.append((p_x, p_y))
                
                for i, (px, py) in enumerate(curve_pos):
                    NS_OnCurve.append(Node(SN.id + '-' + str(i) + '-' + EN.id, SN.px - px, SN.py - py, DOT))
            if quadrant == 'Q43':
                CC1_x, CC1_y = -(SD - R), -CLL 
                CC2_x, CC2_y = -(2 * sqrt(R ** 2 - (abs(-CLL / 2 - CC1_y)) ** 2) + SD - R), 0
                
                curveSx, curveSy = 0, -sqrt(R ** 2 - (CC2_x) ** 2)
                
                curveCy = -CLL / 2
                curveCx = sqrt(R ** 2 - (abs(curveCy - CC2_y)) ** 2) + CC2_x
                
                curve_pos = []
                
                for x in range(3):
                    p_y = curveSy + (x + 1) * (curveCy - curveSy) / 4
                    p_x = sqrt(R ** 2 - (abs(p_y - CC2_y)) ** 2) + CC2_x
                    curve_pos.append((p_x, p_y))
                curve_pos.append((curveCx, curveCy))
                for x in range(4):
                    p_y = curveCy + (x + 1) * (CC1_y - curveCy) / 5
                    p_x = -sqrt(R ** 2 - (abs(p_y - CC1_y)) ** 2) + CC1_x
                    curve_pos.append((p_x, p_y))
                
                curve_pos.append((-SD, -(btwSJ - L)))
                curve_pos.append((-SD, -(btwSJ)))
                curve_pos.append((-SD, -(btwSJ + L)))
                
                CC1_x, CC1_y = -(SD - R), -(btwSJ + L)
                CC2_x, CC2_y = -(2 * sqrt(R ** 2 - (abs(-1 * (btwSJ + L + CLL / 2) - CC1_y)) ** 2) + SD - R), -2 * btwSJ
                
                curveCy = CC2_y + CLL / 2  
                curveCx = sqrt(R ** 2 - (abs(curveCy - CC2_y)) ** 2) + CC2_x
                curveEx, curveEy = 0, CC2_y + sqrt(R ** 2 - (CC2_x) ** 2)

                for x in range(4):
                    p_y = CC1_y + (x + 1) * (curveCy - CC1_y) / 5
                    p_x = -sqrt(R ** 2 - (abs(p_y - CC1_y)) ** 2) + CC1_x
                    curve_pos.append((p_x, p_y))
                curve_pos.append((curveCx, curveCy))
                for x in range(3):
                    p_y = curveCy + (x + 1) * (curveEy - curveCy) / 4
                    p_x = sqrt(R ** 2 - (abs(p_y - CC2_y)) ** 2) + CC2_x
                    curve_pos.append((p_x, p_y))
                
                for i, (px, py) in enumerate(curve_pos):
                    NS_OnCurve.append(Node(SN.id + '-' + str(i) + '-' + EN.id, SN.px + px, SN.py - py, DOT))
                                
        JDJ_Nodes.append(NS_OnCurve)
    
    numOfNC = 8
    
    for SN_id, EN_id, quadrant, direction in JDJ_pos_info1:
        set_posD_OnCurve1(findN(SN_id), findN(EN_id), quadrant, direction)
        
    def set_posD_OnCurve2(SN, EN, numOfN, quadrant, direction, angle):
        NS_OnCurve = []
        for i in range(numOfN - 1):
            sx = abs(EN.px - SN.px)
            sy = abs(EN.py - SN.py)
            if direction == 'CW':
                if quadrant == 'Q1':
                    C_px, C_py = SN.px, EN.py
                    teata = (pi / 180) * (-90 + angle * ((i + 1) / numOfN))
                if quadrant == 'Q2':
                    C_px, C_py = EN.px, SN.py
                    teata = (pi / 180) * (angle * ((i + 1) / numOfN))
                if quadrant == 'Q3':
                    C_px, C_py = SN.px, EN.py
                    teata = (pi / 180) * (90 + angle * ((i + 1) / numOfN))
                if quadrant == 'Q4':
                    C_px, C_py = EN.px, SN.py
                    teata = (pi / 180) * (180 + angle * ((i + 1) / numOfN))
            else :
                assert direction != 'CW'
                if quadrant == 'Q1':
                    C_px, C_py = EN.px, SN.py
                    teata = (pi / 180) * (-1 * angle * ((i + 1) / numOfN))
                if quadrant == 'Q4':
                    C_px, C_py = SN.px, EN.py
                    teata = (pi / 180) * (-90 - 1 * angle * ((i + 1) / numOfN))
            NS_OnCurve.append(Node(SN.id + '-' + str(i) + '-' + EN.id, C_px + sx * cos(teata) , C_py + sy * sin(teata), DOT))
        JDJ_Nodes.append(NS_OnCurve)

    
    for SN_id, EN_id, numOfN, quadrant in [('12N', '8E', numOfNC, 'Q1'), ('8W', '11N', numOfNC, 'Q4')]:
        set_posD_OnCurve2(findN(SN_id), findN(EN_id), numOfN, quadrant, 'CCW', 90)
    
    JDJ_pos_info2 = [
                    ('0E', '4N', numOfNC, 'Q1'),
                    ('2E', '6N', numOfNC, 'Q1'),
                    ('4S', '7E', numOfNC, 'Q2'),
                    ('6S', '9E', numOfNC, 'Q2'),
                    ('13S', '16E', numOfNC, 'Q2'),
                    ('11S', '14E', numOfNC, 'Q2'),
                    ('7W', '3S', numOfNC, 'Q3'),
                    ('9W', '5S', numOfNC, 'Q3'),
                    ('16W', '12S', numOfNC, 'Q3'),
                    ('14W', '10S', numOfNC, 'Q3'),
                    ('3N', '0W', numOfNC, 'Q4'),
                    ('5N', '2W', numOfNC, 'Q4')
                   ]
    
    for SN_id, EN_id, numOfN, quadrant in JDJ_pos_info2:
        set_posD_OnCurve2(findN(SN_id), findN(EN_id), numOfN, quadrant, 'CW', 90)
    
    Nodes = S_Nodes + J_Nodes + [x for x in chain(*JDJ_Nodes)]
    
    Edges = []
    
    for i in range(len(S_Nodes)):
        Nid = S_Nodes[i].id
        if (0 <= i <= 2):
            Edges.append(Edge(findN(Nid + 'W'), findN(Nid), S2J_SPEED))
            Edges.append(Edge(findN(Nid), findN(Nid + 'E'), S2J_SPEED))
            
        elif (7 <= i <= 9) or (14 <= i <= 16):
            Edges.append(Edge(findN(Nid), findN(Nid + 'W'), S2J_SPEED))
            Edges.append(Edge(findN(Nid + 'E'), findN(Nid), S2J_SPEED))
        else:
            if Nid in ['3', '5', '10', '12']:
                Edges.append(Edge(findN(Nid + 'S'), findN(Nid), S2J_SPEED))
                Edges.append(Edge(findN(Nid), findN(Nid + 'N'), S2J_SPEED))
            else:
                Edges.append(Edge(findN(Nid), findN(Nid + 'S'), S2J_SPEED))
                Edges.append(Edge(findN(Nid + 'N'), findN(Nid) , S2J_SPEED))
    
    Edges.append(Edge(findN('0E'), findN('1W')))
    Edges.append(Edge(findN('1E'), findN('2W')))
    Edges.append(Edge(findN('6S'), findN('13N')))
    Edges.append(Edge(findN('16W'), findN('15E')))
    Edges.append(Edge(findN('15W'), findN('14E')))
    Edges.append(Edge(findN('16W'), findN('15E')))
    Edges.append(Edge(findN('10N'), findN('3S')))
    Edges.append(Edge(findN('8W'), findN('7E')))
    Edges.append(Edge(findN('12N'), findN('5S')))
    
    for JD2N in JDJ_Nodes:
        if JD2N: 
            SN_id, _, EN_id = JD2N[0].id.split('-')
            Edges.append(Edge(findN(SN_id), JD2N[0], J2D_SPEED))
            for i, n in enumerate(JD2N):
                if i == len(JD2N) - 1:
                    Edges.append(Edge(JD2N[-1], findN(EN_id), J2D_SPEED))
                    break
                Edges.append(Edge(JD2N[i], JD2N[i + 1]))
    
    for i, n in enumerate(Nodes):
        n.no = i
        
    return Nodes, Edges
    
'''
import wx
STATION_DIAMETER = 8
JUNCTION_DIAMETER = 5

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'Network', size=(1024, 768), pos=(20, 20))
        self.Nodes, self.Customers, self.PRTs, _ = ex1()
        
        self.vp = ViewPanel(self, self.Nodes)

from util import DragZoomPanel    

class ViewPanel(DragZoomPanel):
    def __init__(self, parent, Nodes):
        DragZoomPanel.__init__(self, parent, -1, style=wx.SUNKEN_BORDER)
        self.SetBackgroundColour(wx.WHITE)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        
        self.Nodes = Nodes
    
    def OnMouseWheel(self, e):
        if e.ControlDown():
            win.OnSpeedUp(None) if e.m_wheelRotation > 0 else win.OnSpeedDown(None)
        else:
            DragZoomPanel.OnMouseWheel(self, e)
        # self.set_scale(self.scale * (self.scale_inc if e.m_wheelRotation > 0 else (1 / self.scale_inc)), e.m_x, e.m_y)
        # self.RefreshGC()

    def OnDrawDevice(self, gc):
        pass
    
    def OnDraw(self, gc):
        old_tr = gc.GetTransform()
        for n in self.Nodes:
            gc.Translate(n.px, n.py)
            if n.nodeType == 0 or n.nodeType == 1:
                gc.SetBrush(wx.Brush(wx.Colour(255, 255, 255)))
                gc.SetPen(wx.Pen(wx.Colour(0, 0, 0), 1))
                gc.DrawEllipse(-STATION_DIAMETER / 2, -STATION_DIAMETER / 2, STATION_DIAMETER, STATION_DIAMETER)
            elif n.nodeType == 2:
                gc.SetBrush(wx.Brush(wx.Colour(255, 255, 255)))
                gc.SetPen(wx.Pen(wx.Colour(0, 0, 0), 0.01))
                gc.DrawEllipse(-JUNCTION_DIAMETER / 2, -JUNCTION_DIAMETER / 2, JUNCTION_DIAMETER, JUNCTION_DIAMETER)
            else:
                assert n.nodeType == 3
#                 gc.SetBrush(wx.Brush(wx.Colour(255, 255, 255)))
#                 gc.SetPen(wx.Pen(wx.Colour(0, 0, 0), 0.01))
#                 gc.DrawEllipse(-1, -1, 2, 2)    
            gc.SetTransform(old_tr)
  '''  
if __name__ == '__main__':
    ex1()
#     app = wx.PySimpleApp()
#     win = MainFrame()
#     win.Show(True)
#     app.MainLoop()
    
        
