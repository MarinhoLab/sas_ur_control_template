import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, GroupAction
from launch_ros.actions import SetRemap
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

    # The target_joint_positions topic of the simulator is remapped to match the same as the robot
    # so that it is controlled via the same signals.
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
        GroupAction(
            actions=[
                SetRemap(src='/sas_robot_driver_coppeliasim/set/target_joint_positions', dst='/ur_1/set/target_joint_positions'),
                coppeliasim_robot_driver_launch,
            ]
        )
    ])
