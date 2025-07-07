# SAS UR Control Template

> [!TIP]
> More information about the SmartArmStack is available in https://smartarmstack.github.io/.

This is a control template for [Universal Robots](https://www.universal-robots.com) robotic manipulators. It relies on [`sas_robot_driver_ur`](https://github.com/MarinhoLab/sas_robot_driver_ur) to communicate
with the robot via [URCL](https://github.com/UniversalRobots/Universal_Robots_Client_Library).

## Docker image

### Simulation demonstrator

https://github.com/user-attachments/assets/bfee1148-bfe3-4425-80da-04fcd65d2b18

![](../../docs/videos/sas_urct_simulation.mp4)

> [!IMPORTANT]
> If running on a `arm64` Linux system host, remember to install
> ```commandline
> sudo apt-get install qemu-user-static
> ```

```commandline
mkdir -p ~/sas_urct/simulation_demo && cd ~/sas_urct/simulation_demo
curl -OL https://raw.githubusercontent.com/MarinhoLab/sas_ur_control_template/refs/heads/main/.devel/simulation_demo/compose.yml
xhost +local:root
docker compose up
```

### Real robot

> [!CAUTION]
> For using the real robot, you **must** have the risk assessments in place. 
> This guide is meant to be helpful but holds absolutely no liability whatsoever. More details are available in the software license.

> [!WARNING]
> This code will move the robot. Be sure that the workspace is free and safe for operation.
> Be sure that the robot is in a joint configuration in which it will not hit itself or anything around it. 

```commandline
mkdir -p ~/sas_urct/robot_demo && cd ~/sas_urct/robot_demo
curl -OL https://raw.githubusercontent.com/MarinhoLab/sas_ur_control_template/refs/heads/main/.devel/robot_demo/compose.yml
docker compose up
```

## From source (advanced)

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

1. Open the scene `scenes/UR3e_480rev0.ttt` on CoppeliaSim and start the simulation.
2. `ros2 launch sas_ur_control_template simulation_example_cpp_launch.py`

## Working with the real robot

> [!IMPORTANT]
> Be sure that the teaching pendant is in `Remove Control` mode.

> [!TIP]
> Use your robot's IP address in `ur1_ip`. Refer to `launch/_real_robot_launch.py`.

Run

```commandline
ros2 launch real_robot_move_example_py_launch.py ur1_ip:=192.170.10.22
```

## See also

https://github.com/UniversalRobots/Universal_Robots_ROS_Driver/issues/507
