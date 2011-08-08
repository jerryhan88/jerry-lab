from __future__ import division #@UnresolvedImport
from random import choice, randrange, seed, shuffle#@UnresolvedImport
from clasese import Job, QC, YC, YT

def gen_input(num_jobs, num_qcs, num_ycs, num_yts):
#    seed(99)
    seed(11)
    jobs = []
    for i in range(num_jobs):
        j_state = choice(['discharging', 'loading'])
        jobs.append(Job(i, j_state))

    qcs = []
    for i in range(num_qcs):
        qcs.append(QC('QC%s' % (i + 1), []))
#        qcs.append(QC('QC%s' % (i+1)))
    
    ycs = []
    for i in range(num_ycs):
        ycs.append(YC('YC%s' % (i + 1), []))
    
    for j in jobs:
        qcs[randrange(len(qcs))].job_sequence.append(j)
        ycs[randrange(len(ycs))].job_list.append(j)        
    
    for qc in qcs:
        shuffle(qc.job_sequence)
    
    yts = []
    for i in range(num_yts):
        yts.append(YT('YT%s' % (i + 1)))
    
    operation_time_list = [1, 2, 3]
    yt_operation_time = {}
    qcs_and_ycs = qcs + ycs
    for i, vehicle in enumerate(qcs_and_ycs):
        yt_operation_time[(vehicle, vehicle)] = 0
        for j in range(len(qcs_and_ycs), (i + 1), -1):
#            print j
#            print qcs_and_ycs
            operation_time = choice(operation_time_list)
            yt_operation_time[(vehicle, qcs_and_ycs[j-1])] = operation_time
            yt_operation_time[(qcs_and_ycs[j-1]), vehicle ] = operation_time
    
    return jobs, qcs, ycs, yts, yt_operation_time


if __name__ == '__main__':
    num_jobs = 8
    num_qcs = 3
    num_ycs = 3
    num_yts = 4
    jobs, qcs, ycs, yts, yt_operation_time= gen_input(num_jobs, num_qcs, num_ycs, num_yts)
    print [(x.id, x.state)for x in jobs]
    
    print ''
    for qc in qcs:
        print 'qc id : ', qc.id, '    sequence : ', [(x.id)for x in qc.job_sequence]
    
    print ''    
    for yc in ycs:
        print 'yc id : ', yc.id, '    job_list : ', [(x.id)for x in yc.job_list]
    
    print ''    
    for yt in yts:
        print 'yt id : ', yt.id    
    
    print ''    
    print 'len(yt_operation_time) : ', len(yt_operation_time)
    for k, v in yt_operation_time.items():
        if k[0].id == k[1].id:
            print ''
        print 'key :', (k[0].id,k[1].id) , '    time : ', v