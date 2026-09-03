import redis
import os
from dotenv import load_dotenv
load_dotenv()
def get_redis_connection():
    try:
        return redis.Redis(
            host=os.getenv("REDIS_HOST"),
            port=int(os.getenv("REDIS_PORT")),
            db=int(os.getenv("REDIS_DB"))
        )
    except (TypeError, ValueError) as e:
        print(f"环境变量配置错误: {e}")
        return None
    except redis.ConnectionError as e:
        print(f"Redis连接失败: {e}")
        return None
    except Exception as e:
        print(f"未知错误: {e}")
        return None

if __name__ == '__main__':
    conn=get_redis_connection()
    conn.get('nam222e')