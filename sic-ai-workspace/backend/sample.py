# pip install fastapi uvicorn requests 
from fastapi import FastAPI

# create an object of FastAPI class
app = FastAPI()
print("FastAPI app created successfully.")
@app.get("/")
def read_root():
    return {"message": "Hello good morning, G 38 group welcome to FAST API"}