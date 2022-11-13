#!/usr/bin/env python

'''
    This is the benchmark program used in the thesis, which performs all functions in the order of workflow.
    It can be used for function check, and is also a good start point for custumization.
'''

'''import system module'''
# import os
import sys
import numpy as np
# sys.path.append("~/my_pkg")
# import subprocess
'''for error evaluation'''
# import scipy.linalg as LA
import math
'''to import reference value in matlab format'''
from mat4py import loadmat


'''import iwb robot modules'''
import iwb_ros.robot
import iwb_ros.test


'''import ros relevant modules'''
import rospy


'''for possible use of iwbrbdl library'''
sys.path.append("/home/blackbird/iwbrbdl")


'''test code'''
# # start roscore
# print("launch roscore: start")
# try:
#     subprocess.Popen(['roscore'], stdout=subprocess.PIPE)
#     print("launch roscore: ok")
# except:
#     print("start roscore: error")


'''robot instantiation'''
print("creat robot object: start")

try:
    robot = iwb_ros.robot.IWB_Robot()
    print("creat robot object: ok")
except Exception as e:
    iwb_ros.robot_base.exception_track(e)
    print("!!!Fatal: create obj failed.!!!")

'''visualization test code， removable'''
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

'''import reference values for result evaluation'''
# ############################### mat import #######################################

data = loadmat('testdata.mat')
M = data['M']
K = data['K']
C = data['C']
J = data['J']
frequenz = data['fr']

# the sequence of rotation terms and translation terms is inverse
# swap 345 with 012 and use J1 as the jacobian matrix from reference data
J1 = []
index = [3,4,5,0,1,2]
for i in index:    
    J1.append(J[i])

################################################################################

'''main process'''
################################# test block ###################################
print("launch visualization: start")
# start visualization
robot.visualization()
# start fake controller for configuration setting
robot.fake_controller()

# start iwb_kdl
robot.iwb_kdl_start()

# wait 3s for program gets fully launched
rospy.sleep(3)

# the configuration for testing
# joint_position is a 1x18 list
joint_position = [0]*18
joint_position[2] = 1.1529
joint_position[5] = -0.0203
joint_position[8] = -0.7054
joint_position[11] = 1.2842
joint_position[14] = 1.2623
joint_position[17] = -0.8003

# # the old testing program to organize a configuration sequence 
# # to check a continuous configuration change
# for i in range(5):
#     position_list.append(joint_position[:]),
#     joint_position[14] = joint_position[14] + 0.3
#     joint_position[11] = joint_position[11] + 0.3
#     joint_position[8] = joint_position[8] + 0.3

# for possible need of a configuration sequence
position_list = []
position_list.append(joint_position[:]),



####### main work process #########
for x in position_list:

    # set robot configuration
    print("the qd is: ", x)
    robot.robot_send_joint_position(x)
    # wait for the execution of last command
    rospy.sleep(0.2)

    # get joint states, jacobian matrix, mass matrix and cartisian mass matrix
    (joint_states, jacobian, mass, cart_mass) = robot.iwb_kdl_get_dynamics_all()

    # print for check
    print("the joints are now at:\t")
    print(joint_states)
    print("##########################################")
    print("mass matrix at current configuration are:\t")
    print(mass)
    print("##########################################")
    print("jacobian matrix at current configuration are:\t")
    print(jacobian)
    print("##########################################")

#########################################################################

'''another old code block, the only different is that the model file
 modified by moveit! is applied here instead of the original one, 
 which may allow further development in path planning.'''
#################################### test code ##########################

'''use the model modified by moveit!'''
# robot.motion_visualization()

'''pykdl test block, removable'''
# from urdf_parser_py.urdf import URDF

# from pykdl_utils.kdl_parser import kdl_tree_from_urdf_model
# kdl_robot = URDF.from_parameter_server()
# tree = kdl_tree_from_urdf_model(kdl_robot)
# print(tree.getNrOfSegments())
# chain = tree.getChain(base_link, end_link)
# print(chain.getNrOfJoints())
###############################################################

##################### mass comparison #########################
# diff = M-mass
# print("the difference in mass matrix:" , diff)
# print("2-norm error evaluation:", LA.norm(diff))
###############################################################

############### calculation of eigenfrequency #################
A = np.block([
                [np.zeros((18, 18)), np.eye((18))],
                [-np.linalg.inv(mass).dot(K), -np.linalg.inv(M).dot(C)],
            ])

omega, _ = np.linalg.eig(A)
omega = omega[::2]
fr = np.sqrt((omega * omega.conjugate()).real)
fr = fr/2/math.pi
fr = np.flip(fr, 0)

# sort the result by value for the comparison in the next step
fr.sort()
frequenz.sort() 

diff_fr = fr-frequenz
print("the error of fr :", np.mean(np.abs(diff_fr)/frequenz))

diff_M = mass-M
absM = np.abs(diff_M)
print("the error of M :", np.mean(np.abs(diff_M)/M))

diff_J = J1-jacobian
print("the error of J :", np.mean(np.abs(diff_J)))

# export the error matrix as a matlab file
export_dic = {'diff_fr':diff_fr,
             'diff_M': diff_M, 
             'diff_J':diff_J, 
             'perc_diff_fr':np.abs(diff_fr)/frequenz,
             'perc_diff_M':np.abs(diff_M)/M,
             'old_J':J,
             'old_m':M,
             'mass':mass
             }
import scipy.io
scipy.io.savemat('error.mat', export_dic)


#############################################################

'''
call this function for a clean process quit
'''
robot.shutdown_all()