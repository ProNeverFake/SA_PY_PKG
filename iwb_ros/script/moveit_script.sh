#!/bin/bash

### ATTENTION: shebang in the first line, otherwise source command will not be recognized.

# ros env setup
. ros_setup.sh

# run the launch file
roslaunch robot_model_moveit_config demo.launch

