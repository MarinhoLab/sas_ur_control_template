import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():

    robot_driver_coppeliasim_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('sas_ur_control_template'), 'launch'),
            '/_coppeliasim_launch.py'])
    )

    sas_operator_side_receiver_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('sas_ur_control_template'), 'launch'),
            '/_sas_operator_side_receiver_launch.py'])
    )
    
    sas_patient_side_manager_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('sas_ur_control_template'), 'launch'),
            '/_sas_patient_side_manager_launch.py'])
    )
    
    sas_robot_kinematics_constrained_multiarm_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('sas_ur_control_template'), 'launch'),
            '/_sas_robot_kinematics_constrained_multiarm_launch.py'])
    )

    return LaunchDescription([
        robot_driver_coppeliasim_launch,
        sas_operator_side_receiver_launch,
        sas_patient_side_manager_launch,
        sas_robot_kinematics_constrained_multiarm_launch
    ])
