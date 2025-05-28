from database import tokens

def addToken(user_id: int, token: str) -> bool:
    if user_id == None:
        return False
    elif user_id == "":
        return False
    elif token == None:
        return False
    elif token == "":
        return False
    elif not tokens.addToken(user_id, token):
        return False
    else:
        return True
    


def validToken(token: str) -> bool:
    if token == None:
        return False
    elif token == "":
        return False
    elif not tokens.validToken(token):
        return False
    else:
        return True
    
def userId(token: str) -> int:
    if token == None:
        return False
    elif token == "":
        return False
    else:
        return tokens.getUserId(token)