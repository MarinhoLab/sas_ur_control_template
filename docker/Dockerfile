FROM ghcr.io/marinholab/sas-full:jazzy
LABEL authors="murilomarinho"
SHELL ["/bin/bash", "-c"]
ENV BASH_ENV="/etc/bash_env"

RUN mkdir -p /root/sas_ur_control_template_devel/src
COPY . /root/sas_ur_control_template_devel/src/sas_ur_control_template
WORKDIR /root/sas_ur_control_template_devel
RUN colcon build
RUN echo "source /root/sas_ur_control_template_devel/install/setup.bash" > /etc/bash_env