from fastapi import FastAPI, HTTPException
import joblib
from typing import List
from pydantic import BaseModel, field_validator
from datetime import datetime
import math
import numpy as np

app = FastAPI()

# Creating a /hello endpoint and send out HTTP status code
@app.get("/hello")
async def hello(name: str):
    return {"message": f"Hello, {name}"}

# # Creating / endpoint, return Not Found to the requester
@app.get("/")
async def root():
    raise HTTPException(status_code=404, detail="Not Found")

# Pandantic Model input features
class HouseRecord(BaseModel):
    MedInc: float
    HouseAge: float
    AveRooms: float
    AveBedrms: float
    Population: float
    AveOccup: float
    Latitude: float
    Longitude: float
    
    # Validator function for AveRooms
    @field_validator("AveRooms")
    def validate_ave_rooms(cls, v):
        if v <= 0:
            raise ValueError("Average rooms must be greater than 0")
        return v
    # Validator function for HouseAge   
    @field_validator("HouseAge")
    def validate_house_age(cls, v):
        if v <= 0:
            raise ValueError("HouseAge must be greater than 0")
        return v
# Pydantic Model for output values
class HousePrediction(BaseModel):
    prediction: float

# Load the model:
model_path = "src/model_pipeline.pkl"
model = joblib.load(model_path)

# Predict endpoint
@app.post("/predict", response_model=HousePrediction)
async def predict_house_value(input_data: HouseRecord):
    inputs_list = list(input_data.model_dump().values())
    prediction = model.predict([inputs_list])[0]
    return {"prediction": prediction}

# Health endpoint
@app.get("/health")
async def health():
    time = datetime.utcnow().isoformat()
    return {"time":time}
