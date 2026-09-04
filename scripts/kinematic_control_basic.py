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
        "controller_gain": 1.,
        "damping": 0.1,
        "effector": DQ([1]),
        "sampling_time": 0.001,
    }

    rclpy.init(args=args)
    rospy_node = Node('sas_robot_driver_ur_task_space_example_node_py')

    rclcpp_init()
    roscpp_node = rclcpp_Node("sas_robot_driver_ur_task_space_example_node_cpp")

    rospy_node.declare_parameter('robot_topic_name', '/ur3e')
    robot_topic_name = rospy_node.get_parameter('robot_topic_name').get_parameter_value().string_value

    clock = Clock(cfg['sampling_time'])
    clock.init()

    rdi = RobotDriverClient(roscpp_node, robot_topic_name)

    while not (rdi.is_enabled()):
        rclcpp_spin_some(roscpp_node)
        time.sleep(0.1)

    try:

        robot_kinematics = get_kinematics()

        joint_limits = rdi.get_joint_limits()
        print(f"Joint limits from RDI: {joint_limits}")
        robot_kinematics.set_lower_q_limit(joint_limits[0])
        robot_kinematics.set_upper_q_limit(joint_limits[1])

        task_space_controller = DQ_PseudoinverseController(robot_kinematics)
        task_space_controller.set_gain(cfg["controller_gain"])
        task_space_controller.set_damping(cfg["damping"])
        task_space_controller.set_control_objective(ControlObjective.Pose)

        q_init = rdi.get_joint_positions()

        sampling_time = 0.001

        # H =
        # [ 1 0 0 -0.01]
        # [ 0 1 0 0    ]
        # [ 0 0 1 0    ]
        # [ 0 0 0 1    ]

        # H =
        # [ 1 0 0 0    ]
        # [ 0 1 0 -0.01]
        # [ 0 0 1 0    ]
        # [ 0 0 0 1    ]

        # H =
        # [ 1 0 0 0    ]
        # [ 0 1 0 0    ]
        # [ 0 0 1 -0.01]
        # [ 0 0 0 1    ]

        y_prime = -(j_ + i_).normalize()
        z_prime = k_
        x_prime = cross(y_prime, z_prime)

        targets = [
            (1.0 + 0.5 * E_ * (  0.05 * z_prime)),
            (1.0 + 0.5 * E_ * (  0.35 * y_prime)),
            (1.0 + 0.5 * E_ * ( -0.10 * z_prime)),
            (1.0 + 0.5 * E_ * (  0.10 * z_prime)),
            (1.0 + 0.5 * E_ * ( -0.35 * y_prime)),
            (1.0 + 0.5 * E_ * ( -0.05 * z_prime)),
            (1.0 + 0.5 * E_ * ( -0.23 * y_prime)),
            (1.0 + 0.5 * E_ * (  0.23 * y_prime)),
        ]

        q = q_init
        xd = robot_kinematics.fkm(q)
        for target in targets:
            xd = target * xd

            for _ in range(10000):
                x = robot_kinematics.fkm(q)
                clock.update_and_sleep()

                # Even this simple example has unwinding, so we take care of that here
                V1 = np.linalg.norm(vec8(x - xd))
                V2 = np.linalg.norm(vec8(x + xd))
                if V2 < V1:
                    xd = -xd

                u = task_space_controller.compute_setpoint_control_signal(q, vec8(xd))
                q = q + u * sampling_time

                rdi.send_target_joint_positions(q)
                rclcpp_spin_some(roscpp_node)

    except Exception as e:
        print("vs050_reference_control::control_loop::Exception caught: ", e)
    except KeyboardInterrupt:
        print("vs050_reference_control::control_loop::KeyboardInterrupt")

    rclcpp_shutdown()

if __name__ == "__main__":
    main()