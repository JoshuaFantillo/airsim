import os
import pprint
import tempfile
import time

import airsim
import cv2
import numpy as np
from airsim import Pose, Quaternionr, Vector3r

import drone.pathFinder as pathFinder
import drone.pointMaker as pointMaker
import drone.setup_path as setup_path

# connect to the AirSim simulator
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)


# GET X,Y Z AXSIS
def coords():
    state = client.getMultirotorState()
    x = pprint.pformat(state.kinematics_estimated.position.x_val)
    y = pprint.pformat(state.kinematics_estimated.position.y_val)
    z = pprint.pformat(state.kinematics_estimated.position.z_val)
    print("x: %s y: %s z: %s" % (x, y, z))

def getGPSData():
    gps_data = client.getGpsData()
    s = pprint.pformat(gps_data)

    print(gps_data.gnss.geo_point.latitude)
    print(gps_data.gnss.geo_point.longitude)

def markersFixedTest():
    # plot points 
    client.simPlotPoints(points = [Vector3r(x,y,0) for x, y in zip(np.linspace(0,50,5), np.linspace(0,0,5))], color_rgba=[1.0, 0.0, 0.0, 1.0], size = 25, is_persistent = True)
    client.simPlotPoints(points = [Vector3r(5,5,0) ], color_rgba=[1.0, 0.0, 0.0, 1.0], size = 25, is_persistent =  True)


# Node points
startPoint, endPoint, nodePoints = pointMaker.nodePointsGet()

# To visualize where the node points are at I placed markers
for index in nodePoints:
    client.simPlotPoints(points = [Vector3r(index[0],index[1],index[2]) ], color_rgba=[1.0, 0.0, 0.0, 1.0], size = 25, is_persistent =  True)
# Made it a function if you want to add different end points NOTE: The drone alaways starts at [0,0,-20] in the airsum by default
def routeToPath():
    # Call A* Search
    flightPath = pathFinder.pathFinder(startPoint,endPoint)
    print("Destination Path")
    print(flightPath)

    # Start flying
    # airsim.wait_key('Press any key to takeoff')
    client.takeoffAsync().join()

    # NOTE: moveToPostion (x,y,z, speed)
    # Fly to destination
    for flightPoint in flightPath:
        coords()
        client.moveToPositionAsync(flightPoint[0], flightPoint[1], flightPoint[2], 5).join()


    client.hoverAsync().join()

    # print("reset")
    # client.reset()

routeToPath()
