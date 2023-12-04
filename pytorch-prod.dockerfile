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