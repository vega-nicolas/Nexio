from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import HTTPException
from models.users import User
from controllers import users, actors, security, tokens

app = APIRouter()
oauth2 = OAuth2PasswordBearer("/api/login/")


@app.post("/api/adduser/")
async def addUser(user: User):
    if users.addUser(user.email, user.username, user.password):
        actors.addInternalActor(user.email, user.username, user.displayName)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"Registre": "Valid"})
    else:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"Registre": "Error"})

@app.post("/api/login/")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    if users.validUser(form.username, form.password):
        token = security.randomToken()
        if tokens.addToken(users.get_id(form.username), token):
            return JSONResponse(
                content={"access_token": token, "token_type": "bearer"},
                status_code=status.HTTP_200_OK
        )
    else:
        return JSONResponse(
            content={"success": False, "message": "Usuario o contraseña incorrectos."},
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    
@app.get("/api/validtoken/")
async def validtoken(token: str = Depends(oauth2)):
    if not tokens.validToken(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"message": "Acceso autorizado", "token": token}