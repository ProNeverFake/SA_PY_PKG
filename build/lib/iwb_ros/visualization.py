#!/usr/bin/env python

print('import iwb_ros.visualization: start.')
# Ref: http://wiki.ros.org/roslaunch/API%20Usage
import os
# used for: test: run the ros bash script
import subprocess
import sys

import roslaunch
import rospy
import rosnode


# initialize the node and the launch process
# rospy.init_node('rviz_mapping', anonymous=True)



def visualize(robot):
    try:
        robot.script_launch("visualization")
        print("visualization: ok")
    except:
        print("!!!Fatal: visualize: Failed.!!!")
    # TODO: use rosnode.is_master_online instead as a flag for finishing the launch work
    rospy.sleep(5)
    

    ################################## raw code
    # cwd = os.getcwd()
    # print(SCRIPT_DIR)
    # os.chdir(SCRIPT_DIR)
    # # process = subprocess.Popen("./rviz_script.sh",shell=True, cwd=SCRIPT_LOCATION, stdout=subprocess.PIPE)
    # # output ignored
    # process = subprocess.Popen("./robot_visualization_launch.sh",shell=True, cwd=SCRIPT_DIR)

    # # wait for 5 sec to make sure the master is online
    # # otherwise: suffer from "unable to communicate with ros master"
    # # TODO: use rosnode.is_master_online instead as a flag for finishing the launch work
    # rospy.sleep(5)
    # # process = subprocess.Popen("./ros_setup.sh",shell=True, cwd=SCRIPT_LOCATION, stdout=subprocess.PIPE)
    # # print("process 2 started.")
    # # std_out = process.communicate()[0]
    # os.chdir(cwd)

    # return the handle of the subprocess for further processing
    # return process



    # try:
        
    #     os.system("bash /opt/ros/noetic/setup.bash")
    #     print("test: source the setup file manually")
    # except:
    #     pass
    # run the launch file 'view_robot.launch'

    # # run launch file with bash script
    # command = 'bash ' + ros_workspace + '/rviz_script.sh'
    # print(command)
    # print(os.system(command))

    ######################################## following: roslaunch pymodule attempt

    # # following the incorrect example code.
    # # launch obj that contains the dir info
    # uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
    # roslaunch.configure_logging(uuid)

    # launch = roslaunch.parent.ROSLaunchParent(
    #     uuid, 
    #     ["/home/blackbird/sa_ws/src/robot_model/launch/view_robot.launch"]
    #     )
    # launch.start()
    # rospy.loginfo("started")

# rospy.sleep(3)
# # 3 seconds later
# launch.shutdown()

print('import iwb_ros.visualization: ok.')
