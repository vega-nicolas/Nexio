from pydantic import BaseModel

class User(BaseModel):
    id: int = None
    email: str = None
    username: str = None
    password: str = None
    created_at: str = None
    enabled: bool = None
    actor: int = None
