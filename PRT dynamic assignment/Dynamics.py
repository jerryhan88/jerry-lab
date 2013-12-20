from __future__ import division
from math import sqrt, pi, cos, sin
from random import randrange, seed, expovariate, random, choice, sample, uniform
from heapq import heappush, heappop
from itertools import chain
import Algorithms
#---------------------------------------------------------------------
# Network example
TRANSFER, STATION, JUNCTION, DOT = range(4)
S2J_SPEED = 6
J2D_SPEED = 9

numOfBerth = 3

def findNode(nID):
    for n in Nodes:
        if n.id == nID:
            return n
    else:
        False
def Network2():
    C_len = [0, 210, 150, 200, 230, 180, 200]
    C = [sum(C_len[:i + 1]) for i in range(len(C_len))]
    
    R_len = [0, 150, 180, 160, 210]
    R = [sum(R_len[:i + 1]) for i in range(len(R_len))]
    
    btwSJ = 70
    btwSD = 30
    S_Nodes = [
             Node('0', C[1] - 50, R[0], STATION), Node('1', C[3] + 30, R[0], STATION), Node('2', C[5], R[0], STATION),
             Node('3', C[0], R[1] + 25, TRANSFER), Node('4', C[2], R[1], STATION), Node('5', C[4], R[1] - 15, STATION), Node('6', C[6], R[1] + 20, STATION),
             Node('7', C[1], R[2], STATION), Node('8', C[3] + 20, R[2], STATION), Node('9', C[5], R[2] + 10, STATION),
             Node('10', C[0], R[3] + 40, STATION), Node('11', C[2], R[3], STATION), Node('12', C[4], R[3] + 20, STATION), Node('13', C[6], R[3] + 50, STATION),
             Node('14', C[1] - 20, R[4], STATION), Node('15', C[3] - 15, R[4], STATION), Node('16', C[5] + 25, R[4], STATION),
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
    numOfNC = 10
    JDJ_pos_info1 = [
                    ('0W', '0E', numOfNC, 'Q41', 'CW'),
                    ('0E', '0W', numOfNC, 'Q32', 'CW'),
                    ('1W', '1E', numOfNC, 'Q32', 'CCW'),
                    ('1E', '1W', numOfNC, 'Q41', 'CCW'),
                    ('2W', '2E', numOfNC, 'Q41', 'CW'),
                    ('2E', '2W', numOfNC, 'Q32', 'CW'),
                    ('7E', '7W', numOfNC, 'Q32', 'CW'),
                    ('7W', '7E', numOfNC, 'Q41', 'CW'),
                    ('8E', '8W', numOfNC, 'Q41', 'CCW'),
                    ('8W', '8E', numOfNC, 'Q32', 'CCW'),
                    ('9E', '9W', numOfNC, 'Q32', 'CW'),
                    ('9W', '9E', numOfNC, 'Q41', 'CW'),
                    ('14E', '14W', numOfNC, 'Q41', 'CCW'),
                    ('14W', '14E', numOfNC, 'Q32', 'CCW'),
                    ('15E', '15W', numOfNC, 'Q32', 'CW'),
                    ('15W', '15E', numOfNC, 'Q41', 'CW'),
                    ('16E', '16W', numOfNC, 'Q41', 'CCW'),
                    ('16W', '16E', numOfNC, 'Q32', 'CCW'),
                    
                    ('3S', '3N', numOfNC, 'Q21', 'CCW'),
                    ('3N', '3S', numOfNC, 'Q43', 'CCW'),
                    ('4N', '4S', numOfNC, 'Q43', 'CCW'),
                    ('4S', '4N', numOfNC, 'Q21', 'CCW'),
                    ('5S', '5N', numOfNC, 'Q21', 'CCW'),
                    ('5N', '5S', numOfNC, 'Q43', 'CCW'),
                    ('6N', '6S', numOfNC, 'Q43', 'CCW'),
                    ('6S', '6N', numOfNC, 'Q21', 'CCW'),
                    ('10S', '10N', numOfNC, 'Q43', 'CW'),
                    ('10N', '10S', numOfNC, 'Q21', 'CW'),
                    ('11N', '11S', numOfNC, 'Q21', 'CW'),
                    ('11S', '11N', numOfNC, 'Q43', 'CW'),
                    ('12S', '12N', numOfNC, 'Q43', 'CW'),
                    ('12N', '12S', numOfNC, 'Q21', 'CW'),
                    ('13N', '13S', numOfNC, 'Q21', 'CW'),
                    ('13S', '13N', numOfNC, 'Q43', 'CW'),
                    ]
    
    def set_posD_OnCurve1(SN, EN, numOfN, quadrant, direction, angle):
        NS_OnCurve = []
        for i in range(numOfN - 1):
            C_px = (SN.px + EN.px) / 2
            C_py = (SN.py + EN.py) / 2
            if quadrant == 'Q32' or quadrant == 'Q41':
                sx = abs(SN.px - EN.px) / 2
                sy = btwSD
            else:
                sx = btwSD
                sy = abs(SN.py - EN.py) / 2
            if direction == 'CW':
                if quadrant == 'Q21':
                    teata = (pi / 180) * (-90 + angle * ((i + 1) / numOfN))
                if quadrant == 'Q43':
                    teata = (pi / 180) * (90 + angle * ((i + 1) / numOfN))
                if quadrant == 'Q32':
                    teata = (pi / 180) * (angle * ((i + 1) / numOfN))
                if quadrant == 'Q41': 
                    teata = (pi / 180) * (180 + angle * ((i + 1) / numOfN))
            else:
                assert direction != 'CW'
                if quadrant == 'Q21':
                    teata = (pi / 180) * (90 - 1 * angle * ((i + 1) / numOfN))
                if quadrant == 'Q43':
                    teata = (pi / 180) * (-90 - 1 * angle * ((i + 1) / numOfN))
                if quadrant == 'Q41':
                    teata = (pi / 180) * (-1 * angle * ((i + 1) / numOfN))
                if quadrant == 'Q32':
                    teata = (pi / 180) * (180 + -1 * angle * ((i + 1) / numOfN))
                    
            NS_OnCurve.append(Node(SN.id + '-' + str(i) + '-' + EN.id, C_px + sx * cos(teata) , C_py + sy * sin(teata), DOT))
        JDJ_Nodes.append(NS_OnCurve)
    
    numOfNC = 8
    
    for SN_id, EN_id, numOfN, quadrant, direction in JDJ_pos_info1:
        set_posD_OnCurve1(findN(SN_id), findN(EN_id), numOfN, quadrant, direction, 180)
        
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

def Network1():
    c0 = 0
    c1 = c0 + 450
    c2 = c1 + 350
    c3 = c2 + 500
    
    r0 = 0
    r1 = r0 + 300 
    r2 = r1 + 500
    r3 = r2 + 450
    
    btwSJ = 70
    
    global Nodes
    Nodes = [
                Node('1', c0, r0, STATION), Node('1E', c0 + btwSJ, r0, JUNCTION), Node('1S', c0, r0 + btwSJ, JUNCTION),
                Node('2', c1, r0, STATION), Node('2E', c1 + btwSJ, r0, JUNCTION), Node('2W', c1 - btwSJ, r0, JUNCTION), Node('2S', c1, r0 + btwSJ, JUNCTION),
                Node('3', c2, r0, STATION), Node('3W', c2 - btwSJ, r0, JUNCTION), Node('3S', c2, r0 + btwSJ, JUNCTION),
                Node('4', c0, r1, STATION), Node('4E', c0 + btwSJ, r1, JUNCTION), Node('4N', c0, r1 - btwSJ, JUNCTION), Node('4S', c0, r1 + btwSJ, JUNCTION),
                Node('5', c1, r1, TRANSFER), Node('5E', c1 + btwSJ, r1, JUNCTION), Node('5W', c1 - btwSJ, r1, JUNCTION), Node('5N', c1, r1 - btwSJ, JUNCTION), Node('5S', c1, r1 + btwSJ, JUNCTION),
                Node('6', c2, r1, STATION), Node('6E', c2 + btwSJ, r1, JUNCTION), Node('6W', c2 - btwSJ, r1, JUNCTION), Node('6S', c2, r1 + btwSJ, JUNCTION), Node('6N', c2, r1 - btwSJ, JUNCTION),
                Node('7', c3, r1, STATION), Node('7W', c3 - btwSJ, r1, JUNCTION), Node('7S', c3, r1 + btwSJ, JUNCTION),
                Node('8', c0, r2, STATION), Node('8E', c0 + btwSJ, r2, JUNCTION), Node('8N', c0, r2 - btwSJ, JUNCTION),
                Node('9', c1, r2, STATION), Node('9E', c1 + btwSJ, r2, JUNCTION), Node('9W', c1 - btwSJ, r2, JUNCTION), Node('9S', c1, r2 + btwSJ, JUNCTION), Node('9N', c1, r2 - btwSJ, JUNCTION),
                Node('10', c2, r2, STATION), Node('10E', c2 + btwSJ, r2, JUNCTION), Node('10W', c2 - btwSJ, r2, JUNCTION), Node('10S', c2, r2 + btwSJ, JUNCTION), Node('10N', c2, r2 - btwSJ, JUNCTION),
                Node('11', c3, r2, STATION), Node('11W', c3 - btwSJ, r2, JUNCTION), Node('11S', c3, r2 + btwSJ, JUNCTION), Node('11N', c3, r2 - btwSJ, JUNCTION),
                Node('12', c1, r3, STATION), Node('12E', c1 + btwSJ, r3, JUNCTION), Node('12N', c1, r3 - btwSJ, JUNCTION),
                Node('13', c2, r3, STATION), Node('13E', c2 + btwSJ, r3, JUNCTION), Node('13W', c2 - btwSJ, r3, JUNCTION), Node('13N', c2, r3 - btwSJ, JUNCTION),
                Node('14', c3, r3, STATION), Node('14W', c3 - btwSJ, r3, JUNCTION), Node('14N', c3, r3 - btwSJ, JUNCTION),
                
                Node('3E', c2 + btwSJ, r0, JUNCTION),
                Node('3-7.D1', c3 - ((r1 - r0) - btwSJ) + ((r1 - r0) - btwSJ) * cos((pi / 180) * -90 * (11 / 11)), r1 - btwSJ + ((r1 - r0) - btwSJ) * sin((pi / 180) * -90 * (11 / 11)), DOT),
                Node('3-7.D2', c3 - ((r1 - r0) - btwSJ) + ((r1 - r0) - btwSJ) * cos((pi / 180) * -90 * (10 / 11)), r1 - btwSJ + ((r1 - r0) - btwSJ) * sin((pi / 180) * -90 * (10 / 11)), DOT),
                Node('3-7.D3', c3 - ((r1 - r0) - btwSJ) + ((r1 - r0) - btwSJ) * cos((pi / 180) * -90 * (9 / 11)), r1 - btwSJ + ((r1 - r0) - btwSJ) * sin((pi / 180) * -90 * (9 / 11)), DOT),
                Node('3-7.D4', c3 - ((r1 - r0) - btwSJ) + ((r1 - r0) - btwSJ) * cos((pi / 180) * -90 * (8 / 11)), r1 - btwSJ + ((r1 - r0) - btwSJ) * sin((pi / 180) * -90 * (8 / 11)), DOT),
                Node('3-7.D5', c3 - ((r1 - r0) - btwSJ) + ((r1 - r0) - btwSJ) * cos((pi / 180) * -90 * (7 / 11)), r1 - btwSJ + ((r1 - r0) - btwSJ) * sin((pi / 180) * -90 * (7 / 11)), DOT),
                Node('3-7.D6', c3 - ((r1 - r0) - btwSJ) + ((r1 - r0) - btwSJ) * cos((pi / 180) * -90 * (6 / 11)), r1 - btwSJ + ((r1 - r0) - btwSJ) * sin((pi / 180) * -90 * (6 / 11)), DOT),
                Node('3-7.D7', c3 - ((r1 - r0) - btwSJ) + ((r1 - r0) - btwSJ) * cos((pi / 180) * -90 * (5 / 11)), r1 - btwSJ + ((r1 - r0) - btwSJ) * sin((pi / 180) * -90 * (5 / 11)), DOT),
                Node('3-7.D8', c3 - ((r1 - r0) - btwSJ) + ((r1 - r0) - btwSJ) * cos((pi / 180) * -90 * (4 / 11)), r1 - btwSJ + ((r1 - r0) - btwSJ) * sin((pi / 180) * -90 * (4 / 11)), DOT),
                Node('3-7.D9', c3 - ((r1 - r0) - btwSJ) + ((r1 - r0) - btwSJ) * cos((pi / 180) * -90 * (3 / 11)), r1 - btwSJ + ((r1 - r0) - btwSJ) * sin((pi / 180) * -90 * (3 / 11)), DOT),
                Node('3-7.D10', c3 - ((r1 - r0) - btwSJ) + ((r1 - r0) - btwSJ) * cos((pi / 180) * -90 * (2 / 11)), r1 - btwSJ + ((r1 - r0) - btwSJ) * sin((pi / 180) * -90 * (2 / 11)), DOT),
                Node('3-7.D11', c3 - ((r1 - r0) - btwSJ) + ((r1 - r0) - btwSJ) * cos((pi / 180) * -90 * (1 / 11)), r1 - btwSJ + ((r1 - r0) - btwSJ) * sin((pi / 180) * -90 * (1 / 11)), DOT),
                Node('7N', c3, r1 - btwSJ, JUNCTION),
                
                Node('12W', c1 - btwSJ, r3, JUNCTION),
                Node('12-8.D1', c1 - btwSJ + ((c1 - c0) - btwSJ) * cos((pi / 180) * (-180 + -90 * (10 / 11))), r2 + btwSJ + ((c1 - c0) - btwSJ) * sin((pi / 180) * (-180 + -90 * (10 / 11))), DOT),
                Node('12-8.D2', c1 - btwSJ + ((c1 - c0) - btwSJ) * cos((pi / 180) * (-180 + -90 * (9 / 11))), r2 + btwSJ + ((c1 - c0) - btwSJ) * sin((pi / 180) * (-180 + -90 * (9 / 11))), DOT),
                Node('12-8.D3', c1 - btwSJ + ((c1 - c0) - btwSJ) * cos((pi / 180) * (-180 + -90 * (8 / 11))), r2 + btwSJ + ((c1 - c0) - btwSJ) * sin((pi / 180) * (-180 + -90 * (8 / 11))), DOT),
                Node('12-8.D4', c1 - btwSJ + ((c1 - c0) - btwSJ) * cos((pi / 180) * (-180 + -90 * (7 / 11))), r2 + btwSJ + ((c1 - c0) - btwSJ) * sin((pi / 180) * (-180 + -90 * (7 / 11))), DOT),
                Node('12-8.D5', c1 - btwSJ + ((c1 - c0) - btwSJ) * cos((pi / 180) * (-180 + -90 * (6 / 11))), r2 + btwSJ + ((c1 - c0) - btwSJ) * sin((pi / 180) * (-180 + -90 * (6 / 11))), DOT),
                Node('12-8.D6', c1 - btwSJ + ((c1 - c0) - btwSJ) * cos((pi / 180) * (-180 + -90 * (5 / 11))), r2 + btwSJ + ((c1 - c0) - btwSJ) * sin((pi / 180) * (-180 + -90 * (5 / 11))), DOT),
                Node('12-8.D7', c1 - btwSJ + ((c1 - c0) - btwSJ) * cos((pi / 180) * (-180 + -90 * (4 / 11))), r2 + btwSJ + ((c1 - c0) - btwSJ) * sin((pi / 180) * (-180 + -90 * (4 / 11))), DOT),
                Node('12-8.D8', c1 - btwSJ + ((c1 - c0) - btwSJ) * cos((pi / 180) * (-180 + -90 * (3 / 11))), r2 + btwSJ + ((c1 - c0) - btwSJ) * sin((pi / 180) * (-180 + -90 * (3 / 11))), DOT),
                Node('12-8.D9', c1 - btwSJ + ((c1 - c0) - btwSJ) * cos((pi / 180) * (-180 + -90 * (2 / 11))), r2 + btwSJ + ((c1 - c0) - btwSJ) * sin((pi / 180) * (-180 + -90 * (2 / 11))), DOT),
                Node('12-8.D10', c1 - btwSJ + ((c1 - c0) - btwSJ) * cos((pi / 180) * (-180 + -90 * (1 / 11))), r2 + btwSJ + ((c1 - c0) - btwSJ) * sin((pi / 180) * (-180 + -90 * (1 / 11))), DOT),
                Node('8S', c0, r2 + btwSJ, JUNCTION),
           ]
    
    Edges = [
                Edge(findNode('1'), findNode('1E'), S2J_SPEED), Edge(findNode('1S'), findNode('1'), S2J_SPEED),
                Edge(findNode('2W'), findNode('2'), S2J_SPEED), Edge(findNode('2E'), findNode('2'), S2J_SPEED), Edge(findNode('2'), findNode('2S'), S2J_SPEED),
                Edge(findNode('3'), findNode('3W'), S2J_SPEED), Edge(findNode('3'), findNode('3E'), S2J_SPEED), Edge(findNode('3S'), findNode('3'), S2J_SPEED),
                Edge(findNode('4E'), findNode('4'), S2J_SPEED), Edge(findNode('4'), findNode('4S'), S2J_SPEED), Edge(findNode('4'), findNode('4N'), S2J_SPEED),
                Edge(findNode('5'), findNode('5E'), S2J_SPEED), Edge(findNode('5'), findNode('5W'), S2J_SPEED), Edge(findNode('5S'), findNode('5'), S2J_SPEED), Edge(findNode('5N'), findNode('5'), S2J_SPEED),
                Edge(findNode('6E'), findNode('6'), S2J_SPEED), Edge(findNode('6W'), findNode('6'), S2J_SPEED), Edge(findNode('6'), findNode('6S'), S2J_SPEED), Edge(findNode('6'), findNode('6N'), S2J_SPEED),
                Edge(findNode('7'), findNode('7W'), S2J_SPEED), Edge(findNode('7S'), findNode('7'), S2J_SPEED), Edge(findNode('7N'), findNode('7'), S2J_SPEED),
                Edge(findNode('8'), findNode('8E'), S2J_SPEED), Edge(findNode('8S'), findNode('8'), S2J_SPEED), Edge(findNode('8N'), findNode('8'), S2J_SPEED),
                Edge(findNode('9E'), findNode('9'), S2J_SPEED), Edge(findNode('9W'), findNode('9'), S2J_SPEED), Edge(findNode('9'), findNode('9S'), S2J_SPEED), Edge(findNode('9'), findNode('9N'), S2J_SPEED),
                Edge(findNode('10'), findNode('10E'), S2J_SPEED), Edge(findNode('10'), findNode('10W'), S2J_SPEED), Edge(findNode('10S'), findNode('10'), S2J_SPEED), Edge(findNode('10N'), findNode('10'), S2J_SPEED),
                Edge(findNode('11W'), findNode('11'), S2J_SPEED), Edge(findNode('11'), findNode('11S'), S2J_SPEED), Edge(findNode('11'), findNode('11N'), S2J_SPEED),
                Edge(findNode('12'), findNode('12E'), S2J_SPEED), Edge(findNode('12'), findNode('12W'), S2J_SPEED), Edge(findNode('12N'), findNode('12'), S2J_SPEED),
                Edge(findNode('13W'), findNode('13'), S2J_SPEED), Edge(findNode('13E'), findNode('13'), S2J_SPEED), Edge(findNode('13'), findNode('13N'), S2J_SPEED),
                Edge(findNode('14'), findNode('14W'), S2J_SPEED), Edge(findNode('14N'), findNode('14'), S2J_SPEED),
                
                Edge(findNode('1E'), findNode('2W')), Edge(findNode('3W'), findNode('2E')),
                Edge(findNode('4N'), findNode('1S')), Edge(findNode('2S'), findNode('5N')), Edge(findNode('6N'), findNode('3S')),
                Edge(findNode('5W'), findNode('4E')), Edge(findNode('5E'), findNode('6W')), Edge(findNode('7W'), findNode('6E')),
                Edge(findNode('4S'), findNode('8N')), Edge(findNode('9N'), findNode('5S')), Edge(findNode('6S'), findNode('10N')), Edge(findNode('11N'), findNode('7S')),
                Edge(findNode('8E'), findNode('9W')), Edge(findNode('10W'), findNode('9E')), Edge(findNode('10E'), findNode('11W')),
                Edge(findNode('9S'), findNode('12N')), Edge(findNode('13N'), findNode('10S')), Edge(findNode('11S'), findNode('14N')),
                Edge(findNode('12E'), findNode('13W')), Edge(findNode('14W'), findNode('13E')),
                
                Edge(findNode('1S'), findNode('1E')),
                Edge(findNode('2E'), findNode('2S')), Edge(findNode('2W'), findNode('2S')),
                Edge(findNode('3S'), findNode('3E')), Edge(findNode('3S'), findNode('3W')),
                Edge(findNode('4E'), findNode('4S')), Edge(findNode('4E'), findNode('4N')),
                Edge(findNode('5S'), findNode('5E')), Edge(findNode('5S'), findNode('5W')), Edge(findNode('5N'), findNode('5E')), Edge(findNode('5N'), findNode('5W')),
                Edge(findNode('6E'), findNode('6S')), Edge(findNode('6W'), findNode('6S')), Edge(findNode('6E'), findNode('6N')), Edge(findNode('6W'), findNode('6N')),
                Edge(findNode('7S'), findNode('7W')), Edge(findNode('7N'), findNode('7W')),
                Edge(findNode('8S'), findNode('8E')), Edge(findNode('8N'), findNode('8E')),
                Edge(findNode('9E'), findNode('9S')), Edge(findNode('9W'), findNode('9S')), Edge(findNode('9E'), findNode('9N')), Edge(findNode('9W'), findNode('9N')),
                Edge(findNode('10S'), findNode('10E')), Edge(findNode('10S'), findNode('10W')), Edge(findNode('10N'), findNode('10E')), Edge(findNode('10N'), findNode('10W')),
                Edge(findNode('11W'), findNode('11S')), Edge(findNode('11W'), findNode('11N')),
                Edge(findNode('12N'), findNode('12E')), Edge(findNode('12N'), findNode('12W')),
                Edge(findNode('13E'), findNode('13N')), Edge(findNode('13W'), findNode('13N')),
                Edge(findNode('14N'), findNode('14W')),
                
                Edge(findNode('3E'), findNode('3-7.D1')), Edge(findNode('3-7.D1'), findNode('3-7.D2')), Edge(findNode('3-7.D2'), findNode('3-7.D3')),
                Edge(findNode('3-7.D3'), findNode('3-7.D4')), Edge(findNode('3-7.D4'), findNode('3-7.D5')), Edge(findNode('3-7.D5'), findNode('3-7.D6')),
                Edge(findNode('3-7.D6'), findNode('3-7.D7')), Edge(findNode('3-7.D7'), findNode('3-7.D8')), Edge(findNode('3-7.D8'), findNode('3-7.D9')),
                Edge(findNode('3-7.D9'), findNode('3-7.D10')), Edge(findNode('3-7.D10'), findNode('3-7.D11')), Edge(findNode('3-7.D11'), findNode('7N')),
                
                Edge(findNode('12W'), findNode('12-8.D1')), Edge(findNode('12-8.D1'), findNode('12-8.D2')), Edge(findNode('12-8.D2'), findNode('12-8.D3')),
                Edge(findNode('12-8.D3'), findNode('12-8.D4')), Edge(findNode('12-8.D4'), findNode('12-8.D5')), Edge(findNode('12-8.D5'), findNode('12-8.D6')),
                Edge(findNode('12-8.D6'), findNode('12-8.D7')), Edge(findNode('12-8.D7'), findNode('12-8.D8')), Edge(findNode('12-8.D8'), findNode('12-8.D9')),
                Edge(findNode('12-8.D9'), findNode('12-8.D10')), Edge(findNode('12-8.D10'), findNode('8S')),
            
             ]    
    for i, n in enumerate(Nodes):
        n.no = i
        
    return Nodes, Edges


#---------------------------------------------------------------------
# For calculating measure
Total_empty_travel_distance = 0.0
NumOfPickedUpCustomer = 0

Total_travel_distance = 0.0
Total_customers_flow_time = 0.0
NumOfServicedCustomer = 0

Total_customers_waiting_time = 0.0
NumOfWaitingCustomer = 0
ChaningPointOfNWC = 0.0
MaxCustomerWaitingTime = 0.0

IdleState_time = 0.0
ApproachingState_time = 0.0
SettingState_time = 0.0
TransitingState_time = 0.0
ParkingState_time = 0.0

NumOfCustomerArrivals = 0

#---------------------------------------------------------------------
# For charting measure
WaitingCustomerChanges = []
WaitingTimeChanges = []

#---------------------------------------------------------------------
# Classes

class Node():
    BIG_NUM = 1000000
    def __init__(self, _id, px, py, nodeType):
        self.id = _id
        self.px, self.py = px, py
        self.nodeType = nodeType
        self.no = None
        self.settingPRTs = []
        self.waitingPRTs = [] 
        
        self.edges_inward = []
        self.edges_outward = []
        
    def init_node(self):
        self.visited = False
        self.visitiedCount = 0
        self.minTime = Node.BIG_NUM
    
    def __repr__(self):
        return '%s' % (self.id)
    
class Edge():
    _id = 0
    def __init__(self, _from, _to, maxSpeed=12):
        self.id = Edge._id
        Edge._id += 1
        self._from, self._to = _from, _to
        self.maxSpeed = maxSpeed
        
        delX = self._from.px - self._to.px
        delY = self._from.py - self._to.py
        self.distance = sqrt(delX * delX + delY * delY)
        
        self._from.edges_outward.append(self)
        self._to.edges_inward.append(self)
        
    def __repr__(self):
        return '%s->%s' % (self._from.id, self._to.id)

class Customer():
    def __init__(self, _id, arriving_time, sn, dn):
        self.id = _id
        self.arriving_time = arriving_time
        self.sn, self.dn = sn, dn
        
        self.assigned_PRT = None
    
    def __repr__(self):
        return '(C%d) %s->%s' % (self.id, self.sn.id, self.dn.id)

ST_IDLE, ST_APPROACHING, ST_SETTING, ST_TRANSITING, ST_PARKING = range(5)

class PRT():
    _id = 0
    def __init__(self, init_node):
        self.id = PRT._id
        PRT._id += 1
        self.arrived_n = init_node
        self.px, self.py = self.arrived_n.px, self.arrived_n.py
        
        self.state = ST_IDLE
        self.stateChangingPoint = 0.0
        self.assigned_customer = None
        self.transporting_customer = None
        self.event_seq = []
        self.isWaiting = False
        
        self.last_planed_time = 0.0
        self.path_n, self.path_e = [], []
    
    def __repr__(self):
        return 'PRT%d(S%d-%s)' % (self.id, self.state, self.arrived_n.id)
    
    def set_stateChange(self, state, cur_time):
        self.state, self.stateChangingPoint = state, cur_time
    
    def find_target_event_inEventSeq(self, cur_time, target_prt, event_name, args=None):
        if isinstance(args, Customer):
            for evt in target_prt.event_seq[::-1]:
                if evt[1] == event_name and evt[2] == args:
                    assert evt[0] >= cur_time
                    return evt  
            else:
                assert False
        else:
            for i, evt in enumerate(target_prt.event_seq[::-1]):
                if evt[1] == event_name:
                    assert evt[0] >= cur_time and target_prt.event_seq[len(target_prt.event_seq) - 2 - i][1] == args
                    return evt, target_prt.event_seq[len(target_prt.event_seq) - 2 - i]
            else:
                assert False
    
    def modify_passed_assignedPRT_event(self, cur_time, prev_PRT, target_c):
        # Modify event of tager_c's previous assigned PRT which is already scheduled
        if not prev_PRT:
            return None
        else:
            logger('                    There is the prev PRT for the target customer: %s' % (prev_PRT))
            if prev_PRT.assigned_customer == target_c:
                # Change event of On_ApproachingToTransiting on prev_PRT's event_seq
                A2T_EVT = self.find_target_event_inEventSeq(cur_time, prev_PRT, prev_PRT.On_ApproachingToSetting, target_c)
                assert A2T_EVT 
                A2T_EVT[1] = None
                x = [cur_time, prev_PRT.On_ApproachingToParking, target_c]
                prev_PRT.event_seq.append(x)
                prev_PRT.On_ApproachingToParking(cur_time, target_c)
            else:
                assert prev_PRT.assigned_customer != target_c
    
    def re_assign_customer(self, cur_time, target_c):
        if self.state == ST_IDLE :
            if self.arrived_n != target_c.sn:
                # Idle -> Approaching
                x = [cur_time, self.On_IdleToApproaching, target_c]
                self.event_seq.append(x)
                self.On_IdleToApproaching(cur_time, target_c)
            else:
                # self.arrived_n == target_c.sn
                # Idle -> Transiting
                x = [cur_time, self.On_IdleToSetting, target_c]
                self.event_seq.append(x)
                self.On_IdleToSetting(cur_time, target_c)
        elif self.state == ST_APPROACHING:
            if self.assigned_customer != target_c:
                # Approaching -> Approaching
                # Even though this PRT approaching assigned customer
                # the PRT assigned to target_c has been changed
                x = [cur_time, self.On_ApproachingToApproaching, target_c]
                self.event_seq.append(x)
                self.On_ApproachingToApproaching(cur_time, target_c)
            else:
                # There is no assigned customer change
                assert self.assigned_customer == target_c
        elif self.state == ST_PARKING:
            if self.event_seq[-1][1] == self.On_ParkingToIdle and self.event_seq[-2][1] == self.On_ApproachingToParking:
                # This PRT temporally becomes parking state, but it is going to be approaching soon
                # This situation can be happened, because an assignment is processed by step by step
                x = [cur_time, self.On_ApproachingToApproaching, target_c]
                self.event_seq.append(x)
                self.On_ApproachingToApproaching(cur_time, target_c)
            else:
                assert False
        else:
            assert self.state == ST_TRANSITING
    
    def On_IdleToSetting(self, cur_time, target_c):
        logger('%.1f:    On_I2S - %s, ready for customer %s' % (cur_time, self, target_c))
        assert self.state == ST_IDLE
        prev_PRT = target_c.assigned_PRT
        
        # Measure update
        global IdleState_time, Total_empty_travel_distance, Total_travel_distance, Total_customers_flow_time, NumOfPickedUpCustomer, NumOfServicedCustomer
        IdleState_time += cur_time - self.stateChangingPoint
        NumOfPickedUpCustomer += 1
        update_customerWaitingTimeMeasure(cur_time, -1)
            
        # State update
        self.set_stateChange(ST_SETTING, cur_time)
        self.transporting_customer = remove_A_customerInWaitingList(target_c)
        assert self.transporting_customer
        self.transporting_customer.assigned_PRT = self
        self.arrived_n.settingPRTs.append(self)
        
        # Set things for next state
        seed(2)
        evt_change_point = cur_time + uniform(*SETTING_TIME)
        x = [evt_change_point, self.On_SettingToTransiting, target_c]
        self.event_seq.append(x)
        heappush(event_queue, x)
        
        # Modify event of tager_c's previous assigned PRT which is already scheduled
        self.modify_passed_assignedPRT_event(cur_time, prev_PRT, target_c)
    
    def On_IdleToApproaching(self, cur_time, target_c):
        logger('%.1f:    On_I2A - %s, assigned customer %s' % (cur_time, self, target_c))
        assert self.state == ST_IDLE
        prev_PRT = target_c.assigned_PRT
        
        # Measure update
        global IdleState_time
        IdleState_time += cur_time - self.stateChangingPoint
        
        # State update
        self.set_stateChange(ST_APPROACHING, cur_time)
        self.assigned_customer = target_c
        target_c.assigned_PRT = self
        
        # Set things for next state
        self.path_n, self.path_e = Algorithms.find_SP(self.arrived_n.no, self.assigned_customer.sn.no)
        self.last_planed_time = cur_time
        evt_change_point = cur_time + sum(e.distance // min(PRT_SPEED, e.maxSpeed) for e in self.path_e)
        x = [evt_change_point, self.On_ApproachingToSetting, target_c]
        self.event_seq.append(x)
        heappush(event_queue, x)

        logger('            path: %s' % (self.path_n))
        
        # Modify event of tager_c's previous assigned PRT which is already scheduled
        self.modify_passed_assignedPRT_event(cur_time, prev_PRT, target_c)

    def On_ApproachingToSetting(self, cur_time, target_c):
        logger('%.1f:    On_A2S - %s, ready for customer %s' % (cur_time, self, target_c))
        assert self.state == ST_APPROACHING and self.assigned_customer == target_c
        
        # Measure update
        global ApproachingState_time, NumOfPickedUpCustomer, Total_empty_travel_distance, Total_travel_distance
        ApproachingState_time += cur_time - self.stateChangingPoint
        NumOfPickedUpCustomer += 1
        path_travel_time = cur_time - self.last_planed_time
        travel_distance = sum(e.distance for e in self.path_e)
        Total_empty_travel_distance += travel_distance 
        Total_travel_distance += travel_distance
        update_customerWaitingTimeMeasure(cur_time, -1)
        
        # State update
        self.set_stateChange(ST_SETTING, cur_time)
        self.arrived_n = self.assigned_customer.sn
        self.transporting_customer = remove_A_customerInWaitingList(self.assigned_customer)
        assert self.transporting_customer
        self.assigned_customer = None
        self.arrived_n.settingPRTs.append(self)
        
        # Set things for next state
        seed(2)
        evt_change_point = cur_time + uniform(*SETTING_TIME)
        x = [evt_change_point, self.On_SettingToTransiting, target_c]
        self.event_seq.append(x)
        heappush(event_queue, x)
    
    def On_SettingToTransiting(self, cur_time, target_c):
        logger('%.1f:    On_S2T - %s, picking up customer-%s' % (cur_time, self, target_c))
        assert self.state == ST_SETTING
        prev_PRT = target_c.assigned_PRT
        
        # Measure update
        global SettingState_time
        SettingState_time += cur_time - self.stateChangingPoint
            
        # State update
        self.set_stateChange(ST_TRANSITING, cur_time)
        self.arrived_n.settingPRTs.remove(self)
        print 'removed PRT:', self
        print 'node_settingPRTs', self.arrived_n.settingPRTs 
        
        # Set things for next state
        self.path_n, self.path_e = Algorithms.find_SP(self.transporting_customer.sn.no, self.transporting_customer.dn.no)
        self.last_planed_time = cur_time
        evt_change_point = cur_time + sum(e.distance // min(PRT_SPEED, e.maxSpeed) for e in self.path_e)
        x = [evt_change_point, self.On_TransitingToIdle, target_c]
        self.event_seq.append(x)
        heappush(event_queue, x)
        
        logger('            path: %s' % (self.path_n))

    def On_ApproachingToApproaching(self, cur_time, target_c):
        if self.state == ST_PARKING:
            # This PRT temporally becomes parking state, but it is going to be approaching soon
            # This situation can be happened, because an assignment is processed by step by step
            P2I_EVT, A2P_EVT = self.find_target_event_inEventSeq(cur_time, self, self.On_ParkingToIdle, self.On_ApproachingToParking)
            P2I_EVT[1], A2P_EVT[1] = None, None
            self.state = ST_APPROACHING
        logger('%.1f:    On_A2A - %s, prev_c:%s - new_c:%s' % (cur_time, self, self.assigned_customer, target_c))
        assert self.state == ST_APPROACHING
        prev_customer = self.assigned_customer
        prev_PRT = target_c.assigned_PRT
        
        # Measure update
        global ApproachingState_time
        ApproachingState_time += cur_time - self.stateChangingPoint
        
        # State update
        self.set_stateChange(ST_APPROACHING, cur_time)
        self.assigned_customer = target_c
        target_c.assigned_PRT = self
        
        # Set things for next state
        path_travel_time = cur_time - self.last_planed_time
        _, next_n, xth = Algorithms.find_PRT_position_on_PATH(self.path_e, path_travel_time)
        remain_travel_time = sum(e.distance // min(PRT_SPEED, e.maxSpeed) for e in self.path_e[:xth]) - path_travel_time
        
        
        if next_n == target_c.sn:
            # There is no need to change modification of path
            evt_change_point = cur_time + remain_travel_time
        else:
            path_n_Rerouted, path_e_Rerouted = Algorithms.find_SP(next_n.no, target_c.sn.no)
            self.path_n = self.path_n[:xth] + path_n_Rerouted[1:]
            self.path_e = self.path_e[:xth] + path_e_Rerouted
            evt_change_point = cur_time + remain_travel_time + sum(e.distance // min(PRT_SPEED, e.maxSpeed) for e in path_e_Rerouted)
        x = [evt_change_point, self.On_ApproachingToSetting, target_c]
        self.event_seq.append(x)
        heappush(event_queue, x)
        logger('            path: %s' % (self.path_n))
        logger('            now, around %s' % (next_n.id))
        
        # Modify event of tager_c's previous assigned PRT which is already scheduled
        self.modify_passed_assignedPRT_event(cur_time, prev_PRT, target_c)
        if prev_customer:
            A2T_EVT = self.find_target_event_inEventSeq(cur_time, self, self.On_ApproachingToSetting, prev_customer)        
            A2T_EVT[1] = None        

    def On_ApproachingToParking(self, cur_time, target_c):
        logger('%.1f:    On_A2P - %s, lost %s, ori Path: %s' % (cur_time, self, target_c, self.path_n))
        assert self.state == ST_APPROACHING and self.assigned_customer == target_c
        
        # Measure update
        global ApproachingState_time 
        ApproachingState_time += cur_time - self.stateChangingPoint
        
        # State update
        self.set_stateChange(ST_PARKING, cur_time)
        self.assigned_customer = None
        
        # Set things for next state
        path_travel_time = cur_time - self.last_planed_time
        _, next_n, xth = Algorithms.find_PRT_position_on_PATH(self.path_e, path_travel_time)
        remain_travel_time = sum(e.distance // min(PRT_SPEED, e.maxSpeed) for e in self.path_e[:xth]) - path_travel_time
        
        print 'next_n:', next_n, xth
        
        if next_n.nodeType == STATION or next_n.nodeType == TRANSFER:
            path_n_to_nearStation, path_e_to_nearStation = [next_n], []
        else:
            if next_n.nodeType != JUNCTION:
                print next_n,
                _, _, NextJ_id = next_n.id.split('-')
            else:
                assert next_n.nodeType == JUNCTION
                NextJ_id = next_n.id
            NextS_id = NextJ_id[:-1] 
            path_n_to_nearStation, path_e_to_nearStation = Algorithms.find_SP(findNode(NextJ_id).no, findNode(NextS_id).no)
        
        evt_change_point = cur_time + remain_travel_time + sum(e.distance // min(PRT_SPEED, e.maxSpeed) for e in path_e_to_nearStation)
        self.path_n, self.path_e = self.path_n[:xth] + path_n_to_nearStation, self.path_e[:xth] + path_e_to_nearStation
        x = [evt_change_point, self.On_ParkingToIdle, None]
        self.event_seq.append(x)
        heappush(event_queue, x)
        
        logger('            parking node: %s' % (self.path_n[-1].id))
        print 'changed path: ', self.path_n
        
        
        assert self.path_n[-1].nodeType == STATION or self.path_n[-1].nodeType == TRANSFER

    def On_TransitingToIdle(self, cur_time, target_c):
        logger('%.1f:    On_T2I - %s' % (cur_time, self))    
        assert self.state == ST_TRANSITING
        destS = self.path_n[-1]
#         if len(destS.settingPRTs) > numOfBerth:
        if len(destS.settingPRTs) > 1:
            print destS.settingPRTs
            print destS.settingPRTs[0].event_seq
            for prt in destS.settingPRTs:
                print prt.event_seq[-1]
            min_waitingTime = min(prt.event_seq[-1][0] - cur_time for prt in destS.settingPRTs)
            print cur_time, min_waitingTime
            
            self.isWaiting = True
            destS.waitingPRTs.append(self)
            evt_change_point = cur_time + min_waitingTime
            x = [evt_change_point, self.On_TransitingToIdle, target_c]
            self.event_seq.append(x)
            heappush(event_queue, x)
            print 'limit Capa, prt', self
            return None
        
        if self.isWaiting:
            print 'before', destS.waitingPRTs
            self.isWaiting = False
            destS.waitingPRTs.remove(self)
            print 'After', destS.waitingPRTs
            assert False 
            
        
        # Measure update
        global TransitingState_time, NumOfServicedCustomer, Total_travel_distance, Total_customers_flow_time
        TransitingState_time += cur_time - self.stateChangingPoint
        NumOfServicedCustomer += 1
        travel_distance = sum(e.distance for e in self.path_e)
        Total_travel_distance += travel_distance
        Total_customers_flow_time += cur_time - target_c.arriving_time
        
        # State update
        self.set_stateChange(ST_IDLE, cur_time)
        self.arrived_n = self.transporting_customer.dn
        self.transporting_customer = None
        
        # Set things for next state
        self.path_n, self.path_e = None, None
        self.last_planed_time = cur_time
        dispatcher(cur_time, PRTs, waiting_customers, Nodes)
        
    def On_ParkingToIdle(self, cur_time, args=None):
        logger('%.1f:    On_P2I - %s, arriving node: %s' % (cur_time, self, self.path_n[-1].id))
        print self.path_n
        assert self.path_n[-1].nodeType == STATION or self.path_n[-1].nodeType == TRANSFER 
        assert self.state == ST_PARKING
        
        # Measure update
        global ParkingState_time, Total_travel_distance, Total_empty_travel_distance
        ParkingState_time += cur_time - self.stateChangingPoint
        travel_distance = sum(e.distance for e in self.path_e)
        Total_empty_travel_distance += travel_distance
        Total_travel_distance += travel_distance
        
        # State update
        self.set_stateChange(ST_IDLE, cur_time)
        self.arrived_n = self.path_n[-1]
        
        # Set things for next state
        self.path_n, self.path_e = None, None
        self.last_planed_time = cur_time
        
    def On_ParkingToApproaching(self, cur_time, target_c):
        logger('%.1f:    On_P2A - %s, assigned customer %s' % (cur_time, self, target_c))
        assert self.state == ST_PARKING
        prev_PRT = target_c.assigned_PRT
        
        # Measure update
        global ParkingState_time
        ParkingState_time += cur_time - self.stateChangingPoint
        
        # State update
        self.set_stateChange(ST_APPROACHING, cur_time)
        
        # Set things for next state
        path_travel_time = cur_time - self.last_planed_time
        _, next_n, xth = Algorithms.find_PRT_position_on_PATH(self.path_e, path_travel_time)
        remain_travel_time = sum(e.distance // min(PRT_SPEED, e.maxSpeed) for e in self.path_e[:xth]) - path_travel_time
        next_n = self.path_n[-1]
        
        if next_n == target_c.sn:
            # There is no need to change modification of path
            evt_change_point = cur_time + remain_travel_time
        else:
            path_n_Rerouted, path_e_Rerouted = Algorithms.find_SP(next_n.no, target_c.sn.no)
            self.path_n = self.path_n + path_n_Rerouted[1:]
            self.path_e = self.path_e + path_e_Rerouted
            evt_change_point = cur_time + remain_travel_time + sum(e.distance // min(PRT_SPEED, e.maxSpeed) for e in path_e_Rerouted)
        x = [evt_change_point, self.On_ApproachingToSetting, target_c]
        self.event_seq.append(x)
        heappush(event_queue, x)
        
        # Modify event of tager_c's previous assigned PRT which is already scheduled
        self.modify_passed_assignedPRT_event(cur_time, prev_PRT, target_c)

#---------------------------------------------------------------------
# Generate things such as Network, PRT, Customer

def gen_Network(ns, ns_connection):
    Nodes = [Node(px, py, isStation) for px, py, isStation in ns]
    Edges = []
    for pn, nn in ns_connection:
        Edges.append(Edge(Nodes[pn], Nodes[nn]))
    return Nodes, Edges

def gen_Customer(average_arrival, num_customers, imbalanceLevel, Nodes):
    seed(4)  # 1000, 2000, 3000
#     seed(5)
    accu_pd = []
    pd = [expovariate(1.0 / average_arrival) for _ in range(num_customers)]
    for i, t in enumerate(pd):
        if i == 0:
            accu_pd.append(t)
            continue
        accu_pd.append(accu_pd[-1] + t)
    
    TransferStations = [ i for i, n in enumerate(Nodes) if n.nodeType == TRANSFER]
    Stations = [ i for i, n in enumerate(Nodes) if n.nodeType == STATION]
    
    Customers = []
    for i, t in enumerate(accu_pd):
        if random() <= imbalanceLevel:
            p1 = choice(TransferStations)
            p2 = choice(Stations)
            if random() <= 0.5:
                sn, dn = p1, p2
            else:
                sn, dn = p2, p1
        else:
            sn, dn = sample(Stations, 2)
        Customers.append(Customer(i, t, Nodes[sn], Nodes[dn]))
        
    customerArrivals_txt = open('Info. Arrivals of customers.txt', 'w')
    for c in Customers:
        t, sn, dn = c.arriving_time, c.sn.id, c.dn.id 
        customerArrivals_txt.write('%f,%s-%s\n' % (t, sn, dn))
    customerArrivals_txt.close()
        
    return Customers

def gen_PRT(numOfPRT, Nodes):
    PRTs = []
    for _ in range(numOfPRT):
        target_n_id = randrange(len(Nodes)) 
        while Nodes[target_n_id].nodeType != STATION:
            target_n_id = randrange(len(Nodes)) 
        PRTs.append(PRT(Nodes[target_n_id]))
    return PRTs

#---------------------------------------------------------------------
# Prepare dynamics run
PRT_SPEED = 12  # unit (m/s)
SETTING_TIME = (45.0, 60.0)
waiting_customers = []
event_queue = []

def init_dynamics(_Nodes, _PRTs, _Customers, _dispatcher):
    global Total_empty_travel_distance, NumOfPickedUpCustomer, Total_travel_distance, Total_customers_flow_time, NumOfServicedCustomer  
    Total_empty_travel_distance = 0.0
    NumOfPickedUpCustomer = 0
    Total_travel_distance = 0.0
    Total_customers_flow_time = 0.0
    NumOfServicedCustomer = 0
    global Total_customers_waiting_time, NumOfWaitingCustomer, ChaningPointOfNWC, MaxCustomerWaitingTime  
    Total_customers_waiting_time = 0.0
    NumOfWaitingCustomer = 0
    ChaningPointOfNWC = 0.0
    MaxCustomerWaitingTime = 0.0
    global IdleState_time, ApproachingState_time, SettingState_time, TransitingState_time, ParkingState_time 
    IdleState_time = 0.0
    ApproachingState_time = 0.0
    SettingState_time = 0.0
    TransitingState_time = 0.0
    ParkingState_time = 0.0
    global NumOfCustomerArrivals
    NumOfCustomerArrivals = 0

    global Nodes, PRTs, Customers, dispatcher
    Nodes, PRTs, Customers, dispatcher = _Nodes, _PRTs, _Customers, _dispatcher
    
    for customer in Customers:
        x = [customer.arriving_time, On_CustomerArrival, customer]
        heappush(event_queue, x)

def logger(s):
    print s

on_notify_customer_arrival = lambda x: None

def update_customerWaitingTimeMeasure(cur_time, numOfCustomerChange):
    global Total_customers_waiting_time, NumOfWaitingCustomer, ChaningPointOfNWC, MaxCustomerWaitingTime, WaitingCustomerChanges, WaitingTimeChanges

    # Update measure
    customers_waiting_time = NumOfWaitingCustomer * (cur_time - ChaningPointOfNWC)
    if customers_waiting_time > MaxCustomerWaitingTime:
        MaxCustomerWaitingTime = customers_waiting_time
    Total_customers_waiting_time += customers_waiting_time

    # Memorize things for the next calculation
    if NumOfWaitingCustomer == 0 :
        if numOfCustomerChange == -1: 
            NumOfWaitingCustomer = 0
        else:
            assert numOfCustomerChange == 1
            NumOfWaitingCustomer += numOfCustomerChange
    else:
        NumOfWaitingCustomer += numOfCustomerChange
    ChaningPointOfNWC = cur_time
    
    if WaitingCustomerChanges and WaitingCustomerChanges[-1][0] == cur_time:
        WaitingCustomerChanges.pop()
    WaitingCustomerChanges.append((cur_time, NumOfWaitingCustomer))
    
    if WaitingTimeChanges and WaitingTimeChanges[-1][0] == cur_time:
        WaitingTimeChanges.pop()
    WaitingTimeChanges.append((cur_time, Total_customers_waiting_time))
    

def On_CustomerArrival(cur_time, target_c):
    logger('%.1f: On_CustomerArrival - %s' % (cur_time, target_c))
    customer = Customers.pop(0)
    assert customer == target_c
    waiting_customers.append(customer)
    
    # Measure update
    update_customerWaitingTimeMeasure(cur_time, 1)
    global NumOfCustomerArrivals
    NumOfCustomerArrivals += 1
    
    dispatcher(cur_time, PRTs, waiting_customers, Nodes)
    on_notify_customer_arrival(customer)

def process_events(now):
    while event_queue and event_queue[0][0] <= now:
        even_time, hdlr, args = heappop(event_queue)
        if hdlr != None:
            hdlr(even_time, args)
    if not event_queue:
        return False
    return True

def remove_A_customerInWaitingList(target_customer):
    # Remove servicing customer in waiting_customer
    for i, customer in enumerate(waiting_customers):
        if customer == target_customer:
            return waiting_customers.pop(i)

#---------------------------------------------------------------------
def test():
    from time import sleep
    
    # Generate all inputs: Network, Arrivals of customers, PRTs
#     Nodes, Edges = Network1()
    Nodes, Edges = Network2()
    Customers = gen_Customer(5.0, 5000, 0.0, Nodes)
    PRTs = gen_PRT(40, Nodes)    
    
    Algorithms.init_algorithms(Nodes)
    
    # Choose dispatcher
#     dispatcher = Algorithms.NN0
    dispatcher = Algorithms.NN1
#     dispatcher = Algorithms.NN2
#     dispatcher = Algorithms.NN3
#     dispatcher = Algorithms.NN4
#     dispatcher = Algorithms.NN5
    
    
    init_dynamics(Nodes, PRTs, Customers, dispatcher)
    
    now = 0.0
    while process_events(now):
        now += 1
        sleep(0.0001)

    print        
    print 'Measure------------------------------------------------------------------------------------------------'
    print 'T.TravedDist: %.1f, T.E.TravelDist: %.1f, T.FlowTime: %.1f, T.WaitTime: %.1f' % (Total_travel_distance, Total_empty_travel_distance, Total_customers_flow_time, Total_customers_waiting_time)
    
    print 'IdleState_time: %.1f, ApproachingState_time: %.1f, TransitingState_time: %.1f, ParkingState_time: %.1f' % (IdleState_time, ApproachingState_time, TransitingState_time, ParkingState_time)

if __name__ == '__main__':
    test()
#     tests()