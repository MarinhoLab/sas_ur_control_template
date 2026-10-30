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
from launch.actions import GroupAction, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import SetRemap


def generate_launch_description():

    ur3e_compose_launch = GroupAction(
        actions=[
            # Bridge the teleop master robot's Gazebo topics (source prefix
            # `ur3e_sim`, that model's own name) to the sim robot's driver
            # interface prefix `ur_sim_1`, which the multiarm controller reads.
            SetRemap(src='/ur3e_sim/get/joint_states', dst='/ur_sim_1/get/joint_states'),
            SetRemap(src='/ur3e_sim/set/target_joint_positions', dst='/ur_sim_1/set/target_joint_positions'),
            SetRemap(src='/ur3e_sim/get/joint_positions_min', dst='/ur_sim_1/get/joint_positions_min'),
            SetRemap(src='/ur3e_sim/get/joint_positions_max', dst='/ur_sim_1/get/joint_positions_max'),

        ]
    )

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
        sas_patient_side_manager_launch,
        sas_robot_kinematics_constrained_multiarm_launch
    ])
