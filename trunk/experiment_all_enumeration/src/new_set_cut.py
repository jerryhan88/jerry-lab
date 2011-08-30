from __future__ import division #@UnresolvedImport
from input import ran_example
from random import seed #@UnresolvedImport

def run(jobs, init_qcs_seq, ycs_assign, num_yts):
    qcs_seq, ycs_seq, yts_seq, planed_jobs, qcs_primary_j, agreeable_yt_of_jobs, handling_v = initialize(jobs, init_qcs_seq, ycs_assign, num_yts)
    pass
def initialize(jobs, init_qcs_seq, num, num_yts):
    
    pass
if __name__ == '__main__':
    
    seed(16)
    jobs, qcs_seq, ycs_assign, num_yts = ran_example(4, 1, 2, 2)
    '''
    job : [3:D, 1:D, 2:D, 0:D]
    qcs_seq : [[2:D, 0:D, 3:D, 1:D]]
    ycs_assign : [[3:D, 2:D], [1:D, 0:D]]
    num_yts : 2
    '''
    run(jobs, qcs_seq, ycs_assign, num_yts)