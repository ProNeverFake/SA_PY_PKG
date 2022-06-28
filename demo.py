#!/usr/bin/env python

# import sys
import sys
import os
# sys.path.append("~/my_pkg")
import subprocess
import iwb_ros.robot
import iwb_ros.test




# # start roscore
# print("launch roscore: start")
# try:
#     subprocess.Popen(['roscore'], stdout=subprocess.PIPE)
#     print("launch roscore: ok")
# except:
#     print("start roscore: error")




# instantiation
print("creat robot object: start")
# robot = iwb_ros.robot.IWB_Robot()
try:
    robot = iwb_ros.robot.IWB_Robot()
    print("creat robot object: ok")
except:
    print("!!!Fatal: create obj failed.!!!")


# #################################### visualization code ################################
# print("launch visualization: start")
# # start rviz
# robot.visualization()
# # start fake controller
# robot.fake_controller()
# # user self-programmed code with set function
# # a simple example:
# import rosnode
# print(rosnode.get_node_names())

# joint_position = [0]*18
# i = 0
# n = 0.01
# t = 0



# while True:
#     t = t + 1
#     # print(joint_position)
#     joint_position[0] = i
#     joint_position[1] = i
#     joint_position[2] = i
#     joint_position[17] = i
#     joint_position[14] = i
#     robot.send_joint_position(joint_position)
#     i = i + n

#     if i > 3.14:
#         i = -3.14
    
#     if t >= 2000:
#         break

# robot.shutdown_all()
# ##################################################################################

################################# test block ###################################
print("launch motion planning: start")
# start rviz
robot.visualization()

from urdf_parser_py.urdf import URDF


from pykdl_utils.kdl_parser import kdl_tree_from_urdf_model

# test roslib
# import roslib
# roslib.load_manifest("pykdl_utils")

# problematisch import

import pykdl_utils.joint_kinematics
from pykdl_utils.kdl_kinematics import KDLKinematics
kdl_robot = URDF.from_parameter_server()
tree = kdl_tree_from_urdf_model(kdl_robot)
print(tree.getNrOfSegments())
base_link = "base_link"
end_link = "link_6_x"
chain = tree.getChain(base_link, end_link)

test_kdl_obj = KDLKinematics(kdl_robot, base_link, end_link)
print(test_kdl_obj.get_joint_names())

print(chain.getNrOfJoints())
# q = test_kdl_obj.random_joint_angles()
q = [0]*18
jcb = test_kdl_obj.jacobian(q)
mass = test_kdl_obj.inertia(q)
mass_cart = test_kdl_obj.cart_inertia(q)
import numpy as np

with open('outfile.txt', 'wb') as f:
    for line in mass:
        np.savetxt(f, line, fmt='%.2f')

print(mass)
print("J")
print(jcb)
################################################################################

#################################### motion planning code ##########################
# print("launch motion planning: start")
# # start rviz
# robot.motion_visualization()

# from urdf_parser_py.urdf import URDF


# from pykdl_utils.kdl_parser import kdl_tree_from_urdf_model
# kdl_robot = URDF.from_parameter_server()
# tree = kdl_tree_from_urdf_model(kdl_robot)
# print(tree.getNrOfSegments())
# chain = tree.getChain(base_link, end_link)
# print(chain.getNrOfJoints())


# # start fake controller
# robot.fake_controller()
# # user self-programmed code with set function
# # a simple example:
# import rosnode
# print(rosnode.get_node_names())

# joint_position = [0]*18
# i = 0
# n = 0.01
# t = 0



# while True:
#     t = t + 1
#     # print(joint_position)
#     joint_position[0] = i
#     joint_position[1] = i
#     joint_position[2] = i
#     joint_position[17] = i
#     joint_position[14] = i
#     robot.send_joint_position(joint_position)
#     i = i + n

#     if i > 3.14:
#         i = -3.14
    
#     if t >= 2000:
#         break

robot.shutdown_all()

