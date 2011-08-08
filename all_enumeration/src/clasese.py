from __future__ import division #@UnresolvedImport

class Job:
    def __init__(self, id, type):
        self.id = id
        self.type = type
    def __repr__(self):
        return str(self.id) + ':' + str(self.type)
    def make_nodes(self, num):
        self.nodes = [Node(self.id, i) for i in xrange(num)]
        for i in xrange(1, len(self.nodes)):
            self.nodes[i].prev_nodes.append(self.nodes[i-1])
            self.nodes[i-1].next_nodes.append(self.nodes[i])
    
class Node:
    def __init__(self, j_id, order):
        self.j_id = j_id
        self.order = order
        self.next_nodes = []
        self.prev_nodes = []
    def __repr__(self):
        return '(' + str(self.j_id)+','+str(self.order)+')'
        
'''
class QC:
    def __init__(self, id, job_seq):
        self.id = id
        self.job_seq = job_seq
    def __repr__(self):
        return 'QC'+str(self.id) + ':' + str(self.job_seq)
        
class YC:
    def __init__(self, id, assigned_j):
        self.id = id
        self.assigned_j = assigned_j
        self.job_seq = []
    def __repr__(self):
        return 'YC'+str(self.id) + ':' + str(self.job_seq)
        
class YT:
    def __init__(self, id):
        self.id = id
        self.job_seq = []
    def __repr__(self):
        return 'YT'+str(self.id) + ':' + str(self.job_seq)
''' 
    
if __name__ == '__main__':
    
    '''
    a = Job(1, 'L')
    print a
    b = QC(2, (Job(1, 'L'),Job(2, 'D'),Job(5, 'D')))
    print b
    '''