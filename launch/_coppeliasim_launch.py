from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    joint_names = [
        "/UR3e/joint",
        "/UR3e/link/joint",
        "/UR3e/link/joint/link/joint",
        "/UR3e/link/joint/link/joint/link/joint",
        "/UR3e/link/joint/link/joint/link/joint/link/joint",
        "/UR3e/link/joint/link/joint/link/joint/link/joint/link/joint",
    ]

    coppeliasim_ip = LaunchConfiguration('coppeliasim_ip')
    coppeliasim_timeout = LaunchConfiguration('coppeliasim_timeout')

    return LaunchDescription([
        DeclareLaunchArgument(
            'coppeliasim_ip',
            default_value='127.0.0.1'
        ),
        DeclareLaunchArgument(
             'coppeliasim_timeout',
              default_value='1000'
        ),
        Node(
            package='sas_robot_driver_coppeliasim',
            executable='sas_robot_driver_coppeliasim_node',
            output='screen',
            emulate_tty=True,
            name='ur_1_sim',
            parameters=[{
                "timeout": coppeliasim_timeout,
                "robot_joint_names": joint_names,
                "ip": coppeliasim_ip,
                "port": 23000,
                "joint_limits_min": [-360.0, -360.0, -360.0, -360.0, -360.0, -720.0],  # The last joint has no limit
                "joint_limits_max": [360.0, 360.0, 360.0, 360.0, 360.0, 720.0],  # The last joint has no limit
                "thread_sampling_time_sec": 0.001
            }]
        )

    ])
