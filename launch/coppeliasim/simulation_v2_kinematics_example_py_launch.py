"""Refer to the repository's README.md"""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    xd_topic_name = LaunchConfiguration('xd_topic_name')
    config_file = LaunchConfiguration('config_file')

    return LaunchDescription([
        DeclareLaunchArgument(
            'xd_topic_name',
            default_value='/sas_robot_driver_coppeliasim/object/xd'
        ),
        DeclareLaunchArgument(
            'config_file',
            default_value=os.path.join(get_package_share_directory('sas_ur_control_template'), 'config', 'config.yaml')
        ),
        Node(
            package='sas_ur_control_template',
            executable='kinematic_control.py',
            output='screen',
            emulate_tty=True,
            name='sas_ur_control_template_kinematics_example_py',
            # `xd_topic_name` is kept as a launch argument so the CoppeliaSim
            # scene's `xd` dummy can be overridden without editing the config.
            parameters=[config_file, {'xd_topic_name': xd_topic_name}]
        )
    ])
