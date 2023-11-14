from fastapi.testclient import TestClient
from src.main import app
import pytest

client = TestClient(app)

# Unit test correctly input name to /hello endpoint
def test_name():
    response = client.get("/hello?name=John Luc Picard")
    assert response.status_code == 200
    assert response.json() == {"message":"Hello, John Luc Picard"}

# Unit test for incorrectly input name (i.e no input name)
def test_incorrect_name():
    response = client.get("/hello")
    assert response.status_code == 422
    assert response.json().get('detail')[0].get('msg') == 'Field required'

# Unit test for inputting numbers into name
def test_invalid_interger_name():
    name = "98765"
    response = client.get(f"/hello?name={name}") 
    assert response.status_code == 200
    assert response.json() == {"message": f"Hello, {name}"}

# Unit test for empty name input
def test_empty_name():
    name = ''
    response = client.get(f"/hello?name={name}")
    assert response.status_code == 200
    assert response.json() == {"message": f"Hello, {name}"}

#Unit test for mamesa = name
def test_wrong_name_order():
    response = client.get("/hello?mamesa=name")
    assert response.status_code == 422
    # assert response.json() == {"detail": "Please specify name correctly"} 

# Unit test the root endpoint /
def test_root():
    response = client.get("/")
    assert response.status_code == 404
    
# Unit test the default endpoints of /docs and /json
def test_doc():
    response = client.get("/docs")
    assert response.status_code == 200
    
# Unit for the json endpoint
def test_json():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    
# Unit test for health status 
def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert "time" in response.json()
    
# Unit test for correctly input data
def test_correctly_input_data():
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
def test_zero_value_input_data():
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
def test_negative_value_HouseAge():
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
def test_negative_value_input_data():
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
def test_missing_HouseAge():
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
def test_extra_feature_input_data():
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
def test_multiple_house_input_data():
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
