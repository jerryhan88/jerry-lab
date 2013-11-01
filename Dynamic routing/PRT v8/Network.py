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
        
    ns = [(0, 0, True), (0 + 50, 0, False), (450 - 50, 0, False), (450, 0, True), (450 + 50, 0, False), ((450 + 350) - 50, 0, False), (450 + 350, 0, True), (0, 0, False), (0, 0, False), (0, 0, False),
          (0, 0, False), (450, 0, False), (0, 0, False), (0, 0, False), (0, 0, False),
          (0, 0, False), (0, 0, False), (0, 0, False), (0, 0, False),
          (0, 0, True), (0, 0, False), (0, 0, False), (450, 0, True), (0, 0, False), (0, 0, False), (450 + 350, 0, True), (0, 0, False), (0, 0, False), (450 + 350 + 500, 0, True),
          (0, 0, False), (0, 0, False), (0, 0, False), (0, 0, False),
          (0, 0, False), (0, 0, False), (0, 0, False), (0, 0, False),
          (0, 0, True), (0, 0, False), (0, 0, False), (450, 0, True), (0, 0, False), (0, 0, False), (450 + 350, 0, True), (0, 0, False), (0, 0, False), (450 + 350 + 500, 0, True),
          (0, 0, False), (0, 0, False), (0, 0, False), (0, 0, False),
          (0, 0, False), (0, 0, False), (0, 0, False), (0, 0, False), (0, 0, False),
          (0, 0, False), (0, 0, False), (0, 0, False), (450, 0, True), (0, 0, False), (0, 0, False), (450 + 350, 0, True), (0, 0, False), (0, 0, False), (450 + 350 + 500, 0, True)
           ]
    
    ns_connection = [(1, 0), ]
    
    return ns, ns_connection


if __name__ == '__main__':
    pass
