"""This is a launch file that calls the two launch files and the example script to make the simulated robot
move in CoppeliaSim. For more details, refer to the repository's README.md"""

import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, GroupAction
from launch_ros.actions import Node, SetRemap
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    real_robot_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('sas_ur_control_template'), 'launch'),
            '/_robot_launch.py'])
    )

    # The target_joint_positions topic of the simulator is remapped to match the same as the robot
    # so that it is controlled via the same signals.
    remapped_robot_driver_coppeliasim_launch = \
        (GroupAction
            (
            actions=
            [

                SetRemap(src='/ur1_sim/set/target_joint_positions', dst='/ur1/set/target_joint_positions'),

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
        real_robot_launch,
        remapped_robot_driver_coppeliasim_launch,
        Node(
            package='sas_ur_control_template',
            executable='joint_interface_example.py',
            output='screen',
            emulate_tty=True,
            name='sas_ur_control_template_joint_interface_example_py'
        )
    ])
