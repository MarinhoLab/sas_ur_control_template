FROM murilomarinho/sas:jazzy
LABEL authors="murilomarinho"
SHELL ["/bin/bash", "-c"]
ENV BASH_ENV="/etc/bash_env"

RUN sudo apt-get update && sudo apt-get upgrade -y
RUN python3 -m pip install --upgrade dqrobotics --break-system-packages
RUN mkdir -p /root/sas_ur_control_template_devel/src/