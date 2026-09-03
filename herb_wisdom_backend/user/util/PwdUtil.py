# 密钥加密处理
from passlib.context import CryptContext

crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    return crypt_context.hash(password)

def verify_password(plain_password, hashed_password):
    return crypt_context.verify(plain_password, hashed_password)

if __name__ == '__main__':
    # hash_pwd=hash_password("123456")
    hash_pwd="$2b$12$0RGTBJMampcZ5sVkdF6I6Odqq1r/wUBMUll82mwG8Im2wJhuRst/i"
    print(hash_pwd)
    print(verify_password("123", hash_pwd))

