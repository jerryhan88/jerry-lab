from __future__ import division #@UnresolvedImport
'''
This module have all classes for set scheduling cut algorithm
'''

class Job:
    def __init__(self, id, type):
        self.id = id
        self.type = type
        self.handling_qc_id = None
        self.handling_yc_id = None
        
class QC:
    def __init__(self, id, job_seq, num_of_flag):
        self.id = id
        self.job_seq = job_seq
        self.num_of_flag = num_of_flag
        self.primary_j = job_seq[0]
        self.primary_j_id_in_seq = 0
    def duplicate(self):
        n_qc = QC(self.id, self.job_seq, self.num_of_flag)
        n_qc.primary_j, n_qc.primary_j_id_in_seq = self.primary_j, self.primary_j_id_in_seq
        return n_qc
        
class YC:
    def __init__(self, id, assigned_j):
        self.id = id
        self.assigned_j = assigned_j
        self.job_seq = []
    def duplicate(self):
        n_yc = YC(self.id, self.assigned_j)
        n_yc.job_seq = self.job_seq[:]
        return n_yc
        
class YT:
    def __init__(self, id):
        self.id = id
        self.job_seq = []
    def duplicate(self):
        n_yt = YT(self.id)
        n_yt.job_seq = self.job_seq[:]
        return n_yt

class Node:
    def __init__(self, cut, scheduled_jobs, agreeable_yt_of_job, qcs, ycs, yts):
        '''
        This Node class is used for saving all data and for all enumeration
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
        return Node(d_cut, d_scheduled_jobs, d_agreeable_yt_of_job, d_qcs, d_ycs, d_yts)
    
if __name__ == '__main__':
    '''
    test code
    '''
    import Input
    jobs, qcs, ycs, yts = Input.small_problem()
    scheduled_jobs = [[] for _ in jobs]
    not_agreeable_yt_of_job = [[] for _ in jobs]
    cut = []
    a = Node(cut, scheduled_jobs, not_agreeable_yt_of_job, qcs, ycs, yts)
    print scheduled_jobs
        
        
    '''
    for test duplication
    '''
    a = QC(1,(1,2,5,23), 3)
    b = a.duplicate()
    print a.job_seq
    print b.job_seq[0]
    
    a.job_seq = 1000
    print a.job_seq
    print b.job_seq
