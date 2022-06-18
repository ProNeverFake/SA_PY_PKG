#!/bin/bash
# source the ros1
source /opt/ros/noetic/setup.bash
# source this workspace 
cd ~/sa_ws
catkin_make
source ~/sa_ws/devel/setup.bash

# run the launch file
# roslaunch robot_model view_robot.launch

