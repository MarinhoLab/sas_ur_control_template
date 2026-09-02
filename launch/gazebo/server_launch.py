"""Launch the main Gazebo server with autostart and entity management."""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    config_file = LaunchConfiguration('config_file')

    # The world name and the object/simulator server node names are set in
    # config/config.yaml (blocks `sas_object_server_gazebo_node` and
    # `sas_simulator_server_gazebo_node`).
    object_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(
                get_package_share_directory('sas_robot_driver_gazebo'),
                'launch',
                'object_server_launch.py',
            )
        ]),
        launch_arguments=[
            ('name', 'sas_object_server_gazebo_node'),
            ('config_file', config_file),
        ],
    )

    simulator_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(
                get_package_share_directory('sas_robot_driver_gazebo'),
                'launch',
                'simulator_server_launch.py',
            )
        ]),
        launch_arguments=[
            ('name', 'sas_simulator_server_gazebo_node'),
            ('config_file', config_file),
        ],
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'config_file',
            default_value=os.path.join(get_package_share_directory('sas_ur_control_template'), 'config', 'config.yaml')
        ),
        simulator_server,
        object_server,
    ])


if __name__ == '__main__':
    generate_launch_description()