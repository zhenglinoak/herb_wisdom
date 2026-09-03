from pydantic import BaseModel
# {"user_name":"zz","parent_id":1,"question":"hi","answer":"Hello! How can I assist you today?"}

class SaveChatEntity(BaseModel):
    user_name:str
    parent_id:int
    question:str
    answer:str

