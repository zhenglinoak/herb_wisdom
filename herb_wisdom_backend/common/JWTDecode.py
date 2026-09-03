import os
from typing import Annotated
from dotenv import load_dotenv
from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from common import RedisUtil

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
def auth(t:Annotated[str,Depends(oauth2_scheme)])->dict:
    try:
        p = jwt.decode(t, os.getenv("SECRET_KEY"), algorithms=["HS256"])
        user_name = p.get("user_name")
        if not user_name:
            raise HTTPException(status_code=401, detail="Token 载荷中缺少用户信息")

    except JWTError as e:
        # 这里会捕获到过期、签名错误、格式错误等所有情况
        raise HTTPException(status_code=401, detail=f"Token 验证失败: {str(e)}")

        # Redis 校验
    try:
        with RedisUtil.get_redis_connection() as conn:
            redis_token = conn.get(user_name)
            if not redis_token or redis_token.decode("utf-8") != t:
                raise HTTPException(status_code=401, detail="Token 已失效，请重新登录")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"认证服务内部错误: {str(e)}")

    return p
if __name__ == '__main__':
    token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJ6eiIsImV4cCI6MTc4NjY0Nzc4M30.BXtaiEUthYtUA3Iae4Jhl2JZXUyiZvJrJ0p7Xg7WwpI"
    payload=auth(token)
    print(payload)