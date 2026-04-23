"""Refer to the repository's README.md"""
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='sas_ur_control_template',
            executable='joint_interface_example.py',
            output='screen',
            emulate_tty=True,
            name='sas_ur_control_template_joint_interface_example_py',
            parameters=[{
                "robot_topic_name": "sas_robot_driver_coppeliasim/UR3e"
            }]
        )
    ])
