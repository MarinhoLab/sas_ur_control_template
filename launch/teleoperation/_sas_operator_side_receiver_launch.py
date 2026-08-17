import os
import sys

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration


_REQUIRED_ENV_VARS = ['CONTROL_PC_IP', 'PATIENT_SIDE_PORT', 'OPERATOR_SIDE_PORT']


def generate_launch_description():
    for var in _REQUIRED_ENV_VARS:
        if var not in os.environ or not os.environ[var]:
            print(f"ERROR: Environment variable '{var}' is not set. "
                  f"Please set it in docker/.env or export it before launching.", file=sys.stderr)
            sys.exit(1)

    patient_side_ips = LaunchConfiguration('patient_side_ips')

    return LaunchDescription([
        DeclareLaunchArgument(
            'patient_side_ips',
            default_value=f"[{os.environ['CONTROL_PC_IP']}]"
        ),
        Node(
            package='sas_operator_side_receiver',
            executable='sas_operator_side_receiver_udp_node',
            output='screen',
            emulate_tty=True,
            name='sas_operator_side_receiver_udp_node',
            parameters=[{
                "patient_side_ips": patient_side_ips,
                "patient_side_ports": [int(os.environ['PATIENT_SIDE_PORT'])],
                "operator_side_ports": [int(os.environ['OPERATOR_SIDE_PORT'])]
            }]
        )

    ])
