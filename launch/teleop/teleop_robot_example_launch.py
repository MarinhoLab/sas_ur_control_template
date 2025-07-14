import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, GroupAction
from launch_ros.actions import Node, SetRemap
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():

    real_robot_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('sas_ur_control_template'), 'launch'),
            '/_robot_launch.py'])
    )

    # The target_joint_positions topic of the simulator is remapped to match the same as the robot
    # so that it is controlled via the same signals.
    remapped_robot_driver_coppeliasim_launch = \
        (GroupAction
            (
            actions=
            [

                SetRemap(src='/ur_1_sim/set/target_joint_positions', dst='/ur_1/set/target_joint_positions'),

                IncludeLaunchDescription
                    (
                    PythonLaunchDescriptionSource([os.path.join(
                        get_package_share_directory('sas_ur_control_template'), 'launch'),
                        '/_coppeliasim_launch.py'])
                    ),
            ]
            )
        )

    sas_operator_side_receiver_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('sas_ur_control_template'), 'launch'),
            '/teleop/_sas_operator_side_receiver_launch.py'])
    )
    
    sas_patient_side_manager_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('sas_ur_control_template'), 'launch'),
            '/teleop/_sas_patient_side_manager_launch.py'])
    )
    
    sas_robot_kinematics_constrained_multiarm_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('sas_ur_control_template'), 'launch'),
            '/teleop/_sas_robot_kinematics_constrained_multiarm_launch.py'])
    )

    return LaunchDescription([
        real_robot_launch,
        remapped_robot_driver_coppeliasim_launch,
        sas_operator_side_receiver_launch,
        sas_patient_side_manager_launch,
        sas_robot_kinematics_constrained_multiarm_launch
    ])
