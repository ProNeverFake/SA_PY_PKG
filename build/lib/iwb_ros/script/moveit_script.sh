#!/bin/bash

### ATTENTION: shebang in the first line, otherwise source command will not be recognized.

# source the ros1
source /opt/ros/noetic/setup.bash
# source this workspace 
cd ~/sa_ws
catkin_make
source ~/sa_ws/devel/setup.bash

# run the launch file
roslaunch robot_model_moveit_config demo.launch

