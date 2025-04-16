from fastapi import APIRouter
from models.users import User
from controllers import users, security, actors

app = APIRouter()

@app.post("/api/adduser/")
async def addUser(user: User):
    if users.addUser(user.email, user.username, user.password):
        actors.addInternalActor(user.email, user.username, user.displayName)
        return {"Registre":"Valid"}
    else:
        return {"registre":"Error"}
    
@app.post("/api/login/")
async def login(user: User):
    if users.validUser(user.email, user.password) == True:
        return {"Token": security.randomToken()} 
    else:
        return {"Token": ""}