# sas_ur_control_template

This is a template control package for `sas_robot_driver_ur`. 

## Up to date information

If you create a template of this repository, it will not automatically be up to date with the latest information.
See https://github.com/MarinhoLab/sas_ur_control_template for the latest instructions.

## Initial setup

### 1. Pre-requisites

Follow the installation requirements defined in the [Pre-Requisites @ 📑 Wiki](https://github.com/SmartArmStack/smart_arm_stack_ROS2/wiki/Pre-Requisites).

### 2. Cloning SmartArmStack ROS2

Clone SAS RO2 with [Cloning Instructions @ 📑 Wiki](https://github.com/SmartArmStack/smart_arm_stack_ROS2/wiki/Cloning-Instructions).

### 3. Building and sourcing

```
cd ~/ros2_ws
colcon build
source install/setup.bash
```

## Use this template to create your own repository.
<img width="1175" alt="Screenshot 2024-11-28 at 12 23 00" src="https://github.com/user-attachments/assets/6d030baa-5c0b-403b-a807-79248a54cb0a">

Supposing that you created a repository called `https://github.com/YOUR_USER/sas_ur_control_template.git` based on this template, do

:exclamation: If you're cloning a repository to push changes to Github, remember [to set your ssh keys on Github](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account). Otherwise the step below will not work.
 
```commandLine
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
git clone git@github.com:YOUR_USER/sas_ur_control_template.git
```

:exclamation: This repository is a ROS2 package. If you change the name of the folder, you must remember to change the name on the `package.xml` and `CMakeLists.txt` otherwise `colcon` might misbehave.

## Working in simulation

1. Open the scene `scenes/UR3_470rev4.ttt` on CoppeliaSim. Please be attentive of the version.
2. Start the simulation by clicking the start button.
3. `ros2 launch sas_ur_control_template dummy_move_in_coppeliasim_example_cpp_launch.py`

The robot should move as shown below.

https://github.com/user-attachments/assets/bfee1148-bfe3-4425-80da-04fcd65d2b18

## Working with the real robot

For using the real robot, you **must** have the risk assessments in place. This guide is meant to be helpful but holds absolutely no liability whatsoever. More details are available in the software license.

This code will move the robot. Be sure that the workspace is free and safe for operation.
:exclamation: Be sure that the robot is in a joint configuration in which it will not hit itself or anything around it. Example picture:

1. Be sure that the teaching pendant is in `Remove Control` mode.  
2. Split the terminator into four screens. Now, the order matters.

| `a` | `b` |
|-----|-----|
| `c` | `d` |

3. In `a`, run the CoppeliaSim scene `scenes/UR3_470rev4.ttt` and start the simulation.
4. In `b`, run `ros2 launch sas_ur_control_template real_robot_launch.py`
   - The emergency button must be held at all times.
   - After some seconds of initialization, the robot will be active. 
6. In `c`, run `ros2 launch sas_ur_control_template compose_with_coppeliasim_launch.py`. This will connect the CoppeliaSim scene with the ros2 code.
7. In `d`, run `ros2 run sas_ur_control_template joint_interface_example.py`. The robot will move in a sine wave in joint space, with respect to its initial joint values.


https://github.com/user-attachments/assets/5902f735-6c42-4825-a552-58e565bbf3f3

## Troubleshooting tips

https://github.com/UniversalRobots/Universal_Robots_ROS_Driver/issues/507
