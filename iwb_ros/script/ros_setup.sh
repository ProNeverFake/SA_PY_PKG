#!/bin/bash
# get env var.
. iwb_ros_setting.sh
# source the ros1
source /opt/ros/noetic/setup.bash
# source this workspace 
cd "$path"
catkin_make
source "$source_path"


