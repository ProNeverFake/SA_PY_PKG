#!/bin/bash
# source the ros1
source /opt/ros/noetic/setup.bash
# source this workspace 
cd ~/sa_ws
catkin_make
source ~/sa_ws/devel/setup.bash

# run the launch file
rosrun iwb_state_publisher iwb_state_publisher_v2.py




