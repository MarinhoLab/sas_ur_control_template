import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch_ros.actions import SetRemap, Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():

    longboy_robot_compose_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('sas_r820_ur3e'), 'launch'),
            '/longboy_robot_compose_launch.py'])
    )

    longboy_simulation_compose_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('sas_r820_ur3e'), 'launch'),
            '/longboy_simulation_compose_launch.py'])
    )

    sas_operator_side_receiver_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('sas_r820_ur3e'), 'launch'),
            '/teleop/_sas_operator_side_receiver_launch.py'])
    )
    
    sas_patient_side_manager_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('sas_r820_ur3e'), 'launch'),
            '/teleop/_sas_patient_side_manager_launch.py'])
    )
    
    sas_robot_kinematics_constrained_multiarm_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('sas_r820_ur3e'), 'launch'),
            '/teleop/_sas_robot_kinematics_constrained_multiarm_launch.py'])
    )

    return LaunchDescription([
        longboy_robot_compose_launch,
        longboy_simulation_compose_launch,
        sas_operator_side_receiver_launch,
        sas_patient_side_manager_launch,
        sas_robot_kinematics_constrained_multiarm_launch,
        Node(
            package='topic_tools',
            executable='relay',
            name='longboy_relay',
            parameters=[{
                "input_topic": f"longboy/set/target_joint_positions",
                "output_topic": f"longboy_sim/set/target_joint_positions",
            }]
        ),
    ])
