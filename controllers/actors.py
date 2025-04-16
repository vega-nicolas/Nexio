from database import actors, users
from controllers import security
import re

def addInternalActor(email : str, preferred_username: str, displayName: str) -> bool:
    uri = f"https://nexio.vercel.app/users/{preferred_username}"
    inbox = f"https://nexio.vercel.app/users/{preferred_username}/inbox"
    outbox = f"https://nexio.vercel.app/users/{preferred_username}/outbox"
    publicKey, privateKey = security.genKeys()
    if validate_preferred_username(preferred_username):
        if actors.addActor(users.get_id(email), uri, preferred_username, displayName, inbox, outbox, publicKey, privateKey):
            return True
        else:
            return False
    
def addExternalActor(uri: str, preferred_username: str, displayName: str, inbox: str, outbox: str, publicKey: str) -> bool:
    if actors.addExternalActor(uri, preferred_username, displayName, inbox, outbox, publicKey):
        return True
    else:
        return False
    
def validate_preferred_username(preferred_username: str) -> bool:
    if not re.match(r'^[a-zA-Z0-9]+$', preferred_username):
        return False
    if len(preferred_username) > 30:
        return False
    return True