from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration


def generate_launch_description():

    return LaunchDescription([
        Node(
            package='sas_patient_side_manager',
            executable='sas_patient_side_manager_node',
            output='screen',
            emulate_tty=True,
            name='sas_patient_side_manager_node',
            parameters=[{
                "vrep_ip": "127.0.0.1",
                "vrep_port": 19997,
                "thread_sampling_time_nsec": 8000000,

                "master_manipulator_label_list": ["m0_0"],
                "vrep_camera_list": ["Camera"],
                "vrep_x_list": ["x1"],
                "vrep_xd_list": ["xd1"],
                "robot_kinematics_interface_prefix_list": ["/robot_1_kinematics"],
                "robot_gripper_interface_prefix_list": ["/robot1/gripper"],
                "gripper_invert_signal_list": [True],
                "use_interpolator_list": [True],
                "interpolator_speed_max_list": [50.],
                "interpolator_speed_min_list": [10.],
                "interpolator_speed_decay_seconds_list": [10.],
                "force_feedback_type_list": ["None"],
                "leader_to_follower_quaternions": [[0.,0.,0.,0.]]
            }]
        )

    ])
