# import builtin
import os
import math
# import kdl relevant

from urdf_parser_py.urdf import URDF
from pykdl_utils.kdl_parser import kdl_tree_from_urdf_model

# import ros relevant (if necessary)
# TODO

def robot_dynamic_init():
    
    # prerequisite: roscore online, param /robot_description was set.

    # TODO: check if roscore is online, throw exception if not
    # TODO: check if /robot_description was set, throw exception if not

    # read the robot structure param from rosparam server
    # TODO
    robot_structure = URDF.from_parameter_server()


    return robot_structure

def get_dynamic_tree(robot_structure):
    # get the dynamic tree of the robot
    # TODO
    pass

def get_jacobian(args):
    # get the echtzeitlich jacobian matrix
    # TODO
    pass

def read_joint_state():
    # read the joint states from the topic /joint_states
    # TODO
    pass







