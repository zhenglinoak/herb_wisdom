from fastapi import APIRouter,Depends,File,UploadFile
from common.JWTDecode import auth
from user.entity.UserEntity import User
from user.entity.RegisterEntity import RegisterUser
from user.service import UserService
user_router = APIRouter()


# ============================通过账号和密码登陆============================
@user_router.post("/login")
def login(user:User):
    return UserService.login(user)

# ============================通过邮箱登陆============================
# 发送验证码
@user_router.get("/sendEmailCode")
def send_email_code(email:str):
    print("email:",email)
    return UserService.send_email_code(email)

# 验证验证码
@user_router.get("/verifyCode")
def verify_code(email:str,code:str):
    print("email:",email,"code:",code)
    return UserService.verify_email_code(email,code)


# 退出登陆
@user_router.get("/logout")
def logout(d: dict = Depends(auth)):
    return UserService.logout(d)

# 注册
@user_router.post("/register")
def register(registerUser:RegisterUser):
    return UserService.register(registerUser)

# 上传头像
@user_router.post("/upload/avatar/")
async def upload_avatar(file:UploadFile=File(...),d=Depends(auth)):
    return await UserService.upload_avatar(file,d)
