"""Launch the ur3e robot driver server for Gazebo simulation."""
import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory

_REQUIRED_ENV_VARS = ['GAZEBO_ROBOT_TOPIC_NAME']


def generate_launch_description():
    for var in _REQUIRED_ENV_VARS:
        if var not in os.environ or not os.environ[var]:
            print(f"ERROR: Environment variable '{var}' is not set. "
                  f"Please set it in docker/.env or export it before launching.", file=sys.stderr)
            sys.exit(1)
            
    pkg_share_directory = get_package_share_directory('sas_robot_driver_gazebo')
    world_name = "ur3e_world"
    robot_name = "ur3e"

    ur3e_robot_driver = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(
                pkg_share_directory,
                'launch',
                'robot_driver_server_launch.py',
            )
        ]),
        launch_arguments={
            'joint_positions_topic_prefix': '/model/ur3e/joint/',
            'joint_states_topic': f'/world/{world_name}/model/{robot_name}/model/ur3e_position_controller/model/ur3e/joint_state',
            "joint_names": "['shoulder_pan_joint','shoulder_lift_joint','elbow_joint','wrist_1_joint','wrist_2_joint','wrist_3_joint']",
            'robot_name': f"[{os.environ['GAZEBO_ROBOT_TOPIC_NAME']}]",
        }.items(),
    )

    return LaunchDescription([
        ur3e_robot_driver
    ])


if __name__ == '__main__':
    generate_launch_description()
