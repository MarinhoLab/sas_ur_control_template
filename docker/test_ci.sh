#!/bin/bash
set -e

cd /root/sas_ur_control_template_ci
source /opt/ros/jazzy/setup.bash

echo "=== Building package ==="
colcon build
echo "=== Build complete ==="

source install/setup.bash

echo "=== Package available ==="
ros2 pkg list | grep sas_ur_control_template

echo "=== Checking executables ==="
PKG_LIB=$(ros2 pkg prefix sas_ur_control_template)/lib/sas_ur_control_template
test -x "$PKG_LIB/joint_interface_example.py" && echo "Python node OK"
test -x "$PKG_LIB/joint_interface_example_cpp" && echo "C++ node OK"

echo "=== Launch file syntax ==="
for launch in $(ros2 pkg prefix sas_ur_control_template --share)/launch/*.py; do
    echo "Checking: $launch"
    python3 -c "import ast; ast.parse(open('$launch').read())" && echo "OK"
done

echo "=== All tests passed ==="