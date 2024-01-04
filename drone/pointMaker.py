from .mapMaker import getMapDict

#This class helps get the nodes in the map that will be used
def nodePointsGet():
    nodePointsDict = getMapDict()
    nodePointVals = list(nodePointsDict.values())
    listofPoints = list(nodePointsDict.keys())
    print("The following points are available:\n")
    for x in listofPoints:
        print(listofPoints.index(x)," :: ", x)

    start = nodePointsDict[listofPoints[0]]

    end = nodePointsDict[listofPoints[int(input("Enter end point index: "))]]

    print("Start node: ", start)
    print("End node: ", end)

    return start,end,nodePointVals

# nodePointsGet()