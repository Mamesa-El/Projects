#!/bin/bash

docker build -t cs-firstname-lastname-file-metadata:0.0.1 .

docker run --rm -v ${PWD}:/app cs-firstname-lastname-file-metadata:0.0.1

# sleep 2

docker image rm  cs-firstname-lastname-file-metadata:0.0.1