/**
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
#
# #######################################################################################
#
#   Author: Murilo M. Marinho, email: murilomarinho@ieee.org
#   Based on `joint_interface_example.cpp` from `sas_robot_driver_kuka`
#
# #######################################################################################
**/
#include <rclcpp/rclcpp.hpp>
#include <sas_core/sas_clock.hpp>
#include <sas_common/sas_common.hpp>
#include <sas_robot_driver/sas_robot_driver_client.hpp>
#include <dqrobotics/utils/DQ_Math.h>

using namespace DQ_robotics;

#include<signal.h>
static std::atomic_bool kill_this_process(false);
void sig_int_handler(int)
{
    kill_this_process = true;
}

int main(int argc, char** argv)
{
    if(signal(SIGINT, sig_int_handler) == SIG_ERR)
    {
        throw std::runtime_error("::Error setting the signal int handler.");
    }

    rclcpp::init(argc,argv,rclcpp::InitOptions(),rclcpp::SignalHandlerOptions::None);
    auto node = std::make_shared<rclcpp::Node>("sas_robot_driver_ur_joint_space_example_node_cpp");

    std::string robot_topic_name;
    sas::get_ros_optional_parameter(node, "robot_topic_name", robot_topic_name, std::string("ur_1_sim"));

    // 1 ms clock
    sas::Clock clock{0.001};
    clock.init();

    // Initialize the RobotDriverClient
    sas::RobotDriverClient rdi(node, "ur_1_sim");

    // Wait for RobotDriverClient to be enabled
    while(!rdi.is_enabled() && !kill_this_process)
    {
        std::this_thread::sleep_for(std::chrono::milliseconds(10));
        rclcpp::spin_some(node);
    }

    // Get topic information
    RCLCPP_INFO_STREAM(node->get_logger(),"topic_prefix = " << rdi.get_topic_prefix());

    // Read the values sent by the RobotDriverServer
    auto joint_positions = rdi.get_joint_positions();
    RCLCPP_INFO_STREAM(node->get_logger(),"joint positions = " << joint_positions);


    // For some iterations. Note that this can be stopped with CTRL+C.
    for(auto i=0;i<5000;++i)
    {
        clock.update_and_sleep();

        // Move the joints
        auto target_joint_positions = joint_positions + VectorXd::Ones(joint_positions.size())*deg2rad(10.0 * sin(i / (50.0 * pi)));
        // print(target_joint_positions)
        rdi.send_target_joint_positions(target_joint_positions);

        rclcpp::spin_some(node);
    }

    // Statistics
    RCLCPP_INFO_STREAM(node->get_logger(),"Statistics for the entire loop");

    RCLCPP_INFO_STREAM(node->get_logger(),"  Mean computation time: " << clock.get_statistics(
                                               sas::Statistics::Mean, sas::Clock::TimeType::Computational));
    RCLCPP_INFO_STREAM(node->get_logger(),"  Mean idle time: " << clock.get_statistics(
                                               sas::Statistics::Mean, sas::Clock::TimeType::Idle));
    RCLCPP_INFO_STREAM(node->get_logger(),"  Mean effective thread sampling time: " << clock.get_statistics(
                                               sas::Statistics::Mean, sas::Clock::TimeType::EffectiveSampling));

}
