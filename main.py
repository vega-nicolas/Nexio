from fastapi import FastAPI, Request
from database import model
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from api import users


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="views")

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

model.genTabs()
app.include_router(users.app)