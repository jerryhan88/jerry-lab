from __future__ import division
from Dynamics import PRT, Customer

def scenario0():
    customers = []
    PRTs = []
    
    customers.append(Customer(10, 'C0', Nodes[2], Nodes[4]))
    customers.append(Customer(11, 'C1', Nodes[5], Nodes[7]))
    
    prt0 = PRT()
    prt0.init_position(Nodes[4])
    PRTs.append(prt0)
    
    prt1 = PRT()
    prt1.init_position(Nodes[0])
    PRTs.append(prt1)
    
    return PRTs, customers

def scenario1(Nodes):
    PRTs = []
    
    for init_n in (4, 0, 3):
        prt = PRT(Nodes)
        prt.init_position(Nodes[init_n])
        PRTs.append(prt)
    
    return PRTs

def scenario2(Nodes):
    # there is an transiting PRT
    customers = []
    PRTs = []
    
    customers.append(Customer(10, 'C0', Nodes[2], Nodes[4]))
    customers.append(Customer(11, 'C1', Nodes[5], Nodes[7]))
    
    for init_n in (4, 0, 3):
        prt = PRT()
        prt.init_position(Nodes[init_n])
        PRTs.append(prt)
    
    transiting_prt = PRTs[-1]
    transiting_prt.state = 2
    transiting_prt.next_n = Nodes[4]
    transiting_prt.dest_n = Nodes[8]
    
    return PRTs, customers

def scenario3(Nodes):
    # there is an transiting PRT
    # there is an parking PRT
    customers = []
    PRTs = []
    
    customers.append(Customer(10, 'C0', Nodes[2], Nodes[4]))
    customers.append(Customer(11, 'C1', Nodes[5], Nodes[7]))
    customers.append(Customer(12, 'C2', Nodes[5], Nodes[8]))
    customers.append(Customer(12, 'C3', Nodes[2], Nodes[6]))
    
    for init_n in (4, 0, 3, 5):
        prt = PRT()
        prt.init_position(Nodes[init_n])
        PRTs.append(prt)
    
    transiting_prt = PRTs[-2]
    transiting_prt.state = 2
    transiting_prt.next_n = Nodes[4]
    transiting_prt.dest_n = Nodes[8]
    
    parking_prt = PRTs[-1]
    parking_prt.state = 3
    parking_prt.next_n = Nodes[6]
    parking_prt.px = (parking_prt.next_n.px + parking_prt.arrived_n.px) / 2
      
    parking_prt.py = (parking_prt.next_n.py + parking_prt.arrived_n.py) / 2 
    
    return PRTs, customers

def scenario3(Nodes):
    # there is an approaching PRT
    # there is an transiting PRT
    # there is an parking PRT
    customers = []
    PRTs = []
    
    customers.append(Customer(10, 'C0', Nodes[2], Nodes[4]))
    customers.append(Customer(11, 'C1', Nodes[5], Nodes[7]))
    customers.append(Customer(12, 'C2', Nodes[5], Nodes[8]))
    customers.append(Customer(12, 'C3', Nodes[2], Nodes[6]))
    
    for init_n in (4, 0, 3, 5):
        prt = PRT()
        prt.init_position(Nodes[init_n])
        PRTs.append(prt)
    
    transiting_prt = PRTs[-2]
    transiting_prt.state = 2
    transiting_prt.next_n = Nodes[4]
    transiting_prt.dest_n = Nodes[8]
    
    parking_prt = PRTs[-1]
    parking_prt.state = 3
    parking_prt.next_n = Nodes[6]
    parking_prt.px = (parking_prt.next_n.px + parking_prt.arrived_n.px) / 2
      
    parking_prt.py = (parking_prt.next_n.py + parking_prt.arrived_n.py) / 2 
    
    return PRTs, customers
if __name__ == '__main__':
    pass