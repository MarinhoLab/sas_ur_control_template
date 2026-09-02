"""Launch the ur3e robot driver server for Gazebo simulation."""
import os
import sys

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    config_file = LaunchConfiguration('config_file')

    # The bridge node name is `ur3e_1` (see config/config.yaml). The
    # `GAZEBO_ROBOT_TOPIC_NAME` environment variable still selects the topic
    # prefix the bridge publishes under.
    if 'GAZEBO_ROBOT_TOPIC_NAME' not in os.environ or not os.environ['GAZEBO_ROBOT_TOPIC_NAME']:
        print("ERROR: Environment variable 'GAZEBO_ROBOT_TOPIC_NAME' is not set. "
              "Please set it in docker/.env or export it before launching.", file=sys.stderr)
        sys.exit(1)

    ur3e_robot_driver = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(
                get_package_share_directory('sas_robot_driver_gazebo'),
                'launch',
                'robot_driver_server_launch.py',
            )
        ]),
        launch_arguments=[
            ('name', 'ur3e_1'),
            ('config_file', config_file),
        ],
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'config_file',
            default_value=os.path.join(get_package_share_directory('sas_ur_control_template'), 'config', 'config.yaml')
        ),
        ur3e_robot_driver
    ])


if __name__ == '__main__':
    generate_launch_description()
