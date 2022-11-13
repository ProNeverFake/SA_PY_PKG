#!/usr/bin/env python
'''
    This is the main python module for robot object initialization
'''

# the python module for robot initialization
print('import iwb_ros.robot: start...')

# set the operating environment
import iwb_ros.setting

# import builtin pkg
import os

# import ros relevant
import iwb_ros
import rosnode
import rospy

# # this is the import method from old-version ros
# import roslib
# roslib.load_manifest("pykdl_utils")

# import the iwb_ros pkg
import iwb_ros.robot_base
import iwb_ros.visualization
import iwb_ros.fake_controller
import iwb_ros.robot_dynamic

# import the multithread solution
import threading
import subprocess
import time
import signal

# motionplanning module, unfinished, for further extensions
# import iwb_ros.motionplanning

################################## MACRO ################################
# workspace directory
ROS_WORKSPACE = '~/sa_ws'
PYTHON_PKG_DIR = '~/my_pkg'
SCRIPT_DIR = iwb_ros.__path__[0] + '/script'
print("SCRIPT_DIR = ", SCRIPT_DIR)

# script list used to launch the coresponding ros function from bash script
SCRIPT_LIST = {"ros_setup": './ros_setup.sh',
                "visualization": './robot_visualization_launch.sh',
                "fake_controller":'./fake_controller.sh',
                "iwb_state_publisher": './iwb_state_publisher.sh',
                "ros_shutdown": './ros_shutdown.sh',
                "roscore_launch": './roscore_launch.sh',
                "motion_visualization": './moveit_script.sh',
                "motion_planner": './moveit_planner.sh'
                }
# process handle for multi-thread management 
PROCESS_HANDLE = {}
# whether use the bash script or use python code to launch the corresponding node
USE_SCRIPT = {"fake_controller": True,
                "motion_controller": True,}

''' important:
    for those nodes who may not get launched from launch file,
    a registration must be done in the main thread in adcance!!! 
'''
ROS_NODE_NAME ={"fake_controller": 'iwb_fake_controller',
                }

# FAKE_CONTROLLER_USE_EXAMPLE = True
BASE_LINK = "base_link"
END_LINK = "link_6_x"


# make all the scripts executable (manually chmod + x)
# script_to_execute = os.listdir(SCRIPT_DIR)
# print("scripts' name: ", script_to_execute)
# for script in script_to_execute:
#     script_path = SCRIPT_DIR + '/' + script
#     subprocess.Popen(['chmod', '+x', script_path])
    # st = os.stat(script_path)
    # os.chmod(script_path, st.st_mode | stat.S_IEXEC | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


###############################################################################

