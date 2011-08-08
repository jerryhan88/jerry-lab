from __future__ import division #@UnresolvedImport
from clasese import Job, QC, YC, YT

job0 = Job(0, 'discharging')
job1 = Job(1, 'loading')
job2 = Job(2, 'discharging')
job3 = Job(3, 'discharging')
job4 = Job(4, 'discharging')
job5 = Job(5, 'loading')
jobs = [job0, job1, job2, job3, job4, job5] 

qc1 = QC('QC1', [job0, job1, job2])
qc2 = QC('QC2', [job3, job4, job5])
qcs = [qc1, qc2]

qc_discharging_operation = 2
qc_loading_operation = 2
qc_ready_t_d_d = 2
qc_ready_t_d_l = 1
qc_ready_t_l_d = 1
qc_ready_t_l_l = 2

yc1 = YC('YC1', [job0, job1, job4])
yc2 = YC('YC2', [job2, job3, job5])
ycs = [yc1, yc2]

yc_discharging_operation = 2
yc_loading_operation = 2
yc_ready_t_d_d = 2
yc_ready_t_d_l = 2
yc_ready_t_l_d = 0
yc_ready_t_l_l = 2

yt1 = YT('YT1', job2) 
yt2 = YT('YT2', job0)
yt3 = YT('YT3', job5)
yts = [yt1, yt2, yt3]

yt_operation_time = {(qc1, yc1) : 2, (qc1, yc2) : 3, (qc1, qc2) : 1, (qc2, yc1) : 3, (qc2, yc2) : 2, (yc1, yc2) : 1
                  ,(yc1, qc1) : 2, (yc2, qc1) : 3, (qc2, qc1) : 1, (yc1, qc2) : 3, (yc2, qc2) : 2, (yc2, yc1) : 1
                  ,(qc1, qc1) : 0, (qc2, qc2) : 0, (yc1, yc1) : 0, (yc2, yc2) : 0}
