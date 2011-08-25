from __future__ import division #@UnresolvedImport

class Job(object):
    def __init__(self, id, type):
        self.id = id
        self.type = type
    def __repr__(self):
        return str(self.id) + ':' + str(self.type)
    def __cmp__(self, other):
        return self.id - other.id
    def make_nodes(self, num):
        self.nodes = [Node(self.id, i) for i in xrange(num)]
        for i in xrange(1, len(self.nodes)):
            self.nodes[i].prev_nodes.append(self.nodes[i-1])
            self.nodes[i-1].next_nodes.append(self.nodes[i])

class Node:
    def __init__(self, j_id, order):
        self.j_id = j_id
        self.order = order
        self.visited = False
        self.next_nodes = []
        self.prev_nodes = []
    def __repr__(self):
        return '(' + str(self.j_id)+','+str(self.order)+')'
    def check_delible(self):
        for p_n in self.prev_nodes:
            if not p_n.visited:
                break
        else:
            return True
        return False

class Deposit:
    def __init__(self, cut, scheduled_jobs, agreeable_yt_of_job, qcs, ycs, yts):
        '''
        This Deposit class is used for saving all data and for all enumeration
        '''
        self.cut = cut 
        self.scheduled_jobs = scheduled_jobs 
        self.agreeable_yt_of_job = agreeable_yt_of_job
        self.qcs = qcs
        self.ycs = ycs
        self.yts = yts
    def duplicate(self):
        d_cut = self.cut[:] 
        d_scheduled_jobs = self.scheduled_jobs[:]
        d_agreeable_yt_of_job = [x[:] for x in self.agreeable_yt_of_job]
        d_qcs = [qc.duplicate() for qc in self.qcs]
        d_ycs = [yc.duplicate() for yc in self.ycs]
        d_yts = [yt.duplicate() for yt in self.yts]
        return Deposit(d_cut, d_scheduled_jobs, d_agreeable_yt_of_job, d_qcs, d_ycs, d_yts)

if __name__ == '__main__':
    
    '''
    a = Job(1, 'L')
    print a
    b = QC(2, (Job(1, 'L'),Job(2, 'D'),Job(5, 'D')))
    print b
    '''