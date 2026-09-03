from pymysql import MySQLError

from chat.entity.SaveChatEntity import SaveChatEntity
from common import MySQLUtil
def save_chat(s: SaveChatEntity):
    sql = "INSERT INTO history(user_name, parent_id, question, answer) VALUES(%s, %s, %s, %s)"
    params = [s.user_name, s.parent_id, s.question, s.answer]

    try:
        with MySQLUtil.get_mysql_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                conn.commit()
        return cursor.lastrowid
    except MySQLError as e:
        conn.rollback()
        print(f"保存聊天记录失败, user: {s.user_name}, error: {e}")
        return False


if __name__ == '__main__':
    data={"user_name":"zz","parent_id":1,"question":"hi","answer":"Hello! How can I assist you today?"}
    r=save_chat(SaveChatEntity(**data))
    print(r)


