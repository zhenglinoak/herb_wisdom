from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document

from ai import LoadChatModel, LoadChromaCon
from chat.entity.SaveChatEntity import SaveChatEntity
from chat.dao import ChatDao, HistoryDao
from common import ResponseUtil
from chat.util import ChromaUtil, RecogniseUtil, RRFUtil
from langchain_core.prompts import PromptTemplate
from chat.util import BM25Util, ReRankerUtil
from langchain_core.runnables import RunnableParallel, RunnableLambda, RunnablePassthrough


def _format_docs(documents: list[Document]) -> list[dict]:
    result = []
    for doc in documents:
        meta = doc.metadata or {}
        result.append({
            "id": doc.id or "",
            "metadata": {
                "drug_name": meta.get("drug_name", "") or "",
                "disease": meta.get("disease", "") or "",
                "source": meta.get("source", "") or "",
            },
            "page_content": doc.page_content or "",
        })
    return result


def chat(q, history_id,d):
    name=d.get('user_name')
    llm = LoadChatModel.load_chat_model()
    base_system = "你是一个智能助手，请根据提供的上下文和对话历史，准确回答用户的问题。"
    history = []

    if history_id != 0:
        chroma_memory = ChromaUtil.query_chroma(q, history_id,name)
        if chroma_memory:
            chroma_blocks = []
            for seg in chroma_memory:
                chroma_blocks.append(f"[参考片段]\n{seg}")
            chroma_memory_str = "\n--------\n".join(chroma_blocks)
        else:
            chroma_memory_str = "无相关历史记忆"

        mysql_memory = HistoryDao.get_recent_history(history_id)
        memory_lines = []
        for item in mysql_memory:
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

        memory_context = f"""【相关历史记忆（向量检索匹配，仅供参考）】
        {chroma_memory_str}
    
        【最近连续对话记录（本次会话上下文，请优先遵循）】
        {mysql_memory_str}
        """

        final_system_prompt = base_system + "\n" + memory_context
        print(final_system_prompt)
        history.append(final_system_prompt)

    is_medical = RecogniseUtil.intention_recognition(q)["is_medical"]
    if not is_medical:
        yield {"vector_docs": [], "bm25_docs": []}
        history.append(("user", q))
        for i in llm.stream(history):
            if i.content:
                yield i.content
        return

    template = """
    # Role
    You are a professional Traditional Chinese Medicine (TCM) knowledge base assistant. Your task is to answer the user's question strictly based on the provided [Reference Context] (JSON format drug data).

    # Constraints
    1. **Strictly Data-Bound**: Only extract information from the [Reference Context]. If the data does not contain the drug or disease the user is asking about, reply directly: "抱歉，当前知识库中未收录该药物或相关治疗方案。" (Sorry, the current knowledge base does not contain information on this drug or treatment). DO NOT use outside knowledge or make things up.
    2. **Precise Matching**:
       - If the user asks about a specific drug, list all diseases it treats and the corresponding usage methods found in the data.
       - If the user asks about treating a specific disease, search for entries containing that disease.
    3. **Completeness**: When describing "Usage" (用法), you MUST retain key details such as dosage (e.g., "size of a small bean", "one fen"), administration method (e.g., "take on an empty stomach", "send down with rice soup"), and dietary restrictions (e.g., "avoid green onions and garlic").
    4. **Formatting**:
       - Do not output meta-phrases like "According to the reference" or "The JSON data shows". Output the answer content directly.
       - If a drug has multiple treatment prescriptions, present them clearly using a list format.
    5. **Safety Disclaimer**: At the very end of your answer, you must append: "*注：以上信息仅供参考，具体用药请遵医嘱。*"

    # Reference Context
    {context}

    # History
    {history}

    # Question
    {question}

    # Answer
    Please answer the question in Chinese based on the rules above.
    """
    prompt = PromptTemplate(
        template=template,
        input_variables=["context", "history", "question"]
    )

    vector = LoadChromaCon.load_chroma_conn()
    vector_retriever = vector.as_retriever(search_kwargs={"k": 10})

    vector_result = vector_retriever.invoke(q)
    print(f"vector result:\n {vector_result}\n{'-' * 50}")
    bm25_result = BM25Util.bm25_retriever(vector, q)
    print(f"bm25 result:\n {bm25_result}\n{'-' * 50}")
    rrf_result = RRFUtil.rrf(vector_result, bm25_result)
    print(f"rrf result:\n {rrf_result}\n{'-' * 50}")

    yield {
        "vector_docs": _format_docs(vector_result),
        "bm25_docs": _format_docs(bm25_result),
    }

    chain = (RunnableParallel({
        "context": RunnableLambda(lambda _: rrf_result),
        "history": RunnableLambda(lambda _: history),
        "question": RunnablePassthrough(),
    })
        | RunnableLambda(ReRankerUtil.reranker)
        | prompt
        | llm
        | StrOutputParser()
    )
    for i in chain.invoke(q):
        yield i


def save_chat(save_chat_entity: SaveChatEntity):
    re = ChatDao.save_chat(save_chat_entity)
    ChromaUtil.save_chat_chroma(save_chat_entity.user_name, save_chat_entity.question, save_chat_entity.answer,
                                save_chat_entity.parent_id)
    if re:
        return ResponseUtil.response(200, "会话保存成功", re)
    else:
        return ResponseUtil.response(500, "会话保存失败")