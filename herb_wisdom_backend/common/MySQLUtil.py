import pymysql
import os
from dotenv import load_dotenv
load_dotenv()
def get_mysql_connection():
    try:
        return pymysql.connect(
            host=os.getenv("MYSQL_HOST"),
            port=int(os.getenv("MYSQL_PORT")),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE"),
            charset=os.getenv("MYSQL_CHARSET"),
            cursorclass=pymysql.cursors.DictCursor
        )
    except (TypeError, ValueError) as e:
        print(f"环境变量配置错误: {e}")
        return None
    except pymysql.OperationalError as e:
        print(f"MySQL连接失败: {e}")
        return None
    except Exception as e:
        print(f"未知错误: {e}")
        return None