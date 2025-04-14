from fastapi import FastAPI
from database import connection

app = FastAPI()

@app.get("/")
async def root():
    connection.conn
