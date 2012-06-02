'''
Created on 2012. 6. 2.

@author: JerryHan
'''

from __future__ import division
from classes import Node, Machine

def make_graph(ns):
    ops = ns[1:-1]
    
    cur_item_num = 0
    init_op = []
    end_op = []
    for i, op in enumerate(ops):
        if cur_item_num != op.item_num:
            cur_item_num = op.item_num
            init_op.append(op)
        else:
            ops[i - 1].set_next_by_item(op)
            if  i + 1 != len(ops) and ops[i + 1].item_num != cur_item_num:
                end_op.append(op)
            if i + 1 == len(ops):
                end_op.append(op)

    ns[0].set_next_by_item(init_op[:])  
    
    for op in end_op:
        op.set_next_by_item(ns[-1])

def display_graph(ns, ms):
    print 'operation'
    for op in ns[1:-1]:
        print '    ', op, ' next_by_item : ', op.next_by_item
        
    for op in ns[1:-1]:
        ms[op.machine - 1].assigned_item.append(op)
    print 'machine'
    for m in ms:
        print '    ', m, ' assigned_item : ', m.assigned_item 

def ex1():
    # input
    n0 = Node(0, 0, 0, 0)
    n1 = Node(1, 4, 1, 1)
    n2 = Node(2, 3, 2, 1)
    n3 = Node(3, 2, 2, 2)
    n4 = Node(4, 3, 1, 2)
    n5 = Node(5, 1, 1, 3)
    n6 = Node(6, 2, 2, 3)
    en = Node('*', 0, 0, 0)
    
    ns = [n0, n1, n2, n3, n4, n5, n6, en]
    
    m1 = Machine(1)
    m2 = Machine(2)
    
    ms = [m1, m2]
    
    
    #make graph through input
    make_graph(ns)
    display_graph(ns, ms)
    
def ex2():
    # input
    n0 = Node(0, 0, 0, 0)
    
    n1 = Node(1, 2, 1, 1)   #@UnusedVariable
    n2 = Node(2, 3, 2, 1)   #@UnusedVariable
    
    n3 = Node(3, 3, 1, 2)   #@UnusedVariable
    n4 = Node(4, 3, 3, 2)   #@UnusedVariable
    n5 = Node(5, 2, 2, 2)   #@UnusedVariable
    
    n6 = Node(6, 1, 1, 3)   #@UnusedVariable
    n7 = Node(7, 3, 2, 3)   #@UnusedVariable
    n8 = Node(8, 3, 4, 3)   #@UnusedVariable
    
    n9 = Node(9, 4, 1, 4)   #@UnusedVariable
    n10 = Node(10, 1, 4, 4) #@UnusedVariable
    n11 = Node(11, 3, 3, 4) #@UnusedVariable
    
    n12 = Node(12, 4, 4, 5) #@UnusedVariable
    n13 = Node(13, 4, 3, 5) #@UnusedVariable
    
    en = Node('*', 0, 0, 0)
    
    ns = [n0]
    for x in xrange(1, 14):
        ns.append(eval('n' + str(x)))
    ns.append(en)
    
    ms = [Machine(x + 1)for x in xrange(4)]
    
    make_graph(ns)
    display_graph(ns, ms)

if __name__ == '__main__':
#    ex1()
    ex2()

