import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Pose


def publisher():
    rospy.init_node('action_publisher', anonymous=True)
    pub = rospy.Publisher('action', String, queue_size=1)
    rate = rospy.Rate(2) # Hz
    count = 0
    while not rospy.is_shutdown():
        print(count)
        if(count < 15):
            action_str = "none"
            pub.publish(action_str)
        elif(count < 25):
            action_str = "save_landmark"
            pub.publish(action_str)
        elif(count < 35):
            action_str = "find_camera"
            pub.publish(action_str)
        else:
            action_str = "none"
            pub.publish(action_str)
        count = count + 1
        rate.sleep()
if __name__ == '__main__':
    try:
        publisher()
    except rospy:
        pass
