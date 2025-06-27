#!/bin/bash
set -e

# Build template workspace
cd "$HOME"/sas_tutorial_workspace
colcon build

# Add sas_tutorial_workspace to bash
echo "source $HOME/sas_tutorial_workspace/install/setup.bash" >> ~/.bashrc

# Setup example path
echo "export SAS_UR_CONTROL_TEMPLATE_PATH='${HOME}/sas_tutorial_workspace/src/sas_ur_control_template'">> ~/.bashrc

