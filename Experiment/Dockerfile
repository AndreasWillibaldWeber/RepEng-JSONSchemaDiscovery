# LTS Ubuntu version
FROM ubuntu:22.04

# preconfigure enironment variables for the container
ENV DEBIAN_FRONTEND noninteractive
ENV LANG="C.UTF-8"
ENV LC_ALL="C.UTF-8"
ENV PYTHON=/usr/bin/python3

# install necessary software
RUN apt update && apt install -y \
    ca-certificates \
    wget \
    git \
    jq \
    python3 \
    python3-pip \
    make \
    texlive-base \
    texlive-bibtex-extra \
    texlive-fonts-recommended \
    texlive-fonts-extra \
    texlive-latex-extra \
    texlive-publishers

# create folders
RUN mkdir -p /experiment /tools

# download and install the mongodb tools
WORKDIR /tools
RUN wget https://fastdl.mongodb.org/tools/db/mongodb-database-tools-ubuntu2204-x86_64-100.6.1.deb
RUN apt install -y ./mongodb-database-tools-ubuntu2204-x86_64-100.6.1.deb

# clone and rename the report repository
WORKDIR /
RUN git clone https://github.com/AndreasWillibaldWeber/Report-RepEng-JSONSchemaDiscovery
RUN mv /Report-RepEng-JSONSchemaDiscovery /report

# switch folder
WORKDIR /experiment

# copy the data sets into the container
COPY datasets /datasets

# copy the experiment, script and make files into the container
COPY experiment.py /experiment
COPY smoke.sh /experiment
COPY restore.sh /experiment
COPY Makefile /report

# make scripts executable
RUN chmod +x restore.sh
RUN chmod +x smoke.sh

# install experiment requirements
RUN pip3 install requests rich

# run smoke test
RUN ./smoke.sh
