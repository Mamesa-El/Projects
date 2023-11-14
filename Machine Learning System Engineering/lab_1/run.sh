#!/bin/bash

set -e

docker build -t my-api ./lab1

docker run -d -p 8000:8000 --name apiContainer my-api

sleep 5

echo "testing '/hello' endpoint with ?name=Mamesa"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/hello?name=Mamesa"

echo "testing '/hello' endpoint with ?name=John Luc Picard"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/hello?name=John-Luc-Picard"

echo "testing '/hello' endpoint with no input"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/hello?"

echo "testing '/hello' endpoint with empty space"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/hello?name=%20"

echo "testing '/hello' endpoint with numeric input"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/hello?name=9821321"

echo "testing '/hello' endpoint mamesa=name input"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/hello?mamesa=name"

echo "testing '/' endpoint"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/"

echo "testing '/docs' endpoint"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/docs"

echo "testing '/openapi.json' endpoint and return json format text"
curl -s -w "%{http_code}\n" -X GET "http://localhost:8000/openapi.json"

sleep 5

docker stop apiContainer

docker rm apiContainer

docker image rm my-api