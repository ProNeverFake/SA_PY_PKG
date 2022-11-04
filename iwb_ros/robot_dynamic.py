print("import robot_dynamic: start.")
# import builtin
import os
import math
from pickle import TRUE
import numpy as np
# import kdl relevant

import PyKDL

from urdf_parser_py.urdf import URDF
from pykdl_utils.kdl_parser import kdl_tree_from_urdf_model

# from pykdl_utils.kdl_kinematics import KDLKinematics
# import pykdl_utils.kdl_kinematics
import pykdl_utils.joint_kinematics as kdl_jk

# import ros relevant (if necessary)
import rospy
import rosgraph

# iwb_ros modules
import iwb_ros.robot_base


# TODO
# You should turn to the source codes of pykdl_utils.joint_kinematics to understand how
# the following codes work. At least you need to find some methods IWB_KDL inherits from JointKinematicsWait,
# which are not rewritten here.   

# this is now a method in IWB_KDL
def create_IWB_KDL(base_link, end_link, urdf_filename=None, timeout=2., wait=True, description_param="robot_description"):
    # reformulate the function in kdl_jk to create a new IWB_KDL obj
    if urdf_filename is None:
        urdf_model = URDF.from_parameter_server(key=description_param)
    else:
        # TODO file reading in python, Robot class: what?
        # f = open(urdf_filename, 'r')
        # robot = Robot.from_xml_string(f.read())
        # f.close()
        pass
    
    tree = kdl_tree_from_urdf_model(urdf_model) 

    if wait:
        return IWB_KDL(urdf_model, base_link, end_link, tree)
    else:
        pass
        # return JointKinematicsWait(robot, base_link, end_link, timeout)

# differece between JointKinematics and JointKinematicsWait: whether wait for order to 
# subscribe the topic.

#######################################
# kdl_robot = URDF.from_parameter_server()
# tree = kdl_tree_from_urdf_model(kdl_robot)
# print(tree.getNrOfSegments())
# base_link = "base_link"
# end_link = "link_6_x"
# chain = tree.getChain(base_link, end_link)
# q = [0]*18
# jcb = test_kdl_obj.jacobian(q)
# mass = test_kdl_obj.inertia(q)
#######################################
class IWB_KDL(kdl_jk.JointKinematics):

    read_from_server = ""
    # URDF file path
    urdf_path = ""
    # attr in kdl module format: prefix kdl
    __kdl_urdf_model = ""
    __kdl_tree = ""
    __kdl_chain = ""

    # about iwb robot
    robot_base_link = ""
    robot_end_link = ""
    robot_joint_name = ""
    robot_joint_states = ""
    robot_jacobian = ""
    robot_mass_matrix = ""
    # __eigenfreq = ""
    
    # use the init method from kdl_kine.
    # def __init__(self):
    #     # read urdf model
        
    #     # set up kdl tree

    #     # set up kdl chain

    #     pass

    # old init, out of date
    # def __init__(self, urdf_model, base_link, end_link, kdl_tree=None):
    #     super(IWB_KDL, self).__init__(urdf_model, base_link, end_link, kdl_tree)
    #     self.robot_base_link = base_link
    #     self.robot_end_link = end_link
    #     self.robot_joint_name = self.get_joint_names()

    def __init__(self, base_link, end_link, urdf_filename = None, read_from_server = True):
        
        self.read_from_server = read_from_server
        # get robot structure from urdf file
        urdf_model = self.parse_urdf(urdf_filename)
        # call parent init. method to build the kdl obj
        
        try:
            if self.is_ros_online():
                rospy.init_node('pykdl_listener', anonymous=False)
                kdl_jk.JointKinematics.__init__(self, urdf_model, base_link, end_link)
        except Exception as e:
            iwb_ros.robot_base.exception_track(e)
        
        
        self.robot_base_link = base_link
        self.robot_end_link = end_link

    # parse the urdf file to get robot structure 
    def parse_urdf(self, urdf_filename=None, description_param="robot_description"):
        # reformulate the function in kdl_jk to create a new IWB_KDL obj
        if urdf_filename is None:
            urdf_model = URDF.from_parameter_server(key=description_param)
        else:
            # TODO file reading in python, Robot class: what?
            # f = open(urdf_filename, 'r')
            # robot = Robot.from_xml_string(f.read())
            # f.close()
            pass
        tree = kdl_tree_from_urdf_model(urdf_model) 
        return urdf_model

    # abd
    def set_joint_position(self, joint_position):
        # TODO: check format  
        self.__joint_position = joint_position

    def is_ros_online(self):
        # check if rosmaster is online 
        ros_online = rosgraph.is_master_online()
        if not ros_online:
            raise iwb_ros.robot_base.RosOfflineError("robot_dynamic")
        else:
            return ros_online
    # decide which method to use
    def get_joint_position(self):
        # if self.wait:
        #     return self.get_joint_state()
        # else:
        #     # self.wait_for_joint_angles()
        #     return self.get_joint_angles()
        return self.get_joint_angles()

    def get_jacobian(self):
        # get current joint states
        robot_joint_state = self.get_joint_position()

        jacobian = self.jacobian(robot_joint_state)

        return jacobian

    def get_mass(self):
        robot_joint_state = self.get_joint_position()
        mass = self.inertia(robot_joint_state)
        return mass

    def get_cart_mass(self):
        robot_joint_state = self.get_joint_position()
        cart_mass = self.cart_inertia(robot_joint_state)
        return cart_mass

    # 3 in 1
    def get_dynamics_all(self):

        robot_joint_state = self.get_joint_position()
        jacobian = self.jacobian(robot_joint_state)
        mass = self.inertia(robot_joint_state)
        cart_mass = self.cart_inertia(robot_joint_state)

        return (robot_joint_state, jacobian, mass, cart_mass)
    
    def shutdown(self):
        # how?
        pass

print("import robot_dynamic: ok.")



