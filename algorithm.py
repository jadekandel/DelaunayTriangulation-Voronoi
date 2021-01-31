"""############################################
Algorithms Final Project
Delaunay Triangulations to Voronoi Diagram
Jade Kandle, Katie Munger, Matthew Rasmussen 
############################################"""

from graphics import *
import math
import random

#triangle object 
class Triangle:
  def __init__(self, point1, point2, point3):
    self.point1 = point1  
    self.point2 = point2
    self.point3 = point3
    
    self.edge1 = Line(point1, point2)
    self.edge2 = Line(point2, point3)
    self.edge3 = Line(point3, point1)
  
    #returns circumcenter
    self.circumcenter = getCircumcenter(point1, point2, point3)
    #returns radius squared 
    self.circumradius = getRadius(self.circumcenter, point1) 

#linked list that stores incomplete triangles
class Node:
  def __init__(self,triangle):
    self.data = triangle
    self.next = None

class LinkedList:
  def __init__(self):
    self.head = Node(None) 
    self.tail = None
    self.head.next = self.tail

  def add(self, newData):
    newNode = Node(newData)
    neighborNode = self.head.next
    self.head.next = newNode
    newNode.next = neighborNode

  def delete(self,triangle):
    currNode=self.head
    while currNode.next.data != None:
      if currNode.next.data==triangle:
        currNode.next=currNode.next.next
        return 
      else:
        currNode=currNode.next
            
def createSupertriangle(sortedPoints):
  #create a Supertriangle that 
  length = len(sortedPoints)-1
  #find max x
  maxX = sortedPoints[-1].getX()
  #find min x
  minX = sortedPoints[0].getX()

  #find max y and min y 
  maxY = sortedPoints[0].getY()
  minY = sortedPoints[length].getY()
  for point in sortedPoints:
    currentY = point.getY()
    if currentY > maxY:
      maxY = currentY
    if currentY < minY:
      minY = currentY

  #create margins
  widthMargin = (maxX - minX)
  heightMargin = 1.2 * (maxY - minY)

  #coordinates of rectanlge encompassing all points
  bL = Point(minX, minY)
  tL = Point(minX, maxY)
  tR = Point(maxX, maxY)
  bR = Point(maxX, minY)

  #make point of triangle by adding margins 
  pointA = Point(bL.getX()- widthMargin, bL.getY()-10)
  pointB = Point(bR.getX()+ widthMargin, bL.getY()-10)
  pointC = Point(minX + widthMargin/2, maxY + heightMargin)

  superTriangle = Triangle(pointA, pointB, pointC)
  
  return superTriangle 

def sortPoints(pointList):
  #given a list of points order them by increasing #x-circumcenterCoordinates
  #using mergesort
  if len(pointList) > 1:
    middle = len(pointList)//2
    left = pointList[:middle]
    right = pointList[middle:]

    sortPoints(left)
    sortPoints(right)

    i = j = k = 0

    while i < len(left) and j < len(right):
      leftHolder = left[i]
      rightHolder = right[j]
      if leftHolder.getX() < rightHolder.getX():
        pointList[k] = leftHolder
        i += 1
      else:
        pointList[k] = rightHolder
        j += 1
      k += 1

    while i < len(left):
      pointList[k] = left[i]
      i += 1
      k += 1
    while j < len(right):
      pointList[k] = right[j]
      j += 1
      k += 1
  return pointList 

def drawTriangles(completeTri, window):
  #draw each edge in completeTri
  count = 0
  for i in range (len(completeTri)):
      triangle = completeTri[i]
      edge1 = triangle.edge1
      edge2 = triangle.edge2
      edge3 = triangle.edge3
      edge1.draw(window)
      edge2.draw(window)
      edge3.draw(window)
      count = count + 1

def getCircumcenter(point1,point2,point3):
    #perpendicular bisector of 1st edge
    l1 = Line(point1, point2)
    midpoint1 = l1.getCenter()
    midpointX1 = midpoint1.getX()
    midpointY1= midpoint1.getY()
    #y=mx+b. b=y-mx.
    base = point2.getY()-point1.getY()
    if point2.getY()-point1.getY()==0:
      base=0.01
    slope1 = - ((point2.getX()-point1.getX())/base)
    b1= midpointY1 - (midpointX1 * slope1) #solve for the y intercept
    
    #perpendicular bisector of 2nd edge
    l2 = Line(point2, point3)
    midpoint2 = l2.getCenter()
    midpointX2 = midpoint2.getX()
    midpointY2= midpoint2.getY()
    #y=mx+b. b=y-mx.
    base=point3.getY()-point2.getY()
    if point3.getY()-point2.getY()==0:
      base=0.01
    slope2 = - ((point3.getX()-point2.getX())/base)
    b2= midpointY2 - (midpointX2 * slope2) #solve for the y intercept
    
    #find point of intersection of bisectors
    base = slope1-slope2
    if slope1-slope2==0:
        base=0.1
    x=(b2-b1)/(base)
    y=(slope1*x)+b1
    return Point(x,y)

def getRadius(point1,point2):
  #find distance between circumcenter and point on triangle
    point1X = point1.getX()
    point1Y = point1.getY()
    point2X = point2.getX()
    point2Y = point2.getY()
    radius = ((point2X -point1X)**2) + ((point2Y-point1Y)**2)
    return radius
    
