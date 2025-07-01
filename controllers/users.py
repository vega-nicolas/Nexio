from database import users
import re

formatUsername = r'^[a-zA-Z0-9]+$'
formatEmail = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

def addUser(email: str, username: str, password: str) -> bool:
    if re.match(formatUsername, username.lower().replace(" ", "")) and re.match(formatEmail, email.lower().replace(" ", "")) and len(password) >= 12:
        if users.addUser(email, password) == True:
            return True
        else:
            return False

def validUser(email: str, password: str) -> bool:
    if users.validUser(email, password) == True:
        return True
    else:
        return False
    
def get_id(username: str) -> int:
    id = users.get_id(username)
    if id > 0:
        return id
    else:
        return None