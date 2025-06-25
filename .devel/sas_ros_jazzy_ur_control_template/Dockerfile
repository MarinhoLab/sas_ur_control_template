FROM murilomarinho/sas_ros_jazzy_coppeliasim
LABEL authors="murilomarinho"
ARG ROS_DOMAIN_ID=1
ENV ROS_DOMAIN_ID=$ROS_DOMAIN_ID
SHELL ["/bin/bash", "-c"]
ENV BASH_ENV="/etc/bash_env"

RUN mkdir -p cd ~/sas_tutorial_workspace/src
RUN cd ~/sas_tutorial_workspace/src && git clone https://github.com/MarinhoLab/sas_ur_control_template.git
RUN /bin/bash -c "source /opt/ros/jazzy/setup.bash; cd ~/sas_tutorial_workspace/; colcon build"
