from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from models.users import User
from controllers import users, actors, security

app = APIRouter()

@app.post("/api/adduser/")
async def addUser(user: User):
    if users.addUser(user.email, user.username, user.password):
        actors.addInternalActor(user.email, user.username, user.displayName)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"Registre":"Valid"})
    else:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"Registre":"Error"})
    
@app.post("/api/login/")
async def login(user: User):
    if users.validUser(user.email, user.password) == True:
        return {"Token": security.randomToken()} 
    else:
        return {"Token": ""}