class IWB_Robot:
    # TODO: Set necessary basic attrs for using existing luanch files or so.
    _ros_workspace = ROS_WORKSPACE
    python_pkg_dir = PYTHON_PKG_DIR
    # flag for launch method
    _use_script = USE_SCRIPT
    _ros_node_name = ROS_NODE_NAME
    _script_dir = SCRIPT_DIR
    _script_list = SCRIPT_LIST
    _process_handle = PROCESS_HANDLE
    _controller_name = "none"

    base_link = BASE_LINK
    end_link = END_LINK
    

    # fake_controller_use_example = FAKE_CONTROLLER_USE_EXAMPLE
    # KDL obj
    iwb_kdl = ""

    # def get_kdl_urdf_model(self):
    #     return self._kdl_urdf_model

    def get_process_handle(self, process_handle_name):
        return self._process_handle[process_handle_name]

    def set_process_handle(self, process_handle_name, process_handle):
        self._process_handle[process_handle_name] = process_handle
    
    def kill_process_handle(self, process_handle_name = None):

        handle_dict = self._process_handle
        if len(handle_dict) == 0:
            # no handle exists
            print("!Warning: kill_process_handle: no handle exists.!")
            return None
        if process_handle_name == None:
            # then kill all handles
            if not len(handle_dict) == 0:
                (handle_name, handle) = handle_dict.popitem()
                os.killpg(os.getpgid(handle.pid), signal.SIGTERM)
        else:
            handle = handle_dict[process_handle_name]
            os.killpg(os.getpgid(handle.pid), signal.SIGTERM)

    def get_script_dir(self):
        return self._script_dir

    def get_script_name(self, launch_name):
        return self._script_list[launch_name]

    def get_controller_name(self):
        return self._controller_name
    
    def set_controller_name(self, controller_name):
        self._controller_name = controller_name

    def get_ros_workspace(self):
        return self._ros_workspace

    def get_use_script(self, launch_name):
        return self._use_script[launch_name]

    def get_ros_node_name(self):
        return self._ros_node_name

    def __init__(self):
        # kill possible old roscore
        self.script_launch("ros_shutdown")
        time.sleep(2)
        # # test
        # self.script_launch("roscore_launch")
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

        # set the python_pkg_dir, which may be needed within rosnode
        rospy.set_param('python_pkg_dir', self.python_pkg_dir)

        # read robot param

    def robot_send_joint_position(self, joint_position):
        
        controller_name = self.get_controller_name()

        # decide which set function to call, depending on the controller
        if controller_name == "fake_controller":
            iwb_ros.fake_controller.set_fake_controller(joint_position)
        
    def fake_controller(self, use_example = False):
        '''
        start a fake controller

        args:
            use_example: flag, whether apply the example code (making the 6th link rotate)
                to the controller. Only allowed to use when run from script, otherwise the
                main process would be blocked. (to be recode)
        '''
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
            
            # here only call the function handle!!!! no klamma
            thread = threading.Thread(target=iwb_ros.fake_controller.start_fake_controller, args=(use_example))
            thread.setDaemon(True)
            thread.start()
        # run a example if asked
        if use_example:
            iwb_ros.fake_controller.run_test_example()

    # another fake controller
    def iwb_state_publisher_start(self):
        '''
        a pure ros node to publish joint states.
        '''
        try:
            self.script_launch("iwb_state_publisher")
        except Exception as e:
            iwb_ros.robot_base.exception_track(e)

        rospy.sleep(2)


    def iwb_kdl_start(self):
        '''
        create the iwb_kdl instance as a attr of the main robot class
        '''
        self.iwb_kdl = iwb_ros.robot_dynamic.IWB_KDL(self.base_link, self.end_link)

    # get all the current dynamic attribute of the robot in a tuple
    # in order of joint states, jacobian, mass matrix, cartesian mass matrix
    def iwb_kdl_get_dynamics_all(self):
        '''
        get all the kinematic and dynamic features of the robot.

        return:
            result: a tuple consists of three elements, jacobian matrix, mass matrix and cartesian mass matrix.

        '''
        try:
            result = self.iwb_kdl.get_dynamics_all()
            return result
        except Exception as e:
            iwb_ros.robot_base.exception_track(e)
            self.iwb_kdl.shutdown()

    def simulator(self):
        # TODO: This is prepared for gazebo or other simulators
        # with physical engines to substitute the visualization
        # in riviz and to provide simulation functions.
        pass
    
    def visualization(self):
        '''
            Open rviz to visualize the robot. The robot params in urdf file get stored in 
                ros param "robot_description" in this step.
        '''
        # now the visualization module is abandoned
        try:
            self.script_launch("visualization")
            print("launch visualization: ok.")
        except:
            print("!!!Fatal: launch visualization: failed.!!!")

        # pause the process for a complete launch
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
        # send robot motion order
        pass

    def shutdown_all(self):
        '''
        kill all subprocess and shutdown roscore/rosmaster
        should be called in the end by default (TODO)
        '''
        self.kill_process_handle()
        # this function is used to shutdown all the nodes
        try:
            rosnode.kill_nodes(rosnode.get_node_names())
        except:
            print("!Warning: shutdown_all: cannot kill the nodes.!")
        pass
        
        # shutdown the ros service
        try: 
            self.script_launch("ros_shutdown")
            print("Ros shutdown: ok.")
        except:
            print("!!!Fatal: shutdown roscore: Failed.!!!")
            
        for key in self._process_handle:
            pro = self._process_handle[key]
            os.killpg(os.getpgid(pro.pid), signal.SIGTERM)



    # run a provided script
    def script_launch(self, launch_name):
        '''
        general method to run a corresponding script, which includes the bash commands to
        source the ros installation and execute corresponding launch file.
        the handle of the launched process should be saved into the dictionary

        args: 
            launch_name: the name of the functionality to be launched, according to the 
            dictionary: robot.script_list

        '''

        # launch name key name is the same as process handle key name
        process_handle_name = launch_name
        # get current cd
        cwd = os.getcwd()
        # change cd to script dir
        # os.chdir(self.get_script_dir())
        # use method to get the corresponding script name
        script_name = self.get_script_name(launch_name)
        # run in subprocess
        # process_handle = subprocess.call([script_name], cwd = self.get_script_dir())
        process_handle = subprocess.Popen(script_name,shell=True, cwd=self.get_script_dir())  
        self.set_process_handle(process_handle_name, process_handle)

        os.chdir(cwd)
        # rospy.sleep(5)
        # TODO: alternative check if launch is finished
        # return the process id for further monitoring
    
print('import iwb_ros.robot: ok.')