def drawVoronoi(completeTri, win):
    #for each triangle, look at all other triangles and find neighbors. If they share an edge, connect two triangle's circumcenter
  for i in range (len(completeTri)):
    triangle1=completeTri[i]
    edgeList1 = [triangle1.edge1, triangle1.edge2, triangle1.edge3]
    for j in range (len(completeTri)):
        if i != j:
          triangle2 = completeTri[j] 
          edgeList2 = [triangle2.edge1, triangle2.edge2, triangle2.edge3]
          for edge1 in edgeList1:
            edge1Point1 = edge1.getP1()
            edge1Point2 = edge1.getP2()
            for edge2 in edgeList2:
              edge2Point1 = edge2.getP1()
              edge2Point2 = edge2.getP2()
              if edge1Point1.getX() == edge2Point1.getX() and edge1Point1.getY() == edge2Point1.getY():
                if edge1Point2.getX() == edge2Point2.getX() and edge1Point2.getY() == edge2Point2.getY():
                  line = Line(triangle1.circumcenter,triangle2.circumcenter)
                  line.setOutline("blue")
                  line.draw(win)
              elif edge1Point1.getX() == edge2Point2.getX() and edge1Point1.getY() == edge2Point2.getY():
                if edge1Point2.getX() == edge2Point1.getX() and edge1Point2.getY() == edge2Point1.getY():
                  line = Line(triangle1.circumcenter,triangle2.circumcenter)
                  line.setOutline("blue")
                  line.draw(win)

def main():
  #Create window for drawing 
  window = GraphWin("pattern.ppm", 700, 700)
  
  #create points:
  pointList=[]
  for i in range (100):
    pointList.append(Point(random.randint(150,550),random.randint(150,550)))

  
  #sort points
  pointList = sortPoints(pointList)
  
  #create lists to store complete and incomplete triangles
  completeTri = []
  incompleteTri = LinkedList()

  #create supertriangle
  superTriangle = createSupertriangle(pointList)
  incompleteTri.add(superTriangle)
  
  for i in range (len(pointList)):
    newPoint = pointList[i]
    badEdges = []
  
  #go through incomplete list (While loop), delete triangle either #because it is complete (adding to completeTri) or because it is a bad triangle (add edges to badEdges)
    currNode = incompleteTri.head
    while currNode.next != None:
      currTriangle = currNode.next.data

      x_c = currTriangle.circumcenter.getX()
      x_new = newPoint.getX()
      D2x = (x_c - x_new)**2
      R2 = currTriangle.circumradius
    
      y_c = currTriangle.circumcenter.getY()
      y_new = newPoint.getY()
      D2 = (D2x + (y_c - y_new)**2)
 
      if D2x > R2:
        completeTri.append(currTriangle)
        incompleteTri.delete(currTriangle)
      
      elif D2 < R2:
        badEdges.append(currTriangle.edge1)
        badEdges.append(currTriangle.edge2)
        badEdges.append(currTriangle.edge3)
        incompleteTri.delete(currTriangle)

      else: #move current node b/c nothing is deleted
        currNode = currNode.next

  #go through all edges of badEdges (loop through for each edge in badEdges) -> somehow 
    polygon = []
    
    for k in range (len(badEdges)):
      copy = False
      for j in range(len(badEdges)):
        if k!= j:
          p1X=badEdges[k].getP1().getX()
          p1Y=badEdges[k].getP1().getY()
          p2X=badEdges[k].getP2().getX()
          p2Y=badEdges[k].getP2().getY()

          q1X=badEdges[j].getP1().getX()
          q1Y=badEdges[j].getP1().getY()
          q2X=badEdges[j].getP2().getX()
          q2Y=badEdges[j].getP2().getY()
          
          if (p1X == q1X and p1Y==q1Y and p2X==q2X and p2Y==q2Y) or (p1X == q2X and p1Y==q2Y and p2X==q1X and p2Y==q1Y) :  
            copy = True          
            
      if copy==False:
        polygon.append(badEdges[k])
        currNode=incompleteTri.head
    
    #draw triangles from polygon edges to point 
    for item in polygon:
      point1 = item.getP1()
      point2 = item.getP2()
      newTriangle = Triangle(point1, point2, newPoint)
      incompleteTri.add(newTriangle)
   
    #once we have added last point, add remaining incomplete triangles to complete triangles and draw
    if i == len(pointList)-1:
      currNode = incompleteTri.head.next
      while currNode != None:
        triangle = currNode.data
        completeTri.append(triangle)
        currNode = currNode.next
      
      #loop through completeTri moving triangles not 
      #attatched to a Supertriangle point to a new list
      #essentially deleting the bad triangles 
      triangleFinal = []
      pointAX = superTriangle.point1.getX()
      pointAY = superTriangle.point1.getY()
  
      pointBX = superTriangle.point2.getX()
      pointBY = superTriangle.point2.getY()
  
      pointCX = superTriangle.point3.getX()
      pointCY = superTriangle.point3.getY()

      for triangle in completeTri:
        point1X = triangle.point1.getX()
        point1Y = triangle.point1.getY()
        if point1X == pointAX and point1Y == pointAY or point1X == pointBX and point1Y == pointBY or point1X == pointCX and point1Y == pointCY:
          continue 

        point2X = triangle.point2.getX()
        point2Y = triangle.point2.getY()
        if point2X == pointAX and point2Y == pointAY or point2X == pointBX and point2Y == pointBY or point2X == pointCX and  point2Y == pointCY:
          continue 

        point3X = triangle.point3.getX()
        point3Y = triangle.point3.getY()
        if point3X == pointAX and point3Y == pointAY or  point3X == pointBX and point3Y == pointBY or  point3X == pointCX and point3Y == pointCY:
          continue 
        else:
          triangleFinal.append(triangle)

      #draws the Delaunay Triangulation
      drawTriangles(triangleFinal, window)
      #draws the Voronoi Diagram 
      drawVoronoi(triangleFinal, window)
      
main()
