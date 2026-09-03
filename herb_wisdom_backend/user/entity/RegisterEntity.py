from pydantic import BaseModel,Field

class RegisterUser(BaseModel):
    user_name: str=Field(...,title="User's username")
    password: str=Field(...,title="User's password")
    email: str=Field(...,title="User's email")