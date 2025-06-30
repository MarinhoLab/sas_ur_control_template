#!/bin/bash
set -e

# Run CoppeliaSim, start simulation, and auto quit
# https://manual.coppeliarobotics.com/en/commandLine.htm
cd "$COPPELIASIM_PATH"
./coppeliaSim.sh \
-s20000 \
"$SAS_UR_CONTROL_TEMPLATE_PATH"/scenes/UR3e_480rev0.ttt &

# Sleep a bit so that Coppeliasim can load the simulation
echo "Giving CoppeliaSim some time to relax."
sleep 60

# Run simulation launch file
source "$HOME"/sas_tutorial_workspace/install/setup.bash
ros2 launch sas_ur_control_template dummy_move_in_coppeliasim_example_cpp_launch.py
