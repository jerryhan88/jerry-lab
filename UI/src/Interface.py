'''
Created on 2010-11-12

This is used to connect to the database.
The user, passwd, db are set here.
'''

import MySQLdb

import re
import parameter
import random
import time
num_of_qc = 8#get_num_of_qc()

db = MySQLdb.connect(user='root',passwd='1212',db='tos')
db.autocommit(True)

class Vessel():
    def __init__(self,id,date, eta, etd, favorite_position, length, min_qc, max_qc, total_operation):
        self.id = id
        self.eta = eta
        self.etd = etd
        self.favorite_position = favorite_position
        self.length = length/10
        self.min_qc = min_qc
        self.max_qc = max_qc
        self.total_operation = int(total_operation/30)+(total_operation%30!=0)*1
        self.qc_for_due = self.total_operation / (self.etd - self.eta)
        self.date=date
        ##decision variable
        self.berthing_location = -1
        self.berthing_time = -1
        self.seed = []
        self.berthing_range = -1
        ## best information
        self.best_berthing_location = -1
        self.best_berthing_time = -1
        self.best_seed =[]
        self.best_berthing_range = -1

def initiate_db_for_yc():
    db.autocommit(False)
    cursor = db.cursor()
    delete = "delete from workload" 
    cursor.execute(delete)
    delete = "delete from yc_position" 
    cursor.execute(delete)    
    delete = "delete from detail_workload" 
    cursor.execute(delete)
    delete = "delete from overflow" 
    cursor.execute(delete)
    delete = "delete from original_workload" 
    cursor.execute(delete)
    delete = "delete from original_yc_position" 
    cursor.execute(delete)    
    delete = "delete from original_detail_workload" 
    cursor.execute(delete)
    delete = "delete from original_overflow" 
    cursor.execute(delete)

    block_list=parameter.block_list

    for period in range(1, parameter.num_of_period+1):
        for block in block_list:
            workload = random.randint(0,100)
            insert = "insert into workload (block_id, period, workload) values ('%s', '%d', '%d')" % (block, period, workload)
            cursor.execute(insert)
            insert = "insert into original_workload (block_id, period, workload) values ('%s', '%d', '%d')" % (block, period, workload)
            cursor.execute(insert)
            load = random.randint(0,workload/2)
            workload = workload-load
            discharge = random.randint(0, workload/2)
            workload = workload-discharge
            gate_in = random.randint(0, workload)
            workload = workload - gate_in
            gate_out = random.randint(0,workload)
            pre = workload - gate_out
            
            insert = "insert into detail_workload (block_id, period, loadw, discharge, gate_in, gate_out, pre) values ('%s', '%d','%d','%d','%d','%d','%d')" % (block, period, load, discharge, gate_in, gate_out, pre)
            cursor.execute(insert)
            insert = "insert into original_detail_workload (block_id, period, loadw, discharge, gate_in, gate_out, pre) values ('%s', '%d','%d','%d','%d','%d','%d')" % (block, period, load, discharge, gate_in, gate_out, pre)
            cursor.execute(insert)
            
            
            
    block_list = parameter.block_list + parameter.block_list
    
    for yc in range(1, parameter.num_of_yc+1):
        i = random.randint(0, len(block_list)-1)
        yc_id = "YC"+str(yc)    
        position = block_list.pop(i)
        for period in range(parameter.num_of_period+1):
            insert = "insert into yc_position (yc_id, period, block_id, begin_time) values ('%s', '%d', '%s', 0)" % (yc_id, period, position)
            cursor.execute(insert)
            insert = "insert into original_yc_position (yc_id, period, block_id, begin_time) values ('%s', '%d', '%s', 0)" % (yc_id, period, position)
            cursor.execute(insert)
    db.commit()
    
    block_list=parameter.block_list
    for period in range(1, parameter.num_of_period+1):    
        select = "select block_id, workload from workload where period = '%d'" % period
        cursor.execute(select)
        workload_list = cursor.fetchall()    
        workload={}
        block_yc={}
        for block in workload_list:
            workload[block[0]]=block[1]
            block_yc[block[0]]=[]
    
        select = "select yc_id, block_id from yc_position where period = '%d'" % (period-1)
        cursor.execute(select)
        yc_block_list = cursor.fetchall()   
        for yc in yc_block_list:
            block_yc[yc[1]].append(yc[0])

        for block in block_list:
            overflow = max(workload[block]-parameter.total_time*len(block_yc[block]),0)
            insert = "insert into overflow (block_id, period, overload) values ('%s', '%d', '%d')" % (block, period, overflow)
            cursor.execute(insert)
            insert = "insert into original_overflow (block_id, period, overload) values ('%s', '%d', '%d')" % (block, period, overflow)
            cursor.execute(insert)
    db.commit()
    cursor.close()
    db.autocommit(True)

