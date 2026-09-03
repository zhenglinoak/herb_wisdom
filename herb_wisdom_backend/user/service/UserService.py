import os.path

from user.entity.RegisterEntity import RegisterUser
from user.entity.UserEntity import User
from user.util import SendEmailCode
from user.dao import UserDao
from common import ResponseUtil
from common import RedisUtil
from common import JWTUtil
from user.util import PwdUtil
import uuid
import aiofiles
user_name=''

# 发送邮箱验证码的函数
def send_email_code(email):
    # 检查邮箱是否存在
    user = UserDao.get_user_by_email(email)
    if not user:
        return ResponseUtil.response(500, "邮箱不存在")
    global user_name
    user_name=user[0]['user_name']
    # 发送验证码
    code = SendEmailCode.send_email_code(email)
    if not code:
        return ResponseUtil.response(500, "验证码发送失败")
    # 缓存验证码 这里的时间单位是s(秒)
    with RedisUtil.get_redis_connection() as conn:
        conn.set(email, code, 300)
    return ResponseUtil.response(200, "验证码发送成功")


# 验证邮箱验证码的函数
def verify_email_code(email, code):
    # 检查验证码是否存在
    with RedisUtil.get_redis_connection() as conn:
        cached_code = conn.get(email)
        cached_code=cached_code.decode("utf-8")
        if not cached_code:
            return ResponseUtil.response(500, "验证码不存在")
        if cached_code != code:
            return ResponseUtil.response(500, "验证码错误")
        # TODO 登录成功后，返回token,并且要把token存入redis
        token=JWTUtil.create_access_token({"user_name":user_name})
        # 缓存token 这里的时间单位是s(秒)
        conn.set(user_name, token, 3600)
        return ResponseUtil.response(200, "验证码正确",{"user_name":user_name,"token":token})


def login(user):
    global user_name
    account=user.s
    password=user.password
    u =UserDao.get_user_by_name_or_email(account)
    if not u:
        return ResponseUtil.response(500, "用户名或邮箱不存在")
    r=PwdUtil.verify_password(password,u[0]['password'])
    if not r:
        return ResponseUtil.response(500, "密码错误")

    user_name=u[0]['user_name']
    token = JWTUtil.create_access_token({"user_name": user_name})
    with RedisUtil.get_redis_connection() as conn:
        conn.set(user_name, token, 3600)
    return ResponseUtil.response(200, "登录成功",{"user_name":user_name,"token":token})


def logout(d):
    n=d.get('user_name')
    with RedisUtil.get_redis_connection() as conn:
        conn.delete(n)
        return ResponseUtil.response(200, "退出成功")


def register(registerUser):
    name=registerUser.user_name
    email=registerUser.email
    registerUser.password=PwdUtil.hash_password(registerUser.password)
    user = UserDao.get_user_by_name(name)
    email=UserDao.get_user_by_email(email)
    if user:
        return ResponseUtil.response(500, "用户名已存在")
    if email:
        return ResponseUtil.response(500, "邮箱已存在")
    r=UserDao.register(registerUser)
    if r:
        return ResponseUtil.response(200, "注册成功")
    return ResponseUtil.response(500, "注册失败")



async def upload_avatar(file, d):
    n=d.get('user_name')
    file_ext=file.filename.split('.')[1].lower()
    if file_ext not in ['png','jpg','jpeg']:
        return ResponseUtil.response(500, "文件格式错误")
    # 保存文件
    new_file_name=f"{uuid.uuid4().hex}.{file_ext}"
    save_path=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "media", "avatars")
    os.makedirs(save_path, exist_ok=True)
    file_path=os.path.join(save_path,new_file_name)
    async with aiofiles.open(file_path,'wb') as f:
        content=await file.read()
        await f.write(content)
    avatar_url=f"/media/avatars/{new_file_name}"
    # 更新用户头像
    if not UserDao.update_avatar(n,avatar_url):
        return ResponseUtil.response(200, "上传失败")
    return ResponseUtil.response(200, "上传成功")


if __name__ == '__main__':
    # registerUser=RegisterUser(user_name="zz",password="123",email="3312299408@qq.com")
    # print(register(registerUser))
    # print(registerUser)
    #
    u=User(s="zz",password="123")
    print(u)
    # print(login(u))