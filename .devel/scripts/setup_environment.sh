#!/bin/bash
set -e

# Source ROS and build workspace
source /opt/ros/jazzy/setup.bash
cd "$HOME"/sas_tutorial_workspace
colcon build
source "$HOME"/sas_tutorial_workspace/install/setup.bash

