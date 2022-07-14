#!/usr/bin/env python

# import system module
# import sys
# import os
# sys.path.append("~/my_pkg")
# import subprocess
import iwb_ros.robot
import iwb_ros.test

import sys
sys.path.append("/home/blackbird/iwbrbdl")

# test iwbrbdl
# import iwbRobotics




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
# use this if need motion to varify
#robot.iwb_state_publisher_start()
# start iwb_kdl
robot.iwb_kdl_start()

while True:
    (joint_states, jacobian, mass, cart_mass) = robot.iwb_kdl_get_dynamics_all()
    print(joint_states)
    print(cart_mass)
    

    print("##########################################")
    # remove break if want to try kdl features
    # break



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




######################### here are iwbrbdl codes
import numpy as np
import math

def calcModalParameters(Q, mass, complexModeshapes = False):
        """Calculates and returns the modal parameters (ef, ms, dr) for a given 18D pose
        Args:
            Q ((18,)): 18D pose

        Returns:
            [18x1 array, 18x18 array, 18x1 array]: Modal parameters eigenfrequencies, mode shapes, damping ratios
        """
        # Calc eigenfrequencies f using damped structure analysis
        M = mass

        # Setup of eigenvalue problem
        A = np.block(
            [
                [np.zeros((18, 18)), np.eye((18))],
                [-np.linalg.inv(M).dot(self._K), -np.linalg.inv(M).dot(self._C)],
            ]
        )

        # Solve eigenvalue problems
        if complexModeshapes:
            omega, ms = np.linalg.eig(A)
            ms = ms[::2, ::2]
            ms = np.flipud(np.fliplr(ms))
        else:
            omega, _ = np.linalg.eig(A)
            _ , ms = scipy.linalg.eigh(self._K, M)

    	# Calc mode shapes (i.e. Residues)
        modMs = ms.transpose() @ M @ ms
        for i in range(18):
            ms[:, i] = ms[:, i] / np.sqrt(modMs[i, i])

        # Calc eigenfrequencies and damping ratios
        omega = omega[::2]
        fr = np.sqrt((omega * omega.conjugate()).real)
        dr = -omega.real / fr

        idx = fr.argsort()
        fr = fr[idx]/2/math.pi
        dr = dr[idx]
        if complexModeshapes:
            ms = ms[:,idx]

        log.info("... modal parameters calculated.")

        return fr, ms, dr
