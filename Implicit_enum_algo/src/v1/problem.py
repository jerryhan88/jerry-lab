'''
Created on 2012. 6. 2.

@author: JerryHan
'''

from __future__ import division
from classes import Operation, Machine
from random import randint, seed

def make_graph(ns, ms):
    ops = ns[1:-1]
    cur_item_num = 0
    init_op = []
    end_op = []
    for i, op in enumerate(ops):
        ms[op.machine].assigned_item.append(op.num)
#        print ms[op.machine - 1], ' ', ms[op.machine - 1].assigned_item
        if cur_item_num != op.item:
            cur_item_num = op.item
            init_op.append(op)
        else:
            ops[i - 1].next_by_item.append(op.num)
            op.prev_by_item.append(ops[i - 1].num)
            if  i + 1 != len(ops) and ops[i + 1].item != cur_item_num:
                end_op.append(op)
            if i + 1 == len(ops):
                end_op.append(op)

    ns[0].next_by_item = [x.num for x in init_op]
    
    for op in init_op:
        op.prev_by_item.append(ns[0].num)
    
    for op in end_op:
        op.next_by_item.append(ns[-1].num)
    
    ns[-1].prev_by_item = [x.num for x in end_op] 

def display_graph(ns, ms):
    print 'operation'
    for op in ns[1:-1]:
        print '    ', op, ' next_by_item : ', op.next_by_item
        print '    ', op, ' prev_by_item : ', op.prev_by_item
        print ''
        
#    for op in ns[1:-1]:
#        ms[op.machine].assigned_item.append(op)
    print 'machine'
    for m in ms[1:]:
        print '    ', m, ' assigned_item : ', m.assigned_item 

def ex1():
    # input
    n0 = Operation(0, 0, 0, 0)
    n1 = Operation(1, 4, 1, 1)
    n2 = Operation(2, 3, 2, 1)
    n3 = Operation(3, 2, 2, 2)
    n4 = Operation(4, 3, 1, 2)
    n5 = Operation(5, 1, 1, 3)
    n6 = Operation(6, 2, 2, 3)
    en = Operation('*', 0, 0, 0)
    
    ns = [n0, n1, n2, n3, n4, n5, n6, en]
    
    m1 = Machine(1)
    m2 = Machine(2)
    
    ms = [m1, m2]
    
    #make graph through input
    make_graph(ns)
    return ns, ms
    
def ex2():
    # input
    n0 = Operation(0, 0, 0, 0)
#            num, duration, machine, item
    n1 = Operation(1, 2, 1, 1)   #@UnusedVariable
    n2 = Operation(2, 3, 2, 1)   #@UnusedVariable
    
    n3 = Operation(3, 3, 1, 2)   #@UnusedVariable
    n4 = Operation(4, 3, 3, 2)   #@UnusedVariable
    n5 = Operation(5, 2, 2, 2)   #@UnusedVariable
    
    n6 = Operation(6, 1, 1, 3)   #@UnusedVariable
    n7 = Operation(7, 3, 2, 3)   #@UnusedVariable
    n8 = Operation(8, 3, 4, 3)   #@UnusedVariable
    
    n9 = Operation(9, 4, 1, 4)   #@UnusedVariable
    n10 = Operation(10, 1, 4, 4) #@UnusedVariable
    n11 = Operation(11, 2, 3, 4) #@UnusedVariable
    
    n12 = Operation(12, 4, 4, 5) #@UnusedVariable
    n13 = Operation(13, 4, 3, 5) #@UnusedVariable
    
    en = Operation('*', 0, 0, 0)
    
    ns = [n0]
    for x in xrange(1, 14):
        ns.append(eval('n' + str(x)))
    ns.append(en)
#    print ns
    
    ms = [Machine(x)for x in xrange(5)]
    make_graph(ns, ms)
    return ns, ms

def ex3():
    seed(10)
    return gen_pro(5, 3, 2, 4, 2, 6)

def gen_pro(num_item, num_machine, io_min, io_max, du_min, du_max):
    ms = [Machine(x)for x in xrange(num_machine + 1)]
    
    n0 = Operation(0, 0, 0, 0)
    ns = [n0]
    op_index = 1
#   num, duration, machine, item
    for item in xrange(num_item):
        num_op_in_item = randint(io_min, io_max)
        for _ in xrange(num_op_in_item):
            duration = randint(du_min, du_max)
            machine = randint(1, num_machine)
            ns.append(Operation(op_index, duration, machine, item+1))
            op_index += 1
#        print 'item: ', item, '   # of item: ', num_op_in_item
    en = Operation('*', 0, 0, 0)
    ns.append(en)
    make_graph(ns, ms)
    return ns, ms

if __name__ == '__main__':
#    ns, ms = ex1()
#    ns, ms = ex2()
    ns, ms = ex3() 
    
    display_graph(ns, ms)

