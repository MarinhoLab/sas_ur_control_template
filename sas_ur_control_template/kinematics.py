import os
from ament_index_python.packages import get_package_share_directory

from dqrobotics.interfaces.json11 import DQ_JsonReader

def get_kinematics():
    json_reader = DQ_JsonReader()
    robot_file_path = os.path.join(get_package_share_directory('sas_robot_driver_ur'),'robots','ur3e.json')
    return json_reader.get_serial_manipulator_dh_from_json(robot_file_path)

