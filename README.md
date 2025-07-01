# sas_ur_control_template

This is a template control package for `sas_robot_driver_ur`. 

## Docker image ![Docker Pulls](https://img.shields.io/docker/pulls/murilomarinho/sas_ur_control_template)

> [!CAUTION]
> This image is experimental. Please read docker instructions to know if this level of privileges is acceptable for
> your system and application.

### Do once

> [!IMPORTANT]
> If running on a `arm64` Linux system, remember to install
> ```commandline
> sudo apt-get install qemu-user-static
> ```

> [!NOTE]
> Depending on your network settings, you might want to do in the host to allow the CoppelaSim port.
> ```commandLine
> sudo ufw allow 23000
> ```

```commandline
mkdir -p ~/sas
cd ~/sas
git clone https://github.com/MarinhoLab/sas_ur_control_template.git
```

### Do every time

```commandline
cd ~/sas/sas_ur_control_template/.devel/composed_demo

xhost +local:root
sudo docker compose up
```

## From source (advanced)

> [!IMPORTANT]
> Using this package from source requires some understanding of ROS 2. 

### 1. Pre-requisites

Follow the installation requirements defined in the [SAS Tutorial](https://ros2-tutorial.readthedocs.io/en/latest/sas/installation.html).

### 2. Building and sourcing

As an example, see below.

```
cd ~/sas_tutorial_workspace
colcon build
source install/setup.bash
```

## Clone the repository
 
```commandLine
mkdir -p ~/sas_tutorial_workspace/src
cd ~/sas_tutorial_workspace/src
git clone https://github.com/MarinhoLab/sas_ur_control_template.git
```

### Working in simulation

https://github.com/user-attachments/assets/bfee1148-bfe3-4425-80da-04fcd65d2b18

1. Open the scene `scenes/UR3e_480rev0.ttt` on CoppeliaSim. 
2. Start the simulation by clicking the start button.
3. `ros2 launch sas_ur_control_template dummy_move_in_coppeliasim_example_cpp_launch.py`

## Working with the real robot

https://github.com/user-attachments/assets/5902f735-6c42-4825-a552-58e565bbf3f3

> [!IMPORTANT]
> For using the real robot, you **must** have the risk assessments in place. 
> This guide is meant to be helpful but holds absolutely no liability whatsoever. More details are available in the software license.

> [!WARNING]
> This code will move the robot. Be sure that the workspace is free and safe for operation.
> Be sure that the robot is in a joint configuration in which it will not hit itself or anything around it. 

1. Be sure that the teaching pendant is in `Remove Control` mode.  
2. Split the terminator into four screens. Now, the order matters.

| `a` | `b` |
|-----|-----|
| `c` | `d` |

3. In `a`, run the CoppeliaSim scene `scenes/UR3e_480rev0.ttt` and start the simulation.
4. In `b`, run `ros2 launch sas_ur_control_template real_robot_launch.py`
   - The emergency button must be held at all times.
   - After some seconds of initialization, the robot will be active. 
6. In `c`, run `ros2 launch sas_ur_control_template compose_with_coppeliasim_launch.py`. This will connect the CoppeliaSim scene with the ros2 code.
7. In `d`, run `ros2 run sas_ur_control_template joint_interface_example.py`. The robot will move in a sine wave in joint space, with respect to its initial joint values.

## Troubleshooting tips

https://github.com/UniversalRobots/Universal_Robots_ROS_Driver/issues/507
