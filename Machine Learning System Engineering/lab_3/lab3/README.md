# Lab 3 Documentation
### What your Application Does 
The application in the 'main.py' file provides a FastAPI service using uvicorn (as async webworker), featuring multiple endpoints. Pydantic models are employed to define and validate the structure of request and response bodies for the /predict and /bulk_predict endpoints. The application leverages Redis as a caching backend, ensuring efficient data retrieval for common queries and predictions. Below are the four primary custom made endpoints:

+ **'/hello'** endpoint
    + **Input:** User's name.
    + **Output:** A greeting in the format "Hello, {name}", where {name} is the user's input.

* **/health** endpoint
    + **input**: None required.
    + **output**: Return the current time in UTC format. 

* **'/predict'** endpoint: Predicts house prices in California using a pre-trained sklearn model 'model_pipeline.pkl'.
    + **Input:** Numerical values for features in JSON format. Below is the smaple format <br/> {"MedInc": 8.3252, "HouseAge": 41.0, "AveRooms": -1, "AveBedrms": 1.02380952, "Population": 322.0, "AveOccup": 2.55555556, "Latitude": 37.88, "Longitude": -122.23}.
    + **Output:** A house price prediction value. 

* **'/bulk_predict'** endpoint: Predicts the prices of multiple houses in California using a pre-trained sklearn model named 'model_pipeline.pkl'.
    + **Input:** A set of numerical values representing different houses and their respective features in JSON format. Below is a sample input format:<br/>
    {
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
                "MedInc": 18.3252,
                "HouseAge": 41.0,
                "AveRooms": 6.98412698,
                "AveBedrms": 1.02380952,
                "Population": 322.0,
                "AveOccup": 2.55555556,
                "Latitude": 37.88,
                "Longitude": -122.23
            }, ...]
    }
    + **Output:** A list containing predicted prices for the provided houses.

### How to build the application
The application is constructed based on commands and information provided within the Dockerfile. This Dockerfile guides the creation of a Docker image using the command: ``docker build -t my-api .``, where ``my-api`` is the name of the docker image. Once the docker image is built, can we use the Kubenete commands below to create namename, deployment, and service:

```bash
kubectl apply -f infra/namespace.yaml
kubectl config set-context --current --namespace=w255

kubectl get pods -n w255
kubectl get svc -n w255

kubectl apply -f infra/deployment-redis.yaml
kubectl apply -f infra/deployment-pythonapi.yaml
kubectl apply -f infra/service-prediction.yaml
kubectl apply -f infra/service-redis.yaml
```

<br/>
<br/>

*Model Training:* Before building the Docker image, ensure that the machine learning model is trained and the model artifact, model_pipeline.pkl, exists within the ./lab3 directory. If the model is not present, be sure to train the model and save it to the said directory.

### How to run the application
The application is encapsulated within a Docker container and is seamlessly managed via Kubernetes using Minikube. To initiate the application, simply execute the run.sh shell script from the lab3 root directory using the ``./run.sh`` command. <br/><br/>
Note: This script streamlines several operations: it starts Minikube, sets up the required Poetry environment, checks for the presence of a pre-trained model in the lab_3 directory (training it if absent), and then stores the model artifacts in the lab3 directory. Additionally, the script configures Docker to function within Minikube's environment, setup/configured w255 namespace, and leverages Kubernetes to adeptly deploy and oversee the application and its linked services.

### How to test the application
The test_lab3.py file contains unit tests using FastAPI's TestClient. The tests cover various edge cases for inputs, ranging from negative values or empty strings. Use the command ``poetry run pytest`` to execute all test cases in the test_lab3.py. The test also employ FastAPI's caching that utilize the InMemoryBackend for temporary data storage during the execution of each test case. This negate the need for external caching system like Redis.

# Lab 3 Questions:
1. What are the benefits of caching?<br/>
Caching reduces data retrieval times and computational load by serving frequently requested data without the need for repeated computations. This leads to enhanced performance, faster response times, and cost savings.

2. What is the difference between Docker and Kubernetes?<br/>
Docker packages applications into consistent, isolated containers. Kubernetes is an orchestration tool that manages and scales these containerized applications across clusters of machines. While Docker focuses on running containers, Kubernetes handles their distribution and scaling.

3. What does a kubernetes deployment do?<br/>
A Kubernetes Deployment manages the creation and scaling of pods, specifying the container image to use and desired state. It handles the rollout of updated code, can roll back to earlier versions, and offers features to effectively manage the lifecycle of pods. <Replica pods.>

4. What does a kubernetes service do?<br/>
A Kubernetes Service exposes applications in pods to network traffic, maintaining consistent IP and DNS names regardless of pod changes. It provides load balancing and service discovery by distributing traffic across matching pods based on selector criteria. This ensures uninterrupted access even during application updates or rollbacks.