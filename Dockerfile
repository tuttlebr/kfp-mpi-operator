FROM ubuntu:20.04

# common environemnt variables in Kubeflow
ENV NB_USER jovyan
ENV NB_UID 1000
ENV NB_PREFIX /
ENV HOME /home/$NB_USER
ENV SHELL /bin/bash

# set shell to bash
SHELL ["/bin/bash", "-c"]

# install - usefull linux packages
RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get -yq update \
    && apt-get -yq install --no-install-recommends \
    apt-transport-https \
    bash \
    bzip2 \
    ca-certificates \
    curl \
    git \
    gnupg \
    gnupg2 \
    locales \
    lsb-release \
    nano \
    python3-pip \
    software-properties-common \
    tzdata \
    unzip \
    vim \
    wget \
    zip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# create user and set required ownership
RUN useradd -M -s /bin/bash -N -u ${NB_UID} ${NB_USER} \
    && mkdir -p ${HOME} \
    && chown -R ${NB_USER}:users ${HOME} \
    && chown -R ${NB_USER}:users /usr/local/bin

# set locale configs
RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
    && locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8
ENV LC_ALL en_US.UTF-8

# install - requirements.txt
COPY requirements.txt /tmp
RUN python3 -m pip install --upgrade -r /tmp/requirements.txt --quiet --no-cache-dir \
    && rm -f /tmp/requirements.txt

WORKDIR $HOME

USER $NB_USER