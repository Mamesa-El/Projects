from fastapi import FastAPI, HTTPException
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis
import joblib
from typing import List
from pydantic import BaseModel, field_validator
from datetime import datetime
import numpy as np
import os

app = FastAPI()

redis_host = os.environ.get("REDIS_HOST", "redis-service")
@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(f"redis://{redis_host}")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

@app.get("/hello")
async def hello(name: str):
    return {"message": f"Hello, {name}"}

@app.get("/")
async def root():
    raise HTTPException(status_code=404, detail="Not Found")

@app.get("/health")
async def health():
    time = datetime.utcnow().isoformat()
    return {"time": time}

class HouseRecord(BaseModel):
    MedInc: float
    HouseAge: float
    AveRooms: float
    AveBedrms: float
    Population: float
    AveOccup: float
    Latitude: float
    Longitude: float

    @field_validator("AveRooms")
    def validate_ave_rooms(cls, v):
        if v <= 0:
            raise ValueError("Average rooms must be greater than 0")
        return v

    @field_validator("HouseAge")
    def validate_house_age(cls, v):
        if v <= 0:
            raise ValueError("HouseAge must be greater than 0")
        return v

class HousePrediction(BaseModel):
    prediction: float

class HouseBulkInput(BaseModel):
    houses: list[HouseRecord]

class HouseBulkPrediction(BaseModel):
    bulk_prediction: list[float]

model_path = "model_pipeline.pkl"
model = joblib.load(model_path)

@app.post("/predict", response_model=HousePrediction)
@cache(expire = 30)
async def predict_house_value(input_data: HouseRecord):
    inputs_list = list(input_data.model_dump().values())
    prediction = model.predict([inputs_list])[0]
    return {"prediction": prediction}

@app.post("/bulk_predict", response_model=HouseBulkPrediction)
@cache(expire=30)
async def predict_house_bulk_value(input_data: HouseBulkInput):
    inputs_list = [list(record.model_dump().values()) for record in input_data.houses]
    inputs_array = np.array(inputs_list)
    predictions = model.predict(inputs_array).tolist()
    return {"bulk_prediction": predictions}
