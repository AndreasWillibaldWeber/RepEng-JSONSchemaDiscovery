# RepEng-JSONSchemaDiscovery

Reproducibility Engineering - JSONSchemaDiscovery

## Description

This project provides the reproduction package for 
the JSONSchemaDiscovery.

## Setup the Project and download the dataset

1. clone the repository: ```https://github.com/AndreasWillibaldWeber/RepEng-JSONSchemaDiscovery```
2. download the data from: ```https://www.dropbox.com/sh/j0bxw52b6fj46pm/AACOu60zgbNG1nKhnseYZ8uHa?dl=0```
3. extract the data to the dataset folder (at least the files checkins.bson, tweets.bson, venues.bson)
4. ensure the path looks like ```dataset/foursquare/combined/<filename>.bson```

## Build the Docker Images and run the Docker Container

5. execute in the repository root folder: ```docker compose up --build```
6. use your browser to call: ```http://localhost:4200```
7. create an account, log in, and connect to the database to explore the tool manually.

## Run the Experiment and build the Report

8. use your favourite tool, e.g. VSCode, to attach to the experiment container via tty
9. execute ```./restore.sh``` to load the data into MongoDB
10. navigate to the experiment folder and use: ```python3 experiment.py -d <databasename> -c <collectionname> -o ../report/table.tex``` or use: ```./smoke.sh``` (at the moment it echos just a version number)
11. navigate to the report folder and use ```make``` to build the report

## Shut down the Docker Container

12. use **[STRG] + C** in the command line and then use: ```docker compose down```
