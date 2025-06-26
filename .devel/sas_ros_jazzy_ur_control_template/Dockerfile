FROM murilomarinho/sas_ros_jazzy_coppeliasim
LABEL authors="murilomarinho"
ARG ROS_DOMAIN_ID=1
ENV ROS_DOMAIN_ID=$ROS_DOMAIN_ID
SHELL ["/bin/bash", "-c"]
ENV BASH_ENV="/etc/bash_env"

RUN mkdir -p cd ~/sas_tutorial_workspace/src
RUN cd ~/sas_tutorial_workspace/src && git clone https://github.com/MarinhoLab/sas_ur_control_template.git
RUN cd ~/sas_tutorial_workspace/src/sas_ur_control_template/.devel/scripts && chmod +x setup_environment.sh
RUN cd ~/sas_tutorial_workspace/src/sas_ur_control_template/.devel/scripts && bash -c "./setup_environment.sh"

