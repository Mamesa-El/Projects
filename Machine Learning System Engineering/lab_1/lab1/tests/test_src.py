from fastapi.testclient import TestClient
from src.main import app
import json

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

def test_json():
    response = client.get("/openapi.json")
    assert response.status_code == 200
