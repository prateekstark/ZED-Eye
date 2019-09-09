#!/usr/bin/env python
from math import sin, cos, asin
import rospy
from std_msgs.msg import String
import sys
class coordinate:
    frameID = 0
    x = 0
    y = 0
    z = 0


my_string = ""
my_string1 = ""
def callback(data):
    global my_string
    my_string = data.data
    rospy.loginfo(my_string)

def callback1(data):
    global my_string1
    my_string1 = data.data
    rospy.loginfo(my_string1)



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
    if(len(sys.argv) == 2):
        action = str(sys.argv[1])
        action1 = "save_landmark";
        action2 = "find_camera";

        rospy.init_node('listener1', anonymous=True)
        rospy.init_node('listener', anonymous=True)
        if(action == action1):
            rospy.Subscriber("Chatter", String, callback)
            rospy.Subscriber("Chatter1", String, callback1)
            
            data1 = my_string.split()
            data2 = my_string1.split()
            x = data1[1]
            y = data1[2]
            z = data1[3]
            self_x = data2[1]
            self_y = data2[2]
            self_z = data2[3]
            theta = data2[4]
            objectName = "KUKA Robot"
            pointLocalCoordinate = coordinate()
            pointLocalCoordinate.frameID = 1
            pointLocalCoordinate.x = x
            pointLocalCoordinate.y = y
            pointLocalCoordinate.z = z
            globalCameraCoordinate = coordinate()
            globalCameraCoordinate.x = self_x
            globalCameraCoordinate.y = self_y
            globalCameraCoordinate.z = self_z
            pointGlobalCoordinate = coordinate()
            pointGlobalCoordinate = CameraToMap(globalCameraCoordinate, pointLocalCoordinate, theta)
            reply = input('Do you want to save the landmark to the file?\n')
            if(reply == 'yes'):
                tempWrite = str(pointGlobalCoordinate.x) + " " + str(pointGlobalCoordinate.y) + " " + str(pointGlobalCoordinate.z) + " " + objectName + "\n"
                myFile = open('landmarks.txt', 'a+')
                myFile.write(tempWrite)
                myFile.close()
        elif(action == action2):
            rospy.Subscriber("Chatter", String, callback)
            rospy.Subscriber("Chatter1", String, callback1)
            data1 = my_string.split()
            localx = data1[1]
            localy = data1[2]
            localz = data1[3]
            theta = my_string1.split()[4]
            landmarkLocalCoordinate = coordinate()
            landmarkLocalCoordinate.frameID = 1
            landmarkLocalCoordinate.x = localx
            landmarkLocalCoordinate.y = localy
            landmarkLocalCoordinate.z = localz
            landmarkName = 'KUKA Robot'
            if(isLandmarkPresent(landmarkName)):
                globalLandmarkCoordinate = getLandmarkCoordinate(landmarkName)
                cameraCoordinate = globalCameraCoordinate(globalLandmarkCoordinate, landmarkLocalCoordinate, theta)
                print('x:' + str(cameraCoordinate.x) + ' y:' + str(cameraCoordinate.y) + ' z:' + str(cameraCoordinate.z))
            else:
                raise Exception('landmark information not present!')
        else:
            raise Exception('Wrong Arguments')
    else:
        raise Exception('Wrong Arguments')

main()
