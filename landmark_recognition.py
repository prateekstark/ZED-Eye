#!/usr/bin/env python
from math import sin, cos, asin, acos
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Pose
import sys
class coordinate:
    frameID = 0
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
        rospy.init_node('listener', anonymous=True)
        if(action == action1):
            count = 10000
            while count >= 0:
                print(count)
                rospy.Subscriber("/chatter", String, callback)
                rospy.Subscriber("/amcl_pose", Pose, callback1)
                count = count - 1
            
            
            print(my_string)
            data1 = my_string.split()
            x = float(data1[5])
            y = float(data1[7])
            z = float(data1[9])
            print(str(x) + " " + str(y) + " " + str(z))
            
            self_x = temp_x1
            self_y = temp_x2
            self_z = temp_x3
            or_w = temp_q1
            or_x = temp_q2
            or_y = temp_q3
            or_z = temp_q4
            theta = 2*acos(or_w)
            print("theta = " + str(theta))


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
            count = 10000
            while(count >= 0):
                rospy.Subscriber("/chatter", String, callback)
                rospy.Subscriber("/amcl_pose", String, callback1)
                count = count - 1
            data1 = my_string.split()
            localx = float(data1[5])
            localy = float(data1[7])
            localz = float(data1[9])
            theta = 2*acos(temp_q4)
            print('theta = ' + str(theta))
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
                pub = rospy.Publisher('/amcl_pose', std_msgs.msg.Pose(), queue_size=10)
                given_pose = Pose()
                given_pose.position.x = cameraCoordinate.x
                given_pose.position.y = cameraCoordinate.y
                given_pose.position.z = cameraCoordinate.z
                pub.publish(given_pose)
            else:
                raise Exception('landmark information not present!')
        else:
            raise Exception('Wrong Arguments')
    else:
        raise Exception('Wrong Arguments')

main()