def yc_reset():
    db.autocommit(False)
    cursor = db.cursor()
    delete = "delete from workload" 
    cursor.execute(delete)
    delete = "delete from yc_position" 
    cursor.execute(delete)    
    delete = "delete from detail_workload" 
    cursor.execute(delete)
    delete = "delete from overflow" 
    cursor.execute(delete)
    select = "select * from original_workload "
    cursor.execute(select)
    workload = cursor.fetchall() 
    select = "select * from original_yc_position "
    cursor.execute(select)
    yc_position = cursor.fetchall() 
    select = "select * from original_detail_workload "
    cursor.execute(select)
    detail_workload = cursor.fetchall() 
    select = "select * from original_overflow "
    cursor.execute(select)
    overflow = cursor.fetchall() 
    
    
        #insert = "insert into block_position values ('%s', %d, %d)" % i
        #cursor.execute(insert)
        
    for i in workload:
        insert = "insert into workload (block_id, period, workload) values ('%s', '%d', '%d')" % i
        cursor.execute(insert)
    for i in detail_workload:
        insert = "insert into detail_workload (block_id, period, loadw, discharge, gate_in, gate_out, pre) values ('%s', '%d','%d','%d','%d','%d','%d')" % i
        cursor.execute(insert)
        
    for i in yc_position:       
        insert = "insert into yc_position (yc_id, period, block_id, begin_time) values ('%s', '%d', '%s', '%d')" % i
        cursor.execute(insert)
            
    for i in overflow:
        insert = "insert into overflow (block_id, period, overload) values ('%s', '%d', '%d')" % i
        cursor.execute(insert)
            
    db.commit()
    cursor.close()
    db.autocommit(True)
    
def get_planned_vessel_list():
    cursor = db.cursor()
    basic_date = parameter.basic_date
    begin_date = parameter.begin_date
    selected_vessel_list = []

    select = "select vessel_id from berth_schedule where planned = '%d' " % 1
        ## 0:vessel_id, 1:eta_date, 2:eta, 3:etd_date, 4:etd, 5:favorite_position, 6:length, 7:min_qc, 8:max_qc, 9:total_operation
    cursor.execute(select)
    vessel_index_list = cursor.fetchall()

    for vessel_index in vessel_index_list:
        selected_vessel_list.append(vessel_index[0])

    vessel_info_list = []   
    print selected_vessel_list
    for vessel in selected_vessel_list:
        select = "select vessel_id, eta_date, eta, etd_date, etd, favorite_position, length, min_qc, max_qc, total_operation from vessel where vessel_id = '%s'" % vessel
        ## 0:vessel_id, 1:eta_date, 2:eta, 3:etd_date, 4:etd, 5:favorite_position, 6:length, 7:min_qc, 8:max_qc, 9:total_operation
        cursor.execute(select)
        vessel_info_list.append(cursor.fetchall()[0])
    vessel_list=[]
    for vessel_info in vessel_info_list:
        expect_a_date = int(re.split("/", vessel_info[1])[2])-begin_date
        expect_a = expect_a_date*24 + int(vessel_info[2])
        expect_d_date = int(re.split("/", vessel_info[3])[2])-begin_date
        expect_d = expect_d_date*24 + int(vessel_info[4])
        vessel_list.append(Vessel(vessel_info[0], basic_date, expect_a, expect_d, *vessel_info[5:]))

    for vessel in vessel_list:
        select = "select location, begin, seed from berth_schedule where vessel_id = '%s'" % vessel.id
        cursor.execute(select)
        vessel_info = cursor.fetchall()[0]
        
        raw_seed = re.split(",", vessel_info[2])
        seed = []
        for i in raw_seed:
            seed.append(int(i))
        
        vessel.best_berthing_location = vessel_info[0]
        vessel.best_berthing_time = vessel_info[1]
        vessel.best_seed = seed
        vessel.best_berthing_range = len(seed)

    return vessel_list
    
    

