# AGENTS.md — sas_ur_control_template

Template package for controlling UR robots via SmartArmStack (`sas_robot_driver_ur` for real robots, `sas_robot_driver_gazebo` for simulation). Repo: https://github.com/MarinhoLab/sas_ur_control_template/

## Layout quick map

- `config/config.yaml` — all node parameters, one top-level block per node name. The block name MUST match the node name passed via `name:=` to the launch files (e.g. `ur_sim_1`, `sas_object_server_gazebo_node`).
- `launch/` — teleoperation + CoppeliaSim launches only. **No Gazebo launches live here** — the Gazebo stack is driven by `sas_robot_driver_gazebo`'s own launch files (in the driver package), invoked by `docker/gazebo/compose.yml`.
- `docker/gazebo/compose.yml` — the GazeboSim stack: `setup_vendor.sh ur` → `robot_driver_server_launch.py name:=ur_sim_1` → `object_server_launch.py` → `simulator_server_launch.py` → `gz sim ur3e_world.sdf` (all with `config_file:=<this repo's config.yaml>`).
- `docker/Dockerfile.Gazebo` — builds from `ghcr.io/marinholab/gazebo:jazzy` + `ros-jazzy-sas-*` from the smartarmstack apt repo; `ghcr.io/marinholab/sas-full:jazzy` already contains everything (colcon included).

## Running the GazeboSim stack headlessly (verified 2026-10 with sas-full:jazzy, gz-sim 8.15.0)

Minimal one-liner (mount the repo, run the 3 launches + `gz sim -s`):

```bash
docker run --rm -it -v "$PWD":/ws:ro ghcr.io/marinholab/sas-full:jazzy bash -lc '
  source /opt/ros/jazzy/setup.bash
  ros2 run sas_robot_driver_gazebo setup_vendor.sh ur   # clones UR meshes into ~/.sas/.../vendor (needs network)
  colcon build --base-paths /ws --install-base /root/install
  source /root/install/setup.bash
  CFG=$(ros2 pkg prefix sas_ur_control_template --share)/config/config.yaml
  ros2 launch sas_robot_driver_gazebo robot_driver_server_launch.py name:=ur_sim_1 config_file:=$CFG &
  ros2 launch sas_robot_driver_gazebo object_server_launch.py config_file:=$CFG &
  ros2 launch sas_robot_driver_gazebo simulator_server_launch.py config_file:=$CFG &
  sleep 15
  cd $(ros2 pkg prefix sas_robot_driver_gazebo --share)/sdf
  exec gz sim -s ur3e_world.sdf'
```

Gotchas that cost time (verified the hard way):
1. **`GZ_SIM_HEADLESS` does not exist** in gz-sim 8.x. Headless = `gz sim -s <world>`. Without `-s` the GUI tries to start and aborts (`qt.qpa.xcb: could not connect to display` → SIGKILL). The repo's compose command uses bare `gz sim ur3e_world.sdf`, which only works with a mounted X display.
2. Keep `$CFG`/`$(...)` expansions inside the container shell (use `bash -lc '...'` with single quotes, or a script mounted in the workspace) — if the host expands them you get `malformed launch argument 'config_file:='` and nodes silently don't get config.
3. `setup_vendor.sh ur` needs network (clones Universal_Robots_ROS2_Description). GZ resource path already includes the vendor dir via `environment/gz_sim_resource_path.sh`; don't unset `GZ_SIM_RESOURCE_PATH`.
4. Startup timeline: vendor clone ~10s, colcon ~3s, nodes init ~15s, `::Connected to robot.` → `::Robot initialized.` appears ~10-20s after `gz sim` starts. Use generous timeouts.
5. Verify with: `ros2 topic echo /ur_sim_1/get/joint_states` and `gz topic -l` / `gz topic --echo --topic /world/ur3e_world/...` (note: `gz topic --echo` never exits on its own; always wrap in `timeout`).

## Known repo/image mismatches (as of image 26.10.1130329, repo main @3175b8e)

- **Object-server pose topics are silent unless the world loads the `AbsolutePosePublisher` plugin.** The image's bundled `ur3e_world.sdf` predates the upstream plugin block; upstream `jazzy` branch of MarinhoLab/sas_robot_driver_gazebo has it:
  ```
  <plugin filename="AbsolutePosePublisher" name="absolute_pose_publisher::AbsolutePosePublisher">
      <topic>/world/ur3e_world/absolute_pose/info</topic> ...
  ```
  The repo's `config.yaml` sets `get_pose_topic_name: /world/ur3e_world/absolute_pose/info` and `entity_names: [frame_x, frame_xd, frame_camera]`, but the bundled world has no `frame_camera` model either (only frame_x/frame_xd). Fixing the world (plugin + frame_camera include) makes `/frame_x|frame_xd|frame_camera/get/pose` stream. The `.so` ships at `/opt/ros/jazzy/share/sas_robot_driver_gazebo/plugins/` and `GZ_SIM_SYSTEM_PLUGIN_PATH` is already set.
- **Control is velocity-limited:** each `JointPositionController` uses `cmd_max: 0.25` rad/s, so joints take seconds to reach a new target. When testing motion, command continuously and read back after >=5s; one-shot commands read as "no movement".
- Verified end-to-end: ROS `set/target_joint_positions` → bridge → gz `cmd_pos` (topic `/model/ur3e/joint/<name>/0/cmd_pos`, msg `gz.msgs.VelocityPI`) → robot moves; ROS `get/joint_states` reflects Gazebo state.

## Conventions

- Robot topic prefix: `ur_1` = real robot, `ur_sim_1` = Gazebo sim. Config block names must match node names exactly.
- ROS distro: jazzy (aarch64 image). `ros-jazzy-sas-*` come from the smartarmstack apt repo (`smartarmstack_lgpl.list`).
- Don't push/PR without explicit request; tests here are docker-based, not unit-test based.
