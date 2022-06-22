print("import robot_dynamic: start.")
# import builtin
import os
import math
import numpy as np
# import kdl relevant

import PyKDL
from urdf_parser_py.urdf import URDF
from pykdl_utils.kdl_parser import kdl_tree_from_urdf_model
# from pykdl_utils.kdl_kinematics import KDLKinematics
import pykdl_utils.kdl_kinematics


# import ros relevant (if necessary)
import rospy
import rosgraph


# TODO

# inherite the class from kdl_kinematics 
class IWB_KDL(KDLKinematics):
    # attr in kdl module format: prefix kdl
    __kdl_urdf_model = ""
    __kdl_tree = ""
    __kdl_chain = ""

    # about robot
    base_link = ""
    end_link = ""
    __joint_position = ""
    jacobian = ""
    __mass_matrix = ""
    # __eigenfreq = ""
 
    # use the init method from kdl_kine.
    # def __init__(self):
    #     # read urdf model
        
    #     # set up kdl tree

    #     # set up kdl chain

    #     pass

    def set_joint_position(self, joint_position):
        # TODO: check format  
        self.__joint_position = joint_position
    
    def get_joint_position(self):
        return self.__joint_position

    def is_ros_online():
        # check if rosmaster is online 
        # rospy.is_shutdown() # inverse
        ros_online = rosgraph.is_master_online()
        return ros_online

    def robot_dynamic_init(robot):
        
        # prerequisite: roscore online, param /robot_description was set.
        # TODO: check if roscore is online, throw exception if not

        # TODO: check if /robot_description was set, throw exception if not
        # here only read from server actually

        return robot

    def read_urdf_model(urdf_filename):
        # read the robot structure param from rosparam server, or from file
        # TODO: if no path is given, read from the server
        if urdf_filename == None:
            # read from server
            try:
                urdf_model = URDF.from_parameter_server()
            except:
                print("!!!Fatal: rd.get_urdf_model: read from server failed.!!!")
        else:
            # TODO: read from file (correctness unsure)
            try:
                urdf_model = URDF.load_xml_file(urdf_filename)
            except:
                print("!!!Fatal: rd.get_urdf_model: read from file failed.!!!")
            
        return urdf_model

    def get_jacobian(args):
        # get the echtzeitlich jacobian matrix
        # TODO
        pass

    def read_joint_state():
        # read the joint states from the topic /joint_states
        # TODO
        pass



print("import robot_dynamic: ok.")



