#!/bin/bash
set -e

# Source ROS and build workspace
source /opt/ros/jazzy/setup.bash
cd "$HOME"/sas_tutorial_workspace
colcon build
source "$HOME"/sas_tutorial_workspace/install/setup.bash

# Adding vnc information
## https://www.baeldung.com/linux/docker-container-gui-applications
apt-get update && apt-get install -qqy x11-apps x11vnc xvfb
mkdir ~/.vnc
x11vnc -storepasswd 1234 ~/.vnc/passwd