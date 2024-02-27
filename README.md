# RepEng-JSONSchemaDiscovery

Reproducibility Engineering - JSONSchemaDiscovery

## Description

This project provides the reproduction package for 
the JSONSchemaDiscovery.

## Setup the Project and download the dataset

1. clone the repository: ```https://github.com/AndreasWillibaldWeber/RepEng-JSONSchemaDiscovery```
2. download the data from: ```https://www.dropbox.com/sh/j0bxw52b6fj46pm/AACOu60zgbNG1nKhnseYZ8uHa?dl=0```
3. extract the data to the dataset folder (at least the files checkins.bson, tweets.bson, venues.bson)
4. ensure the path looks like ```/Experiment/dataset/foursquare/combined/<filename>.bson```

## Build the Docker Images and run the Docker Container

5. execute in the repository root folder: ```docker compose up --build```
6. use ```./smoke.sh``` to run smoke tests
7. use your browser to call: ```http://localhost:4200```
8. create an account, log in, and connect to the database to explore the tool manually

## Run the Experiment and build the Report automatically

9. execute ```./doall.sh``` to run the experiment (usable flags: -r, --omit-restore, -s, --smoke, -h, --help)

## Run the Experiment and build the Report manually

10. use your favourite tool, e.g. VSCode, to attach to the experiment container via tty
13. to get information about the system environment execute ```/system_information/collect_system_information.sh```
12. execute ```./restore.sh``` to load the data into MongoDB
13. navigate to the experiment folder and use: ```python3 experiment.py -d <databasename> -c <collectionname> -o ../report/table_result_data.tex```
14. navigate to the report folder and use ```make``` to build the report

## Shut down the Docker Container

13. use **[STRG] + C** in the command line and then use: ```docker compose down```

## Report

1. clone the repository: https://github.com/AndreasWillibaldWeber/Report-RepEng-JSONSchemaDiscovery
2. read the README.md of the repository

## Original Work

[1] Sam Anzaroot, Alexandre Passos, David Belanger, and Andrew McCallum. 2017.
    JSONSchemaDiscovery. https://github.com/gbd-ufsc/JSONSchemaDiscovery.git.

[3] Angelo Augusto Frozza, Ronaldo dos Santos Mello, and Felipe de Souza da Costa.
    2018. An Approach for Schema Extraction of JSON and Extended JSON Document Collections.
    In 2018 IEEE International Conference on Information Reuse and
    Integration (IRI). 356–363. https://doi.org/10.1109/IRI.2018.00060.

### Software Artefacts

* https://github.com/gbd-ufsc/JSONSchemaDiscovery
* https://github.com/feekosta/JSONSchemaDiscovery

### Data Sets

[2] Emre Çelikten, Géraud Le Falher, and Michael Mathioudakis. 2016. Modeling
urban behavior by mining geotagged social data. IEEE transactions on Big Data 3,
2 (2016), 220–233.
