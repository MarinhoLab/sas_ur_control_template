# sas_ur_control_template

This is a template control package for `sas_robot_driver_ur`. 

## Initial setup

### Basic Pre-requisites

https://github.com/SmartArmStack/smart_arm_stack_ROS2/blob/jazzy/README.md#prerequisites

### Additional Pre-requisites

None

### Cloning SmartArmStack ROS2

```commandLine
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
git clone --recurse-submodules -b jazzy https://github.com/SmartArmStack/smart_arm_stack_ROS2.git sas
```

### Building and sourcing

```
cd ~/ros2_ws
colcon build
source install/setup.bash
```

## Use this template to create your own repository.
<img width="1175" alt="Screenshot 2024-11-28 at 12 23 00" src="https://github.com/user-attachments/assets/6d030baa-5c0b-403b-a807-79248a54cb0a">

Supposing that you created a repository called `https://github.com/YOUR_USER/sas_ur_control_template.git` based on this template, do

```commandLine
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
git clone git@github.com:YOUR_USER/sas_ur_control_template.git
```

:exclamation: This repository is a ROS2 package. If you change the name of the folder, you must remember to change the name on the `package.xml` and `CMakeLists.txt` otherwise `colcon` might misbehave.
 
## Interfacing your code with `sas_robot_driver_ur`

This package is intended to expose joint positions of the robot to ROS2. It is based on the [sas_robot_driver](https://github.com/SmartArmStack/sas_robot_driver/tree/jazzy) server--client topology. 

### Server

Each robot node will create a server with ROS2 topics. That is completely managed by [sas_robot_driver](https://github.com/SmartArmStack/sas_robot_driver/tree/jazzy). 
You **must** use a launch file to create your own servers, if needed. For guidance, use `launch/real_robot_launch.py` and modify as needed.

For most users, you will only need to modify the ip address to match the ip address of your robot.

https://github.com/MarinhoLab/sas_ur_control_template/blob/33bb7b7be21ffaf7df0a72052431dbe6af06ce5a/launch/real_robot_launch.py#L28

If you have multiple robots, remember to change each one to have a unique name.

https://github.com/MarinhoLab/sas_ur_control_template/blob/33bb7b7be21ffaf7df0a72052431dbe6af06ce5a/launch/real_robot_launch.py#L26

### Client

After your server is running, you can obtain current joint positions and send joint position commands.
All those are managed through ROS2 topics. 

:exclamation: [sas_robot_driver](https://github.com/SmartArmStack/sas_robot_driver/tree/jazzy) handles all ROS2 publishers and subscribers for you. <ins>DO **NOT** CREATE THEM MANUALLY</ins>. In, C++ **and Python** with the `RobotDriverClient` class.

https://github.com/MarinhoLab/sas_ur_control_template/blob/33bb7b7be21ffaf7df0a72052431dbe6af06ce5a/scripts/joint_interface_example.py#L36

An example on how to do that using `rclpy` is available at 

```
scripts/joint_interface_example.py
```

#### Getting joint positions

https://github.com/MarinhoLab/sas_ur_control_template/blob/33bb7b7be21ffaf7df0a72052431dbe6af06ce5a/scripts/joint_interface_example.py#L62

#### Sending joint position commands

https://github.com/MarinhoLab/sas_ur_control_template/blob/33bb7b7be21ffaf7df0a72052431dbe6af06ce5a/scripts/joint_interface_example.py#L72

### Ok, but what is this ROS composer thing?

When using CoppeliaSim, you will notice that we're not interfacing directly with the robot node. You can see that from the name

https://github.com/MarinhoLab/sas_ur_control_template/blob/33bb7b7be21ffaf7df0a72052431dbe6af06ce5a/scripts/joint_interface_example.py#L51

and the launch file that runs a `sas_robot_driver_ros_composer_node`

https://github.com/MarinhoLab/sas_ur_control_template/blob/33bb7b7be21ffaf7df0a72052431dbe6af06ce5a/launch/compose_with_coppeliasim_launch.py#L22

The composer node has two main roles. First, it allows us to abstract many different devices into a single serial robot. This is important for [complex systems](https://github.com/AISciencePlatform). It also allows us to reflect robot state in CoppeliaSim, as a virtual twin.

These are specified in the following parameters in the launch file and most parameters are probably self-evident. 

https://github.com/MarinhoLab/sas_ur_control_template/blob/33bb7b7be21ffaf7df0a72052431dbe6af06ce5a/launch/compose_with_coppeliasim_launch.py#L29-L33

Please note that this means that CoppeliaSim can be executed in any computer accessible with the ip address and port specified. It can be a completely separate computer, for instance, running Windows or macOS.

## Working with CoppeliaSim

https://github.com/user-attachments/assets/bfee1148-bfe3-4425-80da-04fcd65d2b18

## Working with the real robot

For using the real robot, you **must** have the risk assessments in place. This guide is meant to be helpful but holds absolutely no liability whatsoever. More details are available in the software license.

This code will move the robot. Be sure that the workspace is free and safe for operation.

1. Be sure that the teaching pendant is in `Remove Control` mode.  
2. Split the terminator into four screens. Now, the order matters.

| `a` | `b` |
|-----|-----|
| `c` | `d` |

3. In `a`, run the CoppeliaSim scene `scenes/UR3_470rev4.ttt` and start the simulation.
4. In `b`, run `ros2 launch sas_robot_driver_ur real_robot_launch.py`
   - The emergency button must be held at all times.
   - After some seconds of initialization, the robot will be active. 
6. In `c`, run `ros2 launch sas_robot_driver_ur composed_with_coppeliasim_launch.py`. This will connect the CoppeliaSim scene with the ros2 code.
7. In `d`, run `ros2 run sas_robot_driver_ur joint_interface_example.py`. The robot will move in a sine wave in joint space, with respect to its initial joint values.


https://github.com/user-attachments/assets/5902f735-6c42-4825-a552-58e565bbf3f3

## Troubleshooting tips

https://github.com/UniversalRobots/Universal_Robots_ROS_Driver/issues/507
