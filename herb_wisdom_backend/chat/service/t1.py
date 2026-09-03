import time
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from ai import LoadChatModel
from chat.dao import HistoryDao
from chat.util import ChromaUtil
from chat.util.LoadTools import query_neo4j, get_weather
import  asyncio
def parse_chroma_recall(chroma_result) -> list[BaseMessage]:
    msgs = []
    if not chroma_result or not chroma_result[0]:
        return msgs
    for text in chroma_result[0]:
        user_part, rest = text.split("\nAI: ")
        user_content = user_part.replace("User: ", "")
        ai_content = rest.split("\n对话时间:")[0]
        msgs.append(HumanMessage(content=user_content.strip()))
        msgs.append(AIMessage(content=ai_content.strip()))
    return msgs


def parse_mysql_history(mysql_list) -> list[BaseMessage]:
    msgs = []
    for item in mysql_list:
        msgs.append(HumanMessage(
            content=item["question"],
            additional_kwargs={"create_time": item["create_time"]}
        ))
        msgs.append(AIMessage(
            content=item["answer"],
            additional_kwargs={"create_time": item["create_time"]}
        ))
    return msgs


def build_history_messages(q: str, history_id: int, d: dict) -> list[BaseMessage]:
    """
    仅封装历史记录（chroma向量召回 + mysql近期历史），不含当前用户新提问
    返回可直接喂给agent的消息对象列表
    """
    name=d.get("user_name")

    chroma_memory = ChromaUtil.query_chroma(q, history_id, name)
    mysql_memory = HistoryDao.get_recent_history(history_id)

    chroma_msgs = parse_chroma_recall(chroma_memory)
    mysql_msgs = parse_mysql_history(mysql_memory)

    # 顺序：向量召回久远记忆 → mysql完整近期历史
    full_history = [*chroma_msgs, *mysql_msgs]

    # 截断，避免上下文过长
    MAX_HISTORY = 18
    if len(full_history) > MAX_HISTORY:
        full_history = full_history[-MAX_HISTORY:]
    return full_history
if __name__ == '__main__':
    pass