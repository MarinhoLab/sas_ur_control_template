"""Launch the UR3e simulation control template for Gazebo.

Run directly with:
    python3 ur3e_simulation_example_py_launch.py [robot_topic_name:=ur3e_sim]

Or via Docker Compose:
    docker compose -f docker/gazebo/compose_simulation.yml up
"""
import sys

from launch import LaunchDescription, LaunchService
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description(robot_topic_name='ur3e_sim'):
    """Generate the launch description for UR3e Gazebo simulation."""
    # Parse command-line args like robot_topic_name:=foo
    args = dict(
        (k, v)
        for arg in sys.argv[1:]
        if ':=' in arg
        for k, v in [arg.split(':=', 1)]
    )
    topic = args.get('robot_topic_name', robot_topic_name)

    return LaunchDescription([
        DeclareLaunchArgument(
            'robot_topic_name',
            default_value=topic,
            description='Robot topic name for the UR3e Gazebo simulation driver.',
        ),
        Node(
            package='sas_ur_control_template',
            executable='joint_interface_example.py',
            output='screen',
            emulate_tty=True,
            name='sas_ur_control_template_ur3e_simulation',
            parameters=[{"robot_topic_name": topic}],
        ),
    ])


if __name__ == '__main__':
    ls = LaunchService()
    ls.add_launch_description(generate_launch_description())
    ls.run()