def get_vessel_list(selected_vessel_list):
    cursor = db.cursor()
    basic_date = parameter.basic_date
    begin_date = parameter.begin_date
    vessel_info_list = []
    for vessel in selected_vessel_list:
        select = "select vessel_id, eta_date, eta, etd_date, etd, favorite_position, length, min_qc, max_qc, total_operation from vessel where vessel_id = '%s'" % vessel
        ## 0:vessel_id, 1:eta_date, 2:eta, 3:etd_date, 4:etd, 5:favorite_position, 6:length, 7:min_qc, 8:max_qc, 9:total_operation
        cursor.execute(select)
        vessel_info_list.append(cursor.fetchall()[0])
    cursor.close()
    vessel_list=[]
    for vessel_info in vessel_info_list:
        expect_a_date = int(re.split("/", vessel_info[1])[2])-begin_date
        expect_a = expect_a_date*24 + int(vessel_info[2])
        expect_d_date = int(re.split("/", vessel_info[3])[2])-begin_date
        expect_d = expect_d_date*24 + int(vessel_info[4])
        vessel_list.append(Vessel(vessel_info[0], basic_date, expect_a, expect_d, *vessel_info[5:]))

    return vessel_list
    
#vessel_list = get_vessel_list()        
def original_get_vessel_list():
    cursor = db.cursor()
    basic_date = parameter.basic_date
    begin_date = parameter.begin_date
    select = "select vessel_id, eta_date, eta, etd_date, etd, favorite_position, length, min_qc, max_qc, total_operation from vessel"
    ## 0:vessel_id, 1:eta_date, 2:eta, 3:etd_date, 4:etd, 5:favorite_position, 6:length, 7:min_qc, 8:max_qc, 9:total_operation
    cursor.execute(select)
    vessel_info_list = cursor.fetchall()
    cursor.close()
    vessel_list=[]
    for vessel_info in vessel_info_list:
        expect_a_date = int(re.split("/", vessel_info[1])[2])-begin_date
        expect_a = expect_a_date*24 + int(vessel_info[2])
        expect_d_date = int(re.split("/", vessel_info[3])[2])-begin_date
        expect_d = expect_d_date*24 + int(vessel_info[4])
        vessel_list.append(Vessel(vessel_info[0], basic_date, expect_a, expect_d, *vessel_info[5:]))
    return vessel_list
            
def get_vessel_list_for_show():
    cursor = db.cursor()
    select = "select vessel_id, eta_date, eta, etd_date, etd from vessel"
    ## 0:vessel_id, 1:eta_date, 2:eta, 3:etd_date, 4:etd, 
    cursor.execute(select)
    vessel_info_list = cursor.fetchall()
    cursor.close()
    vessel_list = []
    for vessel in vessel_info_list:
        vessel_list.append([vessel[0], vessel[1]+"_"+vessel[2]+":00", vessel[3]+"_"+vessel[4]+":00"])
    return vessel_list
    
    
def check_vessel(vessel_id):
    cursor = db.cursor()
    select = "select vessel_id, eta_date, eta, etd_date, etd, length, total_operation, favorite_position, max_qc, min_qc from vessel where vessel_id = '%s'" % vessel_id
    cursor.execute(select)
    raw_vessel_info = cursor.fetchall()[0]
    cursor.close()
    vessel_info = [raw_vessel_info[0],raw_vessel_info[1]+"_"+raw_vessel_info[2]+":00", raw_vessel_info[3]+"_"+raw_vessel_info[4]+":00"]
    vessel_info.extend(raw_vessel_info[5:])    
    return vessel_info
    
    
