from database import posts, tokens
from typing import List
from models.post import Post

def addPost(text: str, token: str, ) -> bool:
    if token == None:
        return False
    elif token == "":
        return False
    elif text == None:
        return False
    elif text == "":
        return False
    elif not posts.addPost(tokens.getUserId(token), text):
        return False
    else:
        return True
    
def getAllPosts(page: int) -> List[Post]:
    if page != None:
        output = [
        Post(
            id=output[0],
            user_id=output[1],
            preferred_username=output[2],
            display_name=output[3],
            text=output[4],
            url=output[5],
            created_at=output[6],
            likes=output[7],
            comments=output[8],
            shares=output[9]
        )
        for output in posts.getAllPosts(page)
    ]
        return output
    else:
        return None
    
def deletePost(post_id: int, token: str) -> bool:
    if post_id > 0:
        return posts.deletePost(post_id, tokens.getUserId(token))
    else:
        return False
    
def editPost(edit: str, post_id: int, token: str) -> bool:
    if edit == None:
        return False
    elif edit == "":
        return False
    elif token  == None:
        return False
    elif token == "":
        return False
    elif post_id == None:
        return False
    elif not post_id > 0:
        return False
    else:
       return posts.editPost(edit, post_id, tokens.getUserId(token))