# sparkyShinyIndianaJones

This repository contains MVP solution for tracking the flow of historical artifacts using open data sources.

# Overview

During the development of our projects we worked on following topics:
 - data collection from different sources(wikidata, official museum sites)
 - modelling ML model which from text about concrete historical artifact extracts movements(logical pairs date:location) of it through history
 - packaging the best model to pass it to Spark
 - running it through all of the collected data using pySpark
 - developing of utils which map written date to year and written name of location to latitude and longitude
 - visualizing entities transition via R Shiny technology

# Navigation

Each part of our system is separated to different folder. The report is written in README files for each folder

# Requirements to run
  To run every part of our project you should have Python 3.6.* and R developing tools installed.
  <br>
  Full python environment description can be found in environment.yaml file
  <br>
  For R part you need following libraries:
  - shiny
  - leaflet
  - RColorBrewer
  - ggplot2
  - dplyr
    
# Summary
We developed fully-functional system which does what we declared in our initial report. 
On each layer of the application a lot of improvements can be integrated. 
Our MVP can become cool open-source project.
