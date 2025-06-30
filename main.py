from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api import users, posts
import pages

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(users.app)
app.include_router(posts.app)
app.include_router(pages.app)