from common import MySQLUtil
from pymysql import MySQLError

# 获取左边菜单
def get_menu(user_name:str):
    with MySQLUtil.get_mysql_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("select * from history where user_name=%s and parent_id=0",[user_name])
        return cursor.fetchall()

# 获取对应会话的所有消息
def get_history_content(history_id):
    with MySQLUtil.get_mysql_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("select * from history where history_id=%s or parent_id=%s", [history_id,history_id])
        return cursor.fetchall()

# 删除对应会话的所有消息
def delete_history(history_id):
    try:
        with MySQLUtil.get_mysql_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("delete from history where history_id=%s or parent_id=%s", [history_id, history_id])
            conn.commit()
            return True
    except MySQLError as e:
        conn.rollback()
        print(f"删除历史记录失败：{history_id},异常信息：{e}")
        return False

# 获取最近的消息记录
def get_recent_history(history_id:int,length:int=5):
    sql="SELECT * FROM history WHERE history_id=%s or parent_id=%s ORDER BY create_time DESC LIMIT %s"
    with MySQLUtil.get_mysql_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, [history_id, history_id, length])
        return cursor.fetchall()


def s1(r1):
    memory_lines = []
    for item in r1:
        block = (
            f"User: {item['question']}\n"
            f"AI: {item['answer']}\n"
            f"对话时间: {item['create_time']}"
        )
        memory_lines.append(block)
    if memory_lines:
        mysql_memory_str = "\n\n".join(memory_lines)
    else:
        mysql_memory_str = "暂无近期对话记录"
    return mysql_memory_str
if __name__ == '__main__':
    r=get_recent_history(84)
    print(s1(r))


