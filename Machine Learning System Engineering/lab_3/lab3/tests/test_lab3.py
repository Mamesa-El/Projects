import pytest
from lab3.main import app
from fastapi.testclient import TestClient
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache import FastAPICache

@pytest.fixture
def client():
    FastAPICache.init(InMemoryBackend())
    with TestClient(app) as c:
        yield c

# Unit test correctly input name to /hello endpoint
def test_name(client):
    response = client.get("/hello?name=John Luc Picard")
    assert response.status_code == 200
    assert response.json() == {"message":"Hello, John Luc Picard"}

# Unit test for incorrectly input name (i.e no input name)
def test_incorrect_name(client):
    response = client.get("/hello")
    assert response.status_code == 422
    assert response.json().get('detail')[0].get('msg') == 'Field required'

# Unit test for inputting numbers into name
def test_invalid_interger_name(client):
    name = "98765"
    response = client.get(f"/hello?name={name}") 
    assert response.status_code == 200
    assert response.json() == {"message": f"Hello, {name}"}

# Unit test for empty name input
def test_empty_name(client):
    name = ''
    response = client.get(f"/hello?name={name}")
    assert response.status_code == 200
    assert response.json() == {"message": f"Hello, {name}"}

#Unit test for mamesa = name
def test_wrong_name_order(client):
    response = client.get("/hello?mamesa=name")
    assert response.status_code == 422
    # assert response.json() == {"detail": "Please specify name correctly"} 

# Unit test the root endpoint /
def test_root(client):
    response = client.get("/")
    assert response.status_code == 404
    
# Unit test the default endpoints of /docs and /json
def test_doc(client):
    response = client.get("/docs")
    assert response.status_code == 200
    
# Unit for the json endpoint
def test_json(client):
    response = client.get("/openapi.json")
    assert response.status_code == 200
    
# Unit test for health status 
def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert "time" in response.json()
    
# Unit test for correctly input data
def test_correctly_input_data(client):
    data = {
        "MedInc": 8.3252,
        "HouseAge": 15.0,
        "AveRooms": 5.0,
        "AveBedrms": 1.0,
        "Population": 300.0,
        "AveOccup": 1.5,
        "Latitude": 34.2,
        "Longitude": -118.5
    }
    
    response = client.post("/predict", json=data)
    
    assert response.status_code == 200
    assert "prediction" in response.json()

# Unit test for input value of 0 in the AveRoom
def test_zero_value_input_data(client):
    data = {
        "MedInc": -1.5,
        "HouseAge": 15.0,
        "AveRooms": 0.0,
        "AveBedrms": 1.0,
        "Population": 300.0,
        "AveOccup": 1.5,
        "Latitude": 34.2,
        "Longitude": -118.5
    }
    response = client.post("/predict", json=data)
    assert response.status_code == 422
    assert "detail" in response.json()

# Unit test for input value of 0 in the HouseAge
def test_negative_value_HouseAge(client):
    data = {
        "MedInc": -1.5,
        "HouseAge": -1,
        "AveRooms": 0.0,
        "AveBedrms": 1.0,
        "Population": 300.0,
        "AveOccup": 1.5,
        "Latitude": 34.2,
        "Longitude": -118.5
    }
    response = client.post("/predict", json=data)
    assert response.status_code == 422
    assert "detail" in response.json()

# Unit test for the negative input value in the AveRooms
def test_negative_value_input_data(client):
    data = {
        "MedInc": -1.5,
        "HouseAge": 15.0,
        "AveRooms": -9,
        "AveBedrms": 1.0,
        "Population": 300.0,
        "AveOccup": 1.5,
        "Latitude": 34.2,
        "Longitude": -118.5
    }
    response = client.post("/predict", json=data)
    assert response.status_code == 422
    assert "detail" in response.json()

#Unit test for a missing HouseAge feature
def test_missing_HouseAge(client):
    data = {
        "MedInc": -1.5,
        "AveRooms": -9,
        "AveBedrms": 1.0,
        "Population": 300.0,
        "AveOccup": 1.5,
        "Latitude": 34.2,
        "Longitude": -118.5
    }
    response = client.post("/predict", json=data)
    assert response.status_code == 422
    # assert "detail" in response.json()

# Unit test for have an extra feature
def test_extra_feature_input_data(client):
    data = {
        "MedInc": 8.3252,
        "HouseAge": 15.0,
        "AveRooms": 5.0,
        "AveBedrms": 1.0,
        "Population": 300.0,
        "AveOccup": 1.5,
        "Latitude": 34.2,
        "Longitude": -118.5,
        "newfeature": 100
    }
    
    response = client.post("/predict", json=data)
    assert response.status_code == 200
    # assert "prediction" in response.json()

# Unit test for having more than 1 housing dataset as an input
def test_multiple_house_input_data(client):
    data = [
        {
            "MedInc": 8.3252,
            "HouseAge": 15.0,
            "AveRooms": 5.0,
            "AveBedrms": 1.0,
            "Population": 300.0,
            "AveOccup": 1.5,
            "Latitude": 34.2,
            "Longitude": -118.5
        },
        {
            "MedInc": 7.0,
            "HouseAge": 20.0,
            "AveRooms": 6.0,
            "AveBedrms": 1.1,
            "Population": 400.0,
            "AveOccup": 2.0,
            "Latitude": 34.5,
            "Longitude": -118.7
        }
    ]
    response = client.post("/predict", json=data)
    assert response.status_code == 422

# Correctly Input Bulk Prediction Data
def test_bulk_prediction(client):
    data = {
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
            },
                        {
                "MedInc": 80.3252,
                "HouseAge": 41.0,
                "AveRooms": 9.98412698,
                "AveBedrms": 1.02380952,
                "Population": 322.0,
                "AveOccup": 2.55555556,
                "Latitude": 37.88,
                "Longitude": -122.23
            },
            {
                "MedInc": 81.3252,
                "HouseAge": 41.0,
                "AveRooms": 1.98412698,
                "AveBedrms": 1.02380952,
                "Population": 322.0,
                "AveOccup": 2.55555556,
                "Latitude": 37.88,
                "Longitude": -122.23
            }
        ]
    }
    response = client.post("/bulk_predict", json=data)
    assert response.status_code == 200

# Incorrectly Input Bulk Prediction Data with missing variable
def test_bulk_prediction(client):
    data = {
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
                "AveRooms": 6.98412698,
                "AveBedrms": 1.02380952,
                "Population": 322.0,
                "AveOccup": 2.55555556,
                "Latitude": 37.88,
                "Longitude": -122.23
            }
        ]
    }
    response = client.post("/bulk_predict", json=data)
    assert response.status_code == 422

