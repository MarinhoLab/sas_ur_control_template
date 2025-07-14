from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration


def generate_launch_description():

    return LaunchDescription([
        Node(
            package='sas_operator_side_receiver',
            executable='sas_operator_side_receiver_udp_node',
            output='screen',
            emulate_tty=True,
            name='sas_operator_side_receiver_udp_node',
            parameters=[{
                "patient_side_ips": ["192.168.1.67"],
                "patient_side_ports": [2222],
                "operator_side_ports": [2223]
            }]
        )

    ])
