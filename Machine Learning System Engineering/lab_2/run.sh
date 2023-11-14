#!/bin/bash

cd lab2
# Run pytest within poetry virtualenv
poetry env remove python3.11
poetry install

# stop and remove image in case this script was run before
docker stop apiContainer
docker rm apiContainer

echo "Training the model..."
poetry run python trainer/train.py

echo "Moving model artifacts to api source directory..."
mv model_pipeline.pkl ./src/

echo "Running the test cases..."
poetry run pytest -vv -s

docker build -t my-api .

docker run -d -p 8000:8000 --name apiContainer my-api

# wait for the /health endpoint to return a 200 and then move on
finished=false
while ! $finished; do
    health_status=$(curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/health")
    if [ $health_status == "200" ]; then
        finished=true
        echo "API is ready"
    else
        echo "API not responding yet"
        sleep 1
    fi
done

echo "Test 1: testing '/predict' endpoint with correct data input"
curl -s -w "%{http_code}\n" -X POST "http://127.0.0.1:8000/predict" -H "Content-Type: application/json" -d '{"MedInc": 8.3252, "HouseAge": 41.0, "AveRooms": 5, "AveBedrms": 1.02380952, "Population": 322.0, "AveOccup": 2.55555556, "Latitude": 37.88, "Longitude": -122.23}'; echo

echo "Test 2: testing '/predict' endpoint with negative value for AveRooms"
curl -s -w "%{http_code}\n" -X POST "http://127.0.0.1:8000/predict" -H "Content-Type: application/json" -d '{"MedInc": 8.3252, "HouseAge": 41.0, "AveRooms": -1, "AveBedrms": 1.02380952, "Population": 322.0, "AveOccup": 2.55555556, "Latitude": 37.88, "Longitude": -122.23}'; echo

echo "Test 3: testing '/predict' endpoint with an empty input in AveRooms"
curl -o /dev/null -s -w "%{http_code}\n" -X POST "http://127.0.0.1:8000/predict" -H "Content-Type: application/json" -d '{"MedInc": 8.3252, "HouseAge": 41.0, "AveRooms":, "AveBedrms": 1.02380952, "Population": 322.0, "AveOccup": 2.55555556, "Latitude": 37.88, "Longitude": -122.23}'; echo

echo "Test 4: testing '/predict' endpoint with a negative input in HouseAge"
curl -o /dev/null -s -w "%{http_code}\n" -X POST "http://127.0.0.1:8000/predict" -H "Content-Type: application/json" -d '{"MedInc": 8.3252, "HouseAge": -5, "AveRooms"10:, "AveBedrms": 1.02380952, "Population": 322.0, "AveOccup": 2.55555556, "Latitude": 37.88, "Longitude": -122.23}'; echo

echo "Test 5: testing '/predict' endpoint with a negative input in HouseAge"
curl -o /dev/null -s -w "%{http_code}\n" -X POST "http://127.0.0.1:8000/predict" -H "Content-Type: application/json" -d '{"MedInc": 8.3252, "HouseAge": -5, "AveRooms"10:, "AveBedrms": 1.02380952, "Population": 322.0, "AveOccup": 2.55555556, "Latitude": 37.88, "Longitude": -122.23}'; echo

echo "Test 6: testing '/predict' endpoint with a missing HouseAge feature"
curl -o /dev/null -s -w "%{http_code}\n" -X POST "http://127.0.0.1:8000/predict" -H "Content-Type: application/json" -d '{"MedInc": 8.3252, "AveRooms"10:, "AveBedrms": 1.02380952, "Population": 322.0, "AveOccup": 2.55555556, "Latitude": 37.88, "Longitude": -122.23}'; echo

echo "Test 7: testing '/predict' endpoint with an extra input feautre"
curl -o /dev/null -s -w "%{http_code}\n" -X POST "http://127.0.0.1:8000/predict" -H "Content-Type: application/json" -d '{"MedInc": 8.3252, "HouseAge": -5, "AveRooms"10:, "AveBedrms": 1.02380952, "Population": 322.0, "AveOccup": 2.55555556, "Latitude": 37.88, "Longitude": -122.23, "dimension": 12}'; echo

echo "Test 8: testing '/hello' endpoint with ?name=Mamesa"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/hello?name=Mamesa"

echo "Test 9: testing '/hello' endpoint with ?name=John Luc Picard"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/hello?name=John-Luc-Picard"

echo "Test 10: testing '/hello' endpoint with no input"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/hello?"

echo "Test 11: testing '/hello' endpoint with empty space"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/hello?name=%20"

echo "Test 12: testing '/hello' endpoint with numeric input"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/hello?name=9821321"

echo "Test 13: testing '/hello' endpoint mamesa=name input"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/hello?mamesa=name"

echo "Test 14: testing '/' endpoint"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/"

echo "Test 15: testing '/docs' endpoint"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/docs"

echo "Test 16: testing '/openapi.json' endpoint and return json format text"
curl -s -w "%{http_code}\n" -X GET "http://localhost:8000/openapi.json"

echo "Test 17: testing the health endpoint"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/health"

docker stop apiContainer

docker rm apiContainer

docker image rm my-api


