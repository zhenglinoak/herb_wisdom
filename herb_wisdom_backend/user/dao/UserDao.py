from common import MySQLUtil
from pymysql import MySQLError
from user.entity.RegisterEntity import RegisterUser
# 根据邮箱查询用户
def get_user_by_email(email:str):
    with MySQLUtil.get_mysql_connection() as conn:
        with conn.cursor() as cursor:
            sql="select * from user where email=%s"
            cursor.execute(sql,[email,])
            return cursor.fetchall()

# 根据用户名查询用户
def get_user_by_name(user_name:str):
    with MySQLUtil.get_mysql_connection() as conn:
        with conn.cursor() as cursor:
            sql="select * from user where user_name=%s"
            cursor.execute(sql,[user_name,])
            return cursor.fetchall()

# 根据用户名或邮箱查询用户
def get_user_by_name_or_email(account:str):
    with MySQLUtil.get_mysql_connection() as conn:
        with conn.cursor() as cursor:
            sql="select * from user where user_name=%s or email=%s"
            cursor.execute(sql,[account,account])
            return cursor.fetchall()



# 注册用户
def register(registerUser):
    try:
        with MySQLUtil.get_mysql_connection() as conn:
            with conn.cursor() as cursor:
                sql="insert into user (user_name,password,email) values (%s,%s,%s)"
                cursor.execute(sql,[registerUser.user_name,registerUser.password,registerUser.email])
                conn.commit()
                return True
    except MySQLError as e:
        print(f"注册错误：{e}")
        conn.rollback()
        return False

def update_avatar(n, avatar_url):
    try:
        with MySQLUtil.get_mysql_connection() as conn:
            with conn.cursor() as cursor:
                sql="update user set avatar_url=%s where user_name=%s"
                cursor.execute(sql,[avatar_url,n])
                conn.commit()
                return True
    except MySQLError as e:
        print(f"更新用户头像错误：{e}")
        conn.rollback()
        return False

if __name__ == '__main__':
    # user=get_user_by_name("zz")
    # print("user:",user)
    # print("password:",user[0]['password'])
    # d={"user_name":"cz","password":"123456","email":"zz@qq.com"}
    # print(RegisterUser(**d))
    # print(register(RegisterUser(**d)))
    print(get_user_by_name_or_email("zz"))
