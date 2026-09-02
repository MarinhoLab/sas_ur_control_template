import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    config_file = LaunchConfiguration('config_file')

    return LaunchDescription([
        DeclareLaunchArgument(
            'config_file',
            default_value=os.path.join(get_package_share_directory('sas_ur_control_template'), 'config', 'config.yaml')
        ),
        Node(
            package='sas_robot_kinematics_constrained_multiarm',
            executable='sas_robot_kinematics_constrained_multiarm_node',
            output='screen',
            emulate_tty=True,
            name='sas_robot_kinematics_constrained_multiarm',
            parameters=[config_file]
        )

    ])