def check_vessel_schedule(ship_id):
    cursor = db.cursor()
    select = "select location, berth_t_begin, berth_t_end, begin, end from berth_schedule where vessel_id = '%s'" % ship_id
    cursor.execute(select)
    raw_vessel_schedule = cursor.fetchall()[0]
    cursor.close()
    berth_begin = raw_vessel_schedule[1]+"  "+str(raw_vessel_schedule[3]%24)+":00"
    berth_end = raw_vessel_schedule[2]+"  "+str(raw_vessel_schedule[4]%24)+":00"
    
    return raw_vessel_schedule[0], berth_begin, berth_end
    
def update_db_berth(sorted_vessel_list):
    cursor = db.cursor()
    for vessel in sorted_vessel_list:
        berth_t_begin = vessel.date
        berth_t_begin = berth_t_begin[:-1]+str(vessel.best_berthing_time / 24)
        berth_t_end = vessel.date
        berth_t_end = berth_t_end[:-1]+str((vessel.best_berthing_time+vessel.best_berthing_range)/ 24)
        seed = ""
        for i in vessel.best_seed:
            seed = seed+str(i)+','
        seed = seed[:-1]
        update = "update berth_schedule set berth_t_begin='%s', berth_t_end='%s', location = '%d', begin = '%d', end = '%d', seed = '%s', planned = '%d' where vessel_id = '%s'" % (berth_t_begin, berth_t_end, vessel.best_berthing_location, vessel.best_berthing_time, vessel.best_berthing_time+vessel.best_berthing_range, seed, 1, vessel.id)
        cursor.execute(update)

    cursor.close()
    
def update_db_qc(event_list, state_list):
    cursor = db.cursor()
    event_list.append(999)
    for t in range(len(event_list)-1):
        time_range = str(event_list[t])+","+str(event_list[t+1])
        for v in range(len(state_list[t][0])):
            ship_id = state_list[t][1][v].id
            for i in range(state_list[t][1][v].best_seed[event_list[t]-state_list[t][1][v].best_berthing_time]):
                qc_id = "QC"+str(state_list[t][0][v]+i)
                insert = "insert into qc_assign (time_range, qc_id, ship_id, sequence) values ('%s','%s','%s','%d')" % (time_range, qc_id, ship_id,i)
                cursor.execute(insert)
    cursor.close()

def get_db_qc():
    cursor = db.cursor()
    select = "select DISTINCT time_range from qc_assign"
    cursor.execute(select)
    raw_time_range_list = cursor.fetchall()
    time_range_list = []
    for time_range in raw_time_range_list:
        time = re.split(",", time_range[0])
        time_range_list.append([int(time[0]),int(time[1])])
    time_range_list.sort()
    
    qc_assign_list = []
    for time_range in time_range_list:
        time = str(time_range[0])+","+str(time_range[1])
        select = "select qc_id, ship_id, sequence from qc_assign where time_range = '%s'" % time
        cursor.execute(select)
        qc_assign_list.append(cursor.fetchall())
    vessel_position_dic = {}
    select = "select vessel_id, location from berth_schedule"
    cursor.execute(select)
    vessel_position_list = cursor.fetchall()
    for vessel in vessel_position_list:
        vessel_position_dic[vessel[0]]=vessel[1]
    
    vessel_leave_dic = {}
    select = "select vessel_id, end from berth_schedule"
    cursor.execute(select)
    vessel_position_list = cursor.fetchall()
    cursor.close()
    for vessel in vessel_position_list:
        vessel_leave_dic[vessel[0]]=vessel[1]
    return time_range_list, qc_assign_list, vessel_position_dic, vessel_leave_dic
    
    
def get_db_vessel():
    cursor = db.cursor()
    
    vessel_length_dic={}
    select = "select vessel_id, length from vessel"
    cursor.execute(select)
    vessel_length_list = cursor.fetchall()
    for vessel in vessel_length_list:
        vessel_length_dic[vessel[0]]=vessel[1]
    
    select = "select vessel_id, location, begin, end from berth_schedule"
    cursor.execute(select)
    vessel_location_time = cursor.fetchall()
    cursor.close()
    
    return vessel_length_dic, vessel_location_time

