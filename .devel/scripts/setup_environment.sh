#!/bin/bash
set -e

# Build template workspace
cd "$HOME"/sas_tutorial_workspace
source /opt/ros/jazzy/setup.bash
colcon build

# Add sas_tutorial_workspace to bash
echo "source $HOME/sas_tutorial_workspace/install/setup.bash"\
>> ~/.bashrc

# Setup ROS 2 package path
SAS_UR_CONTROL_TEMPLATE_PATH="${HOME}/sas_tutorial_workspace/src/sas_ur_control_template"

echo "export SAS_UR_CONTROL_TEMPLATE_PATH='${SAS_UR_CONTROL_TEMPLATE_PATH}'"\
>> ~/.bashrc

# Setup example aliases
UR3E_BASIC_EXAMPLE="${SAS_UR_CONTROL_TEMPLATE_PATH}/.devel/scripts/run_simulation_example.sh"
chmod +x "${UR3E_BASIC_EXAMPLE}"

echo "alias ur3e_basic_example='${UR3E_BASIC_EXAMPLE}'"\
>> ~/.bashrc





