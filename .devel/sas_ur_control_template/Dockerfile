FROM murilomarinho/sas:jazzy
LABEL authors="murilomarinho"
SHELL ["/bin/bash", "-c"]
ENV BASH_ENV="/etc/bash_env"

RUN mkdir -p cd ~/sas_tutorial_workspace/src
RUN cd ~/sas_tutorial_workspace/src && git clone https://github.com/MarinhoLab/sas_ur_control_template.git
RUN cd ~/sas_tutorial_workspace/src/sas_ur_control_template/.devel/scripts && chmod +x setup_environment.sh
RUN cd ~/sas_tutorial_workspace/src/sas_ur_control_template/.devel/scripts && ./setup_environment.sh

