#!/usr/bin/python3
"""
# Copyright (c) 2012-2025 Murilo Marques Marinho
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
#
# #######################################################################################
#
#   Author: Murilo M. Marinho, email: murilomarinho@ieee.org
#   Based on `joint_interface_example.py` from `sas_robot_driver_kuka`
#
# #######################################################################################
"""
import time

import rclpy
from rclpy.node import Node

from math import sin, pi

import numpy
from dqrobotics import *  # Despite what PyCharm might say, this is very much necessary or DQs will not be recognized
from dqrobotics.utils.DQ_Math import deg2rad

from sas_common import rclcpp_init, rclcpp_Node, rclcpp_spin_some, rclcpp_shutdown
from sas_robot_driver import RobotDriverClient

from sas_core import Clock, Statistics


def main(args=None):
    try:
        rclpy.init(args=args)
        rospy_node = Node('sas_robot_driver_ur_joint_space_example_node_py')

        rospy_node.declare_parameter('robot_topic_name', 'ur_1_sim')
        robot_topic_name = rospy_node.get_parameter('robot_topic_name').get_parameter_value().string_value

        rclcpp_init()
        roscpp_node = rclcpp_Node("sas_robot_driver_ur_joint_space_example_node_cpp")
       
        # 10 ms clock
        clock = Clock(0.01)
        clock.init()

        # Initialize the RobotDriverClient
        rdi = RobotDriverClient(roscpp_node, robot_topic_name)

        # Wait for RobotDriverClient to be enabled
        while not rdi.is_enabled():
            rclcpp_spin_some(roscpp_node)
            time.sleep(0.1)

        # Get topic information
        print(f"topic prefix = {rdi.get_topic_prefix()}")

        # Read the values sent by the RobotDriverServer
        joint_positions = rdi.get_joint_positions()
        print(f"joint positions = {joint_positions}")

        # For some iterations. Note that this can be stopped with CTRL+C.
        for i in range(0, 5000):
            clock.update_and_sleep()

            # Move the joints
            target_joint_positions = joint_positions + deg2rad([10.0 * sin(i / (50.0 * pi))] * 6)
            # print(target_joint_positions)
            rdi.send_target_joint_positions(target_joint_positions)

            rclcpp_spin_some(roscpp_node)

        # Statistics
        print("Statistics for the entire loop")
        print("  Mean computation time: {}".format(clock.get_statistics(
            Statistics.Mean, Clock.TimeType.Computational)
        ))
        print("  Mean idle time: {}".format(clock.get_statistics(
            Statistics.Mean, Clock.TimeType.Idle)
        ))
        print("  Mean effective thread sampling time: {}".format(clock.get_statistics(
            Statistics.Mean, Clock.TimeType.EffectiveSampling)
        ))

        rclcpp_shutdown()

    except KeyboardInterrupt:
        print("Interrupted by user")
    except Exception as e:
        print("Unhandled excepts", e)


if __name__ == '__main__':
    main()
