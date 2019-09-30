#!/usr/bin/env python
from math import sin, cos, asin, acos
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Pose
import sys

class coordinate:
    x = 0.0
    y = 0.0
    z = 0.0

my_string = ""
my_string1 = ""

temp_x1 = 0;
temp_x2 = 0;
temp_x3 = 0;
temp_q1 = 0;
temp_q2 = 0;
temp_q3 = 0;
temp_q4 = 0;

temp_action = ""

def callback(data):
    global my_string
    my_string = data.data

def callback1(data):
    global temp_x1, temp_x2, temp_x3, temp_q1, temp_q2, temp_q3, temp_q4;
    temp_x1 = data.position.x
    temp_x2 = data.position.y
    temp_x3 = data.position.z
    temp_q1 = data.orientation.w
    temp_q1 = data.orientation.x
    temp_q1 = data.orientation.y
    temp_q1 = data.orientation.z

def callback_action(data):
    global temp_action
    temp_action = data.data

def globalCameraCoordinate(pointGlobalCoordinate, pointLocalCoordinate, theta):
    mapGlobalCoordinate = coordinate()
    mapGlobalCoordinate.x = pointGlobalCoordinate.x - pointLocalCoordinate.x*(cos(theta)) + pointLocalCoordinate.y*(sin(theta))
    mapGlobalCoordinate.y = pointGlobalCoordinate.y - pointLocalCoordinate.x*(sin(theta)) - pointLocalCoordinate.y*(cos(theta))
    mapGlobalCoordinate.z = pointGlobalCoordinate.z - pointLocalCoordinate.z
    return mapGlobalCoordinate

def getTheta(pointGlobalCoordinate1, pointGlobalCoordinate2, pointLocalCoordinate1, pointLocalCoordinate2):
    sin_theta_num = (((pointLocalCoordinate1.x - pointLocalCoordinate2.x)*(pointGlobalCoordinate1.y - pointGlobalCoordinate2.y)) - ((pointGlobalCoordinate1.x - pointGlobalCoordinate2.x)*(pointLocalCoordinate1.y - pointLocalCoordinate2.y)))
    sin_theta_den = ((pointLocalCoordinate1.x - pointLocalCoordinate2.x)*(pointLocalCoordinate1.x - pointLocalCoordinate2.x)) + ((pointLocalCoordinate1.y - pointGlobalCoordinate2.y)*(pointLocalCoordinate1.y - pointGlobalCoordinate2.y))
    sin_theta = sin_theta_num/sin_theta_den
    return asin(sin_theta)

def CameraToMap(globalCameraCoordinate, pointLocalCoordinate, theta):
    pointGlobalCoordinate = coordinate()
    pointGlobalCoordinate.x = globalCameraCoordinate.x + ((pointLocalCoordinate.x*cos(theta)) - (pointLocalCoordinate.y*sin(theta)))
    pointGlobalCoordinate.y = globalCameraCoordinate.y + ((pointLocalCoordinate.x*sin(theta)) + (pointLocalCoordinate.y*cos(theta)))
    pointGlobalCoordinate.z = globalCameraCoordinate.z + pointLocalCoordinate.z
    return pointGlobalCoordinate

def isLandmarkPresent(landmarkName):
    inFile = open('landmarks.txt')
    for line in inFile:
        if(line.find(landmarkName) != -1):
            return True
    inFile.close()
    return False

def getLandmarkCoordinate(landmarkName):
    file = open('landmarks.txt')
    returnCoordinate = coordinate()
    for line in file:
        temp_index = line.find(landmarkName)
        if(temp_index != -1):
            pos_x = line.find('x:')
            pos_y = line.find('y:')
            pos_z = line.find('z:')
            x = float(line[(pos_x+2):(pos_y-1)])
            y = float(line[(pos_y+2):(pos_z-1)])
            z = float(line[(pos_z+2):(temp_index-1)])
            returnCoordinate.x = x
            returnCoordinate.y = y
            returnCoordinate.z = z
    file.close()
    return returnCoordinate

def main():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("/action", String, callback_action)

    while(True):
        rospy.Subscriber("/action", String, callback_action)

        if(temp_action == "save_landmark"):
            rospy.Subscriber("/chatter", String, callback)
            rospy.Subscriber("/amcl_pose", Pose, callback1)
            data1 = my_string.split()
            print(len(data1))
            if(len(data1) == 6):
                object_name = data1[0]
                x = float(data1[3])
                y = float(data1[4])
                z = float(data1[5])
                temp = y
                y = z
                z = -temp
                print(str(x) + " " + str(y) + " " + str(z))

                pointLocalCoordinate = coordinate()
                pointLocalCoordinate.x = x
                pointLocalCoordinate.y = y
                pointLocalCoordinate.z = z
                globalCameraCoordinate = coordinate()
                globalCameraCoordinate.x = temp_x1
                globalCameraCoordinate.y = temp_x2
                globalCameraCoordinate.z = temp_x3
                or_w = temp_q1
                or_x = temp_q2
                or_y = temp_q3
                or_z = temp_q4
                theta = 2*acos(or_w)
                print(x)
                pointGlobalCoordinate = coordinate()
                pointGlobalCoordinate = CameraToMap(globalCameraCoordinate, pointLocalCoordinate, theta)
                if(isLandmarkPresent(object_name) == False):
                    tempWrite = str(pointGlobalCoordinate.x) + " " + str(pointGlobalCoordinate.y) + " " + str(pointGlobalCoordinate.z) + " " + object_name + "\n"
                    myFile = open('landmarks.txt', 'a+')
                    myFile.write(tempWrite)
                    myFile.close()
                else:
                    print("landmark already present")
        elif(temp_action == "find_camera"):
            rospy.Subscriber("/chatter", String, callback)
            rospy.Subscriber("/amcl_pose", Pose, callback1)
            or_w = temp_q1
            theta = 2*acos(or_w)
            print('theta = ' + str(theta))
            data1 = my_string.split()
            if(len(data1) == 6):
                landmarkLocalCoordinate = coordinate()

                landmarkLocalCoordinate.x = float(data1[3])
                landmarkLocalCoordinate.y = float(data1[4])
                landmarkLocalCoordinate.z = float(data1[5])
                theta = 2*acos(temp_q4)

                if(isLandmarkPresent(landmarkName)):
                    landmarkName = data1[0]
                    globalLandmarkCoordinate = getLandmarkCoordinate(landmarkName)
                    cameraCoordinate = globalCameraCoordinate(globalLandmarkCoordinate, landmarkLocalCoordinate, theta)
                    print('x:' + str(cameraCoordinate.x) + ' y:' + str(cameraCoordinate.y) + ' z:' + str(cameraCoordinate.z))
                    pub = rospy.Publisher('/amcl_pose', std_msgs.msg.Pose(), queue_size=10)
                    given_pose = Pose()
                    given_pose.position.x = cameraCoordinate.x
                    given_pose.position.y = cameraCoordinate.y
                    given_pose.position.z = cameraCoordinate.z
                    pub.publish(given_pose)
                else:
                    raise Exception('landmark information not present!')

main()
