from datetime  import datetime, timedelta, timezone
from typing import Any

from dotenv import load_dotenv
from fastapi import HTTPException,status
from jose import jwt, JWTError
import os

load_dotenv()

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(seconds=int(os.getenv('ACCESS_TOKEN_EXPIRE')))
    to_encode.update({
        "exp": expire,
        "user_name":data["user_name"],
    })
    return jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm="HS256")

def decode_access_token(t: str) -> dict:
    try:
        d= jwt.decode(t, os.getenv("SECRET_KEY"))
        return d
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="token验证失败")

if __name__ == '__main__':
    # print(create_access_token({"user_name":"zz"}))
    token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJ6eiIsImV4cCI6MTc4NjU2MDUwM30.flp3H4CVRgGnC9vb1SFeXVz9bEGH67ZD6YBxQZKoFjc"
    decoded = decode_access_token(token)
    print(decoded)