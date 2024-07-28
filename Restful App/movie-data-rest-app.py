"""
REST API Application for querying
movie data set
"""
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"Hello":"World"}