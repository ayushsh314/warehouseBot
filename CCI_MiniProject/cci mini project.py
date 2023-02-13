from cmath import inf
import cv2 as cv
import numpy as np



def refinedContours(img,per = 0.01):
    blur = cv.GaussianBlur(img,(5,5),cv.BORDER_DEFAULT)
    canny = cv.Canny(blur,120,230)
    contours,heir = cv.findContours(canny,cv.RETR_LIST,cv.CHAIN_APPROX_SIMPLE)

    rcontours = []#for storing points of approx points
    for i in contours:
        epi = per*cv.arcLength(i,1)
        refined = cv.approxPolyDP(i,epi,1)
        for j in refined:
            if(j[0,1] <62 or j[0,1]>1025):
                break

        else:
            rcontours.append(refined)
    
    del(blur)
    del(canny)
    del(contours)
    del(heir)
    return rcontours


def Distance(x1,y1,x2,y2):
    x = x1-x2
    y = y1-y2
    return ((x)**2+(y)**2)


def FNode():
    img = cv.imread("area.JPG")
    blank = np.zeros(img.shape,"uint8")
#    grey = cv.cvtColor(img,cv.COLOR_RGB2GRAY)
     #contour poins added only if the they are in a certain range i.e. above eryc logo
    rcontours = refinedContours(img)
    
    for i in range(len(rcontours)):                    #filtering the duplicate rows
        rcontours[i] = np.unique(rcontours[i],axis = 0)
    i = 0
    j = len(rcontours)-1
    while i<j:                     
        if np.array_equal(rcontours[i],rcontours[i+1]): #filtering duplicate contours
            rcontours.pop(i+1)
            j-=1
        else:
            i+=1
    
    

    onlyPoints = [] #list unique points // ease to access
    for i in range(len(rcontours)):
        for j in range(rcontours[i].shape[0]):
            onlyPoints.append(rcontours[i][j,0])
    del rcontours

    

    PosNode = [] #[  [[][][]]   ]
    PosNode.append([[onlyPoints[0].item(0),onlyPoints[0].item(1)]]) #entire thing to cluster the nodes
    for i in range(len(onlyPoints)):
        for j in range(len(PosNode)):
            x1 = onlyPoints[i].item(0)
            y1 = onlyPoints[i].item(1)
            x2 = PosNode[j][0][0]
            y2 = PosNode[j][0][1]
            if( Distance(x1,y1,x2,y2)<7000):           #if point is in certain distance range it put with the any cluster     
                PosNode[j].append([x1,y1])
                break
        else:
            PosNode.append([[x1,y1]])                   #here the point is away from all cluster hence it will start new cluster

    del onlyPoints


    FinalNodes = np.zeros((len(PosNode),2),int)     #array for saving average of coordinates of the clusters
    for i in range(len(PosNode)):
        for j in range(len(PosNode[i])):            
            FinalNodes[i][0]+= PosNode[i][j][0]     #summation of x coordinates
            FinalNodes[i][1]+= PosNode[i][j][1]     #summation of y coordinates
        FinalNodes[i][0]//= len(PosNode[i])         #divison by total entries
        FinalNodes[i][1]//= len(PosNode[i])
   
    del PosNode
    for i in FinalNodes:                            #plotting circles on the main image
        cv.circle(img,i,26,(255,255,255),-1)
    

    rcontours = refinedContours(img,0.15)
    cv.drawContours(blank,rcontours,-1,(255,255,255),1)
    for i in range(len(rcontours)):
        j = 0
        n = 0
        
        while j<len(rcontours[i])-1:
            x1 = rcontours[i][j,0].item(0)
            y1 = rcontours[i][j,0].item(1)
            x2 = rcontours[i][j+1,0].item(0)
            y2 = rcontours[i][j+1,0].item(1)
            if Distance(x1,y1,x2,y2)<500:
                rcontours[i][j,0,0] = (rcontours[i][j,0,0]+rcontours[i][j+1,0,0])/2
                rcontours[i][j,0,1] = (rcontours[i][j,0,1]+rcontours[i][j+1,0,1])/2
                rcontours[i] = rcontours[i][:-1]
            j+=1
    #print(rcontours[1][0,0,0])        
    connections = []
    for i in range(len(FinalNodes)):
        connections.append([])



    i = 0
    while i< len(rcontours):
        if not(len(rcontours[i])==2):
            rcontours.pop(i)
        else:
            i+=1
    for i in rcontours:
        cv.drawContours(blank,i,-1,(0,0,255),4)
        #print(i,'\n\n\n')

    for i in rcontours:
        n = 0
        a = []
        #print(i[0,0]) for (x,y)
        x1 = i[0,0,0]
        y1 = i[0,0,1]
        x3 = i[1,0,0]
        y3 = i[1,0,1]
        for j in range(len(FinalNodes)):
            x2 = FinalNodes[j][0]
            y2 = FinalNodes[j][1]

            if Distance(x1,y1,x2,y2)<1500 or Distance(x3,y3,x2,y2)<1500:
                n +=1
                a.append(j)
            if n>=2:
                connections[a[0]].append(a[1])
                connections[a[1]].append(a[0])
                
                break
    
    
    for i in connections:
        connections[connections.index(i)] = list(set(i))
    
    for i in range(len(connections)):
        for j in connections[i]:
            cv.line(blank,FinalNodes[i],FinalNodes[j],(255,0,0),2)
    
    for i in range(len(FinalNodes)):
        cv.putText(blank,str(i),FinalNodes[i],cv.FONT_HERSHEY_TRIPLEX,1,(255,255,0),1)
    #check for refined points of the lines
    #check if any of the nodes are in 900 radius then it is connected. 
    #cv.imshow("any", blank)
    global adjn,nodes 
    adjn = connections
    nodes = FinalNodes
    Djikstras(3,10)
    cv.imshow("pointOnBlank",blank)  
    cv.waitKey(0)


def Djikstras(sP,eP):      #sP is start point and eP end point
    tw = []
    visited = []
    for i in range(len(adjn)):
        tw.append([inf,0])
    tw[sP][0] = 0
    sp = sP
    for i in range(20):
        for j in range(len(adjn[sp])):
            point = adjn[sP][j]
            if point in visited :
                continue
            
            x1 = nodes[point][0]
            y1 = nodes[point][1]
            x2 = nodes[sp][0]
            y2 = nodes[sp][1]
            d = Distance(x1,y1,x2,y2)
            if(d<tw[point][0]):
                tw[point][0] = d
                tw[point][1] = sp
            visited.append(point)
    print(tw)
    

FNode()
