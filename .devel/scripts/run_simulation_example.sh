#!/bin/bash
set -e

# Run simulation launch file
source "$HOME"/sas_tutorial_workspace/install/setup.bash
ros2 launch sas_ur_control_template dummy_move_in_coppeliasim_example_cpp_launch.py
