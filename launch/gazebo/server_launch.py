"""Launch the main Gazebo server with autostart and entity management."""
import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    pkg_share_directory = get_package_share_directory('sas_robot_driver_gazebo')
    world_name = "ur3e_world"

    gazebo_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(
                pkg_share_directory,
                'launch',
                'server_launch.py',
            )
        ]),
        launch_arguments={
            'autostart': 'true',
            'set_pose_service_name': f'/world/{world_name}/set_pose',
            'get_pose_topic_name': f'/world/{world_name}/absolute_pose/info',
            "entity_names": f"['frame_x','frame_xd', 'frame_camera']",
            'control_service_name': f'/world/{world_name}/control',
        }.items(),
    )

    return LaunchDescription([
        gazebo_server,
    ])


if __name__ == '__main__':
    generate_launch_description()