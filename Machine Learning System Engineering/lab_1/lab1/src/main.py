from fastapi import FastAPI, HTTPException

app = FastAPI()

# Creating a /hello endpoint and send out HTTP status code
@app.get("/hello")
async def hello(name: str):
    return {"message": f"Hello, {name}"}

# # Creating / endpoint, return Not Found to the requester
@app.get("/")
async def root():
    raise HTTPException(status_code=404, detail="Not Found")
