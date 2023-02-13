def astar(startNode, stopNode):
    open_set = set(startNode)
    closed_set = set()
    
    g={} #dictionary to store distance values from start node
    parents={} #dictionary to store adjancency map
    g[startNode]=0
    parents[startNode]=startNode
    
    #finding node with the next least f(n) value, f(n) = g(n)+h(n)
    
    while(len(open_set)>0):
        n=None
        
        for v in open_set: #finding for next lowest f() value
            if n == None or g[v]+heuristic(v) < g[n] + heuristic(v):
                n=v
                
        if n == stopNode or Graph_node[n]==None:
            pass
        else:
            for(m,weight) in get_neighbors(n):
                if m not in open_set and m not in closed_set:
                    open_set.add(m)
                    parents[m]=n
                    g[m]=g[n]+weight
                    
                else: #checking distances and updating g values
                    if(g[m] > g[n] + weight):
                        g[m]=g[n]+weight
                        parents[m]=n
                        
                        if m in closed_set:
                            closed_set.remove(m)
                            open_set.add(m)
                            
        if(n==None):
            print("Path does not exist")
            return None
        if(n==stopNode):
            path=[]
            
            while(parents[n]!=n):
                path.append(n)
                n=parents[n]
                
            path.append(startNode)
            
            path.reverse()
            
            print(path)
            return path
        
        open_set.remove(n)
        closed_set.add(n)
        
    print("Path does not exist")
    return None


def get_neighbors(v):
    if v in Graph_node:
        return Graph_node[v]
    else:
        return None
    
def heuristic(n):
    H_dist = {'A':11,'B':6,'C':99,'D':1,'E':7, 'G':0}
    return H_dist[n]

Graph_node = {'A':[('B',2),('E',3)],
              'B':[('C',1),('G',9)],
              'C':None,
              'E':[('D',6)],
              'D':[('G',1)],
            }

astar('A','G')
                