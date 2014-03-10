from __future__ import division
from data import gen_instances

def read_excel(path):
    from xlrd import open_workbook
    book = open_workbook(path)
    ps_sheet = book.sheet_by_name('parameter_setting')
    
    NUM_PRT = int(ps_sheet.cell_value(1, 8))
    NUM_CUSTOMER = int(ps_sheet.cell_value(1, 3))
    CUSTOMER_ARRIVAL_INTERVAL = ps_sheet.cell_value(1, 6)
    
    PRT_SPEED = ps_sheet.cell_value(1, 0)
    S2J_SPEED = ps_sheet.cell_value(1, 1)
    J2D_SPEED = ps_sheet.cell_value(1, 2)
    SETTING_TIME = (ps_sheet.cell_value(1, 4), ps_sheet.cell_value(1, 5))
    
    Network = Network1_excel(book, S2J_SPEED, J2D_SPEED)
    
    Customers, PRTs = gen_instances(Network, CUSTOMER_ARRIVAL_INTERVAL, NUM_CUSTOMER, NUM_PRT, PRT_SPEED)
    
    import Algorithms, Dynamics
    dispatcher = Algorithms.FCFS    
#     dispatcher = Algorithms.NNBA_I
#     dispatcher = Algorithms.NNBA_IA
#     dispatcher = Algorithms.NNBA_IAT
#     dispatcher = Algorithms.NNBA_IT
#     dispatcher = Algorithms.NNBA_IAP
#     dispatcher = Algorithms.NNBA_IATP
    
    Dynamics.run(SETTING_TIME, PRT_SPEED, Network, PRTs, Customers, dispatcher)
#     Dynamics.run(SETTING_TIME, PRT_SPEED, Network, PRTs, Customers, useVisualizer=True)
    

def Network1_excel(book, S2J_SPEED, J2D_SPEED):
    from Dynamics import Node, Edge, TRANSFER, STATION, JUNCTION, DOT 
    nt_sheet = book.sheet_by_name('network')
    
    Nodes = []
    for row_index in range(1, nt_sheet.nrows):
        r = nt_sheet.row(row_index)
#         Nodes.append(Node((r[0].value), r[1].value, r[2].value, eval(r[3].value), int(r[4].value)))        
        Nodes.append(Node(str(r[0].value), r[1].value, r[2].value, eval(r[3].value), int(r[4].value)))
                 
    def findN(nID):
        for n in Nodes:
            if n.id == nID:
                return n
        else:
            False
    
    Edges = []        
    for row_index in range(1, nt_sheet.nrows):
        extra1 = str(nt_sheet.row(row_index)[5].value).split(",")
        extra = []
        for i in range(len(extra1)-1):
            extra.append(extra1[i])
        for i in extra:
            _from = str(nt_sheet.row(row_index)[0].value)
            _to = str(i)
#             print type(_from), _from, type(_to), _to

            Edges.append(Edge(findN(_from), findN(_to)))

#         _from = str(int(nt_sheet.row(row_index)[0].value))
#         _to = str(int(nt_sheet.row(row_index)[5].value))
#         Edges.append(Edge(findN(_from), findN(_to)))
    for i, n in enumerate(Nodes):
        n.no = i
        
    return Nodes, Edges

if __name__ == '__main__':
    read_excel('prtinput.xlsx')
