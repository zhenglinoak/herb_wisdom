import time
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, AIMessage
from ai import LoadChatModel
from chat.util.LoadTools import query_neo4j, get_weather
import  asyncio
_llm = None

def _init_components():
    global _llm
    if _llm is None:
        print("[Init] 加载ChatModel...")
        t0 = time.time()
        _llm = LoadChatModel.load_chat_model()
        print(f"[Init] ChatModel加载完成，耗时 {time.time() - t0:.2f}s")


# async def chat(q):
def chat(q):
    _init_components()
    llm = _llm
    # current_user_msg = HumanMessage(content=q)
    # messages = [current_user_msg]
    agent = create_agent(
        model=llm,
        system_prompt="""
            你是智能助手，严格遵守规则：
            【工具调用】
            1.问天气/气温/湿度/风力，必须调用get_weather，禁止记忆编造。
            2.问疾病、症状、药品、诊疗、医学概念，必须调用query_neo4j。
            【直接回复】不属于上面两类，直接自己回答，不用工具。
            【约束】最多调用1个工具；拿到工具结果要整理成自然语言，不要直接输出原始数据；调用失败如实告知，不许编造内容。
        """,
        tools=[query_neo4j, get_weather],
        debug=True,
    )

    # async for chunk in agent.astream({"messages": messages}, ):
    # async for chunk in agent.astream({"messages": messages} ):
    #     if "agent" in chunk:
    #         msg = chunk["agent"]["messages"][0]
    #         if isinstance(msg, AIMessage) and msg.content:
    #             yield msg.content
    # res = agent.invoke({"messages": messages})
    # print("-----------------")
    # print(res)

    messages = [
        {
            "role": "user",
            "content": q
        }
    ]

    for token, metadata in agent.stream(
            {"messages": messages},
            stream_mode="messages"
    ):
        if token.content:
            print(token.content, end="", flush=True)


# async  def run_test():
#     async for i in chat("糖尿病的并发症有哪些"):
#         print(i,end="", flush=True)
if __name__ == '__main__':
    # asyncio.run(run_test())
    chat("昆明天气怎么样")