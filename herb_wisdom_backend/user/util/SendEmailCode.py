import os
import random
from email.mime.text import MIMEText
from dotenv import load_dotenv
import smtplib

# 发送邮箱验证码的函数
def send_email_code(email:str):
    load_dotenv()
    # 生成四位数的验证码
    code=''
    for _ in range(4):
        code+=str(random.randint(0,9))

    # 配置邮箱信息
    origin_email=os.getenv("SEND_EMAIL")
    origin_password=os.getenv("SEND_PASSWORD")
    subject="验证码来喽"
    content=f"您的验证码是{code}，请在5分钟内输入"

    # 创建邮件对象
    msg=MIMEText(content,'plain','utf-8')
    msg['From']=origin_email
    msg['To']=email
    msg['Subject']=subject

    # 发送邮件
    try:
        with smtplib.SMTP_SSL("smtp.qq.com",465) as smtp:
            smtp.login(origin_email,origin_password)
            smtp.sendmail(origin_email,email,msg.as_string())
        return code
    except Exception as e:
        print(f"发送邮件失败：{e}")
        return ''
# re=send_email_code("3312299408@qq.com")
# print(f"邮箱验证码：{re}")
