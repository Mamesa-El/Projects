# Lab 2 Documentation
### What is the Application Does 
The application in the 'main.py' file provides a FastAPI service using uvicorn (as async webworker), featuring multiple endpoints. Pydantic function are used to verify the data type of the input and output for /predict endpoint. The three primary custom-made endpoints are '/hello', '/predict', and '/healthcheck'. 

+ **'/hello'** endpoint
    + **Input:** User's name.
    + **Output:** A greeting in the format "Hello, {name}", where {name} is the user's input.

* **'/predict'** endpoint: Predicts house prices in California using a pre-trained sklearn model 'model_pipeline.pkl'.
    + **Input:** Numerical values for features in JSON format, such as {"MedInc": 8.3252, "HouseAge": 41.0, "AveRooms": -1, "AveBedrms": 1.02380952, "Population": 322.0, "AveOccup": 2.55555556, "Latitude": 37.88, "Longitude": -122.23}.
    + **Output:** A house price prediction value. 

* **/health** endpoint
    + **input**: None required.
    + **output**: Return the current time in UTC format. 

### How to build the application
The application is constructed based on commands and information provided within the Dockerfile. This Dockerfile guides the creation of a Docker image using the command: ``docker build -t my-api .``, where ``my-api`` is the name of the docker image. 

### How to run the application
The application, encapsulated in a Docker container, can be initiated with a series of coomand inside run.sh. The shell script can be run form root directory as follow ``./run.sh``. The shell script provides commands to install proper poetry enviornment, train the model, and store the model artifacts to the ``src`` directory. Then the application is built using the code from the section above.

### How to test the application
The test_lab2.py file contains unit tests using FastAPI's TestClient. It tests various edge cases for inputs, like negative values or empty strings. Use the command ``poetry run pytest`` to execute all test cases in the test_lab2.py.

# Lab 2 Questions:
1. What does Pydantic handle for us?
    * Pydantic is used for data validation and settings management using Python type annotations. It checks and validates input values for predictions, raising a ValueError for any incorrectly inputted values that does not match the schema. This ensures that the model receives the correct input format and also provides a consistent output format.
2. What do Docker HEALTHCHECKs do?
    * The docker HEALTHCHECK return health status of the application periodically. This help ensure that the service running inside the container are running as expected. 
3. Describe what the Sequence Diagram below shows.
    * The user would post an input as a JSON format for prediction and a value error is raised if the value input does not statify pydantic schema. If the pydantic schema is satisfy then the value is input into the model for prediction. Then model would make a prediction, store the returned values, and return the values as the model output for the user. 
