#!/bin/bash
set -e

# Run CoppeliaSim, start simulation, and auto quit
# https://manual.coppeliarobotics.com/en/commandLine.htm
cd "$COPPELIASIM_PATH"
./coppeliaSim.sh \
-s0 \
"$HOME"/sas_tutorial_workspace/src/sas_ur_control_template/scenes/UR3e_480rev0.ttt
