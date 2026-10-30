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
from dqrobotics.interfaces.json11 import DQ_JsonReader


def get_kinematics():
    json_reader = DQ_JsonReader()
    robot_file_path = os.path.join(get_package_share_directory('sas_robot_driver_ur'),'robots','ur3e.json')
    return json_reader.get_serial_manipulator_dh_from_json(robot_file_path)

