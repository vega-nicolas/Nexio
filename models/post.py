from pydantic import BaseModel
from datetime import datetime

class Post(BaseModel):
    id: int = None
    user_id: int = None
    preferred_username: str = None
    display_name: str = None
    text: str = None
    created_at: datetime = None
    likes: int = None
    comments: int = None
    shares: int = None