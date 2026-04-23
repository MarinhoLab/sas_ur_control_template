#!/usr/bin/python3
"""
Copyright (C) 2020-2026 Murilo Marques Marinho (www.murilomarinho.info)
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later
version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program. If not,
see <https://www.gnu.org/licenses/>.
"""
import time

import numpy as np

from dqrobotics import *
from dqrobotics.robot_control import DQ_PseudoinverseController, ControlObjective
from math import pi

from sas_ur_control_template.kinematics import get_kinematics

import rclpy
from rclpy.node import Node

from sas_common import rclcpp_init, rclcpp_Node, rclcpp_spin_some, rclcpp_shutdown, ObjectClient
from sas_robot_driver import RobotDriverClient
from sas_core import Clock
from sas_datalogger import DataloggerClient

def main(args=None):

    cfg = {
        "controller_gain": 4.0,
        "damping": 0.1,
        "effector": DQ([1]),
        "q_init": [0, -pi/3.0, pi/3.0, -pi/2, -pi/2, 0],
        "sampling_time": 0.001,
    }

    rclpy.init(args=args)
    rospy_node = Node('sas_robot_driver_ur_task_space_example_node_py')

    rclcpp_init()
    roscpp_node = rclcpp_Node("sas_robot_driver_ur_task_space_example_node_cpp")

    datalogger_client = DataloggerClient(roscpp_node)

    rospy_node.declare_parameter('robot_topic_name', '/sas_robot_driver_coppeliasim/UR3e')
    robot_topic_name = rospy_node.get_parameter('robot_topic_name').get_parameter_value().string_value
    rospy_node.declare_parameter('xd_topic_name', '/sas_robot_driver_coppeliasim/object/xd')
    xd_topic_name = rospy_node.get_parameter('xd_topic_name').get_parameter_value().string_value

    clock = Clock(cfg['sampling_time'])
    clock.init()

    oc_base = ObjectClient(roscpp_node, "/sas_robot_driver_coppeliasim/object/UR3e/UR3e_base")
    oc_x = ObjectClient(roscpp_node, "/sas_robot_driver_coppeliasim/object/x")
    oc_xd = ObjectClient(roscpp_node, xd_topic_name)
    rdi = RobotDriverClient(roscpp_node, robot_topic_name)

    while not (rdi.is_enabled()
               and oc_x.is_enabled()
               and oc_xd.is_enabled()
               and oc_base.is_enabled()
               and datalogger_client.is_enabled()):
        rclcpp_spin_some(roscpp_node)
        time.sleep(0.1)

    try:

        robot_kinematics = get_kinematics()
        robot_kinematics.set_effector(cfg["effector"])
        robot_kinematics.set_reference_frame(oc_base.get_pose())

        joint_limits = rdi.get_joint_limits()
        print(f"Joint limits from RDI: {joint_limits}")
        robot_kinematics.set_lower_q_limit(joint_limits[0])
        robot_kinematics.set_upper_q_limit(joint_limits[1])

        task_space_controller = DQ_PseudoinverseController(robot_kinematics)
        task_space_controller.set_gain(cfg["controller_gain"])
        task_space_controller.set_damping(cfg["damping"])
        task_space_controller.set_control_objective(ControlObjective.Pose)

        for key in cfg:
            datalogger_client.log(key, cfg[key] if not isinstance(cfg[key], DQ) else vec8(cfg[key]))

        q_init = cfg["q_init"]
        rdi.send_target_joint_positions(q_init)

        x_init = robot_kinematics.fkm(q_init)

        oc_x.send_pose(x_init)
        oc_xd.send_pose(x_init)

        sampling_time = 0.001

        # Make sure the initial values have been reflected in the robot and simulation.
        def joint_condition(a, b) -> bool:
            return np.allclose(a, b, atol=1e-3)

        def x_condition(a, b) -> bool:
            return a == b

        while not (joint_condition(q_init, rdi.get_joint_positions())
                and x_condition(x_init, oc_x.get_pose())):
            print(f"Waiting for initial state to be reflected {joint_condition(q_init, rdi.get_joint_positions())},{x_condition(x_init, oc_x.get_pose())}...")
            rclcpp_spin_some(roscpp_node)
            time.sleep(0.1)

        q = q_init
        while True:
            clock.update_and_sleep()

            x = robot_kinematics.fkm(q)
            xd = oc_xd.get_pose()

            # Even this simple example has unwinding, so we take care of that here
            V1 = np.linalg.norm(vec8(x - xd))
            V2 = np.linalg.norm(vec8(x + xd))
            if V2 < V1:
                xd = -xd

            u = task_space_controller.compute_setpoint_control_signal(q, vec8(xd))
            q = q + u * sampling_time


            datalogger_client.log("q", q)
            datalogger_client.log("u", u)
            datalogger_client.log("xd", vec8(xd))
            datalogger_client.log("x", vec8(x))

            rdi.send_target_joint_positions(q)
            oc_x.send_pose(x)
            rclcpp_spin_some(roscpp_node)

    except Exception as e:
        print("vs050_reference_control::control_loop::Exception caught: ", e)
    except KeyboardInterrupt:
        print("vs050_reference_control::control_loop::KeyboardInterrupt")

    rclcpp_shutdown()

if __name__ == "__main__":
    main()