FROM murilomarinho/sas:jazzy
LABEL authors="murilomarinho"
SHELL ["/bin/bash", "-c"]
ENV BASH_ENV="/etc/bash_env"

RUN curl -s --compressed "https://marinholab.github.io/sas_debian_builder_noncommercial/KEY.gpg" \
| gpg --dearmor \
| sudo tee /etc/apt/trusted.gpg.d/smartarmstack_cc_by_nc.gpg >/dev/null
RUN sudo curl -s --compressed -o /etc/apt/sources.list.d/smartarmstack_cc_by_nc.list \
"https://marinholab.github.io/sas_debian_builder_noncommercial/smartarmstack_cc_by_nc.list"
RUN sudo apt update
RUN sudo apt-get install -y ros-jazzy-sas-*

RUN sudo apt-get update && sudo apt-get upgrade -y
RUN python3 -m pip install --upgrade dqrobotics --break-system-packages
RUN mkdir -p /root/sas_ur_control_template_devel/src
COPY . /root/sas_ur_control_template_devel/src/sas_ur_control_template
WORKDIR /root/sas_ur_control_template_devel
RUN colcon build
RUN echo "source /root/sas_ur_control_template_devel/install/setup.bash" > /etc/bash_env