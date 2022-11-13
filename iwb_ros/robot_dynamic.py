'''
    This is the module for pykdl functions. A node is launched to receive
    the message from the robot_state_publisher node. The current robot states are read
    for the calculations of the Jacobian matrix, Mass matrix and eigenfrequencies.
'''

print("import robot_dynamic: start.")

# import the builtins
import os
import math
from pickle import TRUE
import numpy as np

# import the kdl relevant
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
# the following code works. At least some basic knowledge about JointKinematicsWait is necessary,
# from which the iwb_kdl inherits all the properties and methods.
# which are not rewritten here.   

# only be left for referencing. This is now a method in the IWB_KDL class.
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

# hint: differece between JointKinematics and JointKinematicsWait: whether wait for order to 
# subscribe the topic.

####################### test block (removable) ####################
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

###########################################################
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
    

    # # old initialization method, out-of-date method
    # def __init__(self, urdf_model, base_link, end_link, kdl_tree=None):
    #     super(IWB_KDL, self).__init__(urdf_model, base_link, end_link, kdl_tree)
    #     self.robot_base_link = base_link
    #     self.robot_end_link = end_link
    #     self.robot_joint_name = self.get_joint_names()


    '''
        initialize the kdl obj in the robot obj

        arg:
            base_link: the name of the base link
            end_link: the name of the end link
            urdf_filename: the dir of the urdf file
            read_from_server: read the robot structure information
                from the server (1)
        return:
            jacobian: jacobian matrix
    '''
    def __init__(self, base_link, end_link, urdf_filename = None, read_from_server = True):
        # read from server or from the urdf file
        self.read_from_server = read_from_server

        # get the robot structure from urdf file
        urdf_model = self.parse_urdf(urdf_filename)

        # call parent initialization method to build the kdl obj
        try:
            if self.is_ros_online():
                rospy.init_node('pykdl_listener', anonymous=False)
                kdl_jk.JointKinematics.__init__(self, urdf_model, base_link, end_link)
        except Exception as e:
            iwb_ros.robot_base.exception_track(e)
    
        # provide the name of the base and the end link
        self.robot_base_link = base_link
        self.robot_end_link = end_link

    '''
        parse the urdf file to get robot structure

        arg:
            urdf_filename: the dir of the urdf file for parsing,
                not necessary if apply the read from the server
            description_param: the name of the parameter in ros parameter server
                for urdf parsing
        
        return:
            urdf_model: the result of the parse
    '''
    def parse_urdf(self, urdf_filename=None, description_param="robot_description"):
        # reformulate the function in kdl_jk to create a new IWB_KDL obj
        if urdf_filename is None:
            urdf_model = URDF.from_parameter_server(key=description_param)
        else:
            # TODO apply the file reading method in python
            pass
        tree = kdl_tree_from_urdf_model(urdf_model) 
        return urdf_model

    # reserve method for joint setting
    def set_joint_position(self, joint_position):
        # TODO: check format  
        self.__joint_position = joint_position
    
    '''
        check if ros is online

        return:
            ros_online: ros is online (1)
    '''
    def is_ros_online(self):
        # invoke the check method from the ros library
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

    '''
        get the jacobian matrix

        arg:

        return:
            jacobian: jacobian matrix
    '''
    def get_jacobian(self):
        # get current joint states
        robot_joint_state = self.get_joint_position()

        # invoke the method from pykdl to calculate the jacobian matrix
        jacobian = self.jacobian(robot_joint_state)

        return jacobian

    '''
        get the mass matrix

        return:
            mass: mass matrix
    '''
    def get_mass(self):
        robot_joint_state = self.get_joint_position()
        mass = self.inertia(robot_joint_state)
        return mass

    '''
        get the cartisian mass matrix

        return:
            cart_mass: cartisian mass matrix
    '''
    def get_cart_mass(self):
        robot_joint_state = self.get_joint_position()
        cart_mass = self.cart_inertia(robot_joint_state)
        return cart_mass

    '''
        calculate all the results and return them as a tuple

        return:
            (robot_joint_state, jacobian, mass, cart_mass): the tuple of the results
    '''
    def get_dynamics_all(self):

        robot_joint_state = self.get_joint_position()
        jacobian = self.jacobian(robot_joint_state)
        mass = self.inertia(robot_joint_state)
        cart_mass = self.cart_inertia(robot_joint_state)

        return (robot_joint_state, jacobian, mass, cart_mass)
    
    def shutdown(self):
        # reserved shutdown method for the obj
        pass

print("import robot_dynamic: ok.")



