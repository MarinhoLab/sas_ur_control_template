# SAS UR Control Template

This is a template control package for `sas_robot_driver_ur`. 

## Docker image ![Docker Pulls](https://img.shields.io/docker/pulls/murilomarinho/sas)

### Simulation demonstrator

```commandline
mkdir -p ~/sas_urct && cd ~/sas_urct
curl -OL https://raw.githubusercontent.com/MarinhoLab/sas_ur_control_template/refs/heads/main/.devel/simulation_demo/compose.yml
xhost +local:root
docker compose up
```

### Troubleshooting

> [!IMPORTANT]
> If running on a `arm64` Linux system host, remember to install
> ```commandline
> sudo apt-get install qemu-user-static
> ```

## From source (advanced)

> [!IMPORTANT]
> Using this package from source requires some understanding of ROS 2. 

### 1. Pre-requisites

Follow setup in [SAS Tutorial](https://ros2-tutorial.readthedocs.io/en/latest/sas/installation.html).

### 2. Clone the repository
 
```commandLine
mkdir -p ~/sas_tutorial_workspace/src
cd ~/sas_tutorial_workspace/src
git clone https://github.com/MarinhoLab/sas_ur_control_template.git
```

### 3. Building and sourcing

```commandLine
cd ~/sas_tutorial_workspace
colcon build
source install/setup.bash
```

### Working in simulation

https://github.com/user-attachments/assets/bfee1148-bfe3-4425-80da-04fcd65d2b18

1. Open the scene `scenes/UR3e_480rev0.ttt` on CoppeliaSim and start the simulation by clicking the start button.
2. `ros2 launch sas_ur_control_template dummy_move_in_coppeliasim_example_cpp_launch.py`

## Working with the real robot

> [!CAUTION]
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
