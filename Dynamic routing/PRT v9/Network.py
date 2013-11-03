from __future__ import division

def network0():
    sx, sy = 800, 800
        
    ns = [(sx * 0.1, sy * 0.1, True), (sx * 0.4, sy * 0.1, True), (sx * 0.75, sy * 0.1, True),
              (sx * 0.1, sy * 0.3, True), (sx * 0.4, sy * 0.3, True), (sx * 0.75, sy * 0.3, True), (sx * 1.0, sy * 0.3, True),
              (sx * 0.1, sy * 0.62, True), (sx * 0.4, sy * 0.62, True), (sx * 0.75, sy * 0.62, True), (sx * 1.0, sy * 0.62, True)
              , (sx * 0.82, sy * 0.105, False), (sx * 0.88, sy * 0.118, False), (sx * 0.90, sy * 0.13, False)
              , (sx * 0.93, sy * 0.148, False), (sx * 0.9425, sy * 0.1622, False), (sx * 0.97, sy * 0.182, False)
              , (sx * 0.99, sy * 0.22, False)]
    
    ns_connection = [(1, 0), (1, 2), (3, 4), (5, 4), (5, 6),
                     (8, 7), (8, 9), (10, 9), (0, 3), (4, 1),
                     (2, 5), (7, 3), (4, 8), (9, 5), (6, 10)
                     , (11, 2), (12, 11), (13, 12), (14, 13), (15, 14), (16, 15), (17, 16), (6, 17)]
    
    return ns, ns_connection  

def network1():
    c0 = 0
    c1 = c0 + 450
    c2 = c1 + 350
    c3 = c2 + 500
    
    r0 = 0
    r1 = r0 + 300 
    r2 = r1 + 500
    r3 = r2 + 400
    
    btwSJ = 70
    
    STATION, JUNCTION, DOT = 0, 1, 2
        
    ns = [('',c0, r0, STATION), ('',c0 + btwSJ, r0, JUNCTION), ('',c1 - btwSJ, r0, JUNCTION), ('',c1, r0, STATION), ('',c1 + btwSJ, r0, JUNCTION), ('',c2 - btwSJ, r0, JUNCTION), ('',c2, r0, STATION), ('',0, r0, JUNCTION), ('',0, r0, DOT), ('',0, r0, DOT),
          ('',c0, r0 + btwSJ, JUNCTION), ('',c1, r0 + btwSJ, JUNCTION), ('',c2, r0 + btwSJ, JUNCTION), ('',0, 0, DOT), (0, 0, DOT),
          ('',c0, r1 - btwSJ, JUNCTION), ('',c1, r1 - btwSJ, JUNCTION), ('',c2, r1 - btwSJ, JUNCTION), ('',0, 0, JUNCTION),
          ('',c0, r1, STATION), ('',c0 + btwSJ, r1, JUNCTION), ('',c1 - btwSJ, r1, JUNCTION), ('',c1, r1, STATION), ('',c1 + btwSJ, r1, JUNCTION), ('',c1 + btwSJ, r1, JUNCTION), ('',c2, r1, STATION), ('',c2 + btwSJ, r1, JUNCTION), ('',c3 - btwSJ, r1, JUNCTION), ('',c3, r1, STATION),
          ('',c0, r1 + btwSJ, JUNCTION), ('',c1, r1 + btwSJ, JUNCTION), ('',c2, r1 + btwSJ, JUNCTION), ('',c3, r1 + btwSJ, JUNCTION),
          ('',c0, r2 - btwSJ, JUNCTION), ('',c1, r2 - btwSJ, JUNCTION), ('',c2, r2 - btwSJ, JUNCTION), ('',c3, r2 - btwSJ, JUNCTION),
          ('',c0, r2, STATION), ('',c0 + btwSJ, r2, JUNCTION), ('',c1 - btwSJ, r2, JUNCTION), ('',c1, r2, STATION), ('',c1 + btwSJ, r2, JUNCTION), ('',c1 + btwSJ, r2, JUNCTION), ('',c2, r2, STATION), ('',c2 + btwSJ, r2, JUNCTION), ('',c3 - btwSJ, r2, JUNCTION), ('',c3, r2, STATION),
          ('',c0, r2 + btwSJ, JUNCTION), ('',c1, r2 + btwSJ, JUNCTION), ('',c2, r2 + btwSJ, JUNCTION), ('',c3, r2 + btwSJ, JUNCTION),
          ('',c0, r3 - btwSJ, JUNCTION), ('',c1, r3 - btwSJ, JUNCTION), ('',c2, r3 - btwSJ, JUNCTION), ('',c3, r3 - btwSJ, JUNCTION), ('',0, 0, DOT),
          ('',0, 0, DOT), ('',0, 0, DOT), ('',c1 - btwSJ, r3, JUNCTION), ('',c1, r3, STATION), ('',c1 + btwSJ, r3, JUNCTION), ('',c2 - btwSJ, r3, JUNCTION), ('',c2, r3, STATION), ('',c2 + btwSJ, r3, JUNCTION), ('',c3 - btwSJ, r3, JUNCTION), ('',c3, r3, STATION)
           ]
    
    ns_connection = [(1, 0), ]
    
    return ns, ns_connection


if __name__ == '__main__':
    pass
