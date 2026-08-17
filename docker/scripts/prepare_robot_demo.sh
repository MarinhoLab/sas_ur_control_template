#!/bin/bash
set -e

# Set FASTRTPS profile to run over UDP when net=host.
export FASTRTPS_DEFAULT_PROFILES_FILE=/root/sas_tutorial_workspace/src/sas_ur_control_template/docker/scripts/fastrtps_profile.xml

# Show countdown
cd /root/sas_tutorial_workspace/src/sas_ur_control_template/docker/scripts
./countdown.sh 10
