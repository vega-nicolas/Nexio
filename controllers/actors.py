from database import actors, users
from controllers import security

def addInternalActor(email : str, preferred_username: str) -> bool:
    uri = f"@{preferred_username}@nexio.vercel.app"
    inbox = f"https://nexio.vercel.app/users/{preferred_username}/inbox"
    outbox = f"https://nexio.vercel.app/users/{preferred_username}/outbox"
    publicKey, privateKey = security.genKeys()
    if actors.addActor(users.get_id(email), uri, preferred_username, inbox, outbox, publicKey, privateKey):
        return True
    else:
        return False