g = {'a': {'c': 9, 'b': 7, 'f': 14},
     'c': {'a': 9, 'b': 10, 'd': 11, 'f': 2},
     'b': {'a': 7, 'c': 10, 'd': 15},
     'e': {'d': 6, 'f': 9},
     'd': {'c': 11, 'b': 15, 'e': 6},
     'f': {'a': 14, 'c': 2, 'e': 9}}

def dij_algo(graph, start, end):
    dis={}
    todo=[]
    temp={}
    visited = []
    
    for nod in graph:
        dis[nod] = 500
        
    dis[start] = 0
    todo.append(start)
#     while todo != None:
    while todo:     
        for q in g[todo[0]].keys():
            if q not in visited:
    #                 if q not in todo:
    #                    print todo ,'         ',visited
                if start != todo[0]:
                    temp[q] = g[todo[0]][q] + dis[todo[0]]
                else:    
                    temp[q] = g[todo[0]][q]
                if temp.setdefault(q) < dis.setdefault(q):
    #                         print  q ,' : ' ,temp.setdefault(q),dis.setdefault(q)
                    dis[q] = temp.setdefault(q)    
                        
        for l in g[todo[0]].keys():    
            if l not in visited:
                if l not in todo:
                    todo.append(l)     
        else:
                visited.append(todo.pop(0))          
    
    print dis, dis[end] 

if __name__ == '__main__':
    dij_algo(g, 'b', 'f')

