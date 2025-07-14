from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration


def generate_launch_description():

    return LaunchDescription([
        Node(
            package='sas_robot_kinematics_constrained_multiarm',
            executable='sas_robot_kinematics_constrained_multiarm_node',
            output='screen',
            emulate_tty=True,
            name='sas_robot_kinematics_constrained_multiarm',
            parameters=[{
                        "thread_sampling_time_sec": 0.002,
                        "n": 40.0,
                        "n_d": 6.0,
                        "damping": 0.01,
                        "damping_secondary": 0.0000001,
                        "damping_secondary_labels": ["2_8"],
                        "alpha": 0.99999,
                        "alpha_secondary": 0.99,
                        "enable_initial_angle_limit": True,
                        "master_device_labels": ["m0_0"],
                        "robot_driver_interface_node_prefixes": ["arm1"],
                        "robot_kinematics_provider_prefixes": ["arm1_kinematics"],
                        "vrep_port": 23000,
                        "vrep_ip": "127.0.0.1",
                        "robot_parameter_file_paths": [
                        [os.path.join(get_package_share_directory('sas_ur_control_template'), 'robots'),'/ur3e.json']
                        ]
                    }]
        )

    ])
