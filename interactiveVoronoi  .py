from graphics import *
import math
import random


def combinations(lst): 
    pairs=[]
    for i in range(len(lst)-1):
        for j in range(i+1,len(lst)):
            pairs.append([lst[i],lst[j]])                           

    return pairs 
                        

def bisector(lst): #create list of all the perpendicular bisectors
    bisectors=[] 
    for i in range(len(lst)):
        point1 = lst[i][0]
        point2 = lst[i][1]
        l = Line(point1, point2)
        midpoint = l.getCenter()
        midpointX = midpoint.getX()
        midpointY= midpoint.getY()

        #y=mx+b. b=y-mx.
        if (point2.getY()-point1.getY()) == 0:
            (point2.getY()-point1.getY()) == 0.1
        slope = - ((point2.getX()-point1.getX())/(point2.getY()-point1.getY()))
        b= midpointY - (midpointX * slope) #solve for the y intercept
        bisectors.append([slope,b])
    return bisectors
        
def intersection(lst1, lst2, border):
    intersections=[Point(0,0),Point(0,border),Point(border,0),Point(border,border)] #corners 
    #for each bisector, find intersections with border:
    for i in range (len(lst1)):
        if lst1[i][0]==0:
            lst1[i][0]=0.1
        y1= (lst1[i][0]*(border)) + lst1[i][1]
        y2= lst1[i][1]
        x1 = (border - lst1[i][1])/lst1[i][0]  
        x2 = (-lst1[i][1])/lst1[i][0]  

        if y1>0 and y1<=border:
            intersections.append(Point(border,y1))
        if y2>0 and y2<=border:           
            intersections.append(Point(0,y2))
        if x1>0 and x1<=border: 
            intersections.append(Point(x1,border))
        if x2>0 and x2<=border: 
            intersections.append(Point(x2,0))

    #intersection with other bisector:
    #pairBisectors = [[slope1,b1], [slope2,b2]]
    if len(lst2)>2:
        for i in range(len(lst2)):
            line1 = lst2[i][0]
            line2 = lst2[i][1]
            m1 = line1[0]
            b1 = line1[1]
            m2 = line2[0]
            b2 = line2[1]
            base = m1-m2
            if m1-m2==0:
                base=0.1
            x = (b2-b1)/(base)
            y = (m1*x) + b1
            if Point(int(x),int(y)) not in intersections and int(x)>0 and int(y)>0 and int(x)<border and int(x)<border: 
                intersections.append(Point(int(x),int(y)))

    return intersections

def getDistance(point1, point2):
    point1X = point1.getX()
    point1Y = point1.getY()
    point2X = point2.getX()
    point2Y = point2.getY()
    distance = int((math.sqrt(((point2X -point1X)**2) + ((point2Y-point1Y)**2))))
    return distance

def closest(iPoint, pointsList): #find which point the intersection point is closest to
    distances = []
    closestDistance=1000
    closestPoints=[]
    for i in range (len(pointsList)):
        point = pointsList[i]
        distance = getDistance(iPoint,point)
        distances.append(distance)
    for i in range (len(distances)):
        if distances[i] < closestDistance-5:
            closestPoints = []
            closestDistance = (distances[i])
            closestPoints.append(i)
        elif closestDistance-5 <= distances[i]<= closestDistance+5:
            closestPoints.append(i)

    #print("ipoint:", iPoint,"distances:", distances, "closestPoints:", closestPoints)
    return closestPoints


def giftwrapping(lst):
    #find firstPoint
    point1 = lst[0]
    xdistance = lst[0].getX()
    for i in range(1, len(lst)):
        if lst[i].getX() < xdistance:
            xdistance = lst[i].getX()
            point1 = lst[i]
        elif lst[i].getX() == xdistance:
            if lst[i].getY() < point1.getY():
                point1= lst[i]
    newL=[point1]
    lst.remove(point1)

    call = True 
    while call==True:
        point2=lst[0]
        for point in lst:
            vector1 = [point2.getX()-point1.getX(), point2.getY()- point1.getY()] 
            vector2 = [point.getX()-point1.getX(), point.getY()- point1.getY()]
            crossproduct = (vector1[0] * vector2[1])-(vector1[1] * vector2[0])
            if crossproduct < 0: #if point2 is to the right of point
                point2 = point 
            elif crossproduct == 0:
                distance1= getDistance(point1,point)
                distance2= getDistance(point1,point2)
                if distance1 < distance2 and point.getX()>point2.getX():
                    point2 = point
     
        newL.append(point2)
        lst.remove(point2)
        point1 = point2
        vector1 = vector2
        if len(newL)==2:
            lst.append(newL[0])

            
        if len(newL)>2 and newL[0].getX()==newL[-1].getX() and newL[0].getY()==newL[-1].getY() :
            call= False     
        if len(lst)==0:
            call= False
        

    #print ("newL:", newL)
    return newL
     
def colorScheme(choice):
    if choice == "leaf":
        return [color_rgb(0,100,0), color_rgb(158,233,73),3]
    if choice == "giraffe":
        return [color_rgb(138,92,47),color_rgb(223,203,123),30]
    if choice =="scales1":
        r1 = random.randint(0,30)
        r2 = random.randint(70,250)
        r3 = random.randint(0,30)
        return [color_rgb(r1,r2,r3),color_rgb(0,100,0),6]
    if choice =="scales2":
        r1 = random.randint(0,0)
        r2 = random.randint(50,170)
        r3 = random.randint(50,170)
        return [color_rgb(r1,r2,r3),color_rgb(255,128,0),6]
    if choice =="dragonfly":
        n = random.randint(0,40)
        return [color_rgb(210 +n,230,240),color_rgb(40,0,0),2]
    if choice == "desert":
        r1 = random.randint(130,150)
        r2 = random.randint(120,150)
        r3 = random.randint(50,80)
        return [color_rgb(r1,r2,r3),color_rgb(0,0,0),10]
        
            
            
def main ():
    border=700
    win = GraphWin("Click Me!",border,border)
    pointsList=[]
    #choices are leaf, giraffe, dragonfly, scales1, scales2 desert
    color = colorScheme("scales1")
    for i in range(1000):
        p = win.getMouse()
        pointsList.append(p)
        for point in pointsList:
            c = Circle(point,3)
            c.setFill(color_rgb(0,0,0))
            c.draw(win)
        background = Polygon(Point(0,0), Point(0,border), Point(border,border),Point(border,0))
        background.setFill(color[1])
        background.draw(win)
   

        if len(pointsList)>1:
            pairPoints = combinations(pointsList)
            bisectorList = bisector(pairPoints)
            pairBisectors = combinations(bisectorList)
            intersectionList = intersection(bisectorList, pairBisectors, border)

            #for i in range (len(intersectionList)):
#                point = intersectionList[i]
#                c = Circle(point,2)
#                c.setFill(color_rgb(255,0,0))
#                c.draw(win)

            L = []
            for i in range (len(pointsList)):
                L.append([])
            
            for iPoint in intersectionList:
                closestPoints = closest(iPoint,pointsList)
                for i in closestPoints:
                    L[i].append(iPoint)
                
            for i in range(len(L)):
                color = colorScheme("scales1")
                newL=giftwrapping(L[i])
                cell = Polygon(newL)
                cell.setOutline(color[1])
                cell.setWidth(color[2])
                cell.setFill(color[0])
                cell.draw(win)
                
                
             
        
        for point in pointsList:
            c = Circle(point,2)
            c.setFill(color_rgb(0,70,0))
            c.draw(win)
                    

        
                

main() 
