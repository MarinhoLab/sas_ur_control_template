# SAS UR Control Template

> [!TIP]
> Repository for this template: https://github.com/MarinhoLab/sas_ur_control_template \
> More information about SmartArmStack is available in https://smartarmstack.github.io/.

This is a control template for [Universal Robots](https://www.universal-robots.com) robotic manipulators. It relies on [`sas_robot_driver_ur`](https://github.com/MarinhoLab/sas_robot_driver_ur) to communicate
with the robot via [URCL](https://github.com/UniversalRobots/Universal_Robots_Client_Library).

## Docker

Sample containers for real robot and simulated robot motion are available. Those can be tested without cloning this repository. For more advanced use, users are advised to clone and modify the sample cpp code in `src` or the sample Python code in `scripts`.

### Real robot

> [!CAUTION]
> For using the real robot, you **must** have the risk assessments in place. 
> This guide is meant to be helpful but holds absolutely no liability whatsoever. More details are available in the software license.

> [!WARNING]
> This code will move the robot. Be sure that the workspace is free and safe for operation.
> Be sure that the robot is in a joint configuration in which it will not hit itself or anything around it. 

https://github.com/user-attachments/assets/62ac7ccd-d7c8-41f7-8af8-1b17919d90f2

![](./sas_urct_realrobot.mp4)

Run

```commandline
mkdir -p ~/sas_tutorial_workspace/docker/sas_ur_control_template/robot_demo
cd ~/sas_tutorial_workspace/docker/sas_ur_control_template/robot_demo
curl -OL https://raw.githubusercontent.com/MarinhoLab/sas_ur_control_template/refs/heads/main/docker/robot_demo/compose.yml

docker compose up
```
> [!IMPORTANT]
> Be sure that the teaching pendant is in `Remote Control` mode.

> [!TIP]
> Use your robot's IP address in `ur1_ip`. Refer to `launch/_real_robot_launch.py`.

### Joint control simulation

https://github.com/user-attachments/assets/bfee1148-bfe3-4425-80da-04fcd65d2b18

![](./sas_urct_simulation.mp4)

Run

```commandline
mkdir -p ~/sas_tutorial_workspace/docker/sas_ur_control_template/simulation_demo
cd ~/sas_tutorial_workspace/docker/sas_ur_control_template/simulation_demo
curl -OL https://raw.githubusercontent.com/MarinhoLab/sas_ur_control_template/refs/heads/main/docker/simulation_demo_v2/compose.yml

xhost +local:root
docker compose up
```

### Kinematics simulation

The desired pose can be controlled via the `xd` dummy on the CoppeliaSim simulation.

```commandline
mkdir -p ~/sas_tutorial_workspace/docker/sas_ur_control_template/simulation_demo
cd ~/sas_tutorial_workspace/docker/sas_ur_control_template/simulation_demo
curl -OL https://raw.githubusercontent.com/MarinhoLab/sas_ur_control_template/refs/heads/main/docker/simulation_demo_v2_kinematic/compose.yml

xhost +local:root
docker compose up
```

# Configuration

> [!CAUTION]
> Changing network settings can increase [cybersecurity](https://ros2-tutorial.readthedocs.io/en/latest/cybersecurity/index.html) vulnerabilities.
> This guide is meant to be helpful but holds absolutely no liability whatsoever. More details are available in the software license.

## Universal Robots Software 5.25.0

> [!TIP]
> Teaching pendant must be in `Manual` mode.

Necessary settings are shown below.

### Enable Networking

Set the network as needed in your application.

- Hamburger → Settings → System → Network → Static Address

### Enable Remote Control

- Hamburger → Settings → System → Remote Control → Enable

### Enable Services


> [!NOTE]
> Fewer permissions than these might be sufficient, if so please open an [issue](https://github.com/MarinhoLab/sas_ur_control_template/issues).

- Hamburger → Settings → System → Services → Services

|         |                                |
|---------|--------------------------------|
| Enabled | Dashboard Server               |
| Enabled | Primary Client Interface       |
| Enabled | Secondary Client Interface     |
| Enabled | Real-Time Client Interface     |
| Enabled | Real-Time Data Exchange (RTDE) |
| Enabled | Interpreter Mode Socket        |
