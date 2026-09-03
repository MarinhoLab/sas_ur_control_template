import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    config_file = LaunchConfiguration('config_file')

    robot_example_py_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('sas_ur_control_template'), 'launch'),
            '/robot_example_py_launch.py']),
        launch_arguments=[('config_file', config_file)]
    )

    # The simulated robot's target_joint_positions topic is relayed to the
    # real robot's topic so that the example (which drives `ur_1`) controls the
    # simulator via the same signals.
    coppeliasim_robot_driver_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('sas_robot_driver_coppeliasim'), 'launch'),
            '/robot_launch.py']),
        launch_arguments=[
            ('name', 'sas_robot_driver_coppeliasim'),
            ('config_file', config_file),
        ]
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'config_file',
            default_value=os.path.join(get_package_share_directory('sas_ur_control_template'), 'config', 'config.yaml')
        ),
        robot_example_py_launch,
        coppeliasim_robot_driver_launch,
        Node(
            package='topic_tools',
            executable='relay_node',
            name='ur_1_relay',
            parameters=[config_file]
        ),
    ])
