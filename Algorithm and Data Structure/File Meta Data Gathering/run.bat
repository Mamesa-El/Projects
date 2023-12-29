
@echo off
REM Build the Docker image
docker build -t cs-firstname-lastname-file-metadata:0.0.1 .

REM Run the Docker container
docker run --rm -v %CD%:/app cs-firstname-lastname-file-metadata:0.0.1

REM Sleep for 2 seconds is commented out, but here if you need it
REM timeout /t 2

@REM REM Remove the Docker image after running
docker image rm cs-firstname-lastname-file-metadata:0.0.1
