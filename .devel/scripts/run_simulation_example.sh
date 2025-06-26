#!/bin/bash
set -e

# Run CoppeliaSim, start simulation, and auto quit
# https://manual.coppeliarobotics.com/en/commandLine.htm
cd "$COPPELIASIM_PATH"
./coppeliaSim.sh -s -q \
"$HOME"/sas_tutorial_workspace/src/sas_ur_control_template/scenes/sas_UR3_470rev4.ttt &

# Run simulation launch file
source "$HOME"/sas_tutorial_workspace/install/setup.bash
ros2 launch sas_ur_control_template dummy_move_in_coppeliasim_example_cpp_launch.py
