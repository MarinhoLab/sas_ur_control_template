from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='sas_patient_side_manager',
            executable='sas_patient_side_manager_node',
            output='screen',
            emulate_tty=True,
            name='sas_patient_side_manager_node',
            parameters=[{
                "thread_sampling_time_sec": 0.001,
                "master_manipulator_label_list": ["m0_0"],
                "object_client_camera_list": ["frame_camera"],
                "object_client_tag_x_list": ["frame_x"],
                "object_client_tag_xd_list": ["frame_xd"],
                "robot_kinematics_interface_prefix_list": ["arm1_kinematics"],
                "robot_gripper_interface_prefix_list": ["robot1/gripper"],
                "gripper_invert_signal_list": [True],
                "use_interpolator_list": [True],
                "interpolator_speed_max_list": [50.],
                "interpolator_speed_min_list": [10.],
                "interpolator_speed_decay_seconds_list": [10.],
                "force_feedback_type_list": ["ExternalMapped"]
            }]
        )

    ])
