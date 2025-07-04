#!/bin/bash
set -e

# Build template workspace
cd "$HOME"/sas_tutorial_workspace
source /opt/ros/jazzy/setup.bash
colcon build
rm -rf build
rm -rf log

# Add sas_tutorial_workspace to bash_env
echo "source $HOME/sas_tutorial_workspace/install/setup.bash"\
>> /etc/bash_env