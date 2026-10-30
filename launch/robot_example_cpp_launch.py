# Copyright (c) 2012-2026 Murilo Marques Marinho
#
#    This file is part of sas_ur_control_template.
#
#    sas_ur_control_template is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    sas_ur_control_template is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with sas_ur_control_template.  If not, see <https://www.gnu.org/licenses/>.

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    config_file = LaunchConfiguration('config_file')

    real_robot_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('sas_robot_driver_ur'), 'launch'),
            '/robot_launch.py']),
        launch_arguments=[
            ('name', 'ur_1'),
            ('config_file', config_file),
        ]
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'config_file',
            default_value=os.path.join(get_package_share_directory('sas_ur_control_template'), 'config', 'config.yaml')
        ),
        real_robot_launch,
        Node(
            package='sas_ur_control_template',
            executable='joint_interface_example_cpp',
            output='screen',
            emulate_tty=True,
            name='sas_ur_control_template_joint_interface_example',
            parameters=[config_file]
        )
    ])
