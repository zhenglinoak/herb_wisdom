import os
import chromadb
import uuid

CHAT_MEMORY_DB_PATH = os.getenv("CHAT_MEMORY_DB_PATH", "//data/chat_memory_db")


def save_chat_chroma(user_name,question,answer, parent_id):
    client = chromadb.PersistentClient(path=CHAT_MEMORY_DB_PATH)

    collection = client.get_or_create_collection(
        name="chat_history",
        metadata={"hnsw:space": "cosine"}
    )
    docx = f"User: {question}\nAI: {answer}"
    metadatas = {
        "user_name": user_name,
        "parent_id": parent_id,
    }
    collection.add(
        ids=str(uuid.uuid4()),
        documents=docx,
        metadatas=metadatas
    )

def query_chroma(question,id,name):
    client = chromadb.PersistentClient(path=CHAT_MEMORY_DB_PATH)

    collection = client.get_or_create_collection(
        name="chat_history",
        metadata={"hnsw:space": "cosine"}
    )
    re=collection.query(
        query_texts=[question],
        n_results=3,  # 只取最相关的3条作为上下文
        where={ "$and":[{"parent_id":id},{"user_name":name}] },
    )
    return re['documents']
if __name__ == '__main__':
    q=("我叫啥？")
    chrome_re = query_chroma(q,132 ,"zz")
    # 获取最近几条对话（短期记忆）
    print(chrome_re)
    # 格式化记忆内容