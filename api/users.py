from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models.users import User
from controllers import users, actors, security

app = APIRouter()
oauth2 = OAuth2PasswordBearer("/api/validuser/")

@app.post("/api/adduser/")
async def addUser(user: User):
    if users.addUser(user.email, user.username, user.password):
        actors.addInternalActor(user.email, user.username, user.displayName)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"Registre": "Valid"})
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"Registre": "Error"})

@app.post("/api/validuser/")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    if users.validUser(form.username, form.password):
        return JSONResponse(
            status_code=status.HTTP_202_ACCEPTED,
            content={"access_token": security.randomToken(), "token_type": "bearer"}
        )
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"access_token": None}
    )