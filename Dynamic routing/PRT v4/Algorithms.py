from __future__ import division
from math import sqrt
from munkres import Munkres, print_matrix

class NN:
    Longest_dis = 0
    def __init__(self, nodes):
        self.NodeByNode_DMatrix = self.create_NodeByNode_DMatrix(nodes)
        self.hungarian_algo = Munkres()
    
    def create_NodeByNode_DMatrix(self, nodes):
        NodeByNode_DMatrix = []
        for i in nodes:
            from_i = []
            for j in nodes:
                _ , path_e = self.find_SP(i, j, nodes)
                distance = sum([e.distance for e in path_e])
                from_i.append(distance)
                # find longest_distance in network
                if NN_algo.Longest_dis < distance: NN_algo.Longest_dis = distance   
            NodeByNode_DMatrix.append(from_i)
        return NodeByNode_DMatrix
    
    def create_PRTbyCustomer_matrix(self, PRTs, cus_queue, nodes):
        first_arrived_cus = [c for c in cus_queue if c == nodes[c.sn].cus_queue[0]]
        
        row_size, col_size = len(PRTs), len(first_arrived_cus)
        max_M_size = max(row_size, col_size)
        
        PRTbyCustomer_matrix = [[NN_algo.Longest_dis] * max_M_size for _ in range(max_M_size)]
        
        for prt in PRTs:
            for i, cus in enumerate(first_arrived_cus):
                c_wait_n = nodes[cus.sn]
                if prt.state == 0:
                    PRTbyCustomer_matrix[prt.id][i] = self.NodeByNode_DMatrix[prt.arrived_n.id][c_wait_n.id]
                elif prt.state == 1:
                    dx = prt.target_n.px - prt.px  
                    dy = prt.target_n.py - prt.py
                    remain_dis = sqrt(dx * dx + dy * dy) 
                    PRTbyCustomer_matrix[prt.id][i] = self.NodeByNode_DMatrix[prt.target_n.id][c_wait_n.id] + remain_dis 
                else:
                    assert prt.state == 2
                    PRTbyCustomer_matrix[prt.id][i] = self.NodeByNode_DMatrix[prt.dest_n.id][c_wait_n.id]
        
        return PRTbyCustomer_matrix
    
    def assign_PRTtoCustomer(self, PRTbyCustomer_matrix):
        resultOfAssign = self.hungarian_algo.compute(PRTbyCustomer_matrix)
        for row, column in resultOfAssign:
            pass
    
#         m = Munkres()
#         indexes = m.compute(self.NodeByNodeDistance_matrix)
#         total = 0
#         for row, column in indexes:
#             value = self.NodeByNodeDistance_matrix[row][column]
#             total += value
#             print '(%d, %d) -> %d' % (row, column, value)
    
    def find_NearestNode(self, v, Nodes):
        candi_nodes = [n for n in Nodes if any(c for c in n.cus_queue if c.marked == False)]
        if not candi_nodes:
            return None
        target_n = None
        nearest_distance = 1e400
        for n in candi_nodes:
            v.path_n, v.path_e = self.find_SP(v.arrived_n, n, Nodes)
            distance = sum([e.distance for e in v.path_e])
            if distance < nearest_distance:
                target_n = n
        return target_n
    
    def find_SP(self, sn, en, Nodes):
        for n in Nodes:
            n.init_node()
            
        sn.min_d = 0
        todo = [sn]
        
        while todo:
            n = todo.pop(0)
            n.visited = True
            for e in n.edges_outward:
                consi_n = e._to
                dist = n.min_d + e.distance
                if consi_n.min_d >= dist:
                    consi_n.min_d = dist
                if not consi_n.visited and not [x for x in todo if consi_n.id == x.id]:
                    todo.append(consi_n)
        path_n = []
        path_e = []
        path_n.append(en)
        consi_n = en
        while consi_n:
            for e in consi_n.edges_inward:
                if e._from.min_d + e.distance == consi_n.min_d:
                    consi_n = e._from
                    path_e.append(e)
                    break 
            else:
                consi_n = None
                break
            path_n.append(consi_n)
        path_n.reverse()
        path_e.reverse()

        return path_n, path_e