def get_info_for_yc_plan(period):
    cursor = db.cursor()
    select = "select block_id,row, col from block_position"
    cursor.execute(select)
    block_position_list = cursor.fetchall()
    block_position = {}
    block_yc={}
    for block in block_position_list:
        block_position[block[0]]=[block[1],block[2]]
        block_yc[block[0]]=[]
    #print block_position
    
    select = "select block_id, workload from workload where period = '%d'" % period
    cursor.execute(select)
    workload_list = cursor.fetchall()    
    workload={}
    for block in workload_list:
        workload[block[0]]=block[1]
    #print workload
    
    
    select = "select yc_id, block_id from yc_position where period = '%d'" % (period-1)
    cursor.execute(select)
    yc_block_list = cursor.fetchall() 
    cursor.close()   
    yc_position = {}
    for yc in yc_block_list:
        yc_position[yc[0]]=yc[1]
        block_yc[yc[1]].append(yc[0])
    #print yc_position
    #print block_yc
    return workload, block_yc, yc_position, block_position


def save_yc_plan(update_yc_position_time, update_overflow_workload, period):
    cursor = db.cursor()
    for yc in update_yc_position_time:
        update = "update yc_position set block_id='%s',begin_time = '%d' where yc_id = '%s' and period = '%d'" % (update_yc_position_time[yc][0], update_yc_position_time[yc][1], yc, period)
        cursor.execute(update)
    
    if period < 4:
        select = "select block_id, workload from workload where period = '%d'" % (period+1)
        cursor.execute(select)
        workload_list = cursor.fetchall()    
        
        for i in workload_list:
            update = "update workload set workload = '%d' where block_id = '%s' and period = '%d'" % ( i[1]+update_overflow_workload[i[0]], i[0], period+1)
            cursor.execute(update)
    
        for block in parameter.block_list:
    
            select = "select loadw, discharge, gate_in, gate_out, pre from detail_workload where block_id = '%s' and period = '%d'" % (block, period+1)
            cursor.execute(select)
            workload = list(cursor.fetchall()[0])  
            
            add_position = random.randint(0, 4)
            workload[add_position] = workload[add_position]+update_overflow_workload[block]
        
            update = "update detail_workload set loadw= '%d', discharge= '%d', gate_in= '%d', gate_out= '%d', pre = '%d' where block_id = '%s' and period = '%d'" % (workload[0], workload[1], workload[2], workload[3], workload[4],block, period+1)
            cursor.execute(update)
    for block in parameter.block_list:
        update = "update overflow set overload = '%d' where block_id = '%s' and period = '%d'" % (update_overflow_workload[block], block, period)
        cursor.execute(update)
    cursor.close()

                
def get_detail_workload_for_show(block, period):
    cursor = db.cursor()
    select = "select loadw, discharge, gate_in, gate_out, pre from detail_workload where block_id = '%s' and period = '%d'" % (block, period)
    cursor.execute(select)
    return list(cursor.fetchall()[0])
            
    
    
def get_workload_for_show():
    cursor = db.cursor()
    block_list=parameter.block_list
    workload_list = []
    for block in block_list:
        work_list = []
        for period in range(1,5):
            select = "select workload from workload where block_id = '%s' and period = '%d'" % (block, period)
            cursor.execute(select)
            work_list.append(cursor.fetchall()[0][0])   
        work_list.append(0) 
        workload_list.append(work_list)
    cursor.close()
    return workload_list

def get_overload_for_show():
    cursor = db.cursor()
    block_list=parameter.block_list
    workload_list = []
    for block in block_list:
        work_list = []
        for period in range(1,5):
            select = "select overload from overflow where block_id = '%s' and period = '%d'" % (block, period)
            cursor.execute(select)
            work_list.append(cursor.fetchall()[0][0])   
        work_list.append(0) 
        workload_list.append(work_list)
    cursor.close()
    return workload_list

