import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, GroupAction
from launch_ros.actions import Node, SetRemap
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():

    ur3e_compose_launch = GroupAction(
        actions=[

            SetRemap(src='/ur3e_sim/get/joint_states', dst='/ur3e/get/joint_states'),
            SetRemap(src='/ur3e_sim/set/target_joint_positions', dst='/ur3e/set/target_joint_positions'),
            SetRemap(src='/ur3e_sim/get/joint_positions_min', dst='/ur3e/get/joint_positions_min'),
            SetRemap(src='/ur3e_sim/get/joint_positions_max', dst='/ur3e/get/joint_positions_max'),

        ]
    )

    #sas_operator_side_receiver_launch = IncludeLaunchDescription(
    #    PythonLaunchDescriptionSource([os.path.join(
    #        get_package_share_directory('sas_r820_ur3e'), 'launch'),
    #        '/teleoperation/_sas_operator_side_receiver_launch.py'])
    #)
    
    sas_patient_side_manager_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('sas_ur_control_template'), 'launch'),
            '/teleoperation/_sas_patient_side_manager_launch.py'])
    )
    
    sas_robot_kinematics_constrained_multiarm_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('sas_ur_control_template'), 'launch'),
            '/teleoperation/_sas_robot_kinematics_constrained_multiarm_launch.py'])
    )

    return LaunchDescription([
        ur3e_compose_launch,
        #sas_operator_side_receiver_launch,
        sas_patient_side_manager_launch,
        sas_robot_kinematics_constrained_multiarm_launch
    ])
