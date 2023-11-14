cd lab3

echo "1. Start up Minikube..."
minikube start --kubernetes-version=v1.27.3

echo "2. Setup docker daemon to built with Minikube"
eval $(minikube docker-env)

poetry install 

echo "Running pytest.."
poetry run pytest -vv

echo "3. Ensure API model is trained..."
if [ -e "./model_pipeline.pkl" ]; then
    echo " Model is available."
else
    echo "Training Model..."
    python ./trainer/trainer.py
fi

echo "4. Building the docker container..."
docker build -t my-api .

echo "5. Applying w255 name space."
kubectl apply -f infra/namespace.yaml
kubectl config set-context --current --namespace=w255

echo "6. Apply Deployments and Services:"
kubectl apply -f infra/deployment-redis.yaml
kubectl apply -f infra/deployment-pythonapi.yaml
kubectl apply -f infra/service-prediction.yaml
kubectl apply -f infra/service-redis.yaml

kubectl get pods -n w255
kubectl get svc -n w255

echo "7. Wait for your API to be accessible"
kubectl rollout status deployment/deployment-python-api -w

echo "8. Forwarding the local port to access the service endpoint"
kubectl port-forward -n w255 service/apps-deployment-service 8000:8000 &
PID=$!

echo "9. Wait for the /health endpoint to return a 200 and then move on"
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

echo "10. Test cases for different endpoints..."

echo "Test 1: testing '/hello' endpoint with ?name=Mamesa"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/hello?name=Mamesa"

echo "Test 2: testing '/hello' endpoint with ?name=John Luc Picard"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/hello?name=John-Luc-Picard"

echo "Test 3: testing '/hello' endpoint with no input"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/hello?"

echo "Test 4: testing '/hello' endpoint with empty space"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/hello?name=%20"

echo "Test 5: testing '/hello' endpoint with numeric input"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/hello?name=9821321"

echo "Test 6: testing '/hello' endpoint mamesa=name input"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/hello?mamesa=name"

echo "Test 7: testing '/' endpoint"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/"

echo "Test 8: testing '/docs' endpoint"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/docs"

# echo "Test 16: testing '/openapi.json' endpoint and return json format text"
# curl -s -w "%{http_code}\n" -X GET "http://localhost:8000/openapi.json"

echo "Test 9: testing the health endpoint"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/health"

echo "Test 10: testing '/predict' endpoint with correct data input"
curl -s -w "%{http_code}\n" -X POST "http://127.0.0.1:8000/predict" -H "Content-Type: application/json" -d '{"MedInc": 8.3252, "HouseAge": 41.0, "AveRooms": 5, "AveBedrms": 1.02380952, "Population": 322.0, "AveOccup": 2.55555556, "Latitude": 37.88, "Longitude": -122.23}'; echo


echo "Test 11: testing '/predict' endpoint with negative value for AveRooms"
curl -s -w "%{http_code}\n" -X POST "http://127.0.0.1:8000/predict" -H "Content-Type: application/json" -d '{"MedInc": 8.3252, "HouseAge": 41.0, "AveRooms": -1, "AveBedrms": 1.02380952, "Population": 322.0, "AveOccup": 2.55555556, "Latitude": 37.88, "Longitude": -122.23}'; echo

echo "Test 12: testing '/predict' endpoint with an empty input in AveRooms"
curl -o /dev/null -s -w "%{http_code}\n" -X POST "http://127.0.0.1:8000/predict" -H "Content-Type: application/json" -d '{"MedInc": 8.3252, "HouseAge": 41.0, "AveRooms":, "AveBedrms": 1.02380952, "Population": 322.0, "AveOccup": 2.55555556, "Latitude": 37.88, "Longitude": -122.23}'; echo


echo "Test 13: testing the /bulk_predict endpoint with correct input"
curl -X POST "http://127.0.0.1:8000/bulk_predict" \
-H "Content-Type: application/json" \
-d '{
    "houses": [
        {
            "MedInc": 8.3252,
            "HouseAge": 41.0,
            "AveRooms": 6.98412698,
            "AveBedrms": 1.02380952,
            "Population": 322.0,
            "AveOccup": 2.55555556,
            "Latitude": 37.88,
            "Longitude": -122.23
        },
        {
            "MedInc": 8.3252,
            "HouseAge": 41.0,
            "AveRooms": 6.98412698,
            "AveBedrms": 1.02380952,
            "Population": 322.0,
            "AveOccup": 2.55555556,
            "Latitude": 37.88,
            "Longitude": -122.23
        }
    ]
}'

kill ${PID}

kubectl delete -f infra/deployment-pythonapi.yaml
kubectl delete -f infra/deployment-redis.yaml
kubectl delete -f infra/service-prediction.yaml
kubectl delete -f infra/service-redis.yaml

docker rmi -f my-api

minikube stop
minikube delete

# docker rmi $(docker images -f "reference=gcr.io/k8s-minikube/*" -q)

cd ..