def get_yc_movement():
    cursor = db.cursor()
    original_block_yc_dic_list = []
    moved_block_yc_dic_list = []
    for period in range(1,6):
        original_block_yc_dic = {}
        select = "select block_id,yc_id from yc_position where  period = '%d'" % (period-1)
        cursor.execute(select)
        block_yc_list = cursor.fetchall()
        for block, yc in block_yc_list:
            if block in original_block_yc_dic:
                original_block_yc_dic[block].append(yc)
            else:
                original_block_yc_dic[block] = [yc]
        original_block_yc_dic_list.append(original_block_yc_dic)  
        
        moved_block_yc_dic = {}        
        select = "select block_id,yc_id from yc_position where  period = '%d'" % (period)
        cursor.execute(select)
        block_yc_list = cursor.fetchall()
        for block, yc in block_yc_list:
            if block in moved_block_yc_dic:
                moved_block_yc_dic[block].append(yc)
            else:
                moved_block_yc_dic[block] = [yc]
        moved_block_yc_dic_list.append(moved_block_yc_dic)          
    cursor.close()
    return original_block_yc_dic_list, moved_block_yc_dic_list
    
def get_yc_move_time(yc_id, period):
    cursor = db.cursor()
    select = "select begin_time from yc_position where yc_id = '%s' and period = '%d'" % (yc_id,period)
    cursor.execute(select)
    rows = cursor.fetchall()[0][0]
    cursor.close()
    return rows


def initiate_db_for_berth():
    cursor = db.cursor()
    delete = "delete from berth_schedule" 
    cursor.execute(delete)
    delete = "delete from qc_assign" 
    cursor.execute(delete)
    
    select = "select vessel_id, eta_date, eta, etd_date, etd, favorite_position from vessel "
    cursor.execute(select)
    vessel_info_list = cursor.fetchall()
    begin_date = parameter.begin_date
    for vessel_info in vessel_info_list:
        expect_a_date = int(re.split("/", vessel_info[1])[2])-begin_date
        expect_a = expect_a_date*24 + int(vessel_info[2])
        expect_d_date = int(re.split("/", vessel_info[3])[2])-begin_date
        expect_d = expect_d_date*24 + int(vessel_info[4])
        insert = "insert into berth_schedule (vessel_id, berth_t_begin, berth_t_end, location, begin, end, seed, planned) values ('%s', '%s','%s','%d', '%d','%d', '%s','%d')" % (vessel_info[0],vessel_info[1],vessel_info[3],vessel_info[5],expect_a, expect_d, [], 0)
        cursor.execute(insert)
    cursor.close()
    
    
def get_vessel_position_for_show():
    db.autocommit(True)
    cursor = db.cursor()
    select = "select berth_schedule.vessel_id, vessel.length, berth_schedule.location, berth_schedule.begin, berth_schedule.end from vessel, berth_schedule where vessel.vessel_id=berth_schedule.vessel_id"
    cursor.execute(select)
    
    return cursor.fetchall()

def set_initial_block_position_data():
    cursor = db.cursor()
    for r in range(9):
        for c in range(4):
            bid = '%c%d' % (65 + c, r + 1)
            qry = "insert into block_position values ('%s', %d, %d)" % (bid, r + 1, c + 1)
            cursor.execute(qry)
    cursor.close()
    
    
def check_plan_exist(block_id, bay_id):
    cursor = db.cursor()
    select = "select sequence.p_id, seq_num, container_id, _from, _to from plan, sequence where block_id='%s' and bay_id='%d' and sequence.p_id = plan.p_id" % (block_id, bay_id)
    cursor.execute(select)
    sequence_list = cursor.fetchall()
    cursor.close()
    
    return sequence_list

def remove_plan(block_id, bay_id):
    cursor = db.cursor()
    select = "select p_id from plan where block_id='%s' and bay_id='%d'" % (block_id, bay_id)
    cursor.execute(select)
    raw_p_id = cursor.fetchall()
    if len(raw_p_id)!=0:
        p_id = raw_p_id[0][0]
        delete = "delete from plan where block_id='%s' and bay_id='%d'" % (block_id, bay_id)
        cursor.execute(delete)
        
        delete = "delete from sequence where p_id='%d'" % p_id
        
        
        
        

if __name__=='__main__':
    t0=time.time()
    #initiate_db_for_berth()
    #initiate_db_for_yc()
    #get_db_qc()
    #check_vessel_schedule("ship1")
    #print get_vessel_position_for_show()
    #yc_reset()
    #print get_workload_for_show()
    #print get_workload_for_show()
    #set_initial_block_position_data()
    print time.time()-t0
    