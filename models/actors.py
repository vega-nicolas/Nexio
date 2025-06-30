from pydantic import BaseModel

class Actors(BaseModel):
    id: int = None
    user_id: int = None
    uri: str = None
    avatar: str = None
    preferred_username: str = None
    inbox: str = None
    outbox: str = None
    is_local: str = None
    created_at: str = None