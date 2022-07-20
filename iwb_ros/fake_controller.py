#!/usr/bin/env python

print('import iwb_ros.control_fake: start.')

# this module is designed to "control" the robot state/pose
# but only with simple node and topic, not the control pkg (ros_controller)
# the robot arm should be in position immediately (that's why it's fake controller.)

# also import flag
# TODO: vielleicht soll man hier Attribute in obj IWB_Robot lesen.

# the python pkg for ros functionalities
import iwb_ros.robot_base
import rospy
import rosnode

# import the msg type
from sensor_msgs.msg import JointState
from std_msgs.msg import Header

# Attention: node initialization must be in the main thread.
################# initialize the node when the module is imported
# rospy.init_node('iwb_fake_controller')



def initialize_fake_controller():
    
    # initialize ros parameter for fake controller.
    rospy.set_param('fake_controller/joint_name', 
        ['joint_1_x', 'joint_1_y', 'joint_1_z', 'joint_2_x', 'joint_2_y', 'joint_2_z',
        'joint_3_x', 'joint_3_y', 'joint_3_z', 'joint_4_x', 'joint_4_y', 'joint_4_z',
        'joint_5_x', 'joint_5_y', 'joint_5_z', 'joint_6_x', 'joint_6_y', 'joint_6_z'])
    rospy.set_param('fake_controller/joint_position', [0]*18)



# the function to publish the msg
def start_fake_controller(use_example = False):
    print("info: start the fake controller.")
    # # run initialize function
    initialize_fake_controller()
    # 
    pub = rospy.Publisher('iwb_joint_state', JointState, queue_size=10)

    # rospy.init_node('iwb_fake_controller')
    rate = rospy.Rate(10) # the publishing rate is 10hz
    joint_msg = JointState()

    # while ros is ready
    while not rospy.is_shutdown():

        # the message:
        joint_msg.header = Header()
        joint_msg.header.stamp = rospy.Time.now()
        joint_msg.name = rospy.get_param('fake_controller/joint_name')
        joint_msg.position = rospy.get_param('fake_controller/joint_position')
        joint_msg.velocity = []
        joint_msg.effort = []

        # publish the msg to the topic
        pub.publish(joint_msg)


        # "ros.spin", sleep according to the rospy.Rate (10hz)
        rate.sleep()


def set_fake_controller(joint_position):
    # check dim
    if len(joint_position) != 18:
        print("!!Error in control_fake.set_fake_controller: dimension not correct.!!")
    
    # check if fake controller is alive
    node_list = rosnode.get_node_names()
    if "/iwb_fake_controller" in node_list:
        # fake controller is online, then set the rosparam
        rospy.set_param('fake_controller/joint_position', joint_position)
    else:
        raise iwb_ros.robot_base.NodeNotOnline("fake_controller", "set_fake_controller", "iwb_fake_controller")

# run a simple example for test, but will block the main process
def run_test_example():
    joint_position = [0]*18
    i = 0
    n = 0.01
    t = 0

    while True:

        t = t + 1
        # print(joint_position)
        joint_position[0] = i
        joint_position[1] = i
        joint_position[2] = i
        joint_position[17] = i
        joint_position[14] = i
        set_fake_controller(joint_position)
        i = i + n

        if i > 3.14:
            i = -3.14
        
        if t >= 2000:
            break

    
def kill_fake_controller():
    # delete the parameters
    if rospy.has_param('fake_controller/joint_name'):
        rospy.delete_param('fake_controller/joint_name')
    
    if rospy.has_param('fake_controller/joint_position'):
        rospy.delete_param('fake_controller/joint_position')

    # kill the node if it is alive, otherwise print warning.
    # TODO: use a general function to kill nodes?
    node_list = rosnode.get_node_names()
    try: 

        if "/iwb_fake_controller" in node_list:
            rosnode.kill_nodes("/iwb_fake_controller")
        else:
            raise iwb_ros.robot_base.NodeNotOnline("fake_controller", "kill_fake_controller", "iwb_fake_controller")
    except Exception as e:
        iwb_ros.robot_base.exception_track(e)

# ################################## as reference:#########################
# def set_joint_state():
    
#     # create the publisher with topic "joint_states" with msg-type JointState
#     pub = rospy.Publisher('iwb_joint_state', JointState, queue_size=10)

#     rospy.init_node('iwb_state_publisher_v2')
#     rate = rospy.Rate(10) # the publishing rate is 10hz
#     joint_msg = JointState()

#     i = 0
#     n = 0.01

#     # while ros is ready
#     while not rospy.is_shutdown():

#         # the message:
#         joint_msg.header = Header()
#         joint_msg.header.stamp = rospy.Time.now()
#         joint_msg.name = ['joint_1_x', 'joint_1_y', 'joint_1_z', 'joint_2_x', 'joint_2_y', 'joint_2_z',
#             'joint_3_x', 'joint_3_y', 'joint_3_z', 'joint_4_x', 'joint_4_y', 'joint_4_z',
#             'joint_5_x', 'joint_5_y', 'joint_5_z', 'joint_6_x', 'joint_6_y', 'joint_6_z']
#         joint_msg.position = [0]*18
#         joint_msg.position[17] = i
#         joint_msg.velocity = []
#         joint_msg.effort = []

#         # publish the msg to the topic
#         pub.publish(joint_msg)

#         # msg iteration (rotation)
#         i = i + n 
#         if i > 3.14:
#             i = -3.14


#         # "ros.spin", sleep according to the rospy.Rate (10hz)
#         rate.sleep()


print('import iwb_ros.control_fake: ok.')