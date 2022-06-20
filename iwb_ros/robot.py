#!/usr/bin/env python

# the python module for robot initialization

print('import iwb_ros.robot: start.')

# import multithread method
from asyncio import FastChildWatcher

# import builtin pkg
import os

# import ros relevant
import iwb_ros
import rosnode
import rospy
import roslib
# roslib.load_manifest("pykdl_utils")

# import the pkg

import iwb_ros.visualization
import iwb_ros.fake_controller
import iwb_ros.robot_dynamic

# import multithread solution
import threading
import subprocess
import time

# test, import motionplanning later
# import iwb_ros.motionplanning

################################## MACRO ################################
# workspace directory
ROS_WORKSPACE = '~/sa_ws'
PYTHON_PKG_DIR = '~/my_pkg'
SCRIPT_DIR = os.path.dirname(iwb_ros.__file__) + '/script'

SCRIPT_LIST = {"ros_setup": './ros_setup.sh',
                "visualization": './robot_visualization_launch.sh',
                "fake_controller":'./fake_controller.sh',
                "ros_shutdown": './ros_shutdown.sh',
                "roscore_launch": './roscore_launch.sh',
                "motion_visualization": './moveit_script.sh',
                "motion_planner": './moveit_planner.sh'
                }
PROCESS_HANDLE = {"visualization": '',
                "fake_controller": '',
                }
USE_SCRIPT = {"fake_controller": False,
                "motion_controller": True,}

# for those nodes who may not launch from launch file, a register must be done in main thread
ROS_NODE_NAME ={"fake_controller": 'iwb_fake_controller',
                }


###############################################################################

# source the ros konfiguration (run the bash script)
# command = 'bash ' + ros_workspace + '/ros_setup.sh'
# print(command)
# print(os.system(command))


class IWB_Robot:
    # TODO: Set necessary basic attrs for using existing luanch files or so.
    __ros_workspace = ROS_WORKSPACE
    python_pkg_dir = PYTHON_PKG_DIR
    # flag for launch method
    __use_script = USE_SCRIPT
    __ros_node_name = ROS_NODE_NAME
    __script_dir = SCRIPT_DIR
    __script_list = SCRIPT_LIST
    __process_handle = PROCESS_HANDLE
    __controller_name = "none"
    # private attr for kdl
    UNFINISHED
    iwb_ros.robot_dynamic.IWB_KDL


    # def get_kdl_urdf_model(self):
    #     return self.__kdl_urdf_model

    def get_process_handle(self, process_handle_name):
        return self.__process_handle[process_handle_name]

    def set_process_handle(self, process_handle_name, process_handle):
        self.__process_handle[process_handle_name] = process_handle

    def get_script_dir(self):
        return self.__script_dir

    ############### here is not tested #################################
    def get_script_name(self, launch_name):
        return self.__script_list[launch_name]

    def get_controller_name(self):
        return self.__controller_name
    
    def set_controller_name(self, controller_name):
        self.__controller_name = controller_name

    def get_ros_workspace(self):
        return self.__ros_workspace

    def get_use_script(self, launch_name):
        return self.__use_script[launch_name]

    def get_ros_node_name(self):
        return self.__ros_node_name

    def __init__(self):
        # kill possible old roscore
        self.script_launch("ros_shutdown")
        time.sleep(2)
        # start the roscore
        try:
            self.script_launch("roscore_launch")
            print("roscore launch: ok.")
        except:
            print("!!!Fatal: IWB_Robot.__init__: roscore launch failed.!!!")

        time.sleep(2)

        ######################### raw code (the same as the function)
        # cwd = os.getcwd()
        # print(SCRIPT_DIR)
        # os.chdir(SCRIPT_DIR)
        # roscore = subprocess.Popen("./roscore_launch.sh",shell=True, cwd=SCRIPT_DIR)
        # print("test: roscore here")
        # os.chdir(cwd)

        # time.sleep(2)
        ###############################################################


        # alternative: do initialize when call the corresp. function
        ########################################################
        # # register the node in main thread
        # node_name_list = self.get_ros_node_name()
        # for node_name in node_name_list:
        #     rospy.init_node(node_name)
        ########################################################

        # set the python_pkg_dir, which may be in need within rosnode
        rospy.set_param('python_pkg_dir', self.python_pkg_dir)

        # read robot param

        

    
    def send_joint_position(self, joint_position):
        
        controller_name = self.get_controller_name()

        # decide which set function to call, depending on the controller
        if controller_name == "fake_controller":
            iwb_ros.fake_controller.set_fake_controller(joint_position)
        

    def fake_controller(self):
        
        # change the name of controller
        self.set_controller_name("fake_controller")
        use_script = self.get_use_script("fake_controller")

        # if self.get_fake_controller_use_script():
        if use_script:
            try:
                self.script_launch("fake_controller")
                print("launch fake_controller: ok.")
            except:
                print("!!!Fatal: fake_controller script launch: failed.!!!")
        else:
            # register the node
            rospy.init_node(self.get_ros_node_name()["fake_controller"])
            # TODO: use a general function to launch controller
            
            thread = threading.Thread(target=iwb_ros.fake_controller.start_fake_controller)
            thread.setDaemon(True)
            thread.start()
        

    def simulator(self):
        # FUTURE: use simulator.
        pass
    
    def visualization(self):
        try:
            self.script_launch("visualization")
            print("launch visualization: ok.")
        except:
            print("!!!Fatal: launch visualization: failed.!!!")

        rospy.sleep(5)
        # iwb_ros.visualization.visualize(self)

    
    def motion_visualization(self):
        # start moveit configuration and visualization in rviz
        self.script_launch("motion_visualization")
        # to ensure the process launching has finished
        rospy.sleep(5)
       
    def motion_planner(self):
        # script start
        self.script_launch("motion_planner")
    
    def motion_plan_to(self):
        
        pass

    def start_robot_dynamic(self):
        # TODO: "the structure of the program is quite a mess in my mind"
        

        pass


    def shutdown_all(self):
        # kill all subprocess
        # TODO
        # this function is used to shutdown all the nodes
        try:
            rosnode.kill_nodes(rosnode.get_node_names())
        except:
            print("!Warning: shutdown_all: cannot kill the nodes.!")
        pass
        
        try: 
            self.script_launch("ros_shutdown")
            print("Ros shutdown: ok.")
        except:
            print("!!!Fatal: shutdown roscore: Failed.!!!")


    def script_launch(self, launch_name):
        # launch name key name is the same as process handle key name
        process_handle_name = launch_name
        # get current cd
        cwd = os.getcwd()
        # change cd to script dir
        os.chdir(self.get_script_dir())
        # use method to get the corresponding script name
        script_name = self.get_script_name(launch_name)
        # run in subprocess
        process_handle = subprocess.Popen(script_name,shell=True, cwd=self.get_script_dir())
        self.set_process_handle(process_handle_name, process_handle)

        os.chdir(cwd)
        # rospy.sleep(5)
        # TODO: alternative check if launch is finished
        # return the process id for further monitoring
    


print('import iwb_ros.robot: ok.')




