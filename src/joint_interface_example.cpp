#include <rclcpp/rclcpp.hpp>
#include <sas_core/sas_clock.hpp>
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
    auto node = std::make_shared<rclcpp::Node>("sas_ur_control_template_joint_interface_example");

    // 1 ms clock
    sas::Clock clock{0.001};
    clock.init();

    // Initialize the RobotDriverClient
    sas::RobotDriverClient rdi(node, "ur_composed");

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
