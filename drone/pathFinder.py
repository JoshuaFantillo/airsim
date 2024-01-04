import airsim
from airsim import Vector3r, Quaternionr, Pose
import functools
from .mapMaker import getMapDict
import math
import random
#class initiats and sets up nodes
class Node:
    def __init__(self, parent, location):
        self.parent = parent
        # Let location be array [x,y]. parent must be a Node
        self.location = location
        # For herustic function f = g + h 
        # where g is distance current node to start
        # where h is the estimate distance (herustic) to goal
        # Each node should calculate its own herustic function f
        self.g = 0
        self.h = 0
        self.f = 0
    def __eq__(self, cityNode):
        # Compare city names, if they are the same its the same node
        # print("Current self is")
        # print(self.location)
        # print("Current citynode is")
        # print(cityNode)
        return functools.reduce(lambda x, y : x and y, map(lambda p, q: p == q,self.location,cityNode.location), True) 

		#returns path from point A to B
    def PathsFromAToB(self,a,b):
        return functools.reduce(lambda x, y : x and y, map(lambda p, q: p == q,a.parent,b.location), True) 

    def __repr__(self) -> str:
        return "Node->("+str(self.location)+")"
    
    def getLocation(self):
        return self.location

		#adds the heuristic cost and distance cost
    def addHerusticData(self,g,h):
        self.g = g
        self.h = h
        self.f = self.g + self.h
    


# For making all the possible routes
def createNode(parent,currentaxsis,g,h):
    currentNode = Node(parent, currentaxsis)
    currentNode.addHerusticData(g,h)
    return currentNode

	#gets the distance between the two locatons
def distanceBetween(loc1,loc2):
    distance = (loc1[0] - loc2[0])**2 + (loc1[1] - loc2[1])**2
    # print(distance)
    distance = math.sqrt(abs(distance))
    return distance

	#function to create the maze that the drone must traverse 
def createMaze():

    mapDict = getMapDict()

    nodeDict = {}

    for key in mapDict.keys():
        nodeDict[key] = createNode(None,mapDict[key],0,0)

    # print(nodeDict)
	#class to add points to the maze
    def addToMazeArr(mazelist:list,node1,node2):
        random.seed(0)
        arg1 = nodeDict[node1]
        arg2 = nodeDict[node2]
        arg3 = distanceBetween(arg1.getLocation(),arg2.getLocation())
        heuristic = random.randint(5,10)
        heuristic = math.floor(arg3 - heuristic)
        if(heuristic < 0):
            heuristic = 0
        connection1 = createNode(arg1,arg2.getLocation(),arg3,heuristic)
        connection2 = createNode(arg2,arg1.getLocation(),arg3,heuristic)
        mazelist.append(connection1)
        mazelist.append(connection2)
    
    mazeArr = []
	#adds points to the maze
    addToMazeArr(mazeArr,"O","HY1")
    addToMazeArr(mazeArr,"O","H1")
    addToMazeArr(mazeArr,"O","I4")
    addToMazeArr(mazeArr,"H1","H2")
    addToMazeArr(mazeArr,"H2","H3")
    addToMazeArr(mazeArr,"H3","I1")
    addToMazeArr(mazeArr,"I1","H4")
    addToMazeArr(mazeArr,"I4","HX6_7")
    addToMazeArr(mazeArr,"HX6_7","I3")
    addToMazeArr(mazeArr,"I3","HX5")
    addToMazeArr(mazeArr,"HX5","HX2")
    addToMazeArr(mazeArr,"H4","HX2")

    # print("MAZEARRRR")
    # print(mazeArr)
    
    return mazeArr




def pathFinder(city1,city2):
    # Instantiate locations
    maze = createMaze()


    # starting node
    start = Node(None, city1)
    goal = Node(None, city2)

    # The lists, one for current paths, one for travesied paths to prevent infinity loop possibilty
    possiblePaths = []
    previousPaths = []
    #Add the start to the list
    possiblePaths.append(start)   
    # Loop intill you reach the goal  #If list is not empty continue
    while len(possiblePaths) > 0:
        # Index so we can pop it outta list
        currentNode = possiblePaths[0]
        currentIndex = 0

        # Compare nodes f function, pick smallest, set as currentNode
        for index, val in enumerate(possiblePaths):
            if val.f < currentNode.f:
                currentNode = val
                currentIndex = index
        # Remove the smallest route from list, so we can add its neighbouring nodes after
        possiblePaths.pop(currentIndex)
        print("Path Removed: "+",".join(str(e) for e in currentNode.location))
        previousPaths.append(currentNode)

        # If goal is found
        if currentNode == goal:
            path = []
            current = currentNode

            # Make an array of the path from goal to start, return back array of strings
            while current is not None:
                # print("Path was called")
                path.append(current.location)
                # print(current.__dict__)
                current = current.parent
            path = path[::-1]
            return path

        indexToDelete = []
        # Add Possible paths of the removed path
        for index, val in enumerate(maze):
            if val.parent == currentNode:
                indexToDelete.append(index)
                newMaze = []
                # Add path to the possiblepaths 
                # I need to send data where parent: Node they came from location: location
                possiblePaths.append(createNode(currentNode,val.location,val.g,val.h))


        # If I remove an index, it shifts the index....
        newMaze = [v for i, v in enumerate(maze) if i not in indexToDelete]
        maze = newMaze
        for index in maze:
            print("Newmaze is")
            print(index.parent.__dict__,index.__dict__)


# client = airsim.MultirotorClient()
# client.confirmConnection()
# client.enableApiControl(True)
# client.armDisarm(True)

# here = pathFinder([0,0,-20],[50,20,-20])
# print(here)


# state = client.getMultirotorState()
# client.takeoffAsync().join()
# client.moveToPositionAsync(newArray[0][0], newArray[0][1], newArray[0][2], 1).join()
# client.moveToPositionAsync(newArray[1][0], newArray[1][1], newArray[1][2], 1).join()
