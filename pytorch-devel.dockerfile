FROM nvcr.io/nvidia/pytorch:23.06-py3

# Set user specific environment variables
ENV USER root
ENV HOME /root
# Switch to user
USER ${USER}

RUN pip3 install --upgrade pip

RUN pip3 install \
    numpy

# jupyter notebook port
EXPOSE 8888

# Creating a user
ARG USERNAME=torch
ARG UID=1000

RUN adduser --no-create-home --gecos "" -u ${UID} ${USERNAME}
RUN adduser ${USERNAME} sudo
RUN passwd -d ${USERNAME}

RUN cp -rf /root /home/${USERNAME} && \
    chown -R ${USERNAME}:${USERNAME} /home/${USERNAME}


# Set up vnc
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    sudo \
    tigervnc-standalone-server \
    tigervnc-xorg-extension \
    tigervnc-viewer \
    xfce4 \
    xfce4-goodies \
    dbus-x11 \
    x11-xserver-utils

# Create a directory for vnc
RUN mkdir $HOME/.vnc
# Set default password
RUN echo password | vncpasswd -f > $HOME/.vnc/passwd
# Set vnc password file permissions
RUN chmod 600 $HOME/.vnc/passwd
# Create a custom xstartup file
# RUN echo "#!/bin/bash\nstartxfce4 &" > $HOME/.vnc/xstartup
# Make the xstartup file executable
# RUN chmod +x $HOME/.vnc/xstartup
RUN rm -rf /tmp/.X1-lock

RUN cp -rf /root/.vnc /home/${USERNAME} && \
    chown -R ${USERNAME}:${USERNAME} /home/${USERNAME}/.vnc

# Expose VNC port
EXPOSE 5901


# Start VNC server
ENTRYPOINT [ "/bin/bash", "-c", "vncserver :1 -depth 24 -localhost no && sleep 5 && tail -F $HOME/.vnc/*.log" ]