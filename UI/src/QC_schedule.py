'''
Created on 2011-1-20

This is used for the berth planning. 
It is to decide the qc scheduling.
'''

import Interface
import parameter
class Vessel():
    def __init__(self,id, length, location, time, seed):
        self.id = id
        self.length = length
        
        ## best information
        self.best_berthing_location = location
        self.best_berthing_time = time
        self.best_seed =seed
        self.best_berthing_range = len(seed)
        

# a vessel in vessel_list is an list, vessel[0]=num_of_qc, vessel[1]=vessel_position
def generate_state(following_assign, following_position, state_in_one_stage, num_of_qc, vessels):
    if len(vessels)==1:
        for i in range(1, num_of_qc-vessels[0][0]+2):
            qc_assign=[i]
            qc_assign.extend(following_assign)
            vessel_id = [vessels[0][1]]
            vessel_id.extend(following_position)
            state_in_one_stage[tuple(qc_assign)]=[vessel_id]
    else:
        min_qc=1
        for i in range(len(vessels)-1):
            min_qc = min_qc+ vessels[i][0]
        vessel = vessels.pop()
        max_qc=num_of_qc-vessel[0]+1
        for i in range(min_qc, max_qc+1):
            f_assign=[i]
            f_assign.extend(following_assign)
            f_id=[vessel[1]]
            f_id.extend(following_position)
            generate_state(f_assign, f_id, state_in_one_stage, i-1, vessels[:])


#state_in_one_stage={}
#vessels=[[2,15],[3,25],[3,35]]
#generate_state([],[],state_in_one_stage,num_of_qc,vessels)
#print state_in_one_stage
def qc_schedule(vessel_list):
    
    event_dic={}
    for vessel in vessel_list:
        event_dic[vessel.best_berthing_time]=0
        k=vessel.best_seed[0]
        for t in range(1,vessel.best_berthing_range):
            if vessel.best_seed[t]!=k:
                event_dic[vessel.best_berthing_time+t]=0
            k=vessel.best_seed[t]
    event_list = list(event_dic)
    event_list.sort()
    stage_list=[]
    for t in event_list:
        vessels = []
        for vessel in vessel_list:
            if vessel.best_berthing_time<=t and vessel.best_berthing_time+vessel.best_berthing_range>t:
                vessels.append([vessel.best_seed[t-vessel.best_berthing_time], vessel])
        vessels.sort(lambda x,y:cmp(x[1].best_berthing_location, y[1].best_berthing_location))
        state_in_one_stage={}
        #print vessels
        generate_state([],[],state_in_one_stage,Interface.num_of_qc,vessels)
        #for state in state_in_one_stage:
         #   print state, 
          #  for i in state_in_one_stage[state][0]:
           #     print i.best_berthing_location,
            #print
        #print state_in_one_stage
        stage_list.append(state_in_one_stage)
    
    ##stage_list=[{(1,2):[[vessel1, vessel2], value, (2)previous stage]},{}]

    for state in stage_list[0]:
        stage_list[0][state].extend([0, ()])
        
    for stage in range(1, len(stage_list)):
        for state1 in stage_list[stage]:
            min_value = parameter.M
            min_state = ()
            for state0 in stage_list[stage-1]:
                value = check_state(state0, stage_list[stage-1][state0][0], event_list[stage-1], state1, stage_list[stage][state1][0], event_list[stage])
                value = value + stage_list[stage-1][state0][1]
                if value < min_value:
                    min_value = value
                    min_state = state0
            stage_list[stage][state1].extend([min_value, min_state])
         
    min_value = parameter.M
    min_state =()
    
    for state in stage_list[-1]:
        if stage_list[-1][state][1] < min_value:
            min_state=state
    
    state_list=[[min_state, stage_list[-1][min_state][0]]]
    stage_list.reverse()
    new_state = stage_list[0][min_state][2]
    for stage in range(1, len(stage_list)):
        state_list.append([new_state, stage_list[stage][new_state][0]])
        new_state = stage_list[stage][new_state][2]

    state_list.reverse()
    #print state_list
    try:
        Interface.update_db_qc(event_list, state_list)
    except:
        print "please check your db"


def check_state(state0, vessels0, t0, state1, vessels1, t1):
    ship_qc={}
    for v in range(len(state0)):
        qc_list = []
        for i in range(vessels0[v].best_seed[t0-vessels0[v].best_berthing_time]):
            qc_list.append(state0[v]+i)
        ship_qc[vessels0[v].id]=qc_list
    
    new_qc_assign =[]
    for v in range(len(state1)):
        for i in range(vessels1[v].best_seed[t1-vessels1[v].best_berthing_time]):
            new_qc_assign.append([state1[v]+i, vessels1[v].id]) #[qc, ship]
    setup_time = 0
    for qc in new_qc_assign:
        if ship_qc.has_key(qc[1]):
            if ship_qc[qc[1]].count(qc[0])==0:
                setup_time = setup_time+1
        else:
            setup_time = setup_time+1
    return setup_time
    
    pass
if __name__=='__main__':
    vessel_list=[]
    vessel_list.append(Vessel("ship1",24, 5, 1, [3, 3, 3, 3, 3, 3, 2, 2, 2]))
    vessel_list.append(Vessel("ship2",28, 55, 2, [4, 4, 4, 4, 3, 3, 3, 3, 3, 3]))
    vessel_list.append(Vessel("ship3",20, 20, 20, [3, 3, 3, 3, 3, 3, 3, 3]))
    vessel_list.append(Vessel("ship4",24, 10, 11, [2, 2, 3, 3, 3, 3, 3, 3, 3]))
    vessel_list.append(Vessel("ship5",28, 50, 13, [3, 3, 4, 4, 4, 4, 4, 4, 4]))
    vessel_list.append(Vessel("ship6",23, 45, 22, [3, 3, 3, 3, 3, 3, 3, 3, 3]))
    qc_schedule(vessel_list)
    
    
    