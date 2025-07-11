"""This is a launch file that calls the two launch files and the example script to make the simulated robot
move in CoppeliaSim. For more details, refer to the repository's README.md"""

import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, GroupAction
from launch_ros.actions import Node, SetRemap
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    robot_example_py_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('sas_ur_control_template'), 'launch'),
            '/robot_example_py_launch.py'])
    )

    # The target_joint_positions topic of the simulator is remapped to match the same as the robot
    # so that it is controlled via the same signals.
    remapped_robot_driver_coppeliasim_launch = \
        (GroupAction
            (
            actions=
            [

                SetRemap(src='/ur_1_sim/set/target_joint_positions', dst='/ur_1/set/target_joint_positions'),

                IncludeLaunchDescription
                    (
                    PythonLaunchDescriptionSource([os.path.join(
                        get_package_share_directory('sas_ur_control_template'), 'launch'),
                        '/_coppeliasim_launch.py'])
                    ),
            ]
            )
        )

    return LaunchDescription([
        robot_example_py_launch,
        remapped_robot_driver_coppeliasim_launch
    ])
