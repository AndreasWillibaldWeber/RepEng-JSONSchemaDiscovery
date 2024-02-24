# slim LTS version of bookworm with node 18.x.x preconfigured
FROM node:18-bookworm-slim

# preconfigure enironment variables for the container
ENV DEBIAN_FRONTEND noninteractive
ENV LANG="C.UTF-8"
ENV LC_ALL="C.UTF-8"
ENV PYTHON=/usr/bin/python3

# install necessary software
RUN apt update && apt install -y \
    ca-certificates \
    git \
    g++ \
    python3 \
    python3-pip \
    make

# select workdir and user
WORKDIR /app
USER root

# install angular/cli and typescript for global use
RUN npm install -g @angular/cli
RUN npm install -g typescript

# create folder and clone the JSONSchemaDiscovery project from GitHub
RUN cd /app
RUN git clone https://github.com/feekosta/JSONSchemaDiscovery/

# change working directory and checkout the version used for the replication
WORKDIR /app/JSONSchemaDiscovery
RUN git checkout tags/1.1.0

# apply patch to fix npm run dev command
COPY package-json.patch .
RUN git apply package-json.patch

# install all project dependencies 
RUN npm install

# copy the start script and execute it to start the project
WORKDIR /app
COPY entrypoint.sh /app
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]