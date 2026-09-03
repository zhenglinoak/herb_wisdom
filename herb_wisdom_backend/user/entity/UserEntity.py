from pydantic import BaseModel,Field

class User(BaseModel):
    s: str=Field(...,title="User's username or email")
    password: str=Field(...,title="User's password")