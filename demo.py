#!/usr/bin/env python

# import system module
# import sys
# import os
# sys.path.append("~/my_pkg")
# import subprocess
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
print("launch visualization: start")
# start rviz
robot.visualization()
# start fake controller
robot.fake_controller()
# start robot motion example
robot.iwb_state_publisher_start()
# start iwb_kdl
robot.iwb_kdl_start()

while True:
    (joint_states, jacobian, mass, cart_mass) = robot.iwb_kdl_get_dynamics_all()
    print(joint_states)
    print(cart_mass)
    print("##########################################")
    # print(mass)


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

