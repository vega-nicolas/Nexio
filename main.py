from fastapi import FastAPI
from database import connection, model
app = FastAPI()

@app.get("/")
async def root():
    return "hello"
