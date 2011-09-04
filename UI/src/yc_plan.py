'''
Created on 2011-1-20

The algorithm for yc deployment.

'''

from __future__ import division
from cplex import Cplex, SparsePair
import parameter
import Interface



def deployment(period):  #period = 1..4
    workload_list, block_yc, yc_position, block_position = Interface.get_info_for_yc_plan(period)
    block_index = {}    #{0:"A4"}
    yc_index = {}       #{0:"YC2"}
    sink_block_list=[]  
    available_yc = []
    
    w=[] # block unfulfilled workload
    v=[] # yc available time
    r=[] # blcok 1:1 crane,2:0 crane
    c=[] #travel time
         
    #print workload_list
    #print block_yc
    #print yc_position
    #print block_position
    for block in workload_list:
        if workload_list[block]>parameter.total_time * len(block_yc[block]) and len(block_yc[block])<parameter.max_crane:
            sink_block_list.append(len(sink_block_list))
            block_index[len(sink_block_list)-1]=block
            w.append(workload_list[block]-parameter.total_time * len(block_yc[block]))
            r.append(2-len(block_yc[block]))
            
        if workload_list[block]<parameter.total_time and len(block_yc[block])==parameter.max_crane:
            available_yc.extend([len(available_yc),len(available_yc)+1])
            yc_index[len(available_yc)-2]=block_yc[block][0]
            yc_index[len(available_yc)-1]=block_yc[block][1]
            v.extend([parameter.total_time-workload_list[block], parameter.total_time])
            
        if workload_list[block]>parameter.total_time and workload_list[block]<parameter.total_time*parameter.max_crane and len(block_yc[block])==parameter.max_crane:
            available_yc.append(len(available_yc))
            yc_index[len(available_yc)-1]=block_yc[block][1]
            v.append(parameter.total_time*parameter.max_crane-workload_list[block])
        if workload_list[block]<parameter.total_time and len(block_yc[block])==1:
            available_yc.append(len(available_yc))
            yc_index[len(available_yc)-1]=block_yc[block][0]
            v.append(parameter.total_time-workload_list[block])
            
    for yc in available_yc:
        yc_travel_t_list = []
        from_row, from_column = block_position[yc_position[yc_index[yc]]]
        for block in sink_block_list:
            to_row, to_column = block_position[block_index[block]]
            t = abs(to_column-from_column)*parameter.speed_column+abs(to_row-from_row)*parameter.speed_row
            if to_column == from_column:
                t=t+parameter.speed_column
            yc_travel_t_list.append(t)
        c.append(yc_travel_t_list)
#    print w
 #   print v
  #  print r
   # print c
    #print sink_block_list
#    print available_yc
 #   print block_index
  #  print yc_index
        

    # LP model
    om = Cplex()
    om.objective.set_sense(om.objective.sense.minimize)
    # variables and objective
    yij = lambda i, j: 'y_%d_%d' % (i, j)
    u1i= lambda i: 'u1_%d' % (i)
    u2i= lambda i: 'u2_%d' % (i)
    #num_of_sink_block = len(sink_block_list)
    #num_of_available_yc = len(available_yc)
    
    for i in sink_block_list:
        for j in available_yc:
            om.variables.add(types='B', names=[yij(i,j)])  
        om.variables.add(names=[u2i(i)])   
        om.variables.add([1.0], names=[u1i(i)])                             

    # constraints
    # (1)
    
    for j in available_yc:
        yij_list = []
        val = []
        for i in sink_block_list:
            yij_list.append(yij(i,j))
            val.append(1.0)
        exprs = [SparsePair(yij_list,val)]       
        om.linear_constraints.add(exprs, 'L', [1])

    # (2)
    for i in sink_block_list:
        yij_list = []
        val = []
        for j in available_yc:
            yij_list.append(yij(i,j))
            val.append((v[j]-c[j][i])*1.0)  
        yij_list.extend([u1i(i), u2i(i)])     
        val.extend([1.0,-1.0]) 
        exprs = [SparsePair(yij_list,val)]
        om.linear_constraints.add(exprs, 'E', [w[i]])

    # (3)
    for i in sink_block_list:
        yij_list = []
        val = []
        for j in available_yc:
            yij_list.append(yij(i,j))
            val.append(1.0)     
        exprs = [SparsePair(yij_list,val)]
        om.linear_constraints.add(exprs, 'L', [r[i]])

                             
    # (4)   
    for i in sink_block_list:
        exprs = [SparsePair([u1i(i)],[1.0])]
        om.linear_constraints.add(exprs, 'G', [0])                     
        exprs = [SparsePair([u2i(i)],[1.0])]
        om.linear_constraints.add(exprs, 'G', [0])                            

    # solve
    om.set_results_stream(None)
    try:
        #print 'Solve LP..',
        om.solve()
    except:
        pass#print 'Exception while solving!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
    #print 'done.',
    print om.solution.get_status()
    #assert om.solution.get_status() == 1
    #sol.get_status() in (sol.status.MIP_optimal, sol.status.optimal_tolerance)

    
    yc_move=[[om.solution.get_values(yij(i,j)) for i in sink_block_list] for j in available_yc]
    overflow=[om.solution.get_values(u1i(i)) for i in sink_block_list]
    
    for i in range(len(overflow)):
        overflow[i]=int(round(overflow[i]))
    
    update_yc_position_time = {}
    for yc in yc_position:
        update_yc_position_time[yc]=[yc_position[yc], 0]
    
    for j in range(len(yc_move)):
        for i in range(len(yc_move[j])):
            yc_move[j][i]=int(round(yc_move[j][i]))
            if yc_move[j][i]==1:
                update_yc_position_time[yc_index[j]]=[block_index[i],parameter.total_time - v[j]]
    
    update_overflow_workload={}
    for block in workload_list:
        update_overflow_workload[block]=0
    for i in range(len(overflow)):
        update_overflow_workload[block_index[i]]=overflow[i]

    #print update_yc_position_time
    #print update_overflow_workload

    Interface.save_yc_plan(update_yc_position_time, update_overflow_workload, period)
    
    #return yc_move,overflow        

def main():
    for period in range(1,2):
        yc_move,overflow = deployment(period)
        print yc_move
        print overflow
if __name__=='__main__':
    main()
