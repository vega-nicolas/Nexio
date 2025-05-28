from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from api import users
from models.post import Post as ModelPost
from controllers import post, tokens

app = APIRouter()

@app.post("/api/post/")
async def addPost(modelPost: ModelPost, token: str = Depends(users.oauth2)):
    if tokens.validToken(token):
        if post.addPost(modelPost.text, token):
            return JSONResponse(status_code=status.HTTP_201_CREATED, content= {"Post": "Added"})
        else:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"Post": "Error"})    
    else:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"Post": "Error"})
    
@app.get("/api/getpost/{page}/")
async def getAllPosts(page: int):
    allPost = post.getAllPosts(page)
    if allPost != None:
        return allPost
    else:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"Post": "Error"})


@app.delete("/api/post/{id}/")
async def deletePost(id: int, token: str = Depends(users.oauth2)):
    if tokens.validToken(token):
        if post.deletePost(id, token):
            return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content= {"Post":"Deleted"})
        else:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"Post": "Error"})
    else:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"Post": "Error"})
    
@app.patch("/api/post/{id}/")
async def editPost(modelPost: ModelPost, id: int, token: str = Depends(users.oauth2)):
    if tokens.validToken(token):
        if post.editPost(modelPost.text, id, token):
            return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content= {"Post":"Edited"})
        else:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"Post": "Error"})
    else:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"Post": "Error"})