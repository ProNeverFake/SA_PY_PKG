#!/usr/bin/env python
print('import iwb_ros.motionplanning: start.')

# the python pkg for ros functionalities
import sys
import copy
import rospy
import moveit_commander

# import the msg type
from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list
import moveit_msgs.msg
import geometry_msgs.msg
from math import pi


# joint goal initialize in the namespace
joint_goal = [0]*18


# <example, to be removed> set the goal
joint_goal[2] = -pi/4
joint_goal[5] = -pi/4
joint_goal[8] = -pi/4
joint_goal[11] = -pi/4
joint_goal[14] = -pi/4
joint_goal[17] = -pi/4

# initialize the node and the commander obj
moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('iwb_state_publisher_moveit', anonymous=True)

# Instantiate a RobotCommander object
robot = moveit_commander.RobotCommander()

# Instantiate a PlanningSceneInterface object
scene = moveit_commander.PlanningSceneInterface()

 # Instantiate a MoveGroupCommander object
 # the name is set in the model and can be change with running moveit wizard
group_name = "robot_arm"
group = moveit_commander.MoveGroupCommander(group_name)

# create the topic for rviz visualize
display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path',
                                            moveit_msgs.msg.DisplayTrajectory,
                                            queue_size=20)


def get_planning_frame():
    return group.get_planning_frame()

def get_end_effector_link():
    return group.get_end_effector_link()

# get a list of all the groups in the robot:
def get_group_names():
    return group.get_group_names()

# get the whole state of the robot
def get_current_state():
    # TODO: get the current joint state using moveit functions
    return group.get_current_state()

# get the joint states
def get_current_joint_values():
    return group.get_current_joint_values()

def get_pose_state():
    # TODO: get the current pose state using moveit functions
    pass 

def set_joint_state():
    # TODO: set the joint goal state with the input param
    pass

# plan
def plan():
    print(group.go(joint_goal, wait=True))
    # Calling ``stop()`` ensures that there is no residual movement
    group.stop()
    # TODO: set the plan with received param
    
def print():
    # print the plan, maybe later
    pass

# the function to publish the msg

print('import iwb_ros.motionplanning: ok.')
    
if __name__ == '__main__':
    pass

