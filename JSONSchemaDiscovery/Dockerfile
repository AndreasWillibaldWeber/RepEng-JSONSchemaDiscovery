# slim LTS version of bookworm with node 18.x.x preconfigured
FROM node:18-bookworm-slim

# select workdir and user
WORKDIR /app
USER root

# install angular/cli and typescript for global use
RUN npm install -g @angular/cli
RUN npm install -g typescript

# create folder and clone the JSONSchemaDiscovery project from GitHub
RUN cd /app
RUN git clone https://github.com/feekosta/JSONSchemaDiscovery/

# install all project dependencies 
RUN cd JSONSchemaDiscovery; npm install

# copy the start script and execute it to start the project
COPY entrypoint.sh /app
RUN cd /app
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"] 