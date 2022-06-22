print('initialize: start.')

import os

# source from the python script: failed
# alternative: add the source command to the 
# os.system("cd")
# os.system(". /opt/ros/noetic/local_setup.bash")

import sys
# TODO: need to set the pypath to enable find_pkg
sys.path.append("/usr/lib/python3/dist-packages")
sys.path.append("/opt/ros/noetic/lib/python3/dist-packages")
sys.path.append("/usr/local/lib/python3.8/dist-packages")
sys.path.append("/usr/local/lib/python3.8/dist-packages/pykdl_utils")
sys.path.append("")


import rospy
import roslaunch
import iwb_ros.robot


print('initialize: ok.')


# TODO: how to import KDL?