"""Refer to the repository's README.md"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration


def generate_launch_description():

    xd_topic_name = LaunchConfiguration('xd_topic_name')

    return LaunchDescription([
        DeclareLaunchArgument(
            'xd_topic_name',
            default_value='/sas_robot_driver_coppeliasim/object/xd'
        ),
        Node(
            package='sas_ur_control_template',
            executable='kinematic_control.py',
            output='screen',
            emulate_tty=True,
            name='sas_ur_control_template_joint_interface_example_py',
            parameters=[{
                "robot_topic_name": "sas_robot_driver_coppeliasim/UR3e",
                "xd_topic_name": xd_topic_name
            }]
        ),
        Node(
            output='screen',
            emulate_tty=True,
            package='sas_datalogger',
            executable='sas_datalogger_node.py',
            name='sas_datalogger'
        ),
    